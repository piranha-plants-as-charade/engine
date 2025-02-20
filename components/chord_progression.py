from dataclasses import dataclass
from typing import Dict, Tuple, List
from functools import cached_property

from components.chord import Chord


@dataclass(frozen=True)
class ChordAtTime:
    chord: Chord
    start_time: int
    end_time: int


@dataclass
class ChordProgression:

    start_time: int
    end_time: int

    def __post_init__(self):
        self.__chords: Dict[int, Chord] = dict()

    @cached_property
    def chords(self) -> List[ChordAtTime]:
        sorted_chords = sorted(self.__chords.items(), key=lambda x: x[0])
        return [
            ChordAtTime(
                chord=chord,
                start_time=start_time,
                end_time=(
                    self.end_time
                    if i == len(sorted_chords) - 1
                    else sorted_chords[i + 1][0]
                ),
            )
            for i, (start_time, chord) in enumerate(sorted_chords)
        ]

    def clear_chords_cache(self):
        try:
            del self.chords
        except:
            pass

    def add_chords(self, *chords: Tuple[Chord, int]):
        """
        TODO
        """
        for chord, time in chords:
            self.__chords[time] = chord
        self.clear_chords_cache()
