from typing import Tuple, List, Literal
from functools import reduce
from midiutil.MidiFile import MIDIFile
from dataclasses import dataclass

from components.pitch_set import PitchSet


@dataclass
class Note:
    pitch: int
    start: int
    duration: int

    @property
    def end(self) -> int:
        return self.start + self.duration

    def reoctave_near_pitch(
        self,
        target: int,
        direction: Literal["above", "below", "any"] = "any",
    ) -> "Note":
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
            pitch=candidates[direction],
            start=self.start,
            duration=self.duration,
        )


@dataclass
class Roll:

    bpm: int
    quantization: int = 16
    __notes: Tuple[Note, ...] = tuple()

    def Time(self, time: float) -> int:
        return round(time * self.quantization)

    def __len__(self) -> int:
        return reduce(lambda acc, note: max(acc, note.end), self.notes, 0)

    @property
    def notes(self) -> Tuple[Note, ...]:
        return self.__notes

    def add_notes(self, *notes: Note):
        self.__notes = self.__notes + notes

    def get_pitches_at_time(self, time: int) -> PitchSet:
        pitches = [note.pitch for note in self.notes if note.start <= time < note.end]
        return PitchSet(set=frozenset(pitches))

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
        file = MIDIFile(
            numTracks=1,
            ticks_per_quarternote=self.quantization,
        )
        track = 0  # the only track

        time = 0  # start at the beginning
        file.addTrackName(track, time, "Sample Track")
        file.addTempo(track, time, self.bpm)

        # add some notes
        channel = 0
        volume = 100

        for note in self.notes:
            file.addNote(
                track,
                channel,
                note.pitch,
                note.start / self.quantization * 4,  # assumes beat = quarter note
                note.duration / self.quantization * 4,
                volume,
            )

        return file
