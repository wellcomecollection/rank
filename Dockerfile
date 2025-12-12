FROM public.ecr.aws/docker/library/python:3.10 AS tooling

# Install uv
RUN pip install --no-cache-dir uv

# Install Terraform (for formatting)
ARG TERRAFORM_VERSION=1.5.6
RUN wget -q -O /tmp/terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
  unzip -q -o /tmp/terraform.zip -d /usr/local/bin

WORKDIR /project

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml uv.lock README.md ./

# Copy the package source needed for installation
COPY cli/ ./cli/

# Install project + dev dependencies into a local .venv (used by Buildkite tooling)
RUN uv sync --frozen

# Copy the rest of the repository (docs, infra, etc.) for tooling tasks
COPY . ./

FROM public.ecr.aws/docker/library/python:3.10-slim AS rank

WORKDIR /app

# Copy dependency files and source for installation
COPY pyproject.toml uv.lock README.md ./
COPY cli/ ./cli/

RUN pip install --no-cache-dir uv && \
  uv pip install --system .

ENTRYPOINT ["rank"]
