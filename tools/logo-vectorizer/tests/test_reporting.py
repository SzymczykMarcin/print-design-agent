"""Regression checks for report compatibility and data ownership."""

import json
from pathlib import Path

from logo_vectorizer.config import OutputFormat, resolve_output_paths
from logo_vectorizer.reporting import SvgStatistics, build_report, write_report


def test_report_retains_json_contract_and_detaches_inputs(tmp_path: Path) -> None:
    source = Path("brand.png")
    paths = resolve_output_paths(source, tmp_path)
    warnings = ["Review colors."]
    formats = {OutputFormat.PNG}
    report = build_report(
        source=source,
        paths=paths,
        formats=formats,
        warnings=tuple(warnings),
        statistics=SvgStatistics("96", "64", 2, 3),
    )
    warnings.append("Later warning.")
    formats.add(OutputFormat.PDF)
    destination = tmp_path / "report.json"
    write_report(report, destination)
    assert json.loads(destination.read_text(encoding="utf-8")) == {
        "source": "brand.png",
        "engine": "vtracer",
        "width": "96",
        "height": "64",
        "shape_count": 2,
        "contour_count": 3,
        "workflow": "vtracer-no-cleanup",
        "formats": ["png", "svg"],
        "outputs": {"svg": str(paths.svg), "png": str(paths.png)},
        "warnings": ["Review colors."],
    }
