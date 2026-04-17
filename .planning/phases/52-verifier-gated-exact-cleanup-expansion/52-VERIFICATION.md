---
phase: 52-verifier-gated-exact-cleanup-expansion
verified: 2026-04-17T16:00:27Z
status: passed
score: "8/8 must-haves verified"
overrides_applied: 0
---

# Phase 52: Verifier-Gated Exact Cleanup Expansion Verification Report

**Phase Goal:** Broaden exact post-snap cleanup over deduplicated candidate neighborhoods while preserving verifier-owned fallback behavior.  
**Verified:** 2026-04-17T16:00:27Z  
**Status:** PASS  
**Re-verification:** No - initial verification. No previous `52-VERIFICATION.md` existed.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Cleanup can opt into selected, fallback, and retained exact-candidate roots. | VERIFIED | `RepairConfig.expanded_candidate_pool()` enables `("selected", "fallback", "retained")`; `_cleanup_candidate_roots()` reads `FitResult.selected_candidate`, `fallback_candidate`, and retained `candidates`; tests cover fallback and retained repair roots. |
| 2 | Default cleanup remains selected-only and expanded cleanup is bounded but larger than v1.6/v1.8 defaults. | VERIFIED | `RepairConfig()` keeps `top_k=2`, `max_slots=4`, `beam_width=8`, `max_moves=2`, selected-only; expanded preset uses `top_k=3`, `max_slots=8`, `beam_width=32`, `max_moves=3`. |
| 3 | Exact roots and variants are globally deduplicated by exact AST before verifier evaluation. | VERIFIED | Candidate roots use `_expression_dedup_key()` and variants are stored in `deduped_variants` before `verify_candidate()`; review-fix recomputes per-root dedup ownership after final replacement. |
| 4 | Repair promotion remains verifier-gated. | VERIFIED | `cleanup_failed_candidate()` returns `repaired_candidate` only when the winning `VerificationReport.status == "recovered"`; failed cleanup reports serialize no `repaired_ast`. |
| 5 | Subtree-level alternatives are preserved when candidate provenance exposes them. | VERIFIED | `_repair_move_from_neighborhood()` carries `descendant_assignments`, `pruned_assignments`, and `subtree_root`; tests assert terminal-to-child and subtree provenance survives candidate-pool cleanup. |
| 6 | Optimizer-selected and fallback manifests remain unchanged; cleanup only appends repair metadata. | VERIFIED | Benchmark runner writes the original optimizer manifest plus a separate `repair` payload; tests assert selected/fallback candidate ids remain byte-for-byte stable after repair promotion. |
| 7 | Benchmark/report plumbing exposes expanded repair metrics without relabeling repaired candidates as blind, same-AST, compile-only, or perturbed recovery. | VERIFIED | `_extract_run_metrics()` emits root/dedup/accepted-root fields; campaign CSVs include them; classification keeps `repair_status == "repaired"` under `repaired_candidate`. |
| 8 | Targeted before/after evidence artifacts show measured near-miss outcomes and fallback preservation. | VERIFIED | `v1.9-repair-evidence` artifacts contain 4 runs and 2 default-vs-expanded pairs; summary reports 0 default repairs, 0 expanded repairs, 0 improvements, 0 regressions, and fallback manifests preserved for all runs. |

