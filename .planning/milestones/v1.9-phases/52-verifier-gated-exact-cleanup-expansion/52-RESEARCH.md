# Phase 52: Verifier-Gated Exact Cleanup Expansion - Research

**Researched:** 2026-04-17  
**Domain:** exact post-snap cleanup, retained candidate pools, verifier-gated benchmark evidence  
**Confidence:** HIGH for current implementation facts; MEDIUM for the proposed real near-miss evidence subset because improvement is intentionally measured, not assumed.

<user_constraints>
## User Constraints (from 52-CONTEXT.md)

### Locked Decisions
- Expand target-free cleanup around retained exact candidates, not around a hidden target AST.
- Preserve fallback and selected manifests exactly; cleanup may append repair reports and promote only a verifier-recovered repaired expression.
- Keep `repaired_candidate` taxonomy separate from raw, warm-start, compile-only, and same-AST recovery.
- Use bounded larger cleanup settings through configuration or a named preset instead of unbounded search.
- Favor focused near-miss fixtures and a targeted evidence suite over broad campaign reruns in this phase.

### Non-Goals
- Do not weaken verifier status requirements.
- Do not present repaired candidates as blind discovery.
- Do not change Arrhenius or Michaelis same-AST evidence regimes except where shared artifact fields need to remain compatible.
- Do not use target-aware perturbed repair behavior for ordinary target-free cleanup.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
| --- | --- | --- |
| REP-01 | Repair from selected, fallback, and retained exact candidates where available. | `FitResult` already carries `selected_candidate`, `fallback_candidate`, and `candidates`; `cleanup_failed_candidate()` currently reads only `selected_candidate`. [VERIFIED: `src/eml_symbolic_regression/optimize.py:110`, `src/eml_symbolic_regression/repair.py:96`] |
| REP-02 | AST dedup and verifier-gated ranking with larger configurable neighborhood. | `expand_snap_neighborhood()` deduplicates exact AST documents and `cleanup_failed_candidate()` ranks verified variants; Phase 52 needs a named larger preset and benchmark plumbing. [VERIFIED: `src/eml_symbolic_regression/master_tree.py:720`, `src/eml_symbolic_regression/repair.py:184`] |
| REP-03 | Subtree-level alternatives where candidate provenance exposes them. | `SlotAlternative` and `NeighborhoodMove` already carry `subtree_root` and descendant/pruned assignments; candidate-pool roots expose more of this provenance without target AST access. [VERIFIED: `src/eml_symbolic_regression/master_tree.py:99`, `src/eml_symbolic_regression/master_tree.py:788`] |
| REP-04 | Targeted before/after evidence without weakening fallback. | Existing benchmark artifacts already preserve selected/fallback manifests, repair status, and repaired taxonomy; add a focused evidence suite plus synthetic artifact regression. [VERIFIED: `src/eml_symbolic_regression/benchmark.py:1639`, `src/eml_symbolic_regression/benchmark.py:2915`] |
</phase_requirements>

## Summary

Phase 52 should not replace the verifier or the optimizer selector. The implementation should expand the target-free cleanup search roots from only `fit.selected_candidate` to a deduplicated ordered set of selected, fallback, and retained exact candidates, then globally deduplicate exact AST variants before verifier work. [VERIFIED: codebase inspection]

The safest configuration path is both: add a low-level `RepairConfig.expanded_candidate_pool()` preset, and add optional benchmark repair settings outside `OptimizerBudget`. This avoids changing every existing benchmark run ID, because `BenchmarkRun.run_id` hashes `optimizer.as_dict()`. [VERIFIED: `src/eml_symbolic_regression/benchmark.py:586`, `src/eml_symbolic_regression/benchmark.py:607`]

Primary recommendation: implement candidate-pool cleanup in `repair.py`, pass an explicit expanded repair config only from targeted Phase 52 evidence paths, and keep ordinary selected/fallback optimizer manifests immutable in all artifacts. [VERIFIED: `docs/IMPLEMENTATION.md:34`, `docs/IMPLEMENTATION.md:93`]

