# print-design-agent

A workshop for creating print flyers and social media graphics from real photographs, authentic logos, and brand guidelines.

**Status: repository scaffold.** Automation, CorelDRAW integration, and output validation are planned, not implemented.

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
|-- LICENSE                      Code license
|-- .gitignore                   Local and generated file exclusions
|-- .agents/skills/              Future task-specific skills
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

> Work on the project at <absolute project path>. Read the brief and copy, inspect inputs, identify missing information, and propose the next step using this repository's instructions.

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

This is currently an organizational workflow, not an automatic flyer generator. There is no installer or CLI yet. Record project settings in `brief.md` until a configuration format is established through a real project.

Do not commit client materials, commercial fonts, private machine paths, or secrets. Public examples must contain only materials cleared for publication. You may remove `.gitkeep` files from private project copies.

## Workflow and next steps

A future `AGENTS.md` will describe how the agent creates flyers: the design workflow, use of materials and tools, and quality checks. Its contents will be established in a later stage.

Brief -> asset review -> copy and concept -> editable layout -> format adaptations -> export review -> delivery.

First, validate this process on one real flyer. Then add the main skill, necessary Python tools, integration with the existing logo vectorizer, and a CorelDRAW adapter. Add MCP and additional agents when they serve a concrete need.

Code is covered by the [MIT license](LICENSE). Project assets retain their own licensing terms.
