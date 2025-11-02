"""NovelAI Image Generation CLI

A command-line interface for generating images using the NovelAI API.
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv

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


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="NovelAI Image Generation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic generation
  python cli.py "1girl, cat ears, maid" -o output.png

  # Custom settings
  python cli.py "landscape, sunset" --model nai-diffusion-4-5-full --steps 28 --scale 6.0

  # With character reference
  python cli.py "1girl, standing" --reference ref.png --ref-fidelity 0.8

  # With ControlNet
  python cli.py "1girl" --controlnet edge.png --controlnet-strength 0.8

  # Img2Img
  python cli.py "improve quality" --image base.png --strength 0.5

  # Streaming generation
  python cli.py "1girl" --stream --stream-dir streaming_output

  # Batch generation
  python cli.py "1girl" --n-images 4
        """,
    )

    # Required arguments
    parser.add_argument("prompt", type=str, help="Prompt for image generation")

    # Output options
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output",
        help="Output file or directory path (default: output)",
    )

    # Model options
    parser.add_argument(
        "--model",
        type=str,
        default="nai-diffusion-4-5-full",
        choices=[
            "nai-diffusion-4-5-full",
            "nai-diffusion-4-5-inpainting",
            "nai-diffusion-furry-3",
        ],
        help="Model to use (default: nai-diffusion-4-5-full)",
    )

    # Size options
    parser.add_argument(
        "--size",
        type=str,
        default="portrait",
        help='Image size (e.g., "portrait", "landscape", "square", or "832x1216") (default: portrait)',
    )

    # Generation parameters
    parser.add_argument(
        "--steps", type=int, default=23, help="Number of steps (default: 23)"
    )
    parser.add_argument(
        "--scale", type=float, default=5.0, help="Guidance scale (default: 5.0)"
    )
    parser.add_argument(
        "--sampler",
        type=str,
        default="k_euler_ancestral",
        choices=[
            "k_euler_ancestral",
            "k_euler",
            "k_dpmpp_2s_ancestral",
            "k_dpmpp_2m",
            "k_dpmpp_sde",
            "ddim",
        ],
        help="Sampler to use (default: k_euler_ancestral)",
    )
    parser.add_argument("--seed", type=int, help="Random seed (omit for random)")

    # Quality options
    parser.add_argument("--quality", action="store_true", help="Enable quality tags")
    parser.add_argument(
        "--uc-preset",
        type=str,
        default="strong",
        choices=["preset_low_quality", "preset_bad_anatomy", "light", "strong"],
        help="Undesired content preset (default: strong)",
    )
    parser.add_argument("--negative-prompt", type=str, help="Negative prompt")

    # Reference image options
    parser.add_argument("--reference", type=str, help="Character reference image path")
    parser.add_argument(
        "--ref-type",
        type=str,
        default="character",
        choices=["character", "style", "reference"],
        help="Reference type (default: character)",
    )
    parser.add_argument(
        "--ref-fidelity",
        type=float,
        default=0.75,
        help="Reference fidelity 0.0-1.0 (default: 0.75)",
    )

    # Character prompt options
    parser.add_argument(
        "--character-prompt", type=str, help="Character prompt (region prompt)"
    )

    # ControlNet options
    parser.add_argument("--controlnet", type=str, help="ControlNet image path")
    parser.add_argument(
        "--controlnet-strength",
        type=float,
        default=0.75,
        help="ControlNet strength 0.0-1.0 (default: 0.75)",
    )

    # Img2Img options
    parser.add_argument("--image", type=str, help="Base image for img2img")
    parser.add_argument(
        "--strength",
        type=float,
        default=0.7,
        help="Img2Img strength 0.0-1.0 (default: 0.7)",
    )

    # Batch options
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

    # Streaming options
    parser.add_argument(
        "--stream", action="store_true", help="Use streaming generation"
    )
    parser.add_argument(
        "--stream-dir",
        type=str,
        default="streaming_output",
        help="Directory for streaming chunks",
    )

    return parser.parse_args()


def parse_size(size_str: str) -> Any:
    """Parse size string to tuple or return preset name."""
    if "x" in size_str:
        try:
            width, height = map(int, size_str.split("x"))
            return (width, height)
        except ValueError:
            print(f"Error: Invalid size format: {size_str}")
            sys.exit(1)
    return size_str


def load_reference_image(
    args: argparse.Namespace,
) -> Optional[list[CharacterReference]]:
    """Load character reference image if specified."""
    if not args.reference:
        return None

    ref_path = Path(args.reference)
    if not ref_path.exists():
        print(f"Error: Reference image not found: {ref_path}")
        sys.exit(1)

    return [
        CharacterReference(
            image=ref_path,
            type=args.ref_type,
            fidelity=args.ref_fidelity,
        )
    ]


