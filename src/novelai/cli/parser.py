"""Argument parser and validation logic for the CLI."""

from __future__ import annotations

import argparse
import sys

from .constants import (
    DEFAULT_MODEL,
    DEFAULT_SAMPLER,
    DEFAULT_UC_PRESET,
    HELP_EPILOG,
    MODEL_CHOICES,
    REF_TYPE_CHOICES,
    SAMPLER_CHOICES,
    UC_PRESET_CHOICES,
)
from .output import fail


def _validate_range(
    value: float, min_value: float, max_value: float, name: str
) -> float:
    if not (min_value <= value <= max_value):
        raise ValueError(f"{name} must be between {min_value} and {max_value}")
    return value


def parse_bool_value(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError("expected boolean (true/false)")


def parse_seed_value(value: str) -> int | None:
    normalized = value.strip().lower()
    if normalized in {"none", "null", "random"}:
        return None
    return int(value)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="NovelAI Image Generation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_EPILOG,
    )

    parser.add_argument(
        "prompt", nargs="?", type=str, help="Prompt for image generation"
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Run interactive prompt loop for repeated generations",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output",
        help="Output file or directory path (default: output)",
    )
    parser.add_argument(
        "--request-json",
        type=str,
        help="Path to request JSON. Supports high-level params JSON or low-level API request JSON.",
    )
    parser.add_argument(
        "--request-json-stdin",
        action="store_true",
        help="Read request JSON from stdin instead of prompt/options.",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        choices=MODEL_CHOICES,
        help=f"Model to use (default: {DEFAULT_MODEL})",
    )

    parser.add_argument(
        "--size",
        type=str,
        default="portrait",
        help='Image size (e.g., "portrait", "landscape", "square", or "832x1216") (default: portrait)',
    )

    parser.add_argument(
        "--steps", type=int, default=23, help="Number of steps (default: 23)"
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=5.0,
        help="Guidance scale, 0.0-10.0 (default: 5.0)",
    )
    parser.add_argument(
        "--sampler",
        type=str,
        default=DEFAULT_SAMPLER,
        choices=SAMPLER_CHOICES,
        help=f"Sampler to use (default: {DEFAULT_SAMPLER})",
    )
    parser.add_argument("--seed", type=int, help="Random seed (omit for random)")

    parser.add_argument(
        "--quality",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable quality tags (default: true, use --no-quality to disable)",
    )
    parser.add_argument(
        "--uc-preset",
        type=str,
        default=DEFAULT_UC_PRESET,
        choices=UC_PRESET_CHOICES,
        help=f"Undesired content preset (default: {DEFAULT_UC_PRESET})",
    )
    parser.add_argument("--negative-prompt", type=str, help="Negative prompt")

    parser.add_argument("--reference", type=str, help="Character reference image path")
    parser.add_argument(
        "--ref-type",
        type=str,
        default="character&style",
        choices=REF_TYPE_CHOICES,
        help="Reference type (default: character&style)",
    )
    parser.add_argument(
        "--ref-fidelity",
        type=float,
        default=1.0,
        help="Reference fidelity 0.0-1.0 (default: 1.0)",
    )
    parser.add_argument(
        "--ref-strength",
        type=float,
        default=1.0,
        help="Reference strength 0.0-1.0 (default: 1.0)",
    )

    parser.add_argument(
        "--character-prompt", type=str, help="Character prompt (region prompt)"
    )

    parser.add_argument("--controlnet", type=str, help="ControlNet image path")
    parser.add_argument(
        "--controlnet-strength",
        type=float,
        default=0.6,
        help="ControlNet strength 0.01-1.0 (default: 0.6)",
    )

    parser.add_argument("--image", type=str, help="Base image for img2img")
    parser.add_argument(
        "--strength",
        type=float,
        default=0.7,
        help="Img2Img strength 0.01-0.99 (default: 0.7)",
    )

    parser.add_argument(
        "--n-images",
        type=int,
        default=1,
        help="Number of images to generate (default: 1)",
    )
    parser.add_argument(
        "--noise",
        type=float,
        default=0.0,
        help="Img2Img noise amount 0.0-0.99 (default: 0.0)",
    )

    parser.add_argument(
        "--stream", action="store_true", help="Use streaming generation"
    )
    parser.add_argument(
        "--stream-dir",
        type=str,
        default="streaming_output",
        help="Directory for streaming chunks",
    )

    return parser


def parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Parse command line arguments."""
    args = parser.parse_args()

    if args.request_json and args.request_json_stdin:
        parser.error("use either --request-json or --request-json-stdin, not both")

    if args.interactive and (args.request_json or args.request_json_stdin):
        parser.error("request-json mode cannot be combined with --interactive")

    has_json_mode = bool(args.request_json or args.request_json_stdin)
    if not args.interactive and not args.prompt and not has_json_mode:
        parser.error(
            "prompt is required unless --interactive, --request-json, or --request-json-stdin is specified"
        )

    validate_args(args, parser)
    return args


def validate_args(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
    *,
    in_interactive: bool = False,
) -> None:
    """Validate CLI argument ranges and relationships."""
    try:
        if args.steps < 1:
            raise ValueError("steps must be >= 1")
        if args.steps > 50:
            raise ValueError("steps must be <= 50")
        if args.n_images < 1:
            raise ValueError("n-images must be >= 1")
        if args.n_images > 8:
            raise ValueError("n-images must be <= 8")
        _validate_range(args.scale, 0.0, 10.0, "scale")
        _validate_range(args.ref_fidelity, 0.0, 1.0, "ref-fidelity")
        _validate_range(args.ref_strength, 0.0, 1.0, "ref-strength")
        _validate_range(args.controlnet_strength, 0.01, 1.0, "controlnet-strength")
        _validate_range(args.strength, 0.01, 0.99, "strength")
        _validate_range(args.noise, 0.0, 0.99, "noise")
    except ValueError as exc:
        if in_interactive:
            raise
        parser.error(str(exc))


def parse_size(size_str: str) -> str | tuple[int, int]:
    """Parse size string to tuple or return preset name."""
    if "x" in size_str:
        try:
            width, height = map(int, size_str.split("x"))
            return (width, height)
        except ValueError:
            fail(f"Error: Invalid size format: {size_str}")
            sys.exit(1)
    return size_str
