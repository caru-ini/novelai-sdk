from __future__ import annotations

import pytest

from novelai.types import (
    CharacterReference,
    ControlNet,
    ControlNetImage,
    GenerateImageParams,
    I2iParams,
)
from novelai.types.api.image import ImageParameters
from novelai.utils.anlas import calculate_anlas


def test_high_level_estimate_matches_v4_formula() -> None:
    params = GenerateImageParams(
        prompt="1girl, standing",
        model="nai-diffusion-4-5-full",
        size=(1024, 1024),
        steps=28,
        n_samples=2,
    )

    estimate = params.calculate_anlas()

    assert estimate.per_image_anlas == 20
    assert estimate.billable_samples == 2
    assert estimate.total_anlas == 40
    assert estimate.base_anlas == 40
    assert estimate.character_reference_anlas == 0
    assert estimate.vibe_encoding_anlas == 0
    assert estimate.vibe_reference_anlas == 0
    assert estimate.opus_discount_applied is False
    assert str(estimate) == "40"
    assert int(estimate) == 40


def test_opus_lightweight_discount_makes_one_sample_free() -> None:
    params = GenerateImageParams(
        prompt="1girl, standing",
        model="nai-diffusion-4-5-full",
        size=(1024, 1024),
        steps=28,
        n_samples=1,
    )

    estimate = params.calculate_anlas(is_opus=True)

    assert estimate.per_image_anlas == 20
    assert estimate.billable_samples == 0
    assert estimate.total_anlas == 0
    assert estimate.opus_discount_applied is True


def test_character_reference_on_opus_keeps_base_free_and_adds_only_reference_fee() -> (
    None
):
    params = GenerateImageParams(
        prompt="1girl, standing",
        model="nai-diffusion-4-5-full",
        size=(1024, 1024),
        steps=28,
        n_samples=1,
        character_references=[CharacterReference(image=b"ref-image")],
    )

    estimate = params.calculate_anlas(is_opus=True)

    assert estimate.billable_samples == 0
    assert estimate.base_anlas == 0
    assert estimate.character_reference_anlas == 5
    assert estimate.total_anlas == 5
    assert estimate.opus_discount_applied is True


def test_character_reference_adds_five_anlas_without_opus_discount() -> None:
    params = GenerateImageParams(
        prompt="1girl, standing",
        model="nai-diffusion-4-5-full",
        size=(1024, 1024),
        steps=28,
        n_samples=1,
        character_references=[CharacterReference(image=b"ref-image")],
    )

    estimate = params.calculate_anlas()

    assert estimate.billable_samples == 1
    assert estimate.base_anlas == 20
    assert estimate.character_reference_anlas == 5
    assert estimate.total_anlas == 25


def test_img2img_strength_reduces_cost() -> None:
    params = GenerateImageParams(
        prompt="1girl, standing",
        model="nai-diffusion-4-5-full",
        size=(1024, 1024),
        steps=23,
        i2i=I2iParams(image=b"source-image", strength=0.7),
    )

    estimate = params.calculate_anlas()

    assert estimate.per_image_anlas == 12
    assert estimate.total_anlas == 12
    assert estimate.strength_factor == 0.7


def test_inpaint_uses_inpaint_strength_factor_from_low_level_params() -> None:
    params = ImageParameters(
        width=1024,
        height=1024,
        steps=28,
        n_samples=1,
        image="source-image-dummy",
        mask="mask-image-dummy",
        strength=0.2,
        inpaintImg2ImgStrength=0.5,
    )

    estimate = calculate_anlas("nai-diffusion-4-5-full", params)

    assert estimate.per_image_anlas == 10
    assert estimate.base_anlas == 10
    assert estimate.character_reference_anlas == 0
    assert estimate.total_anlas == 10
    assert estimate.strength_factor == 0.5


def test_uncached_vibes_add_encoding_fee_for_v4_plus_models() -> None:
    params = GenerateImageParams(
        prompt="1girl, standing",
        model="nai-diffusion-4-5-full",
        size=(1024, 1024),
        steps=28,
        controlnet=ControlNet(
            images=[
                ControlNetImage(image=b"img-1-dummy"),
                ControlNetImage(image=b"img-2-dummy"),
            ]
        ),
    )

    estimate = params.calculate_anlas()

    assert estimate.base_anlas == 20
    assert estimate.character_reference_anlas == 0
    assert estimate.vibe_encoding_anlas == 4
    assert estimate.vibe_reference_anlas == 0
    assert estimate.total_anlas == 24


def test_multivibe_adds_two_anlas_per_reference_after_four() -> None:
    images = [ControlNetImage(image=f"img-{i}-dummy".encode()) for i in range(5)]
    for image in images:
        image._vibe_data = "dummy-data"

    params = GenerateImageParams(
        prompt="1girl, standing",
        model="nai-diffusion-4-5-full",
        size=(1024, 1024),
        steps=28,
        controlnet=ControlNet(images=images),
    )

    estimate = params.calculate_anlas()

    assert estimate.base_anlas == 20
    assert estimate.character_reference_anlas == 0
    assert estimate.vibe_encoding_anlas == 0
    assert estimate.vibe_reference_anlas == 2
    assert estimate.total_anlas == 22


def test_low_level_reference_count_adds_multivibe_surcharge() -> None:
    params = ImageParameters(
        width=1024,
        height=1024,
        steps=28,
        n_samples=1,
        reference_image_multiple=["a", "b", "c", "d", "e"],
    )

    estimate = calculate_anlas("nai-diffusion-4-5-full", params)

    assert estimate.base_anlas == 20
    assert estimate.character_reference_anlas == 0
    assert estimate.vibe_encoding_anlas == 0
    assert estimate.vibe_reference_anlas == 2
    assert estimate.total_anlas == 22


def test_low_level_character_references_add_five_per_reference_per_requested_sample() -> (
    None
):
    params = ImageParameters(
        width=1024,
        height=1024,
        steps=28,
        n_samples=2,
        director_reference_images=["ref-1", "ref-2"],
    )

    estimate = calculate_anlas("nai-diffusion-4-5-full", params)

    assert estimate.base_anlas == 40
    assert estimate.character_reference_anlas == 20
    assert estimate.total_anlas == 60


def test_unsupported_models_raise_not_implemented() -> None:
    params = ImageParameters(width=832, height=1216, steps=23, n_samples=1)

    with pytest.raises(NotImplementedError):
        calculate_anlas("nai-diffusion-2", params)
