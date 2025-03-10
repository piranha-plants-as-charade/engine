import numpy as np
import numpy.typing as npt
from common.note_collection import NoteCollection
from common.structures.note import Note
from common.structures.pitch import Pitch
from common.roll import Roll
from melody_extraction.util import mode

class NoteCollectionBuilder:
    def __init__(
        self,
        parent: Roll,
        pitch_midi: npt.NDArray[np.float16],
        pitch_t: npt.NDArray[np.float64],
        onset_times: npt.NDArray[np.int32],
    ):
        self._roll = parent
        self._pitch_t = pitch_t
        self._pitch_midi = pitch_midi
        self._onset_times = onset_times

        self._dt = pitch_t[1] - pitch_t[0]

        self._units_per_beat = self._roll.quantization // self._roll.beats_per_measure
        self._frames_per_unit = (
            (1 / self._dt) * 60 / self._roll.beats_per_minute / self._units_per_beat
        )

    def _start_note(self, unit_count: int, note_value: int):
        self._note_start = unit_count
        self._note_value = note_value

    def _end_note(self, unit_count: int):
        assert self._note_start is not None

        self._notes.add(
            Note(
                pitch=Pitch(self._note_value),
                start=self._note_start,
                duration=unit_count - self._note_start,
            )
        )
        self._note_start = None

    def _step(self, unit_count: int, unit_start: int):
        # Note value of current unit.
        current_note_value = mode(
            np.array(
                self._pitch_midi[unit_start : unit_start + int(self._frames_per_unit)]
            )
        )

        # check if percussive signal is closest to this unit
        percussive_onset = False
        while (
            self._onset_idx < len(self._onset_times)
            and self._onset_times[self._onset_idx] < unit_start - self._frames_per_unit / 2
        ):
            self._onset_idx += 1

        if (
            self._onset_idx < len(self._onset_times)
            and self._onset_times[self._onset_idx] < unit_start + self._frames_per_unit / 2
        ):
            # Percussive onset detected in this unit.
            percussive_onset = True

        # End previous note.
        if self._note_start is not None and (
            percussive_onset or self._note_value != current_note_value
        ):
            self._end_note(unit_count)

        # Start new note.
        if self._note_start is None and current_note_value is not None:
            self._start_note(unit_count, current_note_value.astype(int))

    def build(self) -> NoteCollection:
        self._note_start: int | None = None
        self._note_value: int = 0
        self._onset_idx = 0

        self._notes = NoteCollection()

        nonnan = np.where(~np.isnan(self._pitch_midi))[0]
        first_pitch_idx = nonnan[0]
        last_pitch_idx = nonnan[-1]

        unit_count = 0
        for unit_start in range(first_pitch_idx, last_pitch_idx, int(self._frames_per_unit)):
            self._step(unit_count, unit_start)
            unit_count += 1

        # End the last note.
        if self._note_start is not None:
            self._end_note(unit_count)

        return self._notes
