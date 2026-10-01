# Spec

Status: approved by Ty 01/10 (same words as the intent: remove the option).

- `data/index.json` `recon`: delete the one sentence "Bấm 'Mở file nguồn' ở bảng chi tiết để xem trực tiếp trên SharePoint." Nothing else changes.
- The weekly run wrote that sentence on its own (30/09, a64ced5); the runbook does not ask for it, so no runbook change.
- Promise: `grep -c "Mở file nguồn" data/index.json` prints 0 at head, the file parses, and after merge the live `data/index.json` has no such sentence while the Pages run is green.
