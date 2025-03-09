from common.roll import Roll
from common.note_collection import NoteCollection
from common.structures.note import Note
from common.structures.pitch import Pitch

from generation.instruments.base import (
    MIDIInstrument,
    MIDIInstrumentExportConfig,
)

BASS_DRUM_PITCH = Pitch(35)


class BassDrum(MIDIInstrument):

    def __init__(self, parent: Roll, name: str):
        super().__init__(parent, name)

    @property
    def export_config(self) -> MIDIInstrumentExportConfig:
        return MIDIInstrumentExportConfig(
            instrument_id=0,
            channel=9,  # percussion must be on the 10th channel
            volume=64,
        )

    def generate(
        self,
        note_collection: NoteCollection,
    ):
        end = max([note.end for note in note_collection.list()])

        measure = 0
        while self._parent.Time(measure, 0) < end:
            time = self._parent.Time(measure, 0)
            self.notes.add(
                Note(pitch=BASS_DRUM_PITCH, start=time, duration=4),
            )
            measure += 1
