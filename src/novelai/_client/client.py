"""High-level NovelAI client with user-friendly interface

This module provides the main interface for interacting with NovelAI's API.
The client supports image generation with automatic validation and type safety.

Example:
    Basic usage with environment variable:
        >>> from novelai import NovelAI
        >>> from novelai.types import GenerateImageParams
        >>>
        >>> # API key loaded from NOVELAI_API_KEY environment variable
        >>> client = NovelAI()
        >>> params = GenerateImageParams(prompt="1girl, cat ears")
        >>> images = client.image.generate(params)
        >>> images[0].save("output.png")

    Direct API key initialization:
        >>> client = NovelAI(api_key="your_api_key_here")

    With context manager:
        >>> with NovelAI() as client:
        ...     images = client.image.generate(params)
        ...     images[0].save("output.png")
"""

from __future__ import annotations

from typing import AsyncIterator, Iterator, cast

from PIL import Image

from .._api.client import _APIClient, _AsyncAPIClient
from .._utils.converter import async_convert_user_params_to_api_request
from ..constants.tools import Emotion
from ..types.api.image import (
    ImageGenerationRequest,
    ImageStreamChunk,
    StreamImageGenerationRequest,
)
from ..types.api.tags import JpTagSuggestion, TagSuggestion
from ..types.user.image import (
    GenerateImageParams,
    GenerateImageStreamParams,
    ImageInput,
)
from ..types.user.tags import SuggestTagsParams
from ..types.user.tools import (
    BackgroundRemovalParams,
    ColorizeParams,
    DeclutterParams,
    DirectorToolParams,
    EmotionParams,
    LineArtParams,
    SketchParams,
    UpscaleParams,
)
from ..types.user.user import Subscription


