---
name: print-preflight
description: Prepare, correct, export and verify a production PDF for one print material against the selected printer's requirements. Also supports explicit read-only audits. Print preparation finishes with a verified release file, not just a report.
---

# Print Preflight

Prepare -> inspect -> correct -> re-export -> verify -> release. A report of
unresolved checks does not substitute for the requested production PDF.

## Mode and context

Read the brief, copy, reviewed design, source and printer specification for the one
selected material. Preparation authorizes necessary technical fixes and exports
within that design, preserving originals and prior revisions. Route substantive
composition changes to `flyer-design`; resolve decisions beyond existing authority.
An explicit inspection-only/no-modification request is read-only: audit completion
does not imply release readiness. Neither mode authorizes external uploads or orders.

Keep candidates in `working/print-candidates/`, renders in `previews/` and evidence
in `reports/`; reserve `exports/print/` for released bytes. Do not silently move or
overwrite existing files. Reuse applicable specs/setup records, but inspect each
new or changed candidate rather than inheriting an old pass.

## 1. Resolve the production target

Use the selected printer/product's current specification, recording its source/date.
Resolve trim, sides/order, bleed, safe insets, process/paper, finishing, PDF standard,
ICC/color requirements, resolution and applicable ink limits. Check project files
and published instructions before asking for missing information. Continue independent
work while waiting; arbitrary profiles or generic 3 mm / 300 PPI presets cannot
establish readiness. A demo needs an authorized, documented production target too.

Plan CMYK with the required destination ICC profile unless the printer explicitly
accepts another managed workflow, such as profiled RGB in PDF/X-4; record exceptions.
Fix incorrect source/destination settings rather than returning to sRGB because it
looks brighter. Profile assignment is not conversion.

## 2. Export and inspect

- Read [checks](references/checks.md) for every initial candidate audit; apply all
  relevant categories. This mandatory coverage is not an optional optimization.
- Read relevant sections of [tools](references/tools.md) when choosing a checker,
  setting up or resolving an unsupported check. Reuse verified tools otherwise.
- Consult [sources](references/sources.md) only for research or disputed guidance;
  generic references never override the actual product specification.

In preparation mode, export a candidate from CDR/SVG if no PDF exists. For PDF-only
inputs use a verified fixup or obtain the source when necessary. Set document size,
page range, bleed, PDF version, color conversion/profile, compression and resampling;
verify actual output instead of trusting editor defaults or successful API calls.
Keep logo/text vector and lettering outlined. Do not rasterize the entire page,
upscale to invent detail or enlarge boxes to invent bleed.

The PDF contains only this material: one page for a single-sided flyer/poster,
front/back as specified for a two-sided flyer. No social versions, mockups, comparison
boards, cover pages or reports; no imposition unless requested by the printer.

Record file size, SHA-256, page count, tool/profile versions and inspect the exact
PDF: geometry, actual bleed, safe insets, effective PPI, paths/text, colors/ICC,
ink coverage, overprint/transparency, finishing and required PDF conformance.
Follow nested objects and inspect every page. Source checks, empty text extraction,
font/image inventories and DPI metadata alone cannot establish compliance.

Render every page; inspect trim and bleed separately and compare with reviewed
artwork and exact copy, including fine lettering, page order and QR payloads.
RGB renders cannot verify separations, ink coverage or press color fidelity.

## 3. Correct until the release gate passes

For each failure, fix its cause, export a new candidate and rerun affected checks
plus file integrity and every page's visual review. Recompute the hash and retain
revision evidence. Do not end with a list of defects you can still fix.
Try a suitable available/installable validator for missing mandatory capabilities.
If blocked by input, permissions, licensing or verification limits, record the
exact blocker and next action; keep the candidate a draft and preparation incomplete.

Write `reports/print-preflight-<revision>.md`: identity/hash, requirement sources,
tool/profile versions, scope, page/object-specific requirement versus observation,
evidence paths, result and correction. Per-check statuses: PASS, FAIL, WARNING,
NOT VERIFIED, NOT APPLICABLE (explain applicability).

| Overall result | Release decision |
| --- | --- |
| FAIL | A mandatory criterion fails: correct and recheck |
| NOT VERIFIED | Required information/evidence is missing: resolve before release |
| PASS WITH WARNINGS | All mandatory criteria pass; listed warnings are advisory only |
| PASS | All applicable mandatory criteria verified and passed |

Never hide a blocker as a warning or irrelevant check. Optional finishing absent
from the job is not a blocker. Only PASS or PASS WITH WARNINGS plus the delivered
verified file completes preparation; an audit report or preview cannot do so.

## 4. Release and hand off

Copy the passing candidate to a descriptive, versioned path in `exports/print/`.
Verify its SHA-256 matches inspected bytes and record the released path. Any later
modification requires reinspection.
Lead with that PDF, finished size and page/side count; link the trim preview and
report separately. Label comparison boards as previews, never production files.
State target and advisory findings; a pass applies to these bytes/specs, not every
physical press result. If blocked, say preparation is incomplete and identify the
missing step. In audit mode, deliver findings without implying a corrected release.
