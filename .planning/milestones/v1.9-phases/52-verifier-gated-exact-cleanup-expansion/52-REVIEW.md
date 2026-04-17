---
phase: 52-verifier-gated-exact-cleanup-expansion
reviewed: 2026-04-17T15:49:24Z
depth: standard
files_reviewed: 13
files_reviewed_list:
  - src/eml_symbolic_regression/repair.py
  - src/eml_symbolic_regression/benchmark.py
  - src/eml_symbolic_regression/campaign.py
  - tests/test_repair.py
  - tests/test_benchmark_runner.py
  - tests/test_benchmark_contract.py
  - tests/test_benchmark_reports.py
  - tests/test_campaign.py
  - docs/IMPLEMENTATION.md
  - README.md
  - artifacts/campaigns/v1.9-repair-evidence/repair-evidence-summary.json
  - artifacts/campaigns/v1.9-repair-evidence/v1.9-repair-evidence/aggregate.json
  - artifacts/campaigns/v1.9-repair-evidence/v1.9-repair-evidence/suite-result.json
findings:
  critical: 0
  warning: 1
  info: 0
  total: 1
status: issues_found
---

# Phase 52: Code Review Report

**Reviewed:** 2026-04-17T15:49:24Z
**Depth:** standard
**Files Reviewed:** 13
**Status:** issues_found

## Summary

Reviewed the verifier-gated repair expansion across repair implementation, benchmark integration, campaign reporting, tests, docs, and sampled generated repair-evidence artifacts. Candidate root ordering, verifier-gated acceptance, repair taxonomy, run identity, and generated artifact validity are mostly coherent. One diagnostics bug can misattribute deduplicated repair variants to the wrong candidate root when a later root replaces an earlier duplicate expression.

Generated JSON artifacts were sampled rather than line-reviewed; all generated JSON files under `artifacts/campaigns/v1.9-repair-evidence/v1.9-repair-evidence/` parsed successfully.

Verification run:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest tests/test_repair.py tests/test_benchmark_runner.py tests/test_benchmark_contract.py tests/test_benchmark_reports.py tests/test_campaign.py
```

Result: 142 passed, 9 numerical RuntimeWarnings from existing EML semantics/verifier overflow and divide-by-zero paths.

## Warnings

### WR-01: Per-root Dedup Counts Can Be Credited To The Wrong Candidate Root

**File:** `src/eml_symbolic_regression/repair.py:216`

**Issue:** `cleanup_failed_candidate()` builds `variants_by_candidate_root` while it is still deduplicating variants globally. `deduped_for_root` increments only when a root first inserts a variant, but if a later root produces the same serialized expression with a stronger `_cleanup_variant_dedup_key()`, line 217 replaces `deduped_variants[key]` without moving the per-root count from the old root to the replacement root. In that case the accepted move provenance can correctly point at the later root, while `variants_by_candidate_root[*].deduped_variant_count` still credits the earlier root. This affects repair evidence diagnostics and report extraction for candidate root contribution counts.

**Fix:** Compute per-root deduped counts after the final `deduped_variants` map is known, or update ownership counts on replacement. For example:

```python
from collections import Counter

# Keep raw variant counts during generation, then after dedup replacement is complete:
owned_counts = Counter(
    (variant.root.root_order, variant.root.candidate.candidate_id)
    for variant in deduped_variants.values()
)

variants_by_root = [
    _candidate_root_variant_payload(
        root,
        variant_count=raw_variant_counts[root.root_order],
        deduped_variant_count=owned_counts[(root.root_order, root.candidate.candidate_id)],
    )
    for root in roots
]
```

Add a regression test where selected and fallback roots generate the same repaired AST but the fallback variant wins dedup ranking; assert both `accepted_candidate_root_source == "fallback"` and the fallback root summary owns the deduped variant count.

---

_Reviewed: 2026-04-17T15:49:24Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
