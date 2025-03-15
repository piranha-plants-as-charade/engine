from dataclasses import dataclass
from typing import ClassVar

from common.structures.chord import Chord, ChordQuality
from common.structures.pitch import Pitch


@dataclass
class ViterbiIndex:
    TOTAL_STATES: ClassVar[int] = 12 * len(ChordQuality)
    index: int = -1

    def __init__(self, index: int):
        self.index = index

    @classmethod
    def from_chord(cls, chord: Chord) -> "ViterbiIndex":
        return cls(
            (chord.root.value % 12) * len(ChordQuality)
            + list(ChordQuality).index(chord.quality)
        )

    def to_chord(self) -> Chord:
        root = self.index // len(ChordQuality)
        quality = list(ChordQuality)[self.index % len(ChordQuality)]
        return Chord(Pitch(root), quality)
