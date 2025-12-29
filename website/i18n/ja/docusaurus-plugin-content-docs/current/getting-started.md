---
sidebar_position: 2
title: はじめに
---

# はじめに

NovelAI SDKを使って、Pythonで簡単に画像を生成する方法を解説します。
プログラミング初心者の方でも分かるように、ステップバイステップで説明します。

## 1. インストール

まずは、`novelai-sdk` をインストールしましょう。

:::info
Python 3.10 以上が必要です。
:::

ターミナル（コマンドプロンプト）を開いて、以下のコマンドを入力してください。

```bash
pip install novelai-sdk
```

`uv` を使っている場合はこちら（推奨）：

```bash
uv add novelai-sdk
```

## 2. APIキーの準備

NovelAIの機能を使うには、**APIキー**が必要です。

1.  [NovelAIのウェブサイト](https://novelai.net/)にログインします。
2.  設定画面（歯車アイコン）を開きます。
3.  「Account」タブの「Get API Key」をクリックしてキーを取得します。

取得したキーは、プログラムに直接書くこともできますが、セキュリティのため**環境変数**または`.env`ファイルを使うのがおすすめです。

### 方法A: .envファイルを使う（おすすめ）

プロジェクトのフォルダに `.env` という名前のファイルを作り、以下のように書きます。

```env
NOVELAI_API_KEY=pst-あなたのAPIキーをここに貼り付け
```

### 方法B: 直接コードに書く（テスト用）

```python
client = NovelAI(api_key="pst-あなたのAPIキー")
```

## 3. 最初の画像を生成する

準備ができたら、さっそく画像を生成してみましょう！
以下のコードを `generate.py` という名前で保存して実行してください。

```python
import os
from novelai import NovelAI
from novelai.types import GenerateImageParams

# 1. クライアントを作ります
# 環境変数 NOVELAI_API_KEY が設定されていれば、引数は不要です
client = NovelAI()

# 2. 生成の設定をします
params = GenerateImageParams(
    # プロンプト（描きたいもの）
    prompt="1girl, cat ears, masterpiece, best quality",
    # モデルの選択（ここでは最新のV4を使用）
    model="nai-diffusion-4-5-full",
    # 画像サイズ（portrait, landscape, squareなど）
    size="portrait",
    # ステップ数（28くらいがおすすめ）
    steps=28,
    # プロンプトへの従順さ（5.0〜6.0くらいが標準）
    scale=5.0,
)

# 3. 画像を生成します
print("画像を生成中...")
images = client.image.generate(params)

# 4. 保存します
if images:
    filename = "output.png"
    images[0].save(filename)
    print(f"保存しました: {filename}")
else:
    print("生成に失敗しました")
```

実行コマンド:

```bash
python generate.py
```

成功すると、同じフォルダに `output.png` が作成されます！

## 次のステップ

*   **[認証の詳細](./authentication.md)**: APIキーの扱い方について詳しく知りたい場合。
*   **[機能例](./examples)**: 特定のキャラクターを出したり、ポーズを指定したい場合。
