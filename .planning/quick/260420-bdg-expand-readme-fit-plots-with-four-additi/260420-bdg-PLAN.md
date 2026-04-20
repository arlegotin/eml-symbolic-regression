---
quick_id: 260420-bdg
slug: expand-readme-fit-plots-with-four-additi
status: planned
created: 2026-04-20
workflow: gsd-quick
type: execute
files_modified:
  - README.md
  - readme-assets/
source_files:
  - README.md
  - src/eml_symbolic_regression/datasets.py
must_haves:
  truths:
    - "README plot gallery has eight plots total."
    - "The update adds four plots: two additional good/verified-style overlays and two additional bad/stretch/failed diagnostics."
    - "Plot styling is conservative: plain white background, simple axes, subdued line colors, no glossy card treatment."
    - "README remains public-facing and avoids .planning, sources, and artifacts references."
---

# Quick Task Plan: Expand README Plot Gallery

## Objective

Add four more README plots and restyle all plot SVGs with a conservative technical look. Split the gallery into good fits and failed/stretch diagnostics.

## Tasks

### Task 1: Regenerate Plot Assets

<files>readme-assets/*.svg</files>

<action>
Regenerate existing plot assets in a conservative style and add four more plots: two good examples and two bad diagnostic examples.
</action>

<verify>
<automated>rg --files readme-assets</automated>
</verify>

<done>
There are eight README SVG plot assets.
</done>

### Task 2: Update README Gallery

<files>README.md</files>

<action>
Update the plot section to describe four good overlays and four failed/stretch diagnostics. Keep the language sober and avoid implying failed diagnostic curves are recovered.
</action>

<verify>
<automated>rg -n "Good fits|Failed and stretch diagnostics|readme-assets|\\.planning|sources|artifacts" README.md</automated>
</verify>

<done>
README has the expanded conservative gallery and no forbidden internal references.
</done>

### Task 3: Verify Focused Checks

<files>README.md</files>

<action>
Run README grep checks, SVG sanity checks, and focused demo/verifier tests.
</action>

<verify>
<automated>PYTHONPATH=src python -m eml_symbolic_regression.cli verify-paper</automated>
<automated>PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos</automated>
<automated>python -m pytest tests/test_semantics_expression.py tests/test_verifier_demos_cli.py</automated>
</verify>

<done>
Focused verification passes without broader generated-output churn.
</done>
