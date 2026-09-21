"""Render SVG or PDF assets using existing native utilities."""

import logging
import shutil
import subprocess
from pathlib import Path

LOGGER = logging.getLogger(__name__)
RENDER_TIMEOUT_SECONDS = 60


class RenderError(RuntimeError):
    """A required renderer is missing or failed."""


def resolve_renderer(name: str, explicit: Path | None = None) -> str:
    """Resolve a supplied executable or a command on PATH."""
    candidate = shutil.which(str(explicit) if explicit is not None else name)
    if candidate is None:
        raise RenderError(f"Cannot find {name}; provide its executable path or add it to PATH.")
    return candidate


def run_renderer(arguments: list[str]) -> None:
    """Run a bounded native render without invoking a shell."""
    LOGGER.debug("Rendering with %s", arguments[0])
    try:
        subprocess.run(arguments, check=True, capture_output=True, timeout=RENDER_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as exc:
        raise RenderError(f"Renderer exceeded {RENDER_TIMEOUT_SECONDS} seconds.") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", errors="replace").strip()
        raise RenderError(f"Renderer failed with exit code {exc.returncode}: {detail}") from exc
    except OSError as exc:
        raise RenderError(f"Cannot start renderer: {exc}") from exc


def render_svg(source: Path, output: Path, dpi: int) -> None:
    """Render the actual SVG, including its physical dimensions."""
    run_renderer(
        [
            resolve_renderer("resvg"),
            "--skip-system-fonts",
            "--dpi",
            str(dpi),
            str(source),
            str(output),
        ]
    )


def render_pdf_page(source: Path, output: Path, page: int, dpi: int, renderer: str) -> None:
    """Rasterize one complete PDF page with Poppler."""
    run_renderer(
        [
            renderer,
            "-f",
            str(page),
            "-l",
            str(page),
            "-r",
            str(dpi),
            "-singlefile",
            "-png",
            str(source),
            str(output.with_suffix("")),
        ]
    )
