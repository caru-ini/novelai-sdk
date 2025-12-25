"""Functions to convert user models to core API models"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .._utils.image import crop_and_resize, image_to_base64
from ..constants import UC_FURRY_FOCUS, UC_HUMAN_FOCUS, UC_LIGHT, UC_NONE, UC_STRONG
from ..types.api import image as api_types
from ..types.user import image as user_types

if TYPE_CHECKING:
    from .._client.client import AsyncNovelAI, NovelAI


def _map_uc_preset_to_int(uc_preset: user_types.UCPreset) -> int:
    """Map UC preset to integer"""
    return {
        UC_STRONG: 0,
        UC_LIGHT: 1,
        UC_FURRY_FOCUS: 2,
        UC_HUMAN_FOCUS: 3,
        UC_NONE: 4,
    }[uc_preset]


def _convert_characters_to_char_prompts(
    characters: list[user_types.Character] | None,
) -> list[api_types.CharacterPrompt] | None:
    """Convert high-level Character list to CharacterPrompt list"""
    if characters is None:
        return None

    return [
        api_types.CharacterPrompt(
            prompt=char.prompt,
            uc=char.negative_prompt,
            center=api_types.CenterPoint(
                x=float(char.position[0]), y=float(char.position[1])
            ),
            enabled=char.enabled,
        )
        for char in characters
    ]


def _convert_characters_to_char_captions(
    characters: list[user_types.Character] | None,
    is_negative: bool = False,
) -> list[api_types.V4CharacterCaption]:
    """Convert high-level Character list to V4CharacterCaption list

    Args:
        characters: List of characters
        is_negative: If True, use negative_prompt instead of prompt
    """
    if characters is None:
        return []

    return [
        api_types.V4CharacterCaption(
            char_caption=char.negative_prompt if is_negative else char.prompt,
            centers=[
                api_types.CenterPoint(
                    x=float(char.position[0]), y=float(char.position[1])
                )
            ],
        )
        for char in characters
        if char.enabled
    ]


def _create_v4_prompts(
    processed_prompt: str,
    processed_negative: str,
    characters: list[user_types.Character] | None = None,
) -> tuple[api_types.V4ConditionInput, api_types.V4ConditionInput]:
    """Create V4 prompt structures from processed prompts and characters"""
    v4_prompt = api_types.V4ConditionInput(
        caption=api_types.V4Caption(
            base_caption=processed_prompt,
            char_captions=_convert_characters_to_char_captions(
                characters, is_negative=False
            ),
        ),
        use_coords=False,
        use_order=True,
    )

    v4_negative_prompt = api_types.V4ConditionInput(
        caption=api_types.V4Caption(
            base_caption=processed_negative,
            char_captions=_convert_characters_to_char_captions(
                characters, is_negative=True
            ),
        ),
        legacy_uc=False,
    )

    return v4_prompt, v4_negative_prompt


def _convert_image_input(
    image: user_types.ImageInput | None,
) -> str | None:
    """Convert image input (Path/PIL/bytes/str) to base64 string"""
    if image is None:
        return None
    return image_to_base64(image)


def _convert_character_references(
    character_references: list[user_types.CharacterReference] | None,
) -> tuple[
    list[str] | None,  # images
    list[api_types.ReferenceConditionInput] | None,  # descriptions
    list[float] | None,  # strengths
    list[float] | None,  # secondary strengths
    list[float] | None,  # information extracted
]:
    """Convert CharacterReference list to separate lists for API

    Returns:
        Tuple of (images, secondary_strengths, types)
    """
    if character_references is None:
        return None, None, None, None, None

    images = [
        crop_and_resize(image_to_base64(ref.image)) for ref in character_references
    ]
    descriptions = [
        api_types.ReferenceConditionInput(
            caption=api_types.ReferenceCaption(base_caption=ref.type),
            legacy_uc=False,
        )
        for ref in character_references
    ]
    strengths = [1.0] * len(character_references)
    information_extracted = [1.0] * len(character_references)
    secondary_strengths = [round(1 - ref.fidelity, 2) for ref in character_references]

    return (
        images,
        descriptions,
        strengths,
        secondary_strengths,
        information_extracted,
    )


def _convert_controlnet(
    controlnet: user_types.ControlNet | None,
    client: NovelAI,
) -> tuple[
    list[str] | None,
    list[float] | None,
]:
    """Convert ControlNet list to separate lists for API"""
    if controlnet is None:
        return None, None
    vibe_data = [img.encode_vibe(client) for img in controlnet.images]
    return vibe_data, [img.strength for img in controlnet.images]


async def _async_convert_controlnet(
    controlnet: user_types.ControlNet | None,
    client: AsyncNovelAI,
) -> tuple[
    list[str] | None,
    list[float] | None,
]:
    """Convert ControlNet list to separate lists for API (async)"""
    if controlnet is None:
        return None, None

    # Check cache first to avoid async calls if possible or gather results
    vibe_data: list[str] = []
    for img in controlnet.images:
        # If cache exists (sync), use it. If not, await.
        # But we can't easily check cache without duplicate logic or strict access.
        # Assuming encode_vibe handles cache check.
        # ControlNetImage.encode_vibe expects 'client' which has 'api_client.image.encode_vibe'.
        # Since client is AsyncNovelAI, encode_vibe returns a coroutine.
        # However, ControlNetImage.encode_vibe type hint says it returns str.
        # This implies ControlNetImage.encode_vibe needs to be async-aware or we bypass it.
        # Bypass it for now to be safe.
        if img._vibe_data:
            vibe_data.append(img._vibe_data)
        else:
            result = await client.api_client.image.encode_vibe(
                api_types.EncodeVibeRequest(
                    image=image_to_base64(img.image),
                    information_extracted=img.info_extracted,
                    model=img.controlnet_model,
                )
            )
            img._vibe_data = result
            vibe_data.append(result)

    return vibe_data, [img.strength for img in controlnet.images]


def convert_user_params_to_api_params(
    params: user_types.GenerateImageParams,
    client: NovelAI,
) -> tuple[str, str, api_types.ImageParameters]:
    """Convert user params to API request components

    Args:
        params: High-level user parameters
        client: NovelAI client

    Returns:
        Tuple of (input_prompt, model, api_parameters)
    """
    if not isinstance(params.size, tuple):
        raise ValueError("Size must be a tuple of ints")
    width, height = params.size

    processed_prompt = params.processed_prompt
    processed_negative = params.processed_negative_prompt

    # For V4 models, create V4 prompt structures
    if params.is_v4(params.model):
        v4_prompt, v4_negative_prompt = _create_v4_prompts(
            processed_prompt, processed_negative, params.characters
        )

        prompt_field = None
    else:
        # Non-V4 models use standard prompt/negative_prompt fields
        v4_prompt = None
        v4_negative_prompt = None
        prompt_field = processed_prompt

    character_prompts = _convert_characters_to_char_prompts(params.characters)

    (
        cr_images,
        cr_descriptions,
        cr_strengths,
        cr_secondary_strengths,
        cr_information_extracted,
    ) = _convert_character_references(params.character_references)

    (
        cn_vibe_data,
        cn_strengths,
    ) = _convert_controlnet(params.controlnet, client)

    # Build ImageParameters with explicit defaults from user params
    generate_params = api_types.ImageParameters(
        params_version=3,
        legacy=False,
        legacy_v3_extend=False,
        deliberate_euler_ancestral_bug=False,
        prefer_brownian=True,
        autoSmea=False,
        sm=False,
        sm_dyn=False,
        add_original_image=True,
        dynamic_thresholding=False,
        legacy_uc=False,
        inpaintImg2ImgStrength=1,
        use_coords=False,
        normalize_reference_strength_multiple=False,
        # Basic parameters
        width=width,
        height=height,
        steps=params.steps,
        scale=params.scale,
        sampler=params.sampler,
        seed=params.seed,
        n_samples=params.n_samples,
        noise_schedule=params.noise_schedule,
        # Prompt fields (depends on model version)
        prompt=prompt_field,
        negative_prompt=processed_negative,
        v4_prompt=v4_prompt,
        v4_negative_prompt=v4_negative_prompt,
        qualityToggle=params.quality,
        ucPreset=_map_uc_preset_to_int(params.uc_preset),
        cfg_rescale=params.cfg_rescale,
        skip_cfg_above_sigma=58 if params.variety_boost else None,
        # i2i
        image=_convert_image_input(getattr(params.i2i, "image", None)),
        strength=getattr(params.i2i, "strength", None),
        noise=getattr(params.i2i, "noise", None),
        # Inpainting
        mask=_convert_image_input(getattr(params.i2i, "mask", None)),
        # ControlNet
        reference_image_multiple=cn_vibe_data,
        reference_strength_multiple=cn_strengths,
        controlnet_strength=getattr(params.controlnet, "strength", 1),
        # Character References
        director_reference_images=cr_images,
        director_reference_descriptions=cr_descriptions,
        director_reference_information_extracted=cr_information_extracted,
        director_reference_secondary_strength_values=cr_secondary_strengths,
        director_reference_strength_values=cr_strengths,
        # Character prompts
        characterPrompts=character_prompts or [],
        # Misc
        image_format=params.image_format,
    )

    return params.prompt, params.model, generate_params


async def async_convert_user_params_to_api_params(
    params: user_types.GenerateImageParams,
    client: AsyncNovelAI,
) -> tuple[str, str, api_types.ImageParameters]:
    """Convert user params to API request components (async)"""
    if not isinstance(params.size, tuple):
        raise ValueError("Size must be a tuple of ints")
    width, height = params.size

    processed_prompt = params.processed_prompt
    processed_negative = params.processed_negative_prompt

    if params.is_v4(params.model):
        v4_prompt, v4_negative_prompt = _create_v4_prompts(
            processed_prompt, processed_negative, params.characters
        )
        prompt_field = None
    else:
        v4_prompt = None
        v4_negative_prompt = None
        prompt_field = processed_prompt

    character_prompts = _convert_characters_to_char_prompts(params.characters)

    (
        cr_images,
        cr_descriptions,
        cr_strengths,
        cr_secondary_strengths,
        cr_information_extracted,
    ) = _convert_character_references(params.character_references)

    (
        cn_vibe_data,
        cn_strengths,
    ) = await _async_convert_controlnet(params.controlnet, client)

    generate_params = api_types.ImageParameters(
        params_version=3,
        legacy=False,
        legacy_v3_extend=False,
        deliberate_euler_ancestral_bug=False,
        prefer_brownian=True,
        autoSmea=False,
        sm=False,
        sm_dyn=False,
        add_original_image=True,
        dynamic_thresholding=False,
        legacy_uc=False,
        inpaintImg2ImgStrength=1,
        use_coords=False,
        normalize_reference_strength_multiple=False,
        width=width,
        height=height,
        steps=params.steps,
        scale=params.scale,
        sampler=params.sampler,
        seed=params.seed,
        n_samples=params.n_samples,
        noise_schedule=params.noise_schedule,
        prompt=prompt_field,
        negative_prompt=processed_negative,
        v4_prompt=v4_prompt,
        v4_negative_prompt=v4_negative_prompt,
        qualityToggle=params.quality,
        ucPreset=_map_uc_preset_to_int(params.uc_preset),
        cfg_rescale=params.cfg_rescale,
        skip_cfg_above_sigma=58 if params.variety_boost else None,
        image=_convert_image_input(getattr(params.i2i, "image", None)),
        strength=getattr(params.i2i, "strength", None),
        noise=getattr(params.i2i, "noise", None),
        mask=_convert_image_input(getattr(params.i2i, "mask", None)),
        reference_image_multiple=cn_vibe_data,
        reference_strength_multiple=cn_strengths,
        controlnet_strength=getattr(params.controlnet, "strength", 1),
        director_reference_images=cr_images,
        director_reference_descriptions=cr_descriptions,
        director_reference_information_extracted=cr_information_extracted,
        director_reference_secondary_strength_values=cr_secondary_strengths,
        director_reference_strength_values=cr_strengths,
        characterPrompts=character_prompts or [],
        # Misc
        image_format=params.image_format,
    )

    return params.prompt, params.model, generate_params


def convert_user_params_to_api_request(
    params: user_types.GenerateImageParams | user_types.GenerateImageStreamParams,
    client: NovelAI,
) -> api_types.ImageGenerationRequest | api_types.StreamImageGenerationRequest:
    """Convert user params to low-level API request

    This is a pure function that converts high-level user parameters
    to low-level API request objects.

    Args:
        params: High-level user parameters (GenerateImageParams or GenerateImageStreamParams)
        client: NovelAI client

    Returns:
        Low-level API request (ImageGenerationRequest or StreamImageGenerationRequest)
    """
    input_prompt, model, generate_params = convert_user_params_to_api_params(
        params, client
    )

    if isinstance(params, user_types.GenerateImageStreamParams):
        stream_params = api_types.ImageStreamParameters(
            **generate_params.model_dump(exclude_unset=True), stream=params.stream
        )
        return api_types.StreamImageGenerationRequest(
            action="generate",
            input=input_prompt,
            model=model,
            parameters=stream_params,
            use_new_shared_trial=True,
        )

    return api_types.ImageGenerationRequest(
        action="generate",
        input=input_prompt,
        model=model,
        parameters=generate_params,
        use_new_shared_trial=True,
    )


async def async_convert_user_params_to_api_request(
    params: user_types.GenerateImageParams | user_types.GenerateImageStreamParams,
    client: AsyncNovelAI,
) -> api_types.ImageGenerationRequest | api_types.StreamImageGenerationRequest:
    """Convert user params to low-level API request (async)"""
    (
        input_prompt,
        model,
        generate_params,
    ) = await async_convert_user_params_to_api_params(params, client)

    if isinstance(params, user_types.GenerateImageStreamParams):
        stream_params = api_types.ImageStreamParameters(
            **generate_params.model_dump(exclude_unset=True), stream=params.stream
        )
        return api_types.StreamImageGenerationRequest(
            action="generate",
            input=input_prompt,
            model=model,
            parameters=stream_params,
            use_new_shared_trial=True,
        )

    return api_types.ImageGenerationRequest(
        action="generate",
        input=input_prompt,
        model=model,
        parameters=generate_params,
        use_new_shared_trial=True,
    )
