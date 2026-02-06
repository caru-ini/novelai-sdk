# 精密参照 (Precise Reference)

:::info
この機能は以前「キャラクター参照」と呼ばれていましたが、2026年2月に「精密参照」に名称変更されました。
:::

参照画像を使用して、キャラクターの外観や画風を制御できます。
精密参照を使うことで、一貫したキャラクターデザインの維持や、特定の画風の適用が可能になります。

## 主な機能

- **複数の参照画像**: 複数の参照を組み合わせて、異なるキャラクターや画風を適用可能
- **参照タイプ**:
  - `"character"`: キャラクターの外観のみ参照
  - `"style"`: 画風のみ参照
  - `"character&style"`: キャラクターと画風の両方を参照（デフォルト）
- **細かい制御**: 各参照に対してfidelityとstrengthを調整可能

## 基本的な使用例

```python
from novelai.types import CharacterReference, GenerateImageParams

# 単一のキャラクター参照
character_references = [
    CharacterReference(
        image="reference.png",  # Base64文字列またはファイルパス
        type="character",  # "character", "style", "character&style"のいずれか
        fidelity=1.0,  # 参照への忠実度（0.0〜1.0、デフォルト: 1.0）
        strength=1.0,  # 参照の重み（0.0〜1.0、デフォルト: 1.0）
    )
]

params = GenerateImageParams(
    prompt="1girl, standing in a garden",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)

# 生成実行（clientは別途初期化済みとする）
# images = client.image.generate(params)
```

## 応用: 複数参照の組み合わせ

異なる画像からキャラクターと画風を組み合わせる：

```python
character_references = [
    CharacterReference(
        image="character.png",
        type="character",  # キャラクターの外観のみ
        fidelity=1.0,
        strength=0.75,
    ),
    CharacterReference(
        image="style.png",
        type="style",  # 画風のみ
        fidelity=1.0,
        strength=0.75,
    ),
]

params = GenerateImageParams(
    prompt="1girl, standing, rating:general, very aesthetic",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)
```

## パラメータ

- **`image`**（必須）: 参照画像（ファイルパス、Base64文字列、またはPIL Image）
- **`type`**: 参照タイプ
  - `"character"`: キャラクターの外観のみ適用
  - `"style"`: 画風のみ適用
  - `"character&style"`: 両方を適用（デフォルト）
- **`fidelity`**: 参照画像への忠実度（0.0〜1.0、デフォルト: 1.0）
- **`strength`**: 複数参照使用時の相対的な重み（0.0〜1.0、デフォルト: 1.0）
