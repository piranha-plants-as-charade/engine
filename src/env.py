import os
from dotenv import dotenv_values
from dataclasses import dataclass


@dataclass
class Env:
    FE_BASE_URL: str
    BE_BASE_URL: str
    INPUT_DIR: str
    OUTPUT_DIR: str


env_config = dotenv_values(".env")

# Throws an error on fail.
ENV = Env(**env_config)  # type: ignore

os.makedirs(ENV.INPUT_DIR, exist_ok=True)
os.makedirs(ENV.OUTPUT_DIR, exist_ok=True)
