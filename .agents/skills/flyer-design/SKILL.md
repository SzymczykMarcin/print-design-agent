---
name: flyer-design
description: Design or revise promotional flyers, posters, banners, and social media graphics from a brief, real assets, and brand guidelines. Covers copy, art direction, editable composition, visual review, and format adaptations. Does not perform print preflight or certify press-ready PDFs.
---

# Flyer Design

Create a promotional piece that communicates a specific offer to a specific audience and gives them a clear next action. Prioritize flyers; adapt the method to posters, banners, and social graphics. Deliver an editable design and inspect its rendered appearance.

## Scope and working context

- Handle communication, copy, composition, asset treatment, and adaptations. Respect supplied production dimensions and templates while designing.
- Leave PDF/X validation, ICC conversion, ink limits, separations, and technical release checks to a separate print-preflight workflow. Do not call a review PDF "print-ready".
- Use the user's project directory and existing organization. In this repository, projects belong in the external workspace: originals in `inputs/`, derivatives in `assets/`, editable designs in `working/`, previews in `previews/`, and decisions in `reports/`. Do not put client work into the skill or public examples.
- Read existing brief, copy, brand assets, and accepted designs before asking questions. Ask only about missing information that changes the design or blocks delivery; continue independent work.
- Make a narrow revision when requested. Preserve accepted elements instead of restarting the whole process.

## 1. Establish the design brief

Identify the audience, offer, communication goal, distribution context, primary action, format, and necessary content. Establish whether the piece is read in the hand, from a distance, or on a phone.

