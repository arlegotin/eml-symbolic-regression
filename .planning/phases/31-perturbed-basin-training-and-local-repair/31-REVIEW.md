---
phase: 31-perturbed-basin-training-and-local-repair
reviewed: 2026-04-15T19:40:35Z
depth: standard
files_reviewed: 19
files_reviewed_list:
  - src/eml_symbolic_regression/basin.py
  - src/eml_symbolic_regression/datasets.py
  - src/eml_symbolic_regression/benchmark.py
  - src/eml_symbolic_regression/proof.py
  - src/eml_symbolic_regression/repair.py
  - src/eml_symbolic_regression/diagnostics.py
  - src/eml_symbolic_regression/campaign.py
  - src/eml_symbolic_regression/cli.py
  - tests/test_basin_targets.py
  - tests/test_benchmark_contract.py
  - tests/test_benchmark_runner.py
  - tests/test_proof_contract.py
  - tests/test_repair.py
  - tests/test_benchmark_reports.py
  - tests/test_basin_bound_report.py
  - tests/test_campaign.py
  - tests/test_diagnostics.py
  - artifacts/diagnostics/phase31-basin-bound/basin-bound.json
  - artifacts/diagnostics/phase31-basin-bound/basin-bound.md
findings:
  critical: 0
  warning: 3
  info: 1
  total: 4
status: issues_found
---

# Phase 31: Code Review Report

**Reviewed:** 2026-04-15T19:40:35Z
**Depth:** standard
**Files Reviewed:** 19
**Status:** issues_found

## Summary

Reviewed the Phase 31 perturbed-basin runner, local repair path, proof taxonomy, campaign/diagnostics reporting, tests, and locked Beer-Lambert bound evidence. The core implementation preserves raw perturbed-tree status separately from repaired candidates, but the aggregate/reporting guardrails still allow claim inflation in two paths: generic bounded evidence classes can satisfy the perturbed-basin threshold, and the bound report can support a noise level from incomplete seed evidence. The locked evidence also points at non-repo `/tmp` run artifacts, which weakens repair/verifier provenance from a clean checkout.

Verification run: `PYTHONPATH=src python -m pytest tests/test_basin_targets.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_proof_contract.py tests/test_repair.py tests/test_benchmark_reports.py tests/test_basin_bound_report.py tests/test_campaign.py tests/test_diagnostics.py -q -m "not integration"` -> 113 passed, 1 deselected, 2 warnings.

## Warnings

### WR-01: Perturbed-Basin Threshold Still Accepts Non-Perturbed Evidence Classes

**File:** `src/eml_symbolic_regression/benchmark.py:1659-1662`
**Issue:** `_counted_evidence_classes_for_claim()` only narrows the bounded allowlist for `paper-shallow-blind-recovery`. For `paper-perturbed-true-tree-basin`, `_threshold_summary()` still uses the generic `bounded_100_percent` allowlist from `proof.py`, which includes `compiler_warm_start_recovered` and `verified_equivalent`. That means a row carrying the perturbed-basin claim metadata but classified as compiler warm-start recovery can pass the perturbed-basin threshold, violating Phase 31's separation from compiler warm starts and the Phase 30 scaffolded-vs-blind blocker pattern.
**Fix:**
```python
def _counted_evidence_classes_for_claim(claim_id: str, policy_classes: tuple[str, ...]) -> tuple[str, ...]:
    if claim_id == "paper-shallow-blind-recovery":
        return (EVIDENCE_CLASSES["blind_training_recovered"],)
    if claim_id == "paper-perturbed-true-tree-basin":
        return (
            EVIDENCE_CLASSES["perturbed_true_tree_recovered"],
            EVIDENCE_CLASSES["repaired_candidate"],
        )
    return policy_classes
```
Add a regression test where a `paper-perturbed-true-tree-basin` aggregate row with `compiler_warm_start_recovered`, `verified_equivalent`, `same_ast`, or `scaffolded_blind_training_recovered` fails the threshold.

### WR-02: Bound Report Can Support a Noise Level from Incomplete Seed Evidence

**File:** `src/eml_symbolic_regression/diagnostics.py:526-540`
**Issue:** `_supported_noise_prefix()` checks only rows that are present for each noise. It has no expected seed/case inventory, so an aggregate with only one passing seed at noise `5.0` reports `raw_supported_noise_max == 5.0` and can recommend `support_declared_bound`. Phase 31's declared contract includes seeds as part of the bound, so missing rows should be treated as incomplete or unsupported rather than silently shrinking the denominator.
**Fix:**
```python
def _supported_noise_prefix(rows, grid, predicate, *, expected_seeds: tuple[int, ...]) -> float | None:
    by_noise: dict[float, list[Mapping[str, Any]]] = {}
    for row in rows:
        by_noise.setdefault(float(row["perturbation_noise"]), []).append(row)

    expected = set(expected_seeds)
    supported = None
    for noise in sorted(grid):
        noise_rows = by_noise.get(float(noise), [])
        observed = {int(row["seed"]) for row in noise_rows if row.get("seed") is not None}
        if observed != expected:
            break
        if not all(predicate(row) for row in noise_rows):
            break
        supported = float(noise)
    return supported
```
Also serialize missing seed/noise rows in the report, and update tests so one passing seed out of two does not support the declared bound.

### WR-03: Locked Evidence References Ephemeral `/tmp` Run Artifacts

**File:** `artifacts/diagnostics/phase31-basin-bound/basin-bound.json:21`
**Issue:** The committed bound evidence cites raw run artifacts under `/tmp/eml-phase31-basin-bound/...` for every bounded and probe row. Those files are not part of the repo artifact set and may not exist on a clean checkout or another machine, so the locked evidence cannot independently prove the verifier/repair provenance it points to. This weakens BASN-03/D-07 because the report links raw outcomes without durable raw artifacts or checksums.
**Fix:** Generate the integration evidence under a committed or reproducible artifact root such as `artifacts/diagnostics/phase31-basin-bound/raw-runs/`, or embed stable `artifact_sha256` plus a minimal raw-run payload snapshot in `basin-bound.json`. Use relative artifact paths in both JSON and Markdown so the evidence remains inspectable from a clean checkout.

## Info

### IN-01: Integration Mark Is Not Registered

**File:** `tests/test_basin_bound_report.py:336`
**Issue:** The fast verification run emits `PytestUnknownMarkWarning` for `pytest.mark.integration`. This does not currently fail the suite, but it will fail under strict marker settings and adds noise to every Phase 31 verification run.
**Fix:** Register the marker in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
markers = [
  "integration: slower benchmark/evidence generation tests",
]
```

---

_Reviewed: 2026-04-15T19:40:35Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
