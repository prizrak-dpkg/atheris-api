FROM tiangolo/uvicorn-gunicorn:python3.9-alpine3.14
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"
WORKDIR /atheris
COPY pyproject.toml /atheris
COPY poetry.lock /atheris
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
COPY . /atheris
CMD ["poetry", "run", "start"]