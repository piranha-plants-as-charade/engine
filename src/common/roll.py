from __future__ import annotations

import os
import tempfile
import scipy.io.wavfile as wav  # type: ignore
from dataclasses import dataclass
from typing import Tuple, Dict, List, Type
from midiutil.MidiFile import MIDIFile  # type: ignore

from common.util import db_to_strength
from common.audio_data import AudioData
from common.note_collection import NoteCollection

from generation.chord_progression import ChordProgression
import generation.instruments.base as instrument


@dataclass(frozen=True)
class RollExportConfig:
    """
    TODO
    """

    output_path: str
    sample_rate: int = 44100
    start_padding: float = 0.5  # in seconds
    soundfont_url: str = (
        "https://github.com/musescore/MuseScore/raw/refs/heads/master/share/sound/MS%20Basic.sf3"
    )
    soundfont_path: str = "../data/soundfonts/ms_basic.sf3"
    midi_db: float = 11
    sample_db: float = 0

    @property
    def start_padding_size(self) -> int:
        return int(self.start_padding * self.sample_rate)


@dataclass(frozen=True)
class RollConfig:
    """
    :param beats_per_minute: The beats per minute in terms of the time signature beat.
    :param quantization: The minimum unit of time (e.g. quantization = 16 means quantize by 16th notes)
    :param time_signature: The time signature of the song.
    """

    beats_per_minute: int
    time_signature: Tuple[int, int]
    quantization: int = 16

    @property
    def beats_per_measure(self) -> int:
        return self.time_signature[0]

    @property
    def beat_duration(self) -> int:
        return self.time_signature[1]


class Roll:

    def __init__(self, config: RollConfig):
        self._config = config
        self._instruments: Dict[str, instrument.Instrument] = dict()
        self._melody: NoteCollection = NoteCollection()
        self._chord_progression: ChordProgression = ChordProgression(0, 0)

    def Duration(self, duration: float) -> int:
        return round(duration / self.beat_duration * self.quantization)

    def Time(self, measure: int, beat: float) -> int:
        return self.Duration((measure * self.beats_per_measure + beat))

    @property
    def beats_per_minute(self) -> int:
        return self._config.beats_per_minute

    @property
    def quantization(self) -> int:
        return self._config.quantization

    @property
    def beats_per_measure(self) -> int:
        return self._config.time_signature[0]

    @property
    def beat_duration(self) -> int:
        return self._config.time_signature[1]

    @property
    def melody(self):
        return self._melody

    def set_melody(self, melody: NoteCollection):
        self._melody = melody

    @property
    def chord_progression(self):
        return self._chord_progression

    def set_chord_progression(self, chord_progression: ChordProgression):
        self._chord_progression = chord_progression

    def get_instrument(self, name: str) -> instrument.Instrument:
        assert name in self._instruments
        return self._instruments[name]

    def list_instruments(self) -> List[instrument.Instrument]:
        return list(self._instruments.values())

    def add_instrument(
        self,
        name: str,
        type: Type[instrument.Instrument],
    ) -> instrument.Instrument:
        assert name not in self._instruments
        self._instruments[name] = type(parent=self, name=name)
        return self.get_instrument(name)

    def generate(self):
        assert self.melody is not None and self.chord_progression is not None
        for ins in self.list_instruments():
            ins.generate()

    def export(self, config: RollExportConfig):
        midi_instruments, sampled_instruments = self._get_instruments_by_type()

        output = self._midi_to_audio_data(config, midi_instruments)

        # Add sampled instruments' WAV datas onto MIDI WAV data.
        for ins in sampled_instruments:
            array = ins.get_audio_data(config).array
            output.add_range((0, len(array)), array * db_to_strength(config.sample_db))

        # Export combined WAV data and close temporary files.
        wav.write(config.output_path, config.sample_rate, output.array)  # type: ignore

    def _get_instruments_by_type(self) -> Tuple[
        List[instrument.MIDIInstrument],
        List[instrument.SampledInstrument],
    ]:
        midi_instruments: List[instrument.MIDIInstrument] = list()
        sampled_instruments: List[instrument.SampledInstrument] = list()
        for ins in self.list_instruments():
            if isinstance(ins, instrument.MIDIInstrument):
                midi_instruments.append(ins)
            elif isinstance(ins, instrument.SampledInstrument):
                sampled_instruments.append(ins)

        return (midi_instruments, sampled_instruments)

    def _midi_to_audio_data(
        self,
        config: RollExportConfig,
        instruments: List[instrument.MIDIInstrument],
    ) -> AudioData:
        if len(instruments) == 0:
            return AudioData()

        # Download soundfont if missing.
        if not os.path.exists(config.soundfont_path):
            os.makedirs(os.path.dirname(config.soundfont_path), exist_ok=True)
            os.system(f"curl -o {config.soundfont_path} -L {config.soundfont_url}")

        # Create temporary files.
        midi_file = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
        midi_wav_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

        # Create MIDI data.
        midi_data = MIDIFile(
            numTracks=len(instruments),
            ticks_per_quarternote=self.quantization,
        )
        for track, ins in enumerate(instruments):
            ins.add_notes_to_track(midi_data, track)

        # Write MIDI data to MIDI file.
        midi_data.writeFile(midi_file)  # type: ignore
        midi_file.flush()

        # Close files before FluidSynth call.
        midi_file.close()
        midi_wav_file.close()

        # Convert MIDI file to WAV file and load WAV file.
        os.makedirs(os.path.dirname(config.output_path), exist_ok=True)
        os.system(
            f"fluidsynth -ni {config.soundfont_path} {midi_file.name} -F {midi_wav_file.name} -r {config.sample_rate}"
        )
        output = AudioData.from_file(
            midi_wav_file.name,
            sample_rate=config.sample_rate,
            db=config.midi_db,
        )
        output.pad_start(config.start_padding_size)

        # Delete temp files.
        os.remove(midi_file.name)
        os.remove(midi_wav_file.name)

        return output
