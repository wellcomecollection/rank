FROM public.ecr.aws/docker/library/python:3.10

ARG POETRY_VERSION=1.5.1
RUN curl -sSL https://install.python-poetry.org | \
    POETRY_HOME=/usr/local \
    POETRY_VERSION=$POETRY_VERSION python3 -

ADD . /project
WORKDIR /project

RUN poetry install --no-cache --no-interaction --no-root

CMD ["true"]
