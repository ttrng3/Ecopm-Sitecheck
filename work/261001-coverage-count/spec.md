# Spec

Status: approved by Ty 01/10 (same words as the intent).

- `index.html`: the coverage heading's number comes from the count of `coverage` files (`covCount`, set in `renderCoverage`), the "Tổng file tuần" tile's range runs from the first to the last `coverage` month, and the "Nguồn" note carries no count ("lịch sử trích tay, các tuần sau qua connector"). The heading shows "—" until the data loads. Same class, same file (review #15): the "Cách đọc" range is derived from the first and last `wk` ids, with "(không còn khoảng trống)" only when no week is a `gap`; the two "TB ~34 / ~23" notes become the last-12-full-weeks average of that unit's `out`, labelled "TB 12 tuần" (the typed values matched no average of the data). No style block and no data file changes.
- Promise: on the served page the heading reads "40 file tuần", equal to the tile and to the `coverage` file count; the range reads 12/2025 → 09/2026; the averages read ~35 and ~30; no console errors; 40 week rows still render.
