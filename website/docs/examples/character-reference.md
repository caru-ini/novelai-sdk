# Character Reference

Maintain consistent character appearances with reference images.
Extremely useful when you want to generate the same character in different situations.

```python
from novelai.types import CharacterReference, GenerateImageParams

# Define Reference
character_references = [
    CharacterReference(
        image="reference.png", # Base64 string or file path
        type="character",
        fidelity=0.75, # Strength (0.0 to 1.0)
    )
]

# Configure Generation
params = GenerateImageParams(
    prompt="1girl, standing in a garden",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)

# Execute (assuming client is initialized)
# images = client.image.generate(params)
```
