# Promotional design workflow

Apply this workflow to design tasks, not unrelated repository maintenance.
Use the user's language and concise replies; repository instructions stay English.
Start a new project with four stages: brief/assets, copy/direction, design/revisions,
delivery with print verification where applicable. State the current next step.

## Scope and intake

One material and target format per task. A two-sided flyer is one material; its
source, PDF and preview are representations of it. Posters, feed graphics, stories
and other adaptations are separate tasks that may reuse accepted work. If several
are requested, establish which comes first and record the rest for later. Do not
create other tasks without an explicit request.

Read existing project notes and supplied assets before asking questions. Establish
purpose, audience, offer/action, dimensions/sides, factual copy, logo/photos and
rights, brand rules, and printer/product requirements for print. Ask at most three
short questions at a time about missing essentials. Draft the brief and copy from
supplied facts; do not require the user to write them first.

Separate missing facts from proposed design choices and unresolved production
specifications. Label assumptions; never invent real business facts, approval or
printer requirements. Continue independent work while answers are pending. Explain
missing assets and possible draft alternatives without replacing authentic subjects.

## Project and environment

Real projects belong outside this public repository. Reuse the supplied location;
otherwise suggest one and ask which to use. Once selected, create missing folders
from [blank-project](examples/blank-project/) without overwriting files. Tell the
user the exact asset location. The [demo](examples/demo-flyer/) contains fictional facts.

| Location | Content |
| --- | --- |
| `inputs/`, `assets/` | Originals; prepared derivatives |
| `working/`, `working/print-candidates/` | Editable sources; unreleased PDFs |
| `previews/`, `reports/` | Review images; decisions and evidence |
| `exports/print/`, `exports/social/` | Verified production PDFs; final digital images |

Use one root Poetry environment and Python 3.12 for all tools, through `poetry run`.
On first setup or a dependency problem, follow [environment preparation](docs/environment.md)
and perform routine authorized installation yourself. No per-tool environments.

## Route, resume and deliver

- Use [flyer-design](.agents/skills/flyer-design/SKILL.md) for composition and visual
  review; use [print-preflight](.agents/skills/print-preflight/SKILL.md) to finish
  print delivery. Its release gate is mandatory; a draft PDF or report alone does
  not complete print preparation. Explicit audit-only requests remain read-only.
- Load only the active skill and reference sections needed for the current step.
  Do not preload every reference, source list or installation guide.
- Maintain existing `brief.md`, `copy.md`, `brandbook.md` and `reports/status.md`:
  accepted direction, copy approval, assets, current revision, next action and gaps.
  Record verified tool versions/paths privately and printer specs with source/date.
- Resume from those records. Reuse research and setup while inputs, requirements
  and environment remain applicable; recheck on changes, errors or stale evidence.
  Cached decisions never replace inspection of a new or changed deliverable.
- Show actual renders, make scoped revisions and preserve originals/accepted work.
  Ask about meaningful unresolved choices, not every routine operation; silence is
  not approval. Let the skills choose implementation tools.
- Hand off artifact/preview links and actual status. For print include the release
  report; unresolved mandatory checks mean incomplete preparation. Creating files
  does not authorize external uploads, sending to a printer or placing an order.
