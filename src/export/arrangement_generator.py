from __future__ import annotations

from typing import Dict, Type

from common.note_collection import NoteCollection

from generation.chord_progression import ChordProgression

import instruments.base as instrument

from export.arrangement import Arrangement, ArrangementMetadata


class ArrangementGenerator:

    def __init__(
        self,
        melody: NoteCollection,
        chord_progression: ChordProgression,
        metadata: ArrangementMetadata,
    ):
        self._melody = melody
        self._chord_progression = chord_progression
        self._metadata = metadata
        self._instruments: Dict[str, instrument.Instrument] = dict()

    @property
    def metadata(self) -> ArrangementMetadata:
        return self._metadata

    @property
    def melody(self):
        return self._melody

    @property
    def chord_progression(self):
        return self._chord_progression

    def add_instrument(
        self,
        name: str,
        instrument_cls: Type[instrument.Instrument],
    ):
        assert name not in self._instruments
        self._instruments[name] = instrument_cls(name=name)

    def generate(self) -> Arrangement:
        parts = [
            ins.generate(self.melody, self.chord_progression, self.metadata)
            for ins in self._instruments.values()
        ]
        return Arrangement(self.metadata, parts)
