from pathlib import Path

import pytest

from logo_vectorizer.config import (
    OutputFormat,
    parse_formats,
    resolve_output_paths,
)


def test_parse_formats_accepts_known_values() -> None:
    assert parse_formats("svg,pdf") == {OutputFormat.SVG, OutputFormat.PDF}


def test_parse_formats_rejects_unknown_values() -> None:
    with pytest.raises(ValueError):
        parse_formats("svg,cdr")


def test_resolve_output_paths_uses_input_stem() -> None:
    paths = resolve_output_paths(Path("Brand Logo.png"), Path("out"))

    assert paths.directory == Path("out") / "Brand Logo"
    assert paths.svg.name == "Brand Logo.vector.svg"
    assert paths.pdf.name == "Brand Logo.print.pdf"
    assert paths.png.name == "Brand Logo.preview.png"
