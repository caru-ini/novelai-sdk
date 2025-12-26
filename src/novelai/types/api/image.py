"""API type definitions"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ...constants import StreamingType


class CenterPoint(BaseModel):
    """Center point coordinates in object format for API"""

    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")


class CharacterPrompt(BaseModel):
    """Character-specific prompt with positioning"""

    prompt: str = Field(..., description="Character prompt")
    uc: str = Field(..., description="Undesired content for character")
    center: CenterPoint = Field(..., description="Character center position")
    enabled: bool = Field(default=True, description="Enable this character prompt")


class EncodeVibeRequest(BaseModel):
    """Parameters for encode vibe-transfer"""

    image: str = Field(..., description="Base64 image data")
    information_extracted: float = Field(
        ..., gt=0, le=1, description="Strength of extract"
    )
    model: str = Field(..., description="Model name")


class V4CharacterCaption(BaseModel):
    """Character caption with positioning for V4"""

    centers: list[CenterPoint] | None = Field(
        None, description="Character center coordinates"
    )
    char_caption: str | None = Field(
        default=None, description="Character-specific caption (normally input)"
    )


class V4Caption(BaseModel):
    """Caption structure for V4"""

    base_caption: str | None = Field(default=None, description="Base caption text")
    char_captions: list[V4CharacterCaption] | None = Field(
        default=None, description="Character captions"
    )


class ReferenceCaption(BaseModel):
    """Caption structure for image reference"""

    base_caption: Literal["character&style", "character"] = Field(
        ..., description="Base caption text"
    )
    char_captions: list[V4CharacterCaption] = Field(default=[], description="Noop.")


class V4ConditionInput(BaseModel):
    """V4 condition input for prompts"""

    caption: V4Caption | None = Field(default=None, description="Caption structure")
    legacy_uc: bool | None = Field(
        default=None, description="Use legacy undesired content"
    )
    use_coords: bool | None = Field(default=None, description="Use coordinates")
    use_order: bool | None = Field(default=None, description="Use order")


class Img2ImgParams(BaseModel):
    """Parameters for i2i generation"""

    color_correct: bool | None = Field(None, description="Apply color correction")
    extra_noise_seed: int | None = Field(None, description="Extra noise seed")
    noise: float | None = Field(None, description="Noise amount")
    strength: float | None = Field(
        None, ge=0.0, le=1.0, description="Strength of transformation. 1 - fidelity"
    )


class ReferenceConditionInput(BaseModel):
    """Character reference condition input"""

    caption: ReferenceCaption | None = Field(None, description="Caption of reference")
    legacy_uc: bool | None = Field(None, description="Use legacy undesired content")


class ImageParameters(BaseModel):
    """Parameters for image generation - complete API specification

    This is a low-level model that mirrors the NovelAI REST API exactly.
    No automatic processing (quality tags, UC presets, v4 prompt conversion) is performed.
    """

    model_config = ConfigDict(extra="forbid")

    # Basic parameters
    width: int | None = Field(
        default=None, ge=64, le=1600, description="Image width (must be multiple of 64)"
    )
    height: int | None = Field(
        default=None,
        ge=64,
        le=1600,
        description="Image height (must be multiple of 64)",
    )
    steps: int | None = Field(
        default=None, ge=1, le=50, description="Number of sampling steps"
    )
    scale: float | None = Field(
        default=None, ge=0.0, le=10.0, description="Prompt guidance scale"
    )
    sampler: str | None = Field(default=None, description="Sampling method")
    seed: int | None = Field(
        default=None, description="Random seed for reproducibility"
    )
    n_samples: int | None = Field(
        default=None, ge=1, le=8, description="Number of images to generate"
    )

    # Prompt parameters
    prompt: str | None = Field(default=None, description="Positive prompt")
    negative_prompt: str | None = Field(default=None, description="Negative prompt")
    ucPreset: int | None = Field(
        default=None, ge=0, le=3, description="Undesired content preset"
    )
    qualityToggle: bool | None = Field(default=None, description="Enable quality tags")

    # V4 prompts (for v4 model)
    v4_prompt: V4ConditionInput | None = Field(
        default=None,
        description="V4 prompt structure (auto-generated from input prompt for V4 models if not provided)",
    )
    v4_negative_prompt: V4ConditionInput | None = Field(
        default=None,
        description="V4 negative prompt structure (auto-generated from negative_prompt for V4 models if not provided)",
    )

    # Sampling parameters
    sm: bool | None = Field(default=None, description="(inop) SMEA sampling")
    sm_dyn: bool | None = Field(default=None, description="(inop) SMEA DYN sampling")
    autoSmea: bool | None = Field(
        default=None, description="(inop) Auto SMEA (alternative to sm/sm_dyn)"
    )
    dynamic_thresholding: bool | None = Field(
        default=None, description="Enable dynamic thresholding"
    )
    cfg_rescale: float | None = Field(
        default=None, ge=0.0, le=1.0, description="CFG rescale"
    )
    noise_schedule: str | None = Field(default=None, description="Noise schedule")
    legacy: bool | None = Field(default=None, description="Use legacy mode")
    legacy_uc: bool | None = Field(
        default=None, description="Use legacy undesired content"
    )
    legacy_v3_extend: bool | None = Field(
        default=None, description="Use legacy V3 extend"
    )
    skip_cfg_above_sigma: Literal[58] | None = Field(
        default=None, description="Skip CFG above sigma (Variety Boost)"
    )
    deliberate_euler_ancestral_bug: bool | None = Field(
        default=None, description="(inop) Maintain Euler ancestral bug compatibility"
    )
    prefer_brownian: bool | None = Field(
        default=None, description="(inop) Prefer Brownian noise"
    )

    # i2i parameters
    image: str | None = Field(default=None, description="Base64 encoded source image")
    strength: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Strength for img2img"
    )
    noise: float | None = Field(default=None, description="Noise amount")
    extra_noise_seed: int | None = Field(default=None, description="Extra noise seed")
    img2img: Img2ImgParams | None = Field(
        default=None, description="Img2img parameters"
    )

    # Inpainting parameters
    mask: str | None = Field(default=None, description="Base64 encoded mask image")
    add_original_image: bool | None = Field(
        default=None, description="Add original image to output"
    )
    color_correct: bool | None = Field(
        default=None, description="Apply color correction"
    )
    inpaintImg2ImgStrength: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Inpaint i2i strength"
    )

    # ControlNet parameters
    controlnet_strength: float | None = Field(
        default=None, ge=0.0, le=1.0, description="ControlNet strength"
    )
    normalize_reference_strength_multiple: bool | None = Field(
        default=None,
        description="Normalize controlnet reference strength for multiple references",
    )

    # Controlnet image parameters
    reference_information_extracted: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Reference information extracted"
    )
    reference_image_multiple: list[str] | None = Field(
        default=None, description="Multiple encoded vibe-transfer data (base64)"
    )
    reference_strength_multiple: list[float] | None = Field(
        default=None, description="Multiple reference strengths"
    )
    reference_information_extracted_multiple: list[float] | None = Field(
        default=None, description="Multiple reference information extracted"
    )

    # Director Tools (Character Reference)
    director_reference_images: list[str] | None = Field(
        default=None, description="Director reference images (base64)"
    )
    director_reference_strength_values: list[float] | None = Field(
        default=None, description="Director reference strengths"
    )
    director_reference_secondary_strength_values: list[float] | None = Field(
        default=None, description="Director reference secondary strengths (Fidelity)"
    )
    director_reference_information_extracted: list[float] | None = Field(
        default=None, description="Director reference information extracted"
    )
    director_reference_descriptions: list[ReferenceConditionInput] | None = Field(
        default=None, description="Director reference descriptions"
    )

    # Character prompts
    characterPrompts: list[CharacterPrompt] | None = Field(
        default=None, description="Character-specific prompts with positioning"
    )

    # Misc
    params_version: int | None = Field(default=None, description="Parameters version")
    use_coords: bool | None = Field(
        default=None, description="Use coordinates for positioning"
    )
    image_format: Literal["webp", "png"] | None = Field(
        default=None, description="Image format (webp is lossless, default is png)"
    )


class ImageStreamParameters(ImageParameters):
    """Parameters for image generation stream"""

    stream: StreamingType | None = Field(
        default=None, description="Enable streaming (msgpack or sse)"
    )


class BaseImageGenerationRequest(BaseModel):
    """Base request for image generation - low-level API model

    This mirrors the NovelAI REST API exactly without any automatic processing.
    """

    model_config = ConfigDict(extra="forbid")

    action: str | None = Field(
        default=None, description="Action type (generate, img2img, infill, etc.)"
    )
    input: str = Field(
        ..., min_length=1, description="Text prompt for image generation"
    )
    model: str | None = Field(default=None, description="Model to use for generation")
    use_new_shared_trial: bool | None = Field(
        default=None, description="Use new shared trial system"
    )
    url: str | None = Field(default=None, description="Optional URL field")


class ImageGenerationRequest(BaseImageGenerationRequest):
    """Complete request for image generation"""

    parameters: ImageParameters = Field(..., description="Generation parameters")


class StreamImageGenerationRequest(BaseImageGenerationRequest):
    """Complete request for image generation (stream)"""

    parameters: ImageStreamParameters = Field(
        ...,
        description="Generation parameters with streaming enabled",
    )


class ImageGenerationResponse(BaseModel):
    """Response from image generation API"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: bytes = Field(..., description="Generated image data in base64 or raw bytes")
    seed: int | None = Field(None, description="Seed used for generation")


class ImageStreamChunk(BaseModel):
    """Chunk of image generation stream"""

    event_type: Literal["intermediate", "final"] = Field(..., description="Event type")
    samp_ix: int = Field(..., description="Sample index")
    step_ix: int | None = Field(default=-1, description="Step index")
    gen_id: int = Field(..., description="Generation ID")
    sigma: float | None = Field(default=-1, description="Sigma")
    image: str = Field(..., description="Image data in base64")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_text_chunk(cls, text: str) -> ImageStreamChunk:
        """Create ImageStreamChunk from text chunk"""
        print(text)
        if text.startswith("data: "):
            text = text.split("data: ")[1]
        return cls.model_validate_json(text)
