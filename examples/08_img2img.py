"""Image-to-image transformation example

This example demonstrates how to use an existing image as a starting point
and transform it according to your prompt.
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import GenerateImageParams, I2iParams

load_dotenv()

client = NovelAI()

source_image = Path("source.png")

if not source_image.exists():
    print(f"Error: Source image not found: {source_image}")
    print("Please provide a source image for img2img transformation.")
    exit(1)

prompt = "winter clothes, snowy background, very aesthetic, masterpiece"

i2i_params = I2iParams(
    image=source_image,
    strength=0.7,
    noise=0.0,
)

params = GenerateImageParams(
    prompt=prompt,
    model="nai-diffusion-4-5-full",
    size=(832, 1216),
    steps=23,
    scale=5.0,
    sampler="k_euler_ancestral",
    i2i=i2i_params,
)

images = client.image.generate(params)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for i, img in enumerate(images):
    img.save(output_dir / f"img2img_{i + 1}.png")
    print(f"Saved: {output_dir / f'img2img_{i + 1}.png'}")

print("\nTip: Adjust 'strength' parameter to control how much the output")
print("differs from the source image. Lower = more similar to source.")
