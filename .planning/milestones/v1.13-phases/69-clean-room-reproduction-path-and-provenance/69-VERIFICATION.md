---
phase: 69
status: passed
verified_at: 2026-04-20
score: 5/5
---

# Phase 69 Verification: Clean-Room Reproduction Path and Provenance

## Verdict

Status: `passed`

Phase goal achieved: a fresh-checkout-oriented v1.13 publication smoke rebuild path now exists, records lock/container provenance, hashes declared inputs and generated outputs, and rejects placeholder metadata outside explicit deterministic fixtures.

## Must-Have Checks

| Must-have | Result | Evidence |
|-----------|--------|----------|
| Single documented command rebuilds a v1.13 publication package from a fresh checkout path. | passed | `publication-rebuild` CLI, `scripts/publication-rebuild.sh`, and `docs/IMPLEMENTATION.md` document/run the smoke rebuild. |
| Committed lockfile and container entrypoint reference the same publication rebuild command. | passed | `requirements-lock.txt` and `Dockerfile` are committed; Docker default command runs `publication-rebuild --smoke --overwrite --allow-dirty`. |
| Publication rebuild does not require `raw-hybrid-paper --require-existing` as the publication entrypoint. | passed | New `publication-rebuild` command calls `write_publication_rebuild`; legacy raw-hybrid command remains unchanged. |
| Generated publication manifests include git revision, command, environment identity, input hashes, output hashes, and `generated_at`. | passed | `/tmp/eml-v113-smoke-clean/manifest.json` includes `git`, `command`, `environment`, `inputs`, `outputs`, and `generated_at`. |
| Publication validation rejects placeholder metadata outside explicit deterministic fixture paths. | passed | `tests/test_publication_rebuild.py` covers rejection of `1970-01-01T00:00:00+00:00` and `"snapshot"` plus explicit fixture allow-listing. |

## Automated Checks

```bash
PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py -q
```

Result: passed, 5 tests.

```bash
PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py tests/test_paper_package.py tests/test_paper_v112.py -q
```

Result: passed, 32 tests.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir /tmp/eml-v113-smoke-clean --smoke --overwrite
```

Result: passed; validation status was `passed`, and the generated manifest recorded `git.dirty: false`.

## Requirement Coverage

- REPRO-01: passed for the smoke publication package command and documentation; full publication campaign remains Phase 76.
- REPRO-02: passed for committed lockfile/container entrypoint support and manifest recording of their hashes.
- REPRO-03: passed for the new publication entrypoint; it does not rely on legacy `raw-hybrid-paper --require-existing`.
- REPRO-04: passed for git, command, environment, input-hash, output-hash, and timestamp provenance fields.
- REPRO-05: passed for validator and regression tests rejecting placeholder metadata outside explicit fixtures.

## Residual Risk

The smoke rebuild proves package shape and provenance mechanics. It intentionally does not run the full v1.13 evidence campaign; Phase 76 must use this infrastructure for the final publication rebuild and claim audit.
