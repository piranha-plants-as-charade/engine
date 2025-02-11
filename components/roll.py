from pydantic import Field
from typing import Tuple, List
from functools import reduce

from lib.pydantic_addons import StrictBaseModel
from components.pitch_collection import PitchCollection
from components.note import Note


class Roll(StrictBaseModel):
    bpm: float = Field(...)
    subdivision: int = Field(16)
    notes: Tuple[Note, ...] = Field(tuple())

    def __len__(self) -> int:
        return reduce(lambda acc, note: max(acc, note.end), self.notes, 0)

    def get_pitches_at_time(self, time: int) -> PitchCollection:
        pitches = [note.pitch for note in self.notes if note.start <= time < note.end]
        return PitchCollection(pitches=frozenset(pitches))

    def get_pitches_indexed_by_time(self) -> List[PitchCollection]:
        return [self.get_pitches_at_time(time) for time in range(len(self))]
