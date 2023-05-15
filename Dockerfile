FROM tiangolo/uvicorn-gunicorn:python3.11
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"
WORKDIR /atheris
COPY pyproject.toml /atheris
COPY . /atheris
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
CMD ["poetry", "run", "start"]