class ImageGeneration:
    """High-level image generation interface

    This class provides convenient methods for generating images using NovelAI's API.
    All generation methods accept Pydantic-validated parameter objects and return
    PIL Image objects for easy manipulation.

    Note:
        This class is not meant to be instantiated directly. Access it through
        the NovelAI client's `image` attribute.

    Example:
        >>> from novelai import NovelAI
        >>> from novelai.types import GenerateImageParams
        >>>
        >>> client = NovelAI()
        >>> params = GenerateImageParams(
        ...     prompt="1girl, masterpiece",
        ...     model="nai-diffusion-4-5-full",
        ...     size="portrait",
        ... )
        >>> images = client.image.generate(params)
    """

    def __init__(self, client: NovelAI):
        self._client = client

    def generate(
        self,
        params: GenerateImageParams,
    ) -> list[Image.Image]:
        """Generate image(s) synchronously with user-friendly parameters

        This method provides a simple interface for image generation with automatic
        validation and PIL Image output. It accepts high-level parameters that are
        converted to the appropriate API request format internally.

        Args:
            params: High-level generation parameters with validation.
                See GenerateImageParams for all available options.

        Returns:
            List of PIL Image objects. Length matches params.n_samples.

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If API key is invalid or missing
            InvalidRequestError: If the request is malformed
            RateLimitError: If rate limit is exceeded
            ServerError: If server returns 5xx error
            NetworkError: If network connection fails

        Example:
            Basic generation:
                >>> params = GenerateImageParams(
                ...     prompt="1girl, cat ears, masterpiece",
                ...     model="nai-diffusion-4-5-full",
                ...     size=(832, 1216),
                ...     steps=28,
                ...     scale=5.0,
                ... )
                >>> images = client.image.generate(params)
                >>> images[0].save("output.png")

            Multiple images:
                >>> params = GenerateImageParams(
                ...     prompt="landscape, mountains",
                ...     n_samples=4,
                ... )
                >>> images = client.image.generate(params)
                >>> for i, img in enumerate(images):
                ...     img.save(f"output_{i}.png")

            With character reference:
                >>> from novelai.types import CharacterReference
                >>> params = GenerateImageParams(
                ...     prompt="1girl, standing",
                ...     character_references=[
                ...         CharacterReference(
                ...             image="reference.png",
                ...             fidelity=0.75,
                ...         )
                ...     ],
                ... )
                >>> images = client.image.generate(params)
        """

        request = cast(ImageGenerationRequest, params.to_api_request(self._client))

        return self._client.api_client.image.generate(request)

    def generate_stream(
        self,
        params: GenerateImageStreamParams,
    ) -> Iterator[ImageStreamChunk]:
        """Generate image(s) with Server-Sent Events (SSE) streaming

        This method streams generation progress in real-time, yielding chunks
        as they are received. Useful for monitoring long-running generations
        or displaying progressive output.

        Args:
            params: Streaming generation parameters. Inherits all options from
                GenerateImageParams with streaming enabled.

        Yields:
            ImageStreamChunk objects containing:
                - event: Event type ("newImage" for completion)
                - data: Base64-encoded image data when complete

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If API key is invalid or missing
            InvalidRequestError: If the request is malformed
            RateLimitError: If rate limit is exceeded
            ServerError: If server returns 5xx error
            NetworkError: If network connection fails or stream is interrupted

        Example:
            Stream generation and save final result:
                >>> from novelai.types import GenerateImageStreamParams
                >>> from base64 import b64decode
                >>> from PIL import Image
                >>> import io
                >>>
                >>> params = GenerateImageStreamParams(
                ...     prompt="1girl, masterpiece",
                ...     model="nai-diffusion-4-5-full",
                ... )
                >>>
                >>> for chunk in client.image.generate_stream(params):
                ...     if chunk.event == "newImage":
                ...         image_data = b64decode(chunk.data)
                ...         image = Image.open(io.BytesIO(image_data))
                ...         image.save("output.png")

            Monitor progress:
                >>> for i, chunk in enumerate(client.image.generate_stream(params)):
                ...     print(f"Chunk {i}: {chunk.event}")
                ...     if chunk.event == "newImage":
                ...         print("Generation complete!")
                ...         break
        """

        request = cast(
            StreamImageGenerationRequest, params.to_api_request(self._client)
        )
        yield from self._client.api_client.image.generate_stream(request)

    def suggest_tags(self, params: SuggestTagsParams) -> list[TagSuggestion]:
        """Get tag completion suggestions for an incomplete tag

        Tag suggestions are free — they consume no Anlas.

        Args:
            params: Tag suggestion parameters (query and model).

        Returns:
            List of TagSuggestion with tag, count, and confidence.

        Example:
            >>> from novelai.types import SuggestTagsParams
            >>> suggestions = client.image.suggest_tags(SuggestTagsParams(prompt="blue"))
            >>> suggestions[0].tag
            'blue archive'
        """
        return self._client.api_client.image.suggest_tags(
            params.model, params.prompt
        ).tags

    def suggest_tags_jp(self, params: SuggestTagsParams) -> list[JpTagSuggestion]:
        """Get Japanese tag suggestions with English tag mapping

        The API returns Japanese tags paired with the English tags to use
        in the actual prompt.

        Args:
            params: Tag suggestion parameters (Japanese query and model).

        Returns:
            List of JpTagSuggestion with jp_tag, en_tag, and power.

        Example:
            >>> from novelai.types import SuggestTagsParams
            >>> suggestions = client.image.suggest_tags_jp(SuggestTagsParams(prompt="青"))
            >>> suggestions[0].en_tag
            'blue theme'
        """
        return self._client.api_client.image.suggest_tags_jp(
            params.model, params.prompt
        )


