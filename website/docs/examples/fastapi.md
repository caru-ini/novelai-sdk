# FastAPI Integration

This example demonstrates how to integrate the NovelAI SDK into a [FastAPI](https://fastapi.tiangolo.com/) web application.

Integrating with FastAPI allows you to build web interfaces or API wrappers around NovelAI's services using asynchronous communication.

## Implementation Overview

Key points of the integration:
- **Lifecycle Management**: Use FastAPI's `lifespan` to initialize the `AsyncNovelAI` client when the server starts and close it when the server stops.
- **Asynchronous Execution**: Utilize the SDK's asynchronous methods to handle multiple requests efficiently.
- **Image Response**: Return generated images directly to the client as a PNG response.

## Example Code

You can find the full source code in [examples/10_fastapi_integration.py](https://github.com/caru-ini/novelai-sdk/blob/main/examples/10_fastapi_integration.py).

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
    # Cleanup
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
    
    # Convert PIL Image to bytes
    import io
    image = images[0]
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")
```

## Running the Server

1. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

2. Run the server using `uvicorn`:
   ```bash
   python examples/10_fastapi_integration.py
   ```

3. Generate an image by visiting the following URL in your browser:
   `http://localhost:8000/generate?prompt=1girl%2C%20cute%2C%20cat%20ears%2C%20maid`
