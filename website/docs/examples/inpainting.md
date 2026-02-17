# Inpainting

Regenerate a masked area of an existing image.
Use a mask image to specify which parts of the image to regenerate while keeping the rest intact.

## Basic Example

```python
from novelai.types import GenerateImageParams, InpaintParams

inpaint_params = InpaintParams(
    image="source.png",   # Source image (file path, Base64, or PIL Image)
    mask="mask.png",      # Mask image (white=inpaint, black=keep)
    strength=1.0,
)

# Model is automatically switched to the inpainting variant
# (e.g. nai-diffusion-4-5-full -> nai-diffusion-4-5-full-inpainting)
params = GenerateImageParams(
    prompt="1girl, standing, smile",
    model="nai-diffusion-4-5-full",
    inpaint=inpaint_params,
)

# images = client.image.generate(params)
```

## Mask Format

The mask image specifies which areas to regenerate:

- **White** (`#FFFFFF`): Area to regenerate (inpaint)
- **Black** (`#000000`): Area to keep unchanged

The mask is automatically preprocessed (binarized and resized) to match the API requirements.

## Parameters

- **`image`** (required): Source image (file path, Base64 string, or PIL Image)
- **`mask`** (required): Mask image defining the inpaint region (file path, Base64 string, or PIL Image)
- **`strength`**: Inpainting strength (`0.01`–`1.0`, default: `1.0`)
  - `1.0`: Fully regenerates the masked area
  - Lower values: Blends original content with new generation
- **`seed`**: Random seed for noise (auto-generated if omitted)

:::info
The model is automatically switched to the inpainting variant (e.g., `nai-diffusion-4-5-full` → `nai-diffusion-4-5-full-inpainting`). You don't need to specify the inpainting model manually.
:::

:::tip
For best results, make the mask slightly larger than the area you want to change. This gives the model more context for seamless blending.
:::
