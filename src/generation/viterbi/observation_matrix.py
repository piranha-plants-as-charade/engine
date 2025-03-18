import numpy as np

from generation.viterbi.viterbi_index import ViterbiIndex


class ObservationMatrix:
    """
    The observation matrix for the Viterbi chord progression generator. This matrix
    represents the probability of observing a particular pitch given a chord.

    The rows are normalized such that they sum to 1.
    
    Current rules:
    - Start with ones to allow a small chance of any pitch, even if it's not in the chord.
    - Add 10 to the probability of the pitches in the chord.
    """

    def __init__(self):
        # Start with ones since we don't want dead ends.
        self._matrix = np.ones((ViterbiIndex.TOTAL_STATES, 12))

        for i in range(ViterbiIndex.TOTAL_STATES):
            chord = ViterbiIndex(i).to_chord()
            for pitch in chord.get_pitches():
                self._matrix[i, pitch.value % 12] += 10

        for r in range(ViterbiIndex.TOTAL_STATES):
            self._matrix[r, :] /= np.sum(self._matrix[r, :])

    @property
    def matrix(self):
        return self._matrix
