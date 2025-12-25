"""High-level Client type definitions"""

from __future__ import annotations

from pathlib import Path
from random import randint
from typing import TYPE_CHECKING, Any, Literal, Self

from PIL import Image as PILImage
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from ..._utils.converter import convert_user_params_to_api_request
from ..._utils.image import image_to_base64
from ...constants import (
    K_EULER_ANCESTRAL,
    NOISE_KARRAS,
    QUALITY_TAGS,
    UC_LIGHT,
    UNDESIRED_CONTENT_PRESETS,
    V4_5_FULL,
    ImageModel,
    ImageSize,
    NoiseSchedule,
    Sampler,
    UCPreset,
)
from ...constants.position import Position, PositionPreset
from ...constants.sizes import PRESET_MAP
from ...types.api.image import EncodeVibeRequest

if TYPE_CHECKING:
    from ..._client.client import NovelAI
    from ...types.api.image import ImageGenerationRequest, StreamImageGenerationRequest


# Type alias for image inputs
# Any for numpy.ndarray (cv2 images)
ImageInput = str | bytes | Path | PILImage.Image | Any


class Character(BaseModel):
    """Character definition with prompt and positioning

    This is a high-level model that combines characterPrompts and char_captions data.
    """

    prompt: str = Field(..., description="Character-specific prompt")
    negative_prompt: str = Field(
        default="", description="Character-specific negative prompt"
    )
    position: tuple[float, float] | PositionPreset = Field(
        default=(0.5, 0.5),
        description="Character center position as (x, y) coordinates",
    )
    enabled: bool = Field(default=True, description="Enable this character")

    @field_validator("position", mode="after")
    @classmethod
    def _parse_position(cls, v: Position) -> tuple[float, float]:
        """Parse position and cache for internal use"""
        # Get size preset
        if isinstance(v, str):
            if len(v) != 2:
                raise ValueError("Invalid position preset")
            # position is 5x5 grid, convert to 0.0-1.0 range
            x_str, y_str = "ABCDE".index(v[0]) + 1, "12345".index(v[1]) + 1
            return (x_str / 5, y_str / 5)

        x, y = v
        if not (0.0 <= x <= 1.0) or not (0.0 <= y <= 1.0):
            raise ValueError("Position coordinates must be between 0.0 and 1.0")
        return v


class ControlNet(BaseModel):
    """ControlNet configuration"""

    images: list[ControlNetImage] = Field(..., description="ControlNet images")
    strength: float = Field(
        default=1.0, ge=0.0, le=1.0, description="ControlNet overall strength"
    )

    @classmethod
    def from_file(cls) -> ControlNet:
        "load controlnet image from .naiv4vibebundle file"
        raise NotImplementedError("Not implemented yet")

    @classmethod
    def export_file(cls) -> None:
        "export controlnet images to .naiv4vibebundle file"
        raise NotImplementedError("Not implemented yet")


