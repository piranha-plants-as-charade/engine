from typing import Tuple, List
from functools import reduce
from midiutil.MidiFile import MIDIFile

from components.pitch_set import PitchSet


class RollNote:

    def __init__(self, *, pitch: int, start: int, duration: int):
        self.pitch = pitch
        self.start = start
        self.duration = duration

    @property
    def end(self) -> int:
        return self.start + self.duration


class Roll:

    def __init__(self, *, bpm: int, quantization: int = 16):
        self.bpm = bpm
        self.quantization = quantization
        self._notes: Tuple[RollNote, ...] = tuple()

    def __len__(self) -> int:
        return reduce(lambda acc, note: max(acc, note.end), self.notes, 0)

    def Note(self, *, pitch: int, start: float, duration: float):
        return RollNote(
            pitch=pitch,
            start=round(start * self.quantization),
            duration=round(duration * self.quantization),
        )

    @property
    def notes(self) -> Tuple[Note, ...]:
        return self._notes

    def add_notes(self, notes: Tuple[Note, ...]):
        self._notes = self._notes + notes

    def get_pitches_at_time(self, time: int) -> PitchSet:
        pitches = [note.pitch for note in self.notes if note.start <= time < note.end]
        return PitchSet(frozenset(pitches))

    def get_pitches_indexed_by_time(self) -> List[PitchSet]:
        return [self.get_pitches_at_time(time) for time in range(len(self))]

    def print_pitches_indexed_by_time(self):
        print(
            *[
                f"{time}: {repr(tuple(sorted(pitches.set)))}"
                for time, pitches in enumerate(self.get_pitches_indexed_by_time())
            ],
            sep="\n",
        )

    def to_midi(self) -> MIDIFile:
        file = MIDIFile(1)  # only 1 track
        track = 0  # the only track

        time = 0  # start at the beginning
        file.addTrackName(track, time, "Sample Track")
        file.addTempo(track, time, 120)

        # add some notes
        channel = 0
        volume = 100

        for note in self.notes:
            file.addNote(
                track,
                channel,
                note.pitch,
                note.start * 4 / self.quantization,  # assuming 4/4
                note.duration * 4 / self.quantization,
                volume,
            )

        return file
