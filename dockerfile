FROM python:3.12.2-slim-bullseye

RUN apt update && apt install -y postgresql-client

WORKDIR /app

COPY pyproject.toml poetry.lock ./


RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

RUN apt install -y libmagic1
COPY src .
