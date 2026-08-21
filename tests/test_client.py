from __future__ import annotations

import asyncio
import warnings

import pytest

from novelai import AsyncNovelAI, NovelAI


def test_api_base_argument_warns_deprecation() -> None:
    with pytest.warns(DeprecationWarning, match="api_base"):
        client = NovelAI(api_key="dummy", api_base="https://api.novelai.net")
    client.close()


def test_api_base_env_var_warns_deprecation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOVELAI_API_BASE", "https://api.novelai.net")

    with pytest.warns(DeprecationWarning, match="NOVELAI_API_BASE"):
        client = NovelAI(api_key="dummy")
    client.close()


def test_async_api_base_argument_warns_deprecation() -> None:
    with pytest.warns(DeprecationWarning, match="api_base"):
        client = AsyncNovelAI(api_key="dummy", api_base="https://api.novelai.net")
    asyncio.run(client.close())


def test_no_deprecation_warning_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NOVELAI_API_BASE", raising=False)

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        client = NovelAI(api_key="dummy")
    client.close()
