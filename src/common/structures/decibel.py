from dataclasses import dataclass


@dataclass(frozen=True)
class dB:

    db: float

    @property
    def strength(self):
        return 10 ** (self.db / 20)