## Current Implementation Facts

- `ExactCandidate` stores `snap`, `slot_alternatives`, verifier report, and selection metrics; `FitResult` stores `selected_candidate`, `fallback_candidate`, and the retained `candidates` tuple. [VERIFIED: `src/eml_symbolic_regression/optimize.py:66`, `src/eml_symbolic_regression/optimize.py:110`]
- Candidate emission captures `model.active_slot_alternatives(top_k=2)` for each legacy snap and hardening checkpoint candidate. [VERIFIED: `src/eml_symbolic_regression/optimize.py:186`]
- Candidate-pool selection already verifies candidates when splits are supplied and ranks by verifier status, extrapolation error, high-precision error, held-out error, post-snap loss, complexity, and soft loss. [VERIFIED: `src/eml_symbolic_regression/optimize.py:281`, `src/eml_symbolic_regression/optimize.py:267`]
- The optimizer manifest serializes the full ranked candidate pool plus selected and fallback candidate manifests. [VERIFIED: `src/eml_symbolic_regression/optimize.py:457`]
- `cleanup_failed_candidate()` currently binds `selected = fit.selected_candidate` and returns `missing_slot_alternatives` if that one candidate lacks alternatives. [VERIFIED: `src/eml_symbolic_regression/repair.py:96`]
- Current cleanup bounds are `cleanup_top_k=2`, `cleanup_max_slots=4`, `cleanup_beam_width=8`, and `cleanup_max_moves=2`. [VERIFIED: `src/eml_symbolic_regression/repair.py:14`]
- Cleanup verifies each neighborhood variant and accepts only if the best verifier-ranked variant has status `recovered`; failed cleanup serializes no `repaired_ast`. [VERIFIED: `src/eml_symbolic_regression/repair.py:173`, `src/eml_symbolic_regression/repair.py:188`, `src/eml_symbolic_regression/repair.py:201`]
- `active_slot_alternatives()` can serialize a child alternative with `subtree_root` and descendant assignments, and `expand_snap_neighborhood()` replays those assignments when constructing exact variants. [VERIFIED: `src/eml_symbolic_regression/master_tree.py:501`, `src/eml_symbolic_regression/master_tree.py:814`]
- `expand_snap_neighborhood()` already exact-AST-deduplicates variants by serialized expression document. [VERIFIED: `src/eml_symbolic_regression/master_tree.py:759`]
- Blind, warm-start, and perturbed-tree benchmark flows call `cleanup_failed_candidate()` after failed exact verification; perturbed-tree then falls back to target-aware repair only if target-free repair fails. [VERIFIED: `src/eml_symbolic_regression/benchmark.py:1639`, `src/eml_symbolic_regression/benchmark.py:1762`, `src/eml_symbolic_regression/benchmark.py:1907`]
- Artifact metrics already expose repair status, variant count, move count, accepted move count, and repair verifier status. [VERIFIED: `src/eml_symbolic_regression/benchmark.py:2470`, `src/eml_symbolic_regression/benchmark.py:2574`]
- The current suite definitions live in `benchmark.py`; there is no `src/eml_symbolic_regression/benchmark_suites.py` file to edit. [VERIFIED: repository file scan]

## Open Questions Answered

1. **Which existing benchmark or fixture path can produce concise before/after evidence?**

   Use a new deterministic fixture in `tests/test_benchmark_runner.py` as the proof that selected-only cleanup fails while candidate-pool cleanup succeeds. The existing monkeypatch pattern already fakes `fit_eml_tree()`/warm-start output and inspects the emitted artifact. [VERIFIED: `tests/test_benchmark_runner.py:64`, `tests/test_benchmark_runner.py:490`]

   For real near-miss evidence, seed a targeted `v1.9-repair-evidence` suite from archived failed-repair subsets such as `artifacts/proof/v1.6/campaigns/proof-shallow-pure-blind/aggregate.json`, `artifacts/proof/v1.6/campaigns/proof-depth-curve/.../proof-depth-curve-depth-4-blind-344a2756d697.json`, and `artifacts/campaigns/v1.6-standard/.../v1-3-standard-beer-perturbation-sweep-7ab0d86550b5.json`. These artifacts show selected-only cleanup misses with retained candidate pools, but they do not prove pool cleanup will improve until Phase 52 code runs. [VERIFIED: artifact scan]

2. **Should larger bounded neighborhood be a preset, fields, suite settings, or both?**

   Use both a `RepairConfig` preset and optional benchmark repair settings, but do not put cleanup knobs into `OptimizerBudget` defaults. Adding default optimizer fields to `OptimizerBudget.as_dict()` would change existing run hashes and artifact paths. [VERIFIED: `src/eml_symbolic_regression/benchmark.py:307`, `src/eml_symbolic_regression/benchmark.py:586`]

   Recommended shape: `RepairConfig.expanded_candidate_pool()` returns a bounded preset such as `top_k=3`, `max_slots=8`, `beam_width=32`, `max_moves=3`, and candidate roots `("selected", "fallback", "retained")`. The exact values are a starting budget and should be adjusted if the focused regression slice is too slow. [ASSUMED: engineering budget estimate]

3. **Does existing provenance already satisfy subtree-level alternatives?**

   Yes for per-candidate terminal-to-child, child-to-terminal, and child-subtree replacement moves exposed by that candidate's serialized alternatives. [VERIFIED: `src/eml_symbolic_regression/master_tree.py:99`, `src/eml_symbolic_regression/master_tree.py:788`, `tests/test_master_tree.py:96`]

   No for arbitrary cross-candidate subtree grafting, such as taking a subtree from candidate B and grafting it into candidate A when A did not serialize that subtree as an alternative. That is not required for Phase 52 unless new evidence shows per-root candidate neighborhoods are insufficient. [VERIFIED: code inference from `ActiveSlotAlternatives` shape]

## Recommended Implementation Slices

### Slice 1: Candidate-Pool Cleanup Core

- Add `RepairConfig.expanded_candidate_pool()` plus optional fields for candidate root sources and larger cleanup bounds. Keep `RepairConfig()` backward-compatible for direct unit callers. [VERIFIED: current config shape at `src/eml_symbolic_regression/repair.py:14`]
- Add a helper in `repair.py`, e.g. `_cleanup_candidate_roots(fit, config)`, that returns selected, fallback, and retained candidates in stable order, deduplicated by exact AST document and candidate ID provenance. [VERIFIED: required inputs exist in `FitResult`]
- Extend `RepairReport` with backward-compatible optional metadata: `candidate_roots_attempted`, `accepted_candidate_id`, `accepted_candidate_source`, and per-root variant counts. Existing tests construct `RepairReport` directly, so every new field needs a default. [VERIFIED: direct construction in `tests/test_repair.py:159`]

### Slice 2: Global Variant Dedup and Ranking

- For each candidate root, call `expand_snap_neighborhood(root.snap, root.slot_alternatives, ...)`; use root-specific operator family from the root expression, as current selected-only cleanup does. [VERIFIED: `src/eml_symbolic_regression/repair.py:149`]
- Deduplicate variants globally by exact AST document before verifier calls so duplicate selected/fallback/hardening roots do not multiply verifier cost. [VERIFIED: local dedup already exists in `src/eml_symbolic_regression/master_tree.py:759`]
- Rank all verified variants with the existing `_cleanup_ranking_key()`, adding stable tie-breakers for source candidate order and candidate ID only after verifier-owned fields. [VERIFIED: current ranking at `src/eml_symbolic_regression/repair.py:491`]
- Do not accept a failed verifier variant and do not serialize `repaired_ast` unless status is `repaired_candidate` and verifier status is `recovered`. [VERIFIED: `src/eml_symbolic_regression/repair.py:76`]

### Slice 3: Benchmark Config and Artifact Evidence

