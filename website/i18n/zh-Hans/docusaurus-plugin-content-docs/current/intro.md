---
id: intro
sidebar_position: 1
title: 概览
slug: /
---

# NovelAI Python SDK

![intro](./images/intro.png)

[![PyPI version](https://img.shields.io/pypi/v/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![Python Version](https://img.shields.io/pypi/pyversions/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/caru-ini/novelai-sdk/blob/main/LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

NovelAI 图像生成 API 的现代、类型安全的 Python SDK。
专为开发体验 (DX) 设计，具有完整的 Pydantic v2 验证和完整的类型提示。

## 主要特性

- **类型安全**: 支持 Python 3.10+，使用 Pydantic v2 进行强大的验证。
- **高级 API**: 直观且易于使用的界面。
- **现代功能**: 支持 V4 模型、角色参考、ControlNet 等。
- **实用工具**: 内置 PIL/Pillow 集成，SSE 流式传输。

## 与替代方案的比较

| 特性                            | novelai-sdk | [novelai-api](https://github.com/Aedial/novelai-api) | [novelai-python](https://github.com/LlmKira/novelai-python) |
| ------------------------------- | :---------: | :--------------------------------------------------: | :---------------------------------------------------------: |
| 类型安全 (Pydantic v2)          |      ✅      |                          ❌                           |                              ✅                              |
| 异步支持                        |      ✅      |                          ✅                           |                              ✅                              |
| 图像生成                        |      ✅      |                          ✅                           |                              ✅                              |
| 文本生成                        |      🚧      |                          ✅                           |                              ✅                              |
| **角色参考**                    |      ✅      |                          ❌                           |                              ❌                              |
| **多角色定位**                  |      ✅      |                          ❌                           |                              ✅                              |
| ControlNet / Vibe Transfer      |      ✅      |                          ❌                           |                              ✅                              |
| SSE 流式传输                    |      ✅      |                          ❌                           |                              ✅                              |
| Python 3.10+                    |      ✅      |                          ❌                           |                              ❌                              |
| 积极维护                        |      ✅      |                          ✅                           |                              ⚠️                              |

✅ 支持 | ❌ 不支持 | 🚧 计划中 | ⚠️ 维护有限

## 数据模型架构

该库设计有两层不同的数据模型：

![Model Architecture](./images/model-architecture.png)

1.  **用户模型 (推荐)**: 具有合理默认值和自动验证的用户友好模型。
2.  **API 模型**: 直接 1:1 映射到 NovelAI 的 API 端点，主要用于内部。

## 下一步

* 查看 **[快速开始](./getting-started.md)** 以在几分钟内生成图像。
* 浏览 **[示例](./examples/index.md)** 以了解特定用例（ControlNet、i2i 等）。
* 阅读 **[认证](./authentication.md)** 了解如何处理 API 密钥。

## 链接

- [GitHub 仓库](https://github.com/caru-ini/novelai-sdk)
- [PyPI](https://pypi.org/project/novelai-sdk/)
- [NovelAI 官网](https://novelai.net/)

## 免责声明

这是一个非官方的客户端库。不隶属于 NovelAI。
需要有效的 NovelAI 订阅。
