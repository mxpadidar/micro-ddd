FROM python:3.12.2-slim-bullseye

RUN apt update && apt install -y postgresql-client

WORKDIR /app

COPY pyproject.toml .


RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY src .
