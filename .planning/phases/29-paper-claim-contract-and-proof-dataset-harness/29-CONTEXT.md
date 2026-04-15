# Phase 29: Paper Claim Contract and Proof Dataset Harness - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 29 defines the v1.5 proof-suite contract: every experiment must map to a paper-grounded claim, a deterministic dataset split contract, a training/evidence mode, and explicit pass/fail thresholds. This phase does not need to improve recovery rates; Phases 30 and 31 use this contract to improve and prove training behavior.

</domain>

<decisions>
## Implementation Decisions

### Claim Taxonomy
- **D-01:** Treat verifier-owned training recovery as the only evidence class that can satisfy bounded 100% training-proof claims.
- **D-02:** Keep catalog verification, compile-only verification, blind training, compiler warm-start training, perturbed true-tree training, repaired candidates, unsupported cases, and failed cases as distinct artifact classes.
- **D-03:** Add a paper-claim matrix with stable claim IDs, paper-grounded statement text, source references, supported claim class, associated suite/cases, and threshold policy.
- **D-04:** Declare pass/fail thresholds before execution; bounded proof suites require 100% verifier-owned recovery, while depth-curve suites report measured behavior without treating expected deeper blind failures as regressions.

### Dataset Contract
- **D-05:** Generate deterministic train, held-out, and extrapolation splits with fixed seeds, sample counts, domains, variable name, formula ID, and normalization metadata.
- **D-06:** Preserve formula provenance in artifacts: symbolic expression, source document, FOR_DEMO or paper linkage, and whether the target is a normalized dimensionless law.
- **D-07:** Generate proof datasets on demand and serialize their metadata into run artifacts; do not commit bulky raw arrays unless a later evidence-lockdown phase explicitly requires them.
- **D-08:** Attach optimizer budgets, seeds, perturbation noise envelopes, and suite thresholds to the suite/case contract so CLI arguments cannot silently redefine proof claims.

### Artifact Schema
- **D-09:** Extend benchmark/proof artifacts rather than creating an unrelated reporting system; reuse existing `benchmark.py`, `campaign.py`, dataset split, verifier, and diagnostics patterns.
- **D-10:** Every run artifact should expose `claim_id`, `claim_class`, `training_mode`, `evidence_class`, `threshold`, `dataset`, `budget`, and `provenance` fields in stable JSON-friendly structures.
- **D-11:** Aggregates must count evidence classes separately, especially blind verifier recovery versus compile/catalog success, unsupported, soft-fit-only, snapped-but-failed, repaired, same-AST, and verified-equivalent outcomes.
- **D-12:** Validation should fail closed when a suite references an unknown claim, missing threshold, invalid split, unsupported training mode, or ambiguous evidence class.

### the agent's Discretion
- Choose exact dataclass names and helper function layout consistent with the current benchmark module.
- Choose whether the first implementation introduces a new module or keeps the contract in `benchmark.py`, provided downstream phases can import it cleanly.
- Choose concise test fixtures that prove the schema without running expensive training loops.

</decisions>

<specifics>
## Specific Ideas

- Preserve the v1.5 milestone distinction that "100% fully functional training" means 100% over declared bounded proof suites, not universal blind recovery.
- Keep the current `radioactive_decay` blind failure family visible as a target for Phase 30 rather than hiding it behind compiler or catalog evidence.
- Favor small deterministic fixtures and metadata assertions in Phase 29; expensive recovery campaigns belong to later phases.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project and Milestone Scope
- `.planning/PROJECT.md` — Core value, paper-fidelity constraints, and completed milestone context.
- `.planning/REQUIREMENTS.md` — v1.5 CLAIM requirements and out-of-scope boundaries.
- `.planning/ROADMAP.md` — Phase 29 goal, success criteria, dependencies, and requirement mapping.
- `.planning/STATE.md` — Current v1.5 decisions and warning against universal deep blind-recovery claims.

### Source Documents
- `sources/NORTH_STAR.md` — Hybrid pipeline, train/evaluate split, complete master tree, snapping, verifier, and evidence expectations.
- `sources/FOR_DEMO.md` — Demo formula provenance and guidance for normalized, dimensionless showcase laws.
- `sources/paper.pdf` — EML definition, complete-tree search framing, complex arithmetic, PyTorch training notes, and reported depth degradation.

### Existing Implementation
- `src/eml_symbolic_regression/benchmark.py` — Suite, case, run, artifact, aggregate, and evidence classification contracts.
- `src/eml_symbolic_regression/datasets.py` — Demo split generation and formula provenance inputs.
- `src/eml_symbolic_regression/campaign.py` — Campaign manifests, tables, figures, and report assembly patterns.
- `src/eml_symbolic_regression/cli.py` — Existing benchmark and campaign CLI entry points.
- `tests/test_benchmark_contract.py` — Current suite contract tests.
- `tests/test_benchmark_runner.py` — Current run artifact and CLI smoke tests.
- `tests/test_campaign.py` — Current campaign manifest, table, plot, and report tests.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `BenchmarkCase`, `BenchmarkSuite`, `BenchmarkRun`, and `BenchmarkRunResult` already provide dataclass-style suite expansion and JSON serialization.
- `DemoSpec.make_splits()` already creates deterministic train, held-out, and extrapolation splits; Phase 29 can expose metadata around that behavior.
- `aggregate_evidence()` and campaign table/report writers already separate recovery classifications and can be extended to include claim classes.

### Established Patterns
- The code uses frozen dataclasses, standard-library JSON, fail-closed validation exceptions, and deterministic run IDs derived from normalized payloads.
- Tests prefer fast fixture-level assertions and filtered suite execution over full campaign runs.
- CLI commands print artifact paths and write JSON/Markdown artifacts under `artifacts/`.

### Integration Points
- Built-in benchmark suite registration in `benchmark.py` is the natural place for v1.5 proof-suite contract metadata.
- Campaign reporting in `campaign.py` can consume aggregate evidence without owning the lower-level claim contract.
- CLI benchmark filters already support formula, start mode, case, seed, and perturbation noise filters; proof-suite additions should preserve that interface.

</code_context>

<deferred>
## Deferred Ideas

- Training improvements for `radioactive_decay`, scaled exponentials, and signed exponentials belong to Phase 30.
- Perturbed true-tree target generation and local repair belong to Phase 31.
- Depth 2 through 6 measured recovery curves belong to Phase 32.
- One-command proof report and evidence lockdown belong to Phase 33.

</deferred>

---

*Phase: 29-paper-claim-contract-and-proof-dataset-harness*
*Context gathered: 2026-04-15*
