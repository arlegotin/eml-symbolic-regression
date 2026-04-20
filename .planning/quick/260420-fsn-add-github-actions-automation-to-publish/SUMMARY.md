---
quick_id: 260420-fsn
slug: add-github-actions-automation-to-publish
status: complete
completed: 2026-04-20
---

# Quick Task Summary: Publish Sanitized Main From Dev

## Outcome

Added a GitHub Actions workflow on `dev` that republishes `main` whenever `dev` is pushed.

## Implementation

- Added `.github/workflows/publish-main.yml`.
- The workflow checks out `dev`, records the source commit, fetches the current remote `main`, creates a new orphan snapshot, removes private/generated paths, commits the sanitized tree, and force-pushes `main` with `--force-with-lease`.
- The sanitized public snapshot excludes `AGENTS.md`, `.github/`, `.planning/`, `artifacts/`, `docs/`, `sources/`, and `tests/`.

## Verification

- Confirmed the workflow is the only non-planning source change.
- Confirmed the workflow trigger is limited to pushes to `dev`.
- Confirmed the workflow grants `contents: write`, which is required for `GITHUB_TOKEN` to push `main`.
