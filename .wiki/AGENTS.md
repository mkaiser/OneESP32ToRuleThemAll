# The wiki: schema and operations

For agents maintaining the knowledge base about the Tecalor TTF07 C (WPM3i), its CAN bus and this firmware, after
[microsoft/llmwiki](https://github.com/microsoft/llmwiki). [`../AGENTS.md`](../AGENTS.md) outranks this file.

The firmware is the source of truth for what is implemented; the wiki is for what is known about the heat pump.

## Layers

| Layer | Path | Rules |
|---|---|---|
| Sources | `raw/` | Immutable inputs: CAN captures (`raw/captures/`), measurement notes, panel photos, external docs. Never edit; add new files named `YYYY-MM-DD-<topic>.<ext>`. |
| Wiki | `wiki/` | Markdown pages: one topic per page, cross-linked with relative links, each fact with its source (raw file or date). |
| Index | `wiki/index.md` | Catalog of all pages with a one-line summary. Update it when adding or renaming a page. |
| Log | `wiki/log.md` | Chronological, append-only: `## YYYY-MM-DD <kind>: <title>` (kinds: ingest, change, test, decision, lint). |

## Registers

**[`wiki/ttf07c-registers.md`](wiki/ttf07c-registers.md) is the source of truth**: one table of every known CAN
register of this TTF07 C (address, firmware name, node, bus traffic, HA entity, confirmation status: test / panel /
analysis / plausible / no value / open). Check it before naming, adding or changing a property; update it in the
same change whenever a register is added, renamed, removed or confirmed, and keep it in step with
`components/wp_core/property.h`. Other pages describe behaviour and tests and link to it; they never repeat
register tables.

## Operations

- **Ingest:** store the source in `raw/`, then update every affected page (not just one) and the index, and append
  to the log, in the same change as the work that produced it.
- **Query:** read `wiki/index.md` first, then the pages. An answer worth keeping is filed into the wiki.
- **Lint** (occasionally): contradictions between pages, stale claims, orphan pages, missing links; fix them and log
  the lint.

## Writing

- Mark uncertain facts as such ("unconfirmed", "returns 0x8000").
- Times in CET (`Europe/Berlin`); a time from another zone is converted or marked (`12:00 UTC`).
- A page states what is known now; how it was found goes to the log.
