---
quick_id: 260420-fsn
slug: add-github-actions-automation-to-publish
status: complete
created: 2026-04-20
---

# Quick Task Plan: Publish Sanitized Main From Dev

## Goal

Add automation so every push to `dev` republishes `main` as a sanitized orphan snapshot of `dev`.

## Tasks

1. Add a GitHub Actions workflow that runs on pushes to `dev`.
2. Build a new orphan `main` snapshot from the pushed `dev` commit.
3. Remove private/generated paths from the public snapshot before committing.
4. Force-push `main` with a lease against the current remote `main` tip.
5. Record quick-task completion in `.planning`.

## Sanitized Paths

- `AGENTS.md`
- `.github/`
- `.planning/`
- `artifacts/`
- `docs/`
- `sources/`
- `tests/`

## Verification

- Workflow YAML is syntactically inspectable.
- Only the workflow and quick-task tracking files are changed on `dev`.
- The workflow uses `contents: write` and `--force-with-lease` for publishing.
