# Piranha Plants as Charade

The premise of this project is to transform an input melody into a full-fledged song in the style of [_Piranha Plants on Parade_](https://www.youtube.com/watch?v=3EkzTUPoWMU) from _Super Mario Bros. Wonder_.

## Setup

### Requirements

- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [FluidSynth](https://github.com/FluidSynth/fluidsynth/wiki/Download)

### Installation

Run the following commands:

```sh
poetry shell    # activates the Poetry environment
poetry install  # installs the Python dependencies
```

Create `/.env.dev` and `/.env.prod`. Below is an example environment file:

```env
BE_AUTH_TOKEN=<TOKEN>
FE_BASE_URL=http://localhost:3000
BE_BASE_URL=http://localhost:8000
INPUT_DIR=../input                 # relative to /src
OUTPUT_DIR=../output               # relative to /src
```

## Development

In `/src`, run the following command:

```sh
fastapi dev app.py
```

This will open a server at `localhost:8000`.

## Deployment

### Google Cloud Platform

This repository comes with a script to deploy the project to Google Cloud Platform's Cloud Run service. To use this script, log into the Google Cloud Platform CLI locally, then run the following command in the repository root:
```sh
./deploy_to_gcloud/run.sh
```

## Endpoints

The endpoint documentation can be found at http://localhost:8000/redoc.
