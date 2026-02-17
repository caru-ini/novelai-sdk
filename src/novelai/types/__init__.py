"""Type definitions for NovelAI API"""

from .user.image import (
    Character,
    CharacterReference,
    ControlNet,
    ControlNetImage,
    GenerateImageParams,
    GenerateImageStreamParams,
    I2iParams,
    ImageInput,
    InpaintParams,
)

__all__ = [
    # High-level user types
    "Character",
    "CharacterReference",
    "GenerateImageParams",
    "GenerateImageStreamParams",
    "ImageInput",
    "I2iParams",
    "InpaintParams",
    "ControlNet",
    "ControlNetImage",
]
