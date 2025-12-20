---
sidebar_position: 2
title: Getting Started
---

# Getting Started

Learn how to easily generate images using Python with the NovelAI SDK.
This guide walks you through the process step-by-step.

## 1. Installation

First, install `novelai-sdk`.

:::info
Python 3.10 or higher is required.
:::

Open your terminal and run:

```bash
pip install novelai-sdk
```

If you are using `uv` (recommended):

```bash
uv add novelai-sdk
```

## 2. Prepare API Key

You need a **NovelAI API Key** to use the features.

1.  Log in to [NovelAI](https://novelai.net/).
2.  Open Settings (Gear icon).
3.  Go to "Account" tab and click "Get API Key".

### Method A: Using .env (Recommended)

Create a `.env` file in your project directory:

```env
NOVELAI_API_KEY=pst-your-api-key-here
```

### Method B: Direct (For testing)

```python
client = NovelAI(api_key="pst-your-api-key-here")
```

## 3. Generate Your First Image

Let's generate an image! Save the following code as `generate.py`.

```python
import os
from novelai import NovelAI
from novelai.types import GenerateImageParams

# 1. Initialize Client
# No arguments needed if NOVELAI_API_KEY env var is set
client = NovelAI()

# 2. Configure Generation
params = GenerateImageParams(
    # Prompt
    prompt="1girl, cat ears, masterpiece, best quality",
    # Model (using V4)
    model="nai-diffusion-4-5-full",
    # Size
    size="portrait",
    # Steps
    steps=28,
    # Scale
    scale=5.0,
)

# 3. Generate
print("Generating image...")
images = client.image.generate(params)

# 4. Save
if images:
    filename = "output.png"
    images[0].save(filename)
    print(f"Saved to: {filename}")
else:
    print("Generation failed")
```

Run it:

```bash
python generate.py
```

## Next Steps

*   **[Authentication](./authentication.md)**: More about API key handling.
*   **[Examples](./examples)**: Character references, poses, etc.
