"""Validated inputs and immutable operation results."""

from dataclasses import dataclass
from math import isfinite
from pathlib import Path

DEFAULT_SIZE_MM = 30.0
DEFAULT_DPI = 300
MIN_DPI = 72
MAX_DPI = 600
QUIET_ZONE_MODULES = 4


def validate_payload(payload: str) -> None:
    """Require content without changing the encoded value."""
    if not isinstance(payload, str) or not payload.strip():
        raise ValueError("Payload must be a non-empty string.")


def validate_dpi(dpi: int) -> None:
    """Bound render resolution for predictable verification costs."""
    if type(dpi) is not int or not MIN_DPI <= dpi <= MAX_DPI:
        raise ValueError(f"DPI must be an integer between {MIN_DPI} and {MAX_DPI}.")


@dataclass(frozen=True)
class QRSettings:
    """Describe physical size including the fixed quiet zone."""

    size_mm: float = DEFAULT_SIZE_MM
    correction: str = "M"

    def __post_init__(self) -> None:
        if (
            isinstance(self.size_mm, bool)
            or not isinstance(self.size_mm, (int, float))
            or not isfinite(self.size_mm)
            or self.size_mm <= 0
        ):
            raise ValueError("Size in millimeters must be finite and positive.")
        if self.correction not in ("L", "M", "Q", "H"):
            raise ValueError("Error correction must be L, M, Q or H.")


@dataclass(frozen=True)
class Detection:
    """Describe one decoded QR and its one-based PDF page, if applicable."""

    payload: str
    page: int | None = None


@dataclass(frozen=True)
class VerificationResult:
    """Report exact matches without hiding other decoded QR codes."""

    expected: str
    detections: tuple[Detection, ...]
    pages_checked: tuple[int, ...] = ()

    @property
    def matched(self) -> bool:
        return any(item.payload == self.expected for item in self.detections)


@dataclass(frozen=True)
class GenerationResult:
    """Record the saved vector asset and its successful rendered round trip."""

    output: Path
    modules: int
    size_mm: float
    module_mm: float
    correction: str
    verification: VerificationResult
