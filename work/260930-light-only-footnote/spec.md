# Spec

Status: approved by Ty 30/09 (same message as the intent).

- `index.html` footnote: "sáng/tối theo hệ thống, bản in luôn sáng" becomes "chỉ giao diện sáng, cả trên màn hình và bản in".
- Text only: no CSS, script, data or chart change. The page already renders light only.
- After merge, the Cowork preview is rebuilt from the new `index.html` (`python3 tools/build-fragment.py`, then publish to the existing preview), because the footnote is renderer text the weekly data refresh does not touch.
- Promise: the served page and the preview both contain "chỉ giao diện sáng" and neither contains "sáng/tối theo hệ thống"; the next Pages run is green.
