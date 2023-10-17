FROM python:3.10-bullseye as build

RUN echo "Настройки Python"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IS_DEV_MODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONHASHSEED=random

RUN echo "Настройки Pip"
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

RUN echo "Установка Poetry"
ENV POETRY_VERSION=1.3.1
RUN pip install "poetry==$POETRY_VERSION"

RUN echo "Кэширование зависимостей Poetry"
WORKDIR /
COPY ../poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi
