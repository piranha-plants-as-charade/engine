from __future__ import annotations  # avoid circular dependency

import os
import librosa
import tempfile
import numpy as np
import scipy.io.wavfile as wav  # type: ignore
from dataclasses import dataclass
from typing import Tuple, Dict, List, Type, DefaultDict
from numpy.typing import NDArray
from midiutil.MidiFile import MIDIFile  # type: ignore
from collections import defaultdict

import generation.instruments.base as instrument  # standard import to avoid circular dependency


@dataclass(frozen=True)
class RollExportConfig:
    output_path: str
    sample_rate: int = 44100
    soundfont_url: str = (
        "https://github.com/musescore/MuseScore/raw/refs/heads/master/share/sound/MS%20Basic.sf3"
    )
    soundfont_path: str = "../data/soundfonts/ms_basic.sf3"


class Roll:
    """
    The representation for a song.

    :param beats_per_minute: The beats per minute in terms of the time signature beat.
    :param quantization: The minimum unit of time (e.g. quantization = 16 means quantize by 16th notes)
    :param time_signature: The time signature of the song.
    """

    def __init__(
        self,
        beats_per_minute: int,
        quantization: int = 16,
        time_signature: Tuple[int, int] = (4, 4),
    ):
        self._beats_per_minute = beats_per_minute
        self._quantization = quantization
        self._time_signature = time_signature
        self._instruments: Dict[str, instrument.Instrument] = dict()

    def Duration(self, duration: float) -> int:
        return round(duration / self.beat_duration * self.quantization)

    def Time(self, measure: int, beat: float) -> int:
        return self.Duration((measure * self.beats_per_measure + beat))

    @property
    def beats_per_minute(self) -> int:
        return self._beats_per_minute

    @property
    def quantization(self) -> int:
        return self._quantization

    @property
    def beats_per_measure(self) -> int:
        return self._time_signature[0]

    @property
    def beat_duration(self) -> int:
        return self._time_signature[1]

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

    def export(self, config: RollExportConfig):
        midi_data, sample_data = self._get_instrument_export_data(config.sample_rate)

        # Download soundfont if missing.
        if not os.path.exists(config.soundfont_path):
            os.makedirs(os.path.dirname(config.soundfont_path), exist_ok=True)
            os.system(f"curl -o {config.soundfont_path} -L {config.soundfont_url}")

        # Create temporary files.
        midi_file = tempfile.NamedTemporaryFile(suffix=".mid")
        midi_wav_file = tempfile.NamedTemporaryFile(suffix=".wav")

        # Write MIDI file.
        with open(midi_file.name, "wb") as fout:
            midi_data.writeFile(fout)  # type: ignore

        # Convert MIDI file to WAV file and load WAV file.
        os.makedirs(os.path.dirname(config.output_path), exist_ok=True)
        os.system(
            f"fluidsynth -ni {config.soundfont_path} {midi_file.name} -F {midi_wav_file.name} -r {config.sample_rate}"
        )
        output: NDArray[np.float32] = librosa.load(  # type: ignore
            midi_wav_file.name,
            sr=config.sample_rate,
            dtype=np.float32,
        )[0]

        # Add sample WAV data onto MIDI WAV data.
        for sample in sample_data:
            # FIXME: This code caps the output to the MIDI duration. It should instead be the max between the MIDI and sample durations.
            for i in range(min(len(output), len(sample))):
                output[i] += sample[i]

        # Export combined WAV data and close temporary files.
        wav.write(config.output_path, config.sample_rate, output)  # type: ignore
        midi_wav_file.close()
        midi_file.close()

    def _get_instrument_export_data(
        self,
        sample_rate: int,
    ) -> Tuple[MIDIFile, List[NDArray[np.float32]]]:
        ins_lists: DefaultDict[
            Type[instrument.InstrumentExportData],
            List[instrument.Instrument],
        ] = defaultdict(lambda: list())
        for ins in self.list_instruments():
            ins_lists[type(ins.export_data)].append(ins)

        midi_data = MIDIFile(
            numTracks=len(ins_lists[instrument.MIDIInstrumentExportData]),
            ticks_per_quarternote=self.quantization,
        )
        for track, ins in enumerate(ins_lists[instrument.MIDIInstrumentExportData]):
            ins.add_self_to_midi_track(midi_data, track)

        sample_data = [
            ins.generate_audio_from_samples(sample_rate)
            for ins in ins_lists[instrument.SampleInstrumentExportData]
        ]

        return (midi_data, sample_data)
