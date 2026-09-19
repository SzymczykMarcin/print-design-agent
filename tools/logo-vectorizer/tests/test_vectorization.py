"""Exercise real tracing, SVG-derived exports, and direct Python usage."""

import json
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

from logo_vectorizer.cli import main
from logo_vectorizer.config import OutputFormat, resolve_output_paths
from logo_vectorizer.pipeline import vectorize


def test_cli_exports_vector_master_pdf_and_faithful_preview(tmp_path):
    source = tmp_path / "ring.png"
    image = Image.new("RGBA", (96, 96), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((10, 10, 86, 86), fill=(20, 80, 160, 255))
    draw.ellipse((32, 32, 64, 64), fill=(255, 255, 255, 0))
    image.save(source)
    assert main([str(source), "--out-dir", str(tmp_path)]) == 0
    paths = resolve_output_paths(source, tmp_path)
    root = ET.parse(paths.svg).getroot()
    assert root.findall(".//{http://www.w3.org/2000/svg}path")
    assert not root.findall(".//{http://www.w3.org/2000/svg}image")
    assert paths.pdf.read_bytes().startswith(b"%PDF")
    preview = Image.open(paths.png).convert("RGBA")
    assert preview.getpixel((48, 48))[3] == 0
    assert preview.getpixel((48, 18)) == (20, 80, 160, 255)
    report = json.loads(paths.report.read_text())
    assert report["workflow"] == "vtracer-no-cleanup"
    assert report["shape_count"] == len(root.findall(".//{http://www.w3.org/2000/svg}path"))


def test_empty_input_has_a_valid_transparent_preview(tmp_path):
    source = tmp_path / "empty.png"
    Image.new("RGBA", (32, 32), (255, 255, 255, 0)).save(source)
    paths = resolve_output_paths(source, tmp_path)
    formats = {OutputFormat.PNG}
    vectorize(source, paths, formats)
    assert formats == {OutputFormat.PNG}
    assert Image.open(paths.png).convert("RGBA").getchannel("A").getbbox() is None
    assert not paths.pdf.exists()


def test_open_corel_uses_retained_master(tmp_path, monkeypatch):
    source = tmp_path / "brand.png"
    image = Image.new("RGBA", (48, 48), (255, 255, 255, 0))
    ImageDraw.Draw(image).rectangle((12, 12, 36, 36), fill=(200, 30, 40, 255))
    image.save(source)
    opened = []
    monkeypatch.setattr("logo_vectorizer.cli.open_in_corel", opened.append)
    assert main([str(source), "--out-dir", str(tmp_path), "--formats", "png", "--open-corel"]) == 0
    assert opened == [resolve_output_paths(source, tmp_path).svg]
