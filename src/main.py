import os

from env import ENV

from common.arrangement_generator import ArrangementGenerator, ArrangementExportConfig, ArrangementMetadata

from melody_extraction.melody_extractor import MelodyExtractor

from generation.chord_progression_generator import ChordProgressionGenerator
from generation.instruments.voice import Voice
from generation.instruments.piano import Piano
from generation.instruments.bass_drum import BassDrum
from generation.instruments.snare_drum import SnareDrum


async def generate(input_path: str) -> str:

    name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(ENV.OUTPUT_DIR, f"{name}.wav")

    # MVP assumptions.
    arrangement_metadata = ArrangementMetadata(
        beats_per_minute=110,
        time_signature=(4, 4),
        quantization=16,
    )

    melody_extractor = MelodyExtractor()
    melody = melody_extractor.extract_melody(arrangement_metadata, input_path)

    chord_progression_generator = ChordProgressionGenerator(
        arrangement_metadata, melody
    )
    chord_progression = chord_progression_generator.generate()

    arrangement = ArrangementGenerator(melody, chord_progression, arrangement_metadata)
    arrangement.add_instrument("Voice 1", Voice)
    arrangement.add_instrument("Piano", Piano)
    arrangement.add_instrument("Bass Drum", BassDrum)
    arrangement.add_instrument("Snare Drum", SnareDrum)

    arrangement.export(ArrangementExportConfig(output_path))

    return output_path
