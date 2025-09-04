#!/bin/bash

##
# This script runs build-backend.sh in a docker container.
# Can also be used to run build-backend.sh in the local terminal environment. See usage
#
# Reasons
#   a) consistent python environment
#   b) consistent version of poetry, also avoid installing pipx and poetry locally (for non backend devs)
#   c) The above also apply for the Gitlab runner environment
#   d) Having a local script to do this helps in development and debugging of the CI job
#   e) The work is reusable as the script of the CI job
#      i.e. `cd ./backend && build-backend-docker.sh local` instead of writing lines of code
#
# EXAMPLE USAGE
#   bash build-backend-docker.sh --help
#   LAMBDA_NAME=rasd_fastapi bash build-backend-docker.sh docker
#   LAMBDA_NAME=rasd_fastapi bash build-backend-docker.sh local
##

# Exit on any errors. Can sometimes cause unexpected exits.
# Detect errors in child scripts we call from this one, instead of continuing blindly. Helps in debugging.
# e.g. if not set, script will not stop on this error: build-backend.sh: line 6: 1: Please provide the name of the lambda on $1! e.g. rasd-fastapi
set -e

PYTHON_VERSION="${PYTHON_VERSION:-3.13.0}"
DOCKER_IMAGE="python:${PYTHON_VERSION}-slim-buster"

if [[ "$1" == "--help" ]] || [[ -z "$1" ]]; then
  echo "
  Usage

    LAMBDA_NAME=name_of_lambda bash $0 docker
    LAMBDA_NAME=name_of_lambda bash $0 local
  "
  exit 0
fi

# Mount the backend directory in the docker container
# and run the sam cli tool wrapper
# Docker 'run' command reference: https://docs.docker.com/engine/reference/commandline/run/
# --rm      removes the container after it finishes running the command
# -v        mounts the sourcepath:/pathinsidecontainer
# --workdir run commands in this directory
command_docker="
docker run \
  --rm \
  -v $(pwd):/rasd \
  --workdir /rasd
  ${DOCKER_IMAGE}
"

# Setup the command to run the child scripts (run-poetry.sh and sam-wrapper.sh)
# See comments inside each script for details
command_general="
  bash build-backend.sh ${LAMBDA_NAME:?Please provide LAMBDA_NAME environment variable}
"

# Check if we're supposed to run this directly in the terminal, or in a docker container
runspace="${1:?"Please provide either 'docker' or 'local' as \$1"}"
if [[ "$1" == "docker" ]]; then
  command="$command_docker $command_general"
elif [[ "$1" == "local" ]]; then
  command=$command_general
fi

# Run the constructed command
1>&2 echo "$0: running command: $command"
eval $command

# Notify operator
1>&2 echo "$0: End of script."