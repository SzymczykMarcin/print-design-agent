# Tools and capability placeholders

Before first use, follow the shared [environment preparation](../../../../docs/environment.md)
procedure: detect/install required dependencies, use the single root Poetry
environment with Python 3.12 for every tool, and verify a real operation.

Read before backend selection, automatic dependency installation, or work needing accurate measurements or specialized image operations.

## Select a usable backend

1. Respect an explicit application choice or existing editable master.
2. Detect CorelDRAW using local application discovery or a user-supplied path. An executable's presence does not prove that its automation interface is available. Use documented, verified capabilities for that edition/version.
3. If CorelDRAW is absent or cannot perform the task with available tools, use Inkscape. Preserve any existing CDR and disclose a switch to SVG. If editing an existing CDR requires unsupported conversion, request a usable export rather than claim a lossless round trip.
4. Detect Inkscape through PATH and appropriate installation locations. Verify its executable with `--version` and inspect `--help` for required CLI options.
5. If Inkscape is missing, install the current stable release using the procedure below. Do not install it merely while authoring or reviewing this skill.

## Use the editor directly

For CorelDRAW on Windows, write project-specific scripts against its documented COM object model, for example with Python and a suitable COM library. Verify the installed edition, registered application, and required methods with a small task-local operation before building the design. Do not assume access was tested on this machine.

Use the application's available capabilities as the composition requires, rather than restricting design to a predefined set of helper functions. Work in the intended document or a new project document; do not modify unrelated open documents. Save scripts with the private project's working files so the design can be reproduced and revised.

For Inkscape, author or modify editable SVG directly and use its verified CLI/actions to query geometry and render previews.

Neither route requires a custom adapter or MCP server. Missing repository integration code is not a missing editor capability. If a required operation fails, diagnose the actual API, dependency, or permission issue before choosing a fallback.

Extract a reusable helper only when repeated work demonstrates a concrete benefit. Such a helper must remain optional and must not limit direct access to the editor.

## Install Inkscape when needed

Automatic installation is the intended fallback in this workflow. Proceed when the active task and host policy permit dependency installation; do not add another confirmation if it is already authorized. A skill does not bypass sandbox, administrator, network, or user restrictions.

- **Windows:** if winget is present, inspect `winget show --id Inkscape.Inkscape --exact --source winget`, then install with `winget install --id Inkscape.Inkscape --exact --source winget`. Verify the publisher, installer source, supported scope, and architecture. Prefer a per-user installation when supported. If winget is unavailable, use an official stable installer or archive from inkscape.org appropriate to the host.
- **macOS:** with an existing Homebrew installation, use `brew install --cask inkscape`; otherwise use the official architecture-matched download. Do not install Homebrew solely as an unannounced prerequisite.
- **Linux:** use the existing distribution package manager and its trusted repositories, e.g. `apt-get install inkscape` on Debian/Ubuntu with the required permissions. Do not add third-party repositories merely to obtain a newer version.

Keep installers and application binaries out of the repository and client deliverables. Verify the installed executable and perform a small SVG-to-PNG export in the project work area before relying on it. If a method fails, diagnose it once and use a verified alternative if practical. If permissions or network access block installation, report the exact blocker, retain any editable SVG already prepared, and mark previews as unrendered. Do not loop through blind downloads or claim success without verification.

## Editable source and rendering

For SVG, use explicit dimensions, a coherent viewBox, stable object IDs, separate outlined-text/vector/image objects, and portable embedded or correctly packaged image links. Inkscape SVG can retain layer names. Text in the composition must be genuine font-derived curves; follow the conversion procedure below. Keep its reconstruction content and typography settings outside the outlined artwork.

Verify commands against the installed version. Typical single-page CLI exports are:

```text
inkscape "absolute/path/design.svg" --export-area-page --export-type=png --export-filename="absolute/path/preview.png"
inkscape "absolute/path/design.svg" --export-area-page --export-type=pdf --export-filename="absolute/path/review.pdf"
```

Use the resolved absolute executable path if it is not on PATH. Set PNG pixel dimensions deliberately for the target. For multiple pages, inspect the installed version's page export options or keep separate editable page files; do not assume one command handles every page.

An Inkscape PDF export is not by itself a PDF/X or color-managed production guarantee. Hand it to the separate print-preflight workflow when print release is requested.

## Convert typeset text to curves

Use this for all newly composed promotional text, including captions and fine
print. Font choice and typesetting come first; native outlining follows immediately
once the block's layout is established, before reviewed artwork is saved or exported.

1. Use the actual available font and weight, with correct shaping, diacritics,
   ligatures, kerning, line breaks, and paragraph layout. Resolve missing glyphs or
   substitutions before conversion; outlining freezes mistakes too.
