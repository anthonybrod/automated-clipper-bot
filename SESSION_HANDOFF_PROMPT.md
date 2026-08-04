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

---## §1 — READY TO PASTE (regenerated 2026-08-04)

```
Continuing the @LacyCrashOuts automated clipper bot project.

FIRST: read C:\Users\AwBro\Desktop\automated clipper bot\START_HERE.md in
full, then run its §0 self-validation before trusting it. Then CLAUDE.md
(21 numbered rules, 16 active) and INDEX.md, which catalogues every document
in the repo and when to read it. Do not reconstruct the plan from this
prompt alone — it is a pointer, the files are the record.

1. DO THIS FIRST — the user's standing instruction
Test that the save system worked, then present the checklist/progress report
and to-do list, then suggest a starting point. Do NOT pick a workstream
first. Commands are in §2 of START_HERE.md.
FIVE cold-start passes have been run and EVERY ONE found real bugs. Assume
this one will too. A pass that finds nothing is a weak test, not a pass.

2. WHERE WE ARE
Repo:   C:\Users\AwBro\Desktop\automated clipper bot
GitHub: github.com/anthonybrod/automated-clipper-bot @ 6d2ef01 (master)
Drive:  "CLAUDE AI CLIP BOT V1 attempt" — user pulls in Colab. Mount Drive
        FIRST or the path won't exist. Claude cannot push there.
Phase:  research. ZERO PIPELINE CODE EXISTS — the honest headline. But as of
        2026-08-04, Stage 3 finally has REAL NUMBERS instead of advice.

3. THE STAGE 3 FINDINGS (2026-08-04, from 50 human-curated moments)
Source: reference/mining_2026-08-04_cVkFMpDLQrM_VERBATIM.md — a curated
best-of, so every segment is a positive example, not an opinion.
- Clip length: median 39.5s, 78% in 20-70s -> target 40s, accept 20-70s,
  hard floor 11s
- Hook openings: 36% direct question, 22% shouted name/imperative, 0%
  narration
- TEXT-ONLY DETECTOR: verbal repetition in 22 of 50 moments (>=3 repeats of
  a short phrase within 10s). Needs only the transcript — no audio, no
  model, no API call. Belongs in the free statistical pre-filter.
- Moment types: physical escalation 28%, verbal roast 20%, authority 12%,
  reveal 12%, romance 12%, heist 10%, one-liner 6%

⚠️ THREE CORRECTIONS THAT CONTRADICT THE CURRENT ARCHITECTURE — resolve
before building Stage 3, do not silently apply:
1. ~20% of curated moments have NO shouting. The Architecture Outline treats
   audio-RMS spikes as a primary pre-filter — that misses 1 moment in 5.
2. Long silences are POSITIVE (physical gags). A low speech-density filter
   would delete the best set-pieces.
3. Clip length cannot be derived from caption-cue gaps (1-2s ASR cadence).

Competitive context, not a threshold: ~60M monthly views on #Lacy across
1,598 clippers, ~100% MoM growth. The payout model pays $0 below a per-post
view minimum, so this field size matters.

4. OPEN CHECKLIST
[ ] ⚡ ASK THE USER: is @LacyCrashOuts the correct handle? The H2 discovery
    agent COULD NOT FIND that account. The whole project targets it. See
    §3b of START_HERE.md. Load-bearing — do not guess.
[ ] H1 — RE-RUN. Lost to a session limit mid-write. Researches @yoxics,
    @scubaryan_, @coresculture. Full prompt preserved in PENDING §H.
[ ] G4/G5/G6 — mine the 3 remaining transcripts (PafYu69s5NA is highest
    value: it opens describing this project's exact problem, already solved)
[ ] A — Rule 20 retroactive review: 1 of 6
[ ] B — source mining: 1 of 12
[ ] D — platform/hosting research: not started
[ ] F — AI folder: PUT OFF, waits on the USER. Do not sweep it unprompted.
[ ] Transcript backup still manual
[ ] Zero pipeline code — the real work has not started
[x] C — 6 transcripts fetched, verified, 2026-08-04
[x] G1/G2/G3 — mined, saved, indexed, 2026-08-04
[x] H2 — CORE discovery, 22 VERIFIED claims
[x] Rule 22 adopted; Rules 8 & 9 dropped (2026-08-03)

5. HOW WE WORK (each rule exists because a specific failure happened)
- Rule 10: the USER decides what is "complete." Never self-stamp.
- Rule 12: verified means checked THIS session. File existence is not
  content verification.
- Rule 14: no rule adopted without explicit confirmation.
- Rule 15/16: sources word-for-word, never condensed; raw kept separate
  from evaluation.
- Rule 20: five roles per tool. Never dismiss a working free tool.
- Rule 21: run every check BEFORE reporting.
- Rule 22: update START_HERE.md last, before the final push, even when a
  usage limit is cutting the session short.
- One agent per source file. Broad-scope agents have died producing nothing;
  single-file agents have succeeded every time.
- COMMIT EACH AGENT'S REPORT ON ARRIVAL, never batch. On 2026-08-04 a
  session limit killed 3 agents mid-write; this practice cost 1 report
  instead of 3.
- NEVER delete, move, overwrite or revert without being asked. Never use
  `git checkout <file>` to undo an edit — it destroyed real work 2026-08-03.
- Budget is first-class: payouts are ~$0.50-$3.00 per 1,000 views. Ask
  before launching agents and confirm usage headroom first.

6. WHAT ONLY THE USER CAN DO
- Pull Drive (Claude has no access). Run validate_environment.py in Colab.
- Create Twitch Developer credentials.
- Triage the AI\ folder and hand over what matters.
- Answer §3b of START_HERE.md. Search the repo before asking anything new —
  INDEX.md says where everything is.
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
