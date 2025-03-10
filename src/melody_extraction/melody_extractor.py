import librosa
import numpy as np
import numpy.typing as npt
from typing import Tuple
from common.audio_data import AudioData
from common.note_collection import NoteCollection
from common.roll import Roll
from melody_extraction.note_collection_builder import NoteCollectionBuilder
from melody_extraction.pitch_detector import PitchDetector, PitchDetectorConfig


class MelodyExtractor:
    @classmethod
    def _harmonic_percussive_split(
        cls,
        audio: AudioData,
    ) -> Tuple[AudioData, npt.NDArray[np.int32]]:
        harmonic_signal: npt.NDArray[np.float32]
        onset_times: npt.NDArray[np.int32]

        D = librosa.stft(audio.array)  # type: ignore

        harmonic, percussive = librosa.decompose.hpss(D)  # type: ignore

        harmonic_signal = librosa.istft(harmonic)  # type: ignore
        onset_env = librosa.onset.onset_strength(S=np.abs(percussive), sr=audio.sample_rate)  # type: ignore
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=audio.sample_rate)  # type: ignore
        onset_times = librosa.frames_to_time(onset_frames, sr=audio.sample_rate)  # type: ignore

        return AudioData(harmonic_signal, audio.sample_rate), onset_times * int(
            audio.sample_rate
        )

    @classmethod
    def extract_melody(cls, input_path: str) -> Tuple[Roll, NoteCollection]:
        audio = AudioData.from_file(input_path)

        harmonic_audio, onset_times = cls._harmonic_percussive_split(audio)

        t, pitch_midi = PitchDetector.detect(harmonic_audio, PitchDetectorConfig())

        # MVP assumptions.
        bpm = 110
        time_signature = (4, 4)
        q = 16

        roll = Roll(beats_per_minute=bpm, quantization=q, time_signature=time_signature)

        ncb = NoteCollectionBuilder(roll, pitch_midi, t, onset_times)
        notes = ncb.build()

        return roll, notes
