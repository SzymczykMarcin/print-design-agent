# print-design-agent

A workshop for creating print flyers and social media graphics from real photographs, authentic logos, and brand guidelines.

**Status: design and print-inspection skills available.** The [flyer-design skill](.agents/skills/flyer-design/SKILL.md) covers promotional design and visual review. The workflow uses direct CorelDRAW COM scripting or editable SVG with Inkscape CLI. The standalone [logo-vectorizer](tools/logo-vectorizer/README.md) prepares raster logos. The [print-preflight skill](.agents/skills/print-preflight/SKILL.md) prepares, corrects and verifies a production PDF against printer requirements; only a passing release completes print preparation. Explicit audit-only requests remain read-only. Other optional helpers remain planned.

## Contents

- [Purpose](#purpose)
- [Repository layout](#repository-layout)
- [Shared runtime](#shared-runtime)
- [Working with private projects](#working-with-private-projects)
- [Workflow and next steps](#workflow-and-next-steps)

## Purpose

Build skills and tools that turn supplied materials into editable designs, print PDFs, and separately composed social media graphics.

- Use deliberate typography, cropping, spacing, and visual hierarchy.
- Keep photographs, logos, and text as separate editable elements.
- Check effective image resolution at the placed size, bleed, fonts, and color settings against the printer's requirements. Changing DPI metadata alone does not improve quality.
- Review exported files both technically and visually.

## Repository layout

```text
print-design-agent/
|-- README.md                    Project overview and usage
|-- AGENTS.md                    User guidance and workflow routing
|-- pyproject.toml               Shared Poetry dependencies and tool commands
|-- poetry.lock                  Locked dependencies for all tools
|-- poetry.toml                  Shared environment policy
|-- .python-version              Python 3.12 for all tools
|-- LICENSE                      Code license
|-- .gitignore                   Local and generated file exclusions
|-- .agents/skills/              Task-specific skills
|-- tools/                      Standalone tools
|   `-- logo-vectorizer/         Own source, tests, and README
|-- examples/
|   |-- blank-project/          Empty project to copy and fill in
|   `-- demo-flyer/             The same structure with sample text
`-- docs/                       Shared environment setup guidance
```

The agent handles required runtime setup using [environment preparation](docs/environment.md): Python 3.12, one shared Poetry environment, dependencies, and smoke tests. Installation remains subject to host permissions and network availability.

Reusable code lives in `tools/<tool-name>/`. Each tool owns its `src/`, `tests/`, and usage guide. All tools share the root Poetry manifest, lockfile, and Python environment; there is no parallel repository-level application package.

The [blank project](examples/blank-project/brief.md) and [filled example](examples/demo-flyer/brief.md) live together with matching folders and document roles. The demo is a fictional ice-cream shop brief with an existing vector logo, a stock photo, Lato fonts, a brandbook and copy for three formats. It includes finished A5 and social designs, CDR/SVG masters, PNG previews, a candidate PDF and an inspection report. Open the [overview](examples/demo-flyer/previews/overview-v01.jpg) or the [delivery index](examples/demo-flyer/reports/status.md). The blank project contains empty fields and asset folders. See the demo [asset register](examples/demo-flyer/assets.md) for sources and separate asset licenses.

Empty directories use `.gitkeep` files so Git can retain them. They do not represent implemented features. Repository documentation, examples, and code use English.

## Shared runtime

Install Python 3.12 and Poetry, then from the repository root:

```shell
poetry env use 3.12
poetry install
poetry run logo-vectorizer --help
poetry run pytest
```

The agent performs missing setup following [environment preparation](docs/environment.md).
There are no separate Python environments or dependency manifests for individual tools.

## Working with private projects

Keep real projects **outside this public repository**, in a workspace of your choice:

```text
chosen-folder/
|-- print-design-agent/          Public repository
`-- print-design-workspace/      Private workspace
    |-- brands/                 Reusable brand materials
    `-- projects/
        `-- 2026-09-flyer-name/  One project
```

1. Create your private workspace outside the repository.
2. Copy [blank-project](examples/blank-project/) into its `projects/` directory and rename it. Consult [demo-flyer](examples/demo-flyer/) for sample input.
3. Fill in `brief.md` and `copy.md`. Put original photographs and logos in `inputs/`. Fill in `brandbook.md` or reference existing rules under `brands/`; record asset sources and rights in `assets.md`. The agent can help complete these documents from supplied facts.
4. Work with the agent from this repository, providing the project's **absolute path** and intended output formats. Writing to an external directory depends on the agent environment's permissions.

Example request:

> Use $flyer-design for the project at <absolute project path>. Read the brief and copy, inspect the supplied assets, and design the requested promotional material.

For print delivery, continue with production preparation:

> Use $print-preflight to prepare the selected flyer for <printer and product>. Read the specification and editable source in <absolute project path>, correct technical issues, export and verify the production PDF.

For a read-only audit, explicitly request inspection without modification. That produces findings, not a corrected release file.

Each project contains:

| Location | Purpose |
| --- | --- |
| `brief.md` | Goal, audience, branding, formats, and production requirements |
| `copy.md` | Draft or approved text for each format |
| `brandbook.md` | Palette, typography, logo and image rules |
| `assets.md` | Asset sources, licenses and usage notes |
| `inputs/` | Originals; never overwrite |
| `assets/` | Prepared copies and derived assets |
| `working/` | Editable source files, such as CDR |
| `previews/` | Review images |
| `working/print-candidates/` | Unreleased PDFs awaiting correction or verification |
| `exports/print/` | Verified production PDFs |
| `exports/social/` | Social media deliverables |
| `reports/` | Decisions and quality checks |

The skill guides an agent; it is not a standalone flyer generator. It prefers usable CorelDRAW and falls back to Inkscape, installing Inkscape when needed and permitted by the host. Missing dedicated helpers are explicitly documented as placeholders. The logo tool has its own CLI in the shared Poetry environment; there is no end-to-end flyer generator. Record project settings in `brief.md` until a configuration format is established through a real project.

Do not commit client materials, commercial fonts, private machine paths, or secrets. Public examples must contain only materials cleared for publication. You may remove `.gitkeep` files from private project copies.

## Workflow and next steps

[AGENTS.md](AGENTS.md) guides the agent through project setup, short intake questions, skill selection, revisions, and delivery. It keeps missing information and project decisions visible without duplicating the skills.

One material per task: brief -> asset review -> copy and concept -> editable layout -> production preparation and verification (print) or export review (digital) -> delivery.

A poster, flyer, feed graphic and story are separate tasks. A later task can reuse the preceding design and assets. The existing multi-format demo is a legacy reference, not an instruction to batch materials or treat its unverified PDF as a production release.

The completed fictional example demonstrates the workflow; its print report records the unresolved printer requirements. Next, validate flyer-design on one real flyer. Use the bundled logo tool where needed, then run print-preflight on the final PDF against the chosen printer's requirements. Add MCP and additional agents when they serve a concrete need.

Code is covered by the [MIT license](LICENSE). Project assets retain their own licensing terms.
