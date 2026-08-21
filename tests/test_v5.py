from __future__ import annotations

import asyncio

import pytest

from novelai._utils.converter import (
    async_convert_user_params_to_api_params,
    convert_user_params_to_api_params,
)
from novelai.types import CharacterReference, ControlNet, ControlNetImage
from novelai.types.api.image import ImageParameters
from novelai.types.user.image import GenerateImageParams


def test_v5_model_uses_v4_prompt_structure() -> None:
    params = GenerateImageParams(
        prompt="1girl, standing",
        model="nai-diffusion-5-full",
        size=(1024, 1024),
    )

    api_params = convert_user_params_to_api_params(params, None)  # type: ignore[arg-type]

    assert GenerateImageParams.is_v5(params.model)
    assert GenerateImageParams.is_v4(params.model)
    assert api_params.params_version == 4
    assert api_params.prompt is None
    assert api_params.v4_prompt is not None
    assert api_params.v4_negative_prompt is not None


@pytest.mark.parametrize(
    "model",
    ["nai-diffusion-4-5-full", "nai-diffusion-3"],
)
def test_existing_models_keep_params_version_three(model: str) -> None:
    params = GenerateImageParams(prompt="1girl", model=model)

    api_params = convert_user_params_to_api_params(params, None)  # type: ignore[arg-type]

    assert api_params.params_version == 3


def test_non_v5_models_do_not_send_v5_fields() -> None:
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
    )

    api_params = convert_user_params_to_api_params(params, None)  # type: ignore[arg-type]

    assert api_params.straight_alpha is None
    assert api_params.tag_hint_transparent_background is None
    assert "straight_alpha" not in api_params.model_dump(exclude_none=True)
    assert "tag_hint_transparent_background" not in api_params.model_dump(
        exclude_none=True
    )


def test_async_converter_uses_v5_params_version() -> None:
    params = GenerateImageParams(prompt="1girl", model="nai-diffusion-5-full")

    api_params = asyncio.run(
        async_convert_user_params_to_api_params(params, None)  # type: ignore[arg-type]
    )

    assert api_params.params_version == 4


def test_controlnet_is_rejected_for_v5() -> None:
    with pytest.raises(
        ValueError, match="Vibe Transfer/ControlNet is not supported for V5 models"
    ):
        GenerateImageParams(
            prompt="1girl",
            model="nai-diffusion-5-full",
            controlnet=ControlNet(images=[ControlNetImage(image=b"reference")]),
        )


def test_character_references_are_rejected_for_v5() -> None:
    with pytest.raises(
        ValueError, match="Character references are only supported for V4.5 models"
    ):
        GenerateImageParams(
            prompt="1girl",
            model="nai-diffusion-5-full",
            character_references=[CharacterReference(image=b"reference")],
        )


def test_v5_only_parameters_are_rejected_for_non_v5() -> None:
    with pytest.raises(
        ValueError,
        match="straight_alpha and tag_hint_transparent_background are only "
        "supported for V5 models",
    ):
        GenerateImageParams(
            prompt="1girl",
            model="nai-diffusion-4-5-full",
            straight_alpha=True,
        )


def test_v5_parameters_are_converted_to_api_fields() -> None:
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-5-full",
        straight_alpha=True,
        tag_hint_transparent_background=True,
    )

    api_params = convert_user_params_to_api_params(params, None)  # type: ignore[arg-type]

    assert api_params.straight_alpha is True
    assert api_params.tag_hint_transparent_background is True


def test_api_image_parameters_accept_v5_fields() -> None:
    params = ImageParameters(
        straight_alpha=True,
        tag_hint_transparent_background=True,
        tag_hint_qt=True,
        tag_hint_uc_preset=2,
    )

    assert params.straight_alpha is True
    assert params.tag_hint_transparent_background is True
    assert params.tag_hint_qt is True
    assert params.tag_hint_uc_preset == 2


def test_anlas_calculation_supports_v5() -> None:
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-5-full",
        size=(1024, 1024),
        steps=28,
    )

    estimate = params.calculate_anlas()

    assert estimate.model == "nai-diffusion-5-full"
    assert estimate.total_anlas == estimate.per_image_anlas
