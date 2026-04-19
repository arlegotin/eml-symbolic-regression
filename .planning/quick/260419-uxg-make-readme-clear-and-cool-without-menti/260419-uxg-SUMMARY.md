---
quick_id: 260419-uxg
slug: make-readme-clear-and-cool-without-menti
status: complete
created: 2026-04-19
completed: 2026-04-19
workflow: gsd-quick
files_modified:
  - README.md
summary_artifact: .planning/quick/260419-uxg-make-readme-clear-and-cool-without-menti/260419-uxg-SUMMARY.md
---

# Quick Task 260419-uxg Summary: Public-Facing README Polish

## Status

README rewrite completed.

The README is now a public-facing brief: it opens with the EML operator, explains the core search trick, shows the technical pipeline, gives concise installation and usage commands, lists demo regimes, and keeps recovery claims bounded by verifier-owned evidence.

## User Constraint

The README no longer mentions internal `.planning`, source-document, or generated-output directory paths. Important context from those materials was embedded directly into the narrative.

## Verification Completed

```bash
rg -n "\.planning|sources/|artifacts/|sources|artifact" README.md
```

Result: passed with no matches.

```bash
rg -n "eml\(x, y\)|complex128|snapping|verifier|training loss alone|not blind discovery" README.md
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli --help
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli verify-paper
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-demos
```

Result: passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks
```

Result: passed.

```bash
python -m pytest tests/test_semantics_expression.py tests/test_verifier_demos_cli.py
```

Result: passed, 18 tests.

## Notes

The installed `eml-sr` console script was not present in the current shell before running an editable install, so CLI behavior was verified through the module entry point.
