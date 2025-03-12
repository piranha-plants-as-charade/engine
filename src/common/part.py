from __future__ import annotations

import math
from midiutil.MidiFile import MIDIFile  # type: ignore

import common.roll as roll
from common.note_collection import NoteCollection
from common.audio_data import AudioData
from common.audio_sample import (
    AudioSample,
    AudioSampleManager,
    AudioSampleManagerConfig,
)

from generation.instruments.base import Instrument, MIDIInstrument, SampledInstrument


class Part:

    def __init__(
        self,
        roll: roll.RollConfig,
        instrument: Instrument,
        notes: NoteCollection,
    ):
        self._roll_config = roll
        self._instrument = instrument
        self._notes = notes

    @property
    def notes(self):
        return self._notes


class MIDIPart(Part):

    def __init__(
        self,
        roll_config: roll.RollConfig,
        instrument: MIDIInstrument,
        notes: NoteCollection,
    ):
        super().__init__(roll_config, instrument, notes)

    def add_notes_to_track(self, midi: MIDIFile, track: int):
        assert isinstance(self._instrument, MIDIInstrument)

        time = 0  # start at the beginning
        channel = self._instrument.export_config.channel
        instrument_id = self._instrument.export_config.instrument_id
        volume = self._instrument.export_config.volume

        midi.addTrackName(track, time, self._instrument.name)  # type: ignore
        midi.addTempo(track, time, self._roll_config.beats_per_minute)  # type: ignore
        midi.addTimeSignature(  # type: ignore
            track,
            time,
            self._roll_config.beats_per_measure,
            int(math.sqrt(self._roll_config.beat_duration)),
            24,
        )
        midi.addProgramChange(track, channel, time, instrument_id)  # type: ignore

        time_scale = self._roll_config.beat_duration / self._roll_config.quantization
        for note in self.notes.list():
            midi.addNote(  # type: ignore
                track,
                channel,
                note.pitch.value,
                note.start * time_scale,
                note.duration * time_scale,
                volume,
            )


class SampledPart(Part):

    def __init__(
        self,
        roll_config: roll.RollConfig,
        instrument: SampledInstrument,
        notes: NoteCollection,
    ):
        super().__init__(roll_config, instrument, notes)

    def get_audio_data(self, config: roll.RollExportConfig) -> AudioData:
        assert isinstance(self._instrument, SampledInstrument)

        def to_sample_time(time: float) -> int:
            m = config.sample_rate * 60 / self._roll_config.beats_per_minute
            m *= self._roll_config.beat_duration / self._roll_config.quantization
            return int(m * time)

        def get_shift_size(sample: AudioSample) -> int:
            return config.start_padding_size + sample.timbre_properties.start_shift

        sample_manager = AudioSampleManager(
            AudioSampleManagerConfig(src=self._instrument.export_config.sample_src)
        )

        audio_data = AudioData()
        for note in self.notes.list():
            timbre = sample_manager.get_random_timbre()
            sample = sample_manager.get_sample(timbre, note.pitch)
            note_len = min(len(sample.audio.array), to_sample_time(note.duration))
            start_time = to_sample_time(note.start) + get_shift_size(sample)
            note_range = (start_time, start_time + note_len)

            audio_data.add_range(
                note_range,
                sample.audio.slice(0, note_len).array
                * sample.timbre_properties.get_envelope(note_len),
            )

        return audio_data
