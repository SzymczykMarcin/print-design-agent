"""Rebuild the fictional demo using Pillow and CorelDRAW's native text outlining."""

import argparse
import base64
import subprocess
import tempfile
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
CREAM = "#FFF6EC"
COCOA = "#49281E"
PINK = "#DF858D"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)


def element(parent, tag, **attributes):
    """Append a namespaced SVG element with explicit attributes."""
    return ET.SubElement(
        parent,
        f"{{{SVG}}}{tag}",
        {key.replace("_", "-"): str(value) for key, value in attributes.items()},
    )


def text(parent, role, lines, x, y, size, leading, bold=False):
    """Typeset named text blocks for native conversion to curves in CorelDRAW."""
    group = element(parent, "g", id=role)
    for index, line in enumerate(lines):
        node = element(
            group,
            "text",
            x=x,
            y=y + index * leading,
            fill=COCOA,
            font_family="Lato",
            font_size=size,
            font_weight="700" if bold else "400",
        )
        node.text = line


def place_logo(parent, x, y, width):
    """Place the original paths with only their transparent outside margin trimmed."""
    logo = ET.parse(PROJECT / "inputs/logos/lodziarnia.svg").getroot()
    container = element(
        parent,
        "svg",
        id="original-logo",
        x=x,
        y=y,
        width=width,
        height=width,
        viewBox="140 135 1000 1000",
    )
    for child in logo:
        container.append(deepcopy(child))


def photo(parent, name, crop, x, y, width, height):
    """Save a full-resolution crop and embed it as a separate photograph object."""
    path = PROJECT / "assets" / f"{name}-photo.jpg"
    with Image.open(PROJECT / "inputs/photos/ice-cream-moment.jpg") as original:
        original.crop(crop).save(path, quality=96, subsampling=0)
    node = element(parent, "image", id="hero-photo", x=x, y=y, width=width, height=height)
    node.set(
        f"{{{XLINK}}}href", "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()
    )


def compose(name):
    """Compose one format independently while preserving brand and exact copy."""
    if name == "flyer-a5-front-v01":
        width, height = 154, 216
        root = ET.Element(f"{{{SVG}}}svg", width="154mm", height="216mm", viewBox="0 0 154 216")
    elif name == "social-feed-v01":
        width, height = 1080, 1350
        root = ET.Element(f"{{{SVG}}}svg", width="1080px", height="1350px", viewBox="0 0 1080 1350")
    else:
        width, height = 1080, 1920
        root = ET.Element(f"{{{SVG}}}svg", width="1080px", height="1920px", viewBox="0 0 1080 1920")
    element(root, "rect", id="cream-background", width=width, height=height, fill=CREAM)
    if width == 154:
        photo(root, name, (0, 350, 3451, 2703), 0, 0, 154, 105)
        element(root, "rect", id="strawberry-divider", x=0, y=105, width=154, height=2, fill=PINK)
        text(root, "headline", ["Make room", "for a little joy."], 12, 123, 10.6, 11.8, True)
        text(
            root,
            "offer",
            ["Vanilla or chocolate. Cone or cup.", "Take an ice-cream break at Lodziarnia."],
            12,
            148,
            4.05,
            5.4,
        )
        element(root, "rect", id="cta-accent", x=12, y=165, width=12, height=1.2, fill=PINK)
        text(root, "call-to-action", ["Drop by for", "your next treat."], 12, 177, 5.4, 6.4, True)
        text(
            root,
            "visit-details",
            ["12 Vanilla Lane, Sampletown", "Daily, 12:00-20:00"],
            12,
            193,
            3.5,
            5,
        )
        text(root, "demo-notice", ["Demo only - fictional shop details."], 12, 205, 2.4, 3)
        place_logo(root, 90, 155, 52)
    elif height == 1350:
        photo(root, name, (0, 350, 3451, 2491), 0, 0, 1080, 670)
        element(root, "rect", id="strawberry-divider", x=0, y=670, width=1080, height=12, fill=PINK)
        text(root, "headline", ["Make room", "for a little joy."], 72, 790, 80, 88, True)
        text(root, "offer", ["Vanilla or chocolate. Cone or cup."], 72, 953, 34, 44)
        text(root, "call-to-action", ["Drop by Lodziarnia."], 72, 1070, 42, 50, True)
        text(
            root,
            "visit-details",
            ["12 Vanilla Lane, Sampletown", "Daily, 12:00-20:00"],
            72,
            1144,
            30,
            42,
        )
        text(root, "demo-notice", ["Demo only - fictional shop details."], 72, 1280, 23, 30)
        place_logo(root, 710, 988, 320)
    else:
        text(root, "headline", ["A little", "ice-cream break."], 72, 265, 90, 100, True)
        photo(root, name, (250, 300, 3200, 3113), 0, 460, 1080, 1030)
        element(
            root, "rect", id="strawberry-divider", x=0, y=1490, width=1080, height=12, fill=PINK
        )
        text(root, "call-to-action", ["Drop by Lodziarnia."], 72, 1580, 42, 50, True)
        text(
            root,
            "visit-details",
            ["12 Vanilla Lane, Sampletown", "Daily, 12:00-20:00"],
            72,
            1640,
            30,
            40,
        )
        text(root, "demo-notice", ["Demo only - fictional shop details."], 72, 1735, 22, 30)
        place_logo(root, 750, 1520, 250)
    return ET.ElementTree(root)


def main():
    """Generate temporary typesetting files and invoke the native CorelDRAW build."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corel-script", type=Path, default=Path(__file__).with_name("export-corel.ps1")
    )
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="lodziarnia-typesetting-") as temporary:
        for name in ("flyer-a5-front-v01", "social-feed-v01", "social-story-v01"):
            compose(name).write(
                Path(temporary) / f"{name}.svg", encoding="utf-8", xml_declaration=True
            )
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-File",
                str(args.corel_script),
                "-ProjectPath",
                str(PROJECT),
                "-InputPath",
                temporary,
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
