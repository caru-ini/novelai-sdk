"""API type definitions for tag suggestions"""

from __future__ import annotations

from pydantic import BaseModel, Field


class TagSuggestion(BaseModel):
    """Single tag suggestion from /ai/generate-image/suggest-tags"""

    tag: str = Field(..., description="Suggested tag")
    count: int = Field(..., description="Occurrence count (capped at 10000)")
    confidence: float = Field(..., description="Suggestion confidence")


class TagSuggestionResponse(BaseModel):
    """Response from /ai/generate-image/suggest-tags"""

    tags: list[TagSuggestion] = Field(..., description="Suggested tags")


class JpTagSuggestion(BaseModel):
    """Single tag suggestion from /ai/generate-image/suggest-tags with lang=jp

    Unlike the English response, the jp variant returns a bare JSON array
    of these objects.
    """

    jp_tag: str = Field(..., description="Japanese tag")
    en_tag: str = Field(..., description="Corresponding English tag")
    power: int = Field(..., description="Relevance score (capped at 10000)")
