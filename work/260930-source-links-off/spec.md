# Spec

Status: approved by Ty 30/09 ("approve 8", in chat; the recommendation was "remove source links").

- `index.html`: the function that built each week's source URL is removed. The week table shows the source file name as plain text instead of a link. The detail table's empty-state note, which linked to the source file, now names the file as plain text.
- Nothing else changes: no data file, stylesheet, chart or routine. The routine prompt and `docs/weekly-refresh.md` never tell the routine to record a link, and no file under `data/` carries the host or the path, so nothing upstream produces it again.
- Not changed, reported to Ty instead: a sentence in `data/index.json` (routine-era data; hand edits to `data/` are out of bounds) still tells readers to open the source from the detail table. It is now stale, but it holds no path.
- The old path stays in git history; rewriting history is Ty's call.
- Promise: a case-insensitive `git grep` of the tree for the file host's domain, the personal-storage path prefix, the person's path segment and the tenant host returns nothing (exit 1); the exact patterns are passed at run time, not written here, so this file does not match itself. The page, served locally and rendered by headless Chrome, draws one row per week in `data/index.json` (40 of 40 at the time of writing) and contains no link to the file host. The file name is shown through the page's `esc()` (reviewer round 1, Low 3).
