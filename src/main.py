import os

from env import ENV

from common.roll import Roll, RollExportConfig

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
    beats_per_minute = 110
    time_signature = (4, 4)
    quantization = 16

    roll = Roll(
        beats_per_minute=beats_per_minute,
        quantization=quantization,
        time_signature=time_signature,
    )

    melody_extractor = MelodyExtractor()
    melody = melody_extractor.extract_melody(roll, input_path)

    chord_progression_generator = ChordProgressionGenerator(roll)
    chord_progression = chord_progression_generator.generate()

    roll.set_melody(melody)
    roll.set_chord_progression(chord_progression)

    roll.add_instrument("Voice 1", Voice)
    roll.add_instrument("Piano", Piano)
    roll.add_instrument("Bass Drum", BassDrum)
    roll.add_instrument("Snare Drum", SnareDrum)

    roll.generate()

    roll.export(RollExportConfig(output_path))

    return output_path
