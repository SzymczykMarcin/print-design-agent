# Design and handoff notes: v01

## Files and decisions

The three compositions were typeset in Lato, opened in CorelDRAW 2024 (25.2.1.313),
converted with native `ConvertToCurves`, saved as CDR, closed and reopened before
PDF export. Matching outlined SVGs provide an open-format alternative. Photographs
are embedded in both masters; the supplied logo remains vector. Temporary live-text
compositions are not included in the delivered artwork.

A warm cream text area separates the message from the busy stock photograph.
Cocoa text, a strawberry divider and the original mark tie the formats together.
The flyer and feed lead with photography; the story starts with a short headline
and uses a taller crop. Copy is taken from `copy.md`; line breaks are layout choices.

- Flyer: 154 x 216 mm canvas including 3 mm bleed, 148 x 210 mm trim.
  The trimmed PNG shows the finished size; the bleed PNG shows the complete PDF.
- Feed: 1080 x 1350 px. The visit details are split onto two lines for readability.
- Story: 1080 x 1920 px. Key copy is inset from top/bottom interface areas;
  actual platform overlays must still be checked when publishing.
- Crop rectangles, font weights, sizes, leading and coordinates are preserved in
  `working/build_demo.py`. Crop derivatives retain source pixels without upsampling.
- The flyer logo was moved inward after visual review to keep its tagline clear
  of trim. The story uses a smaller 250 px logo to prioritize the main message;
  its small tagline is subordinate and should be enlarged if it must be read on a phone.

## Review

Rendered the exported PDFs, checked all three compositions at overview and full
resolution, and compared the visible wording with `copy.md`. The face, hand and
ice cream remain intact; no text crosses the photo or overlaps another block.
The fictional-data notice is present in every format. Fine lettering in the traced
logo retains the supplied irregularities rather than pretending to restore detail.

Native CDRs were reopened successfully and contained no live text. SVGs were parsed
and checked for outlined lettering and embedded imagery. Numerical before/after
outlining comparisons are recorded in `measured-evidence-v01.json`; differences
are nonzero and are not treated as a pixel-identical result. The final rendered
lettering was reviewed independently for missing words, clipping and spacing.

This is a completed design demonstration, not user-approved campaign copy or a
printer-certified release. No printer, production ICC profile, ink limit or PDF/X
acceptance profile has been supplied.

## Rebuild

Run from the repository root in the shared Poetry environment. CorelDRAW must be
installed and its COM server usable on Windows. Install the bundled Lato fonts in
the editor first. Resolve a Poppler directory containing `pdftoppm.exe` and
`pdfinfo.exe`; keep machine-specific locations out of the repository.

```powershell
poetry install
poetry run python examples/demo-flyer/working/build_demo.py
poetry run python examples/demo-flyer/working/finish_demo.py --poppler-bin "<absolute Poppler bin directory>"
```

The build overwrites this example's v01 outputs. Work on a private copy for revisions.
The first script composes temporary SVGs and invokes the project-local PowerShell
export script. The second packages SVG imagery, adds PDF trim/bleed boxes, renders
PNG outputs and records measured evidence. Font source files and exact copy remain
available to reconstruct lettering. Native Corel export may vary across versions.

Users without CorelDRAW can open the delivered SVGs in Inkscape and use the bundled
fonts to re-typeset changed copy before outlining it again. The reproduction script
is a concrete Corel example, not a required adapter or a new repository-wide tool.
