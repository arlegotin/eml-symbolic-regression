---
status: complete
completed: 2026-04-21
commit: 5f9429b
---

# Summary

Removed the push-blocking generated artifact from branch history by replacing the local Phase 81 artifact commit with a slim package commit.

## Removed From Reachable History

- `artifacts/paper/v1.14/linked-artifacts/campaigns/v1.14-corrected-paper-tracks/suite-result.json`

That file was a 149 MB all-in-one benchmark suite snapshot. It duplicated smaller retained evidence artifacts: aggregate JSON/Markdown, report Markdown, CSV tables, source locks, claim audit, release gate, and raw run evidence.

## Code Change

- `run_campaign()` now supports `write_suite_result=False`.
- The publication rebuild uses that mode for the full paper-track campaign, so future v1.14 publication packages do not retain the oversized suite snapshot.
- v1.14 manifest and release-gate metadata no longer reference the removed file.

## Verification

```bash
find . -path ./.git -prune -o -type f -size +100M -print
# no output

git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '$1 == "blob" && $3 > 100000000 {print}'
# no output

PYTHONPATH=src python -m pytest tests/test_campaign.py::test_campaign_writes_manifest_suite_result_and_aggregate tests/test_publication_rebuild.py -q
# 13 passed
```

