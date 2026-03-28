# Anlas Calculation

This document records the base image-generation Anlas calculation reverse-engineered
from the official web interface and current documentation.

It is a best-effort estimate, not a 100% guaranteed source of truth for billing.
The web UI and backend may change independently of this SDK.

The Vibe surcharge values are taken from the official NovelAI image documentation:

- <https://docs.novelai.net/en/image/vibetransfer/>
- <https://docs.novelai.net/en/image/precisereference>

## Scope

The current SDK implementation covers the same pricing branch used for these model
families:

- `nai-diffusion-3`
- `nai-diffusion-3-furry`
- `nai-diffusion-4-*`
- `nai-diffusion-4-5-*`
- `custom`

Those models all use the same base generation formula in the bundled frontend.

## Model Grouping

The frontend first normalizes concrete model IDs into coarse groups:

- `stableDiffusionXL`
- `stableDiffusionXLFurry`
- `v4`

For the SDK's supported model set, all supported models fall into one of those three
groups, and all three groups share the same base-generation formula.

## Base Formula

Given:

- `area = width * height`
- `steps`
- `sm`
- `sm_dyn`

The frontend computes:

```text
base = ceil(2.951823174884865e-6 * area + 5.753298233447344e-7 * area * steps)
```

Then applies the SMEA multiplier:

```text
multiplier = 1.4 if sm and sm_dyn else 1.2 if sm else 1.0
w = base * multiplier
```

## Img2Img / Inpaint Strength

The strength factor is chosen in this order:

```text
strength_factor =
  inpaintImg2ImgStrength if mask is present
  strength               if image is present
  1.0                    otherwise
```

The final per-image cost is:

```text
per_image_anlas = max(ceil(w * strength_factor), 2)
```

So there is always a minimum cost of `2` Anlas per billable image.

## Opus Lightweight Bonus

If all of the following are true:

- the account is Opus
- `width * height <= 1_048_576`
- `steps <= 28`

Then one sample is free:

```text
billable_samples = n_samples - 1
```

Otherwise:

```text
billable_samples = n_samples
```

The base total is:

```text
base_anlas = per_image_anlas * billable_samples
```

## Character Reference Surcharge

For Character / Precise Reference, the SDK currently models:

```text
character_reference_anlas = 5 * reference_count * requested_samples
```

This is added on top of the base generation cost. In practice that means Opus can
reduce the base generation cost to `0` while still leaving Character Reference cost.

## Vibe Surcharges

For V4 and higher models, the SDK also adds the two documented Vibe Transfer
extras:

- Each uncached Vibe encoding adds `2` Anlas
- Each Vibe reference after the fourth adds `2` Anlas

So the full total becomes:

```text
total_anlas =
  base_anlas
  + character_reference_anlas
  + vibe_encoding_anlas
  + vibe_reference_anlas
```

Where:

```text
vibe_encoding_anlas = uncached_vibe_count * 2
vibe_reference_anlas = max(vibe_reference_count - 4, 0) * 2
```

Notes:

- These extras apply only to V4+ models in the current SDK implementation
- High-level `GenerateImageParams.calculate_anlas(...)` can include encoding cost
  because it can inspect `ControlNetImage._vibe_data`
- Low-level `calculate_anlas(model, ImageParameters)` can only include the
  reference-count surcharge because raw image/cache state is no longer available

## Cap Behavior

The frontend uses a per-image cap of `140` Anlas. If the estimated per-image cost
exceeds that cap, the bundle returns a sentinel error value (`-3`).

The Python SDK raises `ValueError` instead, which is clearer than exposing the
bundle's sentinel value as part of the public API.

## SDK Surface

The public convenience API is intentionally kept small:

- `GenerateImageParams.calculate_anlas(...)`
- `novelai.calculate_anlas(...)` for low-level `ImageParameters`

`AnlasEstimate` is a Pydantic model and `str(estimate)` returns the total Anlas
value for compact display. `int(estimate)` returns the same total.
