"""Anlas estimation helpers for NovelAI image generation.

This module implements an image-generation Anlas estimate reverse-engineered
from the official web interface and current documentation.

The current implementation matches the V3, V3 Furry, V4, and V4.5 model
families supported by this SDK, but it is still an estimate and should not be
treated as a 100% guaranteed billing source of truth.
"""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING, Final

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from novelai.types.api.image import ImageParameters
    from novelai.types.user.image import GenerateImageParams, GenerateImageStreamParams

_AREA_COEFFICIENT: Final[float] = 2.951823174884865e-6
_STEP_AREA_COEFFICIENT: Final[float] = 5.753298233447344e-7
_SMEA_MULTIPLIER: Final[float] = 1.2
_SMEA_DYN_MULTIPLIER: Final[float] = 1.4
_MAX_PER_IMAGE_ANLAS: Final[int] = 140
_LIGHTWEIGHT_OPUS_MAX_PIXELS: Final[int] = 1_048_576
_LIGHTWEIGHT_OPUS_MAX_STEPS: Final[int] = 28
_VIBE_EXTRA_ANLAS: Final[int] = 2
_CHARACTER_REFERENCE_EXTRA_ANLAS: Final[int] = 5

_SUPPORTED_V4_STYLE_MODELS: Final[frozenset[str]] = frozenset(
    {
        "nai-diffusion-3",
        "nai-diffusion-3-inpainting",
        "nai-diffusion-3-furry",
        "nai-diffusion-furry-3",
        "nai-diffusion-furry-3-inpainting",
        "nai-diffusion-4-full",
        "nai-diffusion-4-full-inpainting",
        "nai-diffusion-4-curated",
        "nai-diffusion-4-curated-preview",
        "nai-diffusion-4-curated-inpainting",
        "nai-diffusion-4-5-full",
        "nai-diffusion-4-5-full-inpainting",
        "nai-diffusion-4-5-curated",
        "nai-diffusion-4-5-curated-inpainting",
        "custom",
    }
)
_V4_PLUS_VIBE_MODELS: Final[frozenset[str]] = frozenset(
    {
        "nai-diffusion-4-full",
        "nai-diffusion-4-full-inpainting",
        "nai-diffusion-4-curated",
        "nai-diffusion-4-curated-preview",
        "nai-diffusion-4-curated-inpainting",
        "nai-diffusion-4-5-full",
        "nai-diffusion-4-5-full-inpainting",
        "nai-diffusion-4-5-curated",
        "nai-diffusion-4-5-curated-inpainting",
        "custom",
    }
)


class AnlasEstimate(BaseModel):
    """Calculated Anlas cost for a single generation request."""

    model: str
    total_anlas: int
    base_anlas: int
    character_reference_anlas: int
    vibe_encoding_anlas: int
    vibe_reference_anlas: int
    per_image_anlas: int
    requested_samples: int
    billable_samples: int
    strength_factor: float
    opus_discount_applied: bool

    model_config = ConfigDict(frozen=True)

    def __str__(self) -> str:
        return str(self.total_anlas)

    def __int__(self) -> int:
        return self.total_anlas


def _validate_supported_model(model: str) -> str:
    if model in _SUPPORTED_V4_STYLE_MODELS:
        return model

    supported = ", ".join(sorted(_SUPPORTED_V4_STYLE_MODELS))
    raise NotImplementedError(
        "Anlas calculation is currently implemented for the SDK's V3/V3 Furry/V4/"
        f"V4.5 model families. Unsupported model: {model!r}. Supported values: {supported}"
    )


def _strength_factor_from_api_params(params: ImageParameters) -> float:
    if params.mask is not None:
        return params.inpaintImg2ImgStrength or 1.0
    if params.image is not None:
        return params.strength or 1.0
    return 1.0


def _estimate_supported_request(
    *,
    model: str,
    width: int,
    height: int,
    steps: int,
    n_samples: int,
    strength_factor: float,
    sm: bool,
    sm_dyn: bool,
    is_opus: bool,
) -> AnlasEstimate:
    _validate_supported_model(model)

    area = width * height
    multiplier = 1.0
    if sm:
        multiplier = _SMEA_DYN_MULTIPLIER if sm_dyn else _SMEA_MULTIPLIER

    base_cost = ceil(_AREA_COEFFICIENT * area + _STEP_AREA_COEFFICIENT * area * steps)
    per_image_anlas = max(ceil(base_cost * multiplier * strength_factor), 2)

    if per_image_anlas > _MAX_PER_IMAGE_ANLAS:
        raise ValueError(
            "Estimated per-image cost exceeds the current supported cap of "
            f"{_MAX_PER_IMAGE_ANLAS} Anlas: {per_image_anlas}"
        )

    opus_discount_applied = bool(
        is_opus
        and area <= _LIGHTWEIGHT_OPUS_MAX_PIXELS
        and steps <= _LIGHTWEIGHT_OPUS_MAX_STEPS
    )
    billable_samples = max(n_samples - 1, 0) if opus_discount_applied else n_samples

    base_anlas = per_image_anlas * billable_samples

    return AnlasEstimate(
        model=model,
        total_anlas=base_anlas,
        base_anlas=base_anlas,
        character_reference_anlas=0,
        vibe_encoding_anlas=0,
        vibe_reference_anlas=0,
        per_image_anlas=per_image_anlas,
        requested_samples=n_samples,
        billable_samples=billable_samples,
        strength_factor=strength_factor,
        opus_discount_applied=opus_discount_applied,
    )


