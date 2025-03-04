import math
from abc import abstractmethod
from dataclasses import dataclass
from midiutil.MidiFile import MIDIFile  # type: ignore

from .base import Instrument, InstrumentExportConfig


@dataclass(frozen=True)
class MIDIInstrumentExportConfig(InstrumentExportConfig):
    instrument_id: int


class MIDIInstrument(Instrument):

    @property
    @abstractmethod
    def export_config(self) -> MIDIInstrumentExportConfig:
        pass

    def add_self_to_midi_track(self, midi: MIDIFile, track: int):
        time = 0  # start at the beginning
        channel = track
        instrument_id = self.export_config.instrument_id

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
