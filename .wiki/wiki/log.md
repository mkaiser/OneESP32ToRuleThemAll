# Log (all heat pumps)

Chronological, append-only. The TTF07 C wiki keeps **no history** (owner's decision 2026-11-22): its findings go to
its pages, how they were found to the commit messages; its old history remains in the git history.

## 2026-11-22 change: two wikis
Split into this root wiki (knowledge for all heat pumps: firmware history, entity names) and the TTF07 C wiki
`doc/ttf07c/.wiki/` (llmwiki layout: `raw/`, `wiki/`, `AGENTS.md`), which holds the device pages and all sources. Maintainer's decision.

## 2026-11-22 decision: TTF07 C knowledge base goes upstream (T023)
`doc/ttf07c/` (commit 12b) made self-contained: no links out of the folder, no T### or plan references, "owner"
instead of "maintainer", analytics device hash blanked (`<device-hash>`, device page and one capture); local IPs stay
(owner's decision). TTF07 C log deleted and restarted (owner's decision). Raw files ship as they are.

## 2026-11-22 decision: emulation always in phase Komfort (T019)
Phase Eco stops the heating circuit pump on the WPM3i, also with the real FEK; the firmware now always sends Komfort
and Eco only lowers the temperature. Verified after the flash (18:22–18:27 in Eco: pump and compressor on). Details:
[firmware history](firmware-history.md), [heating control](../../doc/ttf07c/.wiki/wiki/heating-control.md).
