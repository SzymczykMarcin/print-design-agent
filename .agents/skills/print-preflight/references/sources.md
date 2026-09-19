# Sources and maintenance

Reviewed 2026-09-19. These are primary printer, standards-community, vendor and
tool-maintainer references. Recheck the selected printer's current product/order
instructions for each job; the links below are not universal production settings.

- [Drukomat: preparing a project for print](https://www.drukomat.pl/blog/zlecasz-projekt-do-druku-na-to-zwroc-uwage/) — format, bleed and printer-facing preparation.
- [Drukomat: A3 six-panel Z-fold instructions](https://www.drukomat.pl/instrukcje/drukomat_ulotka_skladana_A3_6_113.pdf) — example of a specific product template, not a default for other flyers.
- [Ghent Workgroup: Commercial Print](https://gwg.org/commercial-print/) — job-oriented specifications built on PDF/X; distinguish standard conformance from product checks.
- [PDF Association: PDF/X in a Nutshell](https://pdfa.org/resource/pdfx-in-a-nutshell/) — PDF/X purpose and variants.
- [Adobe: analyzing documents with Preflight](https://helpx.adobe.com/acrobat/using/analyzing-documents-preflight-tool-acrobat.html) — profile-based inspection of PDF contents.
- [Adobe: Output Preview](https://helpx.adobe.com/acrobat/using/previewing-output-acrobat-pro.html) — separations, overprint and ink-coverage inspection.
- [Adobe: output intents](https://helpx.adobe.com/acrobat/using/output-intents-pdfs-acrobat-pro.html) — intended output condition versus actual color conversion.
- [qpdf command-line documentation](https://qpdf.readthedocs.io/en/stable/cli.html#option-check) — structural checks and exit statuses; not a PDF/X validator.
- Poppler manuals distributed by Debian: [pdfinfo](https://manpages.debian.org/bookworm/poppler-utils/pdfinfo.1.en.html), [pdfimages](https://manpages.debian.org/bookworm/poppler-utils/pdfimages.1.en.html), [pdffonts](https://manpages.debian.org/bookworm/poppler-utils/pdffonts.1.en.html) — geometry, image ppi and font inventories; verify flags in the installed version.

The outlined-text policy comes from this repository's flyer workflow, not a claim
that PDF/X universally requires outlines. The report statuses and evidence rules
are this skill's operational conventions, not a certification issued by a printer.
