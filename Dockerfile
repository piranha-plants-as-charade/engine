FROM ubuntu:latest
ENV \
  # Poetry configuration.
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=true \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.0.0

# Install packages.
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.11 -y
RUN apt-get install wget curl fluidsynth -y

# Copy in the source code.
COPY . .

# Install Poetry and dependencies.
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install

# Setup an app user so the container doesn't run as the root user.
RUN useradd app
USER app

EXPOSE 8000
WORKDIR /src/
CMD ["poetry", "run", "fastapi", "run", "app.py", "--port", "8000"]