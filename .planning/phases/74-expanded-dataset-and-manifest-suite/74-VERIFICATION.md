---
status: passed
verified_at: "2026-04-20"
implementation_commit: 3da912c
---

# Phase 74: Expanded Dataset and Manifest Suite - Verification

## Result

Passed.

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_expanded_datasets.py -q
```

Result: 12 passed in 2.47s.

```bash
PYTHONPATH=src python -m pytest tests/test_proof_dataset_manifest.py tests/test_expanded_datasets.py -q
```

Result: 22 passed in 2.51s.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli list-datasets
```

Result: listed noisy Beer-Lambert, Michaelis-Menten identifiability, multivariable Arrhenius, unit-aware Ohm law, and real Hubble datasets.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli dataset-manifest real_hubble_1929 --output /tmp/eml-phase74-hubble-manifest.json
```

Result: wrote the real Hubble expanded dataset manifest.

```bash
git diff --check
```

Result: passed.

## Acceptance Checks

- Registry covers noisy synthetic, parameter-identifiability, multivariable, unit-aware, and real dataset categories.
- Real data fixture exists at `data/real/hubble_1929_velocity_distance.csv` and loads train, held-out diagnostic, and final-confirmation splits.
- Expanded manifests include source/generator, units, noise policy, split policy, domain constraints, classification, split roles, and hashes.
- Multivariable synthetic splits verify against their clean symbolic candidate.
- CLI can list expanded datasets and write a manifest.
