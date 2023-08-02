#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

ROOT=$(git rev-parse --show-toplevel)

# Generate the CLI docs
typer cli.main utils docs --name rank --output docs/cli-reference.md

# Only run this bit if we're in buildkite
if [[ "${BUILDKITE:-}" ]]; then
    # Commit any changes
    if [[ `git status --porcelain` ]]; then
        git config user.name "Buildkite on behalf of Wellcome Collection"
        git config user.email "wellcomedigitalplatform@wellcome.ac.uk"

        git remote add ssh-origin $BUILDKITE_REPO || true
        git fetch ssh-origin
        git checkout --track ssh-origin/$BUILDKITE_BRANCH || true

        git add --verbose --update
        git commit -m "Generate CLI docs"

        git push ssh-origin HEAD:$BUILDKITE_BRANCH
        exit 1;
    else
        echo "No changes to commit"
        exit 0;
    fi
fi
