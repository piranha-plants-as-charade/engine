from __future__ import annotations  # avoid circular dependency

import numpy as np
from abc import abstractmethod
from dataclasses import dataclass
from typing import DefaultDict
from numpy.typing import NDArray
from collections import defaultdict

import common.roll as roll
from common.audio_sample import AudioSampleManager, AudioSampleManagerConfig

from .base import Instrument, InstrumentExportConfig


@dataclass(frozen=True)
class SampledInstrumentExportConfig(InstrumentExportConfig):
    sample_src: str


class SampledInstrument(Instrument):

    @property
    @abstractmethod
    def export_config(self) -> SampledInstrumentExportConfig:
        pass

    def generate_audio_from_samples(
        self,
        config: roll.RollExportConfig,
    ) -> NDArray[np.float32]:
        def roll_time_to_sample_time(time: float) -> int:
            m = config.sample_rate * 60 / self._parent.beats_per_minute
            m *= self._parent.beat_duration / self._parent.quantization
            return int(m * time)

        sample_manager = AudioSampleManager(
            AudioSampleManagerConfig(src=self.export_config.sample_src)
        )

        audio_as_dict: DefaultDict[int, np.float32] = defaultdict(lambda: np.float32(0))
        for note in self.notes.list():
            note_range = (
                roll_time_to_sample_time(note.start),
                roll_time_to_sample_time(note.end),
            )
            timbre = sample_manager.get_random_timbre()
            sample = sample_manager.get_sample(timbre, note.pitch)
            sample_len = len(sample.audio)
            sample_envelope = sample.timbre_properties.get_envelope(
                min(sample_len, note_range[1] - note_range[0])
            )
            for i, j in enumerate(range(*note_range)):
                if i >= sample_len:
                    break
                offset = (
                    config.num_start_padding_samples
                    + sample.timbre_properties.start_shift
                )
                audio_as_dict[j + offset] += sample.audio[i] * sample_envelope[i]

        return np.array([audio_as_dict[i] for i in range(max(audio_as_dict.keys()))])
