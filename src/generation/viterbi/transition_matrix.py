import numpy as np
from common.structures.chord import Chord, ChordQuality
from common.structures.pitch import Pitch
from common.structures.interval import Interval

from generation.viterbi.viterbi_index import ViterbiIndex


class TransitionMatrix:
    """
    The transition matrix for the Viterbi chord progression generator. This matrix
    represents the score of transitioning from one chord to another, without
    considering the melody.

    The transition matrix should be interpreted as follows:
        matrix[current_chord, next_chord] = score of transitioning from current to next chord

    Note that a score of zero means the transition is not allowed.

    Current rules:
    - Any I, IV, V chord may be followed by any chord.
    - A V7 chord must resolve to its corresponding I chord.
        - No dom7 after dom7 (unless they are the same chord).

    Considerations to think about:
    - Should the diagonal (same chord) be treated differently?
    - Probabilities of special cadences (eg. V-I)?
    - Data collection for transition matrix?
    """

    def __init__(self, key: Pitch = Pitch.from_str("C")):
        self._matrix = np.zeros((ViterbiIndex.TOTAL_STATES, ViterbiIndex.TOTAL_STATES))

        I_chord = ViterbiIndex.from_chord(Chord(key, ChordQuality.Maj)).index
        IV_chord = ViterbiIndex.from_chord(
            Chord(key + Interval.from_str("4"), ChordQuality.Maj)
        ).index
        V_chord = ViterbiIndex.from_chord(
            Chord(key + Interval.from_str("5"), ChordQuality.Maj)
        ).index

        self._matrix[[I_chord, IV_chord, V_chord], :] = 1

        for c in range(ViterbiIndex.TOTAL_STATES):
            chord = ViterbiIndex(c).to_chord()
            if chord.quality == ChordQuality.Maj:
                # V7 must resolve to I.
                V7 = ViterbiIndex.from_chord(chord.get_V7()).index
                self._matrix[V7, [c, V7]] = 1

    @property
    def matrix(self):
        return self._matrix
