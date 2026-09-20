"""Package the source and measure the one-page print candidate without releasing it."""

import argparse
import base64
import hashlib
import io
import json
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image, ImageCms
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    ContentStream,
    DictionaryObject,
    NameObject,
    RectangleObject,
    TextStringObject,
)

PROJECT = Path(__file__).resolve().parents[1]
NAME = "flyer-a5-front-v02"
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
POINTS_PER_MM = 72 / 25.4


def digest(data):
    """Identify the exact inspected bytes."""
    return hashlib.sha256(data).hexdigest()


def run(*arguments):
    """Run a checked native conversion or inspection."""
    return subprocess.run(
        list(map(str, arguments)), check=True, capture_output=True, text=True
    ).stdout


def package_svg():
    """Embed the untouched photo after checking Corel's decoded export against it."""
    path = PROJECT / "working" / f"{NAME}.svg"
    tree = ET.parse(path)
    source_path = PROJECT / "inputs/photos/ice-cream-moment.jpg"
    source = np.asarray(Image.open(source_path).convert("RGB"), dtype=np.int16)
    for node in tree.findall(f".//{{{SVG}}}image"):
        href = node.get(f"{{{XLINK}}}href")
        if href.startswith("data:"):
            continue
        linked = path.parent / href.replace("\\", "/")
        exported = np.asarray(Image.open(linked).convert("RGB"), dtype=np.int16)
        assert exported.shape == source.shape
        assert np.abs(source - exported).mean() < 0.25, (
            "Export differs materially from the original photo."
        )
        node.set(
            f"{{{XLINK}}}href",
            "data:image/jpeg;base64," + base64.b64encode(source_path.read_bytes()).decode(),
        )
        linked.unlink()
        if not any(linked.parent.iterdir()):
            linked.parent.rmdir()
    assert not tree.findall(f".//{{{SVG}}}text")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def declare_print_geometry(path):
    """Declare existing trim/bleed and the actual CMYK output profile."""
    reader = PdfReader(io.BytesIO(path.read_bytes()))
    writer = PdfWriter(clone_from=reader)
    writer.pdf_header = reader.pdf_header
    page = writer.pages[0]
    bleed = 2 * POINTS_PER_MM
    page.trimbox = RectangleObject([bleed, bleed, 150 * POINTS_PER_MM, 212 * POINTS_PER_MM])
    page.bleedbox = RectangleObject(page.mediabox)
    page.cropbox = RectangleObject(page.mediabox)
    profile = page["/Resources"]["/ColorSpace"]["/DefaultCMYK"].get_object()[1]
    intent = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/OutputIntent"),
            NameObject("/S"): NameObject("/GTS_PDFX"),
            NameObject("/OutputConditionIdentifier"): TextStringObject("FOGRA39"),
            NameObject("/Info"): TextStringObject("ISO Coated v2 (ECI)"),
            NameObject("/RegistryName"): TextStringObject("http://www.color.org"),
            NameObject("/DestOutputProfile"): profile,
        }
    )
    writer.root_object[NameObject("/OutputIntents")] = ArrayObject([writer._add_object(intent)])
    with path.open("wb") as stream:
        writer.write(stream)


def color_space(value):
    """Describe a concrete color space and fingerprint embedded ICC data."""
    value = value.get_object() if hasattr(value, "get_object") else value
    if isinstance(value, list) and value[0] == "/ICCBased":
        profile = value[1].get_object()
        data = profile.get_data()
        return {
            "type": "ICCBased",
            "components": int(profile["/N"]),
            "profile": ImageCms.getProfileDescription(
                ImageCms.ImageCmsProfile(io.BytesIO(data))
            ).strip(),
            "sha256": digest(data),
        }
    return str(value)


def inspect_stream(reader, stream, resources, matrix=None):
    """Follow nested graphics state and record every raster, paint and text operation."""
    matrix = np.eye(3) if matrix is None else matrix.copy()
    stack = []
    evidence = {
        "text_operators": 0,
        "path_paints": 0,
        "rgb_operators": 0,
        "images": [],
        "vector_cmyk_max_percent": 0,
        "color_spaces": {},
        "graphics_states": [],
        "shadings": len(resources.get("/Shading", {})),
        "patterns": len(resources.get("/Pattern", {})),
    }
    for key, value in resources.get("/ColorSpace", {}).items():
        evidence["color_spaces"][str(key)] = color_space(value)
    for state in resources.get("/ExtGState", {}).values():
        obj = state.get_object()
        evidence["graphics_states"].append({str(k): str(v) for k, v in obj.items()})
    for operands, operator in ContentStream(stream, reader).operations:
        evidence["text_operators"] += operator in (b"Tj", b"TJ", b"'", b'"')
        evidence["path_paints"] += operator in (b"f", b"f*", b"B", b"B*", b"S", b"s")
        evidence["rgb_operators"] += operator in (b"rg", b"RG")
        if operator in (b"k", b"K", b"scn", b"SCN") and len(operands) == 4:
            evidence["vector_cmyk_max_percent"] = max(
                evidence["vector_cmyk_max_percent"], sum(map(float, operands)) * 100
            )
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
                width, height = int(obj["/Width"]), int(obj["/Height"])
                space = color_space(obj["/ColorSpace"])
                assert space["components"] == 4
                pixels = np.frombuffer(obj.get_data(), np.uint8).reshape(height, width, 4)
                evidence["images"].append(
                    {
                        "pixels": [width, height],
                        "ppi": [
                            width * 72 / float(np.linalg.norm(matrix[:2, 0])),
                            height * 72 / float(np.linalg.norm(matrix[:2, 1])),
                        ],
                        "color_space": space,
                        "max_ink_percent": float(pixels.astype(np.uint16).sum(2).max()) * 100 / 255,
                        "soft_mask": str(obj.get("/SMask")),
                        "filter": str(obj.get("/Filter")),
                    }
                )
            elif obj.get("/Subtype") == "/Form":
                a, b, c, d, e, f = map(float, obj.get("/Matrix", [1, 0, 0, 1, 0, 0]))
                nested = inspect_stream(
                    reader,
                    obj,
                    obj.get("/Resources", resources),
                    matrix @ np.array([[a, c, e], [b, d, f], [0, 0, 1]]),
                )
                for key in (
                    "text_operators",
                    "path_paints",
                    "rgb_operators",
                    "shadings",
                    "patterns",
                ):
                    evidence[key] += nested[key]
                evidence["images"] += nested["images"]
                evidence["graphics_states"] += nested["graphics_states"]
                evidence["color_spaces"].update(nested["color_spaces"])
                evidence["vector_cmyk_max_percent"] = max(
                    evidence["vector_cmyk_max_percent"], nested["vector_cmyk_max_percent"]
                )
    return evidence


