# Pathways

![GitHub License](https://img.shields.io/github/license/the-turing-way/pathways)
![Codestyle Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/the-turing-way/pathways/ci.yaml)

Curate user pathways for The Turing Way

## Documentation

Read the [user guide](./documentation.md) to learn how to create pathways.

## Development

[Hatch](https://hatch.pypa.io) is used to build and manage environments.

### Code Style

This project uses Black and Ruff.
The configuration of these packages is defined in [pyproject.toml](./pyproject.toml).
The style can be checked with

```console
$ hatch run lint:style
```

Some problems can be fixed automatically with

```console
$ hatch run lint:fmt
```

### Tests

Tests can be run with

```console
$ hatch run test
```
