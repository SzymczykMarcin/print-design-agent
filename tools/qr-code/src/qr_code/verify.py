"""Decode QR codes from actual assets and rendered PDF pages."""

from pathlib import Path
from tempfile import TemporaryDirectory

import zxingcpp
from PIL import Image, ImageOps
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from qr_code.models import (
    DEFAULT_DPI,
    Detection,
    VerificationResult,
    validate_dpi,
    validate_payload,
)
from qr_code.render import render_pdf_page, render_svg, resolve_renderer


def decode_image(path: Path, page: int | None = None) -> tuple[Detection, ...]:
    """Decode only QR codes, compositing transparent images onto white."""
    with Image.open(path) as source:
        oriented = ImageOps.exif_transpose(source).convert("RGBA")
        background = Image.new("RGBA", oriented.size, "white")
        image = Image.alpha_composite(background, oriented).convert("RGB")
        results = zxingcpp.read_barcodes(image, formats=zxingcpp.BarcodeFormat.QRCode)
    return tuple(Detection(item.text, page) for item in results if item.valid)


def pdf_page_numbers(path: Path, page: int | None) -> tuple[int, ...]:
    """Validate the PDF and select all pages or one explicit page."""
    with path.open("rb") as stream:
        reader = PdfReader(stream)
        if reader.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported; supply an unencrypted copy.")
        count = len(reader.pages)
    if not count:
        raise ValueError("PDF contains no pages.")
    if page is not None and page > count:
        raise ValueError(f"Page {page} is outside the PDF's {count} pages.")
    return (page,) if page is not None else tuple(range(1, count + 1))


def verify_file(
    source: Path,
    expected: str,
    *,
    page: int | None = None,
    dpi: int = DEFAULT_DPI,
    pdftoppm: Path | None = None,
) -> VerificationResult:
    """Find an exact payload match without fetching or normalizing its contents."""
    validate_payload(expected)
    validate_dpi(dpi)
    if page is not None and (type(page) is not int or page < 1):
        raise ValueError("Page must be a positive one-based integer.")
    source = Path(source).resolve(strict=True)
    if not source.is_file():
        raise ValueError("Input must be a file.")
    suffix = source.suffix.lower()
    if page is not None and suffix != ".pdf":
        raise ValueError("Page selection is supported only for PDF inputs.")
    with TemporaryDirectory(prefix="qr-verify-") as temporary:
        raster = Path(temporary) / "page.png"
        if suffix == ".svg":
            render_svg(source, raster, dpi)
            return VerificationResult(expected, decode_image(raster))
        if suffix != ".pdf":
            return VerificationResult(expected, decode_image(source))
        try:
            pages = pdf_page_numbers(source, page)
        except PdfReadError as exc:
            raise ValueError(f"Cannot read PDF: {exc}") from exc
        renderer = resolve_renderer("pdftoppm", pdftoppm)
        detections = []
        for number in pages:
            render_pdf_page(source, raster, number, dpi, renderer)
            detections.extend(decode_image(raster, number))
        return VerificationResult(expected, tuple(detections), pages)
