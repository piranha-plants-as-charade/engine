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

    @classmethod
    def from_str(cls, s: str) -> "ChordQuality":
        if s in ["", "+"]:
            return cls.Maj
        if s in ["m", "-"]:
            return cls.Min
        if s in ["7"]:
            return cls.Dom7
        raise ValueError(f"Invalid chord quality: {s}")


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

    def get_V7(self) -> "Chord":
        return Chord(self.root + Interval.from_str("5"), ChordQuality.Dom7)
    
    def to_index(self) -> int:
        """
        Returns the Viterbi index of the chord.

        :return: The Viterbi index.
        """
        return self.root.value % 12 * len(ChordQuality) + list(ChordQuality).index(self.quality)
    
    @classmethod
    def from_index(cls, index: int) -> "Chord":
        """
        Returns a chord from its Viterbi index.

        :param index: The Viterbi index.
        :return: The chord.
        """
        root = index // 3
        quality = list(ChordQuality)[index % 3]
        return Chord(Pitch(root), quality)

    @classmethod
    def from_str(cls, s: str) -> "Chord":
        """
        Constructs a chord from a string representation.

        Examples: "C", "Gm", "F#7"

        :param s: The string representation.
        :return: The chord.
        """
        split = 1
        if len(s) > 1 and s[1] in ['b', '#']:
            split = 2

        return Chord(Pitch.from_str(s[:split]), ChordQuality.from_str(s[split:]))
    
    def __str__(self) -> str:
        root = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][self.root.value % 12]
        quality = ['Maj', 'Min', 'Dom7'][list(ChordQuality).index(self.quality)]
        return f"{root}{quality}"
