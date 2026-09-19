"""Coordinate tracing and exports independently of command-line interaction."""

import logging
from pathlib import Path

from logo_vectorizer.config import OutputFormat, OutputPaths, validate_formats
from logo_vectorizer.diagnostics import execution_stage
from logo_vectorizer.export import write_pdf_from_svg, write_preview_from_svg
from logo_vectorizer.preprocess import prepare_image
from logo_vectorizer.reporting import build_report, read_svg_statistics, write_report
from logo_vectorizer.vtracer_bridge import write_vtracer_svg

logger = logging.getLogger(__name__)


def vectorize(
    input_path: Path,
    paths: OutputPaths,
    formats: set[OutputFormat],
) -> None:
    """Prepare artwork, trace its SVG master, and deliver requested outputs."""
    validate_formats(formats)
    logger.info("Vectorizing %s", input_path)
    logger.debug("Formats: %s; outputs: %s", formats, paths)
    with execution_stage("Load and prepare input"):
        prepared = prepare_image(input_path)
    logger.debug("Prepared image: shape=%s", prepared.rgba.shape)
    with execution_stage("Create output directory"):
        paths.directory.mkdir(parents=True, exist_ok=True)
    with execution_stage("Trace SVG master"):
        write_vtracer_svg(prepared, paths.svg)
    logger.info("Tracing engine: vtracer")
    for warning in prepared.warnings:
        logger.warning("%s", warning)
    _export_derivatives(paths, formats)
    with execution_stage("Write report"):
        report = build_report(
            source=input_path,
            paths=paths,
            formats=formats,
            warnings=prepared.warnings,
            statistics=read_svg_statistics(paths.svg),
        )
        write_report(report, paths.report)
    logger.info("Outputs saved to %s", paths.directory)


def _export_derivatives(paths: OutputPaths, formats: set[OutputFormat]) -> None:
    """Render requested derivatives from the shared SVG master."""
    if OutputFormat.PDF in formats:
        with execution_stage("Export PDF"):
            write_pdf_from_svg(paths.svg, paths.pdf)
    if OutputFormat.PNG in formats:
        with execution_stage("Render PNG preview"):
            write_preview_from_svg(paths.svg, paths.png)
