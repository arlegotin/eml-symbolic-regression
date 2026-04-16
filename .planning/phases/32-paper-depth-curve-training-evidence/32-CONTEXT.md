# Phase 32: Paper Depth-Curve Training Evidence - Context

**Gathered:** 2026-04-16
**Status:** Ready for planning
**Mode:** Auto-discuss from roadmap, proof-contract context, and live depth-curve probes

<domain>
## Phase Boundary

Phase 32 owns the paper-style blind-versus-perturbed depth curve. It must run real training over a deterministic exact EML inventory at depths 2 through 6, report the measured behavior by training mode, and keep deeper blind failures visible as expected boundary evidence rather than as product regressions.

The phase does not attempt to prove universal blind recovery beyond shallow depth. It exists to show the implementation behaves qualitatively like the paper: shallow blind recovery is possible, deeper blind recovery degrades, and perturbed true-tree starts remain materially more reliable on the same exact targets.

</domain>

<decisions>
## Implementation Decisions

### Depth-Curve Scope

- **D-01:** Use a small deterministic exact EML target inventory with one target each at depths 2, 3, 4, 5, and 6.
- **D-02:** Use the same real-axis train, held-out, and extrapolation domain structure across the inventory so depth is the primary changing variable.
- **D-03:** Pair every depth with two execution paths: `blind` + `blind_training` and `perturbed_tree` + `perturbed_true_tree_training`.

### Evidence Semantics

- **D-04:** The depth curve is measured evidence governed by `measured_depth_curve`, not a bounded 100% proof threshold.
- **D-05:** Blind failures at deeper depths remain first-class output rows and must not be rewritten into regressions or hidden from reports.
- **D-06:** Perturbed rows count as comparative basin evidence only when they preserve the explicit perturbed-tree metadata and use nonzero perturbation noise.

### Reporting and Preservation

- **D-07:** Aggregate reports must expose per-depth blind and perturbed recovery rates, seed counts, losses, runtime, and snap metrics.
- **D-08:** Campaign outputs must write a dedicated depth-curve section and depth-curve recovery plot so later milestone reporting can consume them directly.
- **D-09:** Raw artifacts must be reproducibly generated through the built-in `proof-depth-curve` suite and campaign preset so future optimizer changes can compare against the same v1.5 baseline.

### the agent's Discretion

- Choose the exact depth-curve expressions as long as they are exact EML, verifier-safe on the declared real-axis domains, and show the intended qualitative behavior under live training.
- Choose the smallest CI-scale budgets that still separate shallow blind recovery from deeper blind degradation without weakening verifier ownership.

</decisions>

<specifics>
## Specific Ideas

- Depth 2 uses a simple exact EML form with linear real-axis behavior.
- Depth 3 uses the principal-branch `log(x)` identity already expressible in exact EML.
- Depths 4 through 6 should stay finite on the declared domains while remaining difficult enough that blind recovery degrades.
- Phase 30 and Phase 31 already established the measured pure-blind boundary and perturbed true-tree execution path; this phase should reuse those semantics rather than inventing a new training taxonomy.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase and Claim Context
- `.planning/REQUIREMENTS.md` - CURV-01 through CURV-04.
- `.planning/ROADMAP.md` - Phase 32 goal, success criteria, and dependencies.
- `.planning/STATE.md` - v1.5 milestone context and the Phase 32 starting point.
- `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-VERIFICATION.md` - proof claim and threshold contract.
- `.planning/phases/30-bounded-shallow-blind-training-recovery/30-VERIFICATION.md` - measured pure-blind versus bounded scaffolded split.
- `.planning/phases/31-perturbed-basin-training-and-local-repair/31-VERIFICATION.md` - perturbed-tree runner, repair semantics, and basin evidence.

### Existing Code
- `src/eml_symbolic_regression/datasets.py` - demo-spec registry and proof dataset manifests.
- `src/eml_symbolic_regression/benchmark.py` - built-in proof suites, runner artifacts, threshold summaries, and aggregate report plumbing.
- `src/eml_symbolic_regression/proof.py` - `paper-blind-depth-degradation` claim metadata.
- `src/eml_symbolic_regression/campaign.py` - campaign presets, CSV/report generation, and plot hooks.
- `src/eml_symbolic_regression/cli.py` - benchmark/campaign commands and future proof-bundle entry point.

### Tests
- `tests/test_benchmark_contract.py`
- `tests/test_benchmark_runner.py`
- `tests/test_benchmark_reports.py`
- `tests/test_campaign.py`

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- Proof dataset manifests already capture deterministic provenance, domains, and split signatures.
- The perturbed true-tree runner already exists and is verifier-owned from Phase 31.
- Threshold summaries already distinguish bounded proof claims from measured claim boundaries.
- Campaign reports already support proof tables and are the natural place to add depth-curve tables and plots.

### Likely Gaps

- No deterministic depth-2 through depth-6 exact target inventory exists yet.
- No built-in `proof-depth-curve` suite exists yet.
- Aggregate JSON and Markdown do not yet summarize measured blind versus perturbed recovery by depth.
- No dedicated proof-campaign bundle exists yet to preserve the depth-curve raw artifacts under a stable v1.5 root.

</code_context>

<deferred>
## Deferred Ideas

- One-command proof bundle assembly belongs to Phase 33.
- Universal blind recovery claims beyond this deterministic inventory remain out of scope for v1.5.

</deferred>

---

*Phase: 32-paper-depth-curve-training-evidence*
*Context gathered: 2026-04-16*
