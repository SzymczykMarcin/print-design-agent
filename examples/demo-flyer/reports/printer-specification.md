# Printer specification

Selected with user authorization; checked 2026-09-20.
Source: [Print24 flyer product and production FAQ](https://print24.com/uk/printing-products/flyer).

| Parameter | Target | Basis |
| --- | --- | --- |
| Product | A5 portrait, one-sided, 135 gsm coated art paper, CMYK | Demo selection from offered options |
| Trim | 148 x 210 mm | A5 product |
| Bleed | 2 mm on every edge | Published flyer FAQ |
| Artwork page | 152 x 214 mm | Trim plus required bleed |
| Raster resolution | At least 300 PPI at placement | Published minimum |
| Colour | CMYK, ISO Coated v2 (Fogra 39 L) | Published coated-paper requirement |
| Format | PDF | Accepted file format |
| PDF/X | Not mandated on the selected product page | Do not claim PDF/X certification |
| Safe inset | 5 mm inside trim | Project policy; printer warns against edge proximity |
| Finishing | None; no fold, foil, cut path, varnish or imposed sheet | Demo selection |

Use the exact ISO Coated v2 (ECI) profile supplied with CorelDRAW, not merely a
similarly named FOGRA39 profile. Record the embedded profile hash in the audit.
The cited product page does not specify a numeric ink ceiling. Adopt 330% as the
project ceiling corresponding to this profile and measure actual local coverage;
this is a documented production assumption, not an invented Print24 quotation.

The file is a public fictional example. No order, upload or printer proof is
requested. A real order must use matching paper, size and print configuration;
changed specifications require another preflight. Screen review is not a contract
colour proof.
