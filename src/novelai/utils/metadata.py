from typing import Any, Literal

from PIL.Image import Image
from pydantic import BaseModel, ConfigDict

from novelai._utils.image import ImageInput, to_pil_image
from novelai._utils.nai_meta import extract_image_metadata


class ImageMeta(BaseModel):
    """Image metadata model"""

    png_info: dict[str, Any] | None = None
    alpha_info: dict[str, Any] | None = None
    model_config = ConfigDict(extra="allow")


def extract_metadata(image: ImageInput) -> ImageMeta:
    """Extract metadata from an image.

    Args:
        image (ImageInput): The image to extract metadata from.

    Returns:
        ImageMeta: Pydantic BaseModel containing extracted metadata.
    """
    image = to_pil_image(image)

    png_info = getattr(image, "info", None)
    alpha_info = None
    if image.mode == "RGBA":
        # skip if alpha is not present
        alpha_info = extract_image_metadata(image=image, get_fec=False)
    if not isinstance(alpha_info, dict):
        alpha_info = None

    meta = ImageMeta(png_info=png_info, alpha_info=alpha_info)

    return meta


def erase_metadata(
    image: ImageInput, target: Literal["alpha", "png_info", "both"] = "both"
) -> Image:
    """Erase metadata from an image.

    Args:
        image (ImageInput): The image to erase metadata from.
        target Literal["alpha","png_info", "both"]: Data target to erase.

    Returns
        Image: PIL Image object.
    """
    new_image = to_pil_image(image)
    if target in ["both", "alpha"]:
        print("erase Alpha")
        new_image = new_image.convert("RGB")
    if target in ["both", "png_info"]:
        print("erase info")
        new_image.info = {}

    return new_image
