"""Package SVG images, render delivery files and record measured PDF evidence."""

import argparse
import base64
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image, ImageChops, ImageCms, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, RectangleObject

PROJECT = Path(__file__).resolve().parents[1]
NAMES = ("flyer-a5-front-v01", "social-feed-v01", "social-story-v01")
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"


def run(binary, *arguments):
    """Run a native inspection tool and retain its diagnostic output."""
    return subprocess.run(
        [str(binary), *map(str, arguments)], check=True, capture_output=True, text=True
    ).stdout


def package_svg(name):
    """Embed the exported image without changing its rendered pixels."""
    path = PROJECT / "working" / f"{name}.svg"
    tree = ET.parse(path)
    for image in tree.findall(f".//{{{SVG}}}image"):
        source = image.get(f"{{{XLINK}}}href")
        if not source or source.startswith("data:"):
            continue
        linked = path.parent / source.replace("\\", "/")
        with Image.open(linked) as original:
            original.verify()
        crop = PROJECT / "assets" / f"{name}-photo.jpg"
        with Image.open(linked) as exported, Image.open(crop) as source:
            difference = np.abs(
                np.asarray(exported.convert("RGB"), dtype=float)
                - np.asarray(source.convert("RGB"), dtype=float)
            )
            if difference.mean() > 0.01:
                raise ValueError("The exported photo differs from its original crop.")
        image.set(
            f"{{{XLINK}}}href",
            "data:image/jpeg;base64," + base64.b64encode(crop.read_bytes()).decode(),
        )
        linked.unlink()
        linked.parent.rmdir()
    assert not tree.findall(f".//{{{SVG}}}text")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def add_print_boxes(path):
    """Declare the exercise's trim and actual existing bleed without scaling content."""
    reader = PdfReader(path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.pdf_header = reader.pdf_header
    page = writer.pages[0]
    bleed = 3 * 72 / 25.4
    page.trimbox = RectangleObject(
        [bleed, bleed, float(page.mediabox.width) - bleed, float(page.mediabox.height) - bleed]
    )
    page.bleedbox = RectangleObject(page.mediabox)
    page.cropbox = RectangleObject(page.mediabox)
    with path.open("wb") as stream:
        writer.write(stream)


def inspect_stream(reader, stream, resources, seen=None):
    """Count text and path operators recursively through nested forms."""
    seen = set() if seen is None else seen
    counts = {
        "text_show_operators": 0,
        "path_paint_operators": 0,
        "rgb_operators": 0,
        "cmyk_operators": 0,
    }
    for _, operator in ContentStream(stream, reader).operations:
        counts["text_show_operators"] += operator in (b"Tj", b"TJ", b"'", b'"')
        counts["path_paint_operators"] += operator in (b"f", b"f*", b"B", b"B*", b"S")
        counts["rgb_operators"] += operator in (b"rg", b"RG")
        counts["cmyk_operators"] += operator in (b"k", b"K")
    for reference in resources.get("/XObject", {}).values():
        obj = reference.get_object()
        if obj.get("/Subtype") != "/Form" or id(obj) in seen:
            continue
        seen.add(id(obj))
        nested = inspect_stream(reader, obj, obj.get("/Resources", resources), seen)
        for key, value in nested.items():
            counts[key] += value
    return counts


def describe_color_space(value):
    """Describe embedded ICC profiles without process-specific object addresses."""
    if isinstance(value, list) and value[0] == "/ICCBased":
        profile = value[1].get_object()
        return {
            "type": "ICCBased",
            "components": int(profile["/N"]),
            "profile_sha256": hashlib.sha256(profile.get_data()).hexdigest(),
        }
    return str(value)


def image_placements(reader, stream, resources, matrix=None):
    """Measure each raster placement through saved transforms and nested forms."""
    matrix = np.eye(3) if matrix is None else matrix.copy()
    stack, images = [], []
    for operands, operator in ContentStream(stream, reader).operations:
        if operator == b"q":
            stack.append(matrix.copy())
        elif operator == b"Q":
            matrix = stack.pop()
        elif operator == b"cm":
            a, b, c, d, e, f = map(float, operands)
            matrix = matrix @ np.array([[a, c, e], [b, d, f], [0, 0, 1]])
        elif operator == b"Do":
            obj = resources["/XObject"][operands[0]].get_object()
            if obj.get("/Subtype") == "/Image":
                width_pt = float(np.linalg.norm(matrix[:2, 0]))
                height_pt = float(np.linalg.norm(matrix[:2, 1]))
                images.append(
                    {
                        "pixels": [int(obj["/Width"]), int(obj["/Height"])],
                        "ppi": [
                            float(obj["/Width"]) * 72 / width_pt,
                            float(obj["/Height"]) * 72 / height_pt,
                        ],
                        "color_space": describe_color_space(obj.get("/ColorSpace")),
                    }
                )
            elif obj.get("/Subtype") == "/Form":
                a, b, c, d, e, f = map(float, obj.get("/Matrix", [1, 0, 0, 1, 0, 0]))
                nested_matrix = matrix @ np.array([[a, c, e], [b, d, f], [0, 0, 1]])
                images.extend(
                    image_placements(reader, obj, obj.get("/Resources", resources), nested_matrix)
                )
    return images


def render(poppler, pdf, target, width=None, height=None):
    """Render the actual PDF to PNG with an explicit target size."""
    arguments = ["-png", "-singlefile"]
    arguments += ["-scale-to-x", str(width), "-scale-to-y", str(height)] if width else ["-r", "100"]
    run(poppler / "pdftoppm.exe", *arguments, pdf, target.with_suffix(""))


def main():
    """Prepare deliverables and evidence after the CorelDRAW build has completed."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--poppler-bin", type=Path, required=True)
    args = parser.parse_args()
    poppler = args.poppler_bin
    evidence = {"outline_comparison": {}, "pdfs": {}}
    for name in NAMES:
        package_svg(name)
        pdf = (
            PROJECT / ("exports/print" if name.startswith("flyer") else "previews") / f"{name}.pdf"
        )
        before = PROJECT / "reports" / f"{name}-before-outline.pdf"
        with tempfile.TemporaryDirectory(prefix="outline-comparison-") as directory:
            previous, current = Path(directory) / "before.png", Path(directory) / "after.png"
            render(poppler, before, previous)
            render(poppler, pdf, current)
            with Image.open(previous) as first, Image.open(current) as second:
                assert first.size == second.size
                difference = np.asarray(
                    ImageChops.difference(first.convert("RGB"), second.convert("RGB"))
                )
                evidence["outline_comparison"][name] = {
                    "mean_channel_difference_0_255": float(difference.mean()),
                    "changed_pixel_fraction": float(np.any(difference > 0, axis=2).mean()),
                }
        if name.startswith("flyer"):
            add_print_boxes(pdf)
            full = PROJECT / "previews" / f"{name}-bleed.png"
            render(poppler, pdf, full, 1540, 2160)
            with Image.open(full) as image:
                image.crop((30, 30, 1510, 2130)).save(PROJECT / "previews" / f"{name}.png")
        else:
            height = 1350 if "feed" in name else 1920
            destination = PROJECT / "exports/social" / f"{name}.png"
            render(poppler, pdf, destination, 1080, height)
            with Image.open(destination) as image:
                profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
                image.save(destination, icc_profile=profile)
        reader = PdfReader(pdf)
        page = reader.pages[0]
        evidence["pdfs"][name] = {
            "file": pdf.relative_to(PROJECT).as_posix(),
            "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "bytes": pdf.stat().st_size,
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
            "media_mm": [float(x) * 25.4 / 72 for x in page.mediabox],
            "trim_mm": [float(x) * 25.4 / 72 for x in page.trimbox],
            "annotations": len(page.get("/Annots", [])),
            "operators": inspect_stream(reader, page.get_contents(), page["/Resources"]),
            "output_intents": len(reader.trailer["/Root"].get("/OutputIntents", [])),
            "images": image_placements(reader, page.get_contents(), page["/Resources"]),
            "page_font_resources": list(page["/Resources"].get("/Font", {})),
            "color_spaces": {
                str(key): describe_color_space(value.get_object())
                for key, value in page["/Resources"].get("/ColorSpace", {}).items()
            },
            "pdfinfo": run(poppler / "pdfinfo.exe", "-box", pdf),
        }
        assert evidence["pdfs"][name]["operators"]["text_show_operators"] == 0
    for name in NAMES:
        (PROJECT / "reports" / f"{name}-before-outline.pdf").unlink()
    for path in (PROJECT / "working").glob("Backup_of_*.cdr"):
        path.unlink()
    for folder in ("assets", "working", "previews", "exports/print", "exports/social", "reports"):
        (PROJECT / folder / ".gitkeep").unlink(missing_ok=True)
    evidence["poppler_version"] = subprocess.run(
        [str(poppler / "pdfinfo.exe"), "-v"], capture_output=True, text=True
    ).stderr.strip()
    (PROJECT / "reports/measured-evidence-v01.json").write_text(
        json.dumps(evidence, indent=2), encoding="utf-8"
    )
    sheet = Image.new("RGB", (1500, 1020), "#eee8df")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(PROJECT / "inputs/fonts/Lato-Bold.ttf"), 25)
    paths = [
        PROJECT / "previews/flyer-a5-front-v01.png",
        PROJECT / "exports/social/social-feed-v01.png",
        PROJECT / "exports/social/social-story-v01.png",
    ]
    for index, (path, label) in enumerate(
        zip(paths, ("A5 FLYER", "SOCIAL FEED", "SOCIAL STORY"), strict=True)
    ):
        with Image.open(path) as image:
            image.thumbnail((450, 900))
            x = index * 500 + (500 - image.width) // 2
            sheet.paste(image, (x, 75))
        draw.text((index * 500 + 25, 25), label, font=font, fill="#49281E")
    sheet.save(PROJECT / "previews/overview-v01.jpg", quality=92)
    print(json.dumps(evidence["outline_comparison"], indent=2))


if __name__ == "__main__":
    main()
