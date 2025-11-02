"""Image size constants"""

from __future__ import annotations

from typing import Literal

ImageSizePreset = Literal[
    "portrait", "landscape", "square", "large_portrait", "large_landscape"
]
ImageSize = tuple[int, int] | ImageSizePreset

PRESET_MAP: dict[ImageSizePreset, ImageSize] = {
    "portrait": (832, 1216),
    "landscape": (1216, 832),
    "square": (1024, 1024),
    "large_portrait": (1024, 1536),
    "large_landscape": (1536, 1024),
}
