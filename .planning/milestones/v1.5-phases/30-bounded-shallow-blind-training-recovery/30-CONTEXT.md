# Phase 30: Bounded Shallow Blind Training Recovery - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 30 turns the Phase 29 proof contract into a passing bounded shallow blind-training suite. The deliverable is 100% verifier-owned blind recovery over the declared shallow proof suite, including the current `radioactive_decay` and Beer-Lambert-style scaled exponential failures plus signed/scaled exponential variants. This phase may add paper-grounded blind initializers, shallow target inventory, diagnostics, and regression tests, but it must not count catalog, compiler, or warm-start evidence as proof success.

</domain>

<decisions>
## Implementation Decisions

### Proof Suite Scope
- **D-01:** Count only proof-aware blind runs whose derived `evidence_class` is `blind_training_recovered` toward the bounded 100% target.
- **D-02:** Extend the declared shallow proof inventory beyond `exp`, `log`, `radioactive_decay`, and Beer-Lambert to include signed/scaled exponential variants that are shallow enough for this milestone's bounded claim.
- **D-03:** Keep suite seeds, budgets, tolerances, claim IDs, and threshold policies in the suite/case contract; CLI filters are allowed for debugging but cannot redefine the proof target.
- **D-04:** If any proposed signed/scaled variant cannot be supported without exceeding the paper-realistic shallow bound, narrow the supported variant set only with committed evidence and an explicit contract update.

### Recovery Strategy
- **D-05:** Prefer paper-grounded scaffold initializers and shallow EML identities for exponential, logarithmic, scaled exponential, signed exponential, and exponential decay families before increasing generic random-search budgets.
- **D-06:** Preserve blind-training semantics: an initializer may bias the soft master tree from formula-family priors, but it must still train, snap, and pass the verifier; do not route through compiler warm starts or catalog candidates.
- **D-07:** Treat `radioactive_decay` and Beer-Lambert failures as first-class proof targets rather than diagnostics to hide or defer.
- **D-08:** Keep runtime practical for regression tests. Use the smallest deterministic depths, steps, restarts, constants, and seeds that meet the declared proof suite.

### Diagnostics and Regression Gates
- **D-09:** Every proof run artifact must explain scaffold source, best soft loss, post-snap loss, snap margin, active node count, status, and verifier/evidence class.
- **D-10:** Add regression tests that fail if the declared shallow proof suite drops below 100% bounded threshold status.
- **D-11:** Preserve failure diagnostics for any non-proof exploratory variants so future phases can inspect scaffold choice, loss behavior, and snap decisions.
- **D-12:** Keep the existing Phase 29 claim/threshold/evidence taxonomy intact; Phase 30 should improve training behavior, not loosen the definition of recovery.

### the agent's Discretion
- Choose exact scaffold names, helper functions, and tests consistent with the current `optimize.py`, `master_tree.py`, and `benchmark.py` patterns.
- Choose whether signed/scaled exponential variants live in `datasets.py` as new `DemoSpec` entries or in a proof-suite-only target helper, provided artifacts retain formula provenance.
- Choose the least invasive optimizer extension that reaches the bounded proof target with deterministic tests.

</decisions>

<specifics>
## Specific Ideas

- Current baseline run on 2026-04-15: `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.5-shallow-proof --output-dir /tmp/eml-phase30-baseline` recovered 6/12, with all `exp` and `log` runs recovered and all `radioactive_decay` plus Beer-Lambert runs snapped-but-failed.
- Baseline failing scaled exponential runs had snap margins of `1.0` and active node count `7`, so the wrong exact shallow shape is being selected confidently rather than failing from low snap confidence.
- The proof target should become `bounded_100_percent` passed for `paper-shallow-blind-recovery`.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 30 Scope
- `.planning/REQUIREMENTS.md` — SHAL-01 through SHAL-04 and v1.5 out-of-scope boundaries.
- `.planning/ROADMAP.md` — Phase 30 goal, success criteria, and dependency on Phase 29.
- `.planning/STATE.md` — Current milestone decisions and warning against universal deep blind-recovery claims.
- `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-VERIFICATION.md` — Verified Phase 29 proof contract behavior and key links.

### Existing Code
- `src/eml_symbolic_regression/proof.py` — Claim, threshold, training-mode, and evidence-class contract.
- `src/eml_symbolic_regression/datasets.py` — Demo target definitions, provenance fields, and proof dataset manifests.
- `src/eml_symbolic_regression/benchmark.py` — Built-in proof suite, run artifacts, evidence class derivation, metrics, and threshold aggregation.
- `src/eml_symbolic_regression/optimize.py` — Blind training loop, scaffold attempts, diagnostics manifest, and `TrainingConfig`.
- `src/eml_symbolic_regression/master_tree.py` — Soft tree snapping, forced `exp`/`log` scaffold helpers, snap margins, and active node counts.
- `src/eml_symbolic_regression/diagnostics.py` — Blind failure classifier and campaign comparison helpers.

### Tests and Evidence
- `tests/test_optimizer_cleanup.py` — Current optimizer scaffold tests.
- `tests/test_benchmark_contract.py` — `v1.5-shallow-proof` suite contract tests.
- `tests/test_benchmark_runner.py` — Proof-aware run artifact and CLI smoke tests.
- `tests/test_benchmark_reports.py` — Threshold summary and bounded proof aggregation tests.
- `/tmp/eml-phase30-baseline/v1.5-shallow-proof/aggregate.md` — Local baseline evidence generated during smart discuss; useful for planning only, not a committed artifact.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `TrainingConfig.scaffold_initializers` already controls scaffold attempts before random restarts.
- `_apply_scaffold()` currently supports `scaffold_exp` and `scaffold_log` and records scaffold provenance in the optimizer manifest.
- `SoftEMLTree.force_exp()` and `force_log()` already create exact high-margin snapped identities.
- `BenchmarkCase` and `BenchmarkRun` now carry proof metadata and deterministic budgets.
- `aggregate_evidence()` already reports claim-level threshold status from derived evidence classes.

### Established Patterns
- Recovery claims are verifier-owned and evaluated through `verify_candidate()` over train, held-out, extrapolation, and high-precision checks.
- Suite contracts fail closed for malformed proof metadata; Phase 30 should keep this posture.
- Tests use small deterministic suites and focused CLI filters to keep runtime acceptable.
- Optimizer manifests record `best_loss`, `post_snap_loss`, `snap.min_margin`, `snap.active_node_count`, restart logs, and scaffold initialization logs.

### Integration Points
- Add new proof targets in `datasets.py` and register them in the proof suite in `benchmark.py`.
- Add or extend scaffold initializers in `optimize.py` and `master_tree.py`.
- Add proof-suite regression checks in benchmark/report tests, and optimizer-specific tests for any new scaffold behavior.
- Campaign/report code should not need Phase 30-specific changes unless new fields are required for diagnostics.

</code_context>

<deferred>
## Deferred Ideas

- Perturbed true-tree basin recovery and local snap/discrete repair belong to Phase 31.
- Depth 2 through 6 recovery curves belong to Phase 32.
- Final proof campaign report and committed raw evidence lockdown belong to Phase 33.
- External noisy datasets and non-shallow arbitrary elementary formulas remain out of scope for v1.5.

</deferred>

---

*Phase: 30-bounded-shallow-blind-training-recovery*
*Context gathered: 2026-04-15*
