"""High-level tag suggestion type definitions"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from novelai.constants.models import V4_5_FULL, ImageModel


class SuggestTagsParams(BaseModel):
    """Parameters for tag suggestions

    Shared by the English (`suggest_tags`) and Japanese (`suggest_tags_jp`)
    variants — the two differ only in response shape.
    """

    prompt: str = Field(..., min_length=1, description="Incomplete tag query")
    model: ImageModel = Field(
        default=V4_5_FULL, description="Image model to get suggestions for"
    )

    model_config = ConfigDict(extra="forbid")
