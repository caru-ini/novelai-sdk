"""Character reference example

This example shows how to use reference images to control style and character appearance.
Character Reference feature allows you to specify reference images
with different types and fidelity levels.
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import Character, CharacterReference, GenerateImageParams

load_dotenv()

client = NovelAI()

prompt = "1girl, standing"
reference_image_path = Path("reference_character.png")

if not reference_image_path.exists():
    print(f"Error: Reference image not found: {reference_image_path}")
    print("Please provide a reference image.")
    exit(1)

character_references = [
    CharacterReference(
        image=reference_image_path,
        type="character",
        fidelity=0.75,  # higher fidelity means more similar to the reference image
    )
]

characters = [
    Character(
        prompt="girl,leaning forward, v",
        enabled=True,
    )
]

params = GenerateImageParams(
    prompt=prompt,
    model="nai-diffusion-4-5-full",
    size=(832, 1216),
    steps=23,
    scale=5.0,
    quality=True,
    uc_preset="light",
    sampler="k_euler_ancestral",
    character_references=character_references,
)

images = client.image.generate(params)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for i, img in enumerate(images):
    img.save(output_dir / f"character_reference_{i + 1}.png")
    print(f"Saved: {output_dir / f'character_reference_{i + 1}.png'}")
