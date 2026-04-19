---
quick_id: 260419-rld
slug: make-training-artifacts-paper-illustrati
status: in_progress
created: 2026-04-19
---

# Quick Task Plan: Paper-Ready Training Detail Artifacts

## Goal

Make the paper-facing training artifacts detailed enough for data-rich figures and reviewer inspection: per-step losses, objective components, anomaly metrics, candidate lifecycle rows, and deterministic illustration assets.

## Tasks

1. Add per-step trace recording to the EML optimizer manifest.
2. Add paper-facing training-detail artifact generation for v1.12 refresh runs.
3. Emit full JSON/CSV/Markdown source tables for step traces, run summaries, and candidate lifecycle events.
4. Emit deterministic SVG loss-curve figures for shallow and depth-refresh runs.
5. Wire a CLI command for the training-detail package.
6. Add focused tests for trace recording and artifact generation.
7. Rerun the v1.12 evidence refresh with traced manifests, generate training-detail artifacts, and refresh the v1.12 supplement source locks.
8. Commit code, artifacts, and quick-task summary.

## Verification

- Focused tests pass.
- New run artifacts include `trace` rows under optimizer restart logs.
- Training-detail manifest reports nonzero step-trace rows and candidate rows.
- SVG loss-curve figures exist.
- v1.12 supplement audit remains passed after relocking.
