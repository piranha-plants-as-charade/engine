from common.arrangement import ArrangementMetadata
from common.part import SampledPart
from common.note_collection import NoteCollection

from generation.chord_progression import ChordProgression
from generation.instruments.base import (
    SampledInstrument,
    SampledInstrumentExportConfig,
)


class Voice(SampledInstrument):

    def __init__(self, name: str):
        super().__init__(name)

    @property
    def export_config(self) -> SampledInstrumentExportConfig:
        return SampledInstrumentExportConfig(
            sample_src="piranha_plant",
        )

    def generate(
        self,
        melody: NoteCollection,
        chord_progression: ChordProgression,
        arrangement_metadata: ArrangementMetadata,
    ) -> SampledPart:
        notes = NoteCollection()
        notes.add(*melody.list())
        return SampledPart(arrangement_metadata, self, notes)
