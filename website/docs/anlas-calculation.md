---
title: Anlas Calculation
---

# Anlas Calculation

This page summarizes the current Anlas estimation logic used by the SDK.

It is a best-effort estimate based on the current NovelAI web UI and official
documentation. It is useful for previews, but it is not guaranteed to be a
100% accurate billing source of truth.

## What Is Included

- Base image generation cost
- Opus lightweight discount
- Img2img and inpaint strength adjustments
- Vibe encoding surcharge for uncached references in the high-level API
- Additional Vibe surcharge after the fourth reference
- Character Reference surcharge

## Quick Example

```python
from novelai.types import GenerateImageParams

params = GenerateImageParams(
    prompt="1girl, night city",
    model="nai-diffusion-4-5-full",
    size=(1024, 1024),
    steps=28,
)

estimate = params.calculate_anlas(is_opus=True)
print(estimate.total_anlas)
print(estimate.base_anlas)
```

## Important Notes

- `str(estimate)` returns the total Anlas value
- `int(estimate)` returns the same total
- Low-level `calculate_anlas(model, ImageParameters)` cannot infer uncached Vibe
  encoding cost because raw cache state is not available there

For the reverse-engineered details used during implementation, see the
repository note in `docs/for-ai/anlas-calculation.md`.
