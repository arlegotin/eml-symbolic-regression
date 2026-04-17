# Phase 52 Context: Verifier-Gated Exact Cleanup Expansion

## Mode

Autonomous smart-discuss defaults were selected because `$gsd-autonomous` is running non-interactively.

## Phase Goal

Broaden exact post-snap cleanup over deduplicated candidate neighborhoods while preserving verifier-owned fallback behavior.

## Success Criteria

1. Cleanup can consider selected, fallback, and retained exact candidates where candidate pool provenance is available.
2. Cleanup defaults or presets allow a larger deduplicated neighborhood than v1.6/v1.8 config while remaining bounded.
3. Subtree-level alternatives are used when provenance exposes them.
4. Targeted before/after artifacts show whether repair improves near-miss subsets without weakening fallback behavior.

## Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| REP-01 | Repair from more than selected snapped candidate, including fallback and retained exact candidates where available. | Planned |
| REP-02 | Exact cleanup uses AST dedup and verifier-gated ranking with larger configurable neighborhood than v1.6/v1.8 defaults. | Planned |
| REP-03 | Cleanup can consider subtree-level alternatives where candidate provenance exposes them, not only single-slot leaf flips. | Planned |
| REP-04 | Inspect targeted before/after evidence showing whether expanded cleanup improves declared near-miss subsets without weakening fallback behavior. | Planned |

## Current Implementation Signals

- `FitResult` already carries `selected_candidate`, `fallback_candidate`, and retained `candidates`.
- `ExactCandidate` already carries `slot_alternatives` provenance from `SoftEMLTree.active_slot_alternatives(top_k=2)`.
- `cleanup_failed_candidate()` currently expands only `fit.selected_candidate.slot_alternatives`.
- `expand_snap_neighborhood()` already performs exact-AST deduplication and emits move metadata for slot and subtree-shaped changes.
- Benchmark artifacts already distinguish raw status, fallback candidates, repair status, verifier status, and `repaired_candidate` evidence.

## Decisions

- Expand target-free cleanup around retained exact candidates, not around a hidden target AST.
- Preserve fallback and selected manifests exactly; cleanup may append repair reports and promote only a verifier-recovered repaired expression.
- Keep `repaired_candidate` taxonomy separate from raw, warm-start, compile-only, and same-AST recovery.
- Use bounded larger cleanup settings through configuration or a named preset instead of unbounded search.
- Favor focused near-miss fixtures and a targeted evidence suite over broad campaign reruns in this phase.

## Non-Goals

- Do not weaken verifier status requirements.
- Do not present repaired candidates as blind discovery.
- Do not change Arrhenius or Michaelis same-AST evidence regimes except where shared artifact fields need to remain compatible.
- Do not use target-aware perturbed repair behavior for ordinary target-free cleanup.

## Open Questions For Research

1. Which existing benchmark or fixture path can produce a concise before/after artifact proving selected-only cleanup fails while candidate-pool cleanup succeeds?
2. Should the larger bounded neighborhood be represented as a classmethod preset, new config fields, benchmark-suite settings, or both?
3. Does existing neighborhood provenance already satisfy subtree-level alternatives across candidate roots, or is additional candidate provenance needed?

## Candidate Implementation Areas

- `src/eml_symbolic_regression/repair.py`
- `src/eml_symbolic_regression/master_tree.py`
- `src/eml_symbolic_regression/benchmark.py`
- `src/eml_symbolic_regression/benchmark_suites.py`
- `tests/test_repair.py`
- `tests/test_benchmark_runner.py`
- `tests/test_benchmark_contract.py`
- `docs/IMPLEMENTATION.md`
