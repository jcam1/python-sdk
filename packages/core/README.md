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

## Comments & Docstrings

Docstrings should be written in the [Google-style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

## Linting

```sh
# Run linter without fixing
$ uv run riff check {dir_name}
# Run linter & auto-fix
$ uv run riff check {dir_name} --fix
```

## Formatting

```sh
# Run formatter without fixing
$ uv run riff format {dir_name} --check
# Run formatter & auto-fix
$ uv run riff format {dir_name}
```
