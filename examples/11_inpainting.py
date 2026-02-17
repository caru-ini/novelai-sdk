"""Inpainting example

This example demonstrates how to use inpainting to regenerate
a masked area of an existing image.
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import GenerateImageParams, InpaintParams

load_dotenv()

client = NovelAI()

source_image = Path("source.png")
mask_image = Path("mask.png")

if not source_image.exists():
    print(f"Error: Source image not found: {source_image}")
    print("Please provide a source image for inpainting.")
    exit(1)

if not mask_image.exists():
    print(f"Error: Mask image not found: {mask_image}")
    print("Please provide a mask image (white=inpaint, black=keep).")
    exit(1)

prompt = "1girl, standing, ;d"

inpaint_params = InpaintParams(
    image=source_image,
    mask=mask_image,
    strength=1,
)

# Model is automatically switched to the inpainting variant
# (e.g. nai-diffusion-4-5-full -> nai-diffusion-4-5-full-inpainting)
params = GenerateImageParams(
    prompt=prompt,
    model="nai-diffusion-4-5-full",
    size=(832, 1216),
    steps=23,
    scale=5.0,
    sampler="k_euler_ancestral",
    inpaint=inpaint_params,
)

images = client.image.generate(params)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for i, img in enumerate(images):
    img.save(output_dir / f"inpaint_{i + 1}.png")
    print(f"Saved: {output_dir / f'inpaint_{i + 1}.png'}")
