---
id: intro
sidebar_position: 1
title: Overview
slug: /
---

# NovelAI Python SDK

![intro](./images/intro.png)

[![PyPI version](https://img.shields.io/pypi/v/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![Python Version](https://img.shields.io/pypi/pyversions/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/caru-ini/novelai-sdk/blob/main/LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A modern, type-safe Python SDK for NovelAI's image generation API.
Designed for Developer Experience (DX) with full Pydantic v2 validation and complete type hints.

## Key Features

- **Type Safety**: Python 3.10+ support, robust validation with Pydantic v2.
- **High-Level API**: Intuitive and easy-to-use interface.
- **Modern Features**: Support for V4 models, Character References, ControlNet, etc.
- **Utilities**: Built-in PIL/Pillow integration, SSE streaming.

## Comparison with Alternatives

| Feature                         | novelai-sdk | [novelai-api](https://github.com/Aedial/novelai-api) | [novelai-python](https://github.com/LlmKira/novelai-python) |
| ------------------------------- | :---------: | :--------------------------------------------------: | :---------------------------------------------------------: |
| Type Safety (Pydantic v2)       |      ✅      |                          ❌                           |                              ✅                              |
| Async Support                   |      ✅      |                          ✅                           |                              ✅                              |
| Image Generation                |      ✅      |                          ✅                           |                              ✅                              |
| Text Generation                 |      🚧      |                          ✅                           |                              ✅                              |
| **Character Reference**         |      ✅      |                          ❌                           |                              ❌                              |
| **Multi-Character Positioning** |      ✅      |                          ❌                           |                              ✅                              |
| ControlNet / Vibe Transfer      |      ✅      |                          ❌                           |                              ✅                              |
| SSE Streaming                   |      ✅      |                          ❌                           |                              ✅                              |
| Python 3.13+                    |      ✅      |                          ❌                           |                              ❌                              |
| Active Maintenance              |      ✅      |                          ✅                           |                              ⚠️                              |

✅ Supported | ❌ Not supported | 🚧 Planned | ⚠️ Limited maintenance

## Where to Start?

- **[Getting Started](./getting-started.md)**: From installation to your first generation.
- **[Authentication](./authentication.md)**: How to set up your API key.
- **[Examples](./examples)**: Practical usage examples.

## Links

- [GitHub Repository](https://github.com/caru-ini/novelai-sdk)
- [PyPI](https://pypi.org/project/novelai-sdk/)
- [NovelAI Official Site](https://novelai.net/)

## Disclaimer

This is an unofficial client library. Not affiliated with NovelAI.
Requires an active NovelAI subscription.
