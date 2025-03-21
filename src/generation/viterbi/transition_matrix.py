import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass
from typing import Tuple, List, Callable

from common.structures.chord import Chord, ChordQuality
from common.structures.interval import Interval

from generation.viterbi.viterbi_index import ViterbiIndex

from export.arrangement import ArrangementMetadata


@dataclass(frozen=True)
class Transition:
    src: Chord
    dst: Chord
    weight: float


TransitionAlgorithmFn = Callable[
    [ArrangementMetadata],
    Tuple[Tuple[Transition, ...], NDArray[np.float64]],
]


class TransitionAlgorithms:

    @classmethod
    def resolve_to_I_IV_V(
        cls,
        arrangement_metadata: ArrangementMetadata,
    ) -> Tuple[Tuple[Transition, ...], NDArray[np.float64]]:

        chords = (
            Chord(arrangement_metadata.key, ChordQuality.Maj),
            Chord(arrangement_metadata.key + Interval.from_str("4"), ChordQuality.Maj),
            Chord(arrangement_metadata.key + Interval.from_str("5"), ChordQuality.Maj),
        )

        transitions: List[Transition] = []
        for src in chords:
            for dst in chords:
                if src != dst:
                    transitions.append(Transition(src=src, dst=dst, weight=1))
                transitions.append(Transition(src=src, dst=dst.get_V7(), weight=1))
            transitions.append(Transition(src=src.get_V7(), dst=src, weight=1.5))

        priors = np.zeros((ViterbiIndex.TOTAL_STATES))
        prob = 1 / len(chords)
        priors[[ViterbiIndex.from_chord(chord).index for chord in chords]] = prob

        return (tuple(transitions), priors)


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

    def __init__(
        self,
        arrangement_metadata: ArrangementMetadata,
        algorithm: TransitionAlgorithmFn = TransitionAlgorithms.resolve_to_I_IV_V,
    ):
        self._matrix = np.zeros((ViterbiIndex.TOTAL_STATES, ViterbiIndex.TOTAL_STATES))

        for i in range(ViterbiIndex.TOTAL_STATES):
            self._matrix[i, i] = 1

        transitions, self._priors = algorithm(arrangement_metadata)

        for transition in transitions:
            self._matrix[
                ViterbiIndex.from_chord(transition.src).index,
                ViterbiIndex.from_chord(transition.dst).index,
            ] = transition.weight

    @property
    def matrix(self) -> NDArray[np.float64]:
        return self._matrix

    @property
    def priors(self) -> NDArray[np.float64]:
        return self._priors
