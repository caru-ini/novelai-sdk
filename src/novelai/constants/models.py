"""Image model constants"""

from __future__ import annotations

from typing import Literal

ImageModel = Literal[
    "nai-diffusion-5-full",
    "nai-diffusion-5-full-medium",
    "nai-diffusion-5-curated",
    "nai-diffusion-4-5-full",
    "nai-diffusion-4-5-curated",
    "nai-diffusion-4-full",
    "nai-diffusion-4-curated-preview",
    "nai-diffusion-3",
    "nai-diffusion-furry-3",
]

V5_FULL: ImageModel = "nai-diffusion-5-full"
V5_FULL_MEDIUM: ImageModel = "nai-diffusion-5-full-medium"
V5_CURATED: ImageModel = "nai-diffusion-5-curated"
V4_5_FULL: ImageModel = "nai-diffusion-4-5-full"
V4_5_CURATED: ImageModel = "nai-diffusion-4-5-curated"
V4_FULL: ImageModel = "nai-diffusion-4-full"
V4_CURATED: ImageModel = "nai-diffusion-4-curated-preview"
V3: ImageModel = "nai-diffusion-3"
V3_FURRY: ImageModel = "nai-diffusion-furry-3"

INPAINTING_MODELS: dict[ImageModel, str] = {
    V5_FULL: "nai-diffusion-5-full-inpainting",
    V5_FULL_MEDIUM: "nai-diffusion-5-full-medium-inpainting",
    V5_CURATED: "nai-diffusion-4-5-curated-inpainting",
    V4_5_FULL: "nai-diffusion-4-5-full-inpainting",
    V4_5_CURATED: "nai-diffusion-4-5-curated-inpainting",
    V4_FULL: "nai-diffusion-4-full-inpainting",
    V4_CURATED: "nai-diffusion-4-curated-inpainting",
    V3: "nai-diffusion-3-inpainting",
    V3_FURRY: "nai-diffusion-furry-3-inpainting",
}
