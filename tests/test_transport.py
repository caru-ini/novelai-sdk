from __future__ import annotations

import asyncio
import base64
import io
import json
import zipfile
from typing import Callable

import httpx
import pytest
from _multipart import request_json, request_parts
from PIL import Image

from novelai import AsyncNovelAI, NovelAI, ServerError
from novelai.types import (
    ControlNet,
    ControlNetImage,
    GenerateImageParams,
    GenerateImageStreamParams,
    I2iParams,
)

Handler = Callable[[httpx.Request], httpx.Response]


def _png_bytes() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (64, 64), (200, 30, 30)).save(buffer, format="PNG")
    return buffer.getvalue()


def _ok(request: httpx.Request) -> httpx.Response:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("image_0.png", _png_bytes())
    return httpx.Response(200, content=buffer.getvalue())


def _recording(captured: list[httpx.Request], *responses: Handler) -> Handler:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        respond = (
            responses[len(captured) - 1] if len(captured) <= len(responses) else _ok
        )
        return respond(request)

    return handler


def _client(handler: Handler) -> NovelAI:
    client = NovelAI(api_key="dummy")
    api = client.api_client
    headers = api.client.headers
    api.client.close()
    api.client = httpx.Client(transport=httpx.MockTransport(handler), headers=headers)
    return client


def _i2i_params() -> GenerateImageParams:
    return GenerateImageParams(
        prompt="1girl", size=(64, 64), i2i=I2iParams(image=_png_bytes())
    )


def test_generation_is_sent_as_multipart_with_image_parts() -> None:
    captured: list[httpx.Request] = []
    client = _client(_recording(captured))

    try:
        images = client.image.generate(_i2i_params())
    finally:
        client.close()

    assert len(images) == 1
    assert captured[0].url == "https://image.novelai.net/ai/generate-image"
    assert captured[0].headers["Content-Type"].startswith("multipart/form-data")
    parameters = request_json(captured[0])["parameters"]
    assert parameters["image"] == "image"
    assert len(parameters["image_cache_secret_key"]) == 64
    Image.open(io.BytesIO(request_parts(captured[0])["image"]))


def test_known_image_is_sent_by_cache_key_only() -> None:
    captured: list[httpx.Request] = []
    client = _client(_recording(captured))
    params = _i2i_params()

    try:
        client.image.generate(params)
        client.image.generate(params)
    finally:
        client.close()

    first = request_json(captured[0])["parameters"]
    second = request_json(captured[1])["parameters"]
    assert "image" not in second
    assert second["image_cache_secret_key"] == first["image_cache_secret_key"]
    assert set(request_parts(captured[1])) == {"request"}


def test_expired_cache_keys_are_resent_with_their_images() -> None:
    captured: list[httpx.Request] = []

    def expired(request: httpx.Request) -> httpx.Response:
        key = request_json(request)["parameters"]["image_cache_secret_key"]
        body = {"message": "INVALID_CACHE_KEYS", "details": {"invalidKeys": [key]}}
        return httpx.Response(400, json=body)

    client = _client(_recording(captured, _ok, expired))
    params = _i2i_params()

    try:
        client.image.generate(params)
        images = client.image.generate(params)
    finally:
        client.close()

    assert len(images) == 1
    assert len(captured) == 3
    assert "image" not in request_json(captured[1])["parameters"]
    assert request_json(captured[2])["parameters"]["image"] == "image"


def test_failed_request_does_not_mark_images_as_cached() -> None:
    captured: list[httpx.Request] = []
    client = _client(_recording(captured, lambda _: httpx.Response(500)))
    params = _i2i_params()

    try:
        with pytest.raises(ServerError):
            client.image.generate(params)
        client.image.generate(params)
    finally:
        client.close()

    assert request_json(captured[1])["parameters"]["image"] == "image"


def test_vibes_are_sent_as_cached_reference_parts() -> None:
    captured: list[httpx.Request] = []
    client = _client(_recording(captured))
    vibe = base64.b64encode(b"encoded vibe").decode()
    images = [ControlNetImage(image=b"unused"), ControlNetImage(image=b"unused")]
    for image in images:
        image._vibe_data = vibe

    try:
        client.image.generate(
            GenerateImageParams(prompt="1girl", controlnet=ControlNet(images=images))
        )
    finally:
        client.close()

    parameters = request_json(captured[0])["parameters"]
    cached = parameters["reference_image_multiple_cached"]
    assert "reference_image_multiple" not in parameters
    key = cached[0]["cache_secret_key"]
    assert cached == [
        {"cache_secret_key": key, "data": "ref_multiple_0"},
        {"cache_secret_key": key},
    ]
    parts = request_parts(captured[0])
    assert set(parts) == {"ref_multiple_0", "request"}
    assert parts["ref_multiple_0"] == b"encoded vibe"


def test_stream_is_sent_as_multipart() -> None:
    captured: list[httpx.Request] = []
    event = {"event_type": "final", "samp_ix": 0, "gen_id": 1, "image": "aW1n"}

    def stream(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=f"data: {json.dumps(event)}\n\n".encode())

    client = _client(_recording(captured, stream))

    try:
        chunks = list(
            client.image.generate_stream(GenerateImageStreamParams(prompt="1girl"))
        )
    finally:
        client.close()

    assert [chunk.event_type for chunk in chunks] == ["final"]
    assert captured[0].url == "https://image.novelai.net/ai/generate-image-stream"
    assert request_json(captured[0])["parameters"]["stream"] == "sse"


def test_async_generation_reuses_cached_images() -> None:
    captured: list[httpx.Request] = []

    async def run() -> None:
        client = AsyncNovelAI(api_key="dummy")
        api = client.api_client
        headers = api.client.headers
        await api.client.aclose()
        api.client = httpx.AsyncClient(
            transport=httpx.MockTransport(_recording(captured)), headers=headers
        )
        params = _i2i_params()
        try:
            await client.image.generate(params)
            await client.image.generate(params)
        finally:
            await client.close()

    asyncio.run(run())

    assert request_json(captured[0])["parameters"]["image"] == "image"
    assert "image" not in request_json(captured[1])["parameters"]
