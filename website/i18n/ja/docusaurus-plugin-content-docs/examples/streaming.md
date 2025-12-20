# ストリーミング生成

画像生成には数秒〜数十秒かかる場合があります。
SSE (Server-Sent Events) ストリーミングを使用すると、生成の過程をリアルタイムで受け取ることができます。
これにより、ユーザーに「動いている」ことをフィードバックでき、体感待ち時間を短縮できます。

```python
from novelai.types import GenerateImageStreamParams
from base64 import b64decode

# クライアント初期化（省略）

params = GenerateImageStreamParams(
    prompt="masterpiece, best quality, scenery, detailed",
    model="nai-diffusion-4-5-full",
    stream="sse", # ストリームモードを有効化
    steps=28,
)

# generate_stream メソッドを使用
for chunk in client.image.generate_stream(params):
    if chunk.image:
        image_data = b64decode(chunk.image)
        print(f"Received chunk: {len(image_data)} bytes")
        # ここでフロントエンドにデータを送ったり、プレビューを表示したりできます
```
