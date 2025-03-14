import os

from env import ENV

from common.arrangement import ArrangementExportConfig, ArrangementMetadata
from common.arrangement_generator import ArrangementGenerator

from melody_extraction.signal import SignalMelodyExtractor

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

    melody_extractor = SignalMelodyExtractor()
    melody = melody_extractor.extract_melody(arrangement_metadata, input_path)

    chord_progression_generator = ChordProgressionGenerator(
        arrangement_metadata, melody
    )
    chord_progression = chord_progression_generator.generate()

    arrangement_generator = ArrangementGenerator(
        melody,
        chord_progression,
        arrangement_metadata,
    )
    arrangement_generator.add_instrument("Voice 1", Voice)
    arrangement_generator.add_instrument("Piano", Piano)
    arrangement_generator.add_instrument("Bass Drum", BassDrum)
    arrangement_generator.add_instrument("Snare Drum", SnareDrum)

    arrangement = arrangement_generator.generate()

    arrangement.export(ArrangementExportConfig(output_path))

    return output_path
