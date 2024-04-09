FROM python:3.12

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=true

# Установка poetry
RUN pip install poetry
ENV PATH="$POETRY_HOME/bin:$HOME/.local/bin:$PATH"

WORKDIR /app

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry install --only main
RUN poetry run python -m textblob.download_corpora

COPY ./src/ ./src/
COPY ./alembic.ini .
COPY ./main.py .
COPY ./settings.py .

# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
