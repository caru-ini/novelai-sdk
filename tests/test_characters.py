from __future__ import annotations

import asyncio

import pytest
from pydantic import ValidationError

from novelai._utils.converter import (
    async_convert_user_params_to_api_params,
    convert_user_params_to_api_params,
)
from novelai.types import Character, GenerateImageParams
from novelai.types.api.image import ImageParameters


def _convert(
    characters: list[Character] | None, model: str = "nai-diffusion-4-5-full"
) -> ImageParameters:
    params = GenerateImageParams(
        prompt="2girls, standing",
        model=model,  # type: ignore[arg-type]
        characters=characters,
    )
    return convert_user_params_to_api_params(params, None)  # type: ignore[arg-type]


def _caption_centers(api_params: ImageParameters) -> list[tuple[float, float]]:
    assert api_params.v4_prompt is not None
    assert api_params.v4_prompt.caption is not None
    assert api_params.v4_prompt.caption.char_captions is not None
    centers: list[tuple[float, float]] = []
    for caption in api_params.v4_prompt.caption.char_captions:
        assert caption.centers is not None
        assert len(caption.centers) == 1
        centers.append((caption.centers[0].x, caption.centers[0].y))
    return centers


def _prompt_centers(api_params: ImageParameters) -> list[tuple[float, float]]:
    assert api_params.characterPrompts is not None
    return [(c.center.x, c.center.y) for c in api_params.characterPrompts]


def test_explicit_positions_enable_use_coords() -> None:
    api_params = _convert(
        [
            Character(prompt="1girl, red hair", position=(0.3, 0.5)),
            Character(prompt="1boy, black hair", position=(0.7, 0.5)),
        ]
    )

    assert api_params.use_coords is True
    assert api_params.v4_prompt is not None
    assert api_params.v4_prompt.use_coords is True
    assert api_params.v4_prompt.use_order is True
    assert _caption_centers(api_params) == [(0.3, 0.5), (0.7, 0.5)]
    assert _prompt_centers(api_params) == [(0.3, 0.5), (0.7, 0.5)]


def test_omitted_positions_leave_placement_to_the_ai() -> None:
    api_params = _convert(
        [
            Character(prompt="1girl, red hair"),
            Character(prompt="1boy, black hair"),
        ]
    )

    assert api_params.use_coords is False
    assert api_params.v4_prompt is not None
    assert api_params.v4_prompt.use_coords is False
    assert api_params.v4_prompt.use_order is True
    assert _caption_centers(api_params) == [(0.5, 0.5), (0.5, 0.5)]
    assert _prompt_centers(api_params) == [(0.5, 0.5), (0.5, 0.5)]


def test_no_characters_sends_use_coords_false() -> None:
    api_params = _convert(None)

    assert api_params.use_coords is False
    assert api_params.v4_prompt is not None
    assert api_params.v4_prompt.use_coords is False


@pytest.mark.parametrize(
    ("preset", "expected"),
    [("A1", (0.1, 0.1)), ("C3", (0.5, 0.5)), ("E5", (0.9, 0.9)), ("B4", (0.3, 0.7))],
)
def test_grid_preset_is_converted_to_coordinates(
    preset: str, expected: tuple[float, float]
) -> None:
    character = Character(prompt="1girl", position=preset)  # type: ignore[arg-type]

    assert character.position == pytest.approx(expected)

    api_params = _convert([character])

    assert api_params.use_coords is True
    assert _caption_centers(api_params)[0] == pytest.approx(expected)


def test_unpositioned_character_is_centered_when_others_have_positions() -> None:
    api_params = _convert(
        [
            Character(prompt="1girl, red hair", position=(0.3, 0.5)),
            Character(prompt="1boy, black hair"),
        ]
    )

    assert api_params.use_coords is True
    assert _caption_centers(api_params) == [(0.3, 0.5), (0.5, 0.5)]


def test_disabled_character_does_not_enable_use_coords() -> None:
    api_params = _convert(
        [
            Character(prompt="1girl, red hair"),
            Character(prompt="1boy, black hair", position=(0.9, 0.5), enabled=False),
        ]
    )

    assert api_params.use_coords is False
    assert api_params.v4_prompt is not None
    assert api_params.v4_prompt.use_coords is False
    # Disabled characters stay in characterPrompts (enabled=False) but drop out
    # of the V4 captions, matching the web UI.
    assert _caption_centers(api_params) == [(0.5, 0.5)]
    assert api_params.characterPrompts is not None
    assert [c.enabled for c in api_params.characterPrompts] == [True, False]
    assert _prompt_centers(api_params) == [(0.5, 0.5), (0.9, 0.5)]


def test_async_converter_enables_use_coords() -> None:
    params = GenerateImageParams(
        prompt="2girls",
        model="nai-diffusion-4-5-full",
        characters=[Character(prompt="1girl", position=(0.2, 0.5))],
    )

    api_params = asyncio.run(
        async_convert_user_params_to_api_params(params, None)  # type: ignore[arg-type]
    )

    assert api_params.use_coords is True
    assert api_params.v4_prompt is not None
    assert api_params.v4_prompt.use_coords is True


@pytest.mark.parametrize("position", [(1.2, 0.5), (0.5, -0.1), "Z9", "C"])
def test_invalid_position_is_rejected(position: object) -> None:
    with pytest.raises(ValidationError):
        Character(prompt="1girl", position=position)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("position", "expected"),
    [
        ((0.2, 0.5), (0.3, 0.5)),  # 0.2 sits on a cell edge; floor(5x) picks cell 1
        ((0.19, 0.99), (0.1, 0.9)),
        ((0.0, 1.0), (0.1, 0.9)),
        ((0.55, 0.45), (0.5, 0.5)),
    ],
)
def test_v4_positions_are_snapped_to_the_grid(
    position: tuple[float, float], expected: tuple[float, float]
) -> None:
    api_params = _convert([Character(prompt="1girl", position=position)])

    assert api_params.use_coords is True
    assert _caption_centers(api_params)[0] == pytest.approx(expected)
    assert _prompt_centers(api_params)[0] == pytest.approx(expected)


def test_v5_positions_are_sent_as_given() -> None:
    api_params = _convert(
        [Character(prompt="1girl", position=(0.19, 0.99))],
        model="nai-diffusion-5-full",
    )

    assert api_params.use_coords is True
    assert _caption_centers(api_params) == [(0.19, 0.99)]
    assert _prompt_centers(api_params) == [(0.19, 0.99)]


def test_snapping_does_not_mutate_user_characters() -> None:
    character = Character(prompt="1girl", position=(0.2, 0.5))

    _convert([character])

    assert character.position == (0.2, 0.5)
