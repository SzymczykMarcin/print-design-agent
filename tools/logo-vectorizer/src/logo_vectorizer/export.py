"""Export vector documents to SVG, PDF, and PNG preview files."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def write_pdf_from_svg(svg_path: Path, pdf_path: Path) -> None:
    """Render a PDF from an SVG master file."""

    from reportlab.graphics import renderPDF
    from svglib.svglib import svg2rlg

    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise RuntimeError(f"Could not parse SVG for PDF export: {svg_path}")
    renderPDF.drawToFile(drawing, str(pdf_path))


def write_preview_from_svg(svg_path: Path, png_path: Path) -> None:
    """Render a PNG preview from an SVG master file."""

    executable = _find_resvg()
    if executable is None:
        raise RuntimeError(
            "resvg-cli is required for PNG previews. Install it with: "
            "python -m pip install resvg-cli"
        )
    try:
        subprocess.run(
            [str(executable), str(svg_path), str(png_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        details = (exc.stderr or exc.stdout or "No renderer diagnostics.").strip()
        raise RuntimeError(f"resvg exited with code {exc.returncode}: {details}") from exc


def _find_resvg() -> Path | None:
    """Find resvg next to Python or on PATH."""
    local = Path(sys.executable).with_name("resvg.exe")
    if local.exists():
        return local
    resolved = shutil.which("resvg")
    return Path(resolved) if resolved else None
