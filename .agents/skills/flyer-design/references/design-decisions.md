# Composition and format decisions

Read for art direction, text fitting, or adaptation to a different medium. These are decision aids, not universal templates.

## Flyer first

A flyer must reward both a quick glance and a closer read. Give the offer a clear entry point, group related information, and make the next action easy to locate. A large logo is not automatically the main message.

Choose the structure from the content:
- A strong photograph with usable negative space can carry a headline and a compact offer.
- A visually busy photograph often needs a separate text zone or a carefully controlled background treatment.
- A product or service comparison can use aligned rows or columns when comparison is the actual task.
- Front and back should have complementary roles: recognition and offer on the front, supporting detail on the back. Do not assume everyone turns the flyer over.
- For folded pieces, use the supplied panel template and reading sequence. Do not guess equal panel widths or folds through important content.

Remove unnecessary content before reducing readable type. If required content is still too dense, change the structure or explain the format constraint.

## Available design moves

Choose a small, coherent set of moves that expresses the idea. This is a vocabulary,
not a requirement to decorate every piece or adopt the same style in every sector.

| Lever | Possible use | Judgment to apply |
| --- | --- | --- |
| Scale and proportion | An oversized keyword, an intimate crop, a dominant product or a quiet detail | Establish a clear lead; do not make everything equally loud |
| Display typography | Condensed or expressive type, a weight/width contrast, purposeful line breaks | Match the voice; keep reading order and supporting details clear |
| Image/type relationship | Type beside, around or selectively overlapping an image; subject crossing a boundary | Protect important image detail and letter recognition; avoid accidental tangencies |
| Shape and silhouette | A geometric frame, irregular panel, cutout or shape echoing the offer | Give the form a reason; do not modify the logo to manufacture a motif |
| Rhythm and movement | Repeated marks, spacing changes, diagonals or a sequence of aligned elements | Lead attention through the message rather than scatter it |
| Color and texture | A focused accent, tonal field, vector hatching or a licensed texture | Preserve local text contrast and useful visual quiet |
| Negative space | An intentional pause around the focal point or between unequal groups | Make space active; do not leave a large region empty merely because composition stopped |

A business flyer can gain character from a precise typographic treatment, a strong
photographic viewpoint or a visual metaphor within a restrained palette. A leisure
brand can sustain more gesture and layering when the main message stays clear.
These are possibilities, not sector stereotypes; a client's reference can point in
a different direction.

## From reference to editable construction

Read a reference at two levels: its communication idea and its visual technique.
For example, excitement might come from a large headline interacting with a person,
not from the particular decorative swirls around them. Preserve that useful
relationship while choosing an original construction appropriate to the supplied assets.

- Use native clipping paths or masks for a subject crossing a shape. Inspect hair,
  hands, transparent edges and halos; keep the original photograph unchanged.
- Build waves, frames, gestures and icons as separate editable vector objects.
- Use a suitable licensed font for expressive lettering and outline after typesetting.
  Never simulate a headline by tracing letters from the reference bitmap.
- Use actual supplied or licensed product photographs for photographic collages.
  Do not imply that stock products or people are the client's products or endorsers.
- Build texture with native vectors or a sufficiently detailed licensed raster;
  keep it away from fine text when it weakens readability.

The image, typography and supporting marks should belong to one visual idea.
Separating a busy photo from copy is one valid technique, not a mandatory top-photo /
bottom-text template. Likewise, overlapping everything is not inherently creative.

## Selecting and challenging a direction

For an unresolved brief, use quick rendered studies to compare genuinely different
relationships: type-led, image-led or integrated composition, where relevant.
Reject the weakest approach before polishing fine details. Do not generate a fixed
number of variants when a supplied reference or accepted concept already resolves
the direction.

Evaluate the actual preview for attention, reading order, brand character,
distinctiveness and craft. A technically clean design can still fail the brief.
Name the specific failing relationship, change it and compare the new render.
One family and a grid can be expressive; adding more fonts or ornaments is not a
substitute for a stronger idea. Record provisional identity changes so the brief
and brandbook follow the chosen direction rather than freezing an early guess.

## Document geometry and image sizing

For print, distinguish three areas before composing: the final trimmed page,
artwork extending beyond it as bleed, and a safe region inside it for essential
content. Use explicit units and the supplied template's trim, fold, mounting, and
binding geometry. Extend edge-to-edge photographs/backgrounds through the bleed;
keep text, logos, and QR codes inside the specified safe region. Bleed and safe
insets are different values; neither has a universal size. If requirements are
missing, record provisional values and keep production status unresolved. Final
technical verification belongs to print preflight.

