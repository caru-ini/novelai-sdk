"""Low-level NovelAI API client - Direct API calls with native schema"""

from __future__ import annotations

import base64
import io
import os
import zipfile
from pathlib import Path
from typing import Iterator

import httpx
from PIL import Image

from ..exceptions import (
    AuthenticationError,
    InvalidRequestError,
    MissingAPIKeyError,
    NetworkError,
    NovelAIError,
    RateLimitError,
    ServerError,
)
from ..types.api.image import (
    EncodeVibeRequest,
    ImageGenerationRequest,
    ImageStreamChunk,
    StreamImageGenerationRequest,
)


class ImageAPI:
    """Image generation API endpoints"""

    def __init__(self, api_base: str | None, client: _APIClient):
        self._client = client
        self.api_base = (
            api_base or os.getenv("NOVELAI_IMAGE_BASE") or "https://image.novelai.net"
        )

    def encode_vibe(self, request: EncodeVibeRequest):
        """Generate vibe-transfer data from base64 image

        Args:
            request: Complete EncodeVibeRequest object

        Returns:
            Base64 String of vibe-transfer data

        Raises:
            AuthenticationError: Invalid API key or insufficient credits
            InvalidRequestError: Invalid parameters
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
            NetworkError: Network connection error
        """
        try:
            response = self._client.client.post(
                f"{self.api_base}/ai/encode-vibe",
                content=request.model_dump_json(exclude_none=True),
            )
            return base64.b64encode(response.content).decode("utf-8")
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def generate(self, request: ImageGenerationRequest) -> list[Image.Image]:
        """Generate image(s) using /ai/generate-image endpoint

        Args:
            request: Complete ImageGenerationRequest object

        Returns:
            List of PIL Image objects

        Raises:
            AuthenticationError: Invalid API key or insufficient credits
            InvalidRequestError: Invalid parameters
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
            NetworkError: Network connection error
        """
        try:
            Path("request.json").write_text(request.model_dump_json(exclude_none=True))
            response = self._client.client.post(
                f"{self.api_base}/ai/generate-image",
                content=request.model_dump_json(exclude_none=True),
            )

            content = self._client.handle_response(response)
            images = self._client.extract_images_from_zip(content)
            return images

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def generate_stream(
        self, request: StreamImageGenerationRequest
    ) -> Iterator[ImageStreamChunk]:
        """Generate image(s) using /ai/generate-image-stream endpoint

        Args:
            request: Complete StreamImageGenerationRequest object with streaming parameters

        Yields:
            Image chunks as ImageStreamChunk objects

        Raises:
            AuthenticationError: Invalid API key or insufficient credits
            InvalidRequestError: Invalid parameters
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
            NetworkError: Network connection error
        """
        try:
            with self._client.client.stream(
                "POST",
                f"{self.api_base}/ai/generate-image-stream",
                content=request.model_dump_json(exclude_none=True),
            ) as response:
                if response.status_code not in (200, 201):
                    # Read full response for error handling
                    content = response.read()
                    temp_response = httpx.Response(
                        status_code=response.status_code,
                        content=content,
                        request=response.request,
                    )
                    self._client.handle_response(temp_response)

                # Stream chunks
                for chunk in response.iter_lines():
                    if chunk and chunk.startswith("data: "):
                        yield ImageStreamChunk.from_text_chunk(chunk)

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e


class _APIClient:
    """Low-level client for NovelAI API

    This client works directly with the native NovelAI API schema.
    Use ImageGenerationRequest objects directly.

    For high-level client, use `novelai.NovelAI` class instead.
    """

    def __init__(
        self,
        api_key: str | None = None,
        image_base: str | None = None,
        text_base: str | None = None,
        api_base: str | None = None,
        timeout: float = 120.0,
    ):
        """Initialize NovelAI API client

        Args:
            api_key: NovelAI API key (Bearer token)
            timeout: Request timeout in seconds

        Raises:
            MissingAPIKeyError: If API key is not provided
        """
        self.text_base = (
            text_base or os.getenv("NOVELAI_TEXT_BASE") or "https://text.novelai.net"
        )
        self.api_base = (
            api_base or os.getenv("NOVELAI_API_BASE") or "https://api.novelai.net"
        )
        self.api_key = api_key or os.getenv("NOVELAI_API_KEY")
        if not self.api_key:
            raise MissingAPIKeyError("API key is required")

        self.timeout = timeout
        self.client = httpx.Client(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        # API endpoints
        self.image = ImageAPI(image_base, self)

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        self.close()

    def close(self):
        """Close the HTTP client"""
        self.client.close()

    def handle_response(self, response: httpx.Response) -> bytes:
        """Handle API response and raise appropriate exceptions"""
        if response.status_code in (200, 201):
            return response.content
        elif response.status_code == 400:
            raise InvalidRequestError(f"Invalid request: {response.text}")
        elif response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        elif response.status_code == 402:
            raise AuthenticationError("Insufficient credits or subscription required")
        elif response.status_code == 409:
            raise InvalidRequestError(f"Conflict: {response.text}")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif 500 <= response.status_code < 600:
            raise ServerError(f"Server error: {response.status_code}")
        else:
            raise NovelAIError(
                f"Unexpected error: {response.status_code} - {response.text}"
            )

    def extract_images_from_zip(self, zip_data: bytes) -> list[Image.Image]:
        """Extract images from ZIP response"""
        images: list[Image.Image] = []

        try:
            with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
                for filename in zf.namelist():
                    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                        with zf.open(filename) as image_file:
                            image = Image.open(io.BytesIO(image_file.read()))
                            images.append(image)
        except zipfile.BadZipFile:
            # If it's not a ZIP, try to open directly as image
            try:
                image = Image.open(io.BytesIO(zip_data))
                images.append(image)
            except Exception as e:
                raise InvalidRequestError(
                    f"Failed to parse response as image: {str(e)}"
                )

        return images
