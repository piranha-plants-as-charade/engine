from components.roll import Roll
from components.note import Note
from transformers.pitch import Pitch
from transformers.chord import Chord, ChordQuality


roll = Roll(
    bpm=120,
    notes=(
        Note(pitch=Pitch("C5"), start=0, duration=5),
        Note(pitch=Pitch("E4"), start=1, duration=3),
        Note(pitch=Pitch("G4"), start=2, duration=1),
    ),
)

mappings = roll.get_pitches_indexed_by_time()
cmaj = Chord("C", ChordQuality.Maj)
cdom7 = Chord("C", ChordQuality.Dom7)
amin7 = Chord("A", ChordQuality.Min7)

print(
    "Mappings:",
    *[
        f"  {time}: {repr(tuple(pitches.pitches))}"
        for time, pitches in enumerate(mappings)
    ],
    sep="\n",
)

assert mappings[3].contains(mappings[0])
assert mappings[2].contains(cmaj)
assert cdom7.contains(mappings[2])
assert amin7.contains(mappings[2])

assert not mappings[2].contains(cdom7)
