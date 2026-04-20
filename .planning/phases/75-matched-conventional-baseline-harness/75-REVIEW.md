---
status: clean
reviewed_at: "2026-04-20"
implementation_commit: b7f32ce
---

# Phase 75: Matched Conventional Baseline Harness - Review

## Findings

No blocking findings.

## Review Notes

- The harness is separate from `benchmark.py`, so baseline comparison rows cannot silently enter EML recovery denominators.
- Every row carries dataset manifest hash, seed, constants policy, start condition, budget, dependency status, and denominator policy.
- The polynomial least-squares adapter gives a real conventional symbolic run path using existing NumPy/SymPy dependencies.
- External SR adapters are dependency-checked through import probes and source-locked in `dependency-locks.json`.
- Unsupported conditions are explicit:
  - EML reference rows are not blind search evidence,
  - polynomial rows require literal fitted coefficients,
  - polynomial rows have no warm-start mode,
  - real observational data has no clean symbolic EML reference.

## Residual Risk

- External SR package execution is not implemented because the local environment does not have those packages installed and Phase 75 deliberately avoids dependency installation.
- The fixed polynomial baseline is useful as a conventional symbolic contract smoke test; it is not a comprehensive symbolic-regression comparator.
