from common.roll import RollConfig
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
        roll_config: RollConfig,
    ) -> SampledPart:
        notes = NoteCollection()
        notes.add(*melody.list())
        return SampledPart(roll_config, self, notes)
