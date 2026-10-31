"""Preset constants for quality tags and undesired content"""

from __future__ import annotations

from typing import Literal

from .models import (
    V3,
    V3_FURRY,
    V4_5_CURATED,
    V4_5_FULL,
    V4_CURATED,
    V4_FULL,
    V5_CURATED,
    V5_FULL,
    V5_FULL_MEDIUM,
    ImageModel,
)

UCPreset = Literal["strong", "light", "furry_focus", "human_focus", "none"]
UndesiredContentPreset = Literal[
    "strong",
    "light",
    "furry_focus",
    "human_focus",
    "not_specified",
]

UC_STRONG: UCPreset = "strong"
UC_LIGHT: UCPreset = "light"
UC_FURRY_FOCUS: UCPreset = "furry_focus"
UC_HUMAN_FOCUS: UCPreset = "human_focus"
UC_NONE: UCPreset = "none"

QUALITY_TAGS: dict[ImageModel, str] = {
    V5_FULL: "very aesthetic, masterpiece, no text",
    V5_FULL_MEDIUM: "very aesthetic, masterpiece, no text",
    V5_CURATED: "very aesthetic, masterpiece, no text",
    V4_5_FULL: "very aesthetic, masterpiece, no text",
    V4_5_CURATED: "very aesthetic, masterpiece, no text, -0.8::feet::, rating:general",
    V4_FULL: "no text, best quality, very aesthetic, absurdres",
    V4_CURATED: "rating:general, best quality, very aesthetic, absurdres",
    V3: "best quality, amazing quality, very aesthetic, absurdres",
    V3_FURRY: "{best quality}, {amazing quality}",
}

_V5_UC: dict[UCPreset, str] = {
    "strong": "lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page",
    "light": "lowres, bad hands, bad anatomy, artistic error, sepia, white haze, worst quality, very displeasing, jpeg artifacts, 0::ai-generated::",
    "furry_focus": "{worst quality}, distracting watermark, unfinished, bad quality, {widescreen}, upscale, {sequence}, {{grandfathered content}}, blurred foreground, chromatic aberration, sketch, everyone, [sketch background], simple, [flat colors], ych (character), outline, multiple scenes, [[horror (theme)]], comic",
    "human_focus": "lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page, @_@, mismatched pupils, glowing eyes, bad anatomy",
    "none": "",
}

UNDESIRED_CONTENT_PRESETS: dict[ImageModel, dict[UCPreset, str]] = {
    V5_FULL: _V5_UC,
    V5_FULL_MEDIUM: _V5_UC,
    V5_CURATED: _V5_UC,
    V4_5_FULL: {
        "strong": "lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page",
        "light": "lowres, artistic error, scan artifacts, worst quality, bad quality, jpeg artifacts, multiple views, very displeasing, too many watermarks, negative space, blank page",
        "furry_focus": "{worst quality}, distracting watermark, unfinished, bad quality, {widescreen}, upscale, {sequence}, {{grandfathered content}}, blurred foreground, chromatic aberration, sketch, everyone, [sketch background], simple, [flat colors], ych (character), outline, multiple scenes, [[horror (theme)]], comic",
        "human_focus": "lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page, @_@, mismatched pupils, glowing eyes, bad anatomy",
        "none": "",
    },
    V4_5_CURATED: {
        "strong": "blurry, lowres, upscaled, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, halftone, multiple views, logo, too many watermarks, negative space, blank page",
        "light": "blurry, lowres, upscaled, artistic error, scan artifacts, jpeg artifacts, logo, too many watermarks, negative space, blank page",
        "human_focus": "blurry, lowres, upscaled, artistic error, film grain, scan artifacts, bad anatomy, bad hands, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, halftone, multiple views, logo, too many watermarks, @_@, mismatched pupils, glowing eyes, negative space, blank page",
        "none": "",
    },
    V4_FULL: {
        "strong": "blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, multiple views, logo, too many watermarks, white blank page, blank page",
        "light": "blurry, lowres, error, worst quality, bad quality, jpeg artifacts, very displeasing, white blank page, blank page",
        "none": "",
    },
    V4_CURATED: {
        "strong": "blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, logo, dated, signature, multiple views, gigantic breasts, white blank page, blank page",
        "light": "blurry, lowres, error, worst quality, bad quality, jpeg artifacts, very displeasing, logo, dated, signature, white blank page, blank page",
        "none": "",
    },
    V3: {
        "strong": "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]",
        "light": "lowres, jpeg artifacts, worst quality, watermark, blurry, very displeasing",
        "human_focus": "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], bad anatomy, bad hands, @_@, mismatched pupils, heart-shaped pupils, glowing eyes",
        "none": "lowres",
    },
    V3_FURRY: {
        "strong": "{{worst quality}}, [displeasing], {unusual pupils}, guide lines, {{unfinished}}, {bad}, url, artist name, {{tall image}}, mosaic, {sketch page}, comic panel, impact (font), [dated], {logo}, ych, {what}, {where is your god now}, {distorted text}, repeated text, {floating head}, {1994}, {widescreen}, absolutely everyone, sequence, {compression artifacts}, hard translated, {cropped}, {commissioner name}, unknown text, high contrast",
        "light": "{worst quality}, guide lines, unfinished, bad, url, tall image, widescreen, compression artifacts, unknown text",
        "none": "lowres",
    },
}
