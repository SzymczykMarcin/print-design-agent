# Print preflight — v02

**Result: PASS WITH WARNINGS.** Technical release for the documented fictional demo;
not approval of the invented business facts for real advertising.

## Released file

- `../exports/print/flyer-a5-front-v02.pdf`
- One single-sided A5 flyer: 148 x 210 mm trim; 152 x 214 mm including bleed.
- 35,526,900 bytes; PDF 1.7.
- SHA-256: `ceba624370eddbf92339e7062dad7ed7ffc6bad6ef2dfbb2afde0bf0131694db`.
- Target: Print24 coated-paper flyer, 135 gsm, four-colour, no finishing.
- Requirement source and assumptions: [printer specification](printer-specification.md),
  checked 2026-09-20 with the user's authorization to select the demo target.

## Evidence and checks

The checks apply to the exact released bytes. Numeric evidence is in
[measured-evidence-v02.json](measured-evidence-v02.json); native type measurements
are in [typography-v02.json](typography-v02.json).

| Check | Observation | Result |
| --- | --- | --- |
| Integrity | Strict pypdf parsing and successful Poppler/Ghostscript rendering; no encryption, annotations, forms, attachments or JavaScript | PASS |
| Page count and orientation | One portrait page; rotation 0, unit scale 1; no social pages or imposed sheet | PASS |
| Geometry | Trim 148 x 210 mm; explicit 2 mm bleed on all sides, matching full MediaBox/CropBox | PASS |
| Actual bleed | Photo, cream and cocoa shapes cover page edges; full-bleed render inspected for blank strips and clipping | PASS |
| Safe placement | All newly typeset blocks at least 5.281 mm inside trim; logo remains inside the safe region | PASS |
| Photo resolution | One 3451 x 5000 CMYK image; actual transformed placement 486.974 PPI on both axes; original source dimensions retained | PASS |
| Vector integrity | 494 path-paint operations; photo is the only raster object; logo and type remain paths | PASS |
| Outlined text | 11 native text blocks converted by Corel; reopened CDR and SVG checked; zero PDF text-show operations including nested forms | PASS |
| Outline fidelity | Before/after renders compared: mean difference 0.948/255, 1.84% pixels changed; visual check confirms matching glyphs, position and wording | PASS |
| Colour | All image and vector spaces use 4-component ISO Coated v2 (ECI); no RGB operators, spot colours, registration colour, patterns or shadings | PASS |
| Output intent | Embedded profile is byte-identical to the actual conversion profile; hash below | PASS |
| Ink load | Full-resolution CMYK image maximum 327.059%; vector paint maximum 299.21%; profile-aware 600 PPI process render maximum 327.059%, below the project ceiling of 330% | PASS |
| Overprint | Explicit fill/stroke overprint false and OPM 0; process render inspected; no white-overprint or unintended knockout issue | PASS |
| Transparency | No soft masks, alpha graphics states, transparency blend modes or effects requiring flattening | PASS |
| PDF standard | Ordinary PDF accepted by the selected product page; PDF/X conformance is not required and is not claimed | NOT APPLICABLE |
| Finishing / QR | No varnish, foil, die-cut, folding, duplex order or QR code requested | NOT APPLICABLE |
| Final appearance | Trim, bleed and enlarged lettering reviewed; photo subject intact; copy matches copy.md, including Polish diacritics and demo notice | PASS |
| Physical colour proof | No contract proof or press sample requested; screen preview is not colour binding | WARNING |
| Logo trace | Existing supplied vector trace retained, including minor irregularities and its small secondary slogan; no claim of a newly mastered brand mark | WARNING |

## Conversion correction

Corel's initial relative-colorimetric conversion produced a peak near 333%.
The final export uses perceptual conversion to the same ISO Coated v2 profile;
its measured peak is 327.059%. This is genuine colour conversion, not profile
relabeling, image upsampling or page rasterization.

Profile SHA-256:
`128dc02f7246cc3807af0323695379f64151a8f27a587736acc59f8b6ce894b8`.

## Tools and scope

CorelDRAW 2024 25.2.1.313 provided native outlining, reopened CDR verification and
CMYK PDF export. The shared Poetry environment provided pypdf 6.19.0, Pillow and
NumPy; Poppler inspected and rendered the PDF. Ghostscript 10.03.1 rendered CMYK
process channels with the exact destination profile at 600 PPI. Full-resolution
image-channel and vector-paint checks supplement the sampled separation render.
The audit script is `../working/inspect_flyer.py`.

Advisories above do not conceal a missing mandatory file check. This release is
specific to the documented product and paper assumptions. No printer upload or
order was performed. The address, opening hours and offer remain fictional demo
content, visibly identified in the artwork.
