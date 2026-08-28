from __future__ import annotations

import asyncio

import httpx

from novelai import AsyncNovelAI, NovelAI
from novelai.types import SuggestTagsParams

_TAGS_RESPONSE = {
    "tags": [
        {"tag": "blue archive", "count": 10000, "confidence": 0.0},
        {"tag": "baby blue", "count": 6221, "confidence": 0.80859375},
    ]
}

_JP_TAGS_RESPONSE = [
    {"jp_tag": "青", "en_tag": "blue theme", "power": 10000},
    {"jp_tag": "青肌", "en_tag": "blue skin", "power": 10000},
]


def _mock_handler(captured: list[httpx.Request]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        body = (
            _JP_TAGS_RESPONSE
            if request.url.params.get("lang") == "jp"
            else _TAGS_RESPONSE
        )
        return httpx.Response(200, json=body)

    return httpx.MockTransport(handler)


def _patched_client(captured: list[httpx.Request]) -> NovelAI:
    client = NovelAI(api_key="dummy")
    api = client.api_client
    headers = api.client.headers
    api.client.close()
    api.client = httpx.Client(transport=_mock_handler(captured), headers=headers)
    return client


def test_suggest_tags_gets_with_query_params() -> None:
    captured: list[httpx.Request] = []
    client = _patched_client(captured)

    try:
        tags = client.image.suggest_tags(SuggestTagsParams(prompt="blue"))
    finally:
        client.close()

    request = captured[0]
    assert request.method == "GET"
    assert request.url.path == "/ai/generate-image/suggest-tags"
    assert request.url.host == "image.novelai.net"
    assert request.url.params["model"] == "nai-diffusion-4-5-full"
    assert request.url.params["prompt"] == "blue"
    assert "lang" not in request.url.params
    assert request.headers["Authorization"] == "Bearer dummy"

    assert tags[0].tag == "blue archive"
    assert tags[1].confidence == 0.80859375


def test_suggest_tags_model_override() -> None:
    captured: list[httpx.Request] = []
    client = _patched_client(captured)

    try:
        client.image.suggest_tags(
            SuggestTagsParams(prompt="blue", model="nai-diffusion-3")
        )
    finally:
        client.close()

    assert captured[0].url.params["model"] == "nai-diffusion-3"


def test_suggest_tags_jp_parses_bare_array() -> None:
    captured: list[httpx.Request] = []
    client = _patched_client(captured)

    try:
        tags = client.image.suggest_tags_jp(SuggestTagsParams(prompt="青"))
    finally:
        client.close()

    assert captured[0].url.params["lang"] == "jp"
    assert tags[0].en_tag == "blue theme"
    assert tags[1].jp_tag == "青肌"


def test_async_suggest_tags_and_jp() -> None:
    captured: list[httpx.Request] = []

    async def run() -> None:
        client = AsyncNovelAI(api_key="dummy")
        api = client.api_client
        headers = api.client.headers
        await api.client.aclose()
        api.client = httpx.AsyncClient(
            transport=_mock_handler(captured), headers=headers
        )
        try:
            tags = await client.image.suggest_tags(SuggestTagsParams(prompt="blue"))
            assert tags[0].tag == "blue archive"
            jp_tags = await client.image.suggest_tags_jp(SuggestTagsParams(prompt="青"))
            assert jp_tags[0].en_tag == "blue theme"
        finally:
            await client.close()

    asyncio.run(run())
    assert captured[0].url.path == "/ai/generate-image/suggest-tags"
    assert captured[1].url.params["lang"] == "jp"
