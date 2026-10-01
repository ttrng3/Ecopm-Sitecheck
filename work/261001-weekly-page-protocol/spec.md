# Spec

Status: approved by Ty 01/10 (same words as the intent).

- `verification/weekly-page.md`: the eight-section protocol (promise, clean state, steps, invariants, adversary, sanctioned substitutes, evidence, traps) plus Not covered.
- `tools/verify_live.py` (stdlib only, not served): 13 verdicts as JSON, exit 0 only when all pass. Words that must not be served come in on `--forbid` and are never written into the repo.
- Step 2 is page JavaScript run in Chrome; step 4 (preview) uses the Artifact tool, with the preview link read from the routine's prompt and never written here.
- No change to the page, the data, `.pages-allow` or the runbook.
- Promise: after #15 is live, step 1 prints `"pass": true` and step 2 prints six trues. Each of six deliberate breakages of a copy (a total off by one, an unmapped unit, a detail claim without a file, an undeclared missing detail, an old heartbeat, a forbidden word) fails its own verdict, and an untouched copy passes.
