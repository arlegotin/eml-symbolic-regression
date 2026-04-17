---
phase: 48-paper-decision-refresh-and-milestone-audit
reviewed: 2026-04-17T06:42:02Z
depth: standard
files_reviewed: 12
files_reviewed_list:
  - src/eml_symbolic_regression/benchmark.py
  - src/eml_symbolic_regression/campaign.py
  - src/eml_symbolic_regression/cli.py
  - src/eml_symbolic_regression/family_triage.py
  - src/eml_symbolic_regression/paper_decision.py
  - src/eml_symbolic_regression/optimize.py
  - tests/test_benchmark_contract.py
  - tests/test_campaign.py
  - tests/test_benchmark_runner.py
  - tests/test_family_triage.py
  - tests/test_optimizer_cleanup.py
  - tests/test_paper_decision.py
findings:
  critical: 0
  warning: 2
  info: 1
  total: 3
status: issues_found
---

# Phase 48: Code Review Report

**Reviewed:** 2026-04-17T06:42:02Z
**Depth:** standard
**Files Reviewed:** 12
**Status:** issues_found

## Summary

Reviewed the v1.8 centered-family suite expansion, campaign wiring, CLI diagnostics, triage artifacts, paper decision memo generation, optimizer metadata, and focused tests. No security issues were found. Two reporting/metadata bugs can corrupt v1.8 evidence artifacts, and one stale copy issue remains in the paper-decision output.

Review verification was static plus two focused probes: a centered `v1.8-family-basin` perturbed-tree row records `perturbed_true_tree.reason=centered_family_same_family_seed_missing` but aggregate reason `unsupported`, and a `v1.8-family-smoke` centered run carries the stale `v1.7` tag. The full pytest suite was not run as part of this read-only review.

## Warnings

### WR-01: Centered Perturbed-Tree Unsupported Reasons Are Lost In Aggregates

**File:** `src/eml_symbolic_regression/benchmark.py:2841`

**Issue:** `_execute_benchmark_run_inner()` now fails closed for centered perturbed-tree rows with `perturbed_true_tree.reason = "centered_family_same_family_seed_missing"`, but `_run_reason()` only checks `compiled_eml`, `warm_start_eml`, and verifier blocks. As a result, `_run_summary()` and `metrics.unsupported_reason` collapse those rows to generic `"unsupported"`. `family_triage._classification_for_run()` depends on the aggregate reason to classify missing same-family seed rows as `missing_integration`, so centered basin/depth-curve rows can be reported as measured failures instead of accepted fail-closed integration gaps.

**Fix:**
```python
def _run_reason(payload: Mapping[str, Any]) -> str:
    ...
    warm = payload.get("warm_start_eml")
    if isinstance(warm, Mapping) and warm.get("status") == "unsupported":
        return str(warm.get("reason") or "unsupported")

    perturbed = payload.get("perturbed_true_tree")
    if isinstance(perturbed, Mapping) and perturbed.get("status") == "unsupported":
        return str(perturbed.get("reason") or "unsupported")

    for key in ("trained_eml_verification", "compiled_eml_verification", "verification"):
        ...
```

Add a regression test that runs a centered `v1.8-family-basin` or `v1.8-family-depth-curve` perturbed-tree case and asserts both `artifact["metrics"]["unsupported_reason"]` and `aggregate["runs"][0]["reason"]` preserve `centered_family_same_family_seed_missing`.

### WR-02: v1.8 Family Suites Are Tagged As v1.7

**File:** `src/eml_symbolic_regression/benchmark.py:980`

**Issue:** `_family_case()` hardcodes `"v1.7"` into every cloned family case. The new v1.8 suites and calibration suite reuse this helper, so generated v1.8 run/case artifacts carry `tags: ["v1.7", "family_matrix", ...]`. That makes downstream evidence metadata and any tag-based filtering/auditing ambiguous or wrong for the v1.8 paper decision package.

**Fix:**
```python
def _family_case(base: BenchmarkCase, variant: _OperatorVariant, *, suite_tag: str) -> BenchmarkCase:
    return replace(
        base,
        id=f"{base.id}-{variant.id}",
        optimizer=_operator_variant_budget(base.optimizer, variant),
        tags=tuple(dict.fromkeys((*base.tags, suite_tag, "family_matrix", *variant.tags))),
        claim_id=None,
        threshold_policy_id=None,
        expect_recovery=False if not variant.operator_family.is_raw else base.expect_recovery,
    )
```

Pass `suite_tag="v1.7"` from the v1.7 suite builder and `suite_tag="v1.8"` from the v1.8/calibration builders. Add a test that `load_suite("v1.8-family-smoke").expanded_runs()` includes `"v1.8"` and excludes `"v1.7"` on v1.8 cases.

## Info

### IN-01: Paper Decision Wait Recommendation Still Names v1.7 Campaigns

**File:** `src/eml_symbolic_regression/paper_decision.py:140`

**Issue:** The default output root and memo header moved to v1.8, but the no-centered-evidence recommendation still says to run the v1.7 family campaigns first. This is stale generated paper-facing copy and can confuse milestone evidence provenance.

**Fix:** Change the text to v1.8 or to version-neutral wording, for example:

```python
"Do not submit the centered-family empirical paper yet. Run the current family campaigns first; "
```

Add a lightweight assertion that the v1.8 decision memo package does not emit stale `v1.7` campaign guidance.

---

_Reviewed: 2026-04-17T06:42:02Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
