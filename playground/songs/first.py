from common.roll import Roll, RollConfig
from common.note_collection import NoteCollection
from common.structures.note import Note
from common.structures.chord import Chord, ChordQuality
from common.structures.pitch import Pitch
from common.structures.interval import Interval

from generation.chord_progression import ChordProgression

key = Pitch.from_str("C")

I = Chord(key, ChordQuality.Maj)
ii = Chord(key + Interval.from_str("2"), ChordQuality.Min)
IV = Chord(key + Interval.from_str("4"), ChordQuality.Maj)
V = Chord(key + Interval.from_str("5"), ChordQuality.Maj)


def get_song():
    roll_config = RollConfig(
        beats_per_minute=110,
        time_signature=(4, 4),
    )

    melody = NoteCollection()
    melody.add(
        Note(Pitch.from_str("C5"), roll_config.Time(0, 0), roll_config.Duration(2)),
        Note(Pitch.from_str("C#5"), roll_config.Time(0, 3), roll_config.Duration(1)),
        Note(Pitch.from_str("D5"), roll_config.Time(1, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("F5"), roll_config.Time(1, 1), roll_config.Duration(1)),
        Note(Pitch.from_str("A4"), roll_config.Time(1, 2), roll_config.Duration(1)),
        Note(Pitch.from_str("E5"), roll_config.Time(1, 3), roll_config.Duration(0.5)),
        Note(
            Pitch.from_str("C#5"), roll_config.Time(1, 3.5), roll_config.Duration(0.5)
        ),
        Note(Pitch.from_str("D5"), roll_config.Time(2, 0), roll_config.Duration(2)),
        Note(Pitch.from_str("D#5"), roll_config.Time(2, 3), roll_config.Duration(1)),
        Note(Pitch.from_str("E5"), roll_config.Time(3, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("G5"), roll_config.Time(3, 1), roll_config.Duration(1)),
        Note(Pitch.from_str("G4"), roll_config.Time(3, 2), roll_config.Duration(1)),
        Note(Pitch.from_str("D5"), roll_config.Time(3, 3), roll_config.Duration(0.5)),
        Note(Pitch.from_str("B4"), roll_config.Time(3, 3.5), roll_config.Duration(0.5)),
        Note(Pitch.from_str("C5"), roll_config.Time(4, 0), roll_config.Duration(2)),
    )

    chord_progression = ChordProgression(
        start_time=roll_config.Time(0, 0),
        end_time=roll_config.Time(4, 2),
    )
    chord_progression.add_chords(
        (I, roll_config.Time(0, 0)),
        (IV, roll_config.Time(1, 0)),
        (ii, roll_config.Time(2, 0)),
        (V, roll_config.Time(3, 0)),
        (I, roll_config.Time(4, 0)),
        (IV.get_V7(), roll_config.Time(0, 2)),
        (ii.get_V7(), roll_config.Time(1, 2)),
        (V.get_V7(), roll_config.Time(2, 2)),
        (I.get_V7(), roll_config.Time(3, 2)),
    )

    return Roll(melody, chord_progression, roll_config)
