from dataclasses import dataclass
from typing import Dict, Tuple, List, FrozenSet
from functools import cached_property

from common.structures.chord import Chord


@dataclass(frozen=True)
class ChordAtTime:
    chord: Chord
    start_time: int
    end_time: int


class ChordProgression:

    def __init__(self, start_time: int, end_time: int):
        self._start_time = start_time
        self._end_time = end_time
        self._chords: Dict[int, Chord] = dict()

    def __len__(self):
        return len(self.chords)

    @property
    def start_time(self) -> int:
        return self._start_time

    @property
    def end_time(self) -> int:
        return self._end_time

    @cached_property
    def chords(self) -> List[ChordAtTime]:
        sorted_chords = sorted(self._chords.items(), key=lambda x: x[0])
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

    def add_chords(self, *chords: Tuple[Chord, int]):
        """
        TODO
        """
        for chord, time in chords:
            # time must be in chord progression time range
            assert (
                self.start_time <= time < self.end_time
            ), f"Chord time {time} is not in chord progression time range [{self.start_time}, {self.end_time})"
            self._chords[time] = chord
        self._clear_chords_cache()

    def get_chords_in_time_interval(
        self,
        time_interval: Tuple[int, int],
    ) -> FrozenSet[Chord]:
        # TODO: test this
        ret: List[Chord] = list()
        for chord_at_time in self.chords:
            if (
                chord_at_time.start_time < time_interval[1]
                and time_interval[0] < chord_at_time.end_time
            ):
                ret.append(chord_at_time.chord)
        return frozenset(ret)

    def _clear_chords_cache(self):
        try:
            del self.chords
        except:
            pass
