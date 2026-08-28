from __future__ import annotations

import asyncio
import base64
import io
import json
import zipfile

import httpx
import pytest
from PIL import Image
from pydantic import ValidationError

from novelai import AsyncNovelAI, NovelAI
from novelai.types import (
    BackgroundRemovalParams,
    ColorizeParams,
    DeclutterParams,
    EmotionParams,
    LineArtParams,
    SketchParams,
    UpscaleParams,
)


def _png_bytes(size: tuple[int, int] = (64, 48)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", size, (200, 30, 30)).save(buffer, format="PNG")
    return buffer.getvalue()


def _zip_response(image_count: int = 1) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for i in range(image_count):
            zf.writestr(f"image_{i}.png", _png_bytes())
    return buffer.getvalue()


# --- Parameter models -------------------------------------------------------


def test_line_art_infers_size_from_image() -> None:
    request = LineArtParams(image=_png_bytes(size=(64, 48))).to_api_request()

    assert request.req_type == "lineart"
    assert (request.width, request.height) == (64, 48)
    assert request.prompt is None
    assert request.defry is None
    # The image must round-trip as valid base64
    Image.open(io.BytesIO(base64.b64decode(request.image)))


def test_explicit_size_is_kept() -> None:
    request = SketchParams(image=_png_bytes(), size=(640, 480)).to_api_request()

    assert request.req_type == "sketch"
    assert (request.width, request.height) == (640, 480)


def test_emotion_assembles_mood_prompt() -> None:
    params = EmotionParams(image=_png_bytes(), emotion="happy", prompt="smile", defry=2)
    request = params.to_api_request()

    assert request.req_type == "emotion"
    assert request.prompt == "happy;;smile"
    assert request.defry == 2


def test_emotion_without_extra_prompt_keeps_separator() -> None:
    request = EmotionParams(image=_png_bytes(), emotion="sad").to_api_request()

    assert request.prompt == "sad;;"
    assert request.defry == 0


def test_emotion_requires_mood() -> None:
    with pytest.raises(ValidationError):
        EmotionParams.model_validate({"image": _png_bytes()})


def test_colorize_passes_prompt_and_defry() -> None:
    params = ColorizeParams(image=_png_bytes(), prompt="blue hair", defry=1)
    request = params.to_api_request()

    assert request.req_type == "colorize"
    assert request.prompt == "blue hair"
    assert request.defry == 1


def test_defry_out_of_range_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ColorizeParams(image=_png_bytes(), defry=6)


def test_prompt_is_unrepresentable_for_prompt_free_tools() -> None:
    # Tools without a prompt option reject it as an unknown field
    for params_cls in (LineArtParams, SketchParams, BackgroundRemovalParams):
        with pytest.raises(ValidationError):
            params_cls.model_validate({"image": _png_bytes(), "prompt": "1girl"})


def test_declutter_keep_bubbles_switches_req_type() -> None:
    assert DeclutterParams(image=_png_bytes()).to_api_request().req_type == "declutter"
    assert (
        DeclutterParams(image=_png_bytes(), keep_bubbles=True).to_api_request().req_type
        == "declutter-keep-bubbles"
    )


def test_background_removal_req_type() -> None:
    request = BackgroundRemovalParams(image=_png_bytes()).to_api_request()

    assert request.req_type == "bg-removal"


# --- HTTP layer --------------------------------------------------------------


def _mock_handler(
    captured: list[httpx.Request], image_count: int = 1
) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(
            200,
            content=_zip_response(image_count),
            headers={"Content-Type": "application/x-zip-compressed"},
        )

    return httpx.MockTransport(handler)


def _patched_client(captured: list[httpx.Request], image_count: int = 1) -> NovelAI:
    client = NovelAI(api_key="dummy")
    api = client.api_client
    headers = api.client.headers
    api.client.close()
    api.client = httpx.Client(
        transport=_mock_handler(captured, image_count), headers=headers
    )
    return client


def test_line_art_hits_augment_image() -> None:
    captured: list[httpx.Request] = []
    client = _patched_client(captured)

    try:
        images = client.tools.line_art(_png_bytes(size=(64, 48)))
    finally:
        client.close()

    assert len(images) == 1
    assert captured[0].url == "https://image.novelai.net/ai/augment-image"
    assert captured[0].method == "POST"
    assert captured[0].headers["Authorization"] == "Bearer dummy"

    body = json.loads(captured[0].content)
    assert body["req_type"] == "lineart"
    assert body["width"] == 64
    assert body["height"] == 48
    # exclude_none: unused options must not be sent at all
    assert "prompt" not in body
    assert "defry" not in body


def test_emotion_sends_mood_prompt_and_defry() -> None:
    captured: list[httpx.Request] = []
    client = _patched_client(captured)

    try:
        client.tools.emotion(_png_bytes(), "laughing", prompt="open mouth", defry=3)
    finally:
        client.close()

    body = json.loads(captured[0].content)
    assert body["req_type"] == "emotion"
    assert body["prompt"] == "laughing;;open mouth"
    assert body["defry"] == 3


def test_remove_background_returns_all_zip_entries() -> None:
    captured: list[httpx.Request] = []
    client = _patched_client(captured, image_count=3)

    try:
        images = client.tools.remove_background(_png_bytes())
    finally:
        client.close()

    assert len(images) == 3
    assert json.loads(captured[0].content)["req_type"] == "bg-removal"


def test_async_colorize() -> None:
    captured: list[httpx.Request] = []

    async def run() -> int:
        client = AsyncNovelAI(api_key="dummy")
        api = client.api_client
        headers = api.client.headers
        await api.client.aclose()
        api.client = httpx.AsyncClient(
            transport=_mock_handler(captured), headers=headers
        )
        try:
            images = await client.tools.colorize(_png_bytes(), prompt="vivid colors")
            return len(images)
        finally:
            await client.close()

    assert asyncio.run(run()) == 1
    body = json.loads(captured[0].content)
    assert body["req_type"] == "colorize"
    assert body["prompt"] == "vivid colors"
    assert body["defry"] == 0


# --- Upscale (/ai/upscale) ---------------------------------------------------


def test_upscale_params_default_model() -> None:
    request = UpscaleParams(image=_png_bytes()).to_api_request()

    assert request.model == "nai-diffusion-5-curated"
    # The image must round-trip as valid base64
    Image.open(io.BytesIO(base64.b64decode(request.image)))


def test_upscale_hits_upscale_endpoint() -> None:
    captured: list[httpx.Request] = []
    client = _patched_client(captured)

    try:
        params = UpscaleParams(image=_png_bytes(), model="nai-diffusion-4-5-full")
        images = client.tools.upscale(params)
    finally:
        client.close()

    assert len(images) == 1
    assert captured[0].url == "https://image.novelai.net/ai/upscale"
    assert captured[0].method == "POST"

    body = json.loads(captured[0].content)
    assert body["model"] == "nai-diffusion-4-5-full"
    assert set(body) == {"image", "model"}


def test_upscale_accepts_raw_image_response() -> None:
    # The upscale endpoint's response is not guaranteed to be a ZIP;
    # a bare image body must decode too.
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, content=_png_bytes(size=(128, 96)))

    client = NovelAI(api_key="dummy")
    api = client.api_client
    headers = api.client.headers
    api.client.close()
    api.client = httpx.Client(transport=httpx.MockTransport(handler), headers=headers)

    try:
        images = client.tools.upscale(UpscaleParams(image=_png_bytes()))
    finally:
        client.close()

    assert images[0].size == (128, 96)


def test_async_upscale() -> None:
    captured: list[httpx.Request] = []

    async def run() -> int:
        client = AsyncNovelAI(api_key="dummy")
        api = client.api_client
        headers = api.client.headers
        await api.client.aclose()
        api.client = httpx.AsyncClient(
            transport=_mock_handler(captured), headers=headers
        )
        try:
            images = await client.tools.upscale(UpscaleParams(image=_png_bytes()))
            return len(images)
        finally:
            await client.close()

    assert asyncio.run(run()) == 1
    assert captured[0].url == "https://image.novelai.net/ai/upscale"
    assert json.loads(captured[0].content)["model"] == "nai-diffusion-5-curated"
