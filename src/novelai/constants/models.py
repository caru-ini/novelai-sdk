"""Image model constants"""

from __future__ import annotations

from typing import Literal

ImageModel = Literal[
    "nai-diffusion-4-5-full",
    "nai-diffusion-4-5-curated",
    "nai-diffusion-4-full",
    "nai-diffusion-4-curated",
    "nai-diffusion-3",
    "nai-diffusion-3-furry",
]

V4_5_FULL: ImageModel = "nai-diffusion-4-5-full"
V4_5_CURATED: ImageModel = "nai-diffusion-4-5-curated"
V4_FULL: ImageModel = "nai-diffusion-4-full"
V4_CURATED: ImageModel = "nai-diffusion-4-curated"
V3: ImageModel = "nai-diffusion-3"
V3_FURRY: ImageModel = "nai-diffusion-3-furry"
