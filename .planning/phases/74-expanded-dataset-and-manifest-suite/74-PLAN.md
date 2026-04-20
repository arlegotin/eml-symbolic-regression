# Phase 74: Expanded Dataset and Manifest Suite - Plan

**Planned:** 2026-04-20
**Status:** Ready for execution

## Objective

Add an expanded dataset registry and manifest contract covering noisy, parameter-stress, multivariable, unit-aware, and real-data evidence inputs.

## Tasks

### 1. Dataset Registry

- Add `ExpandedDatasetSpec` and registry functions to `datasets.py`.
- Generate verifier-compatible `DataSplit` objects.
- Include per-split roles and domains.

### 2. Dataset Families

- Add noisy Beer-Lambert synthetic sweep.
- Add Michaelis-Menten parameter-identifiability stress data.
- Add multivariable Arrhenius surface data.
- Add unit-aware Ohm law data.
- Add committed Hubble 1929 real-data CSV fixture with deterministic splits.

### 3. Manifest Contract

- Add expanded dataset manifests with schema, units, noise policy, split policy, domain constraints, source/generator, classification, split hashes, and compatibility tags.
- Keep proof dataset manifests backward compatible.

### 4. CLI Surface

- Add `list-datasets`.
- Add `dataset-manifest`.

### 5. Tests and Docs

- Add tests for registry coverage, manifest fields, real-data loading, verifier compatibility, and CLI behavior.
- Update implementation docs.

## Acceptance Checks

- Expanded dataset registry covers all required categories.
- Real data fixture path exists and has independent splits.
- Manifests satisfy DATA-02 fields.
- Synthetic expanded datasets produce verifier-compatible splits.
- CLI can list datasets and write a manifest.
