"""Validate public inputs, diagnostic output, and failure propagation."""

import logging
import subprocess

import numpy as np
import pytest
from PIL import Image, ImageDraw

from logo_vectorizer.cli import main
from logo_vectorizer.config import OutputFormat, resolve_output_paths
from logo_vectorizer.errors import ConfigurationError, VectorizationError
from logo_vectorizer.pipeline import vectorize
from logo_vectorizer.preprocess import prepare_pixels


@pytest.fixture(autouse=True)
def restore_application_logging():
    """Release CLI handlers before pytest closes captured streams."""
    yield
    logger = logging.getLogger("logo_vectorizer")
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    logger.setLevel(logging.NOTSET)
    logger.propagate = True


@pytest.mark.parametrize("formats", [set(), {"svg"}, {OutputFormat.SVG, "pdf"}])
def test_invalid_formats_fail_before_creating_outputs(tmp_path, formats):
    source = tmp_path / "missing.png"
    paths = resolve_output_paths(source, tmp_path / "outputs")
    with pytest.raises(ConfigurationError, match="formats"):
        vectorize(source, paths, formats)
    assert not paths.directory.exists()


@pytest.mark.parametrize(
    "rgba",
    [
        np.zeros((1, 1, 3), dtype=np.uint8),
        np.zeros((0, 1, 4), dtype=np.uint8),
        np.zeros((1, 1, 4), dtype=float),
    ],
)
def test_invalid_pixel_arrays_have_clear_errors(rgba):
    with pytest.raises(ValueError, match="rgba"):
        prepare_pixels(rgba)


def test_missing_source_preserves_cause_and_leaves_no_output(tmp_path):
    source = tmp_path / "missing.png"
    paths = resolve_output_paths(source, tmp_path / "outputs")
    with pytest.raises(VectorizationError, match="Load and prepare input") as failure:
        vectorize(source, paths, {OutputFormat.SVG})
    assert isinstance(failure.value.__cause__, FileNotFoundError)
    assert not paths.directory.exists()


@pytest.mark.parametrize("debug", [False, True])
def test_cli_failure_tracebacks_are_debug_only(tmp_path, capsys, debug):
    log_file = tmp_path / "diagnostics.log"
    arguments = [str(tmp_path / "missing.png"), "--log-file", str(log_file)]
    if debug:
        arguments.append("--debug")
    assert main(arguments) == 1
    captured = capsys.readouterr()
    assert "Load and prepare input failed" in captured.err
    assert ("Traceback" in captured.err) == debug
    assert ("Formats:" in captured.err) == debug
    assert "Vectorization complete" not in captured.out
    assert "Load and prepare input failed" in log_file.read_text(encoding="utf-8")


def test_cli_invalid_format_returns_configuration_error(tmp_path, capsys):
    assert main([str(tmp_path / "unused.png"), "--formats", "cdr"]) == 2
    assert "Unsupported output format" in capsys.readouterr().err


def test_renderer_failure_includes_stderr(tmp_path, monkeypatch, capsys):
    source = tmp_path / "brand.png"
    image = Image.new("RGBA", (48, 48), (255, 255, 255, 0))
    ImageDraw.Draw(image).rectangle((12, 12, 36, 36), fill=(200, 30, 40, 255))
    image.save(source)

    def fail_renderer(*args, **kwargs):
        raise subprocess.CalledProcessError(3, "resvg", stderr="Cannot render test SVG")

    monkeypatch.setattr("logo_vectorizer.export.subprocess.run", fail_renderer)
    assert main([str(source), "--out-dir", str(tmp_path), "--formats", "png"]) == 1
    error = capsys.readouterr().err
    assert "Render PNG preview failed" in error
    assert "Cannot render test SVG" in error


def test_debug_success_logs_settings_and_stage_timings(tmp_path, capsys):
    source = tmp_path / "brand.png"
    image = Image.new("RGBA", (48, 48), (255, 255, 255, 0))
    ImageDraw.Draw(image).rectangle((12, 12, 36, 36), fill=(200, 30, 40, 255))
    image.save(source)
    assert main([str(source), "--out-dir", str(tmp_path), "--formats", "svg", "--debug"]) == 0
    logs = capsys.readouterr().err
    assert "VTracer settings:" in logs
    assert "Completed stage: Trace SVG master" in logs
    assert "Prepared image: shape=" in logs
