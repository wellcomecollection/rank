#!/bin/bash

# Helper script for devs to build and deploy the Task Docker image for testing

set -euo pipefail

usage() {
	echo "Usage: $0 [-t TAG|--tag TAG]"
	echo
	echo "Builds and pushes the rank Docker image to ECR."
	echo
	echo "Options:"
	echo "  -t, --tag TAG   Image tag to push (default: dev)"
	echo "  -h, --help      Show this help and exit"
}

TAG="dev"

while [[ $# -gt 0 ]]; do
	case "$1" in
		-t|--tag)
			if [[ $# -lt 2 ]]; then
				echo "Error: $1 requires a value" >&2
				usage >&2
				exit 2
			fi
			TAG="$2"
			shift 2
			;;
		-h|--help)
			usage
			exit 0
			;;
		*)
			echo "Error: unknown argument: $1" >&2
			usage >&2
			exit 2
			;;
	esac
done

IMAGE_REPO="756629837203.dkr.ecr.eu-west-1.amazonaws.com/weco/rank"
IMAGE_REF="${IMAGE_REPO}:${TAG}"

# Set dir as parent dir of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Docker login public
aws ecr-public get-login-password \
--region us-east-1 \
--profile catalogue-developer | docker login \
--username AWS \
--password-stdin public.ecr.aws

# Docker login ECR private (to push built image)
aws ecr get-login-password \
--profile catalogue-developer | docker login \
--username AWS \
--password-stdin 756629837203.dkr.ecr.eu-west-1.amazonaws.com

# From ./catalogue_graph/ build and tag the image
docker buildx build --platform linux/amd64 \
--provenance=false \
-t "$IMAGE_REF" \
--build-arg PYTHON_IMAGE_VERSION="$(cat .python-version)" \
-f Dockerfile .

# Push the built image to ECR
docker push "$IMAGE_REF"