def _supports_v4_plus_vibe_costs(model: str) -> bool:
    return model in _V4_PLUS_VIBE_MODELS


def _with_character_reference_extras(
    estimate: AnlasEstimate,
    *,
    character_reference_count: int,
) -> AnlasEstimate:
    character_reference_anlas = max(character_reference_count, 0) * (
        _CHARACTER_REFERENCE_EXTRA_ANLAS * estimate.requested_samples
    )
    return estimate.model_copy(
        update={
            "character_reference_anlas": character_reference_anlas,
            "total_anlas": estimate.total_anlas + character_reference_anlas,
        }
    )


def _with_vibe_extras(
    estimate: AnlasEstimate,
    *,
    vibe_reference_count: int,
    uncached_vibe_count: int = 0,
) -> AnlasEstimate:
    if not _supports_v4_plus_vibe_costs(estimate.model):
        return estimate

    vibe_encoding_anlas = max(uncached_vibe_count, 0) * _VIBE_EXTRA_ANLAS
    extra_reference_count = max(vibe_reference_count - 4, 0)
    vibe_reference_anlas = extra_reference_count * _VIBE_EXTRA_ANLAS

    return estimate.model_copy(
        update={
            "vibe_encoding_anlas": vibe_encoding_anlas,
            "vibe_reference_anlas": vibe_reference_anlas,
            "total_anlas": estimate.total_anlas
            + vibe_encoding_anlas
            + vibe_reference_anlas,
        }
    )


def calculate_anlas(
    model: str,
    params: ImageParameters,
    *,
    is_opus: bool = False,
) -> AnlasEstimate:
    """Estimate Anlas from low-level API parameters.

    This is intended to closely match the current web UI behavior, but it is
    not guaranteed to be 100% accurate for billing.
    """

    if params.width is None or params.height is None:
        raise ValueError("width and height are required to calculate Anlas")
    if params.steps is None:
        raise ValueError("steps is required to calculate Anlas")
    if params.n_samples is None:
        raise ValueError("n_samples is required to calculate Anlas")

    estimate = _estimate_supported_request(
        model=model,
        width=params.width,
        height=params.height,
        steps=params.steps,
        n_samples=params.n_samples,
        strength_factor=_strength_factor_from_api_params(params),
        sm=bool(params.sm),
        sm_dyn=bool(params.sm and params.sm_dyn),
        is_opus=is_opus,
    )
    estimate = _with_character_reference_extras(
        estimate,
        character_reference_count=len(params.director_reference_images or []),
    )
    return _with_vibe_extras(
        estimate,
        vibe_reference_count=len(params.reference_image_multiple or []),
    )


def calculate_anlas_from_params(
    params: GenerateImageParams | GenerateImageStreamParams,
    *,
    is_opus: bool = False,
) -> AnlasEstimate:
    """Estimate Anlas from high-level generation parameters.

    This is intended to closely match the current web UI behavior, but it is
    not guaranteed to be 100% accurate for billing.
    """

    if not isinstance(params.size, tuple):
        raise ValueError("size must be resolved to a (width, height) tuple")

    width, height = params.size
    i2i = params.i2i
    inpaint = params.inpaint
    has_mask = bool(inpaint and inpaint.mask is not None)
    has_image = bool(i2i and i2i.image is not None)

    if has_mask:
        strength_factor = 1.0
    elif has_image:
        if i2i is None:
            raise ValueError("img2img parameters are required when an image is present")
        strength_factor = i2i.strength
    else:
        strength_factor = 1.0

    estimate = _estimate_supported_request(
        model=params.model,
        width=width,
        height=height,
        steps=params.steps,
        n_samples=params.n_samples,
        strength_factor=strength_factor,
        sm=False,
        sm_dyn=False,
        is_opus=is_opus,
    )
    estimate = _with_character_reference_extras(
        estimate,
        character_reference_count=len(params.character_references or []),
    )
    controlnet_images = params.controlnet.images if params.controlnet else []
    uncached_vibe_count = sum(1 for img in controlnet_images if img._vibe_data is None)
    return _with_vibe_extras(
        estimate,
        vibe_reference_count=len(controlnet_images),
        uncached_vibe_count=uncached_vibe_count,
    )


__all__ = [
    "AnlasEstimate",
    "calculate_anlas",
    "calculate_anlas_from_params",
]