class DirectorTools:
    """High-level Director Tools interface

    Director Tools transform an existing image via the /ai/augment-image
    endpoint: line art extraction, sketch conversion, colorization, emotion
    change, decluttering, and background removal. The 2x upscale
    (/ai/upscale) is also exposed here, matching the web UI grouping.

    All methods return a list of PIL Images. Most tools return a single image,
    but background removal returns three (masked, generated, blend).

    Note:
        This class is not meant to be instantiated directly. Access it through
        the NovelAI client's `tools` attribute.

    Example:
        >>> client = NovelAI()
        >>> images = client.tools.line_art("illustration.png")
        >>> images[0].save("lineart.png")
    """

    def __init__(self, client: NovelAI):
        self._client = client

    def augment(self, params: DirectorToolParams) -> list[Image.Image]:
        """Transform an image with per-tool validated parameters

        This is the generic entry point taking any per-tool parameter model
        (LineArtParams, EmotionParams, ...). The per-tool methods below are
        thin shortcuts that build the same parameters for you.

        Args:
            params: One of the per-tool parameter models. Each model exposes
                exactly the options its tool accepts.

        Returns:
            List of PIL Image objects.

        Raises:
            ValidationError: If parameters are invalid
            AuthenticationError: If API key is invalid or missing
            InvalidRequestError: If the request is malformed
            RateLimitError: If rate limit is exceeded
            ServerError: If server returns 5xx error
            NetworkError: If network connection fails

        Example:
            >>> from novelai.types import EmotionParams
            >>> params = EmotionParams(image="character.png", emotion="happy")
            >>> images = client.tools.augment(params)
        """
        return self._client.api_client.image.augment(params.to_api_request())

    def line_art(self, image: ImageInput) -> list[Image.Image]:
        """Extract black-and-white line art from the image"""
        return self.augment(LineArtParams(image=image))

    def sketch(self, image: ImageInput) -> list[Image.Image]:
        """Convert the image into a pencil-sketch style drawing"""
        return self.augment(SketchParams(image=image))

    def remove_background(self, image: ImageInput) -> list[Image.Image]:
        """Remove the background, keeping the subject

        The API returns three images in order: masked, generated, and blend.
        """
        return self.augment(BackgroundRemovalParams(image=image))

    def declutter(
        self, image: ImageInput, *, keep_bubbles: bool = False
    ) -> list[Image.Image]:
        """Remove text and sound effects from the image

        Args:
            image: Source image to declutter.
            keep_bubbles: Keep speech bubbles instead of removing them.
        """
        return self.augment(DeclutterParams(image=image, keep_bubbles=keep_bubbles))

    def colorize(
        self, image: ImageInput, *, prompt: str = "", defry: int = 0
    ) -> list[Image.Image]:
        """Colorize a line art or grayscale image

        Args:
            image: Source image to colorize.
            prompt: Additional tags to guide the colorization.
            defry: Weakens the effect (0 = full effect, up to 5).
        """
        return self.augment(ColorizeParams(image=image, prompt=prompt, defry=defry))

    def emotion(
        self,
        image: ImageInput,
        emotion: Emotion,
        *,
        prompt: str = "",
        defry: int = 0,
    ) -> list[Image.Image]:
        """Change the expression of the character in the image

        Args:
            image: Source image containing the character.
            emotion: Target mood, e.g. "happy", "sad", "angry".
            prompt: Additional tags to guide the change.
            defry: Weakens the effect (0 = full effect, up to 5).

        Example:
            >>> images = client.tools.emotion("character.png", "laughing")
            >>> images[0].save("laughing.png")
        """
        return self.augment(
            EmotionParams(image=image, emotion=emotion, prompt=prompt, defry=defry)
        )

    def upscale(self, params: UpscaleParams) -> list[Image.Image]:
        """Upscale the image to twice its size

        Unlike the other tools this uses /ai/upscale, and the upscale
        factor is fixed at 2x by the API.

        Args:
            params: Upscale parameters (source image and model).

        Example:
            >>> from novelai.types import UpscaleParams
            >>> images = client.tools.upscale(UpscaleParams(image="illustration.png"))
            >>> images[0].save("upscaled.png")
        """
        return self._client.api_client.image.upscale(params.to_api_request())


class UserAccount:
    """High-level user account interface

    This class exposes account information such as the subscription tier and
    the remaining Anlas balance. Unlike ``GenerateImageParams.calculate_anlas()``,
    which *estimates* the cost of a generation, these methods report the actual
    state of the account from NovelAI's API.

    Note:
        This class is not meant to be instantiated directly. Access it through
        the NovelAI client's `user` attribute.

    Example:
        >>> client = NovelAI()
        >>> client.user.get_anlas()
        4250
        >>> client.user.get_subscription().is_opus
        True
    """

    def __init__(self, client: NovelAI):
        self._client = client

    def get_subscription(self) -> Subscription:
        """Get the current subscription, including Anlas balance and perks

        Returns:
            Subscription object with tier, active status, expiry, perks, and
            the remaining Anlas balance (``subscription.anlas``).

        Raises:
            AuthenticationError: If the API key is invalid
            RateLimitError: If rate limit is exceeded
            ServerError: If server returns 5xx error
            NetworkError: If network connection fails

        Example:
            >>> sub = client.user.get_subscription()
            >>> sub.tier, sub.active, sub.anlas
            (3, True, 4250)
        """
        return self._client.api_client.user.get_subscription()

    def get_anlas(self) -> int:
        """Get the current total Anlas balance (subscription + purchased)

        This is the actual balance reported by NovelAI, not an estimate.

        Returns:
            Total Anlas available on the account.

        Example:
            >>> client.user.get_anlas()
            4250
        """
        return self.get_subscription().anlas


