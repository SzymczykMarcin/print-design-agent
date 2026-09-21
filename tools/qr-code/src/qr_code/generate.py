"""Build standalone vector QR assets with a verified rendered payload."""

from pathlib import Path
from tempfile import TemporaryDirectory

from reportlab.graphics.barcode import qrencoder

from qr_code.models import QUIET_ZONE_MODULES, GenerationResult, QRSettings, validate_payload
from qr_code.verify import verify_file


def encode_matrix(payload: str, correction: str) -> tuple[tuple[bool, ...], ...]:
    """Encode UTF-8 content using automatic QR version selection."""
    qr = qrencoder.QRCode(None, getattr(qrencoder.QRErrorCorrectLevel, correction))
    try:
        qr.addData(payload)
        qr.make()
    except Exception as exc:
        if not str(exc).startswith("code length overflow"):
            raise
        raise ValueError("Payload exceeds the supported QR capacity.") from exc
    width = qr.getModuleCount()
    return tuple(tuple(qr.isDark(row, column) for column in range(width)) for row in range(width))


def build_svg(matrix: tuple[tuple[bool, ...], ...], size_mm: float) -> str:
    """Draw black vector modules on an opaque white four-module quiet zone."""
    extent = len(matrix) + 2 * QUIET_ZONE_MODULES
    commands = "".join(
        f"M{column + QUIET_ZONE_MODULES},{row + QUIET_ZONE_MODULES}h1v1h-1z"
        for row, cells in enumerate(matrix)
        for column, dark in enumerate(cells)
        if dark
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size_mm:g}mm" height="{size_mm:g}mm" viewBox="0 0 {extent} {extent}">'
        f'<rect id="qr-background" width="{extent}" height="{extent}" fill="#fff"/>'
        f'<path id="qr-modules" fill="#000" d="{commands}"/></svg>\n'
    )


def generate_svg(
    payload: str, output: Path, settings: QRSettings | None = None
) -> GenerationResult:
    """Verify the rendered SVG before saving a new file without overwriting."""
    validate_payload(payload)
    settings = settings if settings is not None else QRSettings()
    if not isinstance(settings, QRSettings):
        raise TypeError("Settings must be a QRSettings instance.")
    output = Path(output).absolute()
    if output.suffix.lower() != ".svg":
        raise ValueError("Output must have an .svg extension.")
    if output.exists():
        raise FileExistsError(f"Output already exists: {output}")
    matrix = encode_matrix(payload, settings.correction)
    svg = build_svg(matrix, settings.size_mm)
    with TemporaryDirectory(prefix="qr-generate-") as temporary:
        candidate = Path(temporary) / "candidate.svg"
        candidate.write_text(svg, encoding="utf-8")
        verification = verify_file(candidate, payload)
    if not verification.matched:
        raise ValueError(
            "Rendered QR did not decode exactly; try a larger size or shorter payload."
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(svg)
    return GenerationResult(
        output,
        len(matrix),
        settings.size_mm,
        settings.size_mm / (len(matrix) + 2 * QUIET_ZONE_MODULES),
        settings.correction,
        verification,
    )
