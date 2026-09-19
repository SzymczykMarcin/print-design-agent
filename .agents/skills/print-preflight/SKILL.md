---
name: print-preflight
description: Inspect final print PDFs against printer and product requirements for flyers, posters, banners, and related promotional materials. Check geometry, bleed, image resolution, outlined text, colors, transparency, overprint, and PDF/X when required; produce an evidence-based release report. Does not design artwork or certify unmeasured properties.
---

# Print Preflight

Audit the exact PDF intended for printing, separately from design review. Produce
an actionable report supported by measured properties and rendered inspection.

## Scope and inputs

- Read the private project's brief, printer instructions/template, current PDF,
  approved preview, and copy. Use the editable master when investigating an issue.
- Work in the external project: reports in `reports/`, inspection renders in
  `previews/`, print candidates in `exports/print/`. Preserve originals.
- An inspection request authorizes inspection, not silent fixes, re-exporting,
  uploading files, or ordering print. Apply changes only within an explicitly
  requested correction task, using a new revision and rechecking it afterward.
- Respect this repository's outlined-text workflow. Distinguish that project rule
  from PDF/X requirements; outlining is not universally required by PDF/X.

## 1. Establish the acceptance criteria

Read [inspection criteria](references/checks.md). Collect the chosen printer,
product, substrate/process, trim dimensions, sides/page order, bleed and safe
insets, folds/finishing, accepted PDF standard, color/ICC requirements, image
resolution targets, ink limits, and marks/spot-color rules where applicable.

Use the actual order's specification and template. Consult the printer's current
product instructions online when needed; record URL/version/access date. General
references in [sources](references/sources.md) inform checks but do not override
a product-specific requirement. If sources conflict, flag the conflict rather
than silently choosing one. Do not impose universal 3 mm bleed, 300 ppi, CMYK-only,
or one PDF/X flavor on every job.

If requirements are missing, ask for the material missing information and continue
independent inspection. Report provisional targets explicitly; do not pass release
against guessed requirements. Mark genuinely irrelevant checks as not applicable
with a reason, rather than making every job require every possible specification.

## 2. Identify the file and available evidence

Record the PDF path, byte size, SHA-256, page count, and intended revision. Record
inspection tool versions and any preflight profile name/version. Read
[tools and limitations](references/tools.md) before choosing a checking method.

Inspect the actual PDF, not only the source document, filename, export preset,
DPI metadata, or an earlier preview. If only CDR/SVG is supplied, inspect what is
possible and state that the final PDF is missing; source checks do not release an
unseen export. A logo-vectorizer asset PDF is not the final flyer PDF.

## 3. Run structural, object, and rendered checks

Apply every relevant category in [checks](references/checks.md): file integrity,
page geometry and bleed content, effective image resolution, text as curves,
color/ICC/ink coverage, overprint/transparency, finishing separations, and final
visual/content comparison. Cover all pages; record page-specific findings.

Use the best available measured evidence. A command that runs successfully is not
a passing print check. Distinguish a measured failure from a check the tool cannot
perform. Never infer CMYK compliance from image inventory alone, outlined text
from an empty text extraction, or sufficient bleed from page boxes alone.

Render the candidate PDF and inspect the trimmed result and bleed separately.
Compare with the approved design and copy, including small outlined lettering,
contact details, front/back order, and decoded QR destination. Ordinary RGB renders
cannot establish accurate separations, total ink coverage, or press color fidelity.

## 4. Report the decision

Write `reports/print-preflight-<revision>.md` and retain relevant tool output and
inspection images beside it or in the project's existing evidence folders.
The report must include:

- File identity/hash, requirement sources, tool/profile versions, and scope.
- One row per relevant check: requirement, actual observation, page/object or
  location, evidence path, result, and proposed correction where needed.
- Per-check results: `PASS`, `FAIL`, `WARNING`, `NOT VERIFIED`, or `NOT APPLICABLE`.
- Overall decision and the exact outstanding corrections or missing checks.

Use `FAIL` overall when a confirmed mandatory requirement fails. Otherwise use
`NOT VERIFIED` when a required criterion, measurement, or visual check is missing.
Use `PASS WITH WARNINGS` only when mandatory checks pass and remaining findings
are advisory; use `PASS` when all applicable requirements are verified and pass.
Do not downgrade a failed requirement to a warning because the image looks good.

A pass applies only to the recorded bytes, requirements, and inspection scope; it
is not a guarantee of a physical press result. Mention printer proof/acceptance
only when applicable, without inventing an extra approval gate for every task.

## 5. Corrections and handoff

For an authorized correction, prefer the editable source or a targeted,
color-aware fixup. Preserve the prior revision. Do not silently rasterize the page,
convert every spot ink, flatten all transparency, enlarge the artwork to invent
bleed, or claim upsampling restored missing detail. Follow printer settings.

After a change, regenerate evidence for the new file, rerun affected checks plus
file integrity and all-page visual inspection, and update its hash. Old reports
must not be reused as approval of changed bytes. Return a brief decision, report
link, and highest-priority findings. Route composition changes to `flyer-design`.
