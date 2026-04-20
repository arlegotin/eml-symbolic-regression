# Phase 74: Expanded Dataset and Manifest Suite - Research

**Researched:** 2026-04-20
**Status:** Complete

## Existing Dataset Contract

`DemoSpec.make_splits()` already returns verifier-compatible `DataSplit` objects. `DataSplit` supports multi-variable input dictionaries, explicit roles, and per-split domain metadata. The current proof manifest records split hashes and formula provenance but does not yet include units, noise policy, source classification, real-data source paths, or broader dataset-family metadata.

## Requirements Mapping

`DATA-01` requires coverage across five dataset categories:

- noisy synthetic sweeps,
- parameter-identifiability stress,
- multivariable cases,
- unit-aware formulations,
- real datasets with independent splits.

`DATA-02` requires manifests to record generator/source, units, noise policy, split policy, domain constraints, and synthetic/semi-synthetic/real classification.

## Real Dataset Source

Use a small Hubble 1929 velocity-distance fixture. Source metadata:

- Edwin Hubble, "A relation between distance and radial velocity among extra-galactic nebulae", PNAS 15(3), 168-173, DOI `10.1073/pnas.15.3.168`.
- Duke STA 113 page provides the 24-row tabular data and states free use: `https://www2.stat.duke.edu/courses/Fall03/sta113/Hubble.html`.

This real fixture is noisy observational data and should not be treated as exact formula recovery evidence.

## Integration Strategy

Keep expanded datasets separate from legacy demo specs, but expose common functions:

- list dataset IDs,
- load splits,
- write manifest,
- include compatibility tags for verifier, benchmark-track, and baseline harness contracts.

This keeps Phase 74 small while giving Phase 75 and Phase 76 a stable input surface.

## Test Strategy

- Assert all required dataset categories are present.
- Assert manifests include classification, units, noise policy, split policy, domain constraints, split roles, hashes, and compatibility tags.
- Assert the real Hubble fixture loads from a committed path and has independent train/heldout/final-confirmation splits.
- Assert a multivariable synthetic split verifies exactly against its candidate.
- Assert CLI commands list datasets and write a manifest.

