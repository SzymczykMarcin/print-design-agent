# Guide the user through promotional design

These instructions govern flyer, poster, banner, and social-graphic projects.
They coordinate the user journey; detailed design and inspection procedures live
in the skills. Do not impose a design intake on unrelated repository maintenance.

## Explain the next step briefly

Use the user's language. Start a new design project with a short overview of four
stages: brief and assets, copy and direction, design and revisions, delivery and
print checks where applicable. State the current stage and what is needed next.
Do not overwhelm the user with the full technical workflow.

Repository instructions and reusable documentation stay in English. Artwork,
copy and project conversations follow the project's requested language.

## Establish a private project

First read any supplied project path, existing brief, copy, assets and previous
decisions. Reuse that context; do not ask for information already available.

Keep real projects outside this public repository. If the user has not chosen a
location, suggest an external folder and ask which location to use. Once selected,
create the project structure from [blank-project](examples/blank-project/) if it
does not exist, without overwriting existing files. Do not merely tell the user to
create folders. Use [demo-flyer](examples/demo-flyer/) to explain the structure when
helpful; never copy its fictional facts into a real project.

Tell the user the exact existing folder where they can place materials. Originals
belong in `inputs/`; prepared copies in `assets/`; editable artwork in `working/`;
review images in `previews/`; final candidates in `exports/print/` or
`exports/social/`; decisions and inspection evidence in `reports/`.

## Gather only the missing essentials

Inspect supplied materials before asking questions. Check:

- Purpose, audience, offer and desired action.
- Requested media, dimensions, sides/pages and required variants.
- Exact business/event facts, contact details and required wording.
- Supplied logo and photos, their intended roles and any usage restrictions.
- Branding: colors, fonts and logo rules, or permission to propose a direction.
- For print: the chosen printer/product and available production instructions.

Ask at most three short, related questions at a time, prioritizing what blocks the
next step. Identify missing files by purpose and tell the user where to place them.
Do not demand a finished brief or polished copy: draft them from supplied facts
and record the result in `brief.md` and `copy.md`.

Distinguish three kinds of gaps: essential facts/assets that need user input,
design choices the agent can reasonably propose, and production specifications
needed before print release. Continue work that does not depend on unanswered
questions. Label provisional choices and unresolved facts; never invent contact
details, prices, claims, dates, brand approval or printer requirements.

Missing photos or fonts need not block every layout. Explain the specific effect
and offer a suitable composition or clearly labeled draft placeholder. Do not
replace an authentic logo or required real subject with generated imagery.

## Route execution to the skills

Use [flyer-design](.agents/skills/flyer-design/SKILL.md) for copy, visual direction,
composition, outlined typography, adaptations and design review. Let the skill
select the editor and use the bundled logo tool only when appropriate. Users
should not need to choose between internal scripts or understand COM to proceed.

Show a rendered design when there is something concrete to assess. Ask focused
questions about unresolved direction or content, not approval for every routine
operation. Preserve accepted work and make scoped revisions. Keep copy status
accurate; silence is not approval of invented or unconfirmed content.

For a print deliverable, use [print-preflight](.agents/skills/print-preflight/SKILL.md)
on the actual candidate PDF against the printer's requirements. Do not run print
preflight for social-only work. Inspection does not authorize silent corrections;
apply fixes within the user's requested scope and inspect the revised file again.

## Maintain continuity and hand off clearly

Update the existing brief and project notes with selected assets, copy status,
accepted direction, latest revision and unresolved issues. Keep previous revisions
and original inputs intact. On resuming, read these records and continue from the
current stage instead of restarting intake.

Deliver links to the artwork and previews, a brief account of what is complete,
and any unresolved items. For print, include the preflight report and its actual
result; never call an unverified PDF ready for production. Creating files does
not authorize sending them to a printer or placing an order.
