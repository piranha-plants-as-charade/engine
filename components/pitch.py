from typing import Literal, Optional
from dataclasses import dataclass

from components.interval import Interval
from transformers.pitch import PITCH_TRANSFORMER


@dataclass(frozen=True)
class Pitch:
    """
    TODO
    """

    value: int
    chord_tone: Optional[int] = None

    @classmethod
    def from_str(
        cls,
        value: str,
        chord_tone: Optional[int] = None,
    ) -> "Pitch":
        return cls(
            value=PITCH_TRANSFORMER.from_str(value),
            chord_tone=chord_tone,
        )

    def __add__(self, val: Interval) -> "Pitch":
        return Pitch(self.value + val.value)  # discard `chord_tone`

    def __sub__(self, val: Interval) -> "Pitch":
        return Pitch(self.value - val.value)  # discard `chord_tone`

    def reoctave_near_pitch(
        self,
        target: "Pitch",
        position: Literal["above", "below", "any"] = "any",
    ) -> "Pitch":
        """
        Returns a copy shifted by some number of octaves such that it is nearest to the target pitch given the constraints.

        :param target: The target pitch.
        :param direction: The position of the new pitch relative to the target pitch.
        """
        candidates = {
            "above": target.value + (self.value - target.value) % 12,
            "below": target.value - (target.value - self.value) % 12,
        }
        candidates["any"] = (
            candidates["below"]
            if candidates["above"] - target.value > target.value - candidates["below"]
            else candidates["above"]
        )
        return Pitch(candidates[position], chord_tone=self.chord_tone)
