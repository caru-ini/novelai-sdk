"""ControlNet(Vibe Transfer) example

This example demonstrates how to use ControlNet(Vibe Transfer) to generate images with a reference image.
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import Character, ControlNet, ControlNetImage, GenerateImageParams

load_dotenv()

client = NovelAI()

base_prompt = "1girl, standing, rating:general, simple background, very aesthetic, masterpiece, no text"

reference_image_path = Path("reference.png")

if not reference_image_path.exists():
    print(f"Error: Reference image not found: {reference_image_path}")
    print("Please provide a reference image.")
    exit(1)

controlnet_image = ControlNetImage(image=reference_image_path, strength=0.75)

controlnet = ControlNet(images=[controlnet_image])

characters = [
    Character(
        prompt="girl,leaning forward, v",
        negative_prompt="",
        position=(0.5, 0.5),
        enabled=True,
    )
]

params = GenerateImageParams(
    prompt=base_prompt,
    model="nai-diffusion-4-5-full",
    size=(832, 1216),
    steps=23,
    scale=5.0,
    sampler="k_euler_ancestral",
    seed=3282663226,
    controlnet=controlnet,
    characters=characters,
    cfg_rescale=0.0,
)


images = client.image.generate(params)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for i, img in enumerate(images):
    img.save(output_dir / f"advanced_reference_{i + 1}.png")
    print(f"Saved: {output_dir / f'advanced_reference_{i + 1}.png'}")
