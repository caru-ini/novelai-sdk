"""CLI constants and static help text."""

from __future__ import annotations

from typing import get_args

from novelai.constants.models import ImageModel, V4_5_FULL
from novelai.constants.negative_prompts import UC_LIGHT, UCPreset
from novelai.constants.samplers import K_EULER_ANCESTRAL, Sampler

MODEL_CHOICES = list(get_args(ImageModel))
SAMPLER_CHOICES = list(get_args(Sampler))
UC_PRESET_CHOICES = list(get_args(UCPreset))
REF_TYPE_CHOICES = ["character", "style", "character&style"]
DEFAULT_MODEL = V4_5_FULL
DEFAULT_SAMPLER = K_EULER_ANCESTRAL
DEFAULT_UC_PRESET = UC_LIGHT


INTERACTIVE_HELP = """Interactive commands:
  /help                 Show this help
  /show                 Show current settings
  /quit or /exit        Exit interactive mode
  /set <key> <value>    Update a setting (e.g. /set scale 6.0)
  /unset <key>          Reset optional setting to default/None
  /m <model>            Shortcut for model
  /res <size>           Shortcut for resolution/size
  /st <steps>           Shortcut for steps
  /cfg <scale>          Shortcut for scale
  /sp <sampler>         Shortcut for sampler

Examples:
  /set model nai-diffusion-4-5-full
  /m nai-diffusion-4-5-curated
  /set size 832x1216
  /res landscape
  /st 28
  /cfg 6.0
  /set n-images 4
  /set ref-strength 0.9
  /set stream true
  /unset seed

Any non-command line is treated as a prompt and generated immediately.
"""

HELP_EPILOG = """
Examples:
  # Basic generation
  python -m novelai "1girl, cat ears, maid" -o output.png

  # Custom settings
  python -m novelai "landscape, sunset" --model nai-diffusion-4-5-full --steps 28 --scale 6.0

  # Interactive mode
  python -m novelai --interactive --model nai-diffusion-4-5-full

  # With character reference
  python -m novelai "1girl, standing" --reference ref.png --ref-fidelity 0.8 --ref-strength 0.9

  # With ControlNet
  python -m novelai "1girl" --controlnet edge.png --controlnet-strength 0.8

  # Img2Img
  python -m novelai "improve quality" --image base.png --strength 0.5 --noise 0.1

  # Streaming generation
  python -m novelai "1girl" --stream --stream-dir streaming_output

  # Batch generation
  python -m novelai "1girl" --n-images 4

  # High-level params JSON mode
  python -m novelai --request-json examples/request_user.json -o output

  # Low-level API request JSON mode
  python -m novelai --request-json examples/request_api.json
"""
