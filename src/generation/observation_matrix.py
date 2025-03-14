import numpy as np
from common.structures.chord import ChordQuality

from generation.viterbi_index import ViterbiIndex

class ObservationMatrix():
    """
    The observation matrix for the Viterbi chord progression generator. This matrix
    represents the probability of observing a particular pitch given a chord.
    
    The rows are normalized such that they sum to 1.

    TODO:
    - Extend this to take multiple notes into account.
    """
    def __init__(self):
        N = 12 * len(ChordQuality)
        M = 12
        # Start with ones since we don't want dead ends.
        self._matrix = np.ones((N, M))
        
        for i in range(N):
            chord = ViterbiIndex(i).to_chord()
            for interval in chord.quality.value.intervals:
                self._matrix[i, (chord.root + interval).value % 12] += 10
        
        for r in range(N):
            self._matrix[r, :] /= np.sum(self._matrix[r, :])
    
    @property
    def matrix(self):
        return self._matrix
    