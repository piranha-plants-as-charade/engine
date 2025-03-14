from abc import ABC, abstractmethod
from generation.chord_progression import ChordProgression


class ChordProgressionGenerator(ABC):

    @abstractmethod
    def generate(self) -> ChordProgression:
        pass
