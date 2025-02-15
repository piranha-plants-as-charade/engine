from typing import Tuple
from midiutil.MidiFile import MIDIFile
from dataclasses import dataclass

from components.pitch_set import PitchSet
from components.note import Note


@dataclass
class Roll:
    """
    The representation for a song.

    :param bpm: beat = quarter note.
    :param quantization: The minimum unit of time (e.g. quantization = 16 means quantize by 16th notes)
    """

    bpm: int
    quantization: int = 16
    __notes: Tuple[Note, ...] = tuple()

    def Time(self, time: float) -> int:
        """
        Transforms the input into roll time.

        :param time: The input time with scale: 1 = whole note.
        """
        return round(time * self.quantization)

    @property
    def notes(self) -> Tuple[Note, ...]:
        return self.__notes

    def add_notes(self, *notes: Note):
        """
        Adds notes to the roll.

        :param notes: A single note or a list of notes.
        """
        self.__notes = self.__notes + notes

    def get_pitches_at_time(self, time: int) -> PitchSet:
        """
        Retrieves the existing pitches that cross the given time. Pitches that end at `time` are not retrieved.
        """
        pitches = [note.pitch for note in self.notes if note.start <= time < note.end]
        return PitchSet(set=frozenset(pitches))

    # TODO: replace with something better
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
