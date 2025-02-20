from enum import Enum
from dataclasses import dataclass
from typing import Tuple, FrozenSet

from components.pitch import Pitch
from components.interval import Interval


@dataclass(frozen=True)
class ChordStructure:
    intervals: Tuple[Interval, ...]


class ChordQuality(Enum):

    Maj = ChordStructure(
        intervals=(
            Interval.from_str("1", chord_tone=1),
            Interval.from_str("3", chord_tone=3),
            Interval.from_str("5", chord_tone=5),
        )
    )
    Min = ChordStructure(
        intervals=(
            Interval.from_str("1", chord_tone=1),
            Interval.from_str("b3", chord_tone=3),
            Interval.from_str("5", chord_tone=5),
        )
    )
    Dom7 = ChordStructure(
        intervals=(
            Interval.from_str("1", chord_tone=1),
            Interval.from_str("3", chord_tone=3),
            Interval.from_str("5", chord_tone=5),
            Interval.from_str("b7", chord_tone=7),
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
                Pitch((self.root + iv).value, chord_tone=iv.chord_tone)
                for iv in self.quality.value.intervals
            ]
        )

    def get_V7(self):
        return Chord(self.root + Interval.from_str("5"), ChordQuality.Dom7)
