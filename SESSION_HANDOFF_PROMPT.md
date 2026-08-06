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

## §1 — READY TO PASTE (regenerated 2026-08-06)

```
just to catch you up: Read START_HERE.md in the automated clipper bot repo
first (C:\Users\AwBro\Desktop\automated clipper bot). It's the single
session entry point and it opens with §0 — a self-validation checklist. Run
those checks before trusting anything in it. INDEX.md catalogues every
document in the repo, what's in it, and when to read it — use it instead of
guessing from filenames. reference/PENDING_agent_prompts_resume_2026-08-01.md
holds the detailed per-item agenda including full re-run prompts for
anything that died mid-flight. Don't reconstruct anything from memory or
chat history — read the files.

TASK #1, before anything else:
  Run save_check.sh. It is the GATE — 12 mechanical checks, and if it exits
  non-zero the last save was NOT complete. Then present the checklist,
  progress report and to-do list, then suggest a starting point — in that
  order. Don't pick a workstream first; I hold that choice until after the
  report. SEVEN cold-start passes have been run so far and EVERY ONE found
  real bugs. Assume this one will too. A pass that finds nothing is a weak
  test, not a clean bill of health. Report what you find BEFORE telling me
  it's fine.

TASK #2, check these two first — they were in flight when the session ended:
  a) An H1 agent researching @yoxics / @scubaryan_ / @coresculture on X,
     writing to reference/research_2026-08-06_core_clippers_named_VERBATIM.md
  b) An adversarial workflow attacking the save system (5 attack agents +
     per-finding skeptics + synthesis).
  Check whether either produced output. If a file exists, COMMIT IT
  IMMEDIATELY — do not batch. If they produced nothing, say so plainly;
  don't invent their findings. H1's prompt is preserved in PENDING §H.

THE PROJECT, IN ONE PARAGRAPH: an automated Twitch clipping bot on a $0
open-source stack. It watches a stream, detects the best moments
statistically rather than by watching everything, transcribes and captions
locally with faster-whisper and ffmpeg, cuts to vertical, and posts — with a
human approval gate. Money comes from Clipping.net-style bounties: paid per
1,000 views with a MINIMUM VIEW THRESHOLD per post, so a clip under the
minimum pays $0. That is why hook quality is load-bearing and why every
recurring API cost eats the margin directly.

SOURCES AND DESTINATIONS (confirmed 2026-08-06 — this was corrected, older
docs use the old name):
  IN  — Twitch, PRIMARY for V1:
        https://www.twitch.tv/lacy/
        https://www.twitch.tv/lacy/videos
        https://www.twitch.tv/lacy/clips?range=24hr
        https://www.twitch.tv/lacy/clips?range=7d
  IN  — Kick, secondary and nearly empty, DO NOT PULL without asking:
        https://kick.com/lacy · /videos
        https://kick.com/lacy/clips?sort=date&range=week
        https://kick.com/lacy/clips?sort=view&range=week
  OUT — my own channels:
        https://x.com/CoreCrashOuts
        https://www.youtube.com/@CORECrashOUTS
  @LacyCrashOuts was ALWAYS the output channel; it is now @CoreCrashOuts.
  That is the whole change. Scope: V1 = Lacy only to prove the pipeline,
  V2 = the whole CORE group.

OPEN CHECKLIST — carry this forward and tick things off:
  [ ] H1 — check if it landed; commit immediately if so
  [ ] The save-system workflow — check if it landed; act on confirmed bugs
  [ ] J1 — build the detector EVAL HARNESS. Twitch clips carry view counts
      and point back into VODs, so a detector can be scored on whether it
      picks the moments that actually earned views. NOTHING in this project
      can currently measure detector quality at all. Highest-value item.
  [ ] J2 — cross-reference clip titles against G2's moment taxonomy
  [ ] J3 — pull the 24hr clip window, compare against the 7d distribution
  [ ] J4 — fix the Stage 3 length default (see NEW THIS SESSION)
  [ ] J5 — re-check Kick before V2
  [ ] J6 — re-examine the payout maths against the real view distribution
  [ ] G4/G5/G6 — mine the 3 remaining transcripts. PafYu69s5NA is highest
      value: it opens describing a clip "found, analyzed, cut, and captioned
      automatically and completely for free with Claude"
  [ ] A: Rule 20 retroactive review — 1 of 6
  [ ] B: 12-item source mining — 1 of 12
  [ ] D: Platform / free-inference / hosting research — not started
  [ ] F: the AI\ folder — PUT OFF, waits on ME. Too big; I'll triage it and
      hand you what matters. Do NOT sweep it unprompted
  [ ] Run validate_environment.py in Colab — settles the credentials blocker
  [ ] Fix chat_downloader's KeyError: 'data' before Stage 1 depends on it
  [ ] Answer the 5 open questions in
      reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md
  [ ] Write the first line of actual pipeline code
  [x] Stage 1 source CONFIRMED AND PROVEN WORKING (2026-08-06)
  [x] C: 6 transcripts fetched and verified · G1/G2/G3 mined · H2 done
  [x] All docs corrected to the real links; raw records preserved
  [x] Rule 22 adopted; Rules 8 & 9 dropped; save_check.sh gates the save

LAST SESSION (2026-08-06) — what got built:
  - STAGE 1 IS PROVEN, not theoretical. yt-dlp reaches twitch.tv/lacy's VODs
    AND clips with NO auth and NO API key. Real output: VOD titles and
    durations (one 10,003s stream), plus 964 clips.
  - Pulled 964 real Lacy clips from the last 7 days with durations, view
    counts and titles. Saved raw to research/twitch_clips/ plus a written
    analysis. This is the ONLY ground truth in the repo — every other source
    is somebody talking about clipping; this is 964 moments real humans chose
    to clip and what each one earned. It is free and refreshes daily.
  - Corrected @LacyCrashOuts → the real links across all 9 live docs (17
    mentions). Raw records and verbatim agent reports were NOT edited
    (Rule 16) — 54 mentions preserved, each file given a correction banner.
  - Ported the live-handoff mechanism from Sonovore/claude-code-handoff
    instead of continuing to re-derive one. UserPromptSubmit now injects a
    directive on every message to append durable facts to
    .claude/session-state.md immediately; SessionStart reads it back.
  - Backed up all 4 hooks + the user-level CLAUDE.md into hooks_backup/ —
    they live in ~/.claude/ and were entirely outside version control.
  - Fixed save_check.sh: it hardcoded "today" and threw 3 false alarms on a
    good save at the start of a fresh session.

NEW THIS SESSION — findings, not yet acted on:
  - THE VIEW DISTRIBUTION IS BRUTAL AND IT QUESTIONS THE BUSINESS CASE.
    Across 964 community-clipped Lacy moments: median 5 views, mean 35, only
    6 clips (0.6%) reached 1,000 views, exactly 1 reached 5,000, and all 964
    together total 33,624 views. Top clip ÷ median = ~1,400x.
    CAVEAT, state it every time: Twitch clip views are a DIFFERENT audience
    from reposted Shorts/X, so this is not a payout prediction. What it does
    establish is that SELECTION is where all the value is — an average
    moment earns nothing — and that most posts would land under a per-post
    view minimum. J6 exists to work this through properly.
  - CLIP LENGTH: Twitch data CANNOT give a target length. Median is 30s but
    71% of clips sit at exactly 30/59/29s — those are Twitch's clip-tool UI
    presets, so the number measures a slider, not a moment. What DOES hold:
    G2's acceptance band of 20-70s, corroborated at 89% (862/964) by a
    completely different method. Build on the band, not on a target.
  - G2 remains the best detection source: 50 human-curated moments giving
    hook openings (36% direct question, 22% shouted name, 0% narration),
    seven moment types, and a TEXT-ONLY detector — verbal repetition in 22 of
    50 moments, ≥3 repeats of a short phrase within 10s. It needs only the
    transcript: no audio, no model, no API call. It belongs in the free
    statistical pre-filter.
  - THREE CORRECTIONS THAT CONTRADICT THE ARCHITECTURE OUTLINE, flagged and
    deliberately NOT applied — don't change a design off one source:
      1. ~20% of curated moments contain NO shouting. The outline treats
         audio-RMS spikes as a primary pre-filter; as written it misses one
         moment in five.
      2. Long silences are POSITIVE (physical gags). A low speech-density
         filter would delete the best set-pieces.
      3. Clip length cannot be derived from caption-cue gaps (1-2s ASR
         cadence, not clip boundaries).
  - I was BANNED ON FACEBOOK for failing a bot check, Instagram pending. Two
    of four originally planned Stage 5 outlets are gone or at risk. Stage 5
    stays platform-agnostic — a list of publish targets behind one interface,
    config not code. Which platforms is still workstream D research.

ALSO READ: CLAUDE.md — 21 numbered rules, 16 active. Don't just read them,
apply them: they're strict defaults and deviating from one requires asking me
first. The non-negotiables — I have final say on phase transitions and
"complete" (when I say complete, stamp it "COMPLETE — authorized by user
YYYY-MM-DD"); nothing is factual unless confirmed this session or I OK'd it;
external-AI material is reference only; run every check BEFORE reporting
done, not after I ask; preserve source material word-for-word; keep raw
records separate from evaluation and NEVER rewrite a raw record to reflect a
later finding (Rule 16); don't dismiss free tools — evaluate against all five
roles. Read INDEX.md before hunting for anything, and
reference/MASTER_TOOLS_CATALOG_2026-08-02.md (~110 tools with URLs) before
picking any tool for a stage. When I say "save everything," follow
SAVE_PROTOCOL.md exactly AND run save_check.sh — if it exits non-zero the
save is not done and you don't report it as done.

BEFORE STARTING ANYTHING:
  - Confirm the checkpoint held: git log, git status, synced with origin.
    Last known good is 638c8b3 or later. HEAD one ahead of what
    START_HERE.md's header says is NORMAL; two or more means work landed
    after it was updated (§0 explains why).
  - Confirm I have usage headroom before launching agents. I hit 100% on
    08-04 and 82% on 08-06, and I'm on paid usage now. TELL ME THE COST
    BEFORE launching a workflow — the 08-06 adversarial workflow took the
    session from 49% to 82% in one go and that was for testing
    infrastructure, not project progress.
  - ONE AGENT PER SOURCE FILE. Single-file agents have succeeded every time;
    broad-scope agents covering many files have died producing nothing,
    twice. COMMIT EACH REPORT THE MOMENT IT LANDS — never batch. On 08-04 a
    session limit killed 3 agents mid-write and that practice cost one report
    instead of three.
  - Two unverified leads in START_HERE.md §3 — does the sibling project's
    video code still run, and is validate_environment.py one auth fix from
    passing (one Colab cell settles it). Check before related build work.
  - PORT, DON'T RE-DERIVE (Rule 1). Check SALVAGE_INVENTORY.md and the
    sibling project's pipeline.py before writing any new function. Three days
    were lost building a save system from scratch when a working
    implementation had already been pointed out.

CONTEXT I'll forget: budget is a live constraint — metered, hard weekly reset
Monday 1pm, hit repeatedly, and I'm on paid usage now. Documentation work is
not cheap. Drive has no direct access from your side; you push to GitHub, I
pull in Colab, and a fresh Colab runtime needs drive.mount() before the pull
will work. My prompts are logged verbatim to .claude/session-prompts.log and
durable facts go to .claude/session-state.md — both gitignored, because this
is a PUBLIC repo and they contain raw prompts. Raw transcripts are backed up
at AI\claude_transcripts_backup_<date>\ (68MB). Never use
`git checkout <file>` to undo an edit — it reverts the whole file and
destroyed real work on 08-03. The real Python is at
C:\Users\AwBro\AppData\Local\Programs\Python\Python312\python.exe — "python"
and "py" do NOT resolve. Still zero pipeline code written — that's the honest
headline; everything so far is restoration, research, rules, and now the
first real detection data.
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
