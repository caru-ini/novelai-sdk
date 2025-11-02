"""Basic usage example with NovelAI V4 models

This example demonstrates the simplest way to generate images using NovelAI V4.
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import GenerateImageParams

load_dotenv()

client = NovelAI()  # API key is loaded from environment variable NOVELAI_API_KEY

prompt = "1girl, cat ears, maid, white dress, white background, absurdes"

params = GenerateImageParams(
    prompt=prompt,
    model="nai-diffusion-4-5-full",
    size="portrait",  # or turple (832, 1216) which automatically validated after provided
    steps=23,
    scale=5.0,
    uc_preset="strong",
    quality=True,
    sampler="k_euler_ancestral",
    seed=1234567890,  # or omit to generate a random seed
)

images = client.image.generate(params)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for i, img in enumerate(images):
    img.save(output_dir / f"basic_v4_{i + 1}.png")
    print(f"Saved: {output_dir / f'basic_v4_{i + 1}.png'}")
