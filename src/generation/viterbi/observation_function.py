from typing import Callable, FrozenSet, List, Tuple
import numpy as np
from numpy.typing import NDArray

from common.note_collection import NoteCollection
from common.structures.pitch import Pitch

from generation.viterbi.viterbi_index import ViterbiIndex

ObservationScoreFn = Callable[[int, Tuple[FrozenSet[Pitch], ...]], float]
ObservationScoreFnVectorized = Callable[
    [NDArray[np.int16], Tuple[FrozenSet[Pitch], ...]], float
]


class ObservationFunction:
    """
    A function format of the observation matrix for the Viterbi chord progression generator.
    This function represents the score of observing a particular pitch given a chord.

    :param algorithm: The algorithm to use for calculating the score. By default, this
        is the frequency counter algorithm.
    """

    def __init__(
        self,
        algorithm: ObservationScoreFn | None = None,
    ):
        self.algorithm = (
            ObservationFunction.frequency_counter if algorithm is None else algorithm
        )

    @property
    def algorithm_vectorized(self) -> ObservationScoreFnVectorized:
        return np.vectorize(self.algorithm, excluded=[1])

    @classmethod
    def frequency_counter(cls, i: int, pitches: Tuple[FrozenSet[Pitch], ...]) -> float:
        """
        A simple observation function that counts the number of notes in a chord that are present in
        the given pitches and scales by the number of notes in the chord.

        :param i: The index of the chord.
        :param pitches: The pitches to compare against the chord.
        """
        chord = ViterbiIndex(i).to_chord()
        chord_pitches = [x.value % 12 for x in chord.get_pitches()]
        note_found = False
        score = 0.0
        for timestep in pitches:
            for pitch in timestep:
                note_found = True
                if pitch.value % 12 in chord_pitches:
                    score += 1 / len(chord_pitches)

        # Return constant non-zero score if no notes are found.
        if not note_found:
            return 1

        return score

    def get_score(
        self,
        i: int | NDArray[np.int16],
        notes: NoteCollection,
        start_time: int,
        hop_size: int,
    ) -> float:
        pitches: List[FrozenSet[Pitch]] = []
        for index in range(start_time, start_time + hop_size):
            pitches.append(notes.get_pitches_at_time(index))

        if isinstance(i, np.ndarray):
            return self.algorithm_vectorized(i, tuple(pitches))

        return self.algorithm(i, tuple(pitches))
