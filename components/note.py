from typing import Literal
from dataclasses import dataclass


@dataclass
class Note:
    """
    The representation for a note in `components.Roll`.

    :param pitch: The MIDI pitch.
    :param start: The start time in terms of the associated roll's time.
    :param duration: The start duration in terms of the associated roll's time.
    """
    pitch: int
    start: int
    duration: int

    @property
    def end(self) -> int:
        return self.start + self.duration

    def reoctave_near_pitch(
        self,
        target: int,
        position: Literal["above", "below", "any"] = "any",
    ) -> "Note":
        """
        Returns a copy with the pitch shifted by some number of octaves such that it is nearest to the target pitch given the constraints.

        :param target: The target pitch.
        :param direction: The position of the new pitch relative to the target pitch.
        """
        candidates = {
            "above": target + (self.pitch - target) % 12,
            "below": target - (target - self.pitch) % 12,
        }
        candidates["any"] = (
            candidates["below"]
            if candidates["above"] - target > target - candidates["below"]
            else candidates["above"]
        )
        return Note(
            pitch=candidates[position],
            start=self.start,
            duration=self.duration,
        )
