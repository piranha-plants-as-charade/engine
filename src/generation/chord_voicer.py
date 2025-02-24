from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import FrozenSet, List, Dict, Callable

from common.structures.pitch import Pitch

from generation.chord_progression import ChordProgression


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
