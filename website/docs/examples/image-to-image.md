# Image-to-Image (i2i)

Generate a new image based on an existing image.
Useful for refining rough sketches or changing the style of an image.

```python
from novelai.types import GenerateImageParams

params = GenerateImageParams(
    prompt="cyberpunk style, neon lights, highly detailed",
    model="nai-diffusion-4-5-full",
    
    # Input Image (Base64 string or file path)
    image="input_sketch.png",
    
    # Change Strength
    # Closer to 0.0: Keeps original image
    # Closer to 1.0: Focuses on prompt, deviates from original
    strength=0.7, 
)

# Generation is standard
# images = client.image.generate(params)
```
