import mido  # type: ignore
from typing import Tuple, Set

from common.structures.pitch import Pitch

from export.arrangement import ArrangementMetadata


# TODO: move to class
def extract_arrangement_metadata_from_melody(input_path: str) -> ArrangementMetadata:

    def extract_time_signature(message: mido.MetaMessage) -> Tuple[int, int]:
        # Throws error on fail.
        assert getattr(message, "type") == "time_signature"
        ret = (
            getattr(message, "numerator"),
            getattr(message, "denominator"),
        )
        assert type(ret[0]) is int and type(ret[1]) is int
        return ret

    def extract_key_signature(message: mido.MetaMessage) -> Pitch:
        # Throws error on fail.
        assert getattr(message, "type") == "key_signature"
        key = getattr(message, "key")
        assert type(key) is str
        return Pitch.from_str(key)

    def extract_beats_per_minute(message: mido.MetaMessage) -> int:
        # Throws error on fail.
        assert getattr(message, "type") == "set_tempo"
        microseconds_per_beat = getattr(message, "tempo")
        seconds_per_beat = microseconds_per_beat / 1e6
        beats_per_minute = round(60 / seconds_per_beat)
        return beats_per_minute

    time_signature_set: Set[Tuple[int, int]] = set()
    key_set: Set[Pitch] = set()
    beats_per_minute_set: Set[int] = set()

    file = mido.MidiFile(input_path)
    for message in file.merged_track:  # type: ignore
        if isinstance(message, mido.MetaMessage):
            match getattr(message, "type"):
                case "time_signature":
                    time_signature_set.add(extract_time_signature(message))
                case "key_signature":
                    # Assuming all keys are in major.
                    key_set.add(extract_key_signature(message))
                case "set_tempo":
                    beats_per_minute_set.add(extract_beats_per_minute(message))
                case _:
                    print(message)

    assert len(time_signature_set) == 1
    time_signature = list(time_signature_set)[0]

    assert len(key_set) == 1
    key = list(key_set)[0]

    assert len(beats_per_minute_set) == 1
    beats_per_minute = list(beats_per_minute_set)[0]

    return ArrangementMetadata(
        beats_per_minute=beats_per_minute,
        time_signature=time_signature,
        key=key,
        quantization=16,
    )
