"""Read SVG statistics and serialize explicitly typed vectorization reports."""

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

from logo_vectorizer.config import OutputFormat, OutputPaths


@dataclass(frozen=True)
class SvgStatistics:
    """Describe SVG dimensions verbatim and count path elements and subpaths."""

    width: str | None
    height: str | None
    shape_count: int
    contour_count: int


class ReportOutputs(TypedDict):
    """List delivered files, including the always-retained SVG master."""

    svg: str
    pdf: NotRequired[str]
    png: NotRequired[str]


class VectorizationReport(TypedDict):
    """Describe files and geometry produced by the fixed workflow."""

    source: str
    engine: str
    width: str | None
    height: str | None
    shape_count: int
    contour_count: int
    workflow: Literal["vtracer-no-cleanup"]
    formats: list[str]
    outputs: ReportOutputs
    warnings: list[str]


def read_svg_statistics(path: Path) -> SvgStatistics:
    """Read dimensions and path counts from the delivered SVG."""
    root = ET.parse(path).getroot()
    svg_paths = root.findall(".//{http://www.w3.org/2000/svg}path")
    return SvgStatistics(
        width=root.get("width"),
        height=root.get("height"),
        shape_count=len(svg_paths),
        contour_count=sum(len(re.findall(r"[Mm]", path.get("d", ""))) for path in svg_paths),
    )


def build_report(
    *,
    source: Path,
    paths: OutputPaths,
    formats: set[OutputFormat],
    warnings: tuple[str, ...],
    statistics: SvgStatistics,
) -> VectorizationReport:
    """Build a detached report snapshot without filesystem access."""
    outputs: ReportOutputs = {"svg": str(paths.svg)}
    if OutputFormat.PDF in formats:
        outputs["pdf"] = str(paths.pdf)
    if OutputFormat.PNG in formats:
        outputs["png"] = str(paths.png)
    return VectorizationReport(
        source=str(source),
        engine="vtracer",
        width=statistics.width,
        height=statistics.height,
        shape_count=statistics.shape_count,
        contour_count=statistics.contour_count,
        workflow="vtracer-no-cleanup",
        formats=sorted(outputs),
        outputs=outputs,
        warnings=list(warnings),
    )


def write_report(report: VectorizationReport, destination: Path) -> None:
    """Serialize a report snapshot as UTF-8 JSON."""
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
