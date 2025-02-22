from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import FrozenSet, List, Dict, Callable

from common.chord import ChordQuality
from common.chord_progression import ChordProgression
from common.pitch import Pitch


ChordVoicerMemo = Dict[int, FrozenSet[Pitch]]


@dataclass(frozen=True)
class ChordInChordProgression:
    chord_progression: ChordProgression
    index: int

    def __post_init__(self):
        # index should be in chord progression range
        assert 0 <= self.index < len(self.chord_progression)

    @property
    def chord(self):
        return self.chord_progression.chords[self.index].chord


@dataclass(frozen=True)
class ChordVoicerInstruction:
    condition: Callable[
        [ChordInChordProgression],
        bool,  # run action?
    ]
    action: Callable[
        [ChordVoicerMemo, ChordInChordProgression],
        FrozenSet[Pitch],  # pitch set
    ]


class ChordVoicer(ABC):

    @classmethod
    @abstractmethod
    def get_instructions(cls) -> List[ChordVoicerInstruction]:
        pass

    @classmethod
    def generate(cls, chord_progression: ChordProgression) -> List[FrozenSet[Pitch]]:
        memo: ChordVoicerMemo = dict()
        for instruction in cls.get_instructions():
            for index in range(len(chord_progression.chords)):
                chord = ChordInChordProgression(
                    chord_progression=chord_progression,
                    index=index,
                )
                if instruction.condition(chord):
                    memo[index] = instruction.action(memo, chord)
        return [memo[i] for i in range(len(chord_progression.chords))]


class BlockChordVoicer(ChordVoicer):

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
