from enum import Enum
from dataclasses import dataclass
from typing import Tuple, FrozenSet

from common.structures.pitch import Pitch
from common.structures.interval import Interval


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

    # TODO: test this
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chord):
            return False
        return len(self.get_pitches().symmetric_difference(other.get_pitches())) == 0

    def get_pitches(self) -> FrozenSet[Pitch]:
        reference_pitch = Pitch(64)  # a frame of reference; can be any pitch
        return frozenset(
            [
                Pitch(
                    (self.root + iv).value, chord_degree=iv.chord_degree
                ).reoctave_near_pitch(reference_pitch)
                for iv in self.quality.value.intervals
            ]
        )

    def get_V7(self):
        return Chord(self.root + Interval.from_str("5"), ChordQuality.Dom7)
