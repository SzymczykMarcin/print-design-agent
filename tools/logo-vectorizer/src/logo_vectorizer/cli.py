"""Command-line interface for logo vectorization."""

from __future__ import annotations

import argparse
from pathlib import Path

from logo_vectorizer.config import parse_formats, resolve_output_paths
from logo_vectorizer.corel import open_in_corel
from logo_vectorizer.diagnostics import configure_logging, execution_stage, log_failure
from logo_vectorizer.errors import VectorizationError
from logo_vectorizer.pipeline import vectorize


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description="Vectorize raster logos into SVG, PDF, and PNG.")
    parser.add_argument("input", type=Path, help="Input raster image path.")
    parser.add_argument("--out-dir", type=Path, default=None, help="Output root directory.")
    parser.add_argument("--formats", default="svg,pdf,png", help="Comma-separated: svg,pdf,png.")
    parser.add_argument(
        "--open-corel",
        action="store_true",
        help="Open the generated SVG in CorelDRAW.",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Log stage timings, settings, and tracebacks."
    )
    parser.add_argument("--log-file", type=Path, help="Also write application logs to this file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the vectorization pipeline."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        configure_logging(debug=args.debug, log_file=args.log_file)
    except OSError as exc:
        parser.exit(1, f"error: Cannot initialize logging: {exc}\n")
    try:
        formats = parse_formats(args.formats)
    except (ValueError, TypeError) as exc:
        log_failure(str(exc), debug=args.debug)
        return 2
    input_path = args.input.resolve()
    paths = resolve_output_paths(input_path, args.out_dir)
    try:
        vectorize(input_path, paths, formats)
        if args.open_corel:
            with execution_stage("Open SVG in CorelDRAW"):
                open_in_corel(paths.svg)
    except VectorizationError as exc:
        log_failure(str(exc), debug=args.debug)
        return 1
    print(f"Vectorization complete: {paths.directory}")
    return 0
