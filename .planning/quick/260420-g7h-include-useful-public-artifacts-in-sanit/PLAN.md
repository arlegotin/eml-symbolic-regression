# Quick Task 260420-g7h: Include Useful Public Artifacts

## Request

Include `artifacts` in the generated public `main` snapshot, but strip noisy or redundant material so the branch keeps useful evidence without carrying raw experiment payloads.

## Plan

- Update `.github/workflows/publish-main.yml` so the public branch no longer removes `artifacts` wholesale.
- Add a curated artifact pruning step for the public snapshot only.
- Keep reports, paper draft assets, figures, tables, manifests, audits, and compact evidence summaries.
- Remove raw run directories, raw suite-result JSON payloads, aggregate JSON payloads, duplicated supplement source bundles, training step trace dumps, and `.DS_Store` files.
- Verify that the workflow syntax is valid enough to run and that `main` still omits private/planning/source/test folders.

## Acceptance

- `dev` keeps the full artifact history and files.
- `main` includes an `artifacts` tree after the publish workflow runs.
- `main` does not include `AGENTS.md`, `.github`, `.planning`, `docs`, `sources`, or `tests`.
- `main` does not include the configured noisy artifact classes.
