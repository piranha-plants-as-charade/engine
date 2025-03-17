from typing import Callable, List, FrozenSet
import numpy as np
from numpy.typing import NDArray

from common.note_collection import NoteCollection
from common.structures.pitch import Pitch

from generation.viterbi.viterbi_index import ViterbiIndex


def frequency_counter(i: int, pitches: List[FrozenSet[Pitch]], hop_size: int) -> float:
    """
    A simple observation function that counts the number of notes in a chord that are present in
    the given pitches.
    """
    chord = ViterbiIndex(i).to_chord()
    chord_pitches = [x.value % 12 for x in chord.get_pitches()]
    note_found = False
    score = 0
    for timestep in pitches:
        for pitch in timestep:
            note_found = True
            if pitch.value % 12 in chord_pitches:
                score += 1

    # Return constant non-zero score if no notes are found.
    if not note_found:
        return 1

    return score / hop_size


class ObservationFunction:
    """
    A function format of the observation matrix for the Viterbi chord progression generator.
    This function represents the probability of observing a particular pitch given a chord.

    :param algorithm: The algorithm to use for calculating the probability. By default, this
        is the frequency counter algorithm.
    """
    def __init__(
        self,
        algorithm: Callable[
            [int, List[FrozenSet[Pitch]], int], float
        ] = frequency_counter,
    ):
        self.algorithm = algorithm
        self.algorithm_vectorized = np.vectorize(self.algorithm, excluded=[1, 2])

    def get_prob(
        self, i: int | NDArray[np.int16], notes: NoteCollection, start: int, hop_size: int
    ) -> float:
        pitches: List[FrozenSet[Pitch]] = []
        for index in range(start, start + hop_size):
            pitches.append(notes.get_pitches_at_time(index))

        if isinstance(i, np.ndarray):
            return self.algorithm_vectorized(i, pitches, hop_size)

        return self.algorithm(i, pitches, hop_size)
