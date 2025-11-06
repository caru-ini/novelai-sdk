"""Image utilities for converting various formats to base64"""

from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
from typing import Any, TypeGuard, cast

from PIL import Image

ImageInput = str | bytes | Path | Image.Image | Any

PILImageModule: Any = None
np_module: Any = None
pil_available = False
np_available = False
cv2_available = False

try:
    from PIL import Image as PILImageModule

    pil_available = True
except ImportError:
    pass

try:
    import numpy as np_module

    np_available = True
except ImportError:
    pass

try:
    import cv2

    cv2_available = True
    del cv2
except ImportError:
    pass


def to_pil_image(image: ImageInput) -> Image.Image:
    """Convert various image formats to PIL Image

    Args:
        image: Can be:
            - str: File path or base64 string
            - bytes: Raw image bytes

    Returns:
        Image.Image: The converted PIL Image object
    """
    if not pil_available or PILImageModule is None:
        raise ImportError("Pillow is required for image conversion")

    if isinstance(image, str):
        if image.startswith("data:image/"):
            # Base64 string
            image = base64.b64decode(image.split(",")[1])
        else:
            # File path
            image = Path(image)

    if isinstance(image, Path):
        return PILImageModule.open(image)

    if isinstance(image, bytes):
        return PILImageModule.open(BytesIO(image))

    if is_pil_image(image):
        return image

    raise TypeError("Unsupported image type")


def is_pil_image(image: object) -> TypeGuard[Image.Image]:
    """Type guard to check if object is a PIL Image"""
    return hasattr(image, "save") and hasattr(image, "mode") and hasattr(image, "size")


def is_numpy_array(image: object) -> bool:
    """Check if object is a numpy array (cv2 image)"""
    if np_module is None:
        return False
    return isinstance(image, np_module.ndarray)


def crop_and_resize(b64_image: str) -> str:
    """Resize base64 image to 1024x1536 with aspect ratio preserved and centered black padding.

    Args:
        b64_image: Base64-encoded image string (without data URI prefix)

    Returns:
        Base64-encoded PNG string (without data URI prefix)
    """
    if not pil_available or PILImageModule is None:
        raise ImportError("Pillow is required for crop_and_resize")

    try:
        img_data = base64.b64decode(b64_image)
        with BytesIO(img_data) as buf:
            image = PILImageModule.open(buf).convert("RGB")
    except Exception as e:
        raise ValueError(f"Failed to decode base64 image: {e}")

    target_w, target_h = 1024, 1536
    src_w, src_h = image.size

    src_ratio = src_w / src_h
    target_ratio = target_w / target_h

    if src_ratio > target_ratio:
        new_w = target_w
        new_h = int(target_w / src_ratio)
    else:
        new_h = target_h
        new_w = int(target_h * src_ratio)

    resized = image.resize((new_w, new_h), PILImageModule.LANCZOS)

    background = PILImageModule.new("RGB", (target_w, target_h), (0, 0, 0))

    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    background.paste(resized, (offset_x, offset_y))

    buffer = BytesIO()
    background.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def image_to_base64(image: ImageInput) -> str:
    """Convert various image formats to base64 string

    Args:
        image: Can be:
            - str: File path or base64 string
            - bytes: Raw image bytes
            - Path: Pathlib path to image file
            - PIL.Image: PIL Image object
            - numpy.ndarray: OpenCV/cv2 image (BGR or RGB)

    Returns:
        Base64 encoded string (without data URI prefix)

    Raises:
        ValueError: If PIL is not installed and PIL.Image is provided
        FileNotFoundError: If path doesn't exist
        ImportError: If numpy/cv2 is not installed and numpy array is provided
    """
    # Already base64 string
    if isinstance(image, str):
        # Check if it's already base64 (doesn't contain path separators and is long)
        if "/" not in image and "\\" not in image and len(image) > 100:
            return image
        # Otherwise treat as file path
        return path_to_base64(Path(image))

    # Path object
    if isinstance(image, Path):
        return path_to_base64(image)

    # Raw bytes
    if isinstance(image, bytes):
        return base64.b64encode(image).decode("utf-8")

    # numpy array (cv2 image)
    if is_numpy_array(image):
        if not pil_available or PILImageModule is None:
            raise ImportError(
                "Pillow is required to process numpy arrays. "
                "This should not happen as Pillow is a required dependency."
            )

        if np_module is None:
            raise ImportError("numpy is not available")

        # Type narrowing: we know it's a numpy array at this point
        img_array: Any = image

        # Convert numpy array to PIL Image
        # cv2 uses BGR by default, so we need to convert to RGB
        if len(img_array.shape) == 3:
            if img_array.shape[2] == 3:
                # Assume BGR (cv2 default) and convert to RGB
                img_array_rgb: Any = img_array[:, :, ::-1]  # BGR to RGB
                pil_image = PILImageModule.fromarray(img_array_rgb, mode="RGB")
            elif img_array.shape[2] == 4:
                # Assume BGRA and convert to RGBA, then handle alpha
                img_array_rgba: Any = img_array[:, :, [2, 1, 0, 3]]  # BGRA to RGBA
                pil_image = PILImageModule.fromarray(img_array_rgba, mode="RGBA")
                # Convert RGBA to RGB with white background
                background = PILImageModule.new("RGB", pil_image.size, (255, 255, 255))
                background.paste(pil_image, mask=pil_image.split()[3])
                pil_image = background
            else:
                raise ValueError(
                    f"Unsupported number of channels: {img_array.shape[2]}"
                )
        elif len(img_array.shape) == 2:
            # Grayscale image
            pil_image = PILImageModule.fromarray(img_array, mode="L")
            pil_image = pil_image.convert("RGB")
        else:
            raise ValueError(f"Unsupported image shape: {img_array.shape}")

        # Encode as PNG
        buffer = BytesIO()
        pil_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    # PIL Image
    if pil_available and PILImageModule is not None and is_pil_image(image):
        pil_image = image
        buffer = BytesIO()

        # Convert RGBA to RGB if needed
        if pil_image.mode == "RGBA":
            # Create white background
            background = PILImageModule.new("RGB", pil_image.size, (255, 255, 255))
            alpha_channel = pil_image.split()[3]
            background.paste(pil_image, mask=alpha_channel)
            pil_image = cast(Image.Image, background)
        elif pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        pil_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    raise TypeError(
        f"Unsupported image type: {type(image)}. "
        "Supported types: str (path/base64), bytes, pathlib.Path, PIL.Image, numpy.ndarray (cv2)"
    )


def path_to_base64(path: Path) -> str:
    """Convert file path to base64 string

    Args:
        path: Path to image file

    Returns:
        Base64 encoded string

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
