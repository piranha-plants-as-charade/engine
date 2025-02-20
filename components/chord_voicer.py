from abc import ABC, abstractmethod
from typing import FrozenSet


from components.chord import Chord
from components.pitch import Pitch


class ChordVoicer(ABC):

    @abstractmethod
    def voice(self, chord: Chord) -> FrozenSet[Pitch]:
        pass


class BlockChordVoicer(ChordVoicer):

    def voice(self, chord: Chord) -> FrozenSet[Pitch]:

        # if chord.quality == ChordQuality.Dom7 and next is not None:
        #     next_pitch_set = next
        #     next_tones = {
        #         1: filter(lambda x: x[1].scale_tone == 1, next_pitch_set),
        #         3: filter(lambda x: x[1].scale_tone == 3, next_pitch_set),
        #     }
        #     print(next_tones)

        target = Pitch.from_str("C5")
        return frozenset(
            [pitch.reoctave_near_pitch(target) for pitch, _ in chord.get_pitches()]
        )