2. Preserve exact content in `copy.md` and the reproducible typography recipe in
   working notes or the project-local script. Live text may exist transiently for
   composition, but should not remain as hidden duplicates in the delivered artwork.
3. Convert using CorelDRAW's native text-to-curves operation through a verified
   interface, or Inkscape's native object-to-path/text outlining through its verified
   UI or CLI/actions. Another font-aware vector tool is acceptable if it preserves
   the actual font's shaping and layout. Do not guess API methods or action names.
4. Keep converted blocks grouped and named by role. Compare renders before and
   after conversion for changed spacing, clipping, glyph loss, counters, or movement.
   Inspect the saved document's object types: letters must be vector paths, not live
   text, bitmap traces, or embedded text screenshots. Outlining only the PDF export
   does not satisfy the requirement for the CDR/SVG composition.
5. For copy edits, re-typeset the affected block from its stored content and settings,
   convert it again, and repeat the comparison and proofreading. Do not distort
   outlined paragraphs to fit a new format; recompose their typography.

Do not use logo-vectorizer or image generation to construct typeset lettering.
If conversion cannot be performed or verified, retain the recoverable draft and
report the missing operation; do not label the artwork as outlined. This requirement
does not authorize changing an existing client master that must remain untouched.

## Prepare a raster logo

The implemented tool is [tools/logo-vectorizer](../../../../tools/logo-vectorizer/README.md),
resolved relative to this repository, not a user-specific installation path.
Use it when only raster artwork exists and editable or scalable logo paths are
needed. Prefer supplied original SVG/PDF/CDR artwork; do not trace photographs or
vectorize every logo automatically.

1. Inspect the original and read the tool README. Set up the shared root Poetry
   environment and locked dependencies when needed, within host permissions.
2. From the repository root, run through Poetry with the original's absolute path and an explicit
   private output directory, such as `<project>/assets/logos/v01`:
   `poetry run logo-vectorizer "<project>/inputs/logo.png" --out-dir "<project>/assets/logos/v01"`.
   The fixed workflow is VTracer without custom cleanup. Do not supply removed
   engine, palette, quality, mode, or cleanup switches.
3. Inspect the generated preview against the original at placement size and close
   up. Check colors, lettering, thin lines, holes, and pale or transparent details.
   Confirm that the SVG contains vector paths rather than an embedded bitmap.
4. Place the reviewed SVG as a separate logo object in CorelDRAW or Inkscape.
   Keep source artwork unchanged and note the chosen derivative and any limitations
   in the private project's reports. The tool's PDF is an asset, not print approval.

If tracing changes identity, keep a sufficient original raster or request original
vector artwork. Do not hide defects by shrinking the preview or claim that traced
lettering is live text. For failures use `--debug` and optionally `--log-file` in
an existing private directory; diagnose the reported stage instead of recreating
an alternative engine. Never store client logos or outputs in this public tool.

## Capability placeholders

**Status: not implemented in this repository.** These names describe optional helpers for specific capability gaps. They are not installed commands, scripts, MCP tools, or required packages. Do not create tool infrastructure during a flyer task unless requested. Use an existing reliable tool or small project-local calculation where sufficient.

| Placeholder | When needed and intended input | Required result | Current fallback |
| --- | --- | --- | --- |
| TOOL-ASSET-PROBE | Need exact image size, orientation, profile, or usable crop; original image and intended placement | Measured metadata and crop dimensions | Pillow or another installed metadata reader; inspect visually too |
| TOOL-TEXT-MEASURE | Tight text fitting or uncertain font substitution; actual font, copy, frame, style | Renderer-consistent bounds, line breaks, glyph/fallback and overflow information | Native renderer, Inkscape geometry queries and rendered inspection; never estimate fit from character count alone |
| TOOL-PHOTO-MASK | Subject extraction or difficult edge cleanup; image and intended mask | Non-destructive mask/derived image with inspected edges | Existing editor/masking tool; otherwise use a rectangular crop or report that precise cutout is unavailable |
| TOOL-QR | A supplied destination needs a QR code | Real encoded SVG plus decode result from rendered output | Installed QR encoder/decoder libraries; if unavailable, leave a labeled draft placeholder or use the supplied readable URL |
| TOOL-PREVIEW-RENDER | Need to assess the current source or exported review PDF | Images traceable to that exact revision | Native editor/Inkscape for SVG, an available PDF renderer for PDF; disclose inability to view instead of claiming review |

Record an encountered gap in the project's existing notes: placeholder ID, affected task, fallback used, and unresolved limitation. Keep capability placeholders out of client-facing artwork. A temporary visual placeholder, such as a missing QR, must be visibly marked in drafts and resolved or explicitly excluded before finished design delivery.
