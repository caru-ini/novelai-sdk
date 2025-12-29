---
sidebar_position: 3
title: 認証
---

# 認証

NovelAI APIを利用するには認証が必要です。
`novelai-sdk` は複数の認証方法をサポートしています。

## 環境変数（推奨）

セキュリティのベストプラクティスとして、APIキーをコードにハードコードせず、環境変数を使用することを強く推奨します。

`NOVELAI_API_KEY` という環境変数にキーを設定すると、SDKは自動的にそれを読み込みます。

```bash
export NOVELAI_API_KEY="pst-..."
```

Pythonコード:

```python
from novelai import NovelAI

# 自動的に環境変数を読み込みます
client = NovelAI()
```

## .env ファイル

`python-dotenv` などを利用して `.env` ファイルから読み込むことも一般的です。

`.env`:
```env
NOVELAI_API_KEY=pst-your-api-key-here
```

Pythonコード:
```python
from dotenv import load_dotenv
from novelai import NovelAI

load_dotenv()
client = NovelAI()
```

## 直接指定

テストや簡単なスクリプトの場合、クライアントの初期化時に直接キーを渡すことも可能です。

```python
from novelai import NovelAI

client = NovelAI(api_key="pst-your-api-key-here")
```

:::warning
APIキーをGitHubなどの公開リポジトリにコミットしないように注意してください。
:::
