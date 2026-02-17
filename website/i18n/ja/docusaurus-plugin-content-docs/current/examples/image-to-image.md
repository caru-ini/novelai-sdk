# Image-to-Image (i2i)

既存の画像をベースにして、新しい画像を生成します。
ラフスケッチから清書したり、画像のスタイルを変更したりするのに使えます。

## 基本的な使い方

```python
from novelai.types import GenerateImageParams, I2iParams

# i2iパラメータの設定
i2i_params = I2iParams(
    image="input_sketch.png",  # Base64文字列またはファイルパス
    strength=0.7,
    noise=0.0,
)

params = GenerateImageParams(
    prompt="cyberpunk style, neon lights, highly detailed",
    model="nai-diffusion-4-5-full",
    i2i=i2i_params,
)

# 生成は通常通り
# images = client.image.generate(params)
```

## パラメータ

- **`image`** (必須): 元画像（ファイルパス、Base64文字列、PIL Image）
- **`strength`**: 元画像からの変化の度合い（`0.01`–`0.99`、デフォルト: `0.7`）
  - `0.0` に近いほど: 元の画像のまま
  - `1.0` に近いほど: プロンプト重視で元画像から離れる
- **`noise`**: バリエーションのためのノイズ量（`0.0`–`0.99`、デフォルト: `0.0`）
- **`seed`**: ノイズのランダムシード（省略時は自動生成）

:::tip
まず `strength=0.5` から始めて、元画像からの変化量に応じて調整するのがおすすめです。
:::
