# Logo Vectorizer

Standalone logo preparation tool for `flyer-design`. Converts a supplied raster
logo to editable SVG with optional PDF and PNG exports. Uses the tested VTracer
0.6.15 workflow with no custom denoising or palette reduction. No CorelDRAW,
Inkscape, MCP server, or external service is required for vectorization.

## When to use

Prefer an original vector logo. Use this tool when only a raster logo is available
and the design needs editable paths or scalable artwork. It is not a photo
vectorizer, a logo generator, or a way to recover missing detail.

## Shared environment

Use the repository's Python 3.12 and Poetry environment. From the repository root:

```shell
poetry env use 3.12
poetry install
```

The agent handles missing dependencies using [environment preparation](../../docs/environment.md).
This tool has no separate environment or dependency manifest.

## Run

Run from the repository root:

```shell
poetry run logo-vectorizer "/absolute/private-project/inputs/logo.png" --out-dir "/absolute/private-project/assets/logos/v01"
```

Always provide an external `--out-dir` during flyer work. The tool creates a folder
named after the input containing `.vector.svg`, `.print.pdf`, `.preview.png`, and
`report.json`. SVG is always retained; `--formats svg,png` selects optional exports.
Use a fresh revision directory to avoid overwriting previous results.

`--debug` adds settings, stage timings and tracebacks. `--log-file` mirrors logs to
an existing private directory. `--open-corel` optionally launches the SVG using the
installation path in `corel.py`; it is not needed for conversion.

## Review before placing the logo

Compare the preview with the original: brand colors, small lettering, thin lines,
holes and pale details. Import the SVG into the flyer only after visual review.
Tracing yields paths; lettering is not restored as editable text.

The tool preserves RGB before tracing, applies EXIF orientation, removes a
near-white background inferred from opaque borders, and thresholds alpha above
16. Pale details may disappear and partial transparency becomes solid. VTracer
still approximates curves/colors and can retain source noise. Keep originals.
The historical `.print.pdf` name denotes a vector asset, not a certified press-ready
PDF; final print checks belong to the separate preflight workflow.

## Python and development

Run scripts with `poetry run python` from the repository root.

```python
from pathlib import Path
from logo_vectorizer.config import OutputFormat, resolve_output_paths
from logo_vectorizer.pipeline import vectorize

source = Path("/absolute/private-project/inputs/logo.png")
paths = resolve_output_paths(source, Path("/absolute/private-project/assets/logos/v01"))
vectorize(source, paths, {OutputFormat.SVG, OutputFormat.PNG})
```

```shell
poetry run pytest tools/logo-vectorizer/tests
poetry run ruff check tools/logo-vectorizer
```

CLI exit codes: `0` success, `2` invalid arguments, `1` execution failure.
Python raises `ConfigurationError` for invalid formats and `VectorizationError`
with the original exception as its cause for execution failures.

Code follows the repository's [MIT license](../../LICENSE). Dependencies retain
their own licenses. Real logos, environments, and generated comparisons are not
part of this public tool; tests generate synthetic images in temporary folders.
