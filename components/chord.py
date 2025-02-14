from enum import Enum

from transformers.interval import Interval
from components.pitch_set import PitchSet


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


class Chord(PitchSet):

    def __init__(self, root: int, quality: ChordQuality):
        self.root = root
        self.quality = quality
        pitches = [self.root + Interval(iv) for iv in quality.value]
        super().__init__(frozenset(pitches))
    
    def get_V7(self):
        return Chord(self.root + Interval("5"), ChordQuality.Dom7)
    
    def get_viidim(self):
        return Chord(self.root + Interval("7"), ChordQuality.Dim)
