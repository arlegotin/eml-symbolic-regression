# Phase 42 Context: Comparative Evidence Aggregation and Regression Locks

**Phase:** 42
**Milestone:** v1.7 Centered-Family Baseline and Paper Decision
**Requirements:** EVD-03, EVD-04, EVD-05

## Starting Point

Phase 41 added v1.7 family suites and campaign presets. Those runs already emit operator-family and continuation metadata at the benchmark and campaign CSV level.

## Objective

Turn family campaign runs into comparison artifacts that can answer: which operator family recovered what, at which depth/regime, with what anomaly/repair/refit burden, and whether raw defaults remain stable.

## Constraints

- Do not collapse pure blind, scaffolded, warm-start, compile-only, repaired, and perturbed-tree rows into a single claim.
- Comparison tables must tolerate unsupported centered perturbed-tree rows.
- Outputs must be generated as part of normal campaign reporting so evidence is reproducible from the same CLI command.
