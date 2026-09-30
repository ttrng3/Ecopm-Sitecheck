# CLAUDE.md — Ecopm-Sitecheck

EcoPM's weekly site-check dashboard (the operations units in `data/index.json` `depts`), entity **EcoPM**. Live: https://ttrng3.github.io/Ecopm-Sitecheck/

**If you are the scheduled routine:** follow the files your prompt names, `docs/weekly-refresh.md` and `README.md`. They outrank this file. This file adds no step to a run.

## Commands
- Check every `detail` entry has its week file (a quick check, not full validation): `python3 -c "import json,os;d=json.load(open('data/index.json'));m=[k for k,v in d['detail'].items() if k!=v or not os.path.exists('data/weeks/'+v+'.json')];assert not m,m"`
- Build the Cowork preview page: `python3 tools/build-fragment.py` (writes `build/artifact.html`). When the routine refreshes the preview is set by its runbook, not here. Never send `index.html` itself to the preview; Pages does serve it.
- Compare two `data/` trees: `python3 tools/reconcile.py <dir-a> <dir-b>` (exit 0 = same)
- Freshness check, as the daily Action runs it: `python3 .github/scripts/freshness.py`

## Layout
- `index.html` is a renderer holding no data. A refresh never touches it or either of its `<style>` blocks.
- Data: `data/index.json` (`depts`, `wk[]` with `mode` full/raised/gap, `coverage`, `detail{}`, `detailRows`, `recon`, `verdict`, `asof`, `generated`, `generatedUtc`; the README's key table predates the last three), `data/weeks/<YYYY-MM-Wnn>.json` (row detail; the id is the file name), `data/.last-check` (heartbeat, not published).
- `tools/parse_sitecheck.py` pulls row detail from a copy of the workbook (runbook step 4); it needs the file itself, which the connector cannot supply.
- `.pages-allow` lists what Pages publishes; `.github/workflows/pages.yml` deploys only that. A new kind of file under `data/` needs Ty's say-so and its own `.pages-allow` line in its own PR first.
- `README.md` explains the data model and the visual standard; `REVIEW.md` holds the reviewer's rules.

## Rules
- Changes reach `main` through a PR and Ty's ship. The only direct writes are the ones a routine's prompt and runbook allow.
- The runbook and README win over this file and any memory note.
- Never write a Cowork preview URL or artifact id, a person's details or a secret into this public repo.
- Entity separation: this is EcoPM. Never take figures from another company's site-check tree, and never mix the two series.
- `wk[].mode` is never promoted: a `gap` or `raised` week does not become `full` without the source to back it.

## Known mistakes
- Two SharePoint trees hold identically named workbooks with different numbers. Only `ECOPM/ECOPM - SITECHECK/1. Ecopm Sitecheck/` is this project; the other tree belongs to another company and silently corrupts the series (2026-09-22).
- The connector returns only the `TH` summary sheet of these workbooks, never the detail sheets (runbook step 4). The 2026-09-22 run appended W02/W03 with no detail and no note, so the page did not say the detail was missing (2026-09-25).
- When detail was backfilled, `recon`, the week's `note` and a static banner still said it was missing, and a reader believes the sentence over the table (2026-09-25).
- A preview that gets `index.json` without the matching `data/weeks/` files shows the week in the selector and an empty table, with no error (2026-09-25).
- The preview once ran a whole renderer generation behind the repo while its data was current; the freshness check reads data only, so it did not notice (2026-09-23).
- Publishing `index.html` as the preview nests one document inside another and renders blank; the runbook's fragment build exists for this (2026-09-23).
- From W04 the source calls unit `BQL CT21-22` "BQL OSEN"; the map in `tools/parse_sitecheck.py` keeps the original key so the series does not break (2026-09-30).
- Calling a week "behind" from the file list alone was wrong once: the manifest in `data/index.json` said otherwise (2026-09-25).
