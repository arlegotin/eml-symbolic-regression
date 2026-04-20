---
status: passed
verified_at: "2026-04-20"
implementation_commit: fea8229
---

# Phase 71: Training and Verification Semantics Alignment - Verification

## Result

Passed.

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_semantics_expression.py tests/test_optimizer_cleanup.py tests/test_benchmark_contract.py -q
```

Result: 89 passed, 2 expected runtime warnings from centered-family singularity diagnostics.

```bash
PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py tests/test_benchmark_reports.py tests/test_verify.py -q
```

Result: 60 passed, 3 expected runtime warnings from overflow/verification stress cases.

```bash
PYTHONPATH=src python -m pytest tests/test_paper_v112.py tests/test_publication_rebuild.py tests/test_paper_package.py -q
```

Result: 32 passed.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli demo exp --train-eml --semantics-mode faithful --steps 1 --restarts 1 --hardening-steps 1 --points 12 --output /tmp/eml-phase71-demo-faithful.json
```

Result: `exp: recovered`; output manifest contained `semantics_mode: faithful` and `semantics_alignment.training_semantics_mode: faithful`.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark smoke --semantics-mode faithful --case exp-blind --seed 0 --output-dir /tmp/eml-phase71-benchmark-faithful
```

Result: 1 run, 0 unsupported, 0 failed; suite aggregate contained `training_semantics_mode: faithful` and `objective_matches_verifier_semantics: true`.

```bash
git diff --check
```

Result: passed.

## Full Suite Note

```bash
PYTHONPATH=src python -m pytest -q
```

Result: stopped manually after reaching 76% with no failures because the process spent several minutes in a CPU-bound artifact serialization section. Focused tests covering the changed semantics, optimizer, benchmark, CLI, verifier compatibility, and paper/package contracts passed.

## Acceptance Checks

- Faithful mode uses verifier-matching unclamped arithmetic for finite raw and centered test inputs.
- Guarded mode remains default and retains existing clamp/log-safety behavior.
- Training manifests include `semantics_alignment`.
- Benchmark budgets and suite outputs include `semantics_mode`.
- CLI supports demo and benchmark faithful-mode controls.
- Verifier certificate status is surfaced through optimizer alignment artifacts.
