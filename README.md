# Python Boilerplate

## Project Structure

```toml

/projects
├─ 'folder to contain all project-specific files/scripts'
|
└─ [project folders]
├─ src
|   ├─ [project files]
|   └─ [project files]
|
├─ tests
|   ├─ [project tests]
|   └─ [project tests]
|
├─ .env
|   └─ 'project specific env variables'
|
└─ main.py
└─ 'main entry point for the project'

/lib
├─ 'libraries that are tied to a specific (external) dependency (e.g. AWS)'
|
└─ aws
├─ 'AWS-specific functions wrapping around the boto3 library'
├─ cognito
|   └─ 'user management functions for interacting with AWS Cognito'
├─ dynamodb
└─ 'database functions for interacting with AWS DynamoDB'
└─ s3
└─ 'file storage functions for interacting with AWS S3'

/shared
├─ 'shared generic libraries that can be used across projects'
|
├─ config
|   └─ 'shared configuration settings, e.g. for env variables and data paths'
|
├─ logging
|   └─ 'generic logging utility library that can be used in place of `print`'
|
└─ utils
├─ 'generic functions to e.g. safely get dict attributes'
├─ date
|    └─ 'utility functions to e.g. calc the difference between dates'
├─ sanitize
|    └─ 'utility functions to remove unwanted characters from strings for e.g. filenames etc'
└─ timestamp
└─ 'utility functions to generate timestamps in various formats'

.env.shared
└─ 'shared env variables across all projects'

.pre-commit-config.yaml
└─ 'configuration options for the pre-commit hooks'

pyproject.toml
└─ 'poetry (project dependencies) configuration file'

```

## Quick Start

### Setup dependencies

#### Install poetry

To begin, you will need to have Poetry installed on your machine. You can find
the [installation instructions here](https://python-poetry.org/docs/#installation).

#### Install dependencies

This will install all the dependencies listed in the `pyproject.toml` file using poetry.

```commandline
poetry install
```

#### Setup pre-commit hooks

This will create 'hooks' that run automatically before each commit to ensure code quality and consistency.

```commandline
pre-commit install
```

#### Setup shared env variables

This creates a copy of the shared env variables in the root directory. This is used to define env variables that are
shared across all projects.

```commandline
cp .env.example .env.shared
```

## Key packages/tools used in this app

If you are not familiar with the different technologies used in this project, please refer to the respective docs:

- [Poetry](https://python-poetry.org/docs/) - Python dependency management
- [Polars](https://polars.rs/docs/) - Fast multi-threaded DataFrame library for Rust & Python
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK for Python

### Development tools

- [Pre-commit](https://pre-commit.com/) - Git hooks to enforce code quality and consistency
- [Black](https://black.readthedocs.io/en/stable/) - Python code formatter
- [Ruff](https://beta.ruff.rs/docs/) - Python linter to enforce code quality and consistency

