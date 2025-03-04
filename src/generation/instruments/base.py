from __future__ import annotations  # avoid circular dependency

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import common.roll as roll  # standard import to avoid circular dependency
from common.note_collection import NoteCollection


@dataclass(frozen=True)
class InstrumentExportConfig:
    pass


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
    def export_config(self) -> InstrumentExportConfig:
        pass

    @abstractmethod
    def generate(self, *args: Any, **kwargs: Any):
        pass
