# SESSION HANDOFF PROMPT — the standing format

**What this is.** The user pastes a catch-up prompt at the start of every
fresh session. That prompt has a proven format — it worked cold on
2026-08-03 with no re-derivation. This file preserves the format so it is
never re-invented, and holds the **current ready-to-paste version**.

**Two parts:**
- **§1 — READY TO PASTE.** Regenerated at the end of every session. The
  user copies this block verbatim into a new session.
- **§2 — THE TEMPLATE.** What is constant (never changes) vs. what gets
  updated. Use this when regenerating §1.

**Who maintains it:** Claude regenerates §1 as part of the end-of-session
save, alongside `START_HERE.md`. The user just copies.

---
## §1 — READY TO PASTE (regenerated 2026-08-03, all blockers resolved)

```
Continuing the @LacyCrashOuts automated clipper bot project.

FIRST: read C:\Users\AwBro\Desktop\automated clipper bot\START_HERE.md in
full, then run its §0 self-validation before trusting anything in it. Then
read that repo's CLAUDE.md (21 numbered rules, 16 active) and PROJECT.md.
Do not reconstruct the plan from this prompt alone — this is a pointer, the
files are the record.

1. WHERE WE ARE
Repo:   C:\Users\AwBro\Desktop\automated clipper bot
GitHub: github.com/anthonybrod/automated-clipper-bot @ HASHGOESHERE (master)
Drive:  "CLAUDE AI CLIP BOT V1 attempt" — user pulls manually in Colab.
        Claude cannot push there. Mount Drive FIRST or the path won't exist.
Phase:  research and organization. ZERO PIPELINE CODE EXISTS. That is the
honest headline; everything built so far is project restoration, source
verification, tool cataloguing, and the operating rules + save system.

2. DO THIS FIRST — the user's own instruction, verbatim (2026-08-03)
"1st test the save project we made today worked then present the checklist
progress report and to do list and suggest starting point"

Do it in that order. DO NOT pick a workstream first — the user deliberately
declined to choose one until after this report. Step-by-step commands are
in §2 of START_HERE.md. Four cold-start test passes were run on 2026-08-03
and EVERY ONE found real bugs — assume this one will too. A pass that finds
nothing is a weak test, not a clean bill of health.

3. WHAT LANDED LAST SESSION (2026-08-03)
- START_HERE.md — the single session entry point (a router, not a duplicate)
- SAVE_PROTOCOL.md — 9 ordered steps for "save everything", plus the written
  START_HERE.md format so it can't degrade each time it's overwritten
- 4 global hooks in ~/.claude/hooks/ + a user-level ~/.claude/CLAUDE.md that
  loads in EVERY session regardless of working directory
- check_links.sh — 51 links across 5 docs, wired into the Stop hook
- .claude/ added to .gitignore — raw prompt logs were one `git add -A` from
  a public repo
- Rule 22 ADOPTED by the user; Rules 8 & 9 DROPPED by the user

4. OPEN CHECKLIST
[x] Rule 22 — updating START_HERE.md is the non-skippable last action of
    every session. ADOPTED by the user 2026-08-03.
[x] Rules 8 & 9 (ffmpeg faststart; .ass karaoke captions) — DROPPED by the
    user 2026-08-03. Gemini-sourced, adopted without authorization; that is
    why they went, not a technical judgment. Decide them at build time.
[ ] Workstream A — Rule 20 retroactive review: 1 of 6 done (remaining:
    A2 HF-vision, A3 HF-LLM, A4 mining report, A5 78-source audit,
    A6 the 17 videos)
[ ] Workstream B — source mining: 1 of 12 done
[ ] Workstream C — 6 untranscribed YouTube videos: mFOoNPFylLI,
    PafYu69s5NA, QqwNue_KL-4, cVkFMpDLQrM, mVqnCvE337E, lYafPAHVOno
[ ] Workstream D — platform / free-inference / hosting research: not started
[ ] Transcript backup is still manual (SAVE_PROTOCOL step 8) — the one
    unclosed hole in the save system
[ ] Zero pipeline code — the real work has not started

5. HOW WE WORK (each rule exists because a specific failure happened)
- Rule 10: the USER decides what is "complete." Never self-stamp. When they
  authorize it, mark it "COMPLETE — authorized by user YYYY-MM-DD".
- Rule 12: verified means checked THIS session. File existence is not
  content verification.
- Rule 14: no rule is adopted without the user's explicit confirmation.
- Rule 15/16: source material saved word-for-word, never condensed, and kept
  in separate files from any evaluation of it.
- Rule 20: evaluate every tool for five roles — primary, backup/fail-safe,
  cross-check, assist, feature. Never dismiss a working free tool.
- Rule 21: run every check BEFORE reporting, not after being asked.
- Rule 22: update START_HERE.md as the last action, before the final push,
  even when a usage limit is cutting the session short.
- NEVER delete, move, overwrite or revert anything without being asked.
  Never use `git checkout <file>` to undo an edit — it reverts the whole
  file. This destroyed real work on 2026-08-03.
- Budget is a first-class constraint: payouts are ~$0.50-$3.00 per 1,000
  views, so recurring API cost eats the margin directly. Ask before
  launching agents and confirm usage headroom first.

6. WHAT I CANNOT DO
- Push to Google Drive (no Desktop app, no API). The user pulls in Colab:
  mount Drive FIRST, then git pull — or run the full bootstrap cell, which
  clones if the folder doesn't exist and pulls if it does.
- Guarantee the notes caught everything. The verbatim prompt log at
  .claude/session-prompts.log and the raw transcripts are the fallback.

7. WHAT ONLY THE USER CAN ANSWER
See §3b of START_HERE.md — standing questions, kept with their answers.
Search the repo before asking anything new; the whole record is in git and
mirrored in Drive.
```


