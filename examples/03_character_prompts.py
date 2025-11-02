"""Character prompts example for positioning multiple characters

This example demonstrates how to use character prompts to position multiple
characters in specific locations within the image. This is a V4-only feature.
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import Character, GenerateImageParams

load_dotenv()

client = NovelAI()

base_prompt = "2girls, standing, park background, very aesthetic, masterpiece"

"""
Pro tip:
You can specify character(like A1, B2, etc.) instead of (x, y) coordinates.
| A1 | A2 | A3 | A4 | A5 |
| B1 | B2 | B3 | B4 | B5 |
| C1 | C2 | C3 | C4 | C5 | 
| D1 | D2 | D3 | D4 | D5 |
| E1 | E2 | E3 | E4 | E5 |
"""

characters = [
    Character(
        prompt="girl, long blonde hair, red dress, green eyes",
        negative_prompt="",
        position="C3",  # equals (0.5, 0.5)
        enabled=True,
    ),
    Character(
        prompt="girl, short black hair, blue jacket, brown eyes",
        negative_prompt="",
        position=(0.7, 0.5),
        enabled=True,
    ),
]

params = GenerateImageParams(
    prompt=base_prompt,
    model="nai-diffusion-4-5-full",
    size=(1216, 832),
    steps=23,
    scale=5.0,
    sampler="k_euler_ancestral",
    seed=1234567890,
    characters=characters,
)

images = client.image.generate(params)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for i, img in enumerate(images):
    img.save(output_dir / f"character_prompts_{i + 1}.png")
    print(f"Saved: {output_dir / f'character_prompts_{i + 1}.png'}")
