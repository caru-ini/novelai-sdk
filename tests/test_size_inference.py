"""Tests for size handling in GenerateImageParams.

Regression coverage for https://github.com/caru-ini/novelai-sdk/issues/73:
omitting `size` should not fail; defaults are validated and preset names are
resolved, and inpaint/i2i without explicit size auto-infer from the source.
"""

from __future__ import annotations

from PIL import Image

from novelai.types import GenerateImageParams, I2iParams, InpaintParams


def _solid_image(width: int, height: int) -> Image.Image:
    return Image.new("RGB", (width, height), (255, 255, 255))


def test_default_size_resolves_to_portrait_tuple() -> None:
    """Omitting size must resolve the default preset to a tuple, not leave it as a string."""
    params = GenerateImageParams(prompt="1girl")
    assert params.size == (832, 1216)


def test_string_preset_is_resolved_to_tuple() -> None:
    params = GenerateImageParams(prompt="1girl", size="landscape")
    assert params.size == (1216, 832)


def test_explicit_tuple_size_is_kept() -> None:
    params = GenerateImageParams(prompt="1girl", size=(1024, 1024))
    assert params.size == (1024, 1024)


def test_inpaint_without_size_infers_from_source_image() -> None:
    source = _solid_image(1024, 1024)
    mask = _solid_image(1024, 1024)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        inpaint=InpaintParams(image=source, mask=mask, strength=1.0),
    )
    assert params.size == (1024, 1024)


def test_inpaint_with_explicit_size_does_not_override() -> None:
    source = _solid_image(1024, 1024)
    mask = _solid_image(1024, 1024)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        size=(832, 1216),
        inpaint=InpaintParams(image=source, mask=mask, strength=1.0),
    )
    assert params.size == (832, 1216)


def test_i2i_without_size_infers_from_source_image() -> None:
    source = _solid_image(768, 1280)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        i2i=I2iParams(image=source, strength=0.7),
    )
    assert params.size == (768, 1280)


def test_inferred_size_rounds_to_multiple_of_64() -> None:
    # 900x600 = 0.54MP — under the standard cap, so no scaling, only rounding:
    # 900/64 = 14.0625 -> round to 14*64 = 896
    # 600/64 = 9.375   -> round to 9*64  = 576
    source = _solid_image(900, 600)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        inpaint=InpaintParams(image=source, mask=source, strength=1.0),
    )
    assert params.size == (896, 576)


def test_inferred_size_caps_at_standard_resolution() -> None:
    # 1920x1080 = 2.07MP, scaled down to ~1MP preserving 16:9 aspect ratio.
    # scale = sqrt(1048576 / 2073600) ≈ 0.7111
    # 1920*0.7111 ≈ 1365.3 -> round(21.33)=21 -> 21*64 = 1344
    # 1080*0.7111 ≈ 768.0  -> round(12.0) =12 -> 12*64 = 768
    source = _solid_image(1920, 1080)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        i2i=I2iParams(image=source, strength=0.7),
    )
    width, height = params.size
    assert (width, height) == (1344, 768)
    # Stays within standard tier (~1MP)
    assert width * height <= 1024 * 1024 * 1.1


def test_inferred_size_keeps_small_source_unchanged() -> None:
    # 768x768 is already under the standard cap; should not be scaled up.
    source = _solid_image(768, 768)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        i2i=I2iParams(image=source, strength=0.7),
    )
    assert params.size == (768, 768)


def test_inferred_size_for_3328x4864_matches_portrait_preset() -> None:
    """A common large portrait source (~16MP) collapses cleanly onto the
    832x1216 portrait preset — the canonical case from issue #73."""
    source = _solid_image(3328, 4864)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        inpaint=InpaintParams(image=source, mask=source, strength=1.0),
    )
    assert params.size == (832, 1216)


def test_inferred_size_below_64px_clamps_to_minimum() -> None:
    source = _solid_image(32, 32)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        i2i=I2iParams(image=source, strength=0.7),
    )
    assert params.size == (64, 64)


def test_inferred_size_extreme_aspect_ratio_respects_api_limits() -> None:
    """Sources whose long side exceeds 1600px must scale proportionally so
    that we don't silently distort the aspect ratio with a final clamp."""
    # 4000x100 — area is under 1MP but width far exceeds the 1600px API limit.
    # dim_scale = 1600/4000 = 0.4 -> (1600, 40) -> rounded to (1600, 64).
    source = _solid_image(4000, 100)
    params = GenerateImageParams(
        prompt="1girl",
        model="nai-diffusion-4-5-full",
        i2i=I2iParams(image=source, strength=0.7),
    )
    assert params.size == (1600, 64)
    width, height = params.size
    assert 64 <= width <= 1600
    assert 64 <= height <= 1600
