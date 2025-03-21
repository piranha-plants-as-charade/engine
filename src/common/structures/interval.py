from dataclasses import dataclass, field
from typing import Optional

from transformers.interval import INTERVAL_TRANSFORMER


@dataclass(frozen=True)
class Interval:
    """
    TODO
    """

    value: int
    chord_degree: Optional[int] = field(default=None, compare=False)
    # TODO: add scale degree?

    @classmethod
    def from_str(
        cls,
        value: str,
        chord_degree: Optional[int] = None,
    ) -> "Interval":
        return cls(
            value=INTERVAL_TRANSFORMER.from_str(value),
            chord_degree=chord_degree,
        )

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(self.value + other.value)

    def __sub__(self, other: "Interval") -> "Interval":
        return Interval(self.value - other.value)
