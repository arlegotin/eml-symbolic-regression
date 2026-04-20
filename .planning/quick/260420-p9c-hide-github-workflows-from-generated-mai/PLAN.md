# Quick Task 260420-p9c: Hide GitHub Workflows from Main

## Request

Keep GitHub workflows functional from `dev`, but hide `.github/workflows` from the generated public `main` branch. Also change the generated `main` commit message from `Update public snapshot` to `Update`.

## Plan

- Update `.github/workflows/publish-main.yml` so the generated snapshot removes the whole `.github` tree.
- Use a generic visible workflow label.
- Keep workflow files on `dev`; only the generated `main` snapshot is affected.
- Change the generated public commit message to `Update`.
- Update the CI contract and simulated public snapshot check to match the hidden `.github` policy.
- Keep existing `tests` inclusion and curated artifact pruning unchanged.
- Push `dev` and verify the regenerated `main` branch.

## Acceptance

- `dev` contains `.github/workflows`.
- `main` contains no `.github` paths.
- `main` remains a one-commit generated branch.
- The latest `main` commit subject is `Update`.
- `tests` remain present on `main`.
- CI branch/snapshot contract accepts the new policy.
