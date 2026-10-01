# Spec

Status: approved by Ty 01/10 (same words as the intent).

- `data/index.json` `recon`: "xác nhận đọc đúng cây ECOPM, không phải cây <other entity>." becomes "xác nhận đọc đúng cây ECOPM." Nothing else changes.
- `docs/weekly-refresh.md` step 2 gains two lines: never name the other entity in `recon`, `verdict` or any note; say only that the ECOPM tree was read. The new lines do not name it either.
- Promise: outside `REVIEW.md` (the reviewer's own rule) and `data/weeks/`, `grep -rn` of the other entity's name prints nothing at head; the file parses; after merge the live `data/index.json` has no such name and the Pages run is green. The weekly run on 5 Oct writes `recon` without it.
