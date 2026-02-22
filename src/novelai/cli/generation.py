"""Image generation implementations for the CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Optional

from PIL import Image as PILImage
from pydantic import TypeAdapter, ValidationError
from rich.table import Table

from novelai import NovelAI
from novelai.types import (
    Character,
    CharacterReference,
    ControlNet,
    ControlNetImage,
    GenerateImageParams,
    GenerateImageStreamParams,
    I2iParams,
)
from novelai.types.api.image import (
    ImageGenerationRequest,
    ImageParameters,
    ImageStreamChunk,
    ImageStreamParameters,
    StreamImageGenerationRequest,
)

from .output import console, fail, info, success, warn
from .parser import parse_size


def _save_images(images: list[PILImage.Image], output: str) -> None:
    output_path = Path(output)

    if len(images) == 1:
        if output_path.suffix == "":
            output_path = output_path / "image.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        images[0].save(output_path)
        success(f"Saved: {output_path}")
        return

    if output_path.suffix != "":
        output_path = output_path.parent
    output_path.mkdir(parents=True, exist_ok=True)
    for i, img in enumerate(images):
        img_path = output_path / f"image_{i + 1:04d}.png"
        img.save(img_path)
        success(f"Saved: {img_path}")


def _save_stream_chunks(chunks: Iterable[ImageStreamChunk], stream_dir: str) -> None:
    output_dir = Path(stream_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    total_bytes = 0
    chunk_count = 0

    from base64 import b64decode

    for chunk in chunks:
        decoded_image = b64decode(chunk.image.encode("utf-8"))
        total_bytes += len(decoded_image)
        chunk_count += 1
        chunk_path = output_dir / f"chunk_{chunk_count:04d}.png"
        chunk_path.write_bytes(decoded_image)
        info(
            f"Received chunk {chunk_count}: {len(decoded_image)} bytes (total: {total_bytes} bytes)"
        )

    if chunk_count == 0:
        raise RuntimeError(
            "No stream chunks were received. If your request JSON uses stream=msgpack, "
            "this CLI currently supports SSE streaming only."
        )

    success(f"Streaming complete! Received {total_bytes} bytes total")
    success(f"Saved {chunk_count} chunks to: {output_dir}")


def _load_request_json(args: argparse.Namespace) -> dict[str, object]:
    try:
        if args.request_json_stdin:
            raw = sys.stdin.read()
        else:
            request_path = Path(args.request_json)
            if not request_path.exists():
                fail(f"Error: Request JSON not found: {request_path}")
                sys.exit(1)
            raw = request_path.read_text(encoding="utf-8")
        payload: object = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"Error: Invalid JSON: {exc}")
        sys.exit(1)

    adapter: TypeAdapter[dict[str, object]] = TypeAdapter(dict[str, object])
    try:
        return adapter.validate_python(payload)
    except ValidationError as exc:
        fail(f"Error: Request JSON must be an object with string keys:\n{exc}")
        sys.exit(1)


def _as_object_dict(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    adapter: TypeAdapter[dict[str, object]] = TypeAdapter(dict[str, object])
    try:
        return adapter.validate_python(value)
    except ValidationError:
        return None


def _sanitize_low_level_payload(payload: dict[str, object]) -> dict[str, object]:
    """Drop unknown keys from low-level API request payload."""
    allowed_top = set(ImageGenerationRequest.model_fields) | set(
        StreamImageGenerationRequest.model_fields
    )
    cleaned: dict[str, object] = {k: v for k, v in payload.items() if k in allowed_top}

    parameters_obj = _as_object_dict(cleaned.get("parameters"))
    if parameters_obj is not None:
        allowed_params = set(ImageParameters.model_fields) | set(
            ImageStreamParameters.model_fields
        )
        cleaned["parameters"] = {
            k: v for k, v in parameters_obj.items() if k in allowed_params
        }
    return cleaned


def _normalize_low_level_stream_mode(
    payload: dict[str, object], *, force_stream: bool
) -> dict[str, object]:
    """Ensure low-level stream request is compatible with this CLI's SSE parser."""
    parameters_obj = _as_object_dict(payload.get("parameters"))
    if parameters_obj is None:
        return payload

    normalized = dict(payload)
    params: dict[str, object] = dict(parameters_obj)
    stream_value = params.get("stream")

    if force_stream:
        if stream_value != "sse":
            if stream_value is not None:
                warn(
                    f"Low-level request stream={stream_value!r} is not supported by this CLI parser. "
                    "Overriding to 'sse'."
                )
            params["stream"] = "sse"
            normalized["parameters"] = params

    return normalized


