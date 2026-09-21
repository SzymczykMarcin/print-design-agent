# QR code tool

Generate a standalone vector SVG and verify exact QR content in SVG, raster images,
or rendered PDF pages. This is an asset tool, not an editor adapter or print preflight.
All commands use the repository's shared Python 3.12 Poetry environment.

## Generate

```shell
poetry run qr-code generate "https://example.org/meetings" --output "/private/project/assets/website-qr.svg" --size-mm 36
```

- Black vector modules, opaque white background, four-module quiet zone on each edge.
- Size includes the quiet zone. Default: 30 mm and medium (`M`) error correction.
  `--correction L|M|Q|H` selects another level; automatic version selection remains enabled.
- The actual SVG is rendered with resvg and independently decoded with zxing-cpp
  before saving. No existing file is overwritten; choose a new revision path.
- Payload is preserved exactly, including Unicode and whitespace. URLs are neither
  fetched nor shortened. JSON output includes module size and verification evidence.

## Verify the placed artwork

```shell
poetry run qr-code verify "/private/project/previews/flyer.png" --expected "https://example.org/meetings"
poetry run qr-code verify "/private/project/working/candidate.pdf" --page 2 --expected "https://example.org/meetings" --pdftoppm "/path/to/pdftoppm"
```

PDF verification requires Poppler's `pdftoppm` on PATH or its explicit executable
path. No machine-specific path is built into the tool. SVG rendering uses resvg
from the root Poetry dependencies. Raster images use their existing pixels; PDF
and SVG default to a 300-PPI render (`--dpi`, 72–600). Temporary renders are cleaned up.
Encrypted PDFs are rejected. Raster verification reads the first image frame.

Without `--page`, every PDF page is checked. Success means **at least one exact
match anywhere in the selected pages**, not one match per page. All decoded QR
payloads and their page numbers are reported, including other destinations. Use
separate page-specific calls when each side must contain its own code.

Commands write JSON to stdout and errors to stderr. Exit codes: `0` exact match,
`1` no match or operational failure, `2` invalid arguments/data. Put `--debug` before
`generate` or `verify` for tracebacks. Reports contain decoded content; store client
reports privately.

## Python API

```python
from pathlib import Path
from qr_code import QRSettings, generate_svg, verify_file

asset = generate_svg("https://example.org", Path("/private/assets/qr.svg"), QRSettings(36))
result = verify_file(Path("/private/previews/flyer.png"), "https://example.org")
assert result.matched
```

Validation applies to both Python and CLI callers. Frozen data classes hold
settings/results; encoding, rendering and verification are separate functions.

## Placement and limits

Preserve the white quiet zone and square proportions. Keep modules as vector paths.
SVG black is not a CMYK ink prescription: set modules to process K-only in the print
editor and inspect the exported PDF. Verify again after placement, resizing, color
conversion and export. The generation check does not replace that final-file check.

A successful software decode is not proof of real-world scan reliability, adequate
printed module size, a working website, suitable paper/contrast or print readiness.
Choose physical size for the content and viewing conditions; test an actual-size
proof for important campaigns. This tool does not modify source artwork or PDFs.

## Tests

```shell
poetry run pytest tools/qr-code/tests
poetry run ruff check tools/qr-code
```

Tests exercise real SVG rendering/decoding, Unicode, quiet-zone geometry, overwrite
protection, invalid inputs, wrong/missing payloads and multi-page PDF placement.
The PDF integration test skips if Poppler is unavailable; install it to run that check.
