from __future__ import annotations

import pytest
from pydantic import ValidationError

from novelai._utils.converter import (
    convert_user_params_to_api_params,
    convert_user_params_to_api_request,
)
from novelai.constants.models import (
    V3,
    V4_5_CURATED,
    V4_5_FULL,
    V4_FULL,
    V5_FULL,
    ImageModel,
)
from novelai.constants.negative_prompts import UNDESIRED_CONTENT_PRESETS
from novelai.types.user.image import GenerateImageParams

V4_5_FULL_STRONG = UNDESIRED_CONTENT_PRESETS[V4_5_FULL]["strong"]


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        (V4_5_FULL, "1girl, very aesthetic, masterpiece, no text"),
        (
            V4_5_CURATED,
            "1girl, very aesthetic, masterpiece, no text, -0.8::feet::, rating:general",
        ),
        (V4_FULL, "1girl, no text, best quality, very aesthetic, absurdres"),
        (V3, "1girl, best quality, amazing quality, very aesthetic, absurdres"),
    ],
)
def test_quality_tags_follow_the_model(model: ImageModel, expected: str) -> None:
    params = GenerateImageParams(prompt="1girl", model=model)

    assert params.processed_prompt == expected


def test_quality_tags_go_before_the_text_marker() -> None:
    params = GenerateImageParams(prompt="1girl, text: Hello", model=V4_5_FULL)

    assert (
        params.processed_prompt
        == "1girl,, very aesthetic, masterpiece, no text text: Hello"
    )


@pytest.mark.parametrize(
    ("prompt", "expected"),
    [
        ("a|b", "a, very aesthetic, masterpiece, no text|b"),
        ("||x|y|| z|w", "||x|y|| z, very aesthetic, masterpiece, no text|w"),
    ],
)
def test_quality_tags_only_touch_the_base_segment(prompt: str, expected: str) -> None:
    params = GenerateImageParams(prompt=prompt, model=V4_5_FULL)

    assert params.processed_prompt == expected


def test_v3_quality_tags_keep_segment_weights() -> None:
    params = GenerateImageParams(prompt="cat:0.7|dog", model=V3)
    tags = "best quality, amazing quality, very aesthetic, absurdres"

    assert params.processed_prompt == f"cat, {tags}:0.7|dog, {tags}"


@pytest.mark.parametrize(
    ("quality", "expected"),
    [
        (True, "1girl, transparent background, very aesthetic, masterpiece, no text"),
        (False, "1girl, transparent background"),
    ],
)
def test_transparent_background_joins_the_quality_tags(
    quality: bool, expected: str
) -> None:
    params = GenerateImageParams(
        prompt="1girl",
        model=V5_FULL,
        quality=quality,
        tag_hint_transparent_background=True,
    )

    assert params.processed_prompt == expected


def test_uc_preset_precedes_negative_prompt_and_adds_nsfw() -> None:
    params = GenerateImageParams(
        prompt="1girl", model=V4_5_FULL, uc_preset="strong", negative_prompt="bad hands"
    )

    assert params.processed_negative_prompt == f"nsfw, {V4_5_FULL_STRONG}, bad hands"


def test_nsfw_prompt_keeps_nsfw_out_of_the_uc() -> None:
    params = GenerateImageParams(
        prompt="nsfw, 1girl", model=V4_5_FULL, uc_preset="strong"
    )

    assert params.processed_negative_prompt == V4_5_FULL_STRONG


def test_curated_models_never_add_nsfw() -> None:
    params = GenerateImageParams(prompt="1girl", model=V4_5_CURATED, uc_preset="strong")

    assert (
        params.processed_negative_prompt
        == UNDESIRED_CONTENT_PRESETS[V4_5_CURATED]["strong"]
    )


def test_uc_preset_only_prefixes_the_base_negative_segment() -> None:
    params = GenerateImageParams(
        prompt="1girl", model=V4_5_FULL, uc_preset="strong", negative_prompt="|blurry"
    )

    assert params.processed_negative_prompt == f"nsfw, {V4_5_FULL_STRONG}|blurry"


def test_none_preset_keeps_only_the_negative_prompt() -> None:
    params = GenerateImageParams(
        prompt="1girl", model=V4_5_FULL, uc_preset="none", negative_prompt="bad hands"
    )

    assert params.processed_negative_prompt == "bad hands"


def test_v3_none_preset_falls_back_to_lowres() -> None:
    params = GenerateImageParams(prompt="1girl", model=V3, uc_preset="none")

    assert params.processed_negative_prompt == "lowres"


def test_uc_preset_must_be_offered_by_the_model() -> None:
    with pytest.raises(ValidationError, match="not available"):
        GenerateImageParams(prompt="1girl", model=V4_FULL, uc_preset="furry_focus")


@pytest.mark.parametrize(
    ("quality", "uc_preset", "expected_qt", "expected_uc"),
    [(True, "light", 1, 3), (False, "strong", 0, 2), (True, "none", 1, 0)],
)
def test_presets_are_sent_as_tag_hints(
    quality: bool, uc_preset: str, expected_qt: int, expected_uc: int
) -> None:
    params = GenerateImageParams(
        prompt="1girl",
        model=V4_5_FULL,
        quality=quality,
        uc_preset=uc_preset,  # type: ignore[arg-type]
    )

    api_params = convert_user_params_to_api_params(params, None)  # type: ignore[arg-type]

    assert api_params.tag_hint_qt == expected_qt
    assert api_params.tag_hint_uc_preset == expected_uc
    assert api_params.ucPreset is None
    assert api_params.qualityToggle is None


def test_request_uses_the_processed_prompts() -> None:
    params = GenerateImageParams(prompt="1girl", model=V4_5_FULL, uc_preset="strong")

    request = convert_user_params_to_api_request(params, None)  # type: ignore[arg-type]

    assert request.input == params.processed_prompt
    v4_prompt = request.parameters.v4_prompt
    v4_negative_prompt = request.parameters.v4_negative_prompt
    assert v4_prompt is not None and v4_prompt.caption is not None
    assert v4_negative_prompt is not None and v4_negative_prompt.caption is not None
    assert v4_prompt.caption.base_caption == params.processed_prompt
    assert v4_negative_prompt.caption.base_caption == params.processed_negative_prompt
    assert request.parameters.negative_prompt == params.processed_negative_prompt
