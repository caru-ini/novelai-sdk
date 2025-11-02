from __future__ import annotations


class NovelAIError(Exception):
    """Base exception for NovelAI API errors"""

    pass


class MissingAPIKeyError(NovelAIError):
    """Raised when API key is missing"""

    pass


class AuthenticationError(NovelAIError):
    """Raised when authentication fails"""

    pass


class InvalidRequestError(NovelAIError):
    """Raised when request parameters are invalid"""

    pass


class RateLimitError(NovelAIError):
    """Raised when rate limit is exceeded"""

    pass


class ServerError(NovelAIError):
    """Raised when server returns 5xx error"""

    pass


class NetworkError(NovelAIError):
    """Raised when network request fails"""

    pass