class NovelAI:
    """High-level client for NovelAI API

    This is the main entry point for interacting with NovelAI's services.
    The client handles authentication, request management, and provides
    access to image generation features through a clean, type-safe interface.

    The client automatically loads the API key from the NOVELAI_API_KEY
    environment variable if not provided directly. It supports context
    manager protocol for automatic resource cleanup.

    Attributes:
        image: ImageGeneration instance for image generation operations
        tools: DirectorTools instance for image augmentation (line art, emotion, etc.)
        user: UserAccount instance for subscription and Anlas balance
        api_client: Internal low-level API client (not recommended for direct use)

    Example:
        Using environment variable:
            >>> import os
            >>> os.environ["NOVELAI_API_KEY"] = "your_api_key"
            >>> client = NovelAI()

        Direct initialization:
            >>> client = NovelAI(api_key="your_api_key")

        With context manager:
            >>> with NovelAI() as client:
            ...     params = GenerateImageParams(prompt="1girl")
            ...     images = client.image.generate(params)

        Custom timeout:
            >>> client = NovelAI(timeout=180.0)  # 3 minutes
    """

    def __init__(
        self,
        api_key: str | None = None,
        image_base: str | None = None,
        text_base: str | None = None,
        api_base: str | None = None,
        timeout: float = 120.0,
    ):
        """Initialize NovelAI client with optional configuration

        Args:
            api_key: NovelAI API key (Bearer token). If None, attempts to load
                from NOVELAI_API_KEY environment variable. Must be provided
                via one of these methods before making API requests.
            image_base: Image API base URL. Also serves user account
                endpoints such as /user/subscription.
                Default behavior uses NovelAI's official endpoint.
            text_base: Text API base URL.
                Default behavior uses NovelAI's official endpoint.
            api_base: Deprecated. No SDK endpoint uses api.novelai.net
                anymore; use image_base instead. Passing this (or setting
                NOVELAI_API_BASE) emits a DeprecationWarning.
            timeout: Request timeout in seconds. Applies to all HTTP requests.
                Default is 120.0 seconds (2 minutes). Increase for slow
                connections or complex generations.

        Raises:
            ValueError: If API key is not provided and NOVELAI_API_KEY
                environment variable is not set (raised when attempting
                to make API requests, not during initialization)

        Example:
            Load from environment:
                >>> from dotenv import load_dotenv
                >>> load_dotenv()  # Loads .env file
                >>> client = NovelAI()

            Direct API key:
                >>> client = NovelAI(api_key="your_key_here")

            Custom timeout:
                >>> client = NovelAI(timeout=300.0)  # 5 minutes for slow connections
        """
        self.api_client = _APIClient(
            api_key=api_key,
            image_base=image_base,
            text_base=text_base,
            api_base=api_base,
            timeout=timeout,
        )
        self.image = ImageGeneration(self)
        self.tools = DirectorTools(self)
        self.user = UserAccount(self)

    @property
    def api_key(self) -> str:
        """Get the currently configured API key

        Returns:
            The API key string used for authentication

        Raises:
            ValueError: If API key is not set (neither provided during
                initialization nor found in NOVELAI_API_KEY environment variable)

        Example:
            >>> client = NovelAI(api_key="your_key")
            >>> print(client.api_key)
            your_key
        """
        api_key = self.api_client.api_key
        if api_key is None:
            raise ValueError("API key is not set")
        return api_key

    @property
    def timeout(self) -> float:
        """Get the request timeout in seconds

        Returns:
            Timeout value in seconds

        Example:
            >>> client = NovelAI(timeout=180.0)
            >>> print(client.timeout)
            180.0
        """
        return self.api_client.timeout

    def __enter__(self):
        """Enter context manager

        Returns:
            Self for use in with statement

        Example:
            >>> with NovelAI() as client:
            ...     # client is automatically closed on exit
            ...     images = client.image.generate(params)
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit context manager and cleanup resources

        Automatically closes the HTTP client connection pool when
        exiting the context manager.

        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        """
        self.close()

    def close(self):
        """Close the HTTP client and release resources

        This method closes the underlying HTTP client connection pool.
        Should be called when done using the client, or use context
        manager for automatic cleanup.

        Example:
            Manual cleanup:
                >>> client = NovelAI()
                >>> try:
                ...     images = client.image.generate(params)
                ... finally:
                ...     client.close()

            Automatic cleanup (preferred):
                >>> with NovelAI() as client:
                ...     images = client.image.generate(params)
        """
        self.api_client.close()