- Add an optional benchmark repair settings object or `repair_preset` field to `BenchmarkCase`/`BenchmarkRun`, defaulting to `None`; include it in `run_id` only when non-default. [VERIFIED: run identity construction at `src/eml_symbolic_regression/benchmark.py:586`]
- Route blind, warm-start, and perturbed-tree cleanup calls through `_repair_config_for_run(run)`; keep target-aware perturbed repair as fallback only after target-free cleanup fails. [VERIFIED: current call sites at `src/eml_symbolic_regression/benchmark.py:1639`, `src/eml_symbolic_regression/benchmark.py:1762`, `src/eml_symbolic_regression/benchmark.py:1907`]
- Add `v1.9-repair-evidence` to `BUILTIN_SUITES` with focused near-miss cases and explicit expanded repair settings; do not attach proof claim IDs. [VERIFIED: current focused suite pattern at `src/eml_symbolic_regression/benchmark.py:1467`]
- Add artifact metrics for source candidate ID/source when a repair is accepted, but keep `classification` and `evidence_class` as `repaired_candidate`. [VERIFIED: `src/eml_symbolic_regression/benchmark.py:2915`, `src/eml_symbolic_regression/benchmark.py:2960`]

### Slice 4: Docs and Evidence Notes

- Update `docs/IMPLEMENTATION.md` to say cleanup can use selected/fallback/retained candidate roots when an expanded repair preset is selected. [VERIFIED: existing cleanup docs at `docs/IMPLEMENTATION.md:34`]
- Document that `v1.9-repair-evidence` is targeted near-miss repair evidence, not blind discovery and not a proof denominator. [VERIFIED: current regime-separation docs at `docs/IMPLEMENTATION.md:105`]

## Testing Strategy

- `tests/test_repair.py`: selected candidate has no verifier-recovering neighborhood; fallback or retained candidate has a low-margin subtree alternative that recovers. Assert accepted report names the non-selected source candidate and leaves original selected/fallback candidates unchanged. [VERIFIED: current selected-only cleanup test at `tests/test_repair.py:316`]
- `tests/test_repair.py`: selected/fallback/retained roots with the same AST deduplicate to one root and do not inflate variant counts. [VERIFIED: duplicate AST risk observed in archived artifact scan]
- `tests/test_repair.py`: retained candidate subtree alternative emits `terminal_to_child` or `child_subtree_replacement` with `subtree_root` and descendant assignments. [VERIFIED: existing subtree assertions at `tests/test_repair.py:340`]
- `tests/test_benchmark_runner.py`: fake `fit_eml_tree()` returns selected-only failure plus fallback/retained repair success; `execute_benchmark_run()` emits `status == repaired_candidate`, `repair_status == repaired`, selected/fallback manifests still match the optimizer payload, and repair metadata identifies the source candidate. [VERIFIED: artifact promotion test pattern at `tests/test_benchmark_runner.py:490`]
- `tests/test_benchmark_contract.py`: `v1.9-repair-evidence` exists, expands deterministic run IDs, and existing focused suite run IDs such as Michaelis remain unchanged unless a repair config is explicitly present. [VERIFIED: existing stable run ID test at `tests/test_benchmark_contract.py:158`]
- `tests/test_benchmark_reports.py` or `tests/test_campaign.py`: aggregate repair metrics remain grouped under `repaired_candidate`, not blind recovery or same-AST recovery. [VERIFIED: existing taxonomy tests at `tests/test_benchmark_reports.py:387`]

Recommended verification commands:

```bash
python -m pytest tests/test_repair.py tests/test_master_tree.py -q
python -m pytest tests/test_benchmark_runner.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.9-repair-evidence --output-dir artifacts/campaigns/v1.9-repair-evidence
```

## Evidence Strategy

