# インペインティング

既存の画像のマスクで指定した領域を再生成します。
マスク画像を使って、画像の一部だけを再生成し、残りはそのまま保持できます。

## 基本的な使い方

```python
from novelai.types import GenerateImageParams, InpaintParams

inpaint_params = InpaintParams(
    image="source.png",   # 元画像（ファイルパス、Base64、PIL Image）
    mask="mask.png",      # マスク画像（白=再生成、黒=保持）
    strength=1.0,
)

# モデルは自動的にインペインティング用バリアントに切り替えられます
# (例: nai-diffusion-4-5-full -> nai-diffusion-4-5-full-inpainting)
params = GenerateImageParams(
    prompt="1girl, standing, smile",
    model="nai-diffusion-4-5-full",
    inpaint=inpaint_params,
)

# images = client.image.generate(params)
```

## マスクの形式

マスク画像で再生成する領域を指定します:

- **白** (`#FFFFFF`): 再生成する領域（インペイント）
- **黒** (`#000000`): そのまま保持する領域

マスクはAPI要件に合わせて自動的に前処理（二値化・リサイズ）されます。

## パラメータ

- **`image`** (必須): 元画像（ファイルパス、Base64文字列、PIL Image）
- **`mask`** (必須): インペイント領域を定義するマスク画像（ファイルパス、Base64文字列、PIL Image）
- **`strength`**: インペインティングの強度（`0.01`–`1.0`、デフォルト: `1.0`）
  - `1.0`: マスク領域を完全に再生成
  - 低い値: 元のコンテンツと新しい生成をブレンド
- **`seed`**: ノイズのランダムシード（省略時は自動生成）

:::info
モデルは自動的にインペインティング用バリアントに切り替えられます（例: `nai-diffusion-4-5-full` → `nai-diffusion-4-5-full-inpainting`）。手動でインペインティングモデルを指定する必要はありません。
:::

:::tip
変更したい領域よりもマスクを少し大きめに作ると、シームレスなブレンドのためのコンテキストをモデルに与えられて効果的です。
:::
