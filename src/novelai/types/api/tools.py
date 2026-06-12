"""API type definitions for Director Tools"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AugmentImageRequest(BaseModel):
    """Request for image augmentation - low-level API model

    This mirrors the NovelAI /ai/augment-image REST API exactly.
    No automatic processing (size inference, emotion prompt assembly) is performed.
    """

    model_config = ConfigDict(extra="forbid")

    req_type: str = Field(..., description="Director tool to apply")
    width: int = Field(..., gt=0, description="Width of the source image in pixels")
    height: int = Field(..., gt=0, description="Height of the source image in pixels")
    image: str = Field(..., description="Base64 encoded source image")
    prompt: str | None = Field(
        default=None,
        description=(
            "Tool prompt (colorize/emotion only). "
            "The emotion tool expects the 'mood;;prompt' format."
        ),
    )
    defry: int | None = Field(
        default=None,
        ge=0,
        le=5,
        description="Weakens the tool effect (colorize/emotion only, 0 = full effect)",
    )
