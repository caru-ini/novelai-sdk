"""
Advanced example of character references(precise references).

This example shows how to use new precise character references(formally called character references),
introduced in February 2026.
The reference type can be set to "char", "style", or "both" for a single image.
Multiple references are supported and can be combined to apply different characters and styles.
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import Character, CharacterReference, GenerateImageParams

load_dotenv()

client = NovelAI()

base_prompt = "1girl, standing, rating:general, simple background, very aesthetic, masterpiece, no text"

char_image = Path("reference_character.png")
style_image = Path("reference_style.png")

if not char_image.exists():
    print(f"Error: Reference image not found: {char_image}")
    print("Please provide a reference image.")
    exit(1)

if not style_image.exists():
    print(f"Error: Reference image not found: {style_image}")
    print("Please provide a reference image.")
    exit(1)

character_references = [
    CharacterReference(
        image=char_image,
        type="character",
        fidelity=1,
        strength=0.75,
    ),
    CharacterReference(
        image=style_image,
        type="style",
        fidelity=1,
        strength=0.75,
    ),
]

characters = [
    Character(
        prompt="girl, v",
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
    character_references=character_references,
    characters=characters,
    cfg_rescale=0.0,
)


images = client.image.generate(params)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for i, img in enumerate(images):
    img.save(output_dir / f"advanced_reference_{i + 1}.png")
    print(f"Saved: {output_dir / f'advanced_reference_{i + 1}.png'}")
