# print-design-agent

A workshop for creating print flyers and social media graphics from real photographs, authentic logos, and brand guidelines.

**Status: design and print-inspection skills available.** The [flyer-design skill](.agents/skills/flyer-design/SKILL.md) covers promotional design and visual review. The workflow uses direct CorelDRAW COM scripting or editable SVG with Inkscape CLI. The standalone [logo-vectorizer](tools/logo-vectorizer/README.md) prepares raster logos. The [print-preflight skill](.agents/skills/print-preflight/SKILL.md) checks final print PDFs against printer requirements and reports evidence and unresolved checks; inspection depends on available tools. Other optional helpers remain planned.

## Contents

- [Purpose](#purpose)
- [Repository layout](#repository-layout)
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
|-- LICENSE                      Code license
|-- .gitignore                   Local and generated file exclusions
|-- .agents/skills/              Task-specific skills
|-- tools/logo-vectorizer/       Standalone logo tool, tests, and usage guide
|-- src/print_design_agent/      Future tools and integrations
|-- tests/                      Tool tests
|-- examples/
|   |-- blank-project/          Empty project to copy and fill in
|   `-- demo-flyer/             The same structure with sample text
`-- docs/                       Future detailed documentation
```

The blank project and filled example live together so their structure is easy to compare. The demo describes a fictional plant-care workshop; it includes no photographs, logos, fonts, or finished artwork.

Empty directories use `.gitkeep` files so Git can retain them. They do not represent implemented features. Repository documentation, examples, and code use English.

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
3. Fill in `brief.md` and `copy.md`. Put original photographs and logos in `inputs/`. Describe the branding or reference its directory under `brands/`.
4. Work with the agent from this repository, providing the project's **absolute path** and intended output formats. Writing to an external directory depends on the agent environment's permissions.

Example request:

> Use $flyer-design for the project at <absolute project path>. Read the brief and copy, inspect the supplied assets, and design the requested promotional material.

After design, request a technical inspection:

> Use $print-preflight on <absolute PDF path> for the project at <absolute project path>. Compare it with the supplied printer requirements and write an evidence-based report. Do not modify the artwork.

Each project contains:

| Location | Purpose |
| --- | --- |
| `brief.md` | Goal, audience, branding, formats, and production requirements |
| `copy.md` | Draft or approved text |
| `inputs/` | Originals; never overwrite |
| `assets/` | Prepared copies and derived assets |
| `working/` | Editable source files, such as CDR |
| `previews/` | Review images |
| `exports/print/` | Print deliverables |
| `exports/social/` | Social media deliverables |
| `reports/` | Decisions and quality checks |

The skill guides an agent; it is not a standalone flyer generator. It prefers usable CorelDRAW and falls back to Inkscape, installing Inkscape when needed and permitted by the host. Missing dedicated helpers are explicitly documented as placeholders. The logo tool has its own installation and CLI; there is no end-to-end flyer generator. Record project settings in `brief.md` until a configuration format is established through a real project.

Do not commit client materials, commercial fonts, private machine paths, or secrets. Public examples must contain only materials cleared for publication. You may remove `.gitkeep` files from private project copies.

## Workflow and next steps

[AGENTS.md](AGENTS.md) guides the agent through project setup, short intake questions, skill selection, revisions, and delivery. It keeps missing information and project decisions visible without duplicating the skills.

Brief -> asset review -> copy and concept -> editable layout -> format adaptations -> export review -> delivery.

Next, validate flyer-design on one real flyer. Use the bundled logo tool where needed, then run print-preflight on the final PDF against the chosen printer's requirements. Add MCP and additional agents when they serve a concrete need.

Code is covered by the [MIT license](LICENSE). Project assets retain their own licensing terms.