For each placed raster image, calculate resolution using the source pixels that
remain in its visible crop, before any artificial upsampling:

- `effective_ppi_x = retained_pixel_width / (placed_width_mm / 25.4)`
- `effective_ppi_y = retained_pixel_height / (placed_height_mm / 25.4)`

Compare both axes with the brief or printer's target. For example, a 1200-pixel-wide
crop placed at 100 mm provides about 305 ppi; at 200 mm it provides about 152 ppi.
Include bleed when measuring an image spanning the full bleed area. For rotated
images, use their physical dimensions before rotation, not the rotated bounding
box. Record the crop, placement, calculated resolution, and any deficit in project
notes. If no target exists, establish and label a working target appropriate to
the medium and viewing distance instead of treating 300 ppi as universal.

For digital output, check retained pixels against the requested export dimensions.
Vector text and logos are resolution-independent; embedded raster images are not.

## Typography and language

Build a small set of functional text styles: headline, supporting text, details, and CTA. One family with suitable weights can be enough, but it is not a default prescription for restraint. Use a contrasting display face or lettering when it strengthens the voice and emphasis; keep informational text easy to read. Existing brand rules govern the available choices.

Judge font size using the actual font, viewing distance, audience, and background. For body paragraphs, 10-12 pt and leading around 120-145% are useful starting points from Practical Typography, not mandatory values for every flyer. Short display lines and narrow promotional blocks need their own treatment; do not impose book-length line measures.

Use natural line breaks that preserve phrases, avoid stranded short words where the language requires it, and check local punctuation, diacritics, dates, currency, phone numbers, and nonbreaking spaces. Avoid excessively tracked paragraphs, stretched type, and tightly packed all-caps body copy. Thin reversed type needs especially careful visual judgment.

Retain exact copy in `copy.md` and record font family/version where available, weight, size, leading, tracking, alignment, text frame, and intentional line breaks in the project's working notes or generation script. These are the reconstruction source when outlined text changes. Re-typeset from that source instead of editing individual letter shapes to change wording.

Use installed fonts with the required glyph coverage. A brand font takes priority over a generic style preference. If it is unavailable, identify a substitution as a proposal rather than a faithful brand match.

## Images, color, and space

Choose the crop around the communication subject, leaving space where the text actually belongs. Preserve faces, product details, and useful context. Check masks at the edges; a poor cutout is not improved by adding a shadow.

Use contrast and whitespace to separate groups and establish emphasis. Contrast is local: sample or inspect the area behind text, not just the nominal background color. A digital contrast calculation can assist review but does not certify readability on paper.

Align to a coherent grid while allowing a deliberate focal exception. Keep recurring gaps and edges consistent. Do not make every element a box, use identical cards for unrelated content, or make every line bold. Decorative effects must support the concept.

## Medium adaptations

| Medium | Design decision |
| --- | --- |
| Handheld flyer | Support scanning and closer reading; keep the offer and action easy to find. |
| Poster | Design for viewing distance: fewer words, stronger focal point, and details appropriate to where people can stop. |
| Physical banner / roll-up | Account for viewing distance, extreme proportions, mounting, eyelets, hems, and concealed base areas using the supplied template. Do not assume a scaled-up flyer will work. |
| Social feed | Compose for a phone viewport; move supporting detail into the caption when permitted. Match the actual placement's current aspect ratio and crop behavior. |
| Stories / vertical placements | Keep essential content away from platform overlays using current placement guidance. Recompose instead of stretching a feed image. |
| Digital banner | Identify the placement, pixel size, and file constraints. Use a short message with a legible action; verify any file-size limit. |

Check current platform documentation for requested social placements. Organic posts, paid ads, profile grids, and shared thumbnails can crop differently. Do not treat a remembered pixel size or fixed safe-zone percentage as timeless.

In a later, separate adaptation task, reuse the accepted typography, palette, photo treatment and recognizable motifs while composing for that new format.

## Revision decisions

When feedback is vague, identify the likely failing layer: message, hierarchy, imagery, typography, density, or brand fit. Change that layer and retain successful work.

When the user requests exact copy or layout, preserve it; explain any unavoidable fit issue rather than silently editing or substituting. When fonts, assets, or facts are missing, complete the parts that do not depend on them and clearly distinguish a draft from a finished design.