def load_character_prompt(args: argparse.Namespace) -> Optional[list[Character]]:
    """Load character prompt if specified."""
    if not args.character_prompt:
        return None

    return [
        Character(
            prompt=args.character_prompt,
            enabled=True,
        )
    ]


def load_controlnet(args: argparse.Namespace) -> Optional[ControlNet]:
    """Load ControlNet if specified."""
    if not args.controlnet:
        return None

    controlnet_path = Path(args.controlnet)
    if not controlnet_path.exists():
        print(f"Error: ControlNet image not found: {controlnet_path}")
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
        print(f"Error: Base image not found: {img_path}")
        sys.exit(1)

    return I2iParams(
        image=img_path,
        strength=args.strength,
        noise=0.0,
    )


def generate_streaming(client: NovelAI, args: argparse.Namespace) -> None:
    """Generate images using streaming."""
    print("Starting streaming generation...")

    size = parse_size(args.size)

    params = GenerateImageStreamParams(
        prompt=args.prompt,
        model=args.model,
        size=size,
        steps=args.steps,
        scale=args.scale,
        sampler=args.sampler,
        seed=args.seed,
        quality=args.quality,
        uc_preset=args.uc_preset,
        negative_prompt=args.negative_prompt,
        stream="sse",
    )

    output_dir = Path(args.stream_dir)
    output_dir.mkdir(exist_ok=True)

    total_bytes = 0
    chunk_count = 0

    try:
        for chunk in client.image.generate_stream(params):
            from base64 import b64decode

            decoded_image = b64decode(chunk.image.encode("utf-8"))
            total_bytes += len(decoded_image)
            chunk_count += 1

            chunk_path = output_dir / f"chunk_{chunk_count:04d}.png"
            chunk_path.write_bytes(decoded_image)

            print(
                f"Received chunk {chunk_count}: {len(decoded_image)} bytes (total: {total_bytes} bytes)"
            )

        print(f"\n✓ Streaming complete! Received {total_bytes} bytes total")
        print(f"✓ Saved {chunk_count} chunks to: {output_dir}")

    except Exception as e:
        print(f"Error during streaming: {e}")
        sys.exit(1)


def generate_standard(client: NovelAI, args: argparse.Namespace) -> None:
    """Generate images using standard method."""
    size = parse_size(args.size)

    # Load optional features
    character_references = load_reference_image(args)
    character_prompts = load_character_prompt(args)
    controlnet = load_controlnet(args)
    i2i = load_base_image(args)

    params = GenerateImageParams(
        prompt=args.prompt,
        model=args.model,
        size=size,
        steps=args.steps,
        scale=args.scale,
        sampler=args.sampler,
        seed=args.seed,
        quality=args.quality,
        uc_preset=args.uc_preset,
        negative_prompt=args.negative_prompt,
        n_samples=args.n_images,
        character_references=character_references,
        characters=character_prompts,
        controlnet=controlnet,
        i2i=i2i,
    )

    print(f"Generating {args.n_images} image(s)...")
    print(f"Model: {args.model}")
    print(f"Size: {size}")
    print(f"Steps: {args.steps}, Scale: {args.scale}, Sampler: {args.sampler}")
    if args.seed:
        print(f"Seed: {args.seed}")
    if character_references:
        print(f"Reference: {args.reference} (fidelity: {args.ref_fidelity})")
    if controlnet:
        print(f"ControlNet: {args.controlnet} (strength: {args.controlnet_strength})")
    if i2i:
        print(f"Img2Img: {args.image} (strength: {args.strength})")
    print()

    try:
        images = client.image.generate(params)

        # Determine output path
        output_path = Path(args.output)

        if args.n_images == 1:
            # Single image: save to specified file or default
            if output_path.suffix == "":
                output_path = output_path / "image.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            images[0].save(output_path)
            print(f"✓ Saved: {output_path}")
        else:
            # Multiple images: save to directory
            if output_path.suffix != "":
                output_path = output_path.parent
            output_path.mkdir(parents=True, exist_ok=True)

            for i, img in enumerate(images):
                img_path = output_path / f"image_{i + 1:04d}.png"
                img.save(img_path)
                print(f"✓ Saved: {img_path}")

        print(f"\n✓ Successfully generated {len(images)} image(s)!")

    except Exception as e:
        print(f"Error during generation: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Parse arguments
    args = parse_args()

    # Initialize client
    try:
        client = (
            NovelAI()
        )  # API key is loaded from NOVELAI_API_KEY environment variable
    except Exception as e:
        print(f"Error: Failed to initialize NovelAI client: {e}")
        print("Make sure NOVELAI_API_KEY is set in your environment or .env file")
        sys.exit(1)

    # Generate images
    if args.stream:
        generate_streaming(client, args)
    else:
        generate_standard(client, args)


if __name__ == "__main__":
    main()