## §2 — THE TEMPLATE

Six sections, in this order. **Constants stay word-for-word; variables get
updated from real state, never from memory.**

### Section 1 — "just to catch you up:"
**CONSTANT:**
- Read `START_HERE.md` first, full repo path
- Name the detailed-agenda file behind it
- *"Don't reconstruct anything from memory or chat history — read the files."*

### Section 2 — "TASK #1, before anything else:"
**VARIABLE.** The single specific next action, not a menu. If it has parts,
number them. Say what is already done so it isn't redone. Pulled from
`START_HERE.md` §2.

### Section 2b — "OPEN CHECKLIST — carry this forward and tick things off:"
**VARIABLE.** Every open item as a `[ ]` checkbox, including things blocked
on the user. Prose describes; a checklist *tracks*. This is what survives
across many sessions — items get ticked, not rewritten. Keep blocked items
in the list rather than moving them elsewhere, so nothing quietly drops.

### Section 3 — "THEN [n] research workstreams, my pick of order:"
**VARIABLE progress, CONSTANT structure.** One lettered entry each, with
current progress `(x of y done)` and any non-obvious note (a gotcha, a
reusable script, why it matters). Pulled from the resume file's agenda board.

### Section 4 — "ALSO READ:"
**MOSTLY CONSTANT.** Rule count changes; the rest holds:
- `CLAUDE.md` — N rules, M active
- *"Don't just read them, apply them: they're strict defaults and deviating
  from one requires asking me first."*
- **The non-negotiables, spelled out** (not just "follow the rules") — final
  say on completion; nothing factual unless confirmed; external-AI is
  reference only; run checks BEFORE reporting; preserve source verbatim;
  raw records separate from evaluation; don't dismiss free tools
- `MASTER_TOOLS_CATALOG` before picking any tool
- `PROJECT.md` currency date

### Section 5 — "BEFORE STARTING ANYTHING:"
**CONSTANT structure, VARIABLE values:**
- Confirm the checkpoint: `git log`, `git status`, synced with origin —
  **with the real last-known-good commit hash**
- What to raise early (open decisions the user owes an answer on; usage
  headroom before agents)
- Unverified leads to check before related build work

### Section 4b — "LAST SESSION — what got built:"
**VARIABLE.** A short progress report: what actually shipped last session.
Not a changelog of every commit — the things a fresh session needs to know
exist so it doesn't rebuild them. This is the section that stops a stale
prompt sending someone to redo finished work (which happened on
2026-08-03 — the prompt still said "build START_HERE.md" after it existed).

### Section 4c — "NEW THIS SESSION — things found, not yet acted on:"
**VARIABLE.** New ideas, tools, discoveries, and bugs found but not yet
resolved. Distinct from 4b: that is *done*, this is *known but open*.
Include external tools/repos discovered and what was taken from them.
Without this section, findings die with the session that made them.

### Section 5 — "BEFORE STARTING ANYTHING:"
**CONSTANT structure, VARIABLE values:**
- Confirm the checkpoint: `git log`, `git status`, synced with origin —
  **with the real last-known-good commit hash**, plus the note that HEAD
  being one ahead is normal
- What to raise early (open decisions the user owes an answer on; usage
  headroom before agents)
- Unverified leads to check before related build work
- Anything installed last session that is being exercised for the first
  time this session

### Section 6 — "CONTEXT I'll forget:"
**MOSTLY CONSTANT.** The operational reality that never survives a context
reset:
- Budget is live — metered, hard weekly reset Monday 1pm, hit repeatedly
- Documentation work is not cheap (cite a real burn-rate data point)
- Drive mechanism: Claude pushes to GitHub, user pulls in Colab, fresh
  runtime needs `drive.mount()` first
- Where the raw record lives (prompt log + transcript backup) and that it
  is the fallback when a curated note is missing or disputed
- **The honest headline** — currently "still zero pipeline code"

---

## §3 — Maintenance rules

1. **Regenerate §1 before the final push of every session**, alongside
   `START_HERE.md`. If Rule 22 is adopted, this is covered by it.
2. **Never carry a stale commit hash.** "Last known good" is the single
   most load-bearing line — a wrong hash sends the next session chasing a
   checkpoint that doesn't exist. Verify with `git log` before writing it.
3. **Keep the non-negotiables spelled out, not summarized.** "Follow the
   rules" demonstrably does not work — this project's failure report
   documents 9 standing rules being available and not consulted. Naming the
   specific ones that get broken is the point.
4. **Update the honest headline.** It currently reads "still zero pipeline
   code." When that changes, change it. It is the line that stops a list of
   green checkmarks from implying more progress than exists.
5. **Never delete a section.** If something no longer applies, mark it
   resolved rather than removing it.
