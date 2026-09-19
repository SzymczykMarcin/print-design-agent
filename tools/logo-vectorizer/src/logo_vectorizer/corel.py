"""CorelDRAW integration helpers."""

from __future__ import annotations

import subprocess
from pathlib import Path

DEFAULT_COREL_PATH = Path(
    r"C:\Program Files\Corel\CorelDRAW Graphics Suite\25\Programs64\CorelDRW.exe"
)


def open_in_corel(svg_path: Path, corel_path: Path = DEFAULT_COREL_PATH) -> None:
    """Open the generated SVG in CorelDRAW."""

    if not corel_path.exists():
        raise FileNotFoundError(f"CorelDRAW executable was not found: {corel_path}")
    subprocess.Popen([str(corel_path), str(svg_path)])