- First produce deterministic unit/benchmark-runner evidence that selected-only cleanup misses but candidate-pool cleanup succeeds; this proves REP-01 and REP-03 independent of stochastic training. [VERIFIED: current monkeypatchable benchmark pattern]
- Then run `v1.9-repair-evidence` over archived near-miss-inspired real cases and compare `raw_status`, `repair_status`, `repair_variant_count`, `repair_verifier_status`, selected/fallback IDs, and final `evidence_class`. [VERIFIED: metrics already extracted in `src/eml_symbolic_regression/benchmark.py:2470`]
- Treat no-improvement on real near-miss subsets as valid evidence if fallback behavior and taxonomy are unchanged. REP-04 asks whether expanded cleanup improves declared subsets; it does not require guaranteeing improvement. [VERIFIED: requirement wording in `52-CONTEXT.md`]

## Risks

- **Run ID churn:** adding cleanup fields to `OptimizerBudget.as_dict()` would invalidate many stable artifact paths. Use optional non-default repair config on benchmark cases/runs instead. [VERIFIED: `src/eml_symbolic_regression/benchmark.py:307`, `src/eml_symbolic_regression/benchmark.py:586`]
- **Verifier cost blowup:** selected, fallback, and retained roots can be duplicate ASTs; global dedup and hard caps are required before verifier calls. [VERIFIED: archived artifacts showed duplicate candidate roots with identical losses]
- **Taxonomy weakening:** a repaired expression must stay `repaired_candidate` and must not update raw, warm-start, or same-AST status. [VERIFIED: `src/eml_symbolic_regression/benchmark.py:2915`]
- **Subtree overreach:** cross-root subtree grafting would become a new search algorithm and provenance schema. Keep Phase 52 to per-root serialized alternatives unless evidence proves otherwise. [VERIFIED: current provenance shape]
- **Report compatibility:** `RepairReport` is constructed directly in tests; new fields must be optional defaults and `as_dict()` must remain backward-compatible. [VERIFIED: `tests/test_repair.py:159`]

## Execution Unknowns

1. Do the real archived near-miss subsets improve under expanded candidate-pool cleanup? This requires implementation and the targeted `v1.9-repair-evidence` run. [VERIFIED: artifact scan found near misses but did not prove future repair success]
2. Are the proposed expanded caps (`top_k=3`, `max_slots=8`, `beam_width=32`, `max_moves=3`) fast enough for benchmark-runner tests and the focused evidence suite? Start there, then reduce only if the focused slice is too slow. [ASSUMED: engineering budget estimate]
3. Should accepted repair metadata list every attempted root or only the accepted root plus summary counts? Recommendation: accepted root plus per-root counts is enough for artifacts; full per-root move dumps may be too large. [ASSUMED: artifact-size tradeoff]

## Sources

- `52-CONTEXT.md` - phase decisions, non-goals, open questions, and implementation areas. [VERIFIED: local planning doc]
- `src/eml_symbolic_regression/repair.py` - current selected-only cleanup, verifier ranking, report serialization, target-aware fallback repair. [VERIFIED: code]
- `src/eml_symbolic_regression/master_tree.py` - slot alternatives, subtree provenance, AST replay, and neighborhood dedup. [VERIFIED: code]
- `src/eml_symbolic_regression/optimize.py` - exact candidate pool, selected/fallback retention, verifier-gated candidate ranking. [VERIFIED: code]
- `src/eml_symbolic_regression/benchmark.py` - cleanup call sites, benchmark suite definitions, run identity, metrics, and taxonomy. [VERIFIED: code]
- `tests/test_repair.py`, `tests/test_master_tree.py`, `tests/test_benchmark_runner.py`, `tests/test_benchmark_contract.py` - current regression patterns to extend. [VERIFIED: tests]
- `docs/IMPLEMENTATION.md` - current public contract for cleanup, fallback preservation, evidence regimes, and v1.9 focused suites. [VERIFIED: docs]
- Archived artifacts under `artifacts/proof/v1.6/` and `artifacts/campaigns/v1.6-standard/` - near-miss examples with failed selected-only repair and retained candidate pools. [VERIFIED: artifact scan]
