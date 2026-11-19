---
name: close-session
description: Close out a working session on the OneESP32ToRuleThemAll fork (TTF07 C / heatpump-ttf07c) - write up the plans, put the findings where they are read (wiki), run the todo housekeeping, delete what is spent, run the gate, commit and report. Use when the maintainer says to close, finish, end or wrap up the session, when work is being paused for the day, or before a long break.
---

# Close a session

**Keep to `workflow.md`**'s *Closing a session*: those seven steps are the
checklist, and the rules above them carry the reasoning. Work through them in
order, whether the work is finished or only paused. This skill adds what each
step means in this repository, nothing else.

A session that produced no commit still closes: the knowledge it found is the
part that is lost.

## 1. Write up every plan you touched

A status log entry per plan under `plans/`, newest first: what you finished,
what it changed, what you were starting, what is uncommitted. The next session
has only this file.

## 2. Put the knowledge where it is read

- a measured or external fact (a test, a capture, a register, a panel menu) ->
  its wiki page under `.wiki/wiki/`, cited, plus the index and an entry in
  `.wiki/wiki/log.md` (ingest rules: `.wiki/AGENTS.md`);
- a decision about the code -> `.wiki/wiki/firmware-history.md` or
  `plans/T002-T009-upstream.md`, with a `decision` entry in `.wiki/wiki/log.md`;
- a trap in the development loop -> `dev/development.md`.

A finding that lives only in the conversation is lost when it ends.

## 3. Run the todo housekeeping

Run `/todo-housekeeping`. **Ask first whether to take the incoming items in**
-- "Incoming items by maintainer" is a holding area, and closing a session is
not by itself a request to empty it (`workflow.md`). Everything else in that
skill runs either way: close what this session finished, with its evidence;
take in what is new; reorder; raise the next free item number if you minted
one.

## 4. Delete what is spent

A finished plan, a stale handover, a working file that outlived its run (a
capture under `/share/heatpump-capture/` once it is in `.wiki/raw/captures/`).
A plan whose work is done goes once what survives it has landed in step 2; git
keeps the file.

## 5. Run the gate

```bash
C=$(docker ps --format '{{.Names}}' | grep -m1 '_esphome$')
docker exec $C esphome compile /config/esphome/heatpump-ttf07c.yaml
```

Read its real result -- the exit code and the `[SUCCESS]`/`[FAILED]` summary,
not the last cheerful line. It takes about 10 minutes: give it a timeout of 20
minutes, because a timeout kill reads exactly like a red gate.

`docker exec $C esphome config /config/esphome/heatpump-ttf07c.yaml` is enough
only when nothing outside documentation changed; a docs-only change needs only
links that resolve.

## 6. Commit your own paths

`git commit -- <your paths>`, never `git add -A`. No attribution trailers
(`AGENTS.md`). Another agent's uncommitted or staged files stay standing and
stay out of your commit. **Ask before pushing, every time** (`AGENTS.md`), and
never push to upstream.

## 7. Report

Open with the current time in CET (`TZ=Europe/Berlin date`), then: what
changed, what is uncommitted and why, whose work you left standing in the
tree, what became of the incoming items if you took them in, and the one thing
you would start next.
