from typing import Callable, FrozenSet, List, Tuple
import numpy as np
from numpy.typing import NDArray

from common.util import EPSILON
from common.note_collection import NoteCollection
from common.structures.pitch import Pitch

from generation.viterbi.viterbi_index import ViterbiIndex

ObservationScoreFn = Callable[[int, Tuple[FrozenSet[Pitch], ...]], float]
ObservationScoreFnVectorized = Callable[
    [NDArray[np.int16], Tuple[FrozenSet[Pitch], ...]], float
]


class ObservationScoringFunctions:

    @classmethod
    def frequency_counter(
        cls,
        viterbi_index: int,
        pitches: Tuple[FrozenSet[Pitch], ...],
    ) -> float:
        """
        A simple observation function that counts the number of notes in a chord that are present in
        the given pitches and scales by the number of notes in the chord.

        :param viterbi_index: The Viterbi index of the chord.
        :param pitches: The pitches to compare against the chord.
        """
        chord = ViterbiIndex(viterbi_index).to_chord()
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


class ObservationModel:
    """
    A function format of the observation matrix for the Viterbi chord progression generator.
    This function represents the score of observing a particular pitch given a chord.

    :param algorithm: The algorithm to use for calculating the score. By default, this
        is the frequency counter algorithm.
    """

    def __init__(
        self,
        scoring_fn: ObservationScoreFn = ObservationScoringFunctions.frequency_counter,
    ):
        self.scoring_fn = scoring_fn

    @property
    def vectorized_scoring_fn(self) -> ObservationScoreFnVectorized:
        return np.vectorize(self.scoring_fn, excluded=[1])

    def get_score(
        self,
        viterbi_index: int | NDArray[np.int16],
        notes: NoteCollection,
        start_time: int,
        hop_size: int,
    ) -> float:
        pitches: List[FrozenSet[Pitch]] = []
        for index in range(start_time, start_time + hop_size):
            pitches.append(notes.get_pitches_at_time(index))

        if isinstance(viterbi_index, np.ndarray):
            return self.vectorized_scoring_fn(viterbi_index, tuple(pitches))

        return np.log(self.scoring_fn(viterbi_index, tuple(pitches)) + EPSILON)
