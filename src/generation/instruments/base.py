from __future__ import annotations  # avoid circular dependency

import math
import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import DefaultDict, Any
from numpy.typing import NDArray
from collections import defaultdict
from midiutil.MidiFile import MIDIFile  # type: ignore

import common.roll as roll  # standard import to avoid circular dependency
from common.audio_sample import AudioSampleManager, AudioSampleManagerConfig
from common.note_collection import NoteCollection


@dataclass(frozen=True)
class MIDIInstrumentExportData:
    instrument_id: int


@dataclass(frozen=True)
class SampleInstrumentExportData:
    sample_src: str


InstrumentExportData = MIDIInstrumentExportData | SampleInstrumentExportData


class Instrument(ABC):

    def __init__(self, parent: roll.Roll, name: str):
        self._parent = parent
        self._name = name
        self._notes = NoteCollection()

    @property
    def name(self) -> str:
        return self._name

    @property
    def notes(self) -> NoteCollection:
        return self._notes

    @property
    @abstractmethod
    def export_data(self) -> InstrumentExportData:
        pass

    @abstractmethod
    def generate(self, *args: Any, **kwargs: Any):
        pass

    def generate_audio_from_samples(
        self,
        config: roll.RollExportConfig,
    ) -> NDArray[np.float32]:
        assert type(self.export_data) is SampleInstrumentExportData

        def roll_time_to_sample_time(time: float) -> int:
            m = config.sample_rate * 60 / self._parent.beats_per_minute
            m *= self._parent.beat_duration / self._parent.quantization
            return int(m * time)

        sample_manager = AudioSampleManager(
            AudioSampleManagerConfig(src=self.export_data.sample_src)
        )

        audio_as_dict: DefaultDict[int, np.float32] = defaultdict(lambda: np.float32(0))
        for note in self.notes.list():
            note_range = (
                roll_time_to_sample_time(note.start),
                roll_time_to_sample_time(note.end),
            )
            timbre = sample_manager.get_random_timbre()
            sample = sample_manager.get_sample(timbre, note.pitch)
            sample_len = len(sample.audio)
            sample_envelope = sample.timbre_properties.get_envelope(
                min(sample_len, note_range[1] - note_range[0])
            )
            for i, j in enumerate(range(*note_range)):
                if i >= sample_len:
                    break
                offset = (
                    config.num_start_padding_samples
                    + sample.timbre_properties.start_shift
                )
                audio_as_dict[j + offset] += sample.audio[i] * sample_envelope[i]

        return np.array([audio_as_dict[i] for i in range(max(audio_as_dict.keys()))])

    def add_self_to_midi_track(self, midi: MIDIFile, track: int):
        assert type(self.export_data) is MIDIInstrumentExportData

        time = 0  # start at the beginning
        channel = track
        instrument_id = self.export_data.instrument_id

        midi.addTrackName(track, time, self.name)  # type: ignore
        midi.addTempo(track, time, self._parent.beats_per_minute)  # type: ignore
        midi.addTimeSignature(  # type: ignore
            track,
            time,
            self._parent.beats_per_measure,
            math.floor(math.sqrt(self._parent.beat_duration)),
            24,
        )
        midi.addProgramChange(track, channel, time, instrument_id)  # type: ignore

        time_scale = self._parent.beat_duration / self._parent.quantization
        for note in self.notes.list():
            midi.addNote(  # type: ignore
                track,
                channel,
                note.pitch.value,
                note.start * time_scale,
                note.duration * time_scale,
                100,
            )
