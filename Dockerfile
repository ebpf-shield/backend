FROM python:3.12-slim

WORKDIR /code

COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY /app /code/app

EXPOSE 80

ENTRYPOINT uvicorn app.main:app --host 0.0.0.0 --port 8080