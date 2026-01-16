# FastAPI 集成

此示例演示了如何将 NovelAI SDK 集成到 [FastAPI](https://fastapi.tiangolo.com/) Web 应用程序中。

与 FastAPI 集成使您能够使用异步通信构建 Web 界面或 NovelAI 服务的 API 包装器。

## 实现概述

集成要点：
- **生命周期管理**: 使用 FastAPI 的 `lifespan` 在服务器启动时初始化 `AsyncNovelAI` 客户端，并在服务器停止时关闭它。
- **异步执行**: 利用 SDK 的异步方法高效处理多个请求。
- **图像响应**: 直接将生成的图像作为 PNG 响应返回给客户端。

## 示例代码

您可以在 [examples/10_fastapi_integration.py](https://github.com/caru-ini/novelai-sdk/blob/main/examples/10_fastapi_integration.py) 中找到完整的源代码。

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
    # API 密钥会自动从环境变量 NOVELAI_API_KEY 加载
    client = AsyncNovelAI()
    yield
    # 清理
    if client:
        await client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/generate")
async def generate_image(prompt: str):
    if client is None:
        raise HTTPException(status_code=500, detail="Client not initialized")
    
    params = GenerateImageParams(
        prompt=prompt,
        model="nai-diffusion-4-5-full",
        size="portrait",
    )
    
    images = await client.image.generate(params)
    if not images:
         raise HTTPException(status_code=500, detail="No image generated")
    
    # 将 PIL Image 转换为字节
    import io
    image = images[0]
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")
```

## 运行服务器

1. 安装所需的依赖项：
   ```bash
   pip install fastapi uvicorn
   ```

2. 使用 `uvicorn` 运行服务器：
   ```bash
   python examples/10_fastapi_integration.py
   ```

3. 通过在浏览器中访问以下 URL 生成图像：
   `http://localhost:8000/generate?prompt=1girl%2C%20cute%2C%20cat%20ears%2C%20maid`
