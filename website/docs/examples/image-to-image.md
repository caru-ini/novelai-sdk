# Image-to-Image (i2i)

Generate a new image based on an existing image.
Useful for refining rough sketches or changing the style of an image.

```python
from novelai.types import GenerateImageParams, I2iParams

# Configure i2i parameters
i2i_params = I2iParams(
    image="input_sketch.png",  # Base64 string or file path
    # Change Strength
    # Closer to 0.0: Keeps original image
    # Closer to 1.0: Focuses on prompt, deviates from original
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
