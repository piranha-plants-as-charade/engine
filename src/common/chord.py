from enum import Enum
from dataclasses import dataclass
from typing import Tuple, FrozenSet

from common.pitch import Pitch
from common.interval import Interval


@dataclass(frozen=True)
class ChordStructure:
    intervals: Tuple[Interval, ...]


class ChordQuality(Enum):

    Maj = ChordStructure(
        intervals=(
            Interval.from_str("1", chord_degree=1),
            Interval.from_str("3", chord_degree=3),
            Interval.from_str("5", chord_degree=5),
        )
    )
    Min = ChordStructure(
        intervals=(
            Interval.from_str("1", chord_degree=1),
            Interval.from_str("b3", chord_degree=3),
            Interval.from_str("5", chord_degree=5),
        )
    )
    Dom7 = ChordStructure(
        intervals=(
            Interval.from_str("1", chord_degree=1),
            Interval.from_str("3", chord_degree=3),
            Interval.from_str("5", chord_degree=5),
            Interval.from_str("b7", chord_degree=7),
        )
    )


@dataclass(frozen=True)
class Chord:
    """
    Represents a music chord.

    TODO: Add the bass note.

    :param root: The root note (NOT the bass note).
    :param quality: The chord quality.
    """

    root: Pitch
    quality: ChordQuality

    def get_pitches(self) -> FrozenSet[Pitch]:
        return frozenset(
            [
                Pitch((self.root + iv).value, chord_degree=iv.chord_degree)
                for iv in self.quality.value.intervals
            ]
        )

    def get_V7(self):
        return Chord(self.root + Interval.from_str("5"), ChordQuality.Dom7)
