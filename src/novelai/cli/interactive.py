"""Interactive mode implementation."""

from __future__ import annotations

import argparse
import copy
import shlex
from typing import Any, Callable

from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from novelai import NovelAI

from .constants import (
    INTERACTIVE_HELP,
    MODEL_CHOICES,
    REF_TYPE_CHOICES,
    SAMPLER_CHOICES,
    UC_PRESET_CHOICES,
)
from .generation import generate_standard, generate_streaming
from .output import console, info, success, warn
from .parser import parse_bool_value, parse_seed_value, validate_args

KEY_ALIASES = {
    "m": "model",
    "model": "model",
    "res": "size",
    "resolution": "size",
    "size": "size",
    "st": "steps",
    "steps": "steps",
    "cfg": "scale",
    "scale": "scale",
    "sp": "sampler",
    "sampler": "sampler",
}

MODEL_LABELS = {
    "nai-diffusion-4-5-full": "v4.5-full",
    "nai-diffusion-4-5-curated": "v4.5-curated",
    "nai-diffusion-4-full": "v4-full",
    "nai-diffusion-4-curated": "v4-curated",
    "nai-diffusion-3": "v3",
    "nai-diffusion-3-furry": "v3-furry",
}


def _interactive_setters() -> dict[str, tuple[str, Callable[[str], Any]]]:
    return {
        "model": ("model", str),
        "size": ("size", str),
        "steps": ("steps", int),
        "scale": ("scale", float),
        "sampler": ("sampler", str),
        "seed": ("seed", parse_seed_value),
        "quality": ("quality", parse_bool_value),
        "uc-preset": ("uc_preset", str),
        "negative-prompt": ("negative_prompt", str),
        "reference": ("reference", str),
        "ref-type": ("ref_type", str),
        "ref-fidelity": ("ref_fidelity", float),
        "ref-strength": ("ref_strength", float),
        "character-prompt": ("character_prompt", str),
        "controlnet": ("controlnet", str),
        "controlnet-strength": ("controlnet_strength", float),
        "image": ("image", str),
        "strength": ("strength", float),
        "n-images": ("n_images", int),
        "noise": ("noise", float),
        "output": ("output", str),
        "stream": ("stream", parse_bool_value),
        "stream-dir": ("stream_dir", str),
    }


def _normalize_set_key(key: str) -> str:
    key = key.strip().lower()
    return KEY_ALIASES.get(key, key)


def _build_prompt_label(args: argparse.Namespace) -> str:
    model = MODEL_LABELS.get(args.model, args.model)
    stream = " stream" if args.stream else ""
    return (
        "[bold cyan]novelai[/bold cyan] "
        f"[dim]({model} | {args.size} | st={args.steps} | cfg={args.scale}{stream})[/dim]"
    )


def _show_current_short(key: str, args: argparse.Namespace) -> None:
    value = getattr(args, key.replace("-", "_"), None)
    info(f"{key}={value}")
    if key == "model":
        info(f"choices: {', '.join(MODEL_CHOICES)}")
    if key == "sampler":
        info(f"choices: {', '.join(SAMPLER_CHOICES)}")


def _normalize_unset_value(key: str, defaults: argparse.Namespace) -> Any:
    optional_null_keys = {
        "seed",
        "negative_prompt",
        "reference",
        "character_prompt",
        "controlnet",
        "image",
    }
    if key in optional_null_keys:
        return None
    return getattr(defaults, key)


def _print_interactive_status(args: argparse.Namespace) -> None:
    table = Table(title="Current settings")
    table.add_column("Key", style="cyan")
    table.add_column("Value")
    table.add_row("model", str(args.model))
    table.add_row("size", str(args.size))
    table.add_row(
        "params", f"steps={args.steps}, scale={args.scale}, sampler={args.sampler}"
    )
    table.add_row(
        "flags", f"seed={args.seed}, quality={args.quality}, uc-preset={args.uc_preset}"
    )
    table.add_row("output", f"n-images={args.n_images}, output={args.output}")
    table.add_row("stream", f"stream={args.stream}, stream-dir={args.stream_dir}")
    if args.negative_prompt:
        table.add_row("negative-prompt", str(args.negative_prompt))
    if args.reference:
        table.add_row(
            "reference",
            f"{args.reference} (type={args.ref_type}, fidelity={args.ref_fidelity}, strength={args.ref_strength})",
        )
    if args.character_prompt:
        table.add_row("character-prompt", str(args.character_prompt))
    if args.controlnet:
        table.add_row(
            "controlnet", f"{args.controlnet} (strength={args.controlnet_strength})"
        )
    if args.image:
        table.add_row(
            "image", f"{args.image} (strength={args.strength}, noise={args.noise})"
        )
    console.print(table)


