# Shared Poetry environment

All tools in this repository use **one Python 3.12 environment managed by Poetry**.
The root `pyproject.toml` declares packages, commands and dependencies; `poetry.lock`
records resolved versions. `.python-version` records the shared Python minor version.
Run setup and tool commands from the repository root.

## Agent responsibilities

1. Detect Python 3.12 and Poetry. Verify their actual executable paths and versions.
   If missing, install compatible releases using official installers or trusted OS
   packages, preferably per user and within host permissions. Install Poetry using
   its [official procedure](https://python-poetry.org/docs/#installation).
2. Select the interpreter with `poetry env use <absolute-path-to-python-3.12>`.
   Poetry creates/reuses the single repository environment in its managed cache;
   `poetry.toml` records this policy. If another project's environment is active,
   leave it before setup so Poetry cannot accidentally reuse it.
3. Run `poetry install` from the repository root. Install the committed lockfile;
   do not run `poetry update` or regenerate the lock merely to launch a tool.
4. Verify `poetry env info`, imports, and a real operation. Use `poetry run` for
   every tool and Python command, including project-local design scripts.

Do not create per-tool environments, run `python -m venv`, install project libraries
with pip, or add nested dependency manifests. Poetry's own installation is separate
from project dependencies. Do not disable Poetry isolation to install libraries
into the system Python. Native editors and PDF utilities remain OS applications,
not separate Python environments.

## Commands

```shell
poetry env use /absolute/path/to/python3.12
poetry install
poetry run logo-vectorizer "/absolute/private-project/inputs/logo.png" --out-dir "/absolute/private-project/assets/logos/v01"
poetry run pytest
poetry run ruff check tools
poetry run ruff format --check tools
```

On Windows, supply the absolute path to `python.exe` to `poetry env use`. Shell
activation is unnecessary. Do not change PowerShell execution policy or replace
the OS Python to run a tool.

## New dependencies and tools

Add runtime dependencies at the root with `poetry add <package>`; use
`poetry add --group dev <package>` for development tools. Preserve deliberate pins
such as VTracer. Commit the manifest and updated lockfile together. New tools keep
their source, tests and README in `tools/<name>/`; register packages, commands and
test locations in the root manifest. Resolve version conflicts for the shared
environment instead of creating a second one.

Use the [flyer tooling guidance](../.agents/skills/flyer-design/references/tools.md)
for CorelDRAW/Inkscape and [preflight guidance](../.agents/skills/print-preflight/references/tools.md)
for PDF utilities. Detect existing applications and install missing required free
tools when permitted. Do not purchase licenses or alter unrelated installations.

## Verify and record

After setup or dependency changes, run the relevant tests and a real synthetic
operation in a temporary/private folder. Logo verification must exercise SVG and
required PNG/PDF exports, including native VTracer and resvg. Editor verification
must create/save/render a document. An installation log or `--help` alone is not
proof of readiness. Reuse working installations without reinstalling every task.

Record interpreter, Poetry and native-tool versions, environment path and smoke-test
results in private notes. Keep environments, logs and machine paths out of Git.

If network, permissions, licensing or compatibility block setup, diagnose the
specific failed command and report the exact blocker. Continue independent work;
never claim readiness without successful verification or bypass host restrictions.
Routine authorized setup belongs to the agent, not a checklist handed to the user.
