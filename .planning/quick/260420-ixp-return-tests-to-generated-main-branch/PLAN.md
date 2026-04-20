# Quick Task 260420-ixp: Return Tests to Main

## Request

Return the `tests` folder to the generated public `main` branch.

## Plan

- Update `.github/workflows/publish-main.yml` so the publication job no longer removes `tests`.
- Keep existing exclusions for `AGENTS.md`, `.github`, `.planning`, `docs`, and `sources`.
- Keep the existing curated artifact pruning policy unchanged.
- Push `dev` so GitHub Actions regenerates `main`.
- Verify `origin/main` contains `tests` and still omits the intended private/planning/source paths.

## Acceptance

- `main` contains tracked files under `tests`.
- `main` remains a one-commit public snapshot.
- `main` still excludes `AGENTS.md`, `.github`, `.planning`, `docs`, and `sources`.
