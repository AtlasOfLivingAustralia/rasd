# RASD Backend

## Overview

The RASD backend is a Python 3.9 AWS Lambda which uses FastAPI and Mangum and is deployed with CodePipeline and CloudFormation.

## Table of Contents

- [RASD Backend](#rasd-backend)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Architecture](#architecture)
    - [Application](#application)
    - [Structure](#structure)
    - [Development Tools](#development-tools)
  - [Environment Variables](#environment-variables)
  - [Development](#development)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Tasks](#tasks)
    - [Development Server](#development-server)
    - [Build](#build)
    - [Unit Tests](#unit-tests)
    - [Type Checking](#type-checking)
    - [Linting](#linting)
  - [Build & Deployment](#build-deployment)
    - [Local Building](#local-building)
    - [Local Deployment](#local-deployment)

## Architecture

This application uses a variety of technologies in order to be deployed in a serverless environment, whilst still being
developed as a regular FastAPI application.

### Application

- [FastAPI](https://fastapi.tiangolo.com/) REST API ASGI application
- [Mangum](https://mangum.io/) as an adapter for running ASGI applications in AWS Lambda

### Structure

- Structure of application is adapted from [`full-stack-fastapi-postgresql`](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/0.5.0/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app)
- The code itself is nested within a `lambdas` directory, as it was originally expected that the project would require
  multiple lambdas (which was not the case).

```
backend
├── lambdas
│   └── rasd_fastapi            # RASD FastAPI Application
│       ├── api                 # FastAPI REST API
│       ├── core                # Core modules (e.g., settings, auth)
│       ├── crud                # CRUD utilities and abstractions
│       ├── db                  # Database abstraction
│       ├── emails              # Emailing functionality and templates
│       ├── models              # Database models and vocabularies
│       ├── schemas             # REST API request and response schemas
│       ├── services            # External service functionality
│       └── types               # Custom data types and validation
└── tests                       # RASD backend unit tests
```

### Development Tools

- [`poethepoet`](https://github.com/nat-n/poethepoet) as a quick and easy task runner
- [`pytest`](https://docs.pytest.org/) & [`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/) for unit testing and coverage
- [`mypy`](https://mypy.readthedocs.io/en/stable/) for type-checking analysis
- [`ruff`](https://github.com/charliermarsh/ruff) for linting

## Environment Variables & Secrets

In order to run the RASD backend, there are a number of required environment variables that **must** be set. We have set them up cloudformation, which will set environment variables when creating the lambda function. For an up-to-date list of all environment variables, see the `lambdas/rasd_fastapi/core/settings.py` file.

Another thing to setup is AWS secrets. The `ABN_LOOKUP_GUID` variable should be set in newly created environment.

## Development

### Requirements

This project requires:

- Python 3.9
- Poetry

### Installation

To install the dependencies for this project:

```shell
# Ensure your current Python version is 3.9
$ pyenv local 3.9

# Install dependencies using Poetry
$ poetry install

# Enter the Poetry virtual environment shell
$ poetry shell
```

### Tasks

This project uses `poethepoet` as a quick and easy task runner.
To see the existing tasks check the `pyproject.toml` or use:

```shell
$ poe --help
...
CONFIGURED TASKS
  serve
  test
  type
  lint
  clean
```

### Development Server

To start a local development server using `uvicorn`:

```shell
$ poe serve
```

Note that in order to run the application, there are required environment variables that must be set.
See the [Environment Variables](#environment-variables) section above for more details.

### Unit Tests

To run the unit-test suite:

```shell
$ poe test
```

### Type Checking

To run the type-checker over the codebase:

```shell
$ poe type
```

### Linting

To run the linter over the codebase:

```shell
$ poe lint
```

### Clean

To clean the backend directory, and remove caches and build artifacts:

```shell
$ poe clean
```

## Build & Deployment

This serverless application is deployed using `CodePipeline` and `CloudFormation`.
Please see the top level `README.md` file for build & deployment instructions.
Note that it is not recommended to build or deploy locally, and the below instructions are provided at the user's risk.

### Local Building

To build the backend in your local environment for deployment:
1. Follow the [installation instructions](#installation) section above
2. Run `LAMBDA_NAME=rasd_fastapi bash build-backend-wrapper.sh local`
3. The built `dist/rasd_fastapi/` directory will be created