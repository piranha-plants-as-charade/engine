from typing import FrozenSet, Set
from dataclasses import dataclass
from functools import cached_property

from components.pitch import Pitch


# TODO: replace?
@dataclass
class PitchSet:

    set: FrozenSet[Pitch]

    @cached_property
    def unoctaved_set(self) -> Set[int]:
        return set([pitch.value % 12 for pitch in self.set])

    def contains(self, group: "PitchSet", ignore_octaves: bool = True) -> bool:
        if ignore_octaves:
            return self.unoctaved_set.issuperset(group.unoctaved_set)
        return self.set.issuperset(group.set)
