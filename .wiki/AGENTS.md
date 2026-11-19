# The wiki: schema and operations

For agents maintaining the knowledge bases of this firmware fork, after
[microsoft/llmwiki](https://github.com/microsoft/llmwiki). [`../AGENTS.md`](../AGENTS.md) outranks this file.

The firmware is the source of truth for what is implemented; the wiki is for what is known about the heat pump.

## Two wikis

| Wiki | Path | Scope |
|---|---|---|
| Root (this one) | `.wiki/` | Knowledge for all heat pumps of this firmware: firmware history, entity names |
| TTF07 C | `doc/ttf07c/.wiki/` (schema additions in its `AGENTS.md`) | Everything specific to the TTF07 C / WPM3i: registers (source of truth), CAN bus, heating control, FEK2, writes, sources and captures; the history before 2026-11-22 |

Both use the same layout and the rules below. A finding goes to the wiki of its scope; a page that grows general
moves to the root wiki.

## Layers (in each wiki)

| Layer | Path | Rules |
|---|---|---|
| Sources | `raw/` | Immutable inputs: CAN captures (`raw/captures/`), measurement notes, external docs; **no photos** (transcribe them into a page). Never edit; add new files named `YYYY-MM-DD-<topic>.<ext>`. |
| Wiki | `wiki/` | Markdown pages: one topic per page, cross-linked with relative links, each fact with its source (raw file or date). |
| Index | `wiki/index.md` | Catalog of all pages with a one-line summary. Update it when adding or renaming a page. |
| Log | `wiki/log.md` | Chronological, append-only: `## YYYY-MM-DD <kind>: <title>` (kinds: ingest, change, test, decision, lint). |
| Schema | `AGENTS.md` | This file; the TTF07 C wiki's `AGENTS.md` adds its specifics (registers page as source of truth). |

## Operations

- **Ingest:** store the source in the `raw/` of the wiki it belongs to, then update every affected page (not just one) and the index, and append
  to the log, in the same change as the work that produced it.
- **Query:** read `wiki/index.md` first, then the pages. An answer worth keeping is filed into the wiki.
- **Lint** (occasionally): contradictions between pages, stale claims, orphan pages, missing links; fix them and log
  the lint.

## Writing

- Mark uncertain facts as such ("unconfirmed", "returns 0x8000").
- Times in CET (`Europe/Berlin`); a time from another zone is converted or marked (`12:00 UTC`).
- A page states what is known now; how it was found goes to the log.
