---
phase: 69
slug: clean-room-reproduction-path-and-provenance
status: complete
created: 2026-04-20
completed: 2026-04-20
workflow: gsd-execute-phase
plan: .planning/phases/69-clean-room-reproduction-path-and-provenance/69-PLAN.md
key_files:
  created:
    - src/eml_symbolic_regression/publication.py
    - tests/test_publication_rebuild.py
    - requirements-lock.txt
    - Dockerfile
    - scripts/publication-rebuild.sh
  modified:
    - src/eml_symbolic_regression/cli.py
    - docs/IMPLEMENTATION.md
summary_artifact: .planning/phases/69-clean-room-reproduction-path-and-provenance/69-SUMMARY.md
---

# Phase 69 Summary: Clean-Room Reproduction Path and Provenance

## Status

Complete. Phase 69 adds a v1.13 publication rebuild smoke path with explicit provenance and validation.

## Delivered

- Added `src/eml_symbolic_regression/publication.py` with `PublicationRebuildPaths`, `write_publication_rebuild`, and `validate_publication_package`.
- Added `publication-rebuild` CLI support with `--output-dir`, `--smoke`, `--overwrite`, and `--allow-dirty`.
- Added `scripts/publication-rebuild.sh` as the shell entrypoint for the same command.
- Added `requirements-lock.txt` and `Dockerfile` so the publication manifest can record lock/container identity.
- Added tests for smoke package generation, CLI registration, hash-bearing provenance rows, placeholder rejection, and explicit deterministic-fixture allow-listing.
- Documented the v1.13 publication rebuild contract in `docs/IMPLEMENTATION.md`.

## Verification Completed

```bash
PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py -q
```

Result: passed, 4 tests.

```bash
PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py tests/test_paper_package.py tests/test_paper_v112.py -q
```

Result: passed, 31 tests.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir /tmp/eml-v113-smoke --smoke --overwrite --allow-dirty
```

Result: passed; `/tmp/eml-v113-smoke/manifest.json` and `/tmp/eml-v113-smoke/validation.json` were written, and validation status was `passed`.

## Commit

Implementation commit: `21562e5`.

## Notes

The smoke rebuild validates package shape and provenance mechanics. It does not claim to run the final full v1.13 evidence campaign; Phase 76 owns the final evidence rebuild, claim audit, and public release gate.
