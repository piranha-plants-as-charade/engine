from typing import FrozenSet

from common.note_collection import NoteCollection
from common.structures.chord import Chord
from common.structures.note import Note
from common.structures.pitch import Pitch
from common.structures.interval import Interval

from generation.chord_progression import ChordProgression

from instruments.base import (
    MIDIInstrument,
    MIDIInstrumentExportConfig,
)

from export.arrangement import ArrangementMetadata
from export.part import MIDIPart

from .chord_voicer import PianoChordVoicer


class Piano(MIDIInstrument):

    def __init__(self, name: str):
        super().__init__(name)

    @property
    def export_config(self) -> MIDIInstrumentExportConfig:
        return MIDIInstrumentExportConfig(
            instrument_id=0,  # acoustic grand
            channel=0,
            volume=90,
        )

    def generate(
        self,
        melody: NoteCollection,
        chord_progression: ChordProgression,
        arrangement_metadata: ArrangementMetadata,
    ) -> MIDIPart:
        notes = NoteCollection()
        chord_voicings = PianoChordVoicer.generate(chord_progression)
        for i, chord in enumerate(chord_progression.chords):
            self._add_stride_pattern(
                arrangement_metadata,
                notes,
                chord.chord,
                chord_voicings[i],
                chord.start_time,
                chord.end_time,
            )
        return MIDIPart(arrangement_metadata, self, notes)

    def _add_stride_pattern(
        self,
        arrangement_metadata: ArrangementMetadata,
        notes: NoteCollection,
        chord: Chord,
        chord_voicing: FrozenSet[Pitch],
        start: int,
        end: int,
    ):
        for i, time in enumerate(range(start, end)):
            if i % 8 == 0:
                notes.add(
                    Note(
                        pitch=chord.root,
                        start=time,
                        duration=arrangement_metadata.Duration(1 / 2),
                    ).reoctave_near_pitch(Pitch.from_str("C3"))
                )
            elif i % 8 == 4:
                prev_pitch_set = notes.get_pitches_at_time(
                    time - arrangement_metadata.Duration(1)
                )
                notes.add(
                    Note(
                        pitch=chord.root + Interval.from_str("5"),
                        start=time,
                        duration=arrangement_metadata.Duration(1 / 2),
                    ).reoctave_near_pitch(
                        list(prev_pitch_set)[0],
                        position="below",
                    )
                )
            elif i % 4 == 2:
                notes.add(
                    *[
                        Note(
                            pitch=pitch,
                            start=time,
                            duration=arrangement_metadata.Duration(1 / 4),
                        )
                        for pitch in chord_voicing
                    ]
                )
