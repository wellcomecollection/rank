FROM public.ecr.aws/docker/library/python:3.10 AS tooling

ENV UV_HOME=/root/.local
ENV PATH="$UV_HOME/bin:$PATH"
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Terraform (for formatting)
ARG TERRAFORM_VERSION=1.5.6
RUN wget -q -O /tmp/terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
  unzip -q -o /tmp/terraform.zip -d /usr/local/bin

WORKDIR /project

ENV UV_PROJECT_ENVIRONMENT=.venv
ENV PATH="/project/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . ./

RUN uv sync --frozen
RUN uv build --wheel

FROM public.ecr.aws/docker/library/python:3.10-slim as rank

COPY --from=tooling /project/dist/ ./dist

RUN pip install ./dist/*.whl

ENTRYPOINT ["rank"]
