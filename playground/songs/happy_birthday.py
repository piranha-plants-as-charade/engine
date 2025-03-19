from common.note_collection import NoteCollection
from common.structures.note import Note
from common.structures.chord import Chord, ChordQuality
from common.structures.pitch import Pitch

from generation.chord_progression import ChordProgression

from export.arrangement import ArrangementMetadata
from export.arrangement_generator import ArrangementGenerator


def get_song():
    arrangement_metadata = ArrangementMetadata(
        beats_per_minute=110,
        time_signature=(3, 4),
    )

    melody = NoteCollection()
    melody.add(
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(0, 2),
            arrangement_metadata.Duration(0.75),
        ),
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(0, 2.75),
            arrangement_metadata.Duration(0.25),
        ),
        Note(
            Pitch.from_str("A4"),
            arrangement_metadata.Time(1, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(1, 1),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("C5"),
            arrangement_metadata.Time(1, 2),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("B4"),
            arrangement_metadata.Time(2, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(2, 2),
            arrangement_metadata.Duration(0.75),
        ),
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(2, 2.75),
            arrangement_metadata.Duration(0.25),
        ),
        Note(
            Pitch.from_str("A4"),
            arrangement_metadata.Time(3, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(3, 1),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("D5"),
            arrangement_metadata.Time(3, 2),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("C5"),
            arrangement_metadata.Time(4, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(4, 2),
            arrangement_metadata.Duration(0.75),
        ),
        Note(
            Pitch.from_str("G4"),
            arrangement_metadata.Time(4, 2.75),
            arrangement_metadata.Duration(0.25),
        ),
        Note(
            Pitch.from_str("G5"),
            arrangement_metadata.Time(5, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("E5"),
            arrangement_metadata.Time(5, 1),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("C5"),
            arrangement_metadata.Time(5, 2),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("B4"),
            arrangement_metadata.Time(6, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("A4"),
            arrangement_metadata.Time(6, 1),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("F5"),
            arrangement_metadata.Time(6, 2),
            arrangement_metadata.Duration(0.75),
        ),
        Note(
            Pitch.from_str("F5"),
            arrangement_metadata.Time(6, 2.75),
            arrangement_metadata.Duration(0.25),
        ),
        Note(
            Pitch.from_str("E5"),
            arrangement_metadata.Time(7, 0),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("C5"),
            arrangement_metadata.Time(7, 1),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("D5"),
            arrangement_metadata.Time(7, 2),
            arrangement_metadata.Duration(1),
        ),
        Note(
            Pitch.from_str("C5"),
            arrangement_metadata.Time(8, 0),
            arrangement_metadata.Duration(1),
        ),
    )

    chord_progression = ChordProgression(
        start_time=arrangement_metadata.Time(0, 0),
        end_time=arrangement_metadata.Time(9, 0),
    )
    chord_progression.add_chords(
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), arrangement_metadata.Time(0, 0)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), arrangement_metadata.Time(1, 0)),
        (
            Chord(Pitch.from_str("D"), ChordQuality.Dom7),
            arrangement_metadata.Time(1, 2),
        ),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), arrangement_metadata.Time(2, 0)),
        (
            Chord(Pitch.from_str("G"), ChordQuality.Dom7),
            arrangement_metadata.Time(2, 2),
        ),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), arrangement_metadata.Time(3, 0)),
        (
            Chord(Pitch.from_str("G"), ChordQuality.Dom7),
            arrangement_metadata.Time(3, 2),
        ),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), arrangement_metadata.Time(4, 0)),
        (
            Chord(Pitch.from_str("G"), ChordQuality.Dom7),
            arrangement_metadata.Time(4, 2),
        ),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), arrangement_metadata.Time(5, 0)),
        (Chord(Pitch.from_str("A"), ChordQuality.Min), arrangement_metadata.Time(5, 1)),
        (
            Chord(Pitch.from_str("D"), ChordQuality.Dom7),
            arrangement_metadata.Time(5, 2),
        ),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), arrangement_metadata.Time(6, 0)),
        (
            Chord(Pitch.from_str("G"), ChordQuality.Dom7),
            arrangement_metadata.Time(6, 2),
        ),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), arrangement_metadata.Time(7, 0)),
        (
            Chord(Pitch.from_str("D"), ChordQuality.Dom7),
            arrangement_metadata.Time(7, 1),
        ),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), arrangement_metadata.Time(7, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), arrangement_metadata.Time(8, 0)),
    )

    return ArrangementGenerator(melody, chord_progression, arrangement_metadata)
