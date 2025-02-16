import re
from functools import cache
from typing import Dict

from transformers.interval import INTERVAL_TRANSFORMER


class PitchTransformer:
    def __init__(self):
        note_names = "CDEFGAB"
        self.pitch_offsets: Dict[str, int] = {}
        for i, name in enumerate(note_names):
            self.pitch_offsets[name] = INTERVAL_TRANSFORMER.major_scale_intervals[i + 1]

    @cache
    def from_str(self, input: str) -> int:
        regex = r"^([ABCDEFG])([#b]*)(\d*)$"  # structure: note, accidental (optional), octave (optional)
        match = re.search(regex, input)
        assert match is not None
        name, accidental = match.group(1), match.group(2)
        octave = (
            int(match.group(3)) if len(match.group(3)) > 0 else 0
        )  # default octave to 0 if missing

        C0_offset = 12  # C0 = 12
        accidental_offset = accidental.count("#") - accidental.count("b")
        return self.pitch_offsets[name] + octave * 12 + accidental_offset + C0_offset


PITCH_TRANSFORMER = PitchTransformer()

Pitch = PITCH_TRANSFORMER.from_str
