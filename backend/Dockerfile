FROM python:3.8.3-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CODECOV_TOKEN 0d496f2e-5b00-47ee-9c8b-ffd168c7846e

RUN apt-get update \
  && apt-get -y install curl netcat gcc \
  && apt-get clean

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
