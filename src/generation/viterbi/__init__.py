import math
import numpy as np
from numpy.typing import NDArray

from logger import LOGGER

from common.note_collection import NoteCollection

from generation.chord_progression import ChordProgression
from generation.viterbi.transition_model import TransitionModel
from generation.viterbi.observation_model import ObservationModel
from generation.chord_progression_generator import ChordProgressionGenerator
from generation.viterbi.viterbi_index import ViterbiIndex

from export.arrangement import ArrangementMetadata


class ViterbiChordProgressionGenerator(ChordProgressionGenerator):
    """
    A chord progression generator using the Vitberi algorithm.

    Note that we are starting at the end of the melody and working backwards.

    TODO:
    - Need to determine key of melody.

    :param arrangement_metadata: The arrangement metadata.
    :param melody: The melody to generate the chord progression for.
    :param hop_size: The hop size for the melody relative to the length of a measure.
        For example, hop_size=0.5 means the melody is divided into 2 chunks per measure.
    """

    def __init__(
        self,
        arrangement_metadata: ArrangementMetadata,
        melody: NoteCollection,
        hop_size: float = 0.5,
    ):
        self._transition_model = TransitionModel(arrangement_metadata)

        self._observation_model = ObservationModel()

        self._melody = melody
        self._arrangement_metadata = arrangement_metadata

        measure_duration = self._arrangement_metadata.Duration(
            self._arrangement_metadata.beats_per_measure
        )

        # Hop size of a chunk in terms of quantized units.
        self._hop_size = round(measure_duration * hop_size)

    def generate(self) -> ChordProgression:
        melody_end = self._melody.list()[-1].start + self._melody.list()[-1].duration
        quantization = self._arrangement_metadata.quantization
        end_time = int(np.ceil(melody_end / quantization) * quantization)

        transition_matrix = self._transition_model.matrix
        priors = self._transition_model.priors

        chord_progression = ChordProgression(start_time=0, end_time=end_time)

        # Total number of observations (melody chunks).
        T = math.ceil(chord_progression.end_time / self._hop_size)

        # DP table for path probabilities.
        probs = np.ones((ViterbiIndex.TOTAL_STATES, T))
        # DP table for backtracking (points to previous state).
        parent = np.zeros((ViterbiIndex.TOTAL_STATES, T))

        # Initialize with priors and first observation.
        probs[:, 0] = priors * self._get_observation_score_at_time(
            np.arange(ViterbiIndex.TOTAL_STATES),
            start_time=0,
        )

        for t in range(1, T):
            time = t * self._hop_size
            for i in range(ViterbiIndex.TOTAL_STATES):
                score = self._get_observation_score_at_time(i, start_time=time)
                candidate_probs = probs[:, t - 1] * transition_matrix[:, i] * score
                probs[i, t] = np.max(candidate_probs)
                parent[i, t] = np.argmax(candidate_probs)

            if probs[:, t].sum() == 0:
                LOGGER.warning(
                    f"Probabilities converged to zero at t={t}. Reverting to `priors` at t={t}."
                )
                probs[:, t] = priors * self._get_observation_score_at_time(
                    np.arange(ViterbiIndex.TOTAL_STATES),
                    start_time=time,
                )
                # FIXME: handle `parent[:, t]`
        
        # Reconstruct the optimal path.
        path = np.zeros(T, dtype=int)
        path[T - 1] = np.argmax(probs[:, T - 1])
        for t in reversed(range(0, T - 1)):
            path[t] = parent[path[t + 1], t + 1]

        # Build chord progression.
        prev_chord = -1
        for t in range(T):
            if path[t] != prev_chord:
                chord_progression.add_chords(
                    (ViterbiIndex(path[t]).to_chord(), t * self._hop_size)
                )
            prev_chord = path[t]

        return chord_progression

    def _get_observation_score_at_time(
        self,
        viterbi_index: int | NDArray[np.int16],
        start_time: int,
    ):
        return self._observation_model.get_score(
            viterbi_index,
            notes=self._melody,
            start_time=start_time,
            hop_size=self._hop_size,
        )
