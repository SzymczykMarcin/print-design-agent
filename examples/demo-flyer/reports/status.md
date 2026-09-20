# Demo delivery — v02

One Polish, single-sided A5 flyer. The earlier multi-format outputs were removed
at the user's request; original photo, logo and existing fonts were preserved.
The new direction, copy and brandbook replace the previous restrained example.

## Open the result

- [Print PDF](../exports/print/flyer-a5-front-v02.pdf)
- [Trim preview](../previews/flyer-a5-front-v02.png)
- [Bleed preview](../previews/flyer-a5-front-v02-bleed.png)
- [CorelDRAW source](../working/flyer-a5-front-v02.cdr)
- [Self-contained SVG source](../working/flyer-a5-front-v02.svg)
- [Print preflight](print-preflight-v02.md): PASS WITH WARNINGS.

## Design review

The person and ice cream attract attention; an organic cream panel and strawberry
field connect the photograph to the large headline. Cocoa anchors the invitation
and visit details. Pacifico and Bebas Neue create a youthful voice; Lato provides
clear practical information. The design was built from real assets, native text
and editable vector shapes, without generative imagery.

Corrections after rendering: repaired Corel's SVG import origin and namespace
handling; outlined actual named text objects; reduced the logo to recover clear
space; increased headline/CTA scale; separated the script descender from the bold
headline; moved the demo notice fully inside the safe inset. Corrected excessive
ink coverage through the documented profile conversion.

Overview, close-up lettering, trimmed page and full bleed were reviewed. Saved CDR
was reopened and exported; packaged SVG was independently reopened by resvg. The
sources agree in composition. Screen RGB and CMYK-render previews differ in colour;
neither is a contract proof. Original JPEG remains embedded in the portable SVG.

Copy is authored fictional demo content, not approved for a real business. Further
user design feedback is still welcome; technical release is not a claim of aesthetic
approval. A poster or social version would be a separate task.

## Rebuild

Use the shared root Poetry environment. Native CorelDRAW with the bundled fonts
and ISO Coated v2 (ECI) is needed for this example's recorded recipe.

1. `poetry run python examples/demo-flyer/working/compose_flyer.py`
2. Run `examples/demo-flyer/working/export-corel.ps1` in PowerShell.
3. Run `poetry run python examples/demo-flyer/working/inspect_flyer.py --help`, then
   supply the installed Poppler directory, Ghostscript executable, exact ICC file
   and a temporary scratch directory. The script audits a candidate; it does not
   automatically approve the design or release it.
4. Review new renders and audit evidence. Only a passing file may replace a release,
   under a new revision and with a matching hash. Temporary live-text assembly and
   before/after comparison PDFs are rebuild artifacts, not delivered masters.

Photo/ICC separations and comparison renders used only for inspection stay outside
the public delivery. Prepared-photo copies are unnecessary here because the original
photo is embedded directly; the example does not keep empty asset folders merely
to fill a template. Asset rights and font licenses are recorded in `../assets.md`.
