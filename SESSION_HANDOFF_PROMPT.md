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

## §1 — READY TO PASTE (current as of 2026-08-03)

> ⚠️ Regenerate this block before the final push of every session.
> "Last known good" below must match the actual final commit.

```
just to catch you up: Read START_HERE.md in the automated clipper bot repo
first (C:\Users\AwBro\Desktop\automated clipper bot). It's the single
session entry point — state now, next action, blockers, where things are.
reference/PENDING_agent_prompts_resume_2026-08-01.md holds the detailed
per-item agenda behind it. Don't reconstruct anything from memory or chat
history — read the files.

TASK #1, before anything else:
  Propose Rule 22 and get my explicit yes or no — updating START_HERE.md is
  the last action of every session, before the final push, non-skippable,
  even when a usage limit is cutting things off. This is the part that makes
  the reference system automated rather than dependent on you remembering.
  START_HERE.md itself is already built (commit 8dc0890).

THEN four research workstreams, my pick of order:
  A. Rule 20 retroactive review (1 of 6 done) — re-check already-"completed"
     work for free tools dismissed too readily. A6, the 17 already-mined
     YouTube videos, is likely the biggest single payoff in the project.
  B. 12-item source mining (1 of 12 done). Items 2-12 already carry the
     Rule 20 instruction in their prompt template.
  C. 6 untranscribed YouTube videos. research/fetch_transcripts.py already
     exists and hit 17/17 before — reuse it, don't browser-scrape. The 3
     Lacy-specific ones are the only source anywhere for what a clip-worthy
     moment actually looks like.
  D. Platform / free-inference / hosting research (not started). Scope is in
     reference/research_targets_platforms_2026-08-02.md. Highest-leverage
     lead: Ollama on a free Oracle ARM VM.

ALSO READ: CLAUDE.md — 21 rules, 15 active. Don't just read them, apply
them: they're strict defaults and deviating from one requires asking me
first. The non-negotiables — I have final say on phase transitions and
"complete"; nothing is factual unless confirmed this session or I OK'd it;
external-AI material (Gemini etc.) is reference only; run every check BEFORE
reporting done, not after I ask; preserve source material word-for-word;
keep raw records separate from evaluation; don't dismiss free tools —
evaluate against all five roles. Also read
reference/MASTER_TOOLS_CATALOG_2026-08-02.md (~110 tools with URLs) before
picking any tool for a stage. PROJECT.md is current as of 2026-08-02.

BEFORE STARTING ANYTHING:
  - Confirm the checkpoint held: git log, git status, synced with origin.
    Last known good is 8dc0890, clean tree, local = GitHub = Drive.
  - Raise these early: I owe you a yes/no on provisional Rules 8 and 9, and
    on the uncommitted .gitignore + START_HERE backup-documentation change.
    You need to confirm I have usage headroom before launching agents.
  - Two unverified leads are in the resume file — does the sibling project's
    video code still run, and is validate_environment.py one auth fix from
    passing. Check those before related build work, not after.

CONTEXT I'll forget: budget is a live constraint (metered, hard weekly reset
Monday 1pm, hit repeatedly). Documentation work is not cheap — one recent
session went fresh to 100% on a single agent plus note-keeping. Drive has no
direct access from your side; you push to GitHub, I pull in Colab, and a
fresh Colab runtime needs drive.mount() before the pull will work. Raw
session transcripts are backed up outside the repo at
AI\claude_transcripts_backup_<date>\ — they're the fallback when a curated
note is missing or disputed. Still zero pipeline code written — that's the
honest headline, everything so far is restoration, research, and rules.
```

---

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

### Section 6 — "CONTEXT I'll forget:"
**MOSTLY CONSTANT.** The operational reality that never survives a context
reset:
- Budget is live — metered, hard weekly reset Monday 1pm, hit repeatedly
- Documentation work is not cheap (cite a real burn-rate data point)
- Drive mechanism: Claude pushes to GitHub, user pulls in Colab, fresh
  runtime needs `drive.mount()` first
- Transcript backup location and why it exists
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
