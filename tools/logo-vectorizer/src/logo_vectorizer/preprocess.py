"""Prepare source alpha and orientation without denoising or palette reduction."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

LIGHT_BACKGROUND_THRESHOLD = 230
BACKGROUND_COLOR_TOLERANCE = 24
ALPHA_VISIBILITY_THRESHOLD = 16


@dataclass(frozen=True)
class PreparedImage:
    """Store tracing pixels and preparation warnings."""

    rgba: np.ndarray
    warnings: tuple[str, ...]


def prepare_image(path: Path) -> PreparedImage:
    """Load source pixels with EXIF orientation applied."""
    with Image.open(path) as image:
        rgba = np.array(ImageOps.exif_transpose(image).convert("RGBA"), dtype=np.uint8)
    return prepare_pixels(rgba)


def prepare_pixels(rgba: np.ndarray) -> PreparedImage:
    """Copy RGB unchanged, remove near-white backgrounds, and threshold alpha."""
    validate_rgba(rgba)
    pixels = _remove_light_border_background(rgba.copy())
    warnings = ()
    if np.any((pixels[:, :, 3] > 0) & (pixels[:, :, 3] < 255)):
        warnings = ("Partial transparency is thresholded into solid shapes during tracing.",)
    pixels[:, :, 3] = np.where(pixels[:, :, 3] > ALPHA_VISIBILITY_THRESHOLD, 255, 0)
    return PreparedImage(pixels, warnings)


def _remove_light_border_background(rgba: np.ndarray) -> np.ndarray:
    """Remove near-white colors estimated from the opaque image border."""
    if np.any(rgba[:, :, 3] < 255):
        return rgba

    rgb = rgba[:, :, :3].astype(np.int16)
    border = np.concatenate([rgb[0, :, :], rgb[-1, :, :], rgb[:, 0, :], rgb[:, -1, :]])
    background = np.median(border, axis=0)

    if float(np.mean(background)) < LIGHT_BACKGROUND_THRESHOLD:
        return rgba

    distance = np.linalg.norm(rgb - background, axis=2)
    alpha = np.where(distance < BACKGROUND_COLOR_TOLERANCE, 0, 255).astype(np.uint8)
    return np.dstack([rgba[:, :, :3], alpha])


def validate_rgba(rgba: np.ndarray) -> None:
    """Require a nonempty height-by-width-by-four uint8 image."""
    if not isinstance(rgba, np.ndarray) or rgba.dtype != np.uint8:
        raise ValueError("rgba must be a NumPy array with dtype uint8.")
    if rgba.ndim != 3 or rgba.shape[2] != 4 or min(rgba.shape[:2]) == 0:
        raise ValueError("rgba must have shape (height, width, 4) with nonzero dimensions.")
