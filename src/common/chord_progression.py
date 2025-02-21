from dataclasses import dataclass
from typing import Dict, Tuple, List
from functools import cached_property

from common.chord import Chord


@dataclass(frozen=True)
class ChordAtTime:
    chord: Chord
    start_time: int
    end_time: int


@dataclass
class ChordProgression:

    def __init__(self, start_time: int, end_time: int):
        self.__start_time = start_time
        self.__end_time = end_time
        self.__chords: Dict[int, Chord] = dict()

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

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
            assert (
                self.start_time <= time < self.end_time
            )  # time must be in chord progression time range
            self.__chords[time] = chord
        self.clear_chords_cache()
