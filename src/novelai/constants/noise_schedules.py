"""Noise schedule and streaming constants"""

from __future__ import annotations

from typing import Literal

NoiseSchedule = Literal["karras", "exponential", "polyexponential"]

NOISE_KARRAS: NoiseSchedule = "karras"
NOISE_EXPONENTIAL: NoiseSchedule = "exponential"
NOISE_POLYEXPONENTIAL: NoiseSchedule = "polyexponential"

StreamingType = Literal["msgpack", "sse"]
