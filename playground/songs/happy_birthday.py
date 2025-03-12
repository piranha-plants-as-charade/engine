from common.roll import Roll, RollConfig
from common.note_collection import NoteCollection
from common.structures.note import Note
from common.structures.chord import Chord, ChordQuality
from common.structures.pitch import Pitch

from generation.chord_progression import ChordProgression


def get_song():
    roll_config = RollConfig(
        beats_per_minute=110,
        time_signature=(3, 4),
    )

    melody = NoteCollection()
    melody.add(
        Note(Pitch.from_str("G4"), roll_config.Time(0, 2), roll_config.Duration(0.75)),
        Note(
            Pitch.from_str("G4"), roll_config.Time(0, 2.75), roll_config.Duration(0.25)
        ),
        Note(Pitch.from_str("A4"), roll_config.Time(1, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("G4"), roll_config.Time(1, 1), roll_config.Duration(1)),
        Note(Pitch.from_str("C5"), roll_config.Time(1, 2), roll_config.Duration(1)),
        Note(Pitch.from_str("B4"), roll_config.Time(2, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("G4"), roll_config.Time(2, 2), roll_config.Duration(0.75)),
        Note(
            Pitch.from_str("G4"), roll_config.Time(2, 2.75), roll_config.Duration(0.25)
        ),
        Note(Pitch.from_str("A4"), roll_config.Time(3, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("G4"), roll_config.Time(3, 1), roll_config.Duration(1)),
        Note(Pitch.from_str("D5"), roll_config.Time(3, 2), roll_config.Duration(1)),
        Note(Pitch.from_str("C5"), roll_config.Time(4, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("G4"), roll_config.Time(4, 2), roll_config.Duration(0.75)),
        Note(
            Pitch.from_str("G4"), roll_config.Time(4, 2.75), roll_config.Duration(0.25)
        ),
        Note(Pitch.from_str("G5"), roll_config.Time(5, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("E5"), roll_config.Time(5, 1), roll_config.Duration(1)),
        Note(Pitch.from_str("C5"), roll_config.Time(5, 2), roll_config.Duration(1)),
        Note(Pitch.from_str("B4"), roll_config.Time(6, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("A4"), roll_config.Time(6, 1), roll_config.Duration(1)),
        Note(Pitch.from_str("F5"), roll_config.Time(6, 2), roll_config.Duration(0.75)),
        Note(
            Pitch.from_str("F5"), roll_config.Time(6, 2.75), roll_config.Duration(0.25)
        ),
        Note(Pitch.from_str("E5"), roll_config.Time(7, 0), roll_config.Duration(1)),
        Note(Pitch.from_str("C5"), roll_config.Time(7, 1), roll_config.Duration(1)),
        Note(Pitch.from_str("D5"), roll_config.Time(7, 2), roll_config.Duration(1)),
        Note(Pitch.from_str("C5"), roll_config.Time(8, 0), roll_config.Duration(1)),
    )

    chord_progression = ChordProgression(
        start_time=roll_config.Time(0, 0),
        end_time=roll_config.Time(8, 2),
    )
    chord_progression.add_chords(
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll_config.Time(0, 0)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll_config.Time(1, 0)),
        (Chord(Pitch.from_str("D"), ChordQuality.Dom7), roll_config.Time(1, 2)),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), roll_config.Time(2, 0)),
        (Chord(Pitch.from_str("G"), ChordQuality.Dom7), roll_config.Time(2, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll_config.Time(3, 0)),
        (Chord(Pitch.from_str("G"), ChordQuality.Dom7), roll_config.Time(3, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll_config.Time(4, 0)),
        (Chord(Pitch.from_str("G"), ChordQuality.Dom7), roll_config.Time(4, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll_config.Time(5, 0)),
        (Chord(Pitch.from_str("A"), ChordQuality.Min), roll_config.Time(5, 1)),
        (Chord(Pitch.from_str("D"), ChordQuality.Dom7), roll_config.Time(5, 2)),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), roll_config.Time(6, 0)),
        (Chord(Pitch.from_str("G"), ChordQuality.Dom7), roll_config.Time(6, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll_config.Time(7, 0)),
        (Chord(Pitch.from_str("D"), ChordQuality.Dom7), roll_config.Time(7, 1)),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), roll_config.Time(7, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll_config.Time(8, 0)),
    )

    return Roll(melody, chord_progression, roll_config)
