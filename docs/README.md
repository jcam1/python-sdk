# Docs

> [!IMPORTANT]
> This `README` is mainly for the advanced users (e.g., contributors of this repo).

This directory contains the auto-generated documentation for the SDK.

## 📄 Build

Run the following commands that generate a collection of documents under [`./docs`](./) directory.

```sh
# cd into the root directory
$ cd python-sdk
# generate documentation from the google-styled docstrings
$ uv run pdoc ./packages/core/jpyc-core-sdk -o ./docs/core -d google
```

## 🔍 UI

Type the following into your browser to see the contents.

```sh
{absolute_path_of_any_parent_directories}/python-sdk/docs/core/index.html
```