def main():
    """Write auditable measurements and renders; release still requires visual review."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--poppler-bin", type=Path, required=True)
    parser.add_argument("--ghostscript", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    package_svg()
    pdf = PROJECT / "working/print-candidates" / f"{NAME}.pdf"
    declare_print_geometry(pdf)
    reader = PdfReader(pdf, strict=True)
    page = reader.pages[0]
    measured = inspect_stream(reader, page.get_contents(), page["/Resources"])
    measured.update(
        {
            "sha256": digest(pdf.read_bytes()),
            "bytes": pdf.stat().st_size,
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
            "annotations": len(page.get("/Annots", [])),
            "forms": bool(reader.trailer["/Root"].get("/AcroForm")),
            "embedded_files": bool(reader.trailer["/Root"].get("/Names", {}).get("/EmbeddedFiles")),
            "media_mm": [float(v) / POINTS_PER_MM for v in page.mediabox],
            "trim_mm": [float(v) / POINTS_PER_MM for v in page.trimbox],
            "bleed_mm": [float(v) / POINTS_PER_MM for v in page.bleedbox],
            "rotation": page.get("/Rotate", 0),
            "user_unit": page.get("/UserUnit", 1),
            "output_profile": color_space(
                ["/ICCBased", reader.trailer["/Root"]["/OutputIntents"][0]["/DestOutputProfile"]]
            ),
            "pdfinfo": run(args.poppler_bin / "pdfinfo.exe", "-box", pdf),
        }
    )
    for name in ("before-outline", "outlined-rgb"):
        run(
            args.poppler_bin / "pdftoppm.exe",
            "-r",
            "150",
            "-png",
            "-singlefile",
            PROJECT / "working" / f"{name}.pdf",
            args.scratch / name,
        )
    before = np.asarray(Image.open(args.scratch / "before-outline.png"), dtype=np.int16)
    after = np.asarray(Image.open(args.scratch / "outlined-rgb.png"), dtype=np.int16)
    measured["outlining"] = {
        "mean_channel_difference": float(np.abs(before - after).mean()),
        "changed_pixel_fraction": float(np.any(before != after, axis=2).mean()),
    }
    run(
        args.poppler_bin / "pdftoppm.exe",
        "-r",
        "254",
        "-png",
        "-singlefile",
        pdf,
        PROJECT / "previews" / f"{NAME}-bleed",
    )
    Image.open(PROJECT / "previews" / f"{NAME}-bleed.png").crop((20, 20, 1500, 2120)).save(
        PROJECT / "previews" / f"{NAME}.png"
    )
    separation = args.scratch / "process-cmyk.tif"
    run(
        args.ghostscript,
        "-q",
        "-dSAFER",
        "-dBATCH",
        "-dNOPAUSE",
        "-sDEVICE=tiff32nc",
        "-r600",
        "-sOutputICCProfile=" + str(args.profile),
        "-sOutputFile=" + str(separation),
        pdf,
    )
    with Image.open(separation) as image:
        assert image.mode == "CMYK"
        inks = np.asarray(image, dtype=np.uint16)
        measured["separation"] = {
            "resolution_ppi": 600,
            "max_local_ink_percent": float(inks.sum(2).max()) * 100 / 255,
            "profile_sha256": digest(args.profile.read_bytes()),
            "ghostscript_version": run(args.ghostscript, "--version").strip(),
            "overprint_flags": [s for s in measured["graphics_states"] if "/op" in s or "/OP" in s],
        }
        del inks
    type_bounds = json.loads(
        (PROJECT / "reports/typography-v02.json").read_text(encoding="utf-8-sig")
    )
    measured["minimum_type_distance_inside_trim_mm"] = min(
        min(b["Left"] - 2, 150 - b["Left"] - b["Width"], 212 - b["Top"], b["Top"] - b["Height"] - 2)
        for b in type_bounds
    )
    (PROJECT / "reports/measured-evidence-v02.json").write_text(
        json.dumps(measured, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {k: v for k, v in measured.items() if k not in ("pdfinfo", "graphics_states")}, indent=2
        )
    )
    assert len(reader.pages) == 1 and not reader.is_encrypted
    assert measured["text_operators"] == 0 and measured["path_paints"] > 100
    assert measured["rgb_operators"] == 0
    assert all(min(im["ppi"]) >= 300 for im in measured["images"])
    assert (
        max(measured["vector_cmyk_max_percent"], measured["separation"]["max_local_ink_percent"])
        <= 330
    )
    assert measured["output_profile"]["sha256"] == digest(args.profile.read_bytes())


if __name__ == "__main__":
    main()