def generate_from_request_json(client: NovelAI, args: argparse.Namespace) -> None:
    """Generate images from JSON request payload."""
    payload = _load_request_json(args)

    parameters = payload.get("parameters")
    is_low_level = isinstance(parameters, dict) and (
        "input" in payload or "action" in payload
    )

    try:
        if is_low_level:
            payload = _sanitize_low_level_payload(payload)
            parameters = _as_object_dict(payload.get("parameters"))
            stream_in_payload = parameters is not None and "stream" in parameters
            is_stream = args.stream or stream_in_payload
            payload = _normalize_low_level_stream_mode(payload, force_stream=is_stream)
            if is_stream:
                info(
                    "[bold cyan]Starting streaming generation from low-level request JSON...[/bold cyan]"
                )
                request = StreamImageGenerationRequest.model_validate(payload)
                chunks = client.api_client.image.generate_stream(request)
                _save_stream_chunks(chunks, args.stream_dir)
            else:
                info("[bold cyan]Generating from low-level request JSON...[/bold cyan]")
                request = ImageGenerationRequest.model_validate(payload)
                images = client.api_client.image.generate(request)
                _save_images(images, args.output)
                success(f"Successfully generated {len(images)} image(s)!")
            return

        if args.stream:
            info(
                "[bold cyan]Starting streaming generation from high-level params JSON...[/bold cyan]"
            )
            params = GenerateImageStreamParams.model_validate(payload)
            chunks = client.image.generate_stream(params)
            _save_stream_chunks(chunks, args.stream_dir)
            return

        info("[bold cyan]Generating from high-level params JSON...[/bold cyan]")
        params = GenerateImageParams.model_validate(payload)
        images = client.image.generate(params)
        _save_images(images, args.output)
        success(f"Successfully generated {len(images)} image(s)!")
    except ValidationError as exc:
        fail(f"Error: Request JSON validation failed:\n{exc}")
        sys.exit(1)
    except Exception as e:
        fail(f"Error during request-json generation: {e}")
        sys.exit(1)


def load_reference_image(
    args: argparse.Namespace,
) -> Optional[list[CharacterReference]]:
    """Load character reference image if specified."""
    if not args.reference:
        return None

    ref_path = Path(args.reference)
    if not ref_path.exists():
        fail(f"Error: Reference image not found: {ref_path}")
        sys.exit(1)

    return [
        CharacterReference(
            image=ref_path,
            type=args.ref_type,
            fidelity=args.ref_fidelity,
            strength=args.ref_strength,
        )
    ]


def load_character_prompt(args: argparse.Namespace) -> Optional[list[Character]]:
    """Load character prompt if specified."""
    if not args.character_prompt:
        return None

    return [Character(prompt=args.character_prompt, enabled=True)]


def load_controlnet(args: argparse.Namespace) -> Optional[ControlNet]:
    """Load ControlNet if specified."""
    if not args.controlnet:
        return None

    controlnet_path = Path(args.controlnet)
    if not controlnet_path.exists():
        fail(f"Error: ControlNet image not found: {controlnet_path}")
        sys.exit(1)

    controlnet_image = ControlNetImage(
        image=controlnet_path,
        strength=args.controlnet_strength,
    )

    return ControlNet(images=[controlnet_image])


def load_base_image(args: argparse.Namespace) -> Optional[I2iParams]:
    """Load base image for img2img if specified."""
    if not args.image:
        return None

    img_path = Path(args.image)
    if not img_path.exists():
        fail(f"Error: Base image not found: {img_path}")
        sys.exit(1)

    return I2iParams(
        image=img_path,
        strength=args.strength,
        noise=args.noise,
    )


def generate_streaming(client: NovelAI, args: argparse.Namespace) -> None:
    """Generate images using streaming."""
    info("[bold cyan]Starting streaming generation...[/bold cyan]")

    size = parse_size(args.size)

    params_kwargs = dict(
        prompt=args.prompt,
        model=args.model,
        size=size,
        steps=args.steps,
        scale=args.scale,
        sampler=args.sampler,
        quality=args.quality,
        uc_preset=args.uc_preset,
        negative_prompt=args.negative_prompt,
        stream="sse",
    )
    if args.seed is not None:
        params_kwargs["seed"] = args.seed
    params = GenerateImageStreamParams(**params_kwargs)

    try:
        _save_stream_chunks(client.image.generate_stream(params), args.stream_dir)
    except Exception as e:
        fail(f"Error during streaming: {e}")
        sys.exit(1)


def generate_standard(client: NovelAI, args: argparse.Namespace) -> None:
    """Generate images using standard method."""
    size = parse_size(args.size)

    character_references = load_reference_image(args)
    character_prompts = load_character_prompt(args)
    controlnet = load_controlnet(args)
    i2i = load_base_image(args)

    params_kwargs = dict(
        prompt=args.prompt,
        model=args.model,
        size=size,
        steps=args.steps,
        scale=args.scale,
        sampler=args.sampler,
        quality=args.quality,
        uc_preset=args.uc_preset,
        negative_prompt=args.negative_prompt,
        n_samples=args.n_images,
        character_references=character_references,
        characters=character_prompts,
        controlnet=controlnet,
        i2i=i2i,
    )
    if args.seed is not None:
        params_kwargs["seed"] = args.seed
    params = GenerateImageParams(**params_kwargs)

    info(f"[bold cyan]Generating {args.n_images} image(s)...[/bold cyan]")
    summary = Table(show_header=False, box=None)
    summary.add_row("Model", str(args.model))
    summary.add_row("Size", str(size))
    summary.add_row(
        "Params",
        f"steps={args.steps}, scale={args.scale}, sampler={args.sampler}",
    )
    if args.seed is not None:
        summary.add_row("Seed", str(args.seed))
    if character_references:
        summary.add_row(
            "Reference",
            f"{args.reference} (fidelity={args.ref_fidelity}, strength={args.ref_strength})",
        )
    if controlnet:
        summary.add_row(
            "ControlNet",
            f"{args.controlnet} (strength={args.controlnet_strength})",
        )
    if i2i:
        summary.add_row(
            "Img2Img",
            f"{args.image} (strength={args.strength}, noise={args.noise})",
        )
    console.print(summary)

    try:
        images = client.image.generate(params)
        _save_images(images, args.output)
        success(f"Successfully generated {len(images)} image(s)!")

    except Exception as e:
        fail(f"Error during generation: {e}")
        sys.exit(1)
