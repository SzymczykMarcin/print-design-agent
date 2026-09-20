"""Compose one A5 flyer from original assets; Corel performs native outlining."""

import base64
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
BROWN, CREAM, PINK, MINT = "#49281E", "#FFF7EB", "#ED91A5", "#A4CDCA"


def text(role, x, y, content, size, family="Lato", color=BROWN, anchor="start"):
    """Typeset a named block with explicit millimetre-based geometry."""
    return (
        f'<text id="{role}" x="{x}" y="{y}" font-family="{family}" '
        f'font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}">{content}</text>'
    )


def compose():
    """Build the photo, organic color fields, authentic logo and live type recipe."""
    photo = base64.b64encode((PROJECT / "inputs/photos/ice-cream-moment.jpg").read_bytes()).decode()
    logo = ET.parse(PROJECT / "inputs/logos/lodziarnia.svg").getroot()
    logo_markup = (
        "".join(ET.tostring(child, encoding="unicode") for child in logo)
        .replace("ns0:", "")
        .replace(":ns0", "")
    )
    objects = [
        f'<rect id="cream-paper" width="152" height="214" fill="{CREAM}"/>',
        (
            f'<image id="original-lifestyle-photo" x="-34" y="-12" width="180" '
            f'height="260.794" xlink:href="data:image/jpeg;base64,{photo}"/>'
        ),
        (
            f'<path id="cream-scoop-panel" fill="{CREAM}" d="M78,-3 H155 V182 C121,177'
            f" 87,181 77,159 C65,139 78,128 72,107 C68,89 59,86 66,69 C77,44 70,32 "
            f'78,-3 Z"/>'
        ),
        (
            f'<path id="strawberry-swoosh" fill="{PINK}" d="M82,70 C104,60 136,68 '
            f'156,60 L156,128 C130,136 93,137 76,126 C62,116 67,81 82,70 Z"/>'
        ),
        (
            f'<g id="authentic-logo" transform="translate(87 8) scale(0.052) '
            f'translate(-140 -135)">{logo_markup}</g>'
        ),
        text("headline-script-one", 109, 88, "Lato", 11.5, "Pacifico", BROWN, "middle"),
        text("headline-script-two", 109, 100, "smakuje", 11, "Pacifico", BROWN, "middle"),
        text("headline-display", 109, 125, "LEPIEJ!", 26, "Bebas Neue", BROWN, "middle"),
        (
            f'<path id="mint-swipe" d="M86,131 Q111,127 136,131" fill="none" '
            f'stroke="{MINT}" stroke-width="2.1" stroke-linecap="round"/>'
        ),
        text("offer-one", 110, 143, "W rożku czy w kubeczku?", 3.3, anchor="middle"),
        text("offer-two", 110, 149, "Po prostu: po swojemu.", 3.3, anchor="middle"),
        f'<circle id="pink-sticker" cx="28" cy="143" r="18" fill="{PINK}"/>',
        (
            f'<circle id="sticker-ring" cx="28" cy="143" r="16.5" fill="none" '
            f'stroke="{CREAM}" stroke-width="0.35"/>'
        ),
        text("sticker-one", 28, 141, "Chwila", 4.8, "Pacifico", BROWN, "middle"),
        text("sticker-two", 28, 148, "dla siebie", 4.1, "Pacifico", BROWN, "middle"),
        (
            f'<path id="cocoa-footer" fill="{BROWN}" d="M-3,176 C28,157 42,178 75,171 '
            f'C106,166 124,159 155,170 V217 H-3 Z"/>'
        ),
        (
            f'<path id="mint-footer-edge" fill="{MINT}" d="M-3,176 C28,157 42,178 '
            f"75,171 C106,166 124,159 155,170 L155,172 C124,161 106,168 75,173 C42,180"
            f' 28,159 -3,178 Z"/>'
        ),
        text(
            "call-to-action", 76, 185, "Wpadnij na lepszy dzień!", 8.2, "Pacifico", CREAM, "middle"
        ),
        text(
            "address",
            76,
            195,
            "ul. Waniliowa 12 · Miasto Przykładowe",
            3.4,
            "Lato",
            CREAM,
            "middle",
        ),
        text("hours", 76, 201, "Codziennie 12:00–20:00", 3.4, "Lato", CREAM, "middle"),
        text(
            "demo-notice",
            76,
            206.3,
            "Projekt demonstracyjny · fikcyjne dane lokalu",
            2.3,
            "Lato",
            CREAM,
            "middle",
        ),
        (
            f'<g id="sunshine-marks" fill="none" stroke="{PINK}" stroke-width="1.2" '
            f'stroke-linecap="round"><path d="M11,40 L8,36 M15,37 L14,32 M9,45 '
            f'L5,44"/></g>'
        ),
        (
            f'<path id="heart-doodle" d="M135,157 C127,151 131,147 135,151 C140,145 '
            f'144,150 135,157 Z" fill="none" stroke="{PINK}" stroke-width="0.8"/>'
        ),
    ]
    svg = (
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" width="152mm" height="214mm" '
            'viewBox="0 0 152 214">'
        )
        + "".join(objects)
        + "</svg>"
    )
    target = PROJECT / "working/assembly.svg"
    target.write_text(svg, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    compose()
