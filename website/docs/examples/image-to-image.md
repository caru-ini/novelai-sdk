# Image-to-Image (i2i)

Generate a new image based on an existing image.
Useful for refining rough sketches or changing the style of an image.

## Basic Example

```python
from novelai.types import GenerateImageParams, I2iParams

# Configure i2i parameters
i2i_params = I2iParams(
    image="input_sketch.png",  # Base64 string or file path
    strength=0.7,
    noise=0.0,
)

params = GenerateImageParams(
    prompt="cyberpunk style, neon lights, highly detailed",
    model="nai-diffusion-4-5-full",
    i2i=i2i_params,
)

# Generation is standard
# images = client.image.generate(params)
```

## Parameters

- **`image`** (required): Source image (file path, Base64 string, or PIL Image)
- **`strength`**: How much the output deviates from the source (`0.01`–`0.99`, default: `0.7`)
  - Closer to `0.0`: Keeps the original image
  - Closer to `1.0`: Focuses on the prompt, deviates from the original
- **`noise`**: Noise injection for variation (`0.0`–`0.99`, default: `0.0`)
- **`seed`**: Random seed for noise (auto-generated if omitted)

:::tip
Start with `strength=0.5` and adjust up or down depending on how much you want to change the original image.
:::
