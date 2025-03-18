import numpy as np

from common.structures.chord import Chord, ChordQuality
from common.structures.interval import Interval
from common.arrangement import ArrangementMetadata
from common.note_collection import NoteCollection

from generation.chord_progression import ChordProgression
from generation.viterbi.transition_matrix import TransitionMatrix
from generation.viterbi.observation_function import ObservationFunction
from generation.chord_progression_generator import ChordProgressionGenerator
from generation.viterbi.viterbi_index import ViterbiIndex


class ViterbiChordProgressionGenerator(ChordProgressionGenerator):
    """
    A chord progression generator using the Vitberi algorithm.

    Note that we are starting at the end of the melody and working backwards.

    TODO:
    - Need to determine key of melody.

    :param arrangement_metadata: The arrangement metadata.
    :param melody: The melody to generate the chord progression for.
    """

    def __init__(
        self,
        arrangement_metadata: ArrangementMetadata,
        melody: NoteCollection,
        hop_size: int | None,
    ):
        self._priors = np.zeros((ViterbiIndex.TOTAL_STATES))
        # End on tonic major
        # TODO: Determine key of melody.
        self._priors[
            [
                ViterbiIndex.from_chord(
                    Chord(arrangement_metadata.key, ChordQuality.Maj)
                ).index,
                ViterbiIndex.from_chord(
                    Chord(
                        arrangement_metadata.key + Interval.from_str("4"),
                        ChordQuality.Maj,
                    )
                ).index,
                ViterbiIndex.from_chord(
                    Chord(
                        arrangement_metadata.key + Interval.from_str("5"),
                        ChordQuality.Maj,
                    )
                ).index,
            ]
        ] = (
            1 / 3
        )
        self._transition_matrix = TransitionMatrix(arrangement_metadata.key).matrix
        self._observation_fn = ObservationFunction()

        self._melody = melody
        self._arrangement_metadata = arrangement_metadata

        self._hop_size = hop_size if hop_size is not None else self._default_hop_size

    @property
    def _default_hop_size(self) -> int:
        measure_duration = self._arrangement_metadata.Duration(
            self._arrangement_metadata.beats_per_measure
        )
        return round(measure_duration / 2)

    def generate(self) -> ChordProgression:
        melody_end = self._melody.list()[-1].start + self._melody.list()[-1].duration
        q = self._arrangement_metadata.quantization
        end = int(np.ceil(melody_end / q) * q)

        chord_progression = ChordProgression(start_time=0, end_time=end)

        # Total number of observations (melody chunks).
        T = int(np.ceil(chord_progression.end_time / self._hop_size))

        # DP table for path probabilities.
        probs = np.ones((ViterbiIndex.TOTAL_STATES, T))
        # DP table for backtracking (points to previous state).
        parent = np.zeros((ViterbiIndex.TOTAL_STATES, T))

        # Initialize with priors and first observation.
        probs[:, 0] = self._priors * self._observation_fn.get_score(
            np.arange(ViterbiIndex.TOTAL_STATES),
            notes=self._melody,
            start_time=0,
            hop_size=self._hop_size,
        )

        t = 1
        for time in range(self._hop_size, melody_end - self._hop_size, self._hop_size):
            for i in range(ViterbiIndex.TOTAL_STATES):
                probs[i, t] = np.max(
                    probs[:, t - 1] * self._transition_matrix[:, i]
                ) * self._observation_fn.get_score(
                    i, self._melody, time, self._hop_size
                )
                parent[i, t] = np.argmax(
                    probs[:, t - 1] * self._transition_matrix[:, i]
                )

            if probs[:, t].sum() == 0:
                print("WARNING: probabilities converged to zero.")

            t += 1

        # Reconstruct the optimal path.
        path = np.zeros(T, dtype=int)
        path[T - 1] = np.argmax(probs[:, T - 1])
        for t in range(T - 2, -1, -1):
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