**Score:** 8/8 truths verified.

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `src/eml_symbolic_regression/repair.py` | Candidate-pool cleanup roots, expanded preset, AST dedup, verifier-gated repair metadata | VERIFIED | Exists; substantive; wired to optimizer candidates, snap-neighborhood expansion, and verifier. |
| `tests/test_repair.py` | Coverage for selected/fallback/retained roots, dedup, verifier gating, subtree alternatives | VERIFIED | Includes focused tests for defaults, fallback/retained repair, duplicate roots, dedup ownership, subtree provenance, and unrecovered variants. |
| `src/eml_symbolic_regression/benchmark.py` | Optional repair config, focused suite, cleanup routing, metrics extraction | VERIFIED | `BenchmarkRepairConfig`, `v1.9-repair-evidence`, three target-free cleanup call sites, and metric extraction are present. |
| `src/eml_symbolic_regression/campaign.py` | Campaign CSV/report visibility for repair metrics | VERIFIED | Run/failure columns include `repair_candidate_root_count`, `repair_deduped_variant_count`, and `repair_accepted_candidate_root_source`. |
| `tests/test_benchmark_runner.py` | Runner regressions for routing, fallback preservation, target-aware fallback | VERIFIED | Covers expanded config routing across blind/warm/perturbed paths and target-aware fallback after expanded target-free miss. |
| `tests/test_benchmark_contract.py` | Suite and run-id stability contracts | VERIFIED | Confirms no-repair run ids stay stable and repair settings only affect explicit repair runs. |
| `tests/test_benchmark_reports.py` | Aggregate taxonomy and repair metric preservation | VERIFIED | Confirms repaired candidates remain separate and metrics survive aggregate rows. |
| `tests/test_campaign.py` | Campaign table/report columns | VERIFIED | Confirms repair metric columns serialize for run and failure rows. |
| `artifacts/campaigns/v1.9-repair-evidence/v1.9-repair-evidence/suite-result.json` | Machine-readable focused suite output | VERIFIED | Parsed successfully; suite id is `v1.9-repair-evidence`; contains 4 results. |
| `artifacts/campaigns/v1.9-repair-evidence/v1.9-repair-evidence/aggregate.json` | Aggregate repair evidence counts | VERIFIED | Counts total 4 runs, 0 repaired candidates, 0 unsupported, 4 failed/snapped-but-failed. |
| `artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.json` | Before/after summary | VERIFIED | Parsed successfully; 2 pairs; expanded presets present; fallback manifests preserved in every pair. |
| `artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.md` | Human-readable evidence summary | VERIFIED | States focused repair-only evidence and measured no-improvement outcome. |
| `docs/IMPLEMENTATION.md` and `README.md` | Reproducible command, artifact paths, regime-safe claim language | VERIFIED | Both cite `v1.9-repair-evidence`, summary artifacts, `expanded_candidate_pool`, and `repaired_candidate` taxonomy boundaries. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `repair.py` | `optimize.py` | `FitResult.selected_candidate`, `fallback_candidate`, `candidates` | WIRED | `gsd-tools verify key-links` passed for plan 52-01. |
| `repair.py` | `master_tree.py` | `expand_snap_neighborhood(root.candidate.snap, bounded, ...)` | WIRED | Root-specific alternatives flow into snap-neighborhood expansion. |
| `repair.py` | `verify.py` | `verify_candidate()` gates repair promotion | WIRED | Best variant is promoted only when verifier status is `recovered`. |
| `benchmark.py` | `repair.py` | `RepairConfig.expanded_candidate_pool()` and `_repair_config_for_run(run)` | WIRED | Blind, warm-start, and perturbed-tree target-free cleanup pass configured repair settings. |
| `benchmark.py` | `campaign.py` | `_extract_run_metrics()` emits repair root/dedup metrics consumed by campaign rows | WIRED | Campaign tests verify run/failure CSV columns. |
| `tests/test_benchmark_runner.py` | `optimize.py` | Fake `FitResult` preserves selected/fallback manifests while cleanup promotes repair | WIRED | Runner test asserts manifest ids remain unchanged. |
| `repair-evidence-summary.json` | `suite-result.json` | Summary paths and pair records derived from suite results | WIRED | JSON validation cross-checked summary artifact paths against suite result paths. |
| `docs/IMPLEMENTATION.md` | `repair-evidence-summary.json` | Documented validated artifact path | WIRED | `rg` verified docs cite the summary JSON. |
| `README.md` | `benchmark.py` | Documented command uses built-in `v1.9-repair-evidence` suite | WIRED | Suite is registered in `BUILTIN_SUITES`. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|---|---|---|---|---|
| `repair.py` | candidate roots and variants | `FitResult` exact candidates plus `expand_snap_neighborhood()` | Yes | FLOWING - roots are enumerated, variants deduped, then verified before ranking. |
| `benchmark.py` | repair payload and metrics | `cleanup_failed_candidate(...).as_dict()` | Yes | FLOWING - top-level artifacts carry `repair`, `repair_status`, and metrics. |
| `campaign.py` | repair CSV columns | aggregate run `metrics` | Yes | FLOWING - row-first/metrics-fallback columns serialize root/dedup fields. |
| `repair-evidence-summary.json` | default/expanded pair metrics | generated suite result per-run artifacts | Yes | FLOWING - JSON validation confirmed pair/run links and fallback preservation booleans. |
| `README.md` / `docs/IMPLEMENTATION.md` | measured repair outcome | `repair-evidence-summary.json` | Yes | FLOWING - docs report 2 pairs, 0 improvements, 0 regressions, fallback preserved. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Phase artifacts exist and contain expected markers | `gsd-tools verify artifacts` for plans 52-01, 52-02, 52-03 | 15/15 artifacts passed | PASS |
| Declared key links are wired | `gsd-tools verify key-links` for plans 52-01, 52-02, 52-03 | 9/9 links verified | PASS |
| Focused source/test slice passes | `PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_repair.py tests/test_master_tree.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_benchmark_reports.py tests/test_campaign.py -q` | 155 passed, 11 existing numerical warnings, 222.19s | PASS |
| Generated evidence is structurally valid | Python JSON validation over suite, aggregate, and repair summary artifacts | Validated 2 pairs, 4 runs, fallback preserved | PASS |
| Docs cite evidence and taxonomy boundaries | `rg "v1\.9-repair-evidence|repair-evidence-summary|expanded candidate-pool cleanup|repaired_candidate|expanded_candidate_pool" README.md docs/IMPLEMENTATION.md` | Matches in both files | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| REP-01 | 52-01, 52-02 | Repair from more than selected snapped candidate, including fallback and retained exact candidates where available. | SATISFIED | `cleanup_candidate_sources` opt-in includes selected/fallback/retained; tests repair from fallback and retained roots; benchmark can route expanded preset. |
| REP-02 | 52-01, 52-02 | AST deduplication and verifier-gated ranking with a larger configurable neighborhood. | SATISFIED | Expanded preset is larger and bounded; roots/variants are deduped by serialized AST; verifier ranking precedes source tie-breakers. |
| REP-03 | 52-01, 52-02 | Cleanup can consider subtree-level alternatives where candidate provenance exposes them. | SATISFIED | Existing `NeighborhoodMove` subtree provenance is preserved in candidate-pool repair moves; tests assert subtree root and descendant/pruned assignments. |
| REP-04 | 52-02, 52-03 | Inspect targeted before/after evidence showing whether expanded cleanup improves near-miss subsets without weakening fallback behavior. | SATISFIED | `v1.9-repair-evidence` suite and summary artifacts compare default vs expanded runs, report no improvement, no regressions, and fallback manifest preservation. |

