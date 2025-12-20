---
sidebar_position: 5
title: Development
---

# Development

Thank you for your interest in contributing to `novelai-sdk`.

## Setup

```bash
git clone https://github.com/caru-ini/novelai-sdk.git
cd novelai-sdk
uv sync
```

## Code Quality

We use `ruff` and `pyright` to maintain code quality.
You can run them easily using `poethepoet` (installed with uv).

```bash
# Format
uv run poe fmt

# Lint
uv run poe lint

# Type check
uv run poe check

# Run all checks
uv run poe pre-commit
```

## Pull Requests

It's recommended to open an Issue for discussion before adding new features.
Please follow these guidelines:

*   Use [Conventional Commits](https://www.conventionalcommits.org/).
*   Ensure `uv run poe pre-commit` passes.

## License

MIT License.
