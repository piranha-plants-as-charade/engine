from typing import Tuple
from midiutil.MidiFile import MIDIFile  # type: ignore
from dataclasses import dataclass

from components.pitch_set import PitchSet
from components.note import Note


@dataclass
class Roll:
    """
    The representation for a song.

    :param beats_per_minute: The beats per minute in terms of the time signature beat.
    :param quantization: The minimum unit of time (e.g. quantization = 16 means quantize by 16th notes)
    :param time_signature: The time signature of the song.
    """

    beats_per_minute: int
    quantization: int = 16
    time_signature: Tuple[int, int] = (4, 4)

    def __post_init__(self):
        self.__notes: Tuple[Note, ...] = tuple()

    def Duration(self, duration: float) -> int:
        return round(duration / self.beat_duration * self.quantization)

    def Time(self, measure: int, beat: float) -> int:
        return self.Duration((measure * self.beats_per_measure + beat))

    @property
    def beats_per_measure(self):
        return self.time_signature[0]

    @property
    def beat_duration(self):
        return self.time_signature[1]

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
        file.addTrackName(track, time, "Sample Track")  # type: ignore
        file.addTempo(track, time, self.beats_per_minute)  # type: ignore
        # TODO: add time signature

        # add some notes
        channel = 0
        volume = 100

        for note in self.notes:
            file.addNote(  # type: ignore
                track,
                channel,
                note.pitch.value,
                note.start / self.quantization * self.beat_duration,
                note.duration / self.quantization * self.beat_duration,
                volume,
            )

        return file
