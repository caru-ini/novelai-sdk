---
id: intro
sidebar_position: 1
title: 概要
slug: /
---

# NovelAI Python SDK

![intro](./images/intro.png)

[![PyPI version](https://img.shields.io/pypi/v/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![Python Version](https://img.shields.io/pypi/pyversions/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/caru-ini/novelai-sdk/blob/main/LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

NovelAIの画像生成APIのための、モダンで型安全なPython SDKです。
Pydantic v2による堅牢なバリデーションと完全な型ヒントを備え、開発者体験（DX）を重視して設計されています。

## 主な機能

- **完全な型安全性**: Python 3.10+対応、Pydantic v2による厳格なバリデーション。
- **高レベルAPI**: 直感的で使いやすいインターフェース。
- **最新機能への対応**: V4モデル、キャラクターリファレンス、ControlNetなどをサポート。
- **便利なユーティリティ**: PIL/Pillow統合、SSEストリーミングなど。

## 他ライブラリとの比較

| 機能                         | novelai-sdk | [novelai-api](https://github.com/Aedial/novelai-api) | [novelai-python](https://github.com/LlmKira/novelai-python) |
| ---------------------------- | :---------: | :--------------------------------------------------: | :---------------------------------------------------------: |
| 型安全 (Pydantic v2)         |      ✅      |                          ❌                           |                              ✅                              |
| 非同期サポート               |      ✅      |                          ✅                           |                              ✅                              |
| 画像生成                     |      ✅      |                          ✅                           |                              ✅                              |
| テキスト生成                 |      🚧      |                          ✅                           |                              ✅                              |
| **キャラクターリファレンス** |      ✅      |                          ❌                           |                              ❌                              |
| **マルチキャラクター配置**   |      ✅      |                          ❌                           |                              ✅                              |
| ControlNet / Vibe Transfer   |      ✅      |                          ❌                           |                              ✅                              |
| SSE ストリーミング           |      ✅      |                          ❌                           |                              ✅                              |
| Python 3.13+                 |      ✅      |                          ❌                           |                              ❌                              |
| アクティブメンテナンス       |      ✅      |                          ✅                           |                              ⚠️                              |

✅ 対応 | ❌ 未対応 | 🚧 予定 | ⚠️ 限定的なメンテナンス

## どこから始めますか？

- **[はじめに](./getting-started.md)**: インストールから最初の画像生成まで。
- **[認証](./authentication.md)**: APIキーの設定方法。
- **[機能例](./examples)**: 実践的な使用例。

## リンク

- [GitHub リポジトリ](https://github.com/caru-ini/novelai-sdk)
- [PyPI](https://pypi.org/project/novelai-sdk/)
- [NovelAI 公式サイト](https://novelai.net/)

## 免責事項

これは非公式のクライアントライブラリです。NovelAIとは提携していません。
利用には有効なNovelAIサブスクリプションが必要です。
