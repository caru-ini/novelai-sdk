"""NovelAI API Client for Python

Usage:
    from novelai import NovelAI
    from novelai.types import GenerateImageParams

    client = NovelAI(api_key="your_key")
    params = GenerateImageParams(prompt="1girl")
    images = client.image.generate(params)

For type definitions, import from .types:
    from novelai.types import GenerateImageParams, Character, etc.

"""

from ._client.client import AsyncNovelAI, NovelAI
from .exceptions import (
    AuthenticationError,
    InvalidRequestError,
    MissingAPIKeyError,
    NetworkError,
    NovelAIError,
    RateLimitError,
    ServerError,
)

# DO NOT EDIT!!
# This value is automatically updated during the release process.
__version__ = "0.4.2"

__all__ = [
    "NovelAI",
    "AsyncNovelAI",
    # Exceptions
    "NovelAIError",
    "AuthenticationError",
    "InvalidRequestError",
    "MissingAPIKeyError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
]
