import os
import typing
import dataclasses
from typing import Dict, Type, Literal, Tuple, Any
from dataclasses import dataclass
from dotenv import dotenv_values


# Any common.structure can appear in an env file.
from common.structures.pitch import Pitch  # type: ignore
from common.structures.interval import Interval  # type: ignore
from common.structures.note import Note  # type: ignore
from common.structures.chord import Chord  # type: ignore


RunMode = Literal["prod", "dev"]


_RUN_MODE_ARGS: Tuple[RunMode, ...] = typing.get_args(RunMode)
_RUN_MODE = os.environ.get("MODE", "dev")
assert _RUN_MODE in _RUN_MODE_ARGS, "Invalid run mode."


@dataclass(frozen=True)
class Env:
    BE_AUTH_TOKEN: str
    FE_BASE_URL: str
    BE_BASE_URL: str
    INPUT_DIR: str
    OUTPUT_DIR: str
    RUN_MODE: RunMode = _RUN_MODE


def load_env(cls: Type[Any], path: str, default_args: Dict[str, Any] = dict()) -> Any:
    arg_types = {field.name: field for field in dataclasses.fields(cls)}
    settings: Dict[str, Any] = dict()
    for arg, val in dotenv_values(path).items():
        if arg not in arg_types:
            continue
        typ = arg_types[arg].type
        # FIXME: this works for now but isn't rigorous
        if typ is not str:
            val = eval(val)  # type: ignore
        settings[arg] = val
    return cls(**{**default_args, **settings})


ENV: Env = load_env(Env, f"../.env.{_RUN_MODE.lower()}")

os.makedirs(ENV.INPUT_DIR, exist_ok=True)
os.makedirs(ENV.OUTPUT_DIR, exist_ok=True)
