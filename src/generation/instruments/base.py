from __future__ import annotations  # avoid circular dependency

import math
from abc import ABC, abstractmethod
from typing import Any
from midiutil.MidiFile import MIDIFile  # type: ignore

import common.roll as roll  # standard import to avoid circular dependency
from common.note_sequence import NoteSequence


class Instrument(ABC):

    def __init__(self, parent: roll.Roll, name: str):
        self._parent = parent
        self._name = name
        self._notes = NoteSequence()

    @property
    def notes(self):
        return self._notes

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

        for note in self.notes.list():
            file.addNote(  # type: ignore
                track,
                channel,
                note.pitch.value,
                note.start * time_scale,
                note.duration * time_scale,
                volume,
            )

        return file
