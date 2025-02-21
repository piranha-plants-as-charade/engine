from dataclasses import dataclass
from typing import FrozenSet

from common.roll import Roll
from common.chord import Chord
from common.note import Note
from common.pitch import Pitch
from common.interval import Interval


@dataclass
class PianoRoll(Roll):

    def add_stride_pattern(
        self,
        chord: Chord,
        chord_voicing: FrozenSet[Pitch],
        start: int,
        end: int,
    ):
        for i, time in enumerate(range(start, end)):
            if i % 8 == 0:
                self.add_notes(
                    Note(
                        pitch=chord.root,
                        start=time,
                        duration=self.Duration(1 / 2),
                    ).reoctave_near_pitch(Pitch.from_str("C3"))
                )
            elif i % 8 == 4:
                self.add_notes(
                    Note(
                        pitch=chord.root + Interval.from_str("5"),
                        start=time,
                        duration=self.Duration(1 / 2),
                    ).reoctave_near_pitch(
                        list(self.get_pitches_at_time(time - self.Duration(1)))[0],
                        position="below",
                    )
                )
            elif i % 4 == 2:
                self.add_notes(
                    *[
                        Note(
                            pitch=pitch,
                            start=time,
                            duration=self.Duration(1 / 4),
                        )
                        for pitch in chord_voicing
                    ]
                )
