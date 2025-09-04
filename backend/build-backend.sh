#!/bin/bash

##
# Simplified build script
# Is called by CI/CD job 'build-backend'
# Is called by build-backer-docker.sh (LAMBDA_NAME=rasd_fastapi bash build-backend-wrapper.sh docker)
#
# USAGE
#   Run from the rasd/backend folder
#   bash build-backend.sh
##

set -e # fail on errors

# Get Lambda name from CLI or environment variable
lambda_name=${1:?Please provide the name of the lambda on \$1! e.g. rasd-fastapi}

# printout where we are and what we have, for CI and general debugging
pwd
ls -al

# Step 1
#   Install pipx, used to install poetry safely
#   https://python-poetry.org/docs/#ci-recommendations
command="python3 -m pip install pipx"
echo "$0: running $command"
eval $command

# Step 2
#   Install poetry, to create requirements.txt, used by SAM
command="pipx install poetry==${GLOBAL_POETRY_VERSION:-2.1.4}"
echo "$0: running $command"
eval $command
#   Install export plugin for Poetry 2.x
command="$poetry_install_path/poetry self add poetry-plugin-export"
echo "$0: running $command"
eval $command
#   fix $PATH so we can use poetry immediately without restarting shell
# command="pipx ensurepath"
# echo "$0: running $command"
# eval $command

# Step 3
#   Use poetry to install dependencies
poetry_install_path="/root/.local/bin" # needed because the shell can't refresh inside the single docker run
command="$poetry_install_path/poetry export -f requirements.txt --with $lambda_name -o lambdas/$lambda_name/requirements.txt"
echo "$0: running $command"
eval $command

# Step 4
#   Create dist folder
command="mkdir -p dist/$lambda_name"
echo "$0: running $command"
eval $command

# Step 5
#   Install the dependencies into the target dist directory
command="pip install -r lambdas/$lambda_name/requirements.txt --target ./dist/$lambda_name --upgrade"
echo "$0: running $command"
eval $command

# Step 6
#   Copy the lambda itself into the target dist directory
#   The directory will then be referenced in Pulumi.yaml and deployed to AWS
command="cp -r lambdas/$lambda_name dist/$lambda_name/"
echo "$0: running $command"
eval $command

# Let operator know script has finished.
# Helps with reading and debugging when multiple scripts run consecutively
1>&2 echo "$0: End of script."