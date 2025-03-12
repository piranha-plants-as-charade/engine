from typing import Literal
from dataclasses import dataclass

from common.structures.pitch import Pitch


@dataclass(frozen=True)
class Note:
    """
    The representation for a note in `common.Arrangement`.

    :param pitch: The MIDI pitch.
    :param start: The start time in terms of the associated arrangement's time.
    :param duration: The start duration in terms of the associated arrangement's time.
    """

    pitch: Pitch
    start: int
    duration: int

    @property
    def end(self) -> int:
        return self.start + self.duration

    def reoctave_near_pitch(
        self,
        target: Pitch,
        position: Literal["above", "below", "any"] = "any",
    ) -> "Note":
        """
        Returns a copy with the pitch shifted by some number of octaves such that it is nearest to the target pitch given the constraints.

        :param target: The target pitch.
        :param position: The position of the new pitch relative to the target pitch.
        """
        return Note(
            pitch=self.pitch.reoctave_near_pitch(target, position),
            start=self.start,
            duration=self.duration,
        )
