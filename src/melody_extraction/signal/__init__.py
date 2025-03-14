import librosa
import numpy as np
from numpy.typing import NDArray
from typing import Tuple
from common.audio_data import AudioData
from common.note_collection import NoteCollection
from common.arrangement import ArrangementMetadata
from melody_extraction.signal.note_collection_builder import NoteCollectionBuilder
from melody_extraction.signal.pitch_detector import PitchDetector, PitchDetectorConfig


class SignalMelodyExtractor:

    def __init__(self):
        pass

    def _harmonic_percussive_split(
        self,
        audio: AudioData,
    ) -> Tuple[AudioData, NDArray[np.int32]]:
        """
        Split the audio into harmonic and percussive components.

        :param audio: The audio to split.
        :return: A tuple containing the harmonic audio and the onset times (percussive elements).
        """
        harmonic_signal: NDArray[np.float32]
        onset_times: NDArray[np.int32]

        D = librosa.stft(audio.array)  # type: ignore

        harmonic, percussive = librosa.decompose.hpss(D)  # type: ignore

        harmonic_signal = librosa.istft(harmonic)  # type: ignore
        onset_env = librosa.onset.onset_strength(S=np.abs(percussive), aggregate=np.median, sr=audio.sample_rate)  # type: ignore
        onset_times = librosa.onset.onset_detect(onset_envelope=onset_env, sr=audio.sample_rate)  # type: ignore

        return AudioData(harmonic_signal, audio.sample_rate), onset_times

    def extract_melody(
        self,
        arrangement_metadata: ArrangementMetadata,
        input_path: str,
    ) -> NoteCollection:
        """
        Extract the melody from the given audio file to an Arrangement and NoteCollection.

        :param input_path: The path to the audio file.
        :return: A tuple containing the Arrangement and NoteCollection.
        """
        audio = AudioData.from_file(input_path)

        audio = AudioData(librosa.effects.trim(audio.array, top_db=10)[0], audio.sample_rate)  # type: ignore

        harmonic_audio, onset_times = self._harmonic_percussive_split(audio)

        t, pitch_midi = PitchDetector.detect(harmonic_audio, PitchDetectorConfig())

        ncb = NoteCollectionBuilder(arrangement_metadata, pitch_midi, t, onset_times)
        notes = ncb.build()

        return notes
