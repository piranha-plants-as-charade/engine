from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import common.arrangement_generator as arrangement_generator
import common.part as part
from common.note_collection import NoteCollection

from generation.chord_progression import ChordProgression


@dataclass(frozen=True)
class InstrumentExportConfig:
    pass


class Instrument(ABC):

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    @abstractmethod
    def export_config(self) -> InstrumentExportConfig:
        pass

    @abstractmethod
    def generate(
        self,
        melody: NoteCollection,
        chord_progression: ChordProgression,
        arrangement_metadata: arrangement_generator.ArrangementMetadata,
    ) -> part.Part:
        pass


@dataclass(frozen=True)
class MIDIInstrumentExportConfig(InstrumentExportConfig):
    instrument_id: int
    channel: int
    volume: int = 96  # from 0 to 127


class MIDIInstrument(Instrument):

    @property
    @abstractmethod
    def export_config(self) -> MIDIInstrumentExportConfig:
        pass

    @abstractmethod
    def generate(
        self,
        melody: NoteCollection,
        chord_progression: ChordProgression,
        arrangement_metadata: arrangement_generator.ArrangementMetadata,
    ) -> part.MIDIPart:
        pass


@dataclass(frozen=True)
class SampledInstrumentExportConfig(InstrumentExportConfig):
    sample_src: str


class SampledInstrument(Instrument):

    @property
    @abstractmethod
    def export_config(self) -> SampledInstrumentExportConfig:
        pass

    @abstractmethod
    def generate(
        self,
        melody: NoteCollection,
        chord_progression: ChordProgression,
        arrangement_metadata: arrangement_generator.ArrangementMetadata,
    ) -> part.SampledPart:
        pass
