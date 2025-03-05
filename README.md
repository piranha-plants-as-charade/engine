# Piranha Plants as Charade

The premise of this project is to transform an input melody into a full-fledged song in the style of [*Piranha Plants on Parade*](https://www.youtube.com/watch?v=3EkzTUPoWMU) from *Super Mario Bros. Wonder*.

## Setup

### Requirements

- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [FluidSynth](https://github.com/FluidSynth/fluidsynth/wiki/Download)

### Installation

Run the following commands:
```sh
poetry shell    # activates the Poetry environment
poetry install  # installs the Python dependencies
```

## Development

In `/src`, run the following command:
```sh
fastapi dev app.py
```
This will open a server at `localhost:8000`. See [Endpoints](#endpoints) for endpoint-specific details.

## Endpoints

### `/generate`

#### Input

| Field | Type       | Description                                                                              |
| ----- | ---------- | ---------------------------------------------------------------------------------------- |
| file  | File (WAV) | An audio file containing a melody to arrange in the style of _Piranha Plants on Parade_. |
