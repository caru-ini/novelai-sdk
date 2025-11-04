# NovelAI Python SDK

![intro](./images/intro.png)

[![PyPI version](https://img.shields.io/pypi/v/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![Python Version](https://img.shields.io/pypi/pyversions/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

[English](/README.md) | 日本語

NovelAIの画像生成APIのための、モダンで型安全なPython SDKです。Pydantic v2による堅牢なバリデーションと完全な型ヒントを備えています。

## 特徴

- Python 3.10+対応、完全な型ヒントとPydantic v2バリデーション
- 自動バリデーション機能を備えた高レベルな便利API
- 簡単な画像操作のためのPIL/Pillow組み込みサポート
- リアルタイム進捗監視のためのSSEストリーミング
- キャラクターリファレンス、ControlNet、マルチキャラクターポジショニング

## クイックスタート

### インストール

```bash
# pipを使用
pip install novelai-sdk

# uv を使用(推奨)
uv add novelai-sdk
```

### 基本的な使い方

```python
from novelai import NovelAI
from novelai.types import GenerateImageParams

# クライアントの初期化(APIキーはNOVELAI_API_KEY環境変数から取得)
client = NovelAI()

# 画像を生成
params = GenerateImageParams(
    prompt="1girl, cat ears, masterpiece, best quality",
    model="nai-diffusion-4-5-full",
    size="portrait",  # または (832, 1216)
    steps=23,
    scale=5.0,
)

images = client.image.generate(params)
images[0].save("output.png")
```

## ドキュメント

### 認証

環境変数または直接初期化でNovelAI APIキーを提供します:

```python
# .envファイルを使用(推奨)
from dotenv import load_dotenv
load_dotenv()
client = NovelAI()

# 環境変数
import os
os.environ["NOVELAI_API_KEY"] = "your_api_key_here"
client = NovelAI()

# 直接初期化
client = NovelAI(api_key="your_api_key_here")
```

### APIアーキテクチャ

このライブラリは、適切なデフォルト値と自動バリデーションを備えた高レベルAPIを提供します。低レベルAPIは内部的にRESTエンドポイントへの直接アクセスのために存在しますが、一般的な使用を意図したものではありません。

#### 高レベルAPI

```python
from novelai import NovelAI
from novelai.types import GenerateImageParams

client = NovelAI()
params = GenerateImageParams(
    prompt="a beautiful landscape",
    model="nai-diffusion-4-5-full",
    size="landscape",
    quality=True,
)
images = client.image.generate(params)
```

## 高度な機能

### キャラクターリファレンス

リファレンス画像で一貫したキャラクターの外観を維持:

```python
from novelai.types import CharacterReference

character_references = [
    CharacterReference(
        image="reference.png",
        type="character",
        fidelity=0.75,
    )
]

params = GenerateImageParams(
    prompt="1girl, standing",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)
```

### マルチキャラクターポジショニング

個別のプロンプトで複数のキャラクターを個別に配置:

```python
from novelai.types import Character

characters = [
    Character(
        prompt="1girl, red hair, blue eyes",
        enabled=True,
        position=(0.2, 0.5),
    ),
    Character(
        prompt="1boy, black hair, green eyes",
        enabled=True,
        position=(0.8, 0.5),
    ),
]

params = GenerateImageParams(
    prompt="two people standing",
    model="nai-diffusion-4-5-full",
    characters=characters,
)
```

### ControlNet(Vibe Transfer)

リファレンス画像で構図やポーズを制御:

```python
from novelai.types import ControlNetModel

params = GenerateImageParams(
    prompt="1girl, standing",
    model="nai-diffusion-4-5-full",
    controlnet_model=ControlNetModel(
        image="pose_reference.png",
        strength=0.6,
    ),
)
```

### ストリーミング生成

生成の進捗をリアルタイムで監視:

```python
from novelai.types import GenerateImageStreamParams
from base64 import b64decode

params = GenerateImageStreamParams(
    prompt="1girl, standing",
    model="nai-diffusion-4-5-full",
    stream="sse",
)

for chunk in client.image.generate_stream(params):
    image_data = b64decode(chunk.image)
    print(f"Received {len(image_data)} bytes")
```

### Image-to-Image

テキストプロンプトで既存の画像を変換:

```python
params = GenerateImageParams(
    prompt="cyberpunk style",
    model="nai-diffusion-4-5-full",
    image="input.png",
    strength=0.5,  # 0.0-1.0
)
```

### バッチ生成

複数のバリエーションを効率的に生成:

```python
params = GenerateImageParams(
    prompt="1girl, various poses",
    model="nai-diffusion-4-5-full",
    n_samples=4,
)

images = client.image.generate(params)
for i, img in enumerate(images):
    img.save(f"output_{i}.png")
```

## サンプル

`examples/`ディレクトリには実用的なデモが含まれています:

**基本的な使い方:**

- `01_basic_v4.py` - V4モデルの入門
- `08_img2img.py` - Image-to-image変換

**高度な機能:**

- `02_character_reference.py` - キャラクターリファレンス
- `03_character_prompts.py` - マルチキャラクターポジショニング
- `04_advanced_reference.py` - リファレンステクニックの組み合わせ
- `05_controlnet.py` - ControlNetの使用

**生成テクニック:**

- `06_batch_generation.py` - バッチ生成
- `07_streaming_generation.py` - ストリーミング進捗

サンプルの実行:

```bash
python examples/01_basic_v4.py
```

## ロードマップ

- [ ] 非同期サポート
- [ ] Vibe transferファイルサポート(`.naiv4vibe`,`.naiv4vibebundle`)
- [ ] Anlas消費量計算機
- [ ] 画像メタデータ抽出
- [ ] テキスト生成APIサポート

## 開発

### セットアップ

```bash
git clone https://github.com/caru-ini/novelai-sdk.git
cd novelai-sdk
uv sync
```

### コード品質

```bash
# コードのフォーマット
uv run poe fmt

# コードのリント
uv run poe lint

# 型チェック
uv run poe check

# poeをグローバルにインストールして簡単にアクセス
uv tool install poe

# コミット前にすべてのチェックを実行
uv run poe pre-commit
```

### テスト

テストは将来のリリースで追加される予定です。

## 必要要件

- Python 3.13+
- httpx (HTTPクライアント)
- Pillow (画像処理)
- Pydantic v2 (バリデーションと型安全性)
- python-dotenv (環境変数)

## 貢献

貢献を歓迎します。大きな変更の場合は、まずissueを開いてください。

### コミットガイドライン

```plaintext
{feat|fix|docs|style|refactor|test|chore}: 短い説明
```

1. リポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. コード品質チェックを実行 (`uv run poe pre-commit`)
4. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
5. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
6. プルリクエストを開く

## ライセンス

MITライセンス。詳細はLICENSEファイルを参照してください。

## リンク

- [NovelAI公式ウェブサイト](https://novelai.net/)
- [NovelAIドキュメント](https://docs.novelai.net/)
- [Issue](https://github.com/caru-ini/novelai-sdk/issues)

## 免責事項

これは非公式のクライアントライブラリです。NovelAIとは提携していません。有効なNovelAIサブスクリプションが必要です。

## 謝辞

NovelAIチームとすべての貢献者に感謝します。
