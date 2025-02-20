from abc import ABC, abstractmethod
from typing import FrozenSet, List, Dict

from components.chord import Chord, ChordQuality
from components.pitch import Pitch


class ChordVoicer(ABC):

    @abstractmethod
    def voice(self, chord_progression: List[Chord]) -> List[FrozenSet[Pitch]]:
        pass


class BlockChordVoicer(ChordVoicer):

    def voice(self, chord_progression: List[Chord]) -> List[FrozenSet[Pitch]]:

        chord_voicings: Dict[int, FrozenSet[Pitch]] = dict()

        def voice_chord(idx: int, chord: Chord):

            if chord.quality == ChordQuality.Dom7:
                current_tones = {
                    pitch.chord_tone: pitch for pitch in chord.get_pitches()
                }
                next_tones = {
                    pitch.chord_tone: pitch for pitch in chord_voicings[idx + 1]
                }
                chord_voicings[idx] = frozenset(
                    [
                        current_tones[3].reoctave_near_pitch(next_tones[1]),
                        current_tones[7].reoctave_near_pitch(next_tones[3]),
                        current_tones[1].reoctave_near_pitch(next_tones[5]),
                    ]
                )
                return

            target_pitch = Pitch.from_str("D4")
            pitch_set = frozenset(
                [
                    pitch.reoctave_near_pitch(target_pitch)
                    for pitch in chord.get_pitches()
                ]
            )
            chord_voicings[idx] = pitch_set

        # voice non-dominants
        for i, chord in enumerate(chord_progression):
            if chord.quality is not ChordQuality.Dom7:
                voice_chord(i, chord)

        # voice dominants
        for i, chord in enumerate(chord_progression):
            if chord.quality is ChordQuality.Dom7:
                voice_chord(i, chord)

        return [chord_voicings[i] for i in range(len(chord_progression))]
