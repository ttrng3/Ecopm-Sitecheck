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

## One surface, on purpose

    schedule → cloud routine → source → GitHub → Pages

**GitHub Pages is the only published surface.** Ty ruled on 2026-09-23 that he
wants control over what exists of his work, so there is no claude.ai artifact
copy of this dashboard: the Pages URL above is the address, full stop.

A mirror artifact existed for a few hours that day and was deleted. Do not
recreate one, and do not add an artifact URL to this repo. `tools/build-fragment.py`
is kept only because it is the one thing that can derive a standalone fragment
of this page if it is ever needed; nothing in the refresh calls it.