### Review And Review-Fix

`52-REVIEW.md` found one warning: per-root deduped variant counts could be credited to the wrong root when a later duplicate variant replaced an earlier one. `52-REVIEW-FIX.md` records the fix. The code now computes `deduped_counts_by_root` after the final `deduped_variants` map is stable, and `tests/test_repair.py::test_candidate_pool_dedup_counts_follow_replacement_owner` covers the replacement-owner case. The full verification pytest slice passed after this fix.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `src/eml_symbolic_regression/benchmark.py` | 798 | local variable named `placeholder` | INFO | Not a stub; it is a temporary `BenchmarkRun` used to compute the stable run id before setting `artifact_path`. |
| Source files | various | optional `None` and empty collection defaults | INFO | Dataclass defaults and normal accumulator initialization; no user-visible hardcoded empty data path found. |

No TODO/FIXME/coming-soon/not-implemented markers were found in the Phase 52 source, tests, docs, or generated summary artifacts.

### Human Verification Required

None. The phase deliverables are code, tests, JSON/Markdown artifacts, and documentation. All declared behaviors were verified with source tracing and commands.

### Risks And Notes

- The focused real near-miss suite measured no expanded-cleanup improvement. This is not a failure of REP-04 because the artifact explicitly reports the result and confirms no final-status regressions or fallback-manifest weakening.
- Exact-AST root dedup intentionally collapses duplicate selected/fallback/retained roots. If future evidence shows same-AST duplicate candidates can expose materially different slot alternatives, a later phase may need merged provenance per deduped root; Phase 52's stated contract and tests require duplicate roots to be considered once.
- Planning metadata note: `.planning/ROADMAP.md` marks Phase 52 complete in the phase list, while a lower requirements table still lists REP-01 through REP-04 as `Pending`; `.planning/REQUIREMENTS.md` marks them complete. This is a roadmap bookkeeping inconsistency, not a code or evidence gap for this phase.

### Gaps Summary

No blocking gaps found. Phase 52 achieved its goal.

---

_Verified: 2026-04-17T16:00:27Z_  
_Verifier: Claude (gsd-verifier)_
