from pydantic import Field, computed_field
from typing import FrozenSet, Set
from functools import cached_property

from lib.pydantic_addons import StrictBaseModel


class PitchCollection(StrictBaseModel):
    pitches: FrozenSet[int] = Field(frozenset())

    @computed_field
    @cached_property
    def unoctaved_pitches(self) -> Set[int]:
        return set([pitch % 12 for pitch in self.pitches])

    def contains(self, group: "PitchCollection", ignore_octaves: bool = True) -> bool:
        if ignore_octaves:
            return self.unoctaved_pitches.issuperset(group.unoctaved_pitches)
        return self.pitches.issuperset(group.pitches)
