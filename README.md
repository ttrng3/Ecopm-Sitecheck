# ECOPM Sitecheck — Điều hành

Live dashboard: **https://ttrng3.github.io/Ecopm-Sitecheck/**

## How this repo is the source of truth

This repo is the single place the ECOPM sitecheck numbers live. GitHub Pages and
the claude.ai artifact both **read** from here. Nothing writes the dashboard by
copying a built HTML file around.

```
SharePoint (ECOPM / ECOPM - SITECHECK / 1. Ecopm Sitecheck)
        │   weekly .xlsx / .xlsb per operations unit
        ▼
weekly refresh routine ──writes──▶ data/index.json + data/weeks/<week>.json
                                          │
                        ┌─────────────────┴─────────────────┐
                        ▼                                   ▼
                 GitHub Pages                        claude.ai artifact
                 (index.html)                        (its own copy of data/)
```

`index.html` is a **renderer with no data baked in** (~34 KB). It fetches `data/`
at load — relative first, falling back to the published
`https://ttrng3.github.io/Ecopm-Sitecheck/data/` — so the same file works as a
Pages site, as an artifact, and from a local copy.

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
