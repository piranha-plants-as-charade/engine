from __future__ import annotations  # avoid circular dependency

from abc import ABC, abstractmethod
from typing import Any
from midiutil.MidiFile import MIDIFile  # type: ignore

import common.roll as roll  # standard import to avoid circular dependency
from common.note_collection import NoteCollection


class Instrument(ABC):

    def __init__(self, parent: roll.Roll, name: str):
        self._parent = parent
        self._name = name
        self._notes = NoteCollection()

    @property
    def name(self) -> str:
        return self._name

    @property
    def notes(self) -> NoteCollection:
        return self._notes

    @property
    @abstractmethod
    def midi_id(self) -> int:
        pass

    @abstractmethod
    def generate(self, *args: Any, **kwargs: Any):
        pass
