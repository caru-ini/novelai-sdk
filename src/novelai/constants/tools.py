"""Director Tools constants"""

from __future__ import annotations

from typing import Literal

DirectorTool = Literal[
    "bg-removal",
    "lineart",
    "sketch",
    "colorize",
    "emotion",
    "declutter",
    "declutter-keep-bubbles",
]

Emotion = Literal[
    "neutral",
    "happy",
    "sad",
    "angry",
    "scared",
    "surprised",
    "tired",
    "excited",
    "nervous",
    "thinking",
    "confused",
    "shy",
    "disgusted",
    "smug",
    "bored",
    "laughing",
    "irritated",
    "aroused",
    "embarrassed",
    "worried",
    "love",
    "determined",
    "hurt",
    "playful",
]
