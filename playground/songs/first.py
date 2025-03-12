from common.arrangement import ArrangementMetadata
from common.arrangement_generator import ArrangementGenerator
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
    arrangement_metadata = ArrangementMetadata(
        beats_per_minute=110,
        time_signature=(4, 4),
    )

    melody = NoteCollection()
    melody.add(
        Note(
            Pitch.from_str("C5"),
            arrangement_metadata.Time(0, 0),
            arrangement_metadata.Duration(2),
        ),
        Note(
            Pitch.from_str("C#5"),
            arrangement_metadata.Time(0, 3),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("D5"),
            arrangement_metadata.Time(1, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("F5"),
            arrangement_metadata.Time(1, 1),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("A4"),
            arrangement_metadata.Time(1, 2),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("E5"),
            arrangement_metadata.Time(1, 3),
            arrangement_metadata.Duration(0.5),
        ),
        Note(
            Pitch.from_str("C#5"),
            arrangement_metadata.Time(1, 3.5),
            arrangement_metadata.Duration(0.5),
        ),
        Note(
            Pitch.from_str("D5"),
            arrangement_metadata.Time(2, 0),
            arrangement_metadata.Duration(2),
        ),
        Note(
            Pitch.from_str("D#5"),
            arrangement_metadata.Time(2, 3),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("E5"),
            arrangement_metadata.Time(3, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("G5"),
            arrangement_metadata.Time(3, 1),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(3, 2),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("D5"),
            arrangement_metadata.Time(3, 3),
            arrangement_metadata.Duration(0.5),
        ),
        Note(
            Pitch.from_str("B4"),
            arrangement_metadata.Time(3, 3.5),
            arrangement_metadata.Duration(0.5),
        ),
        Note(
            Pitch.from_str("C5"),
            arrangement_metadata.Time(4, 0),
            arrangement_metadata.Duration(2),
        ),
    )

    chord_progression = ChordProgression(
        start_time=arrangement_metadata.Time(0, 0),
        end_time=arrangement_metadata.Time(5, 0),
    )
    chord_progression.add_chords(
        (I, arrangement_metadata.Time(0, 0)),
        (IV, arrangement_metadata.Time(1, 0)),
        (ii, arrangement_metadata.Time(2, 0)),
        (V, arrangement_metadata.Time(3, 0)),
        (I, arrangement_metadata.Time(4, 0)),
        (IV.get_V7(), arrangement_metadata.Time(0, 2)),
        (ii.get_V7(), arrangement_metadata.Time(1, 2)),
        (V.get_V7(), arrangement_metadata.Time(2, 2)),
        (I.get_V7(), arrangement_metadata.Time(3, 2)),
    )

    return ArrangementGenerator(melody, chord_progression, arrangement_metadata)
