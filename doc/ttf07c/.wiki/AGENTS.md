# TTF07 C wiki: schema and operations

For agents maintaining the knowledge base about the Tecalor TTF07 C with WPM3i manager, its CAN bus and this
firmware's support for it, after [microsoft/llmwiki](https://github.com/microsoft/llmwiki). The firmware is the source
of truth for what is implemented; this wiki is for what is known about the heat pump.

## Layers

| Layer | Path | Rules |
|---|---|---|
| Sources | `raw/` | Immutable inputs: CAN captures (`raw/captures/`), measurement notes, external docs. **No photos**: transcribe them into a page. Add new files named `YYYY-MM-DD-<topic>.<ext>`. |
| Wiki | `wiki/` | Markdown pages: one topic per page, cross-linked with relative links, each fact with its source (raw file or date). |
| Index | `wiki/index.md` | Catalog of all pages with a one-line summary. Update it when adding or renaming a page. |

## Sources of truth

- **Registers:** [`wiki/ttf07c-registers.md`](wiki/ttf07c-registers.md): one table of every known CAN register
  (address, firmware name, node, bus traffic, HA entity, confirmation status: test / panel / analysis / plausible /
  no value / open). Check it before naming, adding or changing a property; update it in the same change whenever a
  register is added, renamed, removed or confirmed; keep it in step with `components/wp_core/property.h`. Other pages
  link to it and never repeat register tables.
- **Control panel:** [`../control-panel.md`](../control-panel.md): the panel's menu tree.

## Operations

- **Ingest:** store the source in `raw/`, then update every affected page (not just one) and the index, in the same change as the work that produced it.
- **Query:** read `wiki/index.md` first, then the pages. An answer worth keeping is filed into the wiki.
- **Lint** (occasionally): contradictions between pages, stale claims, orphan pages, missing links; fix them.

## Writing

- Mark uncertain facts as such ("unconfirmed", "returns 0x8000").
- Times in CET (`Europe/Berlin`); a time from another zone is converted or marked (`12:00 UTC`).
- A page states what is known now. This wiki keeps **no history (no log)**: how it was found goes to the commit message.
- The heat pump is live: the firmware writes to it only what the owner approved ([writes](wiki/writes.md)).
