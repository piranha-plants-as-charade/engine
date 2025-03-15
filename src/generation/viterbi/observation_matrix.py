import numpy as np

from generation.viterbi.viterbi_index import ViterbiIndex


class ObservationMatrix:
    """
    The observation matrix for the Viterbi chord progression generator. This matrix
    represents the probability of observing a particular pitch given a chord.

    The rows are normalized such that they sum to 1.

    TODO:
    - Extend this to take multiple notes into account.
    """

    def __init__(self):
        total_pitches = 12
        # Start with ones since we don't want dead ends.
        self._matrix = np.ones((ViterbiIndex.TOTAL_STATES, total_pitches))

        for i in range(ViterbiIndex.TOTAL_STATES):
            chord = ViterbiIndex(i).to_chord()
            for pitch in chord.get_pitches():
                self._matrix[i, pitch.value % 12] += 10

        for r in range(ViterbiIndex.TOTAL_STATES):
            self._matrix[r, :] /= np.sum(self._matrix[r, :])

    @property
    def matrix(self):
        return self._matrix
