FROM python:3.11-bullseye AS build

RUN pip install --no-cache-dir poetry==1.4.2

#RUN apt-get update && apt-get install -y swig python-dev python3-dev wget unzip make gcc && apt install -y python-setuptools python3-setuptools

COPY pyproject.toml poetry.lock ./
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

RUN poetry install --no-root --no-cache


FROM python:3.11-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}


RUN mkdir /src/
COPY ./ /src/

EXPOSE 8000


ENTRYPOINT ["/src/entrypoint.sh"]
