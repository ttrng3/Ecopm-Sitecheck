# Spec

Status: approved by Ty 30/09 ("approve 7", in chat).

- `docs/weekly-refresh.md` step 2: the trap paragraph keeps the warning (a second tree on the tenant holds identically named files with different numbers; never read or mix it) and drops the other tree's path, its entity name and its repo. The positive rule is unchanged: only the `ECOPM/ECOPM - SITECHECK/1. Ecopm Sitecheck/` path is this project, and it is the only test. The same step's 2026-09-27 note says "another dashboard's routine".
- `README.md`: the same 2026-09-27 note, reworded the same way.
- `index.html`: two code comments lose the other entity's name. No markup, style or script behaviour changes.
- `tools/reconcile.py`: the docstring's shape table labels the other dashboards by shape, not by name. Docstring only.
- Not changed, reported to Ty instead: `REVIEW.md` (the reviewer's entity-separation rule has to name what it screens for), the source-link host in `index.html` (a working link to the source files; changing it breaks the links), and one sentence in `data/index.json` (routine-written data; hand edits to `data/` are out of bounds).
- Data files under `data/weeks/` contain "TMDV" as a Vietnamese site term (thương mại dịch vụ); that is this project's own data and stays.
- Promise: `git grep -i` for the other entity's name returns only the three reported spots above; the page still renders (no behaviour change); `python3 tools/reconcile.py --help` still prints its usage (it exits 1 by design when given no data trees).
