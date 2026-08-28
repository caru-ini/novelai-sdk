"""Type definitions for NovelAI API"""

from .api.tags import (
    JpTagSuggestion,
    TagSuggestion,
)
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
from .user.tags import SuggestTagsParams
from .user.tools import (
    BackgroundRemovalParams,
    ColorizeParams,
    DeclutterParams,
    DirectorToolParams,
    EmotionParams,
    LineArtParams,
    SketchParams,
    UpscaleParams,
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
    # Director Tools
    "BackgroundRemovalParams",
    "ColorizeParams",
    "DeclutterParams",
    "DirectorToolParams",
    "EmotionParams",
    "LineArtParams",
    "SketchParams",
    "UpscaleParams",
    # Tag suggestions
    "SuggestTagsParams",
    "TagSuggestion",
    "JpTagSuggestion",
    "Subscription",
    "SubscriptionPerks",
    "TrainingStepsLeft",
    "UnlimitedImageGenerationLimit",
]
