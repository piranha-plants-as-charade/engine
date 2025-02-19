from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Literal

from components.pitch import Pitch
from components.interval import Interval
from components.pitch_set import PitchSet


class ChordQuality(Enum):
    @dataclass
    class Data:
        @dataclass
        class PriorityInterval:
            interval: str
            bass_priority: int  # smaller = more important
            chord_priority: int  # smaller = more important

        structure: Tuple[PriorityInterval, ...]

    Maj = Data(
        structure=(
            Data.PriorityInterval(interval="1", bass_priority=1, chord_priority=2),
            Data.PriorityInterval(interval="3", bass_priority=3, chord_priority=1),
            Data.PriorityInterval(interval="5", bass_priority=2, chord_priority=3),
        ),
    )
    Dom7 = Data(
        structure=(
            Data.PriorityInterval(interval="1", bass_priority=1, chord_priority=3),
            Data.PriorityInterval(interval="3", bass_priority=3, chord_priority=1),
            Data.PriorityInterval(interval="5", bass_priority=2, chord_priority=3),
            Data.PriorityInterval(interval="b7", bass_priority=3, chord_priority=2),
        ),
    )


@dataclass
class Chord:
    """
    Represents a music chord.

    TODO: Add the bass note.

    :param root: The root note (NOT the bass note).
    :param quality: The chord quality.
    """

    root: Pitch
    quality: ChordQuality

    def get_pitches(
        self,
        type: Literal["bass", "chord"] = "chord",
        max_num_notes: int = 10,
    ) -> PitchSet:
        structure = list(self.quality.value.structure)
        structure.sort(
            key=lambda iv: iv.bass_priority if type == "bass" else iv.chord_priority,
        )
        return PitchSet(
            set=frozenset(
                [
                    self.root + Interval.from_str(iv.interval)
                    for iv in structure[0:max_num_notes]
                ]
            )
        )

    def get_V7(self):
        return Chord(self.root + Interval.from_str("5"), ChordQuality.Dom7)
