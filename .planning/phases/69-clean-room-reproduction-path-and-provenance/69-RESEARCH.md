# Phase 69 Research: Clean-Room Reproduction Path and Provenance

## RESEARCH COMPLETE

## Phase Summary

Phase 69 should add a publication-oriented rebuild path that can be invoked from a fresh checkout and produces a v1.13 package with real provenance. The existing paper package writers are useful but mostly assemble from already-generated artifacts. The new work should make that dependency explicit, add a smoke rebuild that generates a minimal source package in one command, and provide manifest validation strong enough for later CI and final publication audit.

## Current Implementation Surface

### Existing CLI

- `src/eml_symbolic_regression/cli.py` owns all public commands through `argparse`.
- Paper-facing commands already include `paper-package`, `paper-assets`, `paper-draft`, `paper-refresh`, `paper-figures`, `paper-probes`, `paper-supplement`, and `paper-training-detail`.
- `raw-hybrid-paper` currently defaults to `--require-existing`; this is acceptable for legacy package synthesis, but not for the new publication rebuild path.

### Existing Artifact Writers

- `src/eml_symbolic_regression/paper_package.py` writes v1.11 `manifest.json`, `source-locks.json`, `claim-audit.json`, `claim-audit.md`, `reproduction.md`, and `paper-readiness.md`.
- `src/eml_symbolic_regression/paper_v112.py` writes v1.12 draft, supplement, bounded probes, paper-facing assets, evidence refreshes, and training-detail artifacts.
- `src/eml_symbolic_regression/campaign.py` and `src/eml_symbolic_regression/benchmark.py` already produce campaign manifests, aggregate reports, tables, figures, and run payloads.
- Artifact helpers generally use dataclasses for path bundles, versioned output roots, JSON `schema` fields, explicit overwrite flags, and deterministic JSON formatting.

### Existing Provenance Behavior

- Benchmark aggregate output records `generated_at`, Python/platform, and code version.
- Stable snapshot mode in `benchmark.py` intentionally replaces `generated_at` with `1970-01-01T00:00:00+00:00` and code version with `"snapshot"`.
- Existing paper package manifests include reproduction commands and source locks, but do not consistently record output hashes, environment lock/container identity, or a generated command ledger for every artifact.
- Tests currently assert paper package structure and claim audit behavior, but not publication-grade provenance or placeholder rejection.

## Recommended Technical Approach

### Add a Focused Publication Module

Create a new module such as `src/eml_symbolic_regression/publication.py` or `publication_rebuild.py` with:

- A `PublicationRebuildPaths` dataclass.
- A `write_publication_rebuild(...)` function that coordinates a v1.13 output root.
- A manifest validation function that can be tested independently.
- Small helpers for git revision, command normalization, environment identity, file hashing, and placeholder detection.

Keep this separate from `paper_package.py` so v1.11/v1.12 archive behavior remains stable.

### Add CLI Command

Add a command such as:

```bash
eml-sr publication-rebuild --output-dir artifacts/paper/v1.13 --smoke --overwrite
```

Required behavior:

- `--smoke` generates a minimal but complete v1.13 package from source inputs quickly enough for tests and later CI.
- Full mode should be the same command without `--smoke`; it can initially orchestrate current paper-facing generators and source-lock existing anchors where full evidence generation remains a later Phase 76 concern.
- `--overwrite` should be required to refresh an existing output directory, matching existing package-writer conventions.

### Provenance Schema

The v1.13 publication manifest should record:

- `schema`, `generated_at`, `output_dir`, `mode`, and `command`.
- `git.revision`, `git.branch`, and dirty-state indicator.
- `environment.python`, `environment.platform`, `environment.lockfile`, and `environment.container`.
- `inputs[]` with `role`, `path`, and `sha256`.
- `outputs[]` with `role`, `path`, and `sha256`.
- `validation.status` plus checks for placeholder metadata, missing hashes, and absent required outputs.

Output hashing should be computed after all files are written so the manifest references actual artifact bytes.

### Locked Environment Support

Minimum viable support:

- Commit a lock or constraints file that reflects the Python dependency surface used by the package.
- Commit a container file and entrypoint that runs the same `publication-rebuild` command.
- Record the lockfile hash in the publication manifest.

Avoid making Docker required for normal local tests. Tests can verify that container/lock entrypoints exist and that manifest environment identity includes lockfile information.

### Placeholder Validation

Implement a recursive scanner over generated JSON/Markdown text for:

- `1970-01-01T00:00:00+00:00`
- `"snapshot"`

The scanner should allow explicitly labeled deterministic fixture paths and reject these tokens elsewhere in publication outputs. Tests should cover both a failing publication artifact and an allowed fixture path.

## Planning Risks

- Full evidence generation may be too expensive for Phase 69. Keep the smoke rebuild complete and fast, and let Phase 76 own the full publication campaign.
- Existing v1.11/v1.12 artifacts should not be overwritten. New v1.13 outputs should either regenerate small smoke artifacts or source-lock old anchors as inputs.
- Hashing the manifest itself can become circular. Avoid including the manifest hash inside itself, or write a separate lock/index after the manifest is finalized.
- Git dirty-state handling must not fail developer workflows unnecessarily. Record dirty state, but only fail if the publication validation contract explicitly requires a clean tree.

## Suggested Plan Boundaries

1. Add publication rebuild/provenance module and CLI command.
2. Add lock/container entrypoint files and document the command.
3. Add validation tests for provenance fields, output hashes, and placeholder rejection.
4. Keep legacy package commands behavior-compatible; only the new publication path changes the public rebuild contract.

## Files Likely To Change

- `src/eml_symbolic_regression/cli.py`
- `src/eml_symbolic_regression/publication.py` or `src/eml_symbolic_regression/publication_rebuild.py`
- `tests/test_publication_rebuild.py`
- `README.md` or `docs/IMPLEMENTATION.md`
- `requirements-lock.txt` or equivalent committed lock/constraints file
- `Dockerfile` and an optional small script under `scripts/`
