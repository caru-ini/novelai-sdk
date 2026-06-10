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
from .user.user import (
    Subscription,
    SubscriptionPerks,
    TrainingStepsLeft,
    UnlimitedImageGenerationLimit,
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
    "Subscription",
    "SubscriptionPerks",
    "TrainingStepsLeft",
    "UnlimitedImageGenerationLimit",
]
