from common.roll import Roll, RollConfig
from common.note_collection import NoteCollection
from common.structures.note import Note
from common.structures.chord import Chord, ChordQuality
from common.structures.pitch import Pitch

from generation.chord_progression import ChordProgression


def get_song():
    roll = Roll(
        RollConfig(
            beats_per_minute=110,
            time_signature=(3, 4),
        )
    )

    melody = NoteCollection()
    melody.add(
        Note(Pitch.from_str("G4"), roll.Time(0, 2), roll.Duration(0.75)),
        Note(Pitch.from_str("G4"), roll.Time(0, 2.75), roll.Duration(0.25)),
        Note(Pitch.from_str("A4"), roll.Time(1, 0), roll.Duration(1)),
        Note(Pitch.from_str("G4"), roll.Time(1, 1), roll.Duration(1)),
        Note(Pitch.from_str("C5"), roll.Time(1, 2), roll.Duration(1)),
        Note(Pitch.from_str("B4"), roll.Time(2, 0), roll.Duration(1)),
        Note(Pitch.from_str("G4"), roll.Time(2, 2), roll.Duration(0.75)),
        Note(Pitch.from_str("G4"), roll.Time(2, 2.75), roll.Duration(0.25)),
        Note(Pitch.from_str("A4"), roll.Time(3, 0), roll.Duration(1)),
        Note(Pitch.from_str("G4"), roll.Time(3, 1), roll.Duration(1)),
        Note(Pitch.from_str("D5"), roll.Time(3, 2), roll.Duration(1)),
        Note(Pitch.from_str("C5"), roll.Time(4, 0), roll.Duration(1)),
        Note(Pitch.from_str("G4"), roll.Time(4, 2), roll.Duration(0.75)),
        Note(Pitch.from_str("G4"), roll.Time(4, 2.75), roll.Duration(0.25)),
        Note(Pitch.from_str("G5"), roll.Time(5, 0), roll.Duration(1)),
        Note(Pitch.from_str("E5"), roll.Time(5, 1), roll.Duration(1)),
        Note(Pitch.from_str("C5"), roll.Time(5, 2), roll.Duration(1)),
        Note(Pitch.from_str("B4"), roll.Time(6, 0), roll.Duration(1)),
        Note(Pitch.from_str("A4"), roll.Time(6, 1), roll.Duration(1)),
        Note(Pitch.from_str("F5"), roll.Time(6, 2), roll.Duration(0.75)),
        Note(Pitch.from_str("F5"), roll.Time(6, 2.75), roll.Duration(0.25)),
        Note(Pitch.from_str("E5"), roll.Time(7, 0), roll.Duration(1)),
        Note(Pitch.from_str("C5"), roll.Time(7, 1), roll.Duration(1)),
        Note(Pitch.from_str("D5"), roll.Time(7, 2), roll.Duration(1)),
        Note(Pitch.from_str("C5"), roll.Time(8, 0), roll.Duration(1)),
    )

    chord_progression = ChordProgression(
        start_time=roll.Time(0, 0),
        end_time=roll.Time(8, 2),
    )
    chord_progression.add_chords(
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll.Time(0, 0)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll.Time(1, 0)),
        (Chord(Pitch.from_str("D"), ChordQuality.Dom7), roll.Time(1, 2)),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), roll.Time(2, 0)),
        (Chord(Pitch.from_str("G"), ChordQuality.Dom7), roll.Time(2, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll.Time(3, 0)),
        (Chord(Pitch.from_str("G"), ChordQuality.Dom7), roll.Time(3, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll.Time(4, 0)),
        (Chord(Pitch.from_str("G"), ChordQuality.Dom7), roll.Time(4, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll.Time(5, 0)),
        (Chord(Pitch.from_str("A"), ChordQuality.Min), roll.Time(5, 1)),
        (Chord(Pitch.from_str("D"), ChordQuality.Dom7), roll.Time(5, 2)),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), roll.Time(6, 0)),
        (Chord(Pitch.from_str("G"), ChordQuality.Dom7), roll.Time(6, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll.Time(7, 0)),
        (Chord(Pitch.from_str("D"), ChordQuality.Dom7), roll.Time(7, 1)),
        (Chord(Pitch.from_str("G"), ChordQuality.Maj), roll.Time(7, 2)),
        (Chord(Pitch.from_str("C"), ChordQuality.Maj), roll.Time(8, 0)),
    )

    roll.set_melody(melody)
    roll.set_chord_progression(chord_progression)

    return roll
