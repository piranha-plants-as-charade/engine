import os

from env import ENV

from common.arrangement import ArrangementExportConfig, ArrangementMetadata
from common.arrangement_generator import ArrangementGenerator

from melody_extraction.melody_extractor import MelodyExtractor

from generation.viterbi import ViterbiChordProgressionGenerator
from generation.instruments.voice import Voice
from generation.instruments.piano import Piano
from generation.instruments.bass_drum import BassDrum
from generation.instruments.snare_drum import SnareDrum
import time

async def generate(input_path: str) -> str:

    name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(ENV.OUTPUT_DIR, f"{name}.wav")

    # MVP assumptions.
    arrangement_metadata = ArrangementMetadata(
        beats_per_minute=110,
        time_signature=(4, 4),
        quantization=16,
    )

    start_time = time.time()
    melody_extractor = MelodyExtractor()
    melody = melody_extractor.extract_melody(arrangement_metadata, input_path)

    melody_time = time.time()
    print(f"Melody extraction completed in {melody_time - start_time} seconds")

    chord_progression_generator = ViterbiChordProgressionGenerator(
        arrangement_metadata, melody
    )
    chord_progression = chord_progression_generator.generate()

    chord_generator_time = time.time()
    print(f"Chord generation completed in {chord_generator_time - melody_time} seconds")

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

    arrangement_time = time.time()
    print(f"Arrangement generation completed in {arrangement_time - chord_generator_time} seconds")

    arrangement.export(ArrangementExportConfig(output_path))

    export_time = time.time()
    print(f"Export completed in {export_time - arrangement_time} seconds")

    return output_path
