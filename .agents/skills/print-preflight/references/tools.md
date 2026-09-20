# Evidence tools and limitations

Before first use, follow the shared [environment preparation](../../../../docs/environment.md)
procedure: detect/install required dependencies, use the single root Poetry
environment with Python 3.12 for every tool, and verify a real operation.

Discover installed tools and verify version/help before use. Use absolute paths,
save evidence in the private project, and preserve command exit codes/stderr.
A commercial tool is useful when present but is not assumed to be installed.
For print preparation, use verified editing/export capabilities as well as inspection;
analysis-only behavior applies when the user explicitly requests an audit.
Install dependencies only when needed and permitted by the task and host.

## Dedicated preflight

Use Acrobat Pro Preflight and Output Preview, or an equivalent verified production
preflight tool, for the printer's PDF/X profile, object-level checks, separations,
overprint and ink coverage. Select the actual job profile and record its settings;
a generic green check is insufficient. Use analysis-only mode for an audit, not
an automatic fixup. Export its findings for the report.

CorelDRAW/Inkscape can help inspect the editable design and create a corrected
export, but successfully exporting PDF is not independent PDF/X validation. Compare
the final PDF after export; do not assume the editor and receiving RIP agree.

## Open-source baseline

These read-only inspection examples assume the relevant executables are installed.
Replace placeholders with absolute private paths and verify available options:

```text
qpdf --check "candidate.pdf"
pdfinfo -f 1 -l N -box "candidate.pdf"
pdfimages -list "candidate.pdf"
pdffonts "candidate.pdf"
pdftoppm -png -r 150 "candidate.pdf" "previews/preflight-page"
```

Here `N` is the actual page count. Create the preview destination beforehand.
Choose higher render resolution for fine-detail checks; the sample 150 is a
review-render setting, not a print-resolution acceptance threshold. Check which
page box the renderer uses and inspect trim and bleed deliberately.

| Evidence | What it supports | What it does not establish |
| --- | --- | --- |
| `qpdf --check` | Structural/syntax checks; retain warnings and errors | PDF/X conformance, correct colors, acceptable print appearance |
| `pdfinfo -box` over all pages | Reported page geometry, rotation and metadata | Actual bleed artwork or safe placement of essential content |
| `pdfimages -list` | Image inventory, color descriptions and placed x/y ppi | All vector colors, maximum ink coverage, original detail before upsampling |
| `pdffonts` | Font inventory, embedding/subset indicators | Proof that visible lettering is outlined or readable |
| PDF render plus visual review | Clipping, missing content, layout and comparison | Calibrated press color, conformance, separations or maximum ink coverage |

For qpdf, exit 0 means syntactic success, 2 errors, and 3 warnings. Interpret other
tools' exit codes according to their own documentation, not the qpdf convention.

A small project-local script using a PDF parser may measure boxes or inventory
objects when necessary. It must handle inherited resources, nested objects,
transforms and page units relevant to the claim. Raw text searches for `/RGB`,
`/Font`, or `/OutputIntent` are not reliable PDF analysis. A parser opening the file
is not a conformance validator. Record unimplemented checks instead of inventing
measurements; no comprehensive preflight script ships with this skill.

## Capability gaps

When available tools cannot validate the required PDF/X flavor, profile-dependent
ink coverage, overprint or outlined-text structure, mark those checks `NOT VERIFIED`.
Still finish the checks that can be supported. Specify the exact evidence needed
from a production preflight tool or the printer; do not declare the whole file
ready because simpler tools passed. Do not upload private artwork to an online
checker without authorization. In preparation mode, an unresolved mandatory check
blocks release and task completion; retain the candidate in `working/print-candidates/`.
A report documenting the gap does not replace the required verification.
