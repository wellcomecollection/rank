set -o errexit
set -o nounset
set -o pipefail

ROOT=$(git rev-parse --show-toplevel)

# run the tests for the cli

pytest cli/cli_tests
