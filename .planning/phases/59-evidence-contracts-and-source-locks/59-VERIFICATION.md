# Phase 59 Verification

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper.py -q
PYTHONPATH=src python -m pytest tests/test_raw_hybrid_paper_regression.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli raw-hybrid-paper --preset v1.11-paper-evidence-package --output-dir artifacts/paper/v1.11/raw-hybrid --require-existing --overwrite
```

## Results

- `tests/test_raw_hybrid_paper.py`: 15 passed.
- `tests/test_raw_hybrid_paper_regression.py`: 5 passed.
- v1.11 raw-hybrid package generated successfully.

## Checked Claims

- v1.9 package compatibility remained intact.
- v1.11 source locks include `v1.10-logistic-run` and `v1.10-planck-run`.
- v1.11 scientific-law table uses current logistic depth 15 and Planck depth 14 rows.
- Logistic and Planck remain unsupported diagnostics.
- Claim ledger marks recovery rates as verifier-owned and loss-only recovery as forbidden.