Before laying out a print piece, establish trim size, bleed on each edge, safe content insets, page sides, and any fold or finishing template. Use supplied production requirements; record missing values as draft assumptions rather than printer-approved settings. See [document geometry and image sizing](references/design-decisions.md#document-geometry-and-image-sizing).

Treat supplied facts, brand rules, and required text as constraints. Record unresolved dates, prices, contacts, claims, and dimensions; never invent them. Missing factual content may use conspicuous placeholders in a draft, but must not silently enter a finished deliverable.

Inspect actual source images and logo variants. Choose the lead image for its relevance, clarity, crop options, and useful negative space. Keep subjects recognizable. Prefer original vector logos; do not redraw, recolor, stretch, or regenerate the mark to fit a concept.

When a raster-only logo needs editable paths or scalable artwork, use the bundled
[logo-vectorizer](../../../tools/logo-vectorizer/README.md). Follow the
[logo preparation procedure](references/tools.md#prepare-a-raster-logo) before
placing its SVG. Keep a suitable existing vector or raster when tracing offers no
benefit; never regenerate brand identity to compensate for a poor trace.

Record a compact working brief in the project's existing brief or notes: main message, first thing to notice, supporting proof, action, chosen assets, and format. Avoid a long design manifesto.

## 2. Shape the message

Build a reading order appropriate to the brief:
- **Attention:** a specific headline or unmistakable subject.
- **Value:** the benefit or offer and the evidence supporting it.
- **Action:** what to do next, with the information needed to do it.

For an event, include the relevant who, what, when, where, and reason to attend. For a service or product, explain the benefit and how to inquire or buy. Use the audience's language, not internal design vocabulary.

Edit for clarity and factual fidelity. Separate proposed rewrites from approved copy. Do not manufacture testimonials, discounts, scarcity, or credentials. Preserve required qualifications. If content does not fit, simplify with the user's intent intact, redistribute it, or propose a larger/two-sided format before shrinking everything.

Use one primary call to action; keep necessary secondary contact information subordinate. A QR code supports a real action and needs a readable explanation or alternative contact route. Generate it with a real tool, never draw an approximation.

## 3. Choose a visual direction

Read [composition and adaptations](references/design-decisions.md) when selecting a layout or changing medium.

If brand guidance is incomplete, establish a provisional design system from supplied assets: palette with color values, available font families and weights, text styles, and logo variant/clear-space rules. Record it in the project brief, distinguish supplied rules from proposed choices, and apply it consistently across formats. Do not present sampled logo colors as official specifications or invent brand approval.

Define a brief visual direction: image treatment, typographic character, palette, hierarchy, grid, and balance of content and space. Explain choices through the audience, offer, assets, and brand. Use references for principles, not copied artwork.

Explore materially different directions when the brief calls for exploration or remains ambiguous. For a clear brief, proceed with a reasoned direction; do not force a fixed number of concepts or an approval checkpoint at every stage.

Sketch the information structure before adding decoration. Let the real image and message drive the layout. Neither a mandatory minimalist style nor a fixed image/text ratio is appropriate for every flyer.

## 4. Build an editable composition

Read [tools and capability placeholders](references/tools.md) before selecting a backend or when a required operation lacks a reliable tool.

Prefer the user's working CorelDRAW installation where usable. Otherwise use Inkscape; if missing, install it as described in that reference, within the host's permission rules. Use CorelDRAW directly through documented COM scripting on Windows, or author editable SVG and use Inkscape CLI/actions. Write project-specific scripts as needed; no custom adapter or fixed set of layout operations is required. No Corel-specific path, account, MCP server, or paid application is required by this skill.

- Save a native editable source: CDR when genuinely created by CorelDRAW, SVG for Inkscape. Never disguise a format by renaming its extension.
- Keep outlined text, logos/vectors, and photographs separate, with meaningful object or layer names. Compose text with real fonts, then convert each laid-out block to curves using the editor before treating it as artwork for review or delivery. Follow [text-to-curves](references/tools.md#convert-typeset-text-to-curves); do not defer outlining to print preflight.
- Keep originals unchanged. Use prepared copies for cropping, masking, and retouching.
- Use fonts actually available to the renderer, with the required language glyphs and weights. Follow brand requirements; disclose a missing font instead of silently substituting it.
- Prefer deterministic placement and typography. Image generation may supply an optional background or illustration where suitable; it must not replace required authentic subjects, logos, or typeset copy.
- Use consistent alignment, grouping, spacing, and a deliberate hierarchy. Check text against busy photo regions and avoid incidental tangencies.
- Calculate effective image resolution from retained source pixels after cropping and final placed dimensions, using [image sizing](references/design-decisions.md#document-geometry-and-image-sizing). Compare with the project requirement; use a better source, smaller placement, or revised crop when insufficient. Neither DPI metadata changes nor upsampling recover missing original detail.
- Record crop, font, and asset choices sufficiently to reproduce edits. Package or embed linked images so the source can be reopened; respect font redistribution restrictions.

Use the smallest reliable toolchain. A missing convenience script is not a reason to abandon a task that a verified installed tool can complete.

## 5. Render, assess, and refine

Export a preview from the actual editable source with text converted to curves and inspect it. Reasoning about source coordinates alone is insufficient.

Review at three useful scales: thumbnail for hierarchy, intended viewing size/context for legibility, and close-up for craft. Physical-size judgment on an uncalibrated screen is approximate; request or recommend a sample print when needed.

Check:
- Can the intended viewer identify the offer and next action without explanation?
- Does the first glance land on the intended subject or message?
- Are required facts, logo, contacts, and copy intact?
- Are hierarchy, alignment, line breaks, contrast, spacing, and photo crops intentional?
- Is any text clipped, substituted, lost against imagery, or made too small to fit?
- Does the result feel specific to this brand and material rather than like a generic web card layout?
- Are the editable source and rendered preview consistent?

Proofread the rendered artwork against the current approved `copy.md`, block by block: omissions, spelling, diacritics, dates, prices, phone numbers, addresses, URLs, and qualifications. Check the same facts across all sides and adaptations. Decode any QR from the rendered output and compare its payload with the supplied destination. Outline paths cannot reliably be text-extracted; OCR can assist but does not replace the visual comparison. If copy is not approved, keep its status explicit.

Correct the dominant weakness and re-render the affected result. Prefer refining the composition to accumulating decorations. Do not repeat unchanged checks or claim visual review when no image was inspected. This is a design review, not technical print validation.

## 6. Adapt and hand off

Recompose each requested format around its viewing conditions. Preserve identity and message, but adjust crop, hierarchy, copy density, and CTA placement; do not simply stretch or shrink the flyer.

Reopen the saved CDR/SVG from its delivery location and render it again. Check image links, page dimensions, outlined text, masks, object placement, and agreement with the reviewed preview. Repair missing dependencies before delivery; if reopening is unavailable, record that specific check as unverified rather than claim a verified handoff.

Deliver the editable vector source, its matching text content and typography recipe, appropriate review previews, and requested digital exports. Explain that text in the design is editable as curves, not as live text. A PDF produced here is a design/review export pending technical print checks. Include a short project note with chosen fonts/assets, unresolved items, and intended dimensions/variants for the separate [print-preflight skill](../print-preflight/SKILL.md). If that skill is unavailable, state that status and still deliver completed design work.

Use versioned, descriptive filenames, such as `flyer-a5-front-v01.svg` and `flyer-a5-front-v01-preview.png`. Keep the working source and previews traceable to the same revision.

Report briefly what was designed, where the files are, and what remains unresolved. Do not expose tooling details in the artwork.

## Capability gaps and provenance

The placeholders in [tools.md](references/tools.md#capability-placeholders) are intentionally unimplemented integration points, not commands. Record only gaps actually encountered; use the specified fallback or explain the precise blocked operation.

This is an original promotional-design workflow informed by professional references and Anthropic's concept-then-refine approach. Read [sources](references/sources.md) when checking the basis of a recommendation or updating guidance.
