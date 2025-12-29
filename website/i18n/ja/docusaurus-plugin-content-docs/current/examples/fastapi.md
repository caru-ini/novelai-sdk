# FastAPIとの統合

この例では、NovelAI SDKを[FastAPI](https://fastapi.tiangolo.com/) Webフレームワークと統合する方法を紹介します。

FastAPIと統合することで、非同期通信を利用したNovelAIサービスのWebインターフェースやAPIラッパーを簡単に構築できます。

## 実装の概要

統合における主要なポイントは以下の通りです：

- **ライフサイクル管理**: FastAPIの `lifespan` を使用して、サーバーの起動時に `AsyncNovelAI` クライアントを初期化し、停止時にクローズします。
- **非同期実行**: SDKの非同期メソッドを活用し、複数のリクエストを効率的に処理します。
- **画像レスポンス**: 生成された画像をPNG形式としてクライアントに直接返します。

## サンプルコード

完全なソースコードは [examples/10_fastapi_integration.py](https://github.com/caru-ini/novelai-sdk/blob/main/examples/10_fastapi_integration.py) で確認できます。

```python
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from novelai import AsyncNovelAI
from novelai.types import GenerateImageParams

client: AsyncNovelAI | None = None

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global client
    # API key is loaded from environment variable NOVELAI_API_KEY automatically
    client = AsyncNovelAI()
    yield
    # クリーンアップ
    if client:
        await client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/generate")
async def generate_image(prompt: str):
    if client is None:
        raise HTTPException(status_code=500, detail="クライアントが初期化されていません")
    
    params = GenerateImageParams(
        prompt=prompt,
        model="nai-diffusion-4-5-full",
        size="portrait",
    )
    
    images = await client.image.generate(params)
    if not images:
         raise HTTPException(status_code=500, detail="画像が生成されませんでした")
    
    # PIL Imageをbytesに変換
    import io
    image = images[0]
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")
```

## サーバーの起動方法

1. 必要な依存関係をインストールします：
   ```bash
   pip install fastapi uvicorn
   ```

2. `uvicorn` を使用してサーバーを起動します：

   ```bash
   python examples/10_fastapi_integration.py
   ```

3. ブラウザで以下のURLにアクセスして画像を生成します：
   `http://localhost:8000/generate?prompt=1girl%2C%20cute%2C%20cat%20ears%2C%20maid`
