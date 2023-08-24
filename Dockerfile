FROM public.ecr.aws/docker/library/python:3.10 AS tooling

ARG POETRY_VERSION=1.5.1
RUN curl -sSL https://install.python-poetry.org | \
    POETRY_HOME=/usr/local \
    POETRY_VERSION=$POETRY_VERSION python3 -

# Install Terraform (for formatting)
ARG TERRAFORM_VERSION=1.5.6
RUN wget -q -O /tmp/terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
  unzip -q -o /tmp/terraform.zip -d /usr/local/bin

WORKDIR /project

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-cache --no-interaction --no-root

COPY . ./

RUN poetry install --no-cache --no-interaction --only-root
RUN poetry build --format=wheel

FROM public.ecr.aws/docker/library/python:3.10-slim as rank

COPY --from=tooling /project/dist/ ./dist

RUN pip install ./dist/*.whl

ENTRYPOINT ["rank"]
