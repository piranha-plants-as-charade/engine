from __future__ import annotations  # avoid circular dependency

from typing import Tuple, Dict, List

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
    def beats_per_minute(self):
        return self._beats_per_minute

    @property
    def quantization(self):
        return self._quantization

    @property
    def beats_per_measure(self):
        return self._time_signature[0]

    @property
    def beat_duration(self):
        return self._time_signature[1]

    def get_instrument(self, name: str) -> instrument.Instrument:
        assert name in self._instruments
        return self._instruments[name]

    def get_instruments(self) -> List[instrument.Instrument]:
        return list(self._instruments.values())

    def add_instrument(
        self,
        name: str,
        type: type[instrument.Instrument],
    ) -> instrument.Instrument:
        assert name not in self._instruments
        self._instruments[name] = type(parent=self, name=name)
        return self.get_instrument(name)
