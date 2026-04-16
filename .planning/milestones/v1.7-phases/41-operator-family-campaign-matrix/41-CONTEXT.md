# Phase 41 Context: Operator-Family Campaign Matrix

**Phase:** 41
**Milestone:** v1.7 Centered-Family Baseline and Paper Decision
**Requirements:** EVD-01, EVD-02

## Starting Point

Phase 40 made operator family and continuation schedule metadata first-class in the training and benchmark pipeline. Raw EML remains the default, centered blind runs can train and snap, and unsupported centered warm-start / perturbed-tree modes fail closed with explicit diagnostics.

## Objective

Expose reproducible raw-vs-centered campaign inputs so the existing runner can execute family comparisons without touching archived v1.5/v1.6 evidence directories.

## Constraints

- Keep proof-regime case structure recognizable, but do not reuse v1.5 proof claim thresholds for transformed case IDs.
- Preserve raw variants as baseline anchors inside every family matrix.
- Keep centered warm-start and perturbed-tree rows explicit; fail-closed unsupported rows are acceptable until same-family seeds exist.
- Do not overwrite archived proof/campaign artifacts.
