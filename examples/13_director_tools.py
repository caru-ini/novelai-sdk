"""Director Tools example

Director Tools transform an existing image instead of generating a new one.
This example extracts line art, changes the character's expression, and
removes the background from a single source image.
"""

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import EmotionParams

load_dotenv()

SOURCE_IMAGE = "input.png"


def main():
    # API key is loaded from environment variable NOVELAI_API_KEY
    with NovelAI() as client:
        # Each tool has a dedicated shortcut method
        line_art = client.tools.line_art(SOURCE_IMAGE)
        line_art[0].save("lineart.png")

        # colorize/emotion take a prompt and a defry level (0 = full effect)
        smiling = client.tools.emotion(SOURCE_IMAGE, "happy", defry=1)
        smiling[0].save("happy.png")

        # Background removal may return multiple images (separated layers)
        layers = client.tools.remove_background(SOURCE_IMAGE)
        for i, layer in enumerate(layers):
            layer.save(f"bg_removed_{i}.png")

        # The same calls are available through per-tool parameter models,
        # which can also estimate the Anlas cost before sending
        params = EmotionParams(
            image=SOURCE_IMAGE, emotion="surprised", prompt="wide eyes"
        )
        print(f"Estimated cost: {params.calculate_anlas()} Anlas")
        images = client.tools.augment(params)
        images[0].save("surprised.png")


if __name__ == "__main__":
    main()
