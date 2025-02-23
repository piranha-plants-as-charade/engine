from __future__ import annotations  # avoid circular dependency

import math
from abc import ABC, abstractmethod
from typing import FrozenSet, List, Any
from midiutil.MidiFile import MIDIFile  # type: ignore

from common.pitch import Pitch
from common.note import Note

import generation.roll as roll  # standard import to avoid circular dependency


class Instrument(ABC):

    def __init__(self, parent: roll.Roll, name: str):
        self._parent = parent
        self._name = name
        self._notes: List[Note] = list()

    @property
    def notes(self) -> List[Note]:
        return self._notes

    def add_notes(self, *notes: Note):
        """
        Adds notes to the roll.

        :param notes: A single note or a list of notes.
        """
        self.notes.extend(notes)

    def get_pitches_at_time(self, time: int) -> FrozenSet[Pitch]:
        """
        Retrieves the existing pitches that cross the given time. Pitches that end at `time` are not retrieved.
        """
        pitches = [note.pitch for note in self.notes if note.start <= time < note.end]
        return frozenset(pitches)

    @abstractmethod
    def generate(self, *args: Any, **kwargs: Any):
        pass

    # TODO: replace with something better
    def to_midi(self) -> MIDIFile:
        file = MIDIFile(
            numTracks=1,
            ticks_per_quarternote=self._parent.quantization,
        )
        track = 0  # the only track

        time = 0  # start at the beginning
        file.addTrackName(track, time, "Sample Track")  # type: ignore
        file.addTempo(track, time, self._parent.beats_per_minute)  # type: ignore
        file.addTimeSignature(  # type: ignore
            track,
            time,
            self._parent.beats_per_measure,
            math.floor(math.sqrt(self._parent.beat_duration)),
            24,
        )
        # TODO: add time signature

        # add some notes
        channel = 0
        volume = 100
        time_scale = self._parent.beat_duration / self._parent.quantization

        for note in self.notes:
            file.addNote(  # type: ignore
                track,
                channel,
                note.pitch.value,
                note.start * time_scale,
                note.duration * time_scale,
                volume,
            )

        return file
