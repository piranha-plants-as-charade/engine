from common.roll import Roll

from generation.instruments.base import (
    SampledInstrument,
    SampledInstrumentExportConfig,
)


class Voice(SampledInstrument):

    def __init__(self, parent: Roll, name: str):
        super().__init__(parent, name)

    @property
    def export_config(self) -> SampledInstrumentExportConfig:
        return SampledInstrumentExportConfig(
            sample_src="piranha_plant",
        )

    def generate(self):
        self.notes.add(*self._parent.melody.list())
