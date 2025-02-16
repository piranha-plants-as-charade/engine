from enum import Enum
from dataclasses import dataclass
from typing import Tuple

from transformers.interval import Interval
from components.pitch_set import PitchSet


class ChordQuality(Enum):
    @dataclass
    class Data:
        structure: Tuple[str, ...]

    Maj = Data(
        structure=("1", "3", "5"),
    )
    Min = Data(
        structure=("1", "b3", "5"),
    )
    Dim = Data(
        structure=("1", "b3", "b5"),
    )
    Dom7 = Data(
        structure=("1", "3", "5", "b7"),
    )


class Chord(PitchSet):
    """
    Represents a music chord.

    TODO: Add the bass note.

    :param root: The root note (NOT the bass note).
    :param quality: The chord quality.
    """

    def __init__(self, root: int, quality: ChordQuality):
        self.root = root
        self.quality = quality
        pitches = [self.root + Interval(iv) for iv in quality.value.structure]
        super().__init__(set=frozenset(pitches))

    def get_V7(self):
        return Chord(self.root + Interval("5"), ChordQuality.Dom7)

    def get_viidim(self):
        return Chord(self.root + Interval("7"), ChordQuality.Dim)
