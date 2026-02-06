# Precise Reference

:::info
This feature was previously called "Character Reference" and was renamed to "Precise Reference" in February 2026.
:::

Control character appearance and art style with reference images.
Precise Reference allows you to maintain consistent character designs and apply specific art styles across generations.

## Features

- **Multiple reference images**: Combine multiple references to apply different characters and styles
- **Reference types**:
  - `"character"`: Reference character appearance only
  - `"style"`: Reference art style only
  - `"character&style"`: Reference both character and style (default)
- **Fine control**: Adjust fidelity and strength for each reference

## Basic Example

```python
from novelai.types import CharacterReference, GenerateImageParams

# Single character reference
character_references = [
    CharacterReference(
        image="reference.png",  # Base64 string or file path
        type="character",  # "character", "style", or "character&style"
        fidelity=1.0,  # Reference fidelity (0.0 to 1.0, default: 1.0)
        strength=1.0,  # Reference weight (0.0 to 1.0, default: 1.0)
    )
]

params = GenerateImageParams(
    prompt="1girl, standing in a garden",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)

# Execute (assuming client is initialized)
# images = client.image.generate(params)
```

## Advanced: Multiple References

Combine character and style references from different images:

```python
character_references = [
    CharacterReference(
        image="character.png",
        type="character",  # Character appearance only
        fidelity=1.0,
        strength=0.75,
    ),
    CharacterReference(
        image="style.png",
        type="style",  # Art style only
        fidelity=1.0,
        strength=0.75,
    ),
]

params = GenerateImageParams(
    prompt="1girl, standing, rating:general, very aesthetic",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)
```

## Parameters

- **`image`** (required): Reference image (file path, Base64 string, or PIL Image)
- **`type`**: Reference type
  - `"character"`: Apply character appearance only
  - `"style"`: Apply art style only
  - `"character&style"`: Apply both (default)
- **`fidelity`**: How closely to match the reference (0.0-1.0, default: 1.0)
- **`strength`**: Relative weight when using multiple references (0.0-1.0, default: 1.0)
