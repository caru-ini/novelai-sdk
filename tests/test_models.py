from __future__ import annotations

import io
from typing import get_args

import pytest
from PIL import Image
from pydantic import ValidationError

from novelai._utils.converter import convert_user_params_to_api_request
from novelai.constants.models import (
    INPAINTING_MODELS,
    V3_FURRY,
    V4_5_FULL,
    V4_CURATED,
    V5_CURATED,
    V5_FULL_MEDIUM,
    ImageModel,
)
from novelai.constants.negative_prompts import (
    QUALITY_TAGS,
    UNDESIRED_CONTENT_PRESETS,
)
from novelai.types.user.image import GenerateImageParams, InpaintParams


def _png_bytes(color: tuple[int, int, int] = (200, 30, 30)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (64, 64), color).save(buffer, format="PNG")
    return buffer.getvalue()


def _inpaint() -> InpaintParams:
    return InpaintParams(image=_png_bytes(), mask=_png_bytes((255, 255, 255)))


@pytest.mark.parametrize("model", get_args(ImageModel))
def test_every_model_has_presets_and_an_inpainting_model(model: ImageModel) -> None:
    assert model in INPAINTING_MODELS
    assert model in QUALITY_TAGS
    assert {"strong", "light", "none"} <= set(UNDESIRED_CONTENT_PRESETS[model])


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        (V4_5_FULL, "nai-diffusion-4-5-full-inpainting"),
        (V5_CURATED, "nai-diffusion-4-5-curated-inpainting"),
        (V5_FULL_MEDIUM, "nai-diffusion-5-full-medium-inpainting"),
        (V4_CURATED, "nai-diffusion-4-curated-inpainting"),
        (V3_FURRY, "nai-diffusion-furry-3-inpainting"),
    ],
)
def test_inpainting_uses_the_web_ui_model(model: ImageModel, expected: str) -> None:
    params = GenerateImageParams(prompt="1girl", model=model, inpaint=_inpaint())

    request = convert_user_params_to_api_request(params, None)  # type: ignore[arg-type]

    assert request.model == expected
    assert request.action == "infill"


def test_v5_curated_inpainting_rejects_transparency() -> None:
    with pytest.raises(ValidationError, match="V4.5 Curated"):
        GenerateImageParams(
            prompt="1girl",
            model=V5_CURATED,
            inpaint=_inpaint(),
            straight_alpha=True,
        )
