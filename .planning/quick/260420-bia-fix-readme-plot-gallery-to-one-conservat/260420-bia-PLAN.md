---
quick_id: 260420-bia
slug: fix-readme-plot-gallery-to-one-conservat
status: planned
created: 2026-04-20
workflow: gsd-quick
type: execute
files_modified:
  - README.md
  - readme-assets/
source_files:
  - README.md
  - readme-assets/
must_haves:
  truths:
    - "README shows one 2x2 plot grid with exactly four panels: two good fits and two bad/stretch diagnostics."
    - "Planck uses the same conservative style as the other panels."
    - "Legends do not overlap plotted data."
    - "Target and candidate curves are visibly distinguishable without dashed/solid line clutter."
    - "README still avoids .planning, sources, and artifacts references."
---

# Quick Task Plan: Fix README 2x2 Plot Gallery

## Objective

Replace the current stacked plot gallery with a single conservative 2x2 SVG grid. Use two good examples and two failed/stretch diagnostics. Put the legend outside panel plotting areas and use color/labeling instead of crossing dashed/solid line types.

## Tasks

### Task 1: Replace Plot Assets

<files>readme-assets/fit-gallery.svg</files>

<action>
Remove the previous individual README plot SVGs and generate one 2x2 gallery SVG with Beer-Lambert and Michaelis-Menten as good fits, and Planck and Logistic as bad/stretch diagnostics.
</action>

<verify>
<automated>rg --files readme-assets</automated>
</verify>

<done>
Only the 2x2 gallery asset remains under readme-assets.
</done>

### Task 2: Update README

<files>README.md</files>

<action>
Replace the stacked image list with a short description and one embedded 2x2 gallery image.
</action>

<verify>
<automated>rg -n "fit-gallery|approximation-|\\.planning|sources|artifacts" README.md</automated>
</verify>

<done>
README references the 2x2 gallery and no longer references individual plot assets.
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
Focused verification passes.
</done>
