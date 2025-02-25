from common.roll import Roll
from common.note_collection import NoteCollection

from generation.chord_progression import ChordProgression
from generation.instruments.base import Instrument


class Voice(Instrument):

    def __init__(self, parent: Roll, name: str):
        super().__init__(parent, name)

    @property
    def midi_id(self) -> int:
        return 54  # voice oohs

    def generate(
        self,
        note_collection: NoteCollection,
        chord_progression: ChordProgression,
    ):
        self.notes.add(*note_collection.list())
