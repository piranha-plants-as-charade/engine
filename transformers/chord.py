from enum import Enum

from transformers.interval import Interval
from transformers.pitch import Pitch
from components.pitch_collection import PitchCollection


class ChordQuality(Enum):
    Pow = ("1", "5")
    Maj = ("1", "3", "5")
    Min = ("1", "b3", "5")
    Dim = ("1", "b3", "b5")
    Aug = ("1", "b3", "b5")
    Sus2 = ("1", "2", "5")
    Sus4 = ("1", "4", "5")
    Maj6 = ("1", "3", "5", "6")
    Min6 = ("1", "b3", "5", "6")
    Maj7 = ("1", "3", "5", "7")
    Min7 = ("1", "b3", "5", "b7")
    Dom7 = ("1", "3", "5", "b7")


def Chord(root: str, quality: ChordQuality) -> PitchCollection:
    root_pitch = Pitch(root)
    pitches = [root_pitch + Interval(iv) for iv in quality.value]
    return PitchCollection(pitches=frozenset(pitches))
