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

## §1 — READY TO PASTE (regenerated 2026-08-04, in the §2 template format)

```
just to catch you up: Read START_HERE.md in the automated clipper bot repo
first (C:\Users\AwBro\Desktop\automated clipper bot). It's the single
session entry point, and it opens with §0 — a self-validation checklist.
Run those checks before trusting anything in it. INDEX.md catalogues every
document in the repo, what's in it, and when to read it — use it instead of
guessing from filenames. reference/PENDING_agent_prompts_resume_2026-08-01.md
holds the detailed per-item agenda, including full re-run prompts for
anything that died mid-flight. Don't reconstruct anything from memory or
chat history — read the files.

TASK #1, before anything else:
  Test that the save system actually worked, then present the checklist,
  progress report and to-do list, then suggest a starting point — in that
  order. Don't pick a workstream first; I deliberately held that choice
  until after the report. Commands are in §2 of START_HERE.md. FIVE
  cold-start passes have been run so far and EVERY ONE found real bugs —
  including one that found four contradictions inside START_HERE.md itself,
  and one that found PROJECT.md stale for the third time in three days.
  Assume this one will too. A pass that finds nothing is a weak test, not a
  clean bill of health. Report what you find before telling me it's fine.

TASK #2, ask me early:
  Is @LacyCrashOuts actually the right handle? The CORE discovery agent
  could not find that account anywhere. The entire project targets it, so
  this is load-bearing — don't guess, don't work around it, ask me. See
  §3b of START_HERE.md.

OPEN CHECKLIST — carry this forward and tick things off:
  [ ] ⚡ Confirm the @LacyCrashOuts handle with me (TASK #2)
  [ ] H1 — RE-RUN, lost to a session limit mid-write. Researches @yoxics,
      @scubaryan_, @coresculture on X. Full prompt preserved in PENDING §H
  [ ] G4/G5/G6 — mine the 3 remaining transcripts. PafYu69s5NA is the
      highest value: it opens describing a clip "found, analyzed, cut, and
      captioned automatically and completely for free with Claude" — this
      project's exact problem statement, already solved by someone else
  [ ] A: Rule 20 retroactive review — 1 of 6 (A2 HF-vision, A3 HF-LLM,
      A4 mining report, A5 78-source audit, A6 the 17 videos)
  [ ] B: 12-item source mining — 1 of 12
  [ ] D: Platform / free-inference / hosting research — not started
  [ ] F: the AI\ folder — PUT OFF, waits on ME. Too big; I'll triage it and
      hand you what matters. Do NOT sweep it unprompted
  [ ] Corroborate the three architecture contradictions before changing
      Stage 3 — they rest on one source so far
  [ ] Run validate_environment.py in Colab — settles the credentials blocker
  [ ] Verify whether the sibling project's video code still runs
  [ ] Answer the 5 open questions in
      reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md
  [ ] Fix chat_downloader's KeyError: 'data' before Stage 1 depends on it
  [ ] Transcript backup is still manual — it was skipped once already
  [ ] Write the first line of actual pipeline code
  [x] C: 6 untranscribed videos — 6 of 6, fetched and verified 2026-08-04
  [x] G1/G2/G3 — the 3 Lacy transcripts mined, saved, indexed
  [x] H2 — CORE discovery, 22 VERIFIED claims with a full source list
  [x] Rule 22 adopted; Rules 8 & 9 dropped (both by me, 2026-08-03)

LAST SESSION (2026-08-04) — what got built:
  - Workstream C closed: all 6 missing transcripts fetched, 6/6, verified
    real. 23 transcripts now on disk, every one carrying its source URL on
    line 2 and timestamped per line, so any quote checks at the exact second
  - G1/G2/G3: the 3 Lacy transcripts mined, one agent per file. ~192KB of
    verbatim reports, 2,650+ timestamp citations between them
  - H2: CORE clipper discovery — 22 VERIFIED / 2 UNVERIFIED, no handle
    invented, every one resolving to a real URL
  - INDEX.md — catalogues all 30+ documents, built after an audit found 12
    of 30 referenced by NOTHING a session actually reads
  - check_links.sh now covers INDEX.md: 51 → 108 links verified
  - PROJECT.md finally records the Stage 3 numbers inline (it had gone
    stale a third time — it knew nothing about that day's work)

NEW THIS SESSION — things found, not yet acted on:
  - STAGE 3 FINALLY HAS REAL NUMBERS, from 50 human-curated moments in
    reference/mining_2026-08-04_cVkFMpDLQrM_VERBATIM.md. That source is a
    best-of, so every segment is a positive example rather than an opinion:
      * clip length median 39.5s, 78% in 20-70s → target 40s, accept
        20-70s, hard floor 11s
      * hook openings: 36% direct question, 22% shouted name/imperative,
        and 0% narration
      * moment types: physical escalation 28%, verbal roast 20%,
        authority 12%, reveal 12%, romance 12%, heist 10%, one-liner 6%
      * A TEXT-ONLY DETECTOR: verbal repetition in 22 of 50 moments (≥3
        repeats of a short phrase within 10s). Needs only the transcript —
        no audio, no model, no API call — so it belongs in the free
        statistical pre-filter, the stage whose whole job is keeping most
        of a VOD away from any paid call. Most useful thing found so far.
  - THREE CORRECTIONS THAT CONTRADICT THE ARCHITECTURE OUTLINE. Flagged,
    deliberately NOT applied — don't change a design off one source:
      1. ~20% of curated moments contain NO shouting at all. The outline
         treats audio-RMS spikes as a primary pre-filter — as written it
         misses one moment in five.
      2. Long silences are POSITIVE (physical gags). A low speech-density
         filter would delete the best set-pieces.
      3. Clip length cannot be derived from caption-cue gaps — those are
         1-2s ASR cadence, not clip boundaries.
  - COMPETITIVE CONTEXT, not a threshold: ~60M monthly views on the #Lacy
    hashtag across 1,598 clippers, growing ~100% month over month. That's
    the field this bot enters, and it matters because the payout model pays
    $0 below a per-post view minimum.
  - G1 is a HOSTILE SECONDARY SOURCE — adversarial narrator who admits
    prior errors. Its claims about people and events are leads, not facts.
    It also states what it cannot answer: no VOD timecodes, no view counts,
    no Clipping.net mechanics anywhere in 2,337 snippets.
  - G3's source is NOT Lacy — third-party commentary that contradicts its
    own thesis: the "meticulous blueprint" claim is undercut at [14:35] by
    Lacy saying there are "no set dedicated things that I'm planning."
  - A session limit killed 3 agents mid-write. Two had already written
    their files and survived intact; only H1 was lost. Committing each
    report on arrival instead of batching is why that cost one report
    instead of three — keep doing that.

ALSO READ: CLAUDE.md — 21 numbered rules, 16 active. Don't just read them,
apply them: they're strict defaults and deviating from one requires asking
me first. The non-negotiables — I have final say on phase transitions and
"complete" (and when I say complete, stamp it "COMPLETE — authorized by
user YYYY-MM-DD"); nothing is factual unless confirmed this session or I
OK'd it; external-AI material (Gemini etc.) is reference only; run every
check BEFORE reporting done, not after I ask; preserve source material
word-for-word; keep raw records separate from evaluation; don't dismiss
free tools — evaluate against all five roles. Read INDEX.md before hunting
for anything, and reference/MASTER_TOOLS_CATALOG_2026-08-02.md (~110 tools
with URLs) before picking any tool for a stage. When I say "save
everything," follow SAVE_PROTOCOL.md exactly — it also carries the written
format for every section of START_HERE.md.

BEFORE STARTING ANYTHING:
  - Confirm the checkpoint held: git log, git status, synced with origin.
    Last known good is ce0c5a7 or later. HEAD one ahead of what
    START_HERE.md's header says is NORMAL; two or more means work landed
    after it was updated (START_HERE.md §0 explains why).
  - Raise the @LacyCrashOuts handle question early — load-bearing, and only
    I can settle it.
  - Confirm I have usage headroom before launching agents. I hit 100% on
    2026-08-04 partway through five of them, and I'm on paid usage now.
  - ONE AGENT PER SOURCE FILE. Single-file agents have succeeded every
    time; broad-scope agents covering many files have died producing
    nothing, twice. Commit each report the moment it lands — never batch.
  - Two unverified leads in START_HERE.md §3 — does the sibling project's
    video code still run, and is validate_environment.py one auth fix from
    passing (one Colab cell settles it). Check those before related build
    work, not after.

CONTEXT I'll forget: budget is a live constraint (metered, hard weekly reset
Monday 1pm, hit repeatedly — I hit 100% again on 2026-08-04 and moved onto
paid usage). Documentation work is not cheap. Drive has no direct access
from your side; you push to GitHub, I pull in Colab, and a fresh Colab
runtime needs drive.mount() before the pull will work. My prompts are logged
verbatim to .claude/session-prompts.log (gitignored — public repo), and raw
transcripts are backed up at AI\claude_transcripts_backup_<date>\ (68MB as
of 08-04); both are the fallback when a curated note is missing or disputed.
Never use `git checkout <file>` to undo an edit — it reverts the whole file
and destroyed real work on 2026-08-03. Still zero pipeline code written —
that's the honest headline; everything so far is restoration, research,
rules, and now the first real detection numbers.
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
