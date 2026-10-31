"""Low-level NovelAI API client - Direct API calls with native schema"""

from __future__ import annotations

import base64
import copy
import hashlib
import hmac
import io
import json
import os
import warnings
import zipfile
from typing import Any, AsyncIterator, Iterator

import httpx
from PIL import Image
from pydantic import BaseModel, TypeAdapter, ValidationError

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
    BaseImageGenerationRequest,
    EncodeVibeRequest,
    ImageGenerationRequest,
    ImageStreamChunk,
    StreamImageGenerationRequest,
)
from ..types.api.tags import (
    JpTagSuggestion,
    TagSuggestionResponse,
)
from ..types.api.tools import AugmentImageRequest, UpscaleImageRequest
from ..types.user.user import Subscription

_JP_TAG_LIST_ADAPTER = TypeAdapter(list[JpTagSuggestion])
_MultipartFiles = dict[str, tuple[str, bytes, str]]


class _CacheKeyErrorDetails(BaseModel):
    invalidKeys: list[str] = []


class _CacheKeyError(BaseModel):
    message: str | None = None
    details: _CacheKeyErrorDetails = _CacheKeyErrorDetails()


class BaseAPIClient:
    """Base class containing shared logic for both sync and async clients"""

    _cache_secret: bytes
    _cached_image_keys: set[str]

    @staticmethod
    def multipart_files(body: dict[str, Any]) -> _MultipartFiles:
        """Encode a request body as multipart parts with each image as its own part

        The body is modified in place: image fields are replaced by part names.
        """
        files: _MultipartFiles = {}
        part_names: dict[str, str] = {}

        def attach(data: str, name: str) -> str:
            if data not in part_names:
                part_names[data] = name
                files[name] = ("blob", base64.b64decode(data), "image/png")
            return part_names[data]

        for field in ("image", "mask"):
            if body.get(field):
                body[field] = attach(body[field], field)

        parameters: dict[str, Any] = body.get("parameters") or {}
        for field in ("image", "mask", "reference_image"):
            if parameters.get(field):
                parameters[field] = attach(parameters[field], field)
        for field, part_prefix in (
            ("reference_image_multiple_cached", "ref_multiple"),
            ("director_reference_images_cached", "director_ref"),
        ):
            entries: list[dict[str, str]] = parameters.get(field) or []
            for index, entry in enumerate(entries):
                if entry.get("data"):
                    entry["data"] = attach(entry["data"], f"{part_prefix}_{index}")

        request_json = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
        files["request"] = ("blob", request_json.encode(), "application/json")
        return files

    def cache_images(self, parameters: dict[str, Any]) -> set[str]:
        """Replace images the server already holds with their cache keys

        Returns:
            Keys of the images sent for the first time
        """
        new_keys: set[str] = set()

        def cache_key(data: str) -> tuple[str, bool]:
            key = hmac.new(self._cache_secret, data.encode(), hashlib.sha256)
            digest = key.hexdigest()
            if digest in self._cached_image_keys:
                return digest, True
            self._cached_image_keys.add(digest)
            new_keys.add(digest)
            return digest, False

        for field in ("image", "mask", "reference_image"):
            data: str | None = parameters.get(field)
            if data:
                key, cached = cache_key(data)
                parameters[f"{field}_cache_secret_key"] = key
                if cached:
                    del parameters[field]

        for field in ("reference_image_multiple", "director_reference_images"):
            images: list[str] | None = parameters.get(field)
            if not images:
                continue
            entries: list[dict[str, str]] = []
            for data in images:
                key, cached = cache_key(data)
                entries.append(
                    {"cache_secret_key": key}
                    if cached
                    else {"cache_secret_key": key, "data": data}
                )
            parameters[f"{field}_cached"] = entries
            del parameters[field]

        return new_keys

    def _generation_files(
        self, body: dict[str, Any]
    ) -> tuple[_MultipartFiles, set[str]]:
        sent = copy.deepcopy(body)
        new_keys = self.cache_images(sent["parameters"])
        return self.multipart_files(sent), new_keys

    @staticmethod
    def invalid_cache_keys(response: httpx.Response) -> set[str] | None:
        """Cache keys the server no longer holds, if that is why the request failed"""
        if response.status_code != 400:
            return None
        try:
            error = _CacheKeyError.model_validate_json(response.content)
        except ValidationError:
            return None
        if error.message != "INVALID_CACHE_KEYS":
            return None
        return set(error.details.invalidKeys)

    @staticmethod
    def handle_response(response: httpx.Response) -> bytes:
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

    @staticmethod
    def extract_images_from_zip(zip_data: bytes) -> list[Image.Image]:
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
            response = self._client.post_multipart(
                f"{self.api_base}/ai/encode-vibe", request
            )
            content = self._client.handle_response(response)
            return base64.b64encode(content).decode("utf-8")
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
            response = self._client.post_generation(
                f"{self.api_base}/ai/generate-image", request
            )

            content = self._client.handle_response(response)
            images = self._client.extract_images_from_zip(content)
            return images

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def augment(self, request: AugmentImageRequest) -> list[Image.Image]:
        """Transform an image using /ai/augment-image (Director Tools)

        Args:
            request: Complete AugmentImageRequest object

        Returns:
            List of PIL Image objects (some tools, e.g. bg-removal,
            may return more than one image)

        Raises:
            AuthenticationError: Invalid API key or insufficient credits
            InvalidRequestError: Invalid parameters
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
            NetworkError: Network connection error
        """
        try:
            response = self._client.post_multipart(
                f"{self.api_base}/ai/augment-image", request
            )

            content = self._client.handle_response(response)
            images = self._client.extract_images_from_zip(content)
            return images

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def upscale(self, request: UpscaleImageRequest) -> list[Image.Image]:
        """Upscale an image 2x using /ai/upscale

        Args:
            request: Complete UpscaleImageRequest object

        Returns:
            List of PIL Image objects (normally a single image)

        Raises:
            AuthenticationError: Invalid API key or insufficient credits
            InvalidRequestError: Invalid parameters
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
            NetworkError: Network connection error
        """
        try:
            response = self._client.post_multipart(
                f"{self.api_base}/ai/upscale", request
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
            response = self._client.post_generation(
                f"{self.api_base}/ai/generate-image-stream", request, stream=True
            )
            try:
                if response.status_code not in (200, 201):
                    response.read()
                    self._client.handle_response(response)

                for chunk in response.iter_lines():
                    if chunk and chunk.startswith("data: "):
                        yield ImageStreamChunk.from_text_chunk(chunk)
            finally:
                response.close()

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def suggest_tags(self, model: str, prompt: str) -> TagSuggestionResponse:
        """Get tag suggestions using /ai/generate-image/suggest-tags

        Args:
            model: Image model (e.g. nai-diffusion-4-5-full)
            prompt: Incomplete tag query

        Returns:
            TagSuggestionResponse with the suggested tags

        Raises:
            AuthenticationError: Invalid API key
            InvalidRequestError: Invalid parameters
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
            NetworkError: Network connection error
        """
        try:
            response = self._client.client.get(
                f"{self.api_base}/ai/generate-image/suggest-tags",
                params={"model": model, "prompt": prompt},
            )
            content = self._client.handle_response(response)
            return TagSuggestionResponse.model_validate_json(content)
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def suggest_tags_jp(self, model: str, prompt: str) -> list[JpTagSuggestion]:
        """Get Japanese tag suggestions (lang=jp) with English tag mapping

        The jp variant returns a bare JSON array with a different shape
        than the English response.

        Args:
            model: Image model (e.g. nai-diffusion-4-5-full)
            prompt: Incomplete tag query in Japanese

        Returns:
            List of JpTagSuggestion

        Raises:
            AuthenticationError: Invalid API key
            InvalidRequestError: Invalid parameters
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
            NetworkError: Network connection error
        """
        try:
            response = self._client.client.get(
                f"{self.api_base}/ai/generate-image/suggest-tags",
                params={"model": model, "prompt": prompt, "lang": "jp"},
            )
            content = self._client.handle_response(response)
            return _JP_TAG_LIST_ADAPTER.validate_json(content)
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e


class UserAPI:
    """User account API endpoints

    Served from the image host: NovelAI retired ``/user/*`` on
    api.novelai.net, which now returns 400 "update to the image URL".
    """

    def __init__(self, api_base: str, client: _APIClient):
        self._client = client
        self.api_base = api_base

    def get_subscription(self) -> Subscription:
        """Fetch the account subscription using /user/subscription

        Returns:
            Subscription with tier, perks, and remaining Anlas balance

        Raises:
            AuthenticationError: Invalid API key
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
            NetworkError: Network connection error
        """
        try:
            response = self._client.client.get(
                f"{self.api_base}/user/subscription",
            )
            content = self._client.handle_response(response)
            return Subscription.model_validate_json(content)
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e


class AsyncImageAPI:
    """Async Image generation API endpoints"""

    def __init__(self, api_base: str | None, client: _AsyncAPIClient):
        self._client = client
        self.api_base = (
            api_base or os.getenv("NOVELAI_IMAGE_BASE") or "https://image.novelai.net"
        )

    async def encode_vibe(self, request: EncodeVibeRequest):
        """Generate vibe-transfer data from base64 image asynchronously"""
        try:
            response = await self._client.post_multipart(
                f"{self.api_base}/ai/encode-vibe", request
            )
            content = self._client.handle_response(response)
            return base64.b64encode(content).decode("utf-8")
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    async def generate(self, request: ImageGenerationRequest) -> list[Image.Image]:
        """Generate image(s) using /ai/generate-image endpoint asynchronously"""
        try:
            response = await self._client.post_generation(
                f"{self.api_base}/ai/generate-image", request
            )

            content = self._client.handle_response(response)
            images = self._client.extract_images_from_zip(content)
            return images

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    async def augment(self, request: AugmentImageRequest) -> list[Image.Image]:
        """Transform an image using /ai/augment-image (Director Tools) asynchronously"""
        try:
            response = await self._client.post_multipart(
                f"{self.api_base}/ai/augment-image", request
            )

            content = self._client.handle_response(response)
            images = self._client.extract_images_from_zip(content)
            return images

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    async def upscale(self, request: UpscaleImageRequest) -> list[Image.Image]:
        """Upscale an image 2x using /ai/upscale asynchronously"""
        try:
            response = await self._client.post_multipart(
                f"{self.api_base}/ai/upscale", request
            )

            content = self._client.handle_response(response)
            images = self._client.extract_images_from_zip(content)
            return images

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    async def generate_stream(
        self, request: StreamImageGenerationRequest
    ) -> AsyncIterator[ImageStreamChunk]:
        """Generate image(s) using /ai/generate-image-stream endpoint asynchronously"""
        try:
            response = await self._client.post_generation(
                f"{self.api_base}/ai/generate-image-stream", request, stream=True
            )
            try:
                if response.status_code not in (200, 201):
                    await response.aread()
                    self._client.handle_response(response)

                async for chunk in response.aiter_lines():
                    if chunk and chunk.startswith("data: "):
                        yield ImageStreamChunk.from_text_chunk(chunk)
            finally:
                await response.aclose()

        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    async def suggest_tags(self, model: str, prompt: str) -> TagSuggestionResponse:
        """Get tag suggestions using /ai/generate-image/suggest-tags asynchronously"""
        try:
            response = await self._client.client.get(
                f"{self.api_base}/ai/generate-image/suggest-tags",
                params={"model": model, "prompt": prompt},
            )
            content = self._client.handle_response(response)
            return TagSuggestionResponse.model_validate_json(content)
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    async def suggest_tags_jp(self, model: str, prompt: str) -> list[JpTagSuggestion]:
        """Get Japanese tag suggestions (lang=jp) asynchronously"""
        try:
            response = await self._client.client.get(
                f"{self.api_base}/ai/generate-image/suggest-tags",
                params={"model": model, "prompt": prompt, "lang": "jp"},
            )
            content = self._client.handle_response(response)
            return _JP_TAG_LIST_ADAPTER.validate_json(content)
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e


class AsyncUserAPI:
    """Async User account API endpoints"""

    def __init__(self, api_base: str, client: _AsyncAPIClient):
        self._client = client
        self.api_base = api_base

    async def get_subscription(self) -> Subscription:
        """Fetch the account subscription using /user/subscription asynchronously"""
        try:
            response = await self._client.client.get(
                f"{self.api_base}/user/subscription",
            )
            content = self._client.handle_response(response)
            return Subscription.model_validate_json(content)
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e


class _APIClient(BaseAPIClient):
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
        if api_base is not None or os.getenv("NOVELAI_API_BASE"):
            warnings.warn(
                "api_base / NOVELAI_API_BASE is deprecated: no SDK endpoint uses "
                "api.novelai.net anymore. Use image_base instead.",
                DeprecationWarning,
                stacklevel=2,
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
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        self._cache_secret = os.urandom(32)
        self._cached_image_keys = set()

        # API endpoints
        self.image = ImageAPI(image_base, self)
        self.user = UserAPI(self.image.api_base, self)

    def post_multipart(self, url: str, request: BaseModel) -> httpx.Response:
        """POST a request as multipart form data, like the web UI"""
        body = request.model_dump(mode="json", exclude_none=True)
        return self.client.post(url, files=self.multipart_files(body))

    def post_generation(
        self, url: str, request: BaseImageGenerationRequest, *, stream: bool = False
    ) -> httpx.Response:
        """POST a generation request, resending cached images once if they expired"""
        body = request.model_dump(mode="json", exclude_none=True)
        response = self._send_generation(url, body, stream)
        if response.status_code == 400:
            response.read()
            invalid_keys = self.invalid_cache_keys(response)
            if invalid_keys is not None:
                response.close()
                self._cached_image_keys -= invalid_keys
                response = self._send_generation(url, body, stream)
        return response

    def _send_generation(
        self, url: str, body: dict[str, Any], stream: bool
    ) -> httpx.Response:
        files, new_keys = self._generation_files(body)
        request = self.client.build_request("POST", url, files=files)
        response = self.client.send(request, stream=stream)
        if response.status_code not in (200, 201):
            self._cached_image_keys -= new_keys
        return response

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


class _AsyncAPIClient(BaseAPIClient):
    """Low-level async client for NovelAI API"""

    def __init__(
        self,
        api_key: str | None = None,
        image_base: str | None = None,
        text_base: str | None = None,
        api_base: str | None = None,
        timeout: float = 120.0,
    ):
        self.text_base = (
            text_base or os.getenv("NOVELAI_TEXT_BASE") or "https://text.novelai.net"
        )
        if api_base is not None or os.getenv("NOVELAI_API_BASE"):
            warnings.warn(
                "api_base / NOVELAI_API_BASE is deprecated: no SDK endpoint uses "
                "api.novelai.net anymore. Use image_base instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        self.api_base = (
            api_base or os.getenv("NOVELAI_API_BASE") or "https://api.novelai.net"
        )
        self.api_key = api_key or os.getenv("NOVELAI_API_KEY")
        if not self.api_key:
            raise MissingAPIKeyError("API key is required")

        self.timeout = timeout
        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        self._cache_secret = os.urandom(32)
        self._cached_image_keys = set()

        # API endpoints
        self.image = AsyncImageAPI(image_base, self)
        self.user = AsyncUserAPI(self.image.api_base, self)

    async def post_multipart(self, url: str, request: BaseModel) -> httpx.Response:
        """POST a request as multipart form data, like the web UI"""
        body = request.model_dump(mode="json", exclude_none=True)
        return await self.client.post(url, files=self.multipart_files(body))

    async def post_generation(
        self, url: str, request: BaseImageGenerationRequest, *, stream: bool = False
    ) -> httpx.Response:
        """POST a generation request, resending cached images once if they expired"""
        body = request.model_dump(mode="json", exclude_none=True)
        response = await self._send_generation(url, body, stream)
        if response.status_code == 400:
            await response.aread()
            invalid_keys = self.invalid_cache_keys(response)
            if invalid_keys is not None:
                await response.aclose()
                self._cached_image_keys -= invalid_keys
                response = await self._send_generation(url, body, stream)
        return response

    async def _send_generation(
        self, url: str, body: dict[str, Any], stream: bool
    ) -> httpx.Response:
        files, new_keys = self._generation_files(body)
        request = self.client.build_request("POST", url, files=files)
        response = await self.client.send(request, stream=stream)
        if response.status_code not in (200, 201):
            self._cached_image_keys -= new_keys
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        await self.close()

    async def close(self):
        """Close the Async HTTP client"""
        await self.client.aclose()
