# ECOPM Sitecheck — Điều hành

Live dashboard: **https://ttrng3.github.io/Ecopm-Sitecheck/**

## How this repo is the source of truth

This repo is the single place the ECOPM sitecheck numbers live. GitHub Pages
**reads** from here. Nothing writes the dashboard by copying a built HTML file
around.

```
SharePoint (ECOPM / ECOPM - SITECHECK / 1. Ecopm Sitecheck)
        │   weekly .xlsx / .xlsb per operations unit
        ▼
weekly refresh routine ──writes──▶ data/index.json + data/weeks/<week>.json
                                          │
                                          ▼
                                   GitHub Pages
                                   (index.html)
```

`index.html` is a **renderer with no data baked in** (~34 KB). It fetches `data/`
at load — relative first, falling back to the published
`https://ttrng3.github.io/Ecopm-Sitecheck/data/` — so the same file works as a
Pages site and from a local copy.

## Why the data is split per week

This page used to be a single **1.23 MB** self-contained HTML file: one `CFG`
object held 1.17 MB of row detail, 97.5% of the page. Updating it meant
reproducing all of it through whichever surface was doing the update, and a
chat session cannot emit that byte-exactly. That is why the published page sat
at 15 Sep while the source kept moving.

Now a weekly update writes **two small files**: one `data/weeks/<week>.json`
(~25–45 KB) and the rewritten `data/index.json` (~30 KB).

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | Renderer only. Charts, weekly table, per-unit drill-down, row filters. No data. |
| `data/index.json` | `depts`, `wk[]` (per-week totals), `coverage`, `asof`, `generated` (display), `generatedUtc` (machine), `detail{}` (week id → slug). |
| `data/weeks/<YYYY-MM-Wnn>.json` | That week's rows: `{dept, loc, issue, action, resp, deadline, status}`. |
| `data/.last-check` | Heartbeat. Proves the job ran even when there was no new week. |
| `.github/workflows/freshness-check.yml` | Opens an issue when the job stops, or when the source goes quiet. |

Week ids are already slugs (`2026-09-W02`), so the id and the filename match —
no mapping table to keep in sync.

## Data caveats

- `wk[].mode` is `full` (totals + outstanding), `raised` (only new items known),
  or `gap` (the week's file could not be read). The page renders each
  differently; do not silently promote one to another.
- One week in `wk[]` has no `detail` entry. That is expected and the page shows
  an explicit "chưa trích được" message rather than an empty table.

## Visual standard

Since 2026-09-23 the renderer follows the **Ty Artifact Standard** — the house
Apple-HIG treatment that governs every page Ty builds, not just this one. The
skill `ty-artifact-standard` holds the full rules, and is the only place they
live. It replaced the warm-paper / Playfair treatment.

- Page ground `#F2F2F7`, cards `#FFFFFF` at 12 px radius, hairlines
  `1px solid #E5E5EA`, no drop shadows.
- System font stack only. **Do not add a webfont link back.**
- Ink in three tiers: `#1C1C1E` primary, `#3C3C43` body, `#8E8E93` muted.
- Semantic accents: blue `#007AFF` active/info, green `#34C759` done, amber
  `#FF9500` outstanding, red `#FF3B30` critical. Pill text uses a darkened ink
  of the same hue on a tint, because the raw hexes fail contrast at 12 px.
- **Every status pill carries a dot and a word**, because amber and green sit
  7.1 ΔE apart under protanopia. `.gap` is amber (a missing week is
  outstanding), `.flag` is red (critical) — they used to be the same colour.
- Chart.js: the 8-slot `C.palette` order is fixed and validated. Assign in
  order, never cycle or reorder, and keep the 2px white border between
  doughnut segments — that gap is the second cue green and amber need.
- The `@media print` block and the `beforeprint` hook that expands every
  `<details>` are load-bearing; this page gets photocopied.

A refresh writes `data/`, never the stylesheet. If a refresh finds itself
editing CSS, something has gone wrong — stop and ask.

## Artifact mirror

The chain is **repo-first**, the same shape KSNB has always used:

    schedule → cloud routine → source → GitHub → Pages → artifact mirrored after

**The repo is the source of truth and Pages is the live surface.** The artifact
is a **mirror**, published *after* the repo is correct, and never authoritative.
**Its URL is not recorded here on purpose.** The Pages link above is this page's
address; a claude.ai artifact link would be a second address for the same thing,
and a private one most readers of this repo could not open anyway. The routine
prompt holds the target URL, because that is the only place that needs it. If the two ever disagree, the repo
wins and the artifact is what gets corrected.

How a refresh mirrors it, in this order:

1. Write and verify the repo first. Do not touch the artifact until `main` has
   moved and you have read the commit back.
2. Publish the changed data paths — data/index.json and the new data/weeks/<id>.json — with the artifact's `url` set.
   Files you omit are kept, so a refresh is a small write.
3. Republish the page only when the **renderer** changed, and then publish the
   `tools/build-fragment.py` output, never `index.html` itself. The artifact
   service wraps what you give it, so a complete document nests inside another,
   the inner `<head>` is discarded, and the page renders **blank with no
   console error**. To tell that apart from the other blank cause, read the
   artifact's `index.html` back and count `<html>` tags: two means it nested,
   one means the markup is fine and it is the same-call publish problem.
4. **A failed mirror must never make you undo or retry the repo write.** Report
   it and stop; the site is already correct.

`tools/reconcile.py` diffs this repo's `data/` against the artifact's copy and
says which side is newer.

**Why the ordering is stated this bluntly.** On 2026-09-23 the TMDV artifact was
found *ahead* of its repo, carrying four fixes that had never been committed,
and the ECOPM artifact was found a whole renderer generation *behind*. Neither
was caught by the freshness guards, because both read data timestamps and the
drift was in the page. Repo-first is what keeps that from recurring.
