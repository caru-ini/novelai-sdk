# Image-to-Image (i2i)

既存の画像をベースにして、新しい画像を生成します。
ラフスケッチから清書したり、画像のスタイルを変更したりするのに使えます。

```python
from novelai.types import GenerateImageParams

params = GenerateImageParams(
    prompt="cyberpunk style, neon lights, highly detailed",
    model="nai-diffusion-4-5-full",
    
    # 入力画像（Base64文字列またはファイルパス）
    image="input_sketch.png",
    
    # 変更の強度 (Strength)
    # 0.0 に近いほど元の画像のまま
    # 1.0 に近いほどプロンプト重視で元画像から離れる
    strength=0.7, 
)

# 生成は通常通り
# images = client.image.generate(params)
```
