# キャラクターリファレンス

リファレンス画像を使用することで、生成されるキャラクターの外観を一貫させることができます。
特定のキャラクターを何度も生成したい場合に非常に有効です。

```python
from novelai.types import CharacterReference, GenerateImageParams

# リファレンス画像の定義
character_references = [
    CharacterReference(
        image="reference.png", # Base64文字列またはファイルパス
        type="character",
        fidelity=0.75, # 強度（0.0〜1.0）
    )
]

# 生成設定
params = GenerateImageParams(
    prompt="1girl, standing in a garden",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)

# 生成実行（clientは別途初期化済みとする）
# images = client.image.generate(params)
```
