from __future__ import annotations  # avoid circular dependency

import math
from typing import Tuple, Dict, List, Type
from midiutil.MidiFile import MIDIFile  # type: ignore

import generation.instruments.base as instrument  # standard import to avoid circular dependency


class Roll:
    """
    The representation for a song.

    :param beats_per_minute: The beats per minute in terms of the time signature beat.
    :param quantization: The minimum unit of time (e.g. quantization = 16 means quantize by 16th notes)
    :param time_signature: The time signature of the song.
    """

    def __init__(
        self,
        beats_per_minute: int,
        quantization: int = 16,
        time_signature: Tuple[int, int] = (4, 4),
    ):
        self._beats_per_minute = beats_per_minute
        self._quantization = quantization
        self._time_signature = time_signature
        self._instruments: Dict[str, instrument.Instrument] = dict()

    def Duration(self, duration: float) -> int:
        return round(duration / self.beat_duration * self.quantization)

    def Time(self, measure: int, beat: float) -> int:
        return self.Duration((measure * self.beats_per_measure + beat))

    @property
    def beats_per_minute(self) -> int:
        return self._beats_per_minute

    @property
    def quantization(self) -> int:
        return self._quantization

    @property
    def beats_per_measure(self) -> int:
        return self._time_signature[0]

    @property
    def beat_duration(self) -> int:
        return self._time_signature[1]

    def get_instrument(self, name: str) -> instrument.Instrument:
        assert name in self._instruments
        return self._instruments[name]

    def list_instruments(self) -> List[instrument.Instrument]:
        return list(self._instruments.values())

    def add_instrument(
        self,
        name: str,
        type: Type[instrument.Instrument],
    ) -> instrument.Instrument:
        assert name not in self._instruments
        self._instruments[name] = type(parent=self, name=name)
        return self.get_instrument(name)

    def to_midi(self) -> MIDIFile:

        instruments = self.list_instruments()
        midi_instruments = list(
            filter(
                lambda ins: type(ins.export_data) is instrument.MIDIInstrumentExportData,
                instruments,
            )
        )

        file = MIDIFile(
            numTracks=len(midi_instruments),
            ticks_per_quarternote=self.quantization,
        )

        for track, ins in enumerate(midi_instruments):
            assert type(ins.export_data) is instrument.MIDIInstrumentExportData
            ins_id = ins.export_data.instrument_id
            time = 0  # start at the beginning
            channel = track

            file.addTrackName(track, time, ins.name)  # type: ignore
            file.addTempo(track, time, self.beats_per_minute)  # type: ignore
            file.addTimeSignature(  # type: ignore
                track,
                time,
                self.beats_per_measure,
                math.floor(math.sqrt(self.beat_duration)),
                24,
            )
            file.addProgramChange(track, channel, time, ins_id)  # type: ignore

            time_scale = self.beat_duration / self.quantization
            for note in ins.notes.list():
                file.addNote(  # type: ignore
                    track,
                    channel,
                    note.pitch.value,
                    note.start * time_scale,
                    note.duration * time_scale,
                    100,
                )

        return file
