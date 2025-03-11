from typing import List, FrozenSet, Tuple

from common.structures.note import Note
from common.structures.pitch import Pitch


class NoteCollection:

    def __init__(self):
        self._notes: List[Note] = list()

    def list(self):
        return self._notes

    def add(self, *notes: Note):
        self._notes.extend(notes)

    def get_pitches_at_time(self, time: int) -> FrozenSet[Pitch]:
        pitches = [note.pitch for note in self._notes if note.start <= time < note.end]
        return frozenset(pitches)

    def get_pitches_in_time_range(
        self,
        time_range: Tuple[int, int],
    ) -> FrozenSet[Pitch]:
        pitches = [
            note.pitch
            for note in self._notes
            if note.start < time_range[1] and time_range[0] < note.end
        ]
        return frozenset(pitches)
