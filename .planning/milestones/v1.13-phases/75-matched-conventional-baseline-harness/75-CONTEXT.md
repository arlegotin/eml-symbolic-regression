# Phase 75: Matched Conventional Baseline Harness - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning
**Mode:** Autonomous smart-discuss equivalent

<domain>
## Phase Boundary

Phase 75 adds a standardized baseline-comparison harness. It must keep EML rows, conventional symbolic baselines, dataset manifests, seeds, budgets, constants policy, and blind/warm-start conditions in one comparable contract without merging baseline results into EML recovery denominators.

</domain>

<decisions>
## Implementation Decisions

### Matched Contract First

Create a dedicated harness module instead of overloading the existing benchmark runner. Existing benchmark suites own EML recovery denominators; the baseline harness owns comparison rows.

### Runnable Built-In Conventional Baseline

Include a small deterministic least-squares polynomial symbolic baseline using NumPy/SymPy. It is not a replacement for PySR/gplearn, but it gives the harness a runnable conventional symbolic row without adding dependencies or network setup.

### External Adapters Fail Closed

Check optional external SR adapters (`pysr`, `gplearn`, `pyoperon`, `karoo_gp`) with `importlib`. Missing integrations produce explicit `unavailable` rows and dependency locks instead of installing packages or silently dropping comparators.

### Denominator Separation

Every output must state that baseline rows are excluded from EML recovery denominators. EML reference rows are comparison controls, not new recovery claims.

</decisions>

<code_context>
## Existing Code Insights

- `datasets.py` now exposes expanded dataset splits and manifests with roles, units, source metadata, and compatibility tags.
- `verify.py` can score arbitrary `Candidate` objects across multi-role splits and reports final-confirmation metrics.
- `benchmark.py` already separates track metadata and EML recovery denominators; Phase 75 should not mutate that runner for baseline comparisons.
- `paper_v112.py` has a bounded diagnostic-only dependency probe for conventional SR packages, but not a matched run contract.

</code_context>

<specifics>
## Specific Ideas

- Add `baselines.py` with a row-oriented harness.
- Support adapters:
  - `eml_reference`,
  - `polynomial_least_squares`,
  - `pysr`,
  - `gplearn`,
  - `pyoperon`,
  - `karoo_gp`.
- Write JSON, CSV, Markdown, manifest, and dependency-lock artifacts.
- Add CLI command `baseline-harness`.
- Add tests for:
  - shared dataset manifests and budgets,
  - runnable polynomial baseline,
  - fail-closed external dependency rows,
  - EML denominator separation,
  - CLI artifact generation.

</specifics>

<deferred>
## Deferred Ideas

- Running full PySR/gplearn/pyoperon searches is deferred until dependencies are intentionally installed and source-locked.
- Publication table integration and full evidence rebuild remain Phase 76.

</deferred>
