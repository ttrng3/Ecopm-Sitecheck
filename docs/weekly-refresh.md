# ECOPM weekly refresh runbook

Canonical. If the routine prompt and this file disagree, **this file wins**.

## Runs where?

Any cloud session with the Microsoft 365 connector and the GitHub MCP file
tools. Both are account-level, so this runs with the Mac shut. No step needs it.

## Steps

### 1. Heartbeat, always, before anything else

Write `data/.last-check` — one line, current UTC as `%Y-%m-%dT%H:%M:%SZ`, a
space, then `newest-source=<week or filename>` — and commit it, even on a quiet
run. It separates *"ran, nothing new"* from *"stopped running"* (which
`data/index.json` alone cannot express) and it exercises the write path every
week, so a broken write surfaces on a quiet Monday rather than on the one
Monday that has data.

### 2. Find the newest source

`sharepoint_search`, `fileType: "xlsx"`. Use **only** the tree whose `webUrl`
contains `ECOPM/ECOPM - SITECHECK/1. Ecopm Sitecheck/`.

**The trap:** the `OMNI - CÁC TÀI LIỆU/OMNI - SITECHECK/` tree holds files with
**identical names** and different numbers — that is the OMNI project, with its
own repo (`ttrng3/Omni-sitecheck`). Taking its figures corrupts this series
silently, because the filenames look right.

### 3. Stop if nothing is new

If `data/index.json`'s last `wk[]` entry is already the newest source week,
commit just the heartbeat, report "no new data", and stop.

### 4. Read the workbook

`read_resource` on the file `uri` returns every sheet as tab-separated cell
values, including row detail — no download, no openpyxl. The summary is the
`TH` / `BC TỔNG` sheet; the eight operations units are the `depts` in
`data/index.json`.

### 5. Write two files via the GitHub MCP file tools

`get_file_contents` for the current blob sha, then `create_or_update_file` on
`main`. Shell `git push` can be refused by the auto-mode classifier in an
unattended run — the MCP calls are not, so they are the primary path.

- `data/weeks/<YYYY-MM-Wnn>.json` — array of `{dept, loc, issue, action, resp,
  deadline, status}`, verbatim. Do not translate, tidy, or deduplicate;
  duplicates in the source are a finding, not noise.
- `data/index.json` — append to `wk`, add the week to `detail`, update `asof`,
  `generated` (display, `DD/MM/YYYY`) and `generatedUtc` (ISO). Set `mode`
  honestly: `full`, `raised`, or `gap`.

### 6. Verify, do not assume

Confirm `main` moved using the sha the write returned. Say plainly if you could
not reach the live site rather than claiming a success you did not observe.
