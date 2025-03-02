import os
import librosa
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict
from numpy.typing import NDArray

from common.structures.pitch import Pitch


@dataclass(frozen=True)
class VoiceSampleLibraryConfig:
    """
    :param src: The folder in which the sample file reside (i.e. `data/<src>`), with each file consisting of chromatic ascending notes of the same timbre.
    :param sample_rate: The sample rate at which to load each sample file.
    :param range: The range supported.
    :param beats_per_minute: The tempo at which each note is 1 beat.
    :param sample_window: Each timbre file is divided into 1 beat long partitions. `sample_window` determines how much (percent-wise) of the partition to sample (e.g. (0.25, 0.75) = use the middle half)
    """

    src: str
    sample_rate: int = 44100
    range: Tuple[Pitch, Pitch] = (Pitch.from_str("C3"), Pitch.from_str("G6"))
    beats_per_minute: int = 60
    sample_window: Tuple[float, float] = (0, 0.875)


class VoiceSampleLibrary:

    _data: Dict[Tuple[str, Pitch], NDArray[np.float32]] = dict()

    def __init__(self, config: VoiceSampleLibraryConfig):
        self._config = config
        src = os.path.join("../data/samples", config.src)
        for timbre_file in os.listdir(src):
            try:
                self._load_file(os.path.join(src, timbre_file))
                print(f"Loaded {timbre_file}.")
            except:
                print(f"Failed to load {timbre_file}.")

    def _load_file(self, path: str):
        timbre = os.path.basename(path).split(".")[0]
        # throws an exception if load failed
        data: NDArray[np.float32] = librosa.load(  # type: ignore
            path,
            sr=self.sample_rate,
            dtype=np.float32,
        )[0]

        def splice_file(index: int) -> NDArray[np.float32]:
            def helper(position: float) -> int:
                m = self.sample_rate * 60 / self._config.beats_per_minute
                return int(m * position)

            start = helper(index + self._config.sample_window[0])
            end = helper(index + self._config.sample_window[1])
            return data[start:end]

        for i, pitch_value in enumerate(
            range(self._config.range[0].value, self._config.range[1].value + 1)
        ):
            self._data[(timbre, Pitch(pitch_value))] = splice_file(i)

    @property
    def sample_rate(self) -> int:
        return self._config.sample_rate

    def get_sample(self, timbre: str, pitch: Pitch) -> NDArray[np.float32]:
        return self._data[(timbre, Pitch(pitch.value))]
