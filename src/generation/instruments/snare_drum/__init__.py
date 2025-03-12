from common.roll import RollConfig
from common.part import MIDIPart
from common.note_collection import NoteCollection
from common.structures.note import Note
from common.structures.pitch import Pitch

from generation.chord_progression import ChordProgression
from generation.instruments.base import (
    MIDIInstrument,
    MIDIInstrumentExportConfig,
)

SNARE_DRUM_PITCH = Pitch(38)


class SnareDrum(MIDIInstrument):

    def __init__(self, name: str):
        super().__init__(name)

    @property
    def export_config(self) -> MIDIInstrumentExportConfig:
        return MIDIInstrumentExportConfig(
            instrument_id=0,
            channel=9,  # percussion must be on the 10th channel
            volume=72,
        )

    def generate(
        self,
        melody: NoteCollection,
        chord_progression: ChordProgression,
        roll_config: RollConfig,
    ) -> MIDIPart:
        notes = NoteCollection()
        end = max([note.end for note in melody.list()])

        measure = 0
        while roll_config.Time(measure, 0) < end:
            for beat in range(roll_config.beats_per_measure):
                time = roll_config.Time(measure, beat)
                notes.add(
                    Note(pitch=SNARE_DRUM_PITCH, start=time, duration=2),
                    Note(pitch=SNARE_DRUM_PITCH, start=time + 2, duration=1),
                    Note(pitch=SNARE_DRUM_PITCH, start=time + 3, duration=1),
                )
            measure += 1
        return MIDIPart(roll_config, self, notes)
