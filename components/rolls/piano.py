from components.rolls import Roll
from components.chord import Chord
from components.note import Note
from components.pitch import Pitch
from components.interval import Interval


class PianoRoll(Roll):

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
                        list(self.get_pitches_at_time(time - self.Duration(1)).set)[0],
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
                        ).reoctave_near_pitch(Pitch.from_str("C5"))
                        for pitch in chord.get_pitches(
                            type="chord",
                            max_num_notes=3,
                        ).set
                    ]
                )
