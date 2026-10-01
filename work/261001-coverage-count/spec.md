# Spec

Status: approved by Ty 01/10 (same words as the intent).

- `index.html`: the coverage heading's number comes from the count of `coverage` files (`covCount`, set in `renderCoverage`), the "Tổng file tuần" tile's range runs from the first to the last `coverage` month, and the "Nguồn" note no longer names one week ("37 tuần lịch sử trích tay, các tuần sau qua connector"). No style block and no data file changes.
- Promise: on the served page the heading reads "40 file tuần", equal to the tile and to the `coverage` file count; no console errors; 40 week rows still render.
