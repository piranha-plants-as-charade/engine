from typing import FrozenSet, Set
from functools import cached_property

class PitchSet:

    def __init__(self, set: FrozenSet[int]):
        self.set = set

    @cached_property
    def unoctaved_set(self) -> Set[int]:
        return set([pitch % 12 for pitch in self.set])

    def contains(self, group: "PitchSet", ignore_octaves: bool = True) -> bool:
        if ignore_octaves:
            return self.unoctaved_set.issuperset(group.unoctaved_set)
        return self.set.issuperset(group.set)
