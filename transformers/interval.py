import re
from functools import cache


class IntervalTransformer:
    def __init__(self):
        major_scale_steps = "WWHWWW"
        self.major_scale_intervals = {1: 0}
        for i, step in enumerate(major_scale_steps):
            step = 2 if step == "W" else 1
            self.major_scale_intervals[i + 2] = self.major_scale_intervals[i + 1] + step

    @cache
    def from_str(self, input: str) -> int:
        regex = r"^([#b]*)(\d+)$"  # structure: accidental (optional), size
        match = re.search(regex, input)
        assert match is not None
        accidental, size = match.group(1), int(match.group(2))
        assert size > 0

        accidental_offset = accidental.count("#") - accidental.count("b")
        octave = (size - 1) // 7
        remainder = self.major_scale_intervals[(size - 1) % 7 + 1]
        return remainder + octave * 12 + accidental_offset


INTERVAL_TRANSFORMER = IntervalTransformer()

Interval = INTERVAL_TRANSFORMER.from_str
