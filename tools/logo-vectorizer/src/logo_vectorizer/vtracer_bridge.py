"""Run the fixed VTracer preset used by the accepted no-cleanup trials."""

import logging
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

import vtracer
from PIL import Image

from logo_vectorizer.preprocess import PreparedImage

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VTracerSettings:
    """Define numeric arguments accepted by the VTracer tracing API."""

    filter_speckle: int
    color_precision: int
    layer_difference: int
    corner_threshold: int
    length_threshold: float
    max_iterations: int
    splice_threshold: int
    path_precision: int


SETTINGS = VTracerSettings(
    filter_speckle=2,
    color_precision=7,
    layer_difference=10,
    corner_threshold=50,
    length_threshold=2.5,
    max_iterations=16,
    splice_threshold=35,
    path_precision=4,
)


def write_vtracer_svg(image: PreparedImage, destination: Path) -> None:
    """Trace source colors with fixed spline settings and no custom cleanup."""
    logger.debug("VTracer settings: %s", SETTINGS)
    if not image.rgba[:, :, 3].any():
        _write_empty_svg(image, destination)
        return
    with tempfile.TemporaryDirectory() as temporary_directory:
        source = Path(temporary_directory) / "input.png"
        Image.fromarray(image.rgba).save(source)
        vtracer.convert_image_to_svg_py(
            str(source),
            str(destination),
            colormode="color",
            hierarchical="stacked",
            mode="spline",
            **asdict(SETTINGS),
        )


def _write_empty_svg(image: PreparedImage, destination: Path) -> None:
    """Represent a fully transparent source without calling the tracer."""
    height, width = image.rgba.shape[:2]
    destination.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"/>\n',
        encoding="utf-8",
    )