class AsyncImageGeneration:
    """High-level async image generation interface"""

    def __init__(self, client: AsyncNovelAI):
        self._client = client

    async def generate(
        self,
        params: GenerateImageParams,
    ) -> list[Image.Image]:
        """Generate image(s) asynchronously with user-friendly parameters"""
        request = cast(
            ImageGenerationRequest,
            await async_convert_user_params_to_api_request(params, self._client),
        )
        return await self._client.api_client.image.generate(request)

    async def generate_stream(
        self,
        params: GenerateImageStreamParams,
    ) -> AsyncIterator[ImageStreamChunk]:
        """Generate image(s) with Server-Sent Events (SSE) streaming asynchronously"""
        request = cast(
            StreamImageGenerationRequest,
            await async_convert_user_params_to_api_request(params, self._client),
        )
        async for chunk in self._client.api_client.image.generate_stream(request):
            yield chunk

    async def suggest_tags(self, params: SuggestTagsParams) -> list[TagSuggestion]:
        """Get tag completion suggestions for an incomplete tag asynchronously"""
        return (
            await self._client.api_client.image.suggest_tags(
                params.model, params.prompt
            )
        ).tags

    async def suggest_tags_jp(self, params: SuggestTagsParams) -> list[JpTagSuggestion]:
        """Get Japanese tag suggestions with English tag mapping asynchronously"""
        return await self._client.api_client.image.suggest_tags_jp(
            params.model, params.prompt
        )


class AsyncDirectorTools:
    """High-level async Director Tools interface"""

    def __init__(self, client: AsyncNovelAI):
        self._client = client

    async def augment(self, params: DirectorToolParams) -> list[Image.Image]:
        """Transform an image with per-tool validated parameters asynchronously"""
        return await self._client.api_client.image.augment(params.to_api_request())

    async def line_art(self, image: ImageInput) -> list[Image.Image]:
        """Extract black-and-white line art from the image"""
        return await self.augment(LineArtParams(image=image))

    async def sketch(self, image: ImageInput) -> list[Image.Image]:
        """Convert the image into a pencil-sketch style drawing"""
        return await self.augment(SketchParams(image=image))

    async def remove_background(self, image: ImageInput) -> list[Image.Image]:
        """Remove the background; returns masked, generated, and blend images"""
        return await self.augment(BackgroundRemovalParams(image=image))

    async def declutter(
        self, image: ImageInput, *, keep_bubbles: bool = False
    ) -> list[Image.Image]:
        """Remove text and sound effects from the image"""
        return await self.augment(
            DeclutterParams(image=image, keep_bubbles=keep_bubbles)
        )

    async def colorize(
        self, image: ImageInput, *, prompt: str = "", defry: int = 0
    ) -> list[Image.Image]:
        """Colorize a line art or grayscale image"""
        return await self.augment(
            ColorizeParams(image=image, prompt=prompt, defry=defry)
        )

    async def emotion(
        self,
        image: ImageInput,
        emotion: Emotion,
        *,
        prompt: str = "",
        defry: int = 0,
    ) -> list[Image.Image]:
        """Change the expression of the character in the image"""
        return await self.augment(
            EmotionParams(image=image, emotion=emotion, prompt=prompt, defry=defry)
        )

    async def upscale(self, params: UpscaleParams) -> list[Image.Image]:
        """Upscale the image to twice its size"""
        return await self._client.api_client.image.upscale(params.to_api_request())


class AsyncUserAccount:
    """High-level async user account interface"""

    def __init__(self, client: AsyncNovelAI):
        self._client = client

    async def get_subscription(self) -> Subscription:
        """Get the current subscription, including Anlas balance and perks"""
        return await self._client.api_client.user.get_subscription()

    async def get_anlas(self) -> int:
        """Get the current total Anlas balance (subscription + purchased)"""
        return (await self.get_subscription()).anlas


class AsyncNovelAI:
    """High-level async client for NovelAI API"""

    def __init__(
        self,
        api_key: str | None = None,
        image_base: str | None = None,
        text_base: str | None = None,
        api_base: str | None = None,
        timeout: float = 120.0,
    ):
        self.api_client = _AsyncAPIClient(
            api_key=api_key,
            image_base=image_base,
            text_base=text_base,
            api_base=api_base,
            timeout=timeout,
        )
        self.image = AsyncImageGeneration(self)
        self.tools = AsyncDirectorTools(self)
        self.user = AsyncUserAccount(self)

    @property
    def api_key(self) -> str:
        api_key = self.api_client.api_key
        if api_key is None:
            raise ValueError("API key is not set")
        return api_key

    @property
    def timeout(self) -> float:
        return self.api_client.timeout

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
        """Close the Async HTTP client and release resources"""
        await self.api_client.close()
