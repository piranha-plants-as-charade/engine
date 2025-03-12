import copy
from dataclasses import dataclass
from typing import FrozenSet, Tuple, List
from functools import cached_property
from collections import deque

from common.roll import RollConfig
from common.note_collection import NoteCollection
from common.structures.pitch import Pitch
from common.structures.interval import Interval
from common.structures.chord import Chord, ChordQuality

from generation.chord_progression import ChordProgression


@dataclass(frozen=True)
class _FSMStateContext:
    roll_config: RollConfig
    melody: NoteCollection
    hop_size: float = 1 / 2  # fraction of a measure


@dataclass(frozen=True)
class _FSMState:

    context: _FSMStateContext
    prev_state: "_FSMState | None"
    chord: Chord
    time_interval: Tuple[int, int]

    @property
    def start_time(self):
        return self.time_interval[0]

    @property
    def end_time(self):
        return self.time_interval[1]

    @cached_property
    def out_edges(self) -> List["_FSMState"]:

        if self.start_time <= 0:
            return []

        measure_duration = self.context.roll_config.Duration(
            self.context.roll_config.beats_per_measure
        )
        hop_duration = round(measure_duration * self.context.hop_size)
        next_time_interval = (
            self.start_time - hop_duration,
            self.start_time,
        )
        options = [
            Chord(self.chord.root + Interval.from_str("5"), ChordQuality.Maj)
            # ChordProgressionGenerator.chord_I,
            # ChordProgressionGenerator.chord_IV,
            # ChordProgressionGenerator.chord_V,
            # self.chord.get_V7(),
        ]

        return [
            _FSMState(
                context=self.context,
                chord=option,
                prev_state=self,
                time_interval=next_time_interval,
            )
            for option in options
        ]

    def cost(self):
        if self.prev_state is None:
            return 0
        if self.chord.get_V7() == self.prev_state:
            pass
        return 0

    def total_cost(self):
        instance_cost = self.cost()
        if self.prev_state is None:
            return instance_cost
        return instance_cost + self.prev_state.cost()

    def _notes(self) -> FrozenSet[Pitch]:
        return self.context.melody.get_pitches_in_time_range(self.time_interval)


class ChordProgressionGenerator:

    tonic = Pitch.from_str("C")

    chord_I = Chord(tonic, ChordQuality.Maj)
    chord_ii = Chord(tonic + Interval.from_str("2"), ChordQuality.Min)
    chord_IV = Chord(tonic + Interval.from_str("4"), ChordQuality.Maj)
    chord_V = Chord(tonic + Interval.from_str("5"), ChordQuality.Maj)

    def __init__(self, roll_config: RollConfig, melody: NoteCollection):

        melody_end_time = max([note.end for note in melody.list()])
        melody_end_measure = melody_end_time // roll_config.Duration(
            roll_config.beats_per_measure
        )

        self.starting_state = _FSMState(
            context=_FSMStateContext(roll_config, melody),
            chord=ChordProgressionGenerator.chord_I,
            prev_state=None,
            time_interval=(
                roll_config.Time(melody_end_measure, 0),
                roll_config.Time(melody_end_measure + 1, 0),
            ),
        )

    def generate(self) -> ChordProgression:

        starting_chord_progression = ChordProgression(
            start_time=0,
            end_time=self.starting_state.end_time,
        )

        queue = deque([(self.starting_state, starting_chord_progression)])
        generated_progressions: List[ChordProgression] = list()

        while len(queue) > 0:
            state, chord_progression = queue.popleft()
            chord_progression = copy.deepcopy(chord_progression)
            chord_progression.add_chords((state.chord, state.start_time))

            for next_state in state.out_edges:
                queue.append((next_state, chord_progression))

            if len(state.out_edges) == 0:
                generated_progressions.append(chord_progression)

        return generated_progressions[0]
