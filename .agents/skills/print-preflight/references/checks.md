# Inspection criteria

Use the applicable printer/product requirements as thresholds. Separate project
policy, printer requirements, and measured PDF properties in the report.

## File and page geometry

- Open and parse the entire PDF; record errors, encryption, damaged streams,
  unexpected attachments, annotations/forms, or content that may print differently.
- Check page count, order, front/back orientation, singles versus spreads, and
  scale against the order. Do not impose pages unless the printer requests it.
- Inspect MediaBox, TrimBox, BleedBox, and CropBox per page, including rotation,
  inherited/default values and any UserUnit scaling. Convert PDF points to mm
  using `25.4 / 72` with the actual unit scale. Record when trim is inferred rather
  than explicitly defined; accept only if the receiving workflow permits it.
- Measure bleed separately at every edge. Check that edge-to-edge artwork really
  fills it, with no blank strips, clipped backgrounds, or accidental objects.
  Enlarging a BleedBox does not create artwork beyond the trim.
- Measure critical content against safe insets and folds, cuts, perforations,
  binding, eyelets or concealed roll-up areas. Check printer marks only when
  requested; they must not intrude into usable artwork.

## Raster detail and vector integrity

Measure image resolution at each placement in the PDF, including repeated uses,
transforms and masks. For a visible crop, use retained pixels divided by its
physical size in inches; inspect both axes. Distinguish continuous-tone pictures
from one-bit line art and vector content. Compare with the product's targets.
A PDF has no single meaningful DPI value; a preview rendered at 300 dpi says
nothing about the embedded source resolution. Upsampling can raise measured pixel
counts without adding source detail, so inspect compression and visible artifacts.

Keep intended logo/text paths vector. A full-page bitmap with no font resources
is not proof that text was converted to curves.

## Text as curves

This repository expects composed promotional text to be outlined before handoff.
Inspect actual page content and nested Form XObjects for live text and inspect
lettering as paths in the source/PDF with an object-aware tool. Font inventories
and text extraction are useful clues, not conclusive proof of outlining. Unused
font resources need investigation, not an automatic visible-text failure.

Compare final glyphs, counters, spacing, diacritics and line breaks with approved
copy and the reviewed design. Do not rely on OCR alone. If the user explicitly
permits live text, check font embedding and substitution instead; subset embedding
is not inherently a failure. Record this exception rather than silently changing
the repository's default. Outlining alone does not verify minimum stroke thickness
or legibility at final size.

## Color, ink, overprint and transparency

- Inventory color use in images, vector fills/strokes, gradients and nested objects:
  DeviceRGB, ICCBased, CMYK, Gray, Separation/DeviceN, and relevant blending spaces.
  Compare with the printer's accepted color workflow; RGB is not universally
  forbidden in a color-managed PDF/X-4 workflow.
- Check the required ICC output intent and actual object profiles. Attaching an
  output intent describes the output condition; it does not convert RGB objects
  into CMYK. A profile label alone is not evidence of the intended conversion.
- Inspect local total area coverage using a profile-aware preflight/separation
  tool and the required press limit. An average CMYK ink estimate, simple channel
  count, or RGB screenshot cannot verify the maximum ink load.
- Check unwanted spot inks, duplicate spot names, registration color in artwork,
  small four-color black elements, and black recipes against printer requirements.
  Do not prescribe a universal rich-black mix or convert intended finishing spots.
- Simulate overprint and separations: white objects set to overprint, disappearing
  content, unintended knockout and wrong plate assignments require investigation.
- Check transparency and blend effects against the requested PDF standard and
  receiving RIP. Preserve supported transparency; do not flatten merely because
  transparency exists. If flattening is required, inspect resulting text, seams,
  edges, resolution and color changes after re-export.
- For varnish, foil, white ink or cut paths, verify the printer's exact spot names,
  overprint rules, layer/page separation, dimensions and registration. Mark this
  category not applicable when no special finishing is requested.

## PDF standard and final appearance

If PDF/X is required, validate the specific variant using an actual conformance
profile. A filename, XMP declaration, OutputIntent entry, or export preset is not
proof of conformity. PDF/X validation also does not establish every job-specific
requirement, such as adequate image detail or the intended bleed content.

Inspect renders of every page at intended size and close-up. Compare approved
copy, logo, images, dates/prices, contact information and page order. Decode QR
codes from the final rendered PDF and compare their contents with the supplied
destination; decoding does not prove the remote page is correct or available.
Check scan size and quiet zone in context. Note limitations of screen color and
uncalibrated physical-size judgments without substituting them for measurements.
