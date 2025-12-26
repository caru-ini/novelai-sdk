# Multi-Character Positioning

When generating multiple characters, their traits (hair color, eye color, clothes) can sometimes blend together.
Multi-Character Positioning allows you to assign specific prompts and positions to each character, preventing this issue.

```python
from novelai.types import Character, GenerateImageParams

characters = [
    Character(
        prompt="1girl, red hair, blue eyes, school uniform",
        enabled=True,
        position=(0.2, 0.5), # Left (X: 0.2, Y: 0.5)
    ),
    Character(
        prompt="1boy, black hair, green eyes, casual clothes",
        enabled=True,
        position=(0.8, 0.5), # Right (X: 0.8, Y: 0.5)
    ),
]

params = GenerateImageParams(
    # General prompt can be used, but details should be in characters list
    prompt="two people standing together, holding hands, best quality",
    model="nai-diffusion-4-5-full",
    size=(832, 1216),  # Size must be explicitly specified
    characters=characters,
)
```
