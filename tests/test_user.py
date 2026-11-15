from __future__ import annotations

import asyncio

import httpx
import pytest
from pydantic import ValidationError

from novelai import AsyncNovelAI, NovelAI
from novelai.types import OpusUsage, Subscription

_SAMPLE_RESPONSE: dict[str, object] = {
    "tier": 3,
    "active": True,
    "expiresAt": 1893456000,
    "perks": {
        "maxPriorityActions": 10000,
        "startPriority": 10,
        "contextTokens": 8192,
        "unlimitedMaxPriority": True,
        "moduleTrainingSteps": 10000,
        "voiceGeneration": True,
        "imageGeneration": True,
        "unlimitedImageGeneration": True,
        "unlimitedImageGenerationLimits": [
            {"resolution": 4194304, "maxPrompts": 0},
            {"resolution": 1048576, "maxPrompts": 1},
        ],
    },
    "paymentProcessorData": {"some": "data"},
    "trainingStepsLeft": {
        "fixedTrainingStepsLeft": 1000,
        "purchasedTrainingSteps": 3250,
    },
    "accountType": 0,
    "isGracePeriod": False,
}

# The `usage` object as the API returns it for an Opus account.
_SAMPLE_USAGE: dict[str, object] = {
    "percent": 29,
    "purchasedPercent": 0,
    "isNegative": False,
    "timeUntilNextPercent": 6048,
}

_SAMPLE_RESPONSE_WITH_USAGE: dict[str, object] = {
    **_SAMPLE_RESPONSE,
    "usage": _SAMPLE_USAGE,
}


def test_subscription_parses_camelcase_and_sums_anlas() -> None:
    sub = Subscription.model_validate(_SAMPLE_RESPONSE)

    assert sub.tier == 3
    assert sub.active is True
    assert sub.expires_at == 1893456000
    assert sub.perks.module_training_steps == 10000
    assert sub.perks.unlimited_image_generation is True
    assert sub.perks.unlimited_image_generation_limits[1].max_prompts == 1
    assert sub.training_steps_left.fixed_training_steps_left == 1000
    assert sub.training_steps_left.purchased_training_steps == 3250
    assert sub.anlas == 4250
    assert sub.is_opus is True
    assert sub.tier_name == "Opus"


def test_lower_tier_is_not_opus() -> None:
    sub = Subscription.model_validate({**_SAMPLE_RESPONSE, "tier": 1})

    assert sub.is_opus is False
    assert sub.tier_name == "Tablet"


def test_unknown_higher_tier_is_not_opus() -> None:
    sub = Subscription.model_validate({**_SAMPLE_RESPONSE, "tier": 4})

    assert sub.is_opus is False
    assert sub.tier_name == "Unknown (4)"


def test_missing_training_steps_left_raises() -> None:
    payload = {k: v for k, v in _SAMPLE_RESPONSE.items() if k != "trainingStepsLeft"}

    with pytest.raises(ValidationError):
        Subscription.model_validate(payload)


def test_subscription_without_usage_reports_none() -> None:
    assert Subscription.model_validate(_SAMPLE_RESPONSE).usage is None


def test_usage_parses_api_fields() -> None:
    usage = Subscription.model_validate(_SAMPLE_RESPONSE_WITH_USAGE).usage

    assert usage is not None
    assert usage.percent == 29
    assert usage.purchased_percent == 0
    assert usage.is_negative is False
    assert usage.time_until_next_percent == 6048


def test_usage_tolerates_missing_and_unknown_fields() -> None:
    usage = OpusUsage.model_validate({"percent": 100, "somethingNew": 1})

    assert usage.percent == 100
    assert usage.purchased_percent == 0
    assert usage.is_negative is False
    assert usage.time_until_next_percent == 0


def _mock_handler(
    captured: list[httpx.Request],
    payload: dict[str, object] = _SAMPLE_RESPONSE,
) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json=payload)

    return httpx.MockTransport(handler)


def test_get_subscription_and_get_anlas_hit_user_subscription() -> None:
    captured: list[httpx.Request] = []
    client = NovelAI(api_key="dummy")
    api = client.api_client
    headers = api.client.headers
    api.client.close()
    api.client = httpx.Client(transport=_mock_handler(captured), headers=headers)

    try:
        sub = client.user.get_subscription()
        assert sub.anlas == 4250
        assert client.user.get_anlas() == 4250
    finally:
        client.close()

    assert all(
        r.url == "https://image.novelai.net/user/subscription" and r.method == "GET"
        for r in captured
    )
    assert captured[0].headers["Authorization"] == "Bearer dummy"


def test_async_get_anlas() -> None:
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
            return await client.user.get_anlas()
        finally:
            await client.close()

    assert asyncio.run(run()) == 4250
    assert captured[0].url == "https://image.novelai.net/user/subscription"
    assert captured[0].headers["Authorization"] == "Bearer dummy"


def _get_opus_usage(
    captured: list[httpx.Request], payload: dict[str, object]
) -> OpusUsage | None:
    client = NovelAI(api_key="dummy")
    api = client.api_client
    headers = api.client.headers
    api.client.close()
    api.client = httpx.Client(
        transport=_mock_handler(captured, payload), headers=headers
    )
    try:
        return client.user.get_opus_usage()
    finally:
        client.close()


def test_get_opus_usage_reads_usage_from_user_subscription() -> None:
    captured: list[httpx.Request] = []

    usage = _get_opus_usage(captured, _SAMPLE_RESPONSE_WITH_USAGE)

    assert usage is not None
    assert usage.percent == 29
    assert len(captured) == 1
    assert captured[0].url == "https://image.novelai.net/user/subscription"
    assert captured[0].method == "GET"


def test_get_opus_usage_is_none_when_the_api_reports_no_usage() -> None:
    assert _get_opus_usage([], _SAMPLE_RESPONSE) is None


def test_async_get_opus_usage() -> None:
    captured: list[httpx.Request] = []

    async def run() -> OpusUsage | None:
        client = AsyncNovelAI(api_key="dummy")
        api = client.api_client
        headers = api.client.headers
        await api.client.aclose()
        api.client = httpx.AsyncClient(
            transport=_mock_handler(captured, _SAMPLE_RESPONSE_WITH_USAGE),
            headers=headers,
        )
        try:
            return await client.user.get_opus_usage()
        finally:
            await client.close()

    usage = asyncio.run(run())

    assert usage is not None
    assert usage.percent == 29
    assert captured[0].url == "https://image.novelai.net/user/subscription"
