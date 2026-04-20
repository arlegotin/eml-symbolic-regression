---
phase: 69
status: planned
created: 2026-04-20
type: execute
wave: 1
files_modified:
  - src/eml_symbolic_regression/cli.py
  - src/eml_symbolic_regression/publication.py
  - tests/test_publication_rebuild.py
  - docs/IMPLEMENTATION.md
  - requirements-lock.txt
  - Dockerfile
  - scripts/publication-rebuild.sh
requirements_addressed:
  - REPRO-01
  - REPRO-02
  - REPRO-03
  - REPRO-04
  - REPRO-05
must_haves:
  truths:
    - "A single documented command rebuilds a v1.13 publication package from a fresh checkout path."
    - "Committed lockfile and container entrypoint reference the same publication rebuild command."
    - "Publication rebuild does not require raw-hybrid-paper --require-existing as the publication entrypoint."
    - "Generated publication manifests include git revision, command, environment identity, input hashes, output hashes, and generated_at timestamp."
    - "Publication validation rejects placeholder metadata outside explicit deterministic fixture paths."
---

# Phase 69: Clean-Room Reproduction Path and Provenance - Plan

## Objective

Add a v1.13 clean-room publication rebuild path with real provenance, locked-environment entrypoints, tests, and documentation. Preserve archived v1.11/v1.12 artifacts and avoid changing legacy paper-package behavior except where the new publication command reuses existing helpers.

## Tasks

### Task 1: Add Publication Rebuild Module

<read_first>
- `src/eml_symbolic_regression/paper_package.py`
- `src/eml_symbolic_regression/paper_v112.py`
- `src/eml_symbolic_regression/campaign.py`
- `.planning/phases/69-clean-room-reproduction-path-and-provenance/69-CONTEXT.md`
- `.planning/phases/69-clean-room-reproduction-path-and-provenance/69-RESEARCH.md`
</read_first>

<files>src/eml_symbolic_regression/publication.py</files>

<action>
Create a new publication rebuild module with a `PublicationRebuildPaths` dataclass, a `write_publication_rebuild(...)` function, and a `validate_publication_package(...)` function. The writer must create a v1.13 output directory containing at least `manifest.json`, `source-locks.json`, `reproduction.md`, `validation.json`, and `validation.md`. The manifest must include `schema: eml.v113_publication_rebuild.v1`, `generated_at`, `mode`, `command`, `git` metadata, `environment` metadata, `inputs`, `outputs`, and `validation`. The validation function must reject `1970-01-01T00:00:00+00:00` and `"snapshot"` unless the path is explicitly listed as a deterministic fixture.
</action>

<acceptance_criteria>
- `src/eml_symbolic_regression/publication.py` contains `class PublicationRebuildPaths`.
- `src/eml_symbolic_regression/publication.py` contains `def write_publication_rebuild(`.
- `src/eml_symbolic_regression/publication.py` contains `def validate_publication_package(`.
- Generated `manifest.json` contains `eml.v113_publication_rebuild.v1`.
- Generated `validation.json` contains a top-level `status` field.
</acceptance_criteria>

### Task 2: Add CLI Command and Script Entrypoint

<read_first>
- `src/eml_symbolic_regression/cli.py`
- `pyproject.toml`
</read_first>

<files>src/eml_symbolic_regression/cli.py, scripts/publication-rebuild.sh</files>

<action>
Wire a new CLI command named `publication-rebuild` that accepts `--output-dir`, `--smoke`, `--overwrite`, and `--allow-dirty`. The command must call `write_publication_rebuild` with a normalized reproduction command string. Add `scripts/publication-rebuild.sh` as a small shell entrypoint that runs `python -m eml_symbolic_regression.cli publication-rebuild --output-dir artifacts/paper/v1.13 --smoke --overwrite`.
</action>

<acceptance_criteria>
- `src/eml_symbolic_regression/cli.py` contains `publication-rebuild`.
- `scripts/publication-rebuild.sh` contains `python -m eml_symbolic_regression.cli publication-rebuild`.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir /tmp/eml-v113-smoke --smoke --overwrite` exits 0.
</acceptance_criteria>

### Task 3: Add Lockfile and Container Support

<read_first>
- `pyproject.toml`
- `.planning/REQUIREMENTS.md`
</read_first>

<files>requirements-lock.txt, Dockerfile</files>

<action>
Add a committed `requirements-lock.txt` with the project runtime and dev dependencies currently required by the repo. Add a `Dockerfile` that installs from the lockfile, copies the repo, sets `PYTHONPATH=src`, and runs the same `publication-rebuild` smoke command as its default command.
</action>

<acceptance_criteria>
- `requirements-lock.txt` contains `torch`, `numpy`, `sympy`, `mpmath`, and `pytest`.
- `Dockerfile` contains `COPY requirements-lock.txt`.
- `Dockerfile` contains `publication-rebuild`.
- The publication manifest records the lockfile path and SHA-256 when `requirements-lock.txt` exists.
</acceptance_criteria>

### Task 4: Add Tests for Rebuild and Provenance Validation

<read_first>
- `tests/test_paper_package.py`
- `tests/test_paper_v112.py`
- `src/eml_symbolic_regression/publication.py`
</read_first>

<files>tests/test_publication_rebuild.py</files>

<action>
Add tests that generate a smoke publication package in `tmp_path`, assert manifest fields and hash-bearing input/output rows, assert CLI registration, assert placeholder metadata fails validation in a normal publication artifact, and assert deterministic fixture paths can be explicitly allowed.
</action>

<acceptance_criteria>
- `tests/test_publication_rebuild.py` contains a smoke package generation test.
- `tests/test_publication_rebuild.py` contains a CLI registration test.
- `tests/test_publication_rebuild.py` contains a placeholder rejection test.
- `PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py -q` exits 0.
</acceptance_criteria>

### Task 5: Document the Clean-Room Command

<read_first>
- `README.md`
- `docs/IMPLEMENTATION.md`
</read_first>

<files>docs/IMPLEMENTATION.md</files>

<action>
Document the v1.13 publication rebuild command, smoke/full distinction, lock/container entrypoints, provenance fields, and the rule that placeholder metadata is forbidden outside deterministic fixtures. Keep the documentation concise and do not claim that Phase 69 runs the final full publication evidence campaign.
</action>

<acceptance_criteria>
- `docs/IMPLEMENTATION.md` contains `publication-rebuild`.
- `docs/IMPLEMENTATION.md` contains `requirements-lock.txt`.
- `docs/IMPLEMENTATION.md` contains `Dockerfile`.
- `docs/IMPLEMENTATION.md` says the final full evidence campaign belongs to the publication rebuild/release gate, not Phase 69 alone.
</acceptance_criteria>

## Verification

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_publication_rebuild.py tests/test_paper_package.py tests/test_paper_v112.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli publication-rebuild --output-dir /tmp/eml-v113-smoke --smoke --overwrite
```

Then inspect `/tmp/eml-v113-smoke/manifest.json` for `schema`, `git`, `environment`, `inputs`, `outputs`, and `validation`.

## Risks

- Full publication evidence generation is intentionally deferred to Phase 76; Phase 69 must not overclaim that the smoke path is the final evidence rebuild.
- Manifest self-hashing can become circular. Avoid listing `manifest.json` as an output with a hash inside itself, or write output locks outside the manifest if needed.
- The local tree may be dirty during development. Record dirty state, and let final release gates decide whether dirty state is blocking.
