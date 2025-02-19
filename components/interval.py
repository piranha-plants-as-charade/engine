from dataclasses import dataclass

from transformers.interval import INTERVAL_TRANSFORMER


@dataclass(frozen=True)
class Interval:
    """
    TODO
    """

    value: int

    @classmethod
    def from_str(cls, value: str) -> "Interval":
        return cls(INTERVAL_TRANSFORMER.from_str(value))

    def __add__(self, val: "Interval") -> "Interval":
        return Interval(self.value + val.value)

    def __sub__(self, val: "Interval") -> "Interval":
        return Interval(self.value - val.value)
