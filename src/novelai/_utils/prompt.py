"""Quality tag and undesired content assembly matching the web UI"""

from __future__ import annotations

import re

from ..constants.models import (
    V3,
    V3_FURRY,
    V4_5_CURATED,
    V4_CURATED,
    V5_CURATED,
    ImageModel,
)
from ..constants.negative_prompts import (
    QUALITY_TAGS,
    UNDESIRED_CONTENT_PRESETS,
    UCPreset,
)

_LEGACY_PROMPT_MODELS = frozenset({V3, V3_FURRY})
_SFW_MODELS = frozenset({V4_CURATED, V4_5_CURATED, V5_CURATED})
_TEXT_MARKER = re.compile(r"(?:^|\s|[,.:\[\]{}、。])text:(?!:)", re.IGNORECASE)
_TRAILING_WEIGHT = re.compile(r":[\d.]+$")


def _join_tags(*parts: str) -> str:
    return ", ".join(part for part in parts if part)


def _split_base_prompt(prompt: str) -> tuple[str, str]:
    offset = 0
    for index, part in enumerate(prompt.split("||")):
        if index % 2 == 0 and "|" in part:
            cut = offset + part.index("|")
            return prompt[:cut], prompt[cut:]
        offset += len(part) + 2
    return prompt, ""


def add_quality_tags(
    prompt: str,
    model: ImageModel,
    *,
    quality: bool,
    transparent_background: bool = False,
) -> str:
    """Append the model's quality tags to the prompt"""
    tags = QUALITY_TAGS[model] if quality else ""
    if transparent_background:
        tags = _join_tags("transparent background", tags)
    if not tags:
        return prompt

    if model in _LEGACY_PROMPT_MODELS:
        segments: list[str] = []
        for segment in prompt.split("|"):
            match = _TRAILING_WEIGHT.search(segment)
            weight = match.group(0) if match else ""
            segments.append(
                _join_tags(segment[: len(segment) - len(weight)], tags) + weight
            )
        return "|".join(segments)

    base, rest = _split_base_prompt(prompt)
    marker = _TEXT_MARKER.search(base)
    if marker:
        base = _join_tags(base[: marker.start()], tags) + base[marker.start() :]
    else:
        base = _join_tags(base, tags)
    return base + rest


def solve_undesired_content(
    model: ImageModel,
    uc_preset: UCPreset,
    prompt: str,
    negative_prompt: str,
) -> str:
    """Build the negative prompt from the model's UC preset and the user's input"""
    preset = UNDESIRED_CONTENT_PRESETS[model].get(uc_preset, "")
    add_nsfw = (
        model not in _SFW_MODELS
        and uc_preset != "none"
        and preset != ""
        and "nsfw" not in prompt.lower()
    )

    if model not in _LEGACY_PROMPT_MODELS:
        segments = negative_prompt.split("|")
        segments[0] = _join_tags(preset, segments[0])
        undesired = "|".join(segments)
        return f"nsfw, {undesired}" if add_nsfw else undesired

    if negative_prompt:
        undesired = _join_tags("" if uc_preset == "none" else preset, negative_prompt)
    else:
        undesired = preset
    return _join_tags("nsfw", undesired) if add_nsfw else undesired
