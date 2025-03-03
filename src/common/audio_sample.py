import os
import random
import librosa
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict, Any
from numpy.typing import NDArray
from dotenv import dotenv_values
from functools import cached_property

from common.structures.pitch import Pitch


@dataclass(frozen=True)
class AudioSampleManagerConfig:
    """
    :param src: The folder in which the sample file reside (i.e. `data/<src>`), with each file consisting of chromatic ascending notes of the same timbre.
    :param sample_rate: The sample rate at which to load each sample file.
    :param range: The range supported.
    :param beats_per_minute: The tempo at which each note is 1 beat.
    """

    src: str
    sample_rate: int = 44100
    volume: float = 0.175
    range: Tuple[Pitch, Pitch] = (
        Pitch.from_str("C3"),
        Pitch.from_str("G6"),
    )
    beats_per_minute: int = 60


@dataclass(frozen=True)
class AudioSampleEnvelope:
    start_shift: int = -1000
    start_sample: int = 0
    end_sample: int = 38000

    ease_in_factor: float = 0.1
    ease_out_factor: float = 0.1


@dataclass(frozen=True)
class AudioSample:
    audio: NDArray[np.float32]
    envelope: AudioSampleEnvelope

    @cached_property
    def smoothened_audio(self):
        N = len(self.audio)
        ease_in_samples = int(N * self.envelope.ease_in_factor)
        ease_out_samples = int(N * self.envelope.ease_out_factor)
        window_start = np.hamming(ease_in_samples * 2)[:ease_in_samples]
        window_end = np.hamming(ease_out_samples * 2)[ease_out_samples:]
        window_middle = np.ones(N - len(window_start) - len(window_end))
        return self.audio * np.concatenate([window_start, window_middle, window_end])


class SkipFileOnSampleLoad(Exception):
    pass


class AudioSampleManager:

    _sample_data: Dict[Tuple[str, Pitch], AudioSample] = dict()
    _timbre_data: Dict[str, AudioSampleEnvelope] = dict()

    def __init__(self, config: AudioSampleManagerConfig):
        self._config = config
        for timbre_file in os.listdir(self._samples_dir):
            try:
                self._load_file(os.path.join(self._samples_dir, timbre_file))
            except SkipFileOnSampleLoad:
                pass
            except:
                print(f"Failed to load {timbre_file}.")
            else:
                print(f"Loaded {timbre_file}.")

    @property
    def _samples_dir(self) -> str:
        return os.path.join("../data/samples", self._config.src)

    def _load_envelope(self, timbre: str) -> AudioSampleEnvelope:
        envelope_settings: Dict[str, Any] = dict()
        try:
            arg_types = AudioSampleEnvelope.__annotations__  # { <ARG>: <TYPE> }
            path = os.path.join(self._samples_dir, f"{timbre}.envelope")
            for arg, val in dotenv_values(path).items():
                if arg in arg_types:
                    envelope_settings[arg] = arg_types[arg](val)
        except:
            pass
        return AudioSampleEnvelope(**envelope_settings)

    def _load_file(self, path: str):
        timbre, extension = os.path.basename(path).split(".")
        if extension != "wav":
            raise SkipFileOnSampleLoad()
        envelope = self._load_envelope(timbre)
        self._timbre_data[timbre] = envelope
        # throws an exception if load failed
        data: NDArray[np.float32] = librosa.load(  # type: ignore
            path,
            sr=self.sample_rate,
            dtype=np.float32,
        )[0]
        data *= self._config.volume

        def splice_file(index: int) -> NDArray[np.float32]:
            def position_to_sample_time(position: float) -> int:
                m = self.sample_rate * 60 / self._config.beats_per_minute
                return int(m * position)

            sample_time = position_to_sample_time(index)
            start = sample_time + envelope.start_sample
            end = sample_time + envelope.end_sample
            return data[start:end]

        for i, pitch_value in enumerate(
            range(self._config.range[0].value, self._config.range[1].value + 1)
        ):
            self._sample_data[(timbre, Pitch(pitch_value))] = AudioSample(
                audio=splice_file(i),
                envelope=envelope,
            )

    @property
    def sample_rate(self) -> int:
        return self._config.sample_rate

    def get_sample(self, timbre: str, pitch: Pitch) -> AudioSample:
        return self._sample_data[(timbre, Pitch(pitch.value))]

    def get_random_timbre(self) -> str:
        return random.choice(list(self._timbre_data.keys()))
