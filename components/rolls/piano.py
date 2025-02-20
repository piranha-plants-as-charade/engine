from dataclasses import dataclass

from components.rolls import Roll
from components.chord import Chord
from components.note import Note
from components.pitch import Pitch
from components.interval import Interval
from components.chord_voicer import ChordVoicer, BlockChordVoicer


@dataclass
class PianoRoll(Roll):

    def __post_init__(self):
        self.chord_voicer: ChordVoicer = BlockChordVoicer()
        return super().__post_init__()

    def add_stride_pattern(self, chord: Chord, start: int, end: int):
        for i, time in enumerate(range(start, end)):
            if i % 8 == 0:
                self.add_notes(
                    Note(
                        pitch=chord.root,
                        start=time,
                        duration=self.Duration(1 / 2),
                    ).reoctave_near_pitch(Pitch.from_str("C3"))
                )
            elif i % 8 == 4:
                self.add_notes(
                    Note(
                        pitch=chord.root + Interval.from_str("5"),
                        start=time,
                        duration=self.Duration(1 / 2),
                    ).reoctave_near_pitch(
                        list(self.get_pitches_at_time(time - self.Duration(1)))[0],
                        position="below",
                    )
                )
            elif i % 4 == 2:
                self.add_notes(
                    *[
                        Note(
                            pitch=pitch,
                            start=time,
                            duration=self.Duration(1 / 4),
                        )
                        for pitch in self.chord_voicer.voice(chord)
                    ]
                )
