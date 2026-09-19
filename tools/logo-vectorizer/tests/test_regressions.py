"""Check the accepted preparation behavior without altering source pixels."""

import numpy as np
import pytest

from logo_vectorizer.preprocess import prepare_pixels


def test_rgb_and_existing_transparency_are_preserved_without_mutation():
    rgba = np.array([[[255, 255, 255, 0], [201, 31, 47, 255]]], dtype=np.uint8)
    original = rgba.copy()
    result = prepare_pixels(rgba)
    assert np.array_equal(result.rgba, original)
    assert np.array_equal(rgba, original)
    assert not np.shares_memory(result.rgba, rgba)


def test_partial_alpha_is_thresholded_and_reported():
    rgba = np.array([[[10, 20, 30, 16], [40, 50, 60, 17]]], dtype=np.uint8)
    result = prepare_pixels(rgba)
    assert result.rgba[:, :, 3].tolist() == [[0, 255]]
    assert np.array_equal(result.rgba[:, :, :3], rgba[:, :, :3])
    assert result.warnings


def test_near_white_background_is_removed():
    rgba = np.full((8, 8, 4), 255, dtype=np.uint8)
    rgba[2:6, 2:6] = (200, 30, 40, 255)
    result = prepare_pixels(rgba)
    assert result.rgba[0, 0, 3] == 0
    assert result.rgba[3, 3].tolist() == [200, 30, 40, 255]


@pytest.mark.parametrize(
    "rgba",
    [
        np.zeros((1, 1, 3), dtype=np.uint8),
        np.zeros((0, 1, 4), dtype=np.uint8),
        np.zeros((1, 1, 4), dtype=float),
    ],
)
def test_invalid_pixels_are_rejected(rgba):
    with pytest.raises(ValueError, match="rgba"):
        prepare_pixels(rgba)