def _apply_interactive_set(
    args: argparse.Namespace,
    defaults: argparse.Namespace,
    key: str,
    value: str,
    parser: argparse.ArgumentParser,
) -> None:
    setters = _interactive_setters()
    if key not in setters:
        known = ", ".join(sorted(setters.keys()))
        warn(f"Unknown key: {key}")
        info(f"Available keys: {known}")
        return

    attr, cast_fn = setters[key]
    old_value = getattr(args, attr)
    try:
        new_value = cast_fn(value)
    except Exception as exc:
        warn(f"Invalid value for {key}: {exc}")
        return

    setattr(args, attr, new_value)
    try:
        validate_args(args, parser, in_interactive=True)
    except ValueError:
        setattr(args, attr, old_value)
        warn(f"Rejected value for {key}: {value}")
        return

    if key == "model" and args.model not in MODEL_CHOICES:
        setattr(args, attr, old_value)
        warn(f"Invalid model. Choices: {', '.join(MODEL_CHOICES)}")
        return
    if key == "sampler" and args.sampler not in SAMPLER_CHOICES:
        setattr(args, attr, old_value)
        warn(f"Invalid sampler. Choices: {', '.join(SAMPLER_CHOICES)}")
        return
    if key == "uc-preset" and args.uc_preset not in UC_PRESET_CHOICES:
        setattr(args, attr, old_value)
        warn(f"Invalid uc-preset. Choices: {', '.join(UC_PRESET_CHOICES)}")
        return
    if key == "ref-type" and args.ref_type not in REF_TYPE_CHOICES:
        setattr(args, attr, old_value)
        warn(f"Invalid ref-type. Choices: {', '.join(REF_TYPE_CHOICES)}")
        return

    success(f"Updated {key}={new_value}")

    if key == "reference" and new_value is None:
        args.ref_type = defaults.ref_type
        args.ref_fidelity = defaults.ref_fidelity
        args.ref_strength = defaults.ref_strength
    if key == "controlnet" and new_value is None:
        args.controlnet_strength = defaults.controlnet_strength
    if key == "image" and new_value is None:
        args.strength = defaults.strength
        args.noise = defaults.noise


def interactive_loop(
    client: NovelAI,
    base_args: argparse.Namespace,
    parser: argparse.ArgumentParser,
) -> None:
    """Run interactive prompt loop."""
    args = copy.deepcopy(base_args)
    defaults = parser.parse_args([])

    console.print(
        Panel(
            "Interactive mode started. Enter a prompt to generate images.\n"
            "Type [bold]/help[/bold] for commands, [bold]/quit[/bold] to exit.",
            title="NovelAI CLI",
            border_style="cyan",
        )
    )

    while True:
        try:
            line = Prompt.ask(_build_prompt_label(args)).strip()
        except KeyboardInterrupt:
            warn("Use /quit to exit interactive mode.")
            continue
        except EOFError:
            info("")
            break

        if not line:
            continue

        if line.startswith("/"):
            try:
                tokens = shlex.split(line)
            except ValueError as exc:
                warn(f"Parse error: {exc}")
                continue

            command = tokens[0].lower()
            command_key = _normalize_set_key(command.lstrip("/"))

            if command in {"/quit", "/exit"}:
                break

            if command == "/help":
                console.print(
                    Panel(INTERACTIVE_HELP.strip(), title="Help", border_style="cyan")
                )
                continue

            if command == "/show":
                _print_interactive_status(args)
                continue

            if command == "/set":
                if len(tokens) < 3:
                    warn("Usage: /set <key> <value>")
                    continue
                key = _normalize_set_key(tokens[1])
                value = " ".join(tokens[2:])
                _apply_interactive_set(args, defaults, key, value, parser)
                continue

            if command_key in {"model", "size", "steps", "scale", "sampler"}:
                if len(tokens) == 1:
                    _show_current_short(command_key, args)
                    continue
                value = " ".join(tokens[1:])
                _apply_interactive_set(args, defaults, command_key, value, parser)
                continue

            if command == "/unset":
                if len(tokens) != 2:
                    warn("Usage: /unset <key>")
                    continue
                key = _normalize_set_key(tokens[1]).replace("-", "_")
                if not hasattr(args, key):
                    warn(f"Unknown key: {tokens[1]}")
                    continue
                setattr(args, key, _normalize_unset_value(key, defaults))
                success(f"Reset {tokens[1]}")
                continue

            warn(f"Unknown command: {tokens[0]} (use /help)")
            continue

        args.prompt = line
        if args.stream:
            generate_streaming(client, args)
        else:
            generate_standard(client, args)
