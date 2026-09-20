# Print preflight: v01

**Overall: NOT VERIFIED for production release.** The measurable exercise geometry,
image detail and outlined-text requirements pass. No printer/product specification,
press profile, ink limit or PDF/X validation profile was provided.

## Identity and scope

- Candidate: [flyer-a5-front-v01.pdf](../exports/print/flyer-a5-front-v01.pdf).
- SHA-256: `14212a7e89549eb6d3be4652620b49d84af56d1b1830d651ac5cc2d99216e2b1`.
- Size: 13360424 bytes; one portrait page; unencrypted; no annotations.
- Requirements: `brief.md` exercise assumptions (A5, 3 mm bleed, 5 mm safe inset,
  300 effective PPI). These are not printer-approved requirements.
- Tools: CorelDRAW 2024 / PDF Engine 25.2.1.313; pypdf 6.19.0 for boxes and recursive
  content/image inspection; Poppler pdfinfo/pdftoppm for structure and PDF rendering.
  Exact native version and measurements: [JSON evidence](measured-evidence-v01.json).
- Render evidence: [trim](../previews/flyer-a5-front-v01.png) and
  [full page with bleed](../previews/flyer-a5-front-v01-bleed.png).

## Findings

| Check | Required / expected | Observation and evidence | Result | Action |
| --- | --- | --- | --- | --- |
| File opening | Parse and render page 1 | pypdf, pdfinfo and pdftoppm succeeded; one page; no annotations/encryption | PASS | No structural failure observed; not a PDF/X validator |
| Trim geometry | 148 x 210 mm | Explicit TrimBox from (3,3) to (151,213) mm; numerical rounding below 0.001 mm | PASS | Confirm printer product |
| Bleed geometry | 3 mm all edges | MediaBox/BleedBox 154 x 216 mm; explicit inset TrimBox | PASS | Confirm printer bleed requirement |
| Bleed content | Artwork reaches all bleed edges | Photo extends through top and sides; cream background fills lower sides and bottom; inspected full-page render | PASS | None for exercise |
| Safe placement | Essential artwork at least 5 mm inside trim | Text starts 9 mm inside left trim; logo shifted upward after review; source geometry and final trim render checked | PASS | Physical-size proof still advisable for fine logo lettering |
| Image detail | At least 300 PPI for exercise | Single 3451 x 2353 px photo; measured placement 569.2 x 569.2 PPI; source crop retained without upsampling | PASS | None |
| Text as curves | No live promotional text | Reopened CDR has zero text shapes; SVG has no text nodes; recursive PDF inspection finds zero text-show operators and 485 path-paint operators; rendered lettering reviewed | PASS | Keep copy.md and font recipe for revisions |
| Copy and appearance | Match the fictional demo | Headline, offer, CTA, address, hours and demo notice checked against copy.md; photo action and logo intact | PASS | Fictional content is not approved for a real campaign |
| Color workflow | Printer-specific | Embedded sRGB ICC color spaces; no output intent; no production CMYK conversion asserted | NOT VERIFIED | Obtain accepted color workflow and output profile |
| Overprint / transparency | Printer-specific | Inspected page graphics states disable fill/stroke overprint; no opacity state found there; ordinary RGB rendering only | NOT VERIFIED | Perform production separations/overprint inspection |
| Total ink coverage | Printer/profile-specific | No press profile, limit or separation-aware measurement | NOT VERIFIED | Check with the selected production profile |
| PDF/X | Requested variant and real conformance validation | No variant supplied and no conformance validator run | NOT VERIFIED | Validate only the required standard after export |
| QR / special finishing | Not requested | No QR, cut contour, spot varnish, foil or fold | NOT APPLICABLE | None |
| Physical proof | Fine traced logo lettering | Visually intact but small, with inherited trace irregularities; no printed sample examined | WARNING | Review a physical proof before real distribution |

No claim of press readiness is made. This report applies only to the hash above.
A different PDF, revised content or printer specification requires a new inspection.
