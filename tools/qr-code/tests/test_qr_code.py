"""Exercise the public API against real renderers and independent decoding."""

import json
import shutil
from pathlib import Path
from xml.etree import ElementTree

import pytest
from PIL import Image
from pypdf import PdfWriter
from reportlab.pdfgen.canvas import Canvas

from qr_code import QRSettings, generate_svg, verify_file
from qr_code.cli import main
from qr_code.render import render_svg

PAYLOAD = "https://example.org/meeting?city=Czestochowa&source=flyer"


@pytest.mark.parametrize("correction", ["L", "M", "Q", "H"])
def test_generated_svg_decodes_and_preserves_vector_geometry(tmp_path, correction):
    output = tmp_path / "code.svg"
    result = generate_svg(PAYLOAD, output, QRSettings(36, correction))
    assert result.verification.matched
    root = ElementTree.parse(output).getroot()
    assert root.attrib["width"] == "36mm"
    assert float(root.attrib["viewBox"].split()[-1]) == result.modules + 8
    assert len(root.findall("{http://www.w3.org/2000/svg}path")) == 1
    assert not root.findall("{http://www.w3.org/2000/svg}image")
    assert verify_file(output, PAYLOAD).matched


@pytest.mark.parametrize(
    "payload", ["Zażółć gęślą jaźń", "  exact text  ", "https://example.org/#ą"]
)
def test_payload_roundtrip_is_exact(tmp_path, payload):
    result = generate_svg(payload, tmp_path / "code.svg")
    assert result.verification.detections[0].payload == payload


@pytest.mark.parametrize("size", [0, -1, float("nan"), float("inf"), True, "30"])
def test_size_validation_applies_to_python_api(size):
    with pytest.raises(ValueError, match="Size"):
        QRSettings(size)


def test_invalid_correction_and_payload(tmp_path):
    with pytest.raises(ValueError, match="correction"):
        QRSettings(correction="invalid")
    for payload in (None, "", "   "):
        with pytest.raises(ValueError, match="Payload"):
            generate_svg(payload, tmp_path / "invalid.svg")
    with pytest.raises(ValueError, match="capacity"):
        generate_svg("x" * 10000, tmp_path / "overflow.svg")
    assert not list(tmp_path.iterdir())


def test_existing_output_is_not_modified(tmp_path):
    output = tmp_path / "code.svg"
    output.write_text("original", encoding="utf-8")
    with pytest.raises(FileExistsError):
        generate_svg(PAYLOAD, output)
    assert output.read_text() == "original"


def test_wrong_and_missing_payloads_fail_without_claiming_success(tmp_path):
    output = tmp_path / "code.svg"
    generate_svg(PAYLOAD, output)
    result = verify_file(output, PAYLOAD + "wrong")
    assert not result.matched
    assert result.detections[0].payload == PAYLOAD
    blank = tmp_path / "blank.png"
    Image.new("RGB", (200, 200), "white").save(blank)
    assert not verify_file(blank, PAYLOAD).matched


def test_raster_verification(tmp_path):
    svg = tmp_path / "code.svg"
    png = tmp_path / "code.png"
    generate_svg(PAYLOAD, svg)
    render_svg(svg, png, 150)
    assert verify_file(png, PAYLOAD).matched
    with pytest.raises(ValueError, match="only for PDF"):
        verify_file(png, PAYLOAD, page=1)
    for dpi in (0, 601, True, 150.5):
        with pytest.raises(ValueError, match="DPI"):
            verify_file(png, PAYLOAD, dpi=dpi)


def test_pdf_page_selection_and_document_wide_match(tmp_path):
    renderer = shutil.which("pdftoppm")
    if renderer is None:
        pytest.skip("Poppler is required for PDF integration.")
    svg, png, pdf = (tmp_path / name for name in ("code.svg", "code.png", "artwork.pdf"))
    generate_svg(PAYLOAD, svg)
    render_svg(svg, png, 300)
    canvas = Canvas(str(pdf), pagesize=(300, 400))
    canvas.drawString(20, 350, "First page has no QR")
    canvas.showPage()
    canvas.drawImage(str(png), 50, 200, width=102, height=102)
    canvas.save()
    assert not verify_file(pdf, PAYLOAD, page=1, pdftoppm=Path(renderer)).matched
    selected = verify_file(pdf, PAYLOAD, page=2, pdftoppm=Path(renderer))
    assert selected.matched and selected.detections[0].page == 2
    assert verify_file(pdf, PAYLOAD, pdftoppm=Path(renderer)).pages_checked == (1, 2)
    with pytest.raises(ValueError, match="outside"):
        verify_file(pdf, PAYLOAD, page=3)


def test_encrypted_pdf_is_rejected(tmp_path):
    path = tmp_path / "encrypted.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    writer.encrypt("secret", algorithm="RC4-128")
    writer.write(path)
    with pytest.raises(ValueError, match="Encrypted"):
        verify_file(path, PAYLOAD)


def test_cli_reports_match_and_nonzero_mismatch(tmp_path, capsys):
    path = tmp_path / "code.svg"
    assert main(["generate", PAYLOAD, "--output", str(path)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["verification"]["matched"]
    assert main(["verify", str(path), "--expected", "different"]) == 1
    assert not json.loads(capsys.readouterr().out)["matched"]
    assert main(["generate", PAYLOAD, "--output", str(path), "--size-mm", "nan"]) == 2


def test_missing_renderer_has_actionable_error(tmp_path, monkeypatch):
    from qr_code.render import RenderError

    monkeypatch.setattr(shutil, "which", lambda _: None)
    with pytest.raises(RenderError, match="Cannot find resvg"):
        generate_svg(PAYLOAD, tmp_path / "code.svg")
    assert not (tmp_path / "code.svg").exists()
