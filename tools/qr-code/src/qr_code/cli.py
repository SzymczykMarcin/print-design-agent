"""Expose generation and exact-payload verification as JSON-producing commands."""

import argparse
import json
import logging
from dataclasses import asdict
from pathlib import Path

from qr_code.generate import generate_svg
from qr_code.models import DEFAULT_DPI, DEFAULT_SIZE_MM, QRSettings
from qr_code.render import RenderError
from qr_code.verify import verify_file


def build_parser() -> argparse.ArgumentParser:
    """Define the two focused operations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--debug", action="store_true", help="Include diagnostic tracebacks.")
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate", help="Create and verify a new vector SVG.")
    generate.add_argument("payload")
    generate.add_argument("--output", type=Path, required=True)
    generate.add_argument("--size-mm", type=float, default=DEFAULT_SIZE_MM)
    generate.add_argument("--correction", choices=("L", "M", "Q", "H"), default="M")
    verify = commands.add_parser("verify", help="Read QR codes from an image, SVG or PDF.")
    verify.add_argument("input", type=Path)
    verify.add_argument("--expected", required=True)
    verify.add_argument("--page", type=int, help="One-based PDF page; omitted scans all pages.")
    verify.add_argument(
        "--dpi", type=int, default=DEFAULT_DPI, help="SVG/PDF rendering resolution."
    )
    verify.add_argument("--pdftoppm", type=Path, help="Poppler executable; otherwise use PATH.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Return zero for a match, one for failure, or two for invalid input."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    try:
        if args.command == "generate":
            result = generate_svg(
                args.payload, args.output, QRSettings(args.size_mm, args.correction)
            )
            report = asdict(result)
            report["verification"]["matched"] = result.verification.matched
            matched = result.verification.matched
        else:
            result = verify_file(
                args.input, args.expected, page=args.page, dpi=args.dpi, pdftoppm=args.pdftoppm
            )
            matched = result.matched
            report = {**asdict(result), "matched": matched}
    except (ValueError, TypeError) as exc:
        logging.getLogger(__name__).error("%s", exc, exc_info=args.debug)
        return 2
    except (OSError, RenderError) as exc:
        logging.getLogger(__name__).error("%s", exc, exc_info=args.debug)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return 0 if matched else 1