class ControlNetImage(BaseModel):
    """ControlNet image configuration"""

    image: ImageInput = Field(..., description="ControlNet image")
    info_extracted: float = Field(
        default=0.7,
        ge=0.01,
        le=1.0,
        description="ControlNet information extracted value",
    )
    strength: float = Field(
        default=0.6, ge=0.01, le=1.0, description="ControlNet reference strength"
    )

    controlnet_model: ImageModel = Field(
        default=V4_5_FULL, description="ControlNet model"
    )

    _vibe_data: str | None = None

    def encode_vibe(self, client: NovelAI, disable_cache: bool = False) -> str:
        """Encode vibe-transfer data"""
        if disable_cache or self._vibe_data is None:
            self._vibe_data = client.api_client.image.encode_vibe(
                EncodeVibeRequest(
                    image=image_to_base64(self.image),
                    information_extracted=self.info_extracted,
                    model=self.controlnet_model,
                )
            )
        return self._vibe_data

    @classmethod
    def from_file(cls) -> ControlNetImage:
        "load controlnet image from .naiv4vibe file"
        raise NotImplementedError("Not implemented yet")

    @classmethod
    def export_file(cls) -> None:
        """Export to .naiv4vibe file"""
        raise NotImplementedError("Not implemented yet")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class I2iParams(BaseModel):
    """Parameters for img2img generation"""

    image: ImageInput = Field(..., description="Source image for img2img")
    strength: float = Field(
        default=0.7, ge=0.01, le=0.99, description="Strength for img2img"
    )
    noise: float = Field(
        default=0.0, ge=0.0, le=0.99, description="Noise amount for img2img"
    )
    mask: ImageInput | None = Field(
        default=None,
        description="Mask image for inpainting",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CharacterReference(BaseModel):
    """Character reference image configuration

    This is a high-level model that combines all character reference parameters for a single image.
    """

    image: ImageInput = Field(..., description="Character reference image")
    type: Literal["character", "character&style"] = Field(
        default="character&style", description="Character reference type"
    )
    fidelity: float = Field(
        default=0.75, ge=0.0, le=1.0, description="Reference fidelity"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)


# validators
def validate_size(size: tuple[int, int]) -> bool:
    """Validate image size"""
    width, height = size
    if width < 64 or width > 1600:
        raise ValueError(f"Width must be between 64 and 1600, got {width}")
    if height < 64 or height > 1600:
        raise ValueError(f"Height must be between 64 and 1600, got {height}")
    if width % 64 != 0:
        raise ValueError(f"Width must be multiple of 64, got {width}")
    if height % 64 != 0:
        raise ValueError(f"Height must be multiple of 64, got {height}")
    return True


class GenerateImageParams(BaseModel):
    """High-level parameters for image generation

    This is a user-friendly interface that accepts PIL Images, Pathlib paths,
    and provides sensible defaults.
    """

    # Basic parameters
    prompt: str = Field(..., description="Text prompt for image generation")
    model: ImageModel = Field(
        default=V4_5_FULL, description="Model to use for generation"
    )
    size: ImageSize = Field(
        default="portrait",
        description="Image size as (width, height) tuple or preset name like 'portrait'",
    )

    @field_validator("size", mode="after")
    @classmethod
    def _parse_size(cls, v: ImageSize) -> ImageSize:
        """Parse size and cache width/height for internal use"""

        # Get size preset
        if isinstance(v, str):
            return PRESET_MAP[v]

        # Validate size
        validate_size(v)

        return v

    # Quality and style
    negative_prompt: str | None = Field(default=None, description="Negative prompt")
    quality: bool = Field(default=True, description="Adds quality tags")
    uc_preset: UCPreset = Field(
        default=UC_LIGHT, description="Undesired content preset"
    )

    # Sampling parameters
    steps: int = Field(default=23, ge=1, le=50, description="Number of sampling steps")
    scale: float = Field(
        default=5.0, ge=0.0, le=10.0, description="Prompt guidance scale"
    )
    sampler: Sampler = Field(default=K_EULER_ANCESTRAL, description="Sampling method")
    noise_schedule: NoiseSchedule = Field(
        default=NOISE_KARRAS, description="Noise schedule"
    )
    seed: int = Field(
        default_factory=lambda: randint(0, 999999999),
        description="Random seed for reproducibility",
    )
    n_samples: int = Field(
        default=1, ge=1, le=8, description="Number of images to generate"
    )

    # Advanced sampling
    cfg_rescale: float = Field(default=0.0, ge=0.0, le=1.0, description="CFG rescale")
    variety_boost: bool = Field(
        default=False, description="Variety boost (skip_cfg_above_sigma)"
    )

    # i2i
    i2i: I2iParams | None = Field(
        default=None,
        description="Img2img parameters",
    )
    controlnet: ControlNet | None = Field(
        default=None,
        description="ControlNet(Vibe Transfer) configuration",
    )

    # Director Tools (Character Reference) (v4.5 only)
    character_references: list[CharacterReference] | None = Field(
        default=None,
        description="Character reference images with settings (high-level API)",
    )

    # misc
    image_format: Literal["webp", "png"] | None = Field(
        default=None, description="Image format (webp is lossless, None to use png)"
    )

    @model_validator(mode="after")
    def _check_character_references(self) -> Self:
        """Check if character references are compatible with the model"""
        character_references = getattr(self, "character_references", []) or []
        if not self.is_v4_5(self.model) and len(character_references) > 0:
            raise ValueError("Character references are only supported for V4.5 models")

        # currently, multiple character references are not supported for V4 models
        # block multiple references until NovelAI supports it
        if len(character_references) > 1:
            raise ValueError(
                "Multiple character references are not supported for V4 models"
            )
        return self

    # Character prompts (V4, V4.5 only)
    characters: list[Character] | None = Field(
        default=None,
        description="Character-specific prompts with positioning (V4 models only)",
    )

    @model_validator(mode="after")
    def _check_characters(self) -> Self:
        """Check if characters are compatible with the model"""
        characters = getattr(self, "characters", []) or []
        if not self.is_v4(self.model) and len(characters) > 0:
            raise ValueError("Characters are only supported for V4 models")
        return self

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field
    @property
    def processed_prompt(self) -> str:
        """Prompt with quality tags applied"""
        if self.quality:
            return self.prompt + QUALITY_TAGS
        return self.prompt

    @computed_field
    @property
    def processed_negative_prompt(self) -> str:
        """Negative prompt with UC preset applied"""
        base_negative = self.negative_prompt or ""
        uc_text = UNDESIRED_CONTENT_PRESETS.get(self.uc_preset, "")
        return base_negative + uc_text

    @staticmethod
    def is_v4(model: ImageModel) -> bool:
        return model in [
            "nai-diffusion-4-5-full",
            "nai-diffusion-4-5-curated",
            "nai-diffusion-4-full",
            "nai-diffusion-4-curated",
        ]

    @staticmethod
    def is_v4_5(model: ImageModel) -> bool:
        return model in [
            "nai-diffusion-4-5-full",
            "nai-diffusion-4-5-curated",
        ]

    def to_api_request(
        self,
        client: NovelAI,
    ) -> ImageGenerationRequest | StreamImageGenerationRequest:
        """Convert to core API request

        Args:
            client: NovelAI client

        Returns:
            ImageGenerationRequest or StreamImageGenerationRequest for the low-level API
        """

        return convert_user_params_to_api_request(self, client)


class GenerateImageStreamParams(GenerateImageParams):
    """Parameters for image generation stream"""

    # currently we only support sse streaming
    stream: Literal["sse"] = Field(default="sse", description="Streaming type")

    model_config = ConfigDict(arbitrary_types_allowed=True)
