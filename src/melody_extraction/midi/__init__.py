import mido  # type: ignore
from typing import Tuple, Set

from common.arrangement import ArrangementMetadata
from common.structures.pitch import Pitch


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

    time_signatures: Set[Tuple[int, int]] = set()
    keys: Set[Pitch] = set()

    file = mido.MidiFile(input_path)
    for message in file.merged_track:  # type: ignore
        if isinstance(message, mido.MetaMessage):
            match getattr(message, "type"):
                case "time_signature":
                    time_signatures.add(extract_time_signature(message))
                case "key_signature":
                    # Assuming all keys are in major.
                    keys.add(extract_key_signature(message))
                case _:
                    pass

    assert len(time_signatures) == 1
    time_signature = list(time_signatures)[0]

    assert len(keys) == 1
    key = list(keys)[0]

    return ArrangementMetadata(
        beats_per_minute=110,
        time_signature=time_signature,
        key=key,
        quantization=16,
    )
