# Sources and design rationale

Original references checked on 2026-09-19; creative-direction research extended on 2026-09-20. Consult only the source relevant to the current question. Platform specifications and application commands require rechecking when used.

## Design and communication

- [Adobe: anatomy of effective flyers](https://www.adobe.com/express/learn/blog/the-anatomy-of-great-flyer-designs-8-winning-templates-to-get-you-started) — concise information, relevant imagery, hierarchy, and action.
- [Adobe: poster layout](https://www.adobe.com/express/learn/blog/poster-layout-design) — viewing context, focal hierarchy, and adaptation instead of proportional resizing.
- [Nielsen Norman Group: good visual design](https://www.nngroup.com/articles/good-visual-design/) — grids, typographic systems, purposeful imagery, and color. Its examples concern interfaces; apply the principles selectively to promotional print.
- [Butterick: typography rules](https://practicaltypography.com/summary-of-key-rules.html) — body-text size, leading, and line length as starting points. These are not blanket rules for display typography.
- [Mailchimp: campaign copywriting](https://mailchimp.com/resources/how-to-copywrite-for-marketing-campaigns/) — audience, benefits, direct language, and clear action.
- [LinkedIn: single-image ad specifications](https://www.linkedin.com/help/linkedin/answer/a427596/) — an example of placement-specific dimensions, cropping, and text constraints.
- [DENSO WAVE: QR symbol area](https://www.qrcode.com/en/howto/code.html) — real symbol geometry and clear space, for QR asset generation and placement.

## Creative direction: additional primary sources

- [Adobe: five design strategies](https://www.adobe.com/express/learn/blog/the-key-to-better-graphic-design-and-five-design-strategies) — emphasis through scale, color, type character and placement. Informs using display type and image relationships deliberately instead of treating all text as neutral labels.
- [Canva: compositional flow and rhythm](https://www.canva.com/learn/flow-and-rhythm/) — connections between focal points, directional repetition and human gaze. Informs evaluating how attention travels through a composition, not only whether its blocks align.
- [Pentagram: MIT Media Lab](https://www.pentagram.com/work/mit-media-lab) — a documented institutional identity using a shared grid and typographic consistency to support distinct expressions. A case study of creative scope within constraints, not a flyer template or permission to alter a client logo.
- [Pentagram: The Public Theater](https://www.pentagram.com/work/the-public-theater) — promotional work whose typographic expression responds to its cultural context and changes over time. A contrasting case study, not a prescription for loud type in every project.

The skill's workflow and review questions are an original synthesis of these
principles and the repository's observed failure: a readable, technically valid
export was mistaken for a convincing design. These sources do not certify the
quality of any generated result. Inspect relevant visual examples during a real
design task; do not imitate one studio's style or download its assets for reuse.

## Inspiration, not an imported skill

[Anthropic canvas-design](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md) inspired the separation of visual direction, composition, and refinement.

This skill is independently written for promotional communication. It does not copy the upstream prose or bundle its fonts, assets, or code. In particular, it does not adopt the upstream minimal-text ratio, art-object framing, restricted output formats, assumed font path, or fictional user feedback.

The upstream skill has its own [Apache-2.0 license](https://github.com/anthropics/skills/blob/main/skills/canvas-design/LICENSE.txt). If source material is incorporated later, review its notices and attribution requirements at that time.

## Application references

- [CorelDRAW automation](https://community.coreldraw.com/sdk/w/articles/217/controlling-coreldraw-or-corel-designer-applications-from-other-processes) — verify support in the actual installed edition and version.
- [Inkscape installation](https://wiki.inkscape.org/wiki/Installing_Inkscape) and [stable downloads](https://inkscape.org/release/).
- [Microsoft winget Inkscape package](https://github.com/microsoft/winget-pkgs/tree/master/manifests/i/Inkscape/Inkscape).
- [Homebrew Inkscape cask](https://formulae.brew.sh/cask/inkscape).
- [Inkscape CLI](https://wiki.inkscape.org/wiki/Using_the_Command_Line) — prefer the installed executable's help when examples differ by version.

Technical print-release documentation belongs to the separate print-preflight skill. Here, supplied print dimensions and templates are design inputs; no production conformance is claimed.
