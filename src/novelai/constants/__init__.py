"""NovelAI constants - Models, samplers, sizes, noise schedules, and presets

We recommend literal instead of constants - it can be used without importing constants.
Check examples for further details.
"""

from __future__ import annotations

from .models import (
    V3,
    V3_FURRY,
    V4_5_CURATED,
    V4_5_FULL,
    V4_CURATED,
    V4_FULL,
    ImageModel,
)
from .noise_schedule import (
    NOISE_EXPONENTIAL,
    NOISE_KARRAS,
    NOISE_POLYEXPONENTIAL,
    NoiseSchedule,
    StreamingType,
)
from .presets import (
    QUALITY_TAGS,
    UC_FURRY_FOCUS,
    UC_HUMAN_FOCUS,
    UC_LIGHT,
    UC_NONE,
    UC_STRONG,
    UNDESIRED_CONTENT_PRESETS,
    UCPreset,
    UndesiredContentPreset,
)
from .samplers import (
    DDIM,
    K_DPM_2,
    K_DPM_2_ANCESTRAL,
    K_DPM_ADAPTIVE,
    K_DPM_FAST,
    K_DPM_SDE,
    K_EULER,
    K_EULER_ANCESTRAL,
    Sampler,
)
from .sizes import ImageSize, ImageSizePreset

__all__ = [
    # Models
    "ImageModel",
    "V4_5_FULL",
    "V4_5_CURATED",
    "V4_FULL",
    "V4_CURATED",
    "V3",
    "V3_FURRY",
    # Samplers
    "Sampler",
    "K_EULER",
    "K_EULER_ANCESTRAL",
    "K_DPM_2",
    "K_DPM_2_ANCESTRAL",
    "K_DPM_FAST",
    "K_DPM_ADAPTIVE",
    "K_DPM_SDE",
    "DDIM",
    # Sizes
    "ImageSize",
    "ImageSizePreset",
    # Noise
    "NoiseSchedule",
    "NOISE_KARRAS",
    "NOISE_EXPONENTIAL",
    "NOISE_POLYEXPONENTIAL",
    "StreamingType",
    # Presets
    "UCPreset",
    "UndesiredContentPreset",
    "UC_STRONG",
    "UC_LIGHT",
    "UC_FURRY_FOCUS",
    "UC_HUMAN_FOCUS",
    "UC_NONE",
    "QUALITY_TAGS",
    "UNDESIRED_CONTENT_PRESETS",
]
