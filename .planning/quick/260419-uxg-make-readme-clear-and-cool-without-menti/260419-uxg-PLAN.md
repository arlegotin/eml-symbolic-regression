---
quick_id: 260419-uxg
slug: make-readme-clear-and-cool-without-menti
status: planned
created: 2026-04-19
workflow: gsd-quick
type: execute
files_modified:
  - README.md
source_files:
  - README.md
  - pyproject.toml
  - src/eml_symbolic_regression/cli.py
  - src/eml_symbolic_regression/datasets.py
must_haves:
  truths:
    - "README reads as a clear public-facing brief, not internal project notes."
    - "README does not mention .planning, sources, or artifacts paths."
    - "Important technical and claim-boundary context is embedded naturally in the narrative."
    - "Usage commands are runnable and avoid internal output-directory details."
  artifacts:
    - path: README.md
      provides: "Public-facing overview, technical pipeline, usage, demos, and limits"
---

# Quick Task Plan: Public-Facing README Polish

## Objective

Rewrite the current README pass so it feels like the public front door for the package: clear, energetic, technically precise, and easy to use. Remove internal scaffolding references from the README content, specifically mentions of `.planning`, `sources`, and `artifacts`.

## Tasks

### Task 1: Remove Internal Directory Framing

<files>README.md</files>

<action>
Remove the repository-map section and any prose that points readers at internal planning/source/artifact directories. Keep important context by folding it into the main story: the paper grounding, demo choices, evidence regimes, and claim boundaries should remain understandable without path references.
</action>

<verify>
<automated>rg -n "\\.planning|sources/|artifacts/" README.md</automated>
</verify>

<done>
No README line mentions `.planning`, `sources/`, or `artifacts/`.
</done>

### Task 2: Make The README Clearer And Cooler

<files>README.md</files>

<action>
Make the opening and structure more compelling: explain the core trick, show the pipeline, keep concrete technical detail, and avoid marketing overclaim. Prefer short sections with strong headings and concise prose.
</action>

<verify>
<automated>rg -n "eml\\(x, y\\)|complex128|snapping|verifier|training loss alone|not blind discovery" README.md</automated>
</verify>

<done>
README explains what is happening, why EML matters, how the package works, and how claims are checked.
</done>

### Task 3: Keep Usage Runnable Without Internal Output Paths

<files>README.md</files>

<action>
Keep installation and common CLI examples, but avoid commands that expose internal output-directory conventions. Use default output locations where possible and keep examples focused on verify, demos, benchmarks, campaigns, and tests.
</action>

<verify>
<automated>PYTHONPATH=src python -m eml_symbolic_regression.cli --help</automated>
<automated>PYTHONPATH=src python -m eml_symbolic_regression.cli verify-paper</automated>
<automated>PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos</automated>
</verify>

<done>
README gives a new user a short, runnable path without surfacing internal output paths.
</done>
