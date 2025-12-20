"""FastAPI integration example with NovelAI

This example demonstrates how to integrate the NovelAI SDK into a FastAPI web application.
"""

import io
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

from novelai import AsyncNovelAI
from novelai.types import GenerateImageParams

load_dotenv()

# Global instance of the NovelAI client
client: AsyncNovelAI | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI application lifecycle management.
    """
    global client
    # API key is loaded from environment variable NOVELAI_API_KEY automatically
    client = AsyncNovelAI()

    yield

    # Ensure the client is closed
    if client:
        await client.close()


app = FastAPI(title="NovelAI Integration Example", lifespan=lifespan)


@app.get("/generate", responses={200: {"content": {"image/png": {}}}})
async def generate_image(prompt: str = "landscape, masterpiece, high quality"):
    """
    Generate an image based on the provided prompt and return it as a PNG response.
    """
    if client is None:
        raise HTTPException(status_code=500, detail="NovelAI client is not initialized")

    try:
        # Configuration for image generation parameters
        # Style follows examples/09_async_generation.py
        params = GenerateImageParams(
            prompt=prompt,
            model="nai-diffusion-4-5-full",
            size="portrait",
            steps=23,
            scale=5.0,
            uc_preset="strong",
            quality=True,
            sampler="k_euler_ancestral",
        )

        # Image generation request
        images = await client.image.generate(params)

        if not images:
            raise HTTPException(status_code=500, detail="No image generated")

        # Get the first image
        image = images[0]

        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        return Response(content=img_bytes, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
