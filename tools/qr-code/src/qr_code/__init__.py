"""Generate vector QR assets and verify rendered artwork."""

from qr_code.generate import generate_svg
from qr_code.models import GenerationResult, QRSettings, VerificationResult
from qr_code.verify import verify_file

__all__ = ["GenerationResult", "QRSettings", "VerificationResult", "generate_svg", "verify_file"]
