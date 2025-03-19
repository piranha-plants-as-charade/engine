from common.note_collection import NoteCollection
from common.structures.note import Note
from common.structures.pitch import Pitch

from generation.chord_progression import ChordProgression

from instruments.base import (
    MIDIInstrument,
    MIDIInstrumentExportConfig,
)

from export.arrangement import ArrangementMetadata
from export.part import MIDIPart


BASS_DRUM_PITCH = Pitch(35)


class BassDrum(MIDIInstrument):

    def __init__(self, name: str):
        super().__init__(name)

    @property
    def export_config(self) -> MIDIInstrumentExportConfig:
        return MIDIInstrumentExportConfig(
            instrument_id=0,
            channel=9,  # percussion must be on the 10th channel
            volume=64,
        )

    def generate(
        self,
        melody: NoteCollection,
        chord_progression: ChordProgression,
        arrangement_metadata: ArrangementMetadata,
    ) -> MIDIPart:
        notes = NoteCollection()
        end = max([note.end for note in melody.list()])

        measure = 0
        while arrangement_metadata.Time(measure, 0) < end:
            time = arrangement_metadata.Time(measure, 0)
            notes.add(
                Note(pitch=BASS_DRUM_PITCH, start=time, duration=4),
            )
            measure += 1

        return MIDIPart(arrangement_metadata, self, notes)
