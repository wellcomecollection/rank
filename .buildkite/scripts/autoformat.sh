#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

BLACK_VERSION=23.7.0
ROOT=$(git rev-parse --show-toplevel)
PATH=$HOME/.local/bin:$PATH

# Install black
if [[ ! -x "$(command -v black)}" || "$(black --version)" != "$BLACK_VERSION" ]]; then
    mkdir -p $HOME/.local/bin
    wget -O $HOME/.local/bin/black https://github.com/psf/black/releases/download/${BLACK_VERSION}/black_linux
    chmod +x $HOME/.local/bin/black
fi

# Run the formatter
black $ROOT

# Commit any changes
if [[ `git status --porcelain` ]]; then
  git config user.name "Buildkite on behalf of Wellcome Collection"
  git config user.email "wellcomedigitalplatform@wellcome.ac.uk"

  git remote add ssh-origin $BUILDKITE_REPO || true
  git fetch ssh-origin
  git checkout --track ssh-origin/$BUILDKITE_BRANCH || true

  git add --verbose --update
  git commit -m "Apply auto-formatting rules"

  git push ssh-origin HEAD:$BUILDKITE_BRANCH
  exit 1;
else
  echo "There were no changes from auto-formatting"
  exit 0;
fi
