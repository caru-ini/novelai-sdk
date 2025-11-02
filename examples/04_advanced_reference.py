"""Advanced example combining Director Tools and Character Prompts

This example demonstrates the most advanced usage by combining:
- Director Tools (Character Reference) for style/character reference
- Character Prompts for precise character positioning
- Custom positioning and prompts for each character

This recreates the structure from ref_both_075.json reference.
"""

from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import Character, CharacterReference, GenerateImageParams

load_dotenv()

client = NovelAI()

base_prompt = "1girl, standing, rating:general, simple background, very aesthetic, masterpiece, no text"

reference_image_path = Path("reference_character.png")

if not reference_image_path.exists():
    print(f"Error: Reference image not found: {reference_image_path}")
    print("Please provide a reference image.")
    exit(1)

character_references = [
    CharacterReference(
        image=reference_image_path,
        type="character&style",
        fidelity=0.75,
    )
]

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
