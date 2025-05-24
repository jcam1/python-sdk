# Tests

> [!IMPORTANT]
> This `README` is mainly for the advanced users (e.g., contributors of this repo).

This directory contains test code of the SDK.

## 🏃🏻 Run Tests

Run one of the following commands to run tests. Please run `uv run pytest --help` for other available CLI options.

> [!NOTE]
> Testing results are also to be checked on our [CI workflow](../.github/workflows/check.yml).

```sh
# cd into one of the package directories (e.g., `core`)
$ cd python-sdk/packages/core
# run tests with default config
$ uv run pytest
# run tests with verbosity
$ uv run pytest -v
# run tests with coverage info
$ uv run pytest --cov --cov-branch
```

## 🌲 Directory Structure

|           Module | Description                   |
| ---------------: | :---------------------------- |
| [`core`](./core) | Unit tests of `core` package. |
