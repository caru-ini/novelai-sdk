---
sidebar_position: 5
title: 開発
---

# 開発

`novelai-sdk` への貢献に興味を持っていただきありがとうございます。

## セットアップ

開発環境のセットアップ手順です。

```bash
git clone https://github.com/caru-ini/novelai-sdk.git
cd novelai-sdk
uv sync
```

## コード品質ツール

このプロジェクトでは `ruff` や `pyright` を使用してコード品質を維持しています。
`poethepoet` (uvと一緒にインストールされます) を使って簡単に実行できます。

```bash
# コードのフォーマット
uv run poe fmt

# コードのリント
uv run poe lint

# 型チェック
uv run poe check

# コミット前の全チェック
uv run poe pre-commit
```

## プルリクエスト

新機能の追加やバグ修正の際は、まずIssueを立てて議論することを推奨します。
プルリクエストを送る際は、以下のガイドラインに従ってください。

*   コミットメッセージは [Conventional Commits](https://www.conventionalcommits.org/) に従ってください。
*   `uv run poe pre-commit` がパスすることを確認してください。

## ライセンス

MITライセンスの下で公開されています。
