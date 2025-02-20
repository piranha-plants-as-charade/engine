from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import FrozenSet, List, Dict, Callable

from components.chord import Chord, ChordQuality
from components.pitch import Pitch


ChordVoicerMemo = Dict[int, FrozenSet[Pitch]]


@dataclass(frozen=True)
class ChordVoicerInstruction:
    condition: Callable[
        [int, Chord],  # index, chord
        bool,  # run action?
    ]
    action: Callable[
        [ChordVoicerMemo, int, Chord],  # (memo, index, chord)
        FrozenSet[Pitch],  # pitch set
    ]


class ChordVoicer(ABC):

    @classmethod
    @abstractmethod
    def get_instructions(
        cls,
        chord_progression: List[Chord],
    ) -> List[ChordVoicerInstruction]:
        pass

    @classmethod
    def generate(cls, chord_progression: List[Chord]) -> List[FrozenSet[Pitch]]:
        memo: ChordVoicerMemo = dict()
        for instruction in cls.get_instructions(chord_progression):
            for index, chord in enumerate(chord_progression):
                if instruction.condition(index, chord):
                    memo[index] = instruction.action(memo, index, chord)
        return [memo[i] for i in range(len(chord_progression))]


class BlockChordVoicer(ChordVoicer):

    @classmethod
    def get_instructions(
        cls,
        chord_progression: List[Chord],
    ) -> List[ChordVoicerInstruction]:

        def is_default_chord(index: int, chord: Chord) -> bool:
            return not is_resolvable_dominant_chord(index, chord)

        def voice_default_chord(
            memo: ChordVoicerMemo,
            index: int,
            chord: Chord,
        ) -> FrozenSet[Pitch]:
            target_pitch = Pitch.from_str("D4")
            return frozenset(
                [
                    pitch.reoctave_near_pitch(target_pitch)
                    for pitch in chord.get_pitches()
                ]
            )

        def is_resolvable_dominant_chord(index: int, chord: Chord) -> bool:
            if chord.quality is not ChordQuality.Dom7:  # must be dominant chord
                return False
            if index == len(chord_progression) - 1:  # cannot be last chord
                return False
            return True

        def voice_resolvable_dominant_chord(
            memo: ChordVoicerMemo,
            index: int,
            chord: Chord,
        ) -> FrozenSet[Pitch]:
            current_tones = {pitch.chord_tone: pitch for pitch in chord.get_pitches()}
            next_tones = {pitch.chord_tone: pitch for pitch in memo[index + 1]}
            return frozenset(
                [
                    current_tones[3].reoctave_near_pitch(next_tones[1]),
                    current_tones[7].reoctave_near_pitch(next_tones[3]),
                    current_tones[1].reoctave_near_pitch(next_tones[5]),
                ]
            )

        return [
            ChordVoicerInstruction(
                condition=is_default_chord,
                action=voice_default_chord,
            ),
            ChordVoicerInstruction(
                condition=is_resolvable_dominant_chord,
                action=voice_resolvable_dominant_chord,
            ),
        ]
