---
name: todo-housekeeping
description: TODO housekeeping for the OneESP32ToRuleThemAll fork (TTF07 C / heatpump-ttf07c) - take in the maintainer's inbox, close what is done or decided, keep TODO.md forward looking, reorder by priority, take in new issues. Use when the maintainer asks to revise, clean up or update the todo list ("/todo-housekeeping", "update the todo"), when an item is finished, decided, blocked or newly found, when the file has grown long, or at the end of a session that changed what is next.
---

# TODO housekeeping

`TODO.md` is what a session reads to know what to do next, and it holds only that: one sentence an item, its plan
under `plans/`, and its requirements. `AGENTS.md` outranks this skill, and `workflow.md` says what belongs in
`TODO.md`, what belongs in a plan, and how items are numbered; this is the order to apply it in. An item whose
entry grows past a sentence or two gets a plan in `plans/`, and the entry links to it.

## Before the first write

`TODO.md` has more than one writer, and a revision touches all of it.

1. `git status --short TODO.md` and `git diff TODO.md`. Uncommitted changes that are not yours belong to another
   agent: leave them standing, leave them out of your commit, and name them in the report.
2. Re-read the file from disk. Never write back a copy read earlier in the session.
3. Change it as targeted replacements. A whole-file rewrite loses the other writer's work.

## 1. Take in the maintainer's inbox

`TODO.md`'s first section, **From the maintainer**, is read before anything else. Each entry is either done on the
spot, or filed as a numbered item in the right section with a plan under `plans/` where it needs one. Remove what
you took in as you take it, leave standing only what you could not act on (with one line saying what it waits on),
and report each entry's outcome.

## 2. Close what is done, or what was decided

An item leaves the file for one of two reasons, each needing evidence. Judge by looking, never by how the sentence
reads.

**Done** - the work exists:

- `git log --oneline --since=<the last revision of TODO.md>` and the diff of what those commits touched;
- the firmware, yaml, entity or tool the item names, read (and, for a firmware change, flashed: the device's log
  and its HA entities, `dev/development.md`);
- `.wiki/wiki/log.md`, and the page a test or capture landed on.

**Decided** - it was settled that this is not built, or is built another way. A decision closes an item for good,
so write the decision down where the next session finds it *before* taking the item out:

- a decision about the firmware, the yaml or the upstream series -> `.wiki/wiki/firmware-history.md` or the plan it
  belongs to (`plans/upstream.md`), with its reason, and a `decision` entry in `.wiki/wiki/log.md`;
- a decision about the heat pump, a register or a write -> its wiki page, cited, with a `decision` entry in
  `.wiki/wiki/log.md` (an approved write also gets its row in `.wiki/wiki/writes.md`);
- a decision an item carries on its own ("left open on purpose", "ignored for now") -> keep that sentence with
  whatever item still depends on it, or, if nothing does, put it in the commit message that removes it.

An item removed with its decision recorded nowhere is proposed again at the next revision. Preventing that is what
this step is for. An answered entry under **Open decisions** is closed the same way: the answer goes to the
document above, not back into `TODO.md`.

What you cannot decide stays, with one line saying what would decide it. Removing an item is not the same as doing
it.

## 3. Keep it forward looking

Keep what the next session needs in order to act: the decision an item waits on, the measurement that chooses
between two paths, the register, node and panel action a test needs. Drop narrative, superseded options, and
anything the firmware already does.

**Before deleting a test or capture result, confirm the wiki holds it, cited.** If it does not, ingest it first
(`.wiki/AGENTS.md`) and link the page from the item. `TODO.md` must never be the only record of a run.

Keep it short (well under ~200 lines). A section that outgrows that moves its detail to a wiki page or a `plans/`
page and keeps a link.

## 4. Reorder

Within each group, in this order:

1. what the upstream PRs need (`plans/upstream.md`);
2. work a session can start now;
3. work waiting on the season, hardware (the real FEK), the maintainer at the panel or kr0ner (that is
   **Blockers**, with what unblocks it);
4. what an open decision blocks.

**Future work** stays last. **Never renumber**: every item carries a `T###` number minted once and never reused, so
reordering and removing items leave every reference standing (`workflow.md`). A new item takes the next free number
from `TODO.md`'s first line and raises it in the same edit.

## 5. Take in what is new

- Work found in this session or the wiki log since the last revision (`git log -1 --format=%cI -- TODO.md` is the
  cutoff): a register to decode, a test to plan, a fix.
- Upstream: `git fetch upstream` and `git log --oneline HEAD..upstream/master` (a new upstream version is a rebase
  item). Upstream issues and PRs (`gh pr list -R kr0ner/OneESP32ToRuleThemAll`) only if `gh` is logged in; this host
  usually has no GitHub credentials, so skip it and say so.
- The **Recurrent check** entries: due, and still worth doing?
- The status logs of `plans/*.md`: work that finished, or blocked, without reaching `TODO.md`.

## 6. What must not change

- The sections and the grouping by area that `AGENTS.md` ("TODO.md") describes, **From the maintainer** first.
- No item implies a write to the heat pump that the maintainer has not asked for (`AGENTS.md`).
- No history: no "was", "used to", "done on". That belongs in the commit message and in `.wiki/wiki/log.md`.
- Times in CET. Links relative and resolving; a named file exists.

## Done means

- Every link in `TODO.md` resolves (and in any page you ingested into).
- One commit, `git commit -- TODO.md` plus anything you ingested or recorded a decision in; no attribution trailers
  (`AGENTS.md`). Do not push; ask.
- A report: what closed and the evidence for each, what came in and from where, what you could not decide and what
  would decide it, and any other agent's changes you left out of the commit.
