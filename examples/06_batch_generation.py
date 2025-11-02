"""Batch generation example

This example demonstrates how to generate multiple images at once
and save them with different naming patterns.
Seed of each image will seed, seed + 1, ..., seed + n_samples - 1.
WARNING: Running this example consumes Anlas (credit)!!
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import GenerateImageParams

load_dotenv()

client = NovelAI()

prompt = "1girl, cat ears, very aesthetic, masterpiece"

params = GenerateImageParams(
    prompt=prompt,
    model="nai-diffusion-4-5-full",
    size=(832, 1216),
    steps=23,
    scale=5.0,
    sampler="k_euler_ancestral",
    n_samples=4,
)

images = client.image.generate(params)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for i, img in enumerate(images, start=1):
    output_path = output_dir / f"batch_{i:02d}.png"
    img.save(output_path)
    print(f"Saved image {i}/4: {output_path}")

print(f"\nAll {len(images)} images saved successfully!")
