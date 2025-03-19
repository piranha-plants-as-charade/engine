from typing import FrozenSet, List

from common.structures.chord import ChordQuality
from common.structures.pitch import Pitch

from instruments.chord_voicer import (
    ChordVoicer,
    ChordInChordProgression,
    ChordVoicerMemo,
    ChordVoicerInstruction,
)


class PianoChordVoicer(ChordVoicer):

    @classmethod
    def _is_default_chord(cls, chord: ChordInChordProgression) -> bool:
        return not cls._is_resolvable_dominant_chord(chord)

    @classmethod
    def _voice_default_chord(
        cls,
        memo: ChordVoicerMemo,
        chord: ChordInChordProgression,
    ) -> FrozenSet[Pitch]:
        target_pitch = Pitch.from_str("D4")
        return frozenset(
            [
                pitch.reoctave_near_pitch(target_pitch)
                for pitch in chord.chord.get_pitches()
            ]
        )

    @classmethod
    def _is_resolvable_dominant_chord(cls, chord: ChordInChordProgression) -> bool:
        if chord.chord.quality is not ChordQuality.Dom7:  # must be dominant chord
            return False
        if chord.index == len(chord.chord_progression) - 1:  # cannot be last chord
            return False
        return True

    @classmethod
    def _voice_resolvable_dominant_chord(
        cls,
        memo: ChordVoicerMemo,
        chord: ChordInChordProgression,
    ) -> FrozenSet[Pitch]:
        current_tones = {
            pitch.chord_degree: pitch for pitch in chord.chord.get_pitches()
        }
        next_tones = {pitch.chord_degree: pitch for pitch in memo[chord.index + 1]}
        return frozenset(
            [
                current_tones[3].reoctave_near_pitch(next_tones[1]),
                current_tones[7].reoctave_near_pitch(next_tones[3]),
                current_tones[1].reoctave_near_pitch(next_tones[5]),
            ]
        )

    @classmethod
    def get_instructions(cls) -> List[ChordVoicerInstruction]:
        return [
            ChordVoicerInstruction(
                condition=cls._is_default_chord,
                action=cls._voice_default_chord,
            ),
            ChordVoicerInstruction(
                condition=cls._is_resolvable_dominant_chord,
                action=cls._voice_resolvable_dominant_chord,
            ),
        ]
