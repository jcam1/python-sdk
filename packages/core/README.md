# Core SDK

> [!IMPORTANT]
> TODO: README in English

## Package Management

### Add packages

```sh
# Add packages for production
$ uv add {package_name}
# Add packages for development
$ uv add --dev {package_name}
```

### Remove packages

```sh
$ uv remove {package_name}
```

## Testing

```sh
# Run unit tests
$ uv run pytest -v
# Run unit tests with coverage info
$ uv run pytest -v --cov --cov-branch
# Run unit tests ignoring deprecation warnings
$ uv run pytest -W ignore::DeprecationWarning
```

## Static Code Analysis

### Linting

```sh
# Run linter without fixing
$ uv run riff check {dir_name}
# Run linter & auto-fix
$ uv run riff check {dir_name} --fix
```

### Formatting

```sh
# Run formatter without fixing
$ uv run riff format {dir_name} --check
# Run formatter & auto-fix
$ uv run riff format {dir_name}
```

### Type Checking

```sh
# Run mypy
$ uv run mypy {dir_name}
```

### Pre-Commit Hooks

Pre-commit script is configured at [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml). This automatically runs the configured hooks before executing any `git commit` commands.

```sh
# Simulate pre-commit hooks without creating an actual commit
$ uv run pre-commit run --all-files
```

## Comments & Docstrings

Docstrings should be written in the [Google-style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
