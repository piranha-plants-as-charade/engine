from components.rolls import Roll
from components.chord import Chord
from components.note import Note
from transformers.pitch import Pitch
from transformers.interval import Interval


class PianoRoll(Roll):

    def add_stride_pattern(self, chord: Chord, start: int, end: int):
        for i, time in enumerate(range(start, end)):
            if i % 8 == 0:
                self.add_notes(
                    Note(
                        pitch=chord.root,
                        start=time,
                        duration=self.Duration(1 / 2),
                    ).reoctave_near_pitch(Pitch("C3"))
                )
            elif i % 8 == 4:
                self.add_notes(
                    Note(
                        pitch=chord.root + Interval("5"),
                        start=time,
                        duration=self.Duration(1 / 2),
                    ).reoctave_near_pitch(
                        min(self.get_pitches_at_time(time - self.Duration(1)).set),
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
                        ).reoctave_near_pitch(Pitch("C5"))
                        for pitch in chord.set
                    ]
                )
