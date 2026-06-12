"""High-level Director Tools type definitions

Each Director Tool gets its own parameter model, exposing exactly the options
that tool accepts — like the per-tool panels in the NovelAI web UI. Invalid
combinations (e.g. a prompt for line art) are unrepresentable by type.
"""

from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field

from novelai._utils.image import ImageInput, image_to_base64, to_pil_image
from novelai.constants.tools import DirectorTool, Emotion
from novelai.types.api.tools import AugmentImageRequest
from novelai.utils.anlas import calculate_augment_anlas

if TYPE_CHECKING:
    from novelai.utils.anlas import AugmentAnlasEstimate


class _BaseAugmentParams(BaseModel):
    """Shared fields and request conversion for all Director Tools

    Concrete models declare a `tool` Literal field as the union discriminator.
    """

    image: ImageInput = Field(..., description="Source image to transform")
    size: tuple[int, int] | None = Field(
        default=None,
        description=(
            "Source image size as (width, height). "
            "If omitted, it is auto-inferred from the image."
        ),
    )

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    def _req_type(self) -> DirectorTool:
        """API req_type for this tool. Defaults to the `tool` discriminator.

        `tool` lives on the concrete models (with narrowed Literal types that
        pyright would reject as a field override), hence the getattr.
        """
        req_type: DirectorTool = getattr(self, "tool")
        return req_type

    def _api_prompt(self) -> str | None:
        """API prompt for this tool. Only colorize/emotion send one."""
        return None

    def _api_defry(self) -> int | None:
        """API defry for this tool. Only colorize/emotion send one."""
        return None

    def _resolve_size(self, encoded: str | None = None) -> tuple[int, int]:
        """Explicit `size` if set, otherwise inferred from the image"""
        if self.size is not None:
            return self.size
        if encoded is None:
            encoded = image_to_base64(self.image)
        # Decoding our own base64 handles every ImageInput variant uniformly,
        # including raw base64 strings that `to_pil_image` cannot take directly.
        return to_pil_image(base64.b64decode(encoded)).size

    def calculate_anlas(self, *, is_opus: bool = False) -> AugmentAnlasEstimate:
        """Estimate the Anlas cost for this Director Tools request.

        This follows the SDK's reverse-engineered pricing logic and should be
        treated as an estimate rather than a 100% guaranteed billing value.
        """
        width, height = self._resolve_size()
        return calculate_augment_anlas(self._req_type(), width, height, is_opus=is_opus)

    def to_api_request(self) -> AugmentImageRequest:
        """Convert to the low-level /ai/augment-image request

        Unlike image generation, the conversion needs no API access,
        so no client is required.

        Returns:
            AugmentImageRequest for the low-level API
        """
        encoded = image_to_base64(self.image)
        width, height = self._resolve_size(encoded)

        return AugmentImageRequest(
            req_type=self._req_type(),
            width=width,
            height=height,
            image=encoded,
            prompt=self._api_prompt(),
            defry=self._api_defry(),
        )


class LineArtParams(_BaseAugmentParams):
    """Extract black-and-white line art from the image"""

    tool: Literal["lineart"] = "lineart"


class SketchParams(_BaseAugmentParams):
    """Convert the image into a pencil-sketch style drawing"""

    tool: Literal["sketch"] = "sketch"


class BackgroundRemovalParams(_BaseAugmentParams):
    """Remove the background, keeping the subject

    The API may return multiple images (e.g. separated layers).
    """

    tool: Literal["bg-removal"] = "bg-removal"


class DeclutterParams(_BaseAugmentParams):
    """Remove text and sound effects from the image"""

    tool: Literal["declutter"] = "declutter"
    keep_bubbles: bool = Field(
        default=False, description="Keep speech bubbles instead of removing them"
    )

    def _req_type(self) -> DirectorTool:
        return "declutter-keep-bubbles" if self.keep_bubbles else "declutter"


class ColorizeParams(_BaseAugmentParams):
    """Colorize a line art or grayscale image"""

    tool: Literal["colorize"] = "colorize"
    prompt: str = Field(
        default="", description="Additional tags to guide the colorization"
    )
    defry: int = Field(
        default=0, ge=0, le=5, description="Weakens the effect (0 = full effect)"
    )

    def _api_prompt(self) -> str:
        return self.prompt

    def _api_defry(self) -> int:
        return self.defry


class EmotionParams(_BaseAugmentParams):
    """Change the expression of the character in the image"""

    tool: Literal["emotion"] = "emotion"
    emotion: Emotion = Field(..., description="Target mood of the character")
    prompt: str = Field(default="", description="Additional tags to guide the change")
    defry: int = Field(
        default=0, ge=0, le=5, description="Weakens the effect (0 = full effect)"
    )

    def _api_prompt(self) -> str:
        return f"{self.emotion};;{self.prompt}"

    def _api_defry(self) -> int:
        return self.defry


DirectorToolParams = (
    LineArtParams
    | SketchParams
    | BackgroundRemovalParams
    | DeclutterParams
    | ColorizeParams
    | EmotionParams
)
"""Union of all per-tool parameter models, discriminated by the `tool` field."""
