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
    weight: float = 1


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
        """
        Current rules:
        - Any I, IV, V chord may be followed by any chord.
        - A V7 chord must resolve to its corresponding I chord.
            - No dom7 after dom7 (unless they are the same chord).

        Considerations to think about:
        - Should the diagonal (same chord) be treated differently?
        - Probabilities of special cadences (eg. V-I)?
        - Data collection for transition matrix?
        """

        chords = (
            Chord(arrangement_metadata.key, ChordQuality.Maj),
            Chord(arrangement_metadata.key + Interval.from_str("4"), ChordQuality.Maj),
            Chord(arrangement_metadata.key + Interval.from_str("5"), ChordQuality.Maj),
        )

        transitions: List[Transition] = []
        for src in chords:
            for dst in chords:
                transitions.append(Transition(src=src, dst=dst))
                transitions.append(Transition(src=src, dst=dst.get_V7()))
            transitions.append(
                Transition(
                    src=src.get_V7(),
                    dst=src,
                    weight=1.5,  # promote secondary dominant resolutions
                )
            )

        priors = np.zeros((ViterbiIndex.TOTAL_STATES))
        prob = 1 / len(chords)
        priors[[ViterbiIndex.from_chord(chord).index for chord in chords]] = prob

        return (tuple(transitions), priors)


class TransitionManager:
    """
    The transition manager for the Viterbi chord progression generator. It contains a matrix
    that represents the score of transitioning from one chord to another, without
    considering the melody. It also contains the priors that describe the initial state.

    The transition matrix should be interpreted as follows:
        matrix[current_chord, next_chord] = score of transitioning from current to next chord

    Note that a score of zero means the transition is not allowed.
    """

    def __init__(
        self,
        arrangement_metadata: ArrangementMetadata,
        algorithm: TransitionAlgorithmFn = TransitionAlgorithms.resolve_to_I_IV_V,
    ):
        self._matrix = np.zeros((ViterbiIndex.TOTAL_STATES, ViterbiIndex.TOTAL_STATES))

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
