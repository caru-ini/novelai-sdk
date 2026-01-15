"""Preset constants for quality tags and undesired content"""

from __future__ import annotations

from typing import Literal

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

QUALITY_TAGS = ", very aesthetic, masterpiece, no text"

UNDESIRED_CONTENT_PRESETS = {
    "strong": ", lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page, ",
    "light": ", lowres, artistic error, scan artifacts, worst quality, bad quality, jpeg artifacts, multiple views, very displeasing, too many watermarks, negative space, blank page, ",
    "furry_focus": ", {worst quality}, distracting watermark, unfinished, bad quality, {widescreen}, upscale, {sequence}, {{grandfathered content}}, blurred foreground, chromatic aberration, sketch, everyone, [sketch background], simple, [flat colors], ych (character), outline, multiple scenes, [[horror (theme)]], comic, ",
    "human_focus": ", lowres, artistic error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, dithering, halftone, screentone, multiple views, logo, too many watermarks, negative space, blank page, @_@, mismatched pupils, glowing eyes, bad anatomy, ",
    "none": "",
}
