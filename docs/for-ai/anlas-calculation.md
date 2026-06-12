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
- `nai-diffusion-5-*`
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

For V4 and V4.5 models, the SDK also adds the two documented Vibe Transfer
extras. V5 is excluded because it does not support Vibe Transfer or ControlNet:

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

- These extras apply only to V4 and V4.5 models in the current SDK implementation;
  V5 does not support Vibe Transfer or ControlNet
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

## Director Tools (/ai/augment-image)

Reverse-engineered from the official frontend bundle on 2026-06-13
(`_next/static/chunks/_app-63a03a4a01166c4c.js`, cost function exported as
`tY`/`GI`; the image-tools UI lives in chunk `9955-3ce87fd845a9c6af.js`).
Not yet verified against live billing — validate on a funded account by
diffing `client.user.get_anlas()` around real calls and comparing with
`calculate_augment_anlas()`.

The web UI prices every Director Tool by image area only (the tool type does
not change the base price):

1. Normalize the billed area: scale down so `width * height <= 3145728`
   (1536x2048, the UI input cap), then scale up so the area is `>= 1048576`.
   Both scales multiply each dimension by `sqrt(target / area)` and floor.
2. Price the normalized size as a V3 generation at 28 steps, 1 sample,
   no SMEA, strength 1: `max(ceil(2.951823174884865e-6 * area +
   5.753298233447344e-7 * area * 28), 2)`.
3. On an active Opus subscription the cost is `0` when the billed area stays
   within 1MP (i.e. only when the source image is at most 1MP).
4. `bg-removal` is special-cased in the UI: `total = 3 * base + 5`, and the
   Opus discount is explicitly bypassed — background removal is never free.

Sentinels in the frontend (`-2`/`-3` for "too large") are not reproduced;
inputs above 3MP are billed at the scaled-down 3MP-equivalent size, matching
the UI's normalization.

The upscale tool uses a different, bucket-based table
(`[[1048576, 7], [786432, 5], [524288, 3], [409600, 2], [262144, 1]]`, free on
Opus up to 409600 px) — not implemented because the SDK does not expose
upscale yet.

### Price Table

Computed with `calculate_augment_anlas()` at representative boundary sizes.
"Standard tools" covers every tool except `bg-removal` (the price does not
depend on the tool type).

| Input size | Billed size | Standard tools | Standard tools (Opus) | bg-removal (any tier) |
| --- | --- | ---: | ---: | ---: |
| 512x512 | 1024x1024 | 20 | 0 | 65 |
| 832x1216 | 847x1237 | 20 | 0 | 65 |
| 1024x1024 | 1024x1024 | 20 | 0 | 65 |
| 1536x2048 | 1536x2048 | 60 | 60 | 185 |
| 2048x2048 | 1773x1773 | 60 | 60 | 185 |

### Estimator API

- `LineArtParams.calculate_anlas(...)` (and the other per-tool params models)
- `novelai.utils.anlas.calculate_augment_anlas(tool, width, height, ...)`
