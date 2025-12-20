# NovelAI API Examples

This directory contains practical examples demonstrating various features of the NovelAI Python SDK.

## Prerequisites

```bash
# Install the package
pip install -e ..

# Install python-dotenv (for loading .env files)
pip install python-dotenv

# Or with uv
uv sync

# Install python-dotenv with uv
uv add python-dotenv
```

## Examples Overview

### Basic Usage

#### [`01_basic_v4.py`](01_basic_v4.py)

The simplest example showing basic image generation with NovelAI V4 models.

```bash
python 01_basic_v4.py
```

**Key Features:**

- Basic text-to-image generation
- V4 model usage
- Simple parameter configuration

---

### Async Usage

#### [`09_async_generation.py`](09_async_generation.py)

Demonstrates how to use the asynchronous client for better performance in non-blocking applications.

```bash
python 09_async_generation.py
```

**Key Features:**

- `AsyncNovelAI` client usage
- Asynchronous context manager (`async with`)
- Non-blocking execution

---

### Director Tools (Character Reference)

#### [`02_character_reference.py`](02_character_reference.py)

Demonstrates how to use reference images to control character appearance and style.

```bash
python 02_character_reference.py
```

**Key Features:**

- Single character reference
- Type selection (character, style, character&style)
- Fidelity control

**Requirements:** A reference image file (`reference.png`)

---

### ControlNet (Vibe Transfer)

#### [`05_controlnet.py`](05_controlnet.py)

Demonstrates how to use ControlNet (Vibe Transfer) with reference images and character positioning.

```bash
python 05_controlnet.py
```

**Key Features:**

- ControlNet image processing
- Strength parameter control
- Combined with character prompts

**Requirements:** A reference image file (`reference.png`)

---

### Character Prompts (V4+ Feature)

#### [`03_character_prompts.py`](03_character_prompts.py)

Shows how to position multiple characters in specific locations using V4's character prompt feature.

```bash
python 03_character_prompts.py
```

**Key Features:**

- Multiple character positioning
- Per-character prompts
- Coordinate-based placement (x, y)

---

### Advanced Combinations

#### [`04_advanced_reference.py`](04_advanced_reference.py)

Combines Director Tools and Character Prompts for maximum control.

```bash
python 04_advanced_reference.py
```

**Key Features:**

- Character reference + character prompts
- Artist style mixing with weights
- Recreates the structure from `ref_both_075.json`

**Requirements:** A reference image file (`reference.png`)

---

### Batch & Streaming

#### [`06_batch_generation.py`](06_batch_generation.py)

Generate multiple images in a single request.

```bash
python 06_batch_generation.py
```

**Key Features:**

- Multiple images per request (n_samples)
- Efficient batch processing

#### [`07_streaming_generation.py`](07_streaming_generation.py)

Use streaming to receive progressive updates during generation.

```bash
python 07_streaming_generation.py
```

**Key Features:**

- Progressive generation monitoring
- Msgpack streaming format
- Real-time progress tracking

---

### Image Transformation

#### [`08_img2img.py`](08_img2img.py)

Transform an existing image according to your prompt.

```bash
python 08_img2img.py
```

**Key Features:**

- Image-to-image transformation
- Strength parameter control
- Source image preservation

**Requirements:** A source image file (`source.png`)

---

### Web Framework Integration

#### FastAPI ([10_fastapi_integration.py](10_fastapi_integration.py))

Demonstrates how to integrate the SDK into a [FastAPI](https://fastapi.tiangolo.com/) web application.

**Key Features:**

- Lifecycle management using `lifespan` for client initialization and cleanup
- Asynchronous image generation within an API endpoint
- Returning the generated image directly as a PNG response

To run this example, you need to install additional dependencies:

```bash
pip install fastapi uvicorn
```

Then run the server:

```bash
python examples/10_fastapi_integration.py
```

After the server starts, you can generate an image by visiting `http://localhost:8000/generate?prompt=cat`.

---

## Common Parameters

### Model Selection

There are type hints available for model selection.
On your IDE, set cursor to `model=` and `ctrl`+`space` to see available models.

![Model Selection](/docs/images/auto-complete-model.png)

```python
GenerateImageParams(
    ...
    model="|nai-diffusion-4-5-full",
           ↑ set the cursor here and press ctrl+space to see available models
    ...
)
```

### Size Selection

Similarly, there are type hints available for size selection.
Set cursor to `size=` and `ctrl`+`space` to see available preset sizes.

![Size Selection](/docs/images/size-selection.png)

```python
GenerateImageParams(
    ...
    size="|portrait",
          ↑ set the cursor here and press ctrl+space to see available size presets
    ...
)
```

Of course, you can also specify custom sizes as tuples:

```python
GenerateImageParams(
    ...
    size=(512, 768),  # Width x Height in pixels
    ...
)
```

Size is validated when creating the instance.
If the size is invalid, a `ValueError` will be raised.

### Sampling Parameters

```python
GenerateImageParams(
    ...
    steps=23  # Number of sampling steps (1-50)
    scale=5.0  # CFG scale / prompt guidance (0.0-10.0)
    sampler="k_euler_ancestral"  # Sampling method
    seed=1234567890  # Random seed for reproducibility
)
```

### Quality Settings

```python
GenerateImageParams(
    ...
    quality=True  # Automatically adds quality tags
    uc_preset="light"  # Undesired content preset
    negative_prompt="bad quality, low resolution"  # Custom negative prompt
)
```

### Character Positioning

When using character prompts, you can specify where each character should appear in the image.

You can use either coordinate tuples or grid positions:

#### Tuple Format

`(x, y)` with normalized values (0.0-1.0)

- `(0.0, 0.0)` = top-left
- `(0.5, 0.5)` = center
- `(1.0, 1.0)` = bottom-right

#### Grid Format

Use position strings like `"C3"` for easier positioning:

   ```text
             ↑ Top
   | A1 | A2 | A3 | A4 | A5 |
   | B1 | B2 | B3 | B4 | B5 |
   | C1 | C2 | C3 | C4 | C5 | 
   | D1 | D2 | D3 | D4 | D5 |
   | E1 | E2 | E3 | E4 | E5 |
    ← Left           Right →
            ↓ Bottom
   ```

- `"C3"` = center (equivalent to `(0.5, 0.5)`)

## Troubleshooting

### "API key not found"

Make sure you've set your API key either in the code or as an environment variable.

### "Reference image not found"

Some examples require reference images. Create them or use your own images.

### "Invalid size"

Image dimensions must be:

- Between 64 and 1600 pixels
- Multiples of 64

## Further Documentation

- [Project README](../README.md)
- [API Documentation](../docs/)
- [Type Definitions](../src/novelai/types/)
