# Verification: the weekly page

## Promise

Every file https://ttrng3.github.io/Ecopm-Sitecheck/ serves (the page, `index.json`, every week file) is byte-identical to `main`. `main`'s data adds up: every week's units sum to its totals, every claimed detail file exists, and a week without detail says so. The page renders a row for every week, and the newest week with detail renders every one of its rows, with no console error. Nothing private, personal or from another entity is served. The Cowork preview carries either `main`'s data or the last weekly run's.

## Clean state

```bash
cd ~/Projects/Ecopm-Sitecheck && git checkout main && git pull --ff-only
```
Run after a weekly run (the ECOPM Sitecheck routine's cron, `0 14 * * 1` UTC = 21:00 Monday Hanoi, read with `RemoteTrigger get` on 01/10) or after any merge. Wait for the merge's Pages run to go green first (`gh run list -w "Pages (allowlist)" -L1`).

## Steps

1. **Repo and live site.** `python3 tools/verify_live.py --forbid <other entity's name>` → exit 0 and `"pass": true`. The name comes from the runner's own notes (entity separation). It is never written into this repo. Without `--forbid` the entity verdict fails on purpose.
2. **Live page in Chrome.** Open https://ttrng3.github.io/Ecopm-Sitecheck/. Stub dialogs, then run the invariants below. Expected: one row per `wk` entry; the heading number equals the `coverage` file count; clicking the newest week with detail renders as many rows as its week file holds; clicking the newest week without detail (if any) renders the "Chưa trích được" row.
3. **Console.** Reload, then read errors for `TypeError|ReferenceError|Uncaught|SyntaxError`. Expected: none.
4. **Preview.** Get the preview link from the ECOPM Sitecheck routine's prompt (`RemoteTrigger get`). Never write it here. `Artifact list` its files, then `Artifact read` `data/index.json` and the newest week file. Expected files: `index.html` (the fragment the runbook builds), `data/index.json`, and one `data/weeks/<id>.json` per `detail` entry; nothing else. The newest week file's sha256 equals `main`'s. `index.json`'s sha256 equals either `main`'s (`shasum -a 256 data/index.json`) or the last weekly run's: `c=$(git log --format='%h %s' -- data/index.json | grep -v ' (#[0-9]*)$' | head -1 | cut -d' ' -f1); git show $c:data/index.json | shasum -a 256`, i.e. the last commit to `index.json` that is not a squash-merged PR (their titles end `(#N)`); routine runs commit directly. If only PRs (`(#N)` titles) changed it since, it is behind by design until the next run.

## Invariants

Step 1 prints these verdicts, all of which must be true: `has_weeks`, `served_equals_main`, `private_not_served`, `weeks_ordered_unique`, `sums_match`, `coverage_matches_weeks`, `dept_keys_known`, `detail_files_match`, `detail_rows_match`, `missing_detail_declared`, `heartbeat_fresh` (≤ 9 days, pipeline-wiring's watchdog for this pipeline), `data_fresh` (≤ 24 days, `freshness.py`'s default), `no_personal_traces`, `no_forbidden_words`.

Step 2, in the page:
```js
window.confirm=()=>true; window.alert=()=>{};
await new Promise(r=>setTimeout(r,2500));
const d=await fetch('data/index.json?v='+Date.now()).then(r=>r.json());
const rows=[...document.querySelectorAll('#weeklyTbody tr.clickable')].map(r=>r.dataset.id);
const head=[...document.querySelectorAll('h2')].map(h=>h.innerText).find(t=>/file tuần/.test(t))||'';
const cov=d.coverage.reduce((s,m)=>s+m.files.length,0);
const pick=async id=>{const tb=document.getElementById('detailTbody');tb.innerHTML='';document.querySelector(`#weeklyTbody tr[data-id="${id}"]`).click();for(let i=0;i<40;i++){await new Promise(r=>setTimeout(r,200));if(tb.querySelectorAll('tr').length>0)break;}return tb;};
const withDetail=Object.values(d.detail).sort().pop(), file=await fetch(`data/weeks/${withDetail}.json?v=`+Date.now()).then(r=>r.json());
const a=(await pick(withDetail)).querySelectorAll('tr').length;
const without=d.wk.map(w=>w.id).filter(id=>!(id in d.detail)).pop();
const b=without?(await pick(without)).innerText.includes('Chưa trích được'):true;
JSON.stringify({rows_match:rows.length===d.wk.length&&new Set(rows).size===rows.length, newest_row:rows.includes(d.wk.at(-1).id),
  heading_matches:head.includes(' '+cov+' '), detail_rows_render:a===file.length, missing_week_says_so:b,
  no_stale_button:!document.body.innerText.includes('Mở file nguồn')})
```
All of them must be true.

## Adversary

- **A stranger on the public page.** `private_not_served`: README, CLAUDE.md, REVIEW.md, the runbook, the heartbeat, the four `tools/` scripts, this protocol, a `work/` file, `.github/scripts/freshness.py` and `.pages-allow` all answer 404. `no_personal_traces`: no OneDrive `/personal/` path, SharePoint or 1drv link, or email address in the page, `index.json` or any week file (the 30/09 source links held a person's path). Matches are reported by count and file, never by value.
- **The other entity's tree read by mistake** (identical file names, different numbers). `no_forbidden_words` keeps its name off the page. The numbers themselves cannot be told apart by a script: see Not covered.
- **A half-finished run** that appends a week to `wk` without its detail, or claims detail it never wrote. Caught by `detail_files_match`, `detail_rows_match` and `missing_detail_declared`, which looks where runbook step 4 says to write it: that month's `coverage` note (or the week's own note). The 22/09 run said nothing anywhere.
- **A source that renames a unit** (W04: "BQL OSEN"). An unmapped key fails `dept_keys_known`.
- **A run that appends a week to `wk` but not to `coverage`.** The heading and tiles would lag the table. `coverage_matches_weeks`.
- **A routine that stopped running.** `heartbeat_fresh`. **A routine that runs but publishes nothing:** `data_fresh`.
- **A renderer that drifts from the data** (the heading said 38 while the data had 40, and two averages were typed constants, until 01/10, #15). Caught by `heading_matches` and `rows_match`.
- **A preview a generation behind** (23/09). Caught by step 4.

## Sanctioned substitutes

- The forbidden word list is passed on the command line, so the public repo never names the other entity. This proves the served files and the tracked data don't contain it. It does not prove the numbers came from the right tree.
- The preview cannot be fetched by a script (artifact links need the Artifact tool), so step 4 is done by the runner with `Artifact list` and `Artifact read`.

## Evidence

- The JSON from step 1 and the JSON from step 2.
- Screenshots (`save_to_disk: true`): the top of the page, the detail table with the newest week that has detail, and the newest week without detail together with the "Độ phủ nguồn" heading.
- For step 4: the preview's file count and the two hashes.

## Not covered

- Whether the numbers came from the ECOPM tree and not the other entity's. Only the runbook's path rule guards this. The cross-check is manual: compare the previous-week column of the new file with the published previous week.
- Whether the totals equal the workbook's TỔNG CỘNG cell. The workbook is not reachable from here.

## Traps

- Pages answers `cache-control: max-age=600` (10 minutes; checked 01/10 with `curl -sI`). A `served_equals_main` failure straight after a merge is the cache: wait for the Pages run, then re-run. The script adds `?v=` to every request.
- Read the console after a reload. Tracking starts on the first read, so errors from the first load are missed.
- The week file loads after the click, slower on Pages than on a local serve. A fixed 1.2s wait read the table before it filled on the first live run (01/10); `pick` now empties the table, clicks, and waits until any row appears (max 8s), so it never reads the previous week's rows.
- `detailTbody` renders every row (no paging). If paging is ever added, `detail_rows_render` must count the "N / N đầu việc" label instead.
- `generatedUtc` and the heartbeat parse with Python 3.9's `fromisoformat` (`Z`, `+00:00`, 3- or 6-digit fractions). Anything else reads as unparseable and fails `data_fresh` / `heartbeat_fresh`, never a crash.
- Fetching all 39+ week files takes about two minutes; each request retries once on a network error or a 5xx, because one blip failed `served_equals_main` on the first full run (01/10).
- Weekly-run commit titles vary (only one ever began `data:`), and the heartbeat is committed before the data (30/09: heartbeat ceb210a, then data a64ced5), so neither a title prefix nor the heartbeat commit finds the run's data. Step 4 takes the last `index.json` commit that is not a `(#N)` PR merge.
- The preview's `index.json` lags `main` after any PR that touches data. That is by design: the runbook refreshes the preview on the next weekly run. Judge it against the last non-PR `index.json` commit, not `main`.
