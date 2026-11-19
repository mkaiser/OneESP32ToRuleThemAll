---
name: todo-housekeeping
description: Revise TODO.md of the OneESP32ToRuleThemAll fork (TTF07 C / heatpump-ttf07c) - take the maintainer's incoming items in with them, close what is done or what was decided against, keep it forward looking, reorder by priority, take in new work. Use when the maintainer asks to revise, clean up or update the todo list ("/todo-housekeeping", "update the todo"), when it has grown long, and as the todo step of closing a session.
---

# Revise TODO.md

**Keep to `workflow.md`**: it says what belongs in `TODO.md` (its `Todo.md`), what belongs in
a plan under `plans/`, how items are numbered, how the maintainer's incoming
items are handled, and how to write a file more than one agent writes. Read it
first and follow it as it stands; `AGENTS.md` outranks both. This skill adds
only the order to apply it in, and what this project checks along the way.

Before the first write, do what `workflow.md`'s *Several agents write here at
the same time* says: `git status --short TODO.md`, `git diff TODO.md`, re-read
from disk, change only your part. Another agent's uncommitted changes stay
standing, stay out of your commit, and are named in the report.

## 1. Take the incoming items in, with the maintainer

**Incoming items by maintainer** is the first section and the first step
whenever this skill was asked for by name. Reached any other way -- closing a
session, a tidy-up nobody asked for -- **ask first** whether to address them,
and skip the step unless they say so. The section is a holding area; nothing
in it is due.

Taking it in is a conversation, not a filing job. Work through the entries one
at a time:

- small enough to just do: do it, remove it, say what became of it;
- anything else: say what you read the entry to mean, what you would make of
  it -- a numbered item in which section, a plan under `plans/`, an open
  decision, or nothing -- and what it would need. The maintainer settles it.
  Write the item or the plan only once they have, and remove the entry in that
  same edit;
- settled as not worth doing: record the decision where step 2 says, then
  remove the entry.

Never file an entry you had to guess at, and never invent an item from one.
What is left unsettled stays as the maintainer wrote it. Report what became of
every entry.

If the session is not interactive, do none of it: leave the whole section
standing and put what you would propose for each entry in the report.

## 2. Close what is done, or what was decided

An item leaves the file for one of two reasons, each needing evidence. Judge
by looking, never by how the sentence reads.

**Done** - the work exists:

- `git log --oneline --since=<the last revision of TODO.md>` and the diff of
  what those commits touched;
- the firmware, yaml, entity or tool the item names, read (and, for a firmware
  change, flashed: the device's log and its HA entities, `dev/development.md`);
- `.wiki/wiki/log.md`, and the wiki page a test, capture or finding landed on;
- upstream's PRs and issues (`gh pr list -R kr0ner/OneESP32ToRuleThemAll`) only
  if `gh` is logged in; this host usually has no GitHub credentials, so skip it
  and say so.

**Decided** - it was settled that this is not built, or is built another way.
A decision closes an item for good, so write the decision down where the next
session finds it *before* taking the item out:

- a decision about the firmware, the yaml or the upstream series ->
  `.wiki/wiki/firmware-history.md` or the plan it belongs to
  (`plans/T002-T009-upstream.md`), with its reason, and a `decision` entry in
  `.wiki/wiki/log.md`;
- a decision about the heat pump, a register or a write -> its wiki page,
  cited, with a `decision` entry in `.wiki/wiki/log.md` (an approved write also
  gets its row in `.wiki/wiki/writes.md`);
- a decision an item carries on its own ("left open on purpose", "ignored for
  now") -> keep that sentence with whatever item still depends on it, or, if
  nothing does, put it in the commit message that removes it.

An item removed with its decision recorded nowhere is proposed again at the
next revision. Preventing that is what this step is for. An answered entry
under **Open decisions** is closed the same way: the answer goes to the
document above, not back into `TODO.md`.

What you cannot decide stays, with one line saying what would decide it.
Removing an item is not the same as doing it.

## 3. Keep it forward looking

Keep what the next session needs in order to act: the decision an item waits
on, the measurement that chooses between two paths, the register, node and
panel action a test needs. Drop narrative, superseded options, and anything
the firmware already does. An entry that has grown past a sentence or two is a
plan that has not been written yet.

**Before deleting a test or capture result, confirm the wiki holds it, cited.**
If it does not, ingest it first (`.wiki/AGENTS.md`) and link the page from the
item. `TODO.md` must never be the only record of a run.

Keep it short (well under ~200 lines). A section that outgrows that moves its
detail to a wiki page or a `plans/` page, and keeps a link.

## 4. Reorder

Within each group, in this order:

1. what the upstream PRs need (**Release**, `plans/T002-T009-upstream.md`);
2. work a session can start now;
3. work waiting on the season, hardware (the real FEK), the maintainer at the
   panel or kr0ner (that is **Blockers**, with what unblocks it);
4. what an open decision blocks.

**Future work** stays last. Reordering and removing never touch an item's
`T###` number (`workflow.md`); a new item takes the next free number from
`TODO.md`'s first line and raises it in the same edit.

## 5. Take in what is new

```bash
git log -1 --format=%cI -- TODO.md          # the cutoff: the last revision
git fetch upstream && git log --oneline HEAD..upstream/master   # a new upstream version is a rebase item
```

- Work found in this session or in `.wiki/wiki/log.md` since the cutoff: a
  register to decode, a test to plan, a fix.
- Upstream issues (`gh issue list -R kr0ner/OneESP32ToRuleThemAll -s all
  --search "updated:>=<cutoff>"`) only if `gh` is logged in. An issue becomes
  an item only if it is work on this fork: a defect, a wanted feature,
  something that needs support. Carry its `#number`.

Check the **Recurrent check** entries while you are there (due, and still
worth doing?), and the status logs of `plans/*.md` for work that finished
without reaching `TODO.md`.

## 6. What must not change

- The sections and the grouping by area that `AGENTS.md` ("Workflow in this
  project") describes, **Incoming items by maintainer** first among them.
- No secrets in a tracked file (API and OTA keys, WiFi credentials: they live
  in the HA config's `secrets.yaml`), and no item that implies a write to the
  heat pump the maintainer has not asked for (`AGENTS.md`).
- No history (`workflow.md`, *Documents*): no "was", "used to", "done on".
  That belongs in the commit message and in `.wiki/wiki/log.md`.
- Times in CET. Links relative and resolving; a named file exists.

## Done means

- Every link in `TODO.md` resolves (and in any page you ingested into); plus
  `esphome config` (`AGENTS.md`, "Commands") if you touched yaml or C++.
- One commit, `git commit -- TODO.md` plus anything you ingested or recorded a
  decision in; no attribution trailers (`AGENTS.md`). Ask before pushing
  (`workflow.md`).
- A report: what became of each incoming item, what closed and the evidence
  for each, what came in and from where, what you could not decide and what
  would decide it, and any other agent's changes you left out of the commit.
