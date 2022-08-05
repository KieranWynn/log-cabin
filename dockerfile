FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y curl

# https://python-poetry.org/docs/master/#installation
ENV POETRY_VERSION=1.1.13

RUN curl -sSL https://install.python-poetry.org | python3 - --version "$POETRY_VERSION"

# See "Add Poetry to your PATH" in https://python-poetry.org/docs/master/#installing-with-the-official-installer
ENV PATH="/root/.local/bin:$PATH"

# Configure virtualenv location inside project
RUN poetry config virtualenvs.in-project true --local

COPY log_cabin log_cabin
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev

# "python main.py" is entrypoint
ENTRYPOINT [ "poetry", "run", "python", "log_cabin/main.py" ]