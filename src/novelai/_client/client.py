"""High-level NovelAI client with user-friendly interface"""

from __future__ import annotations

from typing import Iterator, cast

from PIL import Image

from .._api.client import _APIClient
from ..types.api.image import (
    ImageGenerationRequest,
    ImageStreamChunk,
    StreamImageGenerationRequest,
)
from ..types.user.image import GenerateImageParams, GenerateImageStreamParams


class ImageGeneration:
    """High-level image generation interface"""

    def __init__(self, client: NovelAI):
        self._client = client

    def generate(
        self,
        params: GenerateImageParams,
    ) -> list[Image.Image]:
        """Generate image(s) using user-friendly parameter structure TODO:generate docs later"""

        request = cast(ImageGenerationRequest, params.to_api_request(self._client))

        return self._client.api_client.image.generate(request)

    def generate_stream(
        self,
        params: GenerateImageStreamParams,
    ) -> Iterator[ImageStreamChunk]:
        """Generate image(s) with streaming"""

        request = cast(
            StreamImageGenerationRequest, params.to_api_request(self._client)
        )
        yield from self._client.api_client.image.generate_stream(request)


class NovelAI:
    """High-level client for NovelAI."""

    def __init__(
        self,
        api_key: str | None = None,
        image_base: str | None = None,
        text_base: str | None = None,
        api_base: str | None = None,
        timeout: float = 120.0,
    ):
        """Initialize NovelAI client

        Args:
            api_key: NovelAI API key (Bearer token)
            image_base: Image API base URL (e.g. https://image.novelai.net)
            text_base: Text API base URL (e.g. https://text.novelai.net)
            api_base: API base URL(e.g. https://api.novelai.net)
            timeout: Request timeout in seconds
        """
        self.api_client = _APIClient(api_key=api_key, timeout=timeout)
        self.image = ImageGeneration(self)

    @property
    def api_key(self) -> str:
        """Get the API key"""
        api_key = self.api_client.api_key
        if api_key is None:
            raise ValueError("API key is not set")
        return api_key

    @property
    def timeout(self) -> float:
        """Get the timeout"""
        return self.api_client.timeout

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
        self.api_client.close()
