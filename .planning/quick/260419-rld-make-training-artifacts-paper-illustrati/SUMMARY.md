---
quick_id: 260419-rld
slug: make-training-artifacts-paper-illustrati
status: complete
completed: 2026-04-19
---

# Quick Task Summary: Paper-Ready Training Detail Artifacts

## Outcome

The v1.12 refresh artifacts now include per-step optimizer traces and a paper-facing training-detail package for data-rich figures, tables, and reviewer inspection.

## Implementation

- Added optimizer restart traces with fit/hardening phase labels, global steps, temperatures, fit loss, objective loss, entropy, size/anomaly objective components, anomaly counters, and by-node metrics.
- Added a `paper-training-detail` CLI command that extracts traced v1.12 campaign runs into JSON, CSV, Markdown, and SVG assets.
- Added training-detail supplement audit coverage so source locks fail if the paper-facing training traces or loss figures are missing.
- Added tests for optimizer trace recording, row extraction, artifact generation, and the CLI command.

## Generated Artifacts

- `artifacts/campaigns/v1.12-evidence-refresh/`
  - Rerun with traced optimizer manifests.
  - 10 shallow refresh runs.
  - 8 depth-refresh runs.
- `artifacts/paper/v1.11/draft/training-detail/`
  - 18 traced run payloads.
  - 4,472 per-step trace rows.
  - 58 run-summary rows.
  - 232 candidate-lifecycle rows.
  - 2 deterministic SVG loss-curve figures.
- `artifacts/paper/v1.11/v1.12-supplement/`
  - Refreshed source locks and source copies.
  - Supplement audit passed with 62 source locks.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_paper_v112.py`
  - 22 passed in 4.59s.
- `PYTHONPATH=src python -m pytest tests/test_optimizer_cleanup.py tests/test_campaign.py tests/test_paper_v112.py`
  - 50 passed in 27.91s.
  - 2 expected numerical warnings from the existing centered-family optimizer path.
- `git diff --check`
  - Passed.

## Reproduction Commands

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-refresh --output-dir artifacts/campaigns/v1.12-evidence-refresh --overwrite
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-training-detail --output-dir artifacts/paper/v1.11/draft/training-detail --refresh-dir artifacts/campaigns/v1.12-evidence-refresh
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-figures --output-dir artifacts/paper/v1.11/draft
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-supplement --output-dir artifacts/paper/v1.11/v1.12-supplement --overwrite
```
