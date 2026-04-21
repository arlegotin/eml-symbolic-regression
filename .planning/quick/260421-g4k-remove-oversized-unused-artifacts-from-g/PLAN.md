---
quick_id: 260421-g4k
status: complete
created: 2026-04-21
---

# Quick Task: Remove Oversized Unused Artifacts From Git History

## Goal

Remove the GitHub push blocker caused by a generated artifact over 100 MB while preserving the corrected v1.14 evidence surface.

## Plan

1. Identify current files and reachable git blobs over GitHub's 100 MB limit.
2. Determine whether the oversized file is source evidence or redundant generated data.
3. Rewrite the local branch tail so the oversized blob is not reachable from `dev`.
4. Patch generation code and generated package metadata so the slim package stays consistent.
5. Verify no current file or reachable git blob exceeds 100 MB.

