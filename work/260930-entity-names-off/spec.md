# Spec

Status: approved by Ty 30/09 ("approve 7", in chat).

- `docs/weekly-refresh.md` step 2: the trap paragraph keeps the warning (a second tree on the tenant holds identically named files with different numbers; never read or mix it) and drops the other tree's path, its entity name and its repo. The positive rule is unchanged: only the `ECOPM/ECOPM - SITECHECK/1. Ecopm Sitecheck/` path is this project, and it is the only test. The same step's 2026-09-27 note says "another dashboard's routine".
- `README.md`: the same 2026-09-27 note, reworded the same way.
- `index.html`: two comments lose the other entity's name. One is a CSS comment inside the base `<style>` block (the filter-bar note), the other a script comment. No rule, markup or behaviour changes; covered by Ty's "approve 7".
- `tools/reconcile.py`: the docstring's shape table labels the other dashboards by shape, not by name. Docstring only.
- Not changed, reported to Ty instead: `REVIEW.md` (the reviewer's entity-separation rule has to name what it screens for), the source-link host in `index.html` (a working link to the source files; changing it breaks the links), and one sentence in `data/index.json` (routine-written data; hand edits to `data/` are out of bounds).
- The abbreviation for thương mại dịch vụ (a commercial area) also appears in `data/weeks/`: `2025-12-W03.json` (`action`, `resp`) and `2026-03-W04.json` (`loc`). There it is this project's own site term, not the other dashboard. It stays.
- Promise: a case-insensitive `git grep` for the other entity's name returns exactly 6 hits on 4 lines, all in the reported spots: `REVIEW.md:33` (1), `REVIEW.md:52` (2), `data/index.json:1356` (1), `index.html:493` (2: the tenant host and a personal account path). The page behaviour is unchanged; `python3 tools/reconcile.py --help` still prints its usage (it exits 1 by design when given no data trees).
- Open for Ty (reviewer round 1, Critical): the `index.html:493` source link encodes one person's account on a public page. Fixing it means pointing the links at a shared library or removing them, which is outside this spec. Ty decides.
