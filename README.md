# NovelAI Python SDK

![intro](./docs/images/intro.png)

[![PyPI version](https://img.shields.io/pypi/v/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![Python Version](https://img.shields.io/pypi/pyversions/novelai-sdk.svg)](https://pypi.org/project/novelai-sdk/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

English | [日本語](/docs/README_jp.md)

A modern, type-safe Python SDK for NovelAI's image generation API. Features robust validation with Pydantic v2 and complete type hints.

## Features

- Python 3.10+ with full type hints and Pydantic v2 validation
- High-level convenience API with automatic validation
- Built-in PIL/Pillow support for easy image operations
- SSE streaming for real-time progress monitoring
- Character references, ControlNet, and multi-character positioning

## Comparison with Alternatives

| Feature                         | novelai-sdk | [novelai-api](https://github.com/Aedial/novelai-api) | [novelai-python](https://github.com/LlmKira/novelai-python) |
| ------------------------------- | :---------: | :--------------------------------------------------: | :---------------------------------------------------------: |
| Type Safety (Pydantic v2)       |      ✅      |                          ❌                           |                              ✅                              |
| Async Support                   |      ✅      |                          ✅                           |                              ✅                              |
| Image Generation                |      ✅      |                          ✅                           |                              ✅                              |
| Text Generation                 |      🚧      |                          ✅                           |                              ✅                              |
| **Character Reference**         |      ✅      |                          ❌                           |                              ❌                              |
| **Multi-Character Positioning** |      ✅      |                          ❌                           |                              ✅                              |
| ControlNet / Vibe Transfer      |      ✅      |                          ❌                           |                              ✅                              |
| SSE Streaming                   |      ✅      |                          ❌                           |                              ✅                              |
| Python 3.13+                    |      ✅      |                          ❌                           |                              ❌                              |
| Active Maintenance              |      ✅      |                          ✅                           |                              ⚠️                              |

✅ Supported | ❌ Not supported | 🚧 Planned | ⚠️ Limited maintenance

## Documentation

For detailed guides and advanced usage, visit our [Documentation Site](https://caru-ini.github.io/novelai-sdk/).

## Quick Start

### Installation

```bash
# Using pip
pip install novelai-sdk

# Using uv (recommended)
uv add novelai-sdk
```

### Basic Usage

```python
from novelai import NovelAI
from novelai.types import GenerateImageParams

# Initialize client (API key from NOVELAI_API_KEY environment variable)
client = NovelAI()

# Generate an image
params = GenerateImageParams(
    prompt="1girl, cat ears, masterpiece, best quality",
    model="nai-diffusion-4-5-full",
    size="portrait",  # or (832, 1216)
    steps=23,
    scale=5.0,
)

images = client.image.generate(params)
images[0].save("output.png")
```

## Authentication

Provide your NovelAI API key via environment variable or direct initialization:

```python
# Using .env file (recommended)
from dotenv import load_dotenv
load_dotenv()
client = NovelAI()

# Environment variable
import os
os.environ["NOVELAI_API_KEY"] = "your_api_key_here"
client = NovelAI()

# Direct initialization
client = NovelAI(api_key="your_api_key_here")
```

### API Architecture

The library provides a high-level API with sensible defaults and automatic validation. A low-level API exists internally for direct REST endpoint access, but is not intended for general use.

#### High-Level API

```python
from novelai import NovelAI
from novelai.types import GenerateImageParams

client = NovelAI()
params = GenerateImageParams(
    prompt="a beautiful landscape",
    model="nai-diffusion-4-5-full",
    size="landscape",
    quality=True,
)
images = client.image.generate(params)
```

## Advanced Features

### Character Reference

Maintain consistent character appearances with reference images:

```python
from novelai.types import CharacterReference

character_references = [
    CharacterReference(
        image="reference.png",
        type="character",
        fidelity=0.75,
    )
]

params = GenerateImageParams(
    prompt="1girl, standing",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)
```

### Multi-Character Positioning

Position multiple characters individually with separate prompts:

```python
from novelai.types import Character

characters = [
    Character(
        prompt="1girl, red hair, blue eyes",
        enabled=True,
        position=(0.2, 0.5),
    ),
    Character(
        prompt="1boy, black hair, green eyes",
        enabled=True,
        position=(0.8, 0.5),
    ),
]

params = GenerateImageParams(
    prompt="two people standing",
    model="nai-diffusion-4-5-full",
    characters=characters,
)
```

### ControlNet (Vibe Transfer)

Control composition and pose with reference images:

```python
from novelai.types import ControlNet, ControlNetImage, GenerateImageParams

controlnet_image = ControlNetImage(image="pose_reference.png", strength=0.6)
controlnet = ControlNet(images=[controlnet_image])

params = GenerateImageParams(
    prompt="1girl, standing",
    model="nai-diffusion-4-5-full",
    controlnet=controlnet,
)
```

### Streaming Generation

Monitor generation progress in real-time:

```python
from novelai.types import GenerateImageStreamParams
from base64 import b64decode

params = GenerateImageStreamParams(
    prompt="1girl, standing",
    model="nai-diffusion-4-5-full",
    stream="sse",
)

for chunk in client.image.generate_stream(params):
    image_data = b64decode(chunk.image)
    print(f"Received {len(image_data)} bytes")
```

### Image-to-Image

Transform existing images with text prompts:

```python
from novelai.types import GenerateImageParams, I2iParams

i2i_params = I2iParams(
    image="input.png",
    strength=0.5,  # 0.0-1.0
    noise=0.0,
)

params = GenerateImageParams(
    prompt="cyberpunk style",
    model="nai-diffusion-4-5-full",
    i2i=i2i_params,
)
```

### Batch Generation

Generate multiple variations efficiently:

```python
params = GenerateImageParams(
    prompt="1girl, various poses",
    model="nai-diffusion-4-5-full",
    n_samples=4,
)

images = client.image.generate(params)
for i, img in enumerate(images):
    img.save(f"output_{i}.png")
```

## Examples

For practical usage examples, see the [Examples Documentation](https://caru-ini.github.io/novelai-sdk/examples/) or the [`examples/`](./examples/) directory.

## Roadmap

- [x] Async support
- [x] FastAPI integration example
- [ ] Vibe transfer file support (`.naiv4vibe`, `.naiv4vibebundle`)
- [ ] Anlas consumption calculator
- [ ] Image metadata extraction
- [ ] Text generation API support

## Development

### Setup

```bash
git clone https://github.com/caru-ini/novelai-sdk.git
cd novelai-sdk
uv sync
```

### Code Quality

```bash
# Format code
uv run poe fmt

# Lint code
uv run poe lint

# Type checking
uv run poe check

# Install poe globally for easier access
uv tool install poe

# Run all checks before committing
uv run poe pre-commit
```

### Testing

Tests will be added in future releases.

## Requirements

- Python 3.13+
- httpx (HTTP client)
- Pillow (image processing)
- Pydantic v2 (validation and type safety)
- python-dotenv (environment variables)

## Contributing

Contributions are welcome. For major changes, please open an issue first.

### Commit Guidelines

```plaintext
{feat|fix|docs|style|refactor|test|chore}: Short description
```

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Run code quality checks (`uv run poe pre-commit`)
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

MIT License. See LICENSE file for details.

## Links

- [NovelAI Official Website](https://novelai.net/)
- [NovelAI Documentation](https://docs.novelai.net/)
- [Issue](https://github.com/caru-ini/novelai-sdk/issues)

## Disclaimer

This is an unofficial client library. Not affiliated with NovelAI. Requires an active NovelAI subscription.

## Acknowledgments

Thanks to the NovelAI team and all contributors.
