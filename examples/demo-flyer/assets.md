# Asset register

Retrieved and inspected: 2026-09-19. Assets retain their own rights; they are not
relicensed under the repository's MIT code license. Paths below are project-relative.

## Logo

- File: `inputs/logos/lodziarnia.svg`.
- Source: user-selected ice-cream-shop logo from the logo-vectorizer project's
  `test-data/logos/results/simplified-verification/lodziarnia/lodziarnia.vector.svg`.
- Preparation: existing VTracer no-cleanup result; copied byte for byte,
  not retraced. Original tracing source was `lodziarnia.png`.
- Format: SVG, 1280 x 1280 source canvas; paths, no embedded raster or live text.
- Wording: LODZIARNIA / SMAK LEPSZYCH DNI.
- Review: the earlier preview was visually inspected; the mark has small trace
  irregularities. Keep it unchanged and inspect its tagline at final placement.
- Permission: included at the repository owner's explicit request for this example.
  Original authorship and a transferable third-party reuse license were not supplied;
  no general license to reuse the logo or trademark is asserted here.
- SHA-256: `dd85f8592fe4dc8fdcb18a0a408cc8378ca829d5e3c203117e0805a82ad3b089`.

## Photograph

- File: `inputs/photos/ice-cream-moment.jpg`.
- Photographer: Isadora Tricerri.
- Source: [A Woman Eating an Ice Cream, Pexels photo 13979845](https://www.pexels.com/photo/a-woman-eating-an-ice-cream-13979845/).
- Download: [original-size JPEG](https://images.pexels.com/photos/13979845/pexels-photo-13979845.jpeg?cs=srgb&dl=pexels-isadora-tricerri-24040026-13979845.jpg&fm=jpg).
- Terms: [Pexels License](https://www.pexels.com/license/), checked 2026-09-19.
  Free use, including promotional materials; attribution is not required.
  The credit here records provenance and is not mandatory artwork copy. No affiliate links.
- Restrictions include no implied endorsement, offensive portrayal, unaltered resale
  or redistribution through stock/wallpaper platforms. This is one design-example
  input, not a stock collection. The photo is not part of the logo or trademark.
- Subject: a person visibly eating soft serve, with warm clothing colors and a busy
  indoor background. This is a lifestyle reference, not evidence of this shop's product,
  premises or customers. Do not add a testimonial beside the person's image.
- Dimensions: 3451 x 5000 px, RGB; downloaded with the stock's sRGB option.
  Original download retained without resizing, upsampling or metadata-only DPI changes.
- Uncropped size at 300 PPI: 292.2 x 423.3 mm.
  Recalculate effective PPI from retained pixels for the actual crop and placement.
- Visual review: face, hand and ice cream are visible; keep them together when cropping.
- SHA-256: `f77e2fd93a5b8d54042b867b7cce227b3aa57a6a9d1d03600e3a123b8dbc893b`.

## Fonts

- Files: `inputs/fonts/Lato-Regular.ttf` (400), `inputs/fonts/Lato-Bold.ttf` (700).
- Source: [Google Fonts Lato directory](https://github.com/google/fonts/tree/main/ofl/lato).
- Original author: Lukasz Dziedzic / tyPoland; original copyright notice is preserved.
- License: SIL Open Font License 1.1, bundled unchanged in `inputs/fonts/OFL.txt`.
  Keep that license with redistributed font files. Fonts are not MIT-licensed.
- Files downloaded unmodified from Google Fonts; font parsing and English/Polish
  letter coverage verified. Editor installation and text outlining belong to design setup.
- Lato-Bold.ttf SHA-256: `8a0aace75d33794eece4b28187bfc1df0bbd2888b5d8a56e01788c8d65d16be1`.
- Lato-Regular.ttf SHA-256: `d636e4683231f931eda222d588e944d082bfd3bdba02f928bee461c0f185b251`.

## Additional display fonts

Retrieved 2026-09-20 from the official Google Fonts repository:

- `inputs/fonts/pacifico/Pacifico-Regular.ttf`: Pacifico Regular;
  [source and authorship](https://github.com/google/fonts/tree/main/ofl/pacifico).
- `inputs/fonts/bebasneue/BebasNeue-Regular.ttf`: Bebas Neue Regular;
  [source and authorship](https://github.com/google/fonts/tree/main/ofl/bebasneue).

Each directory includes its original SIL Open Font License. Fonts remain separate
from the repository's code license. Corel resolved Pacifico, Bebas Neue and Lato by
name; native outlining and the rendered Polish glyphs were checked. Lato Bold is
retained as an original input but is not used in this revision.

## Revision v02 usage

Photo: original 3451 x 5000 pixels, placed 180 x 260.794 mm at (-34, -12) mm
relative to the bleed-page top-left. Vector overlays hide the unused right/lower
areas; the actual PDF placement is 486.97 PPI on both axes. No upsampling.
The self-contained SVG embeds the original JPEG. Corel's PNG export had a mean
0.119/255 channel difference from the original; packaging restores the original
JPEG instead of retaining that unnecessary PNG conversion. The reopened SVG was
visually compared with the native composition. Print conversion is perceptual
sRGB to ISO Coated v2 (ECI), performed by Corel; the PDF stores CMYK photo pixels.
Original logo and photo hashes remain unchanged.
