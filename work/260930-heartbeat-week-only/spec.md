# Spec

Status: approved by Ty 30/09 ("approve for all four", in chat).

- `docs/weekly-refresh.md` step 1: `newest-source=<week or filename>` becomes `newest-source=<week label>` (the last `wk[]` id in `data/index.json`, since the heartbeat runs before the search; `none` if there is none), plus one sentence: the note is the week only, never a file name, person's name, Drive id or figure.
- No other file documents the note (grep of the repo for `newest-source` outside `work/`, 30/09). `.github/scripts/freshness.py` reads only the timestamp, so nothing that parses the file changes.
- Doc text only. Promise: `grep -rn "week or filename" --exclude-dir=work .` prints nothing, and the next weekly run writes a week-only note.
