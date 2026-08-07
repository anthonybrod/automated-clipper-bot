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

## §1 — READY TO PASTE (FINAL HANDOFF, regenerated 2026-08-06)

```
FINAL HANDOFF — @CoreCrashOuts automated clipping bot.

READ THESE FIRST, IN THIS ORDER. Do not reconstruct anything from memory or
chat history — the files are the record and they are written to be read cold:
  1. HANDOFF_REPORT_2026-08-06.md — the complete transfer document. 13 parts:
     scope, architecture, every measured number, open questions, where the
     evidence contradicts the plan, repo map, workstream status, the save
     system, unverified findings, and an honest accounting of cost and waste.
     START HERE IF YOU ARE NEW.
  2. START_HERE.md — session entry point. §0 self-validates; run it.
  3. INDEX.md — catalogue of every document, what's in it, when to read it.
     Use it instead of guessing from filenames.
  4. CLAUDE.md — 21 numbered rules, 16 active. Strict defaults.
  5. reference/PENDING_agent_prompts_resume_2026-08-01.md — the live agenda,
     workstreams A-K, with the exact agent prompts to reuse. Never re-derive
     a prompt that is already written there.
All paths are relative to C:\Users\AwBro\Desktop\automated clipper bot

TASK #1, before anything else:
  Run: bash save_check.sh
  It is the GATE — 12 mechanical checks. Non-zero exit means the last save
  was NOT complete; fix what it names before trusting anything. Then present
  the checklist, progress report and to-do list, then SUGGEST a starting
  point. Do not pick a workstream — I hold that choice until after the
  report. SEVEN cold-start passes have run and EVERY ONE found real bugs.
  Assume this one will too; a pass that finds nothing is a weak test, not a
  clean bill of health. Report what you find BEFORE telling me it's fine.

TASK #2, the highest-priority open item — a PRIVACY issue in ANOTHER repo:
  Workstream K1. An unverified finding says the user-level UserPromptSubmit
  hook fires in EVERY project and its directive names a bare relative path,
  while C:\Users\AwBro\Desktop\youtube auto videos does NOT gitignore
  .claude/ (it ignores only .claude/settings.local.json) and has a public
  GitHub remote. Verify with:
    cd "C:\Users\AwBro\Desktop\youtube auto videos"
    git check-ignore -v .claude/session-state.md; echo "exit=$?"
  exit=1 means NOT ignored. If confirmed, the one-line containment fix is
  adding `.claude/` to that repo's .gitignore. Ask me before changing
  anything in that repo. Full detail: PENDING §K.

=== THE PROJECT ===

An automated Twitch clipping bot on a $0 open-source stack. It watches a
stream, detects clip-worthy moments statistically rather than by watching
everything, transcribes and captions locally with faster-whisper and ffmpeg,
cuts to format, and posts to my channels — with a human approval gate, not
unsupervised.

MONEY: Clipping.net-style bounties, paid per 1,000 views with a MINIMUM VIEW
THRESHOLD per post. A clip under the minimum pays $0. That single fact drives
everything: it is why hook quality is load-bearing rather than cosmetic, why
selection matters more than volume, and why every recurring API cost eats the
margin directly. Payouts run roughly $0.50-$3.00 per 1,000 views.

THE 6 STAGES (full reasoning in PROJECT.md's Architecture Outline):
  1 Ingestion      yt-dlp; chat via Twitch GQL (keyless) or chat-downloader
                   ✅ PROVEN WORKING. Chat path has a known crash (below).
  2 Transcription  faster-whisper, local, word-level timestamps
  3 Detection      THREE-STAGE FUNNEL: free statistical pre-filter → cheap
                   LLM score → expensive LLM detail on top-N only. The funnel
                   IS the cost control — it keeps most of a VOD away from any
                   paid call.
  4 Assembly       ffmpeg — cut, crop, caption. THREE ASSUMPTIONS HERE ARE
                   CONTRADICTED BY REAL DATA (see CONTRADICTIONS below).
  5 Distribution   human approval gate; platform list deliberately OPEN
  6 Orchestration  LangGraph + AsyncSqliteSaver; port the proven retry /
                   dead-letter / budget machinery from the sibling project

THE SINGLE MOST IMPORTANT TECHNIQUE FOUND IN ALL RESEARCH:
  snap_clip_to_words() — LLMs are unreliable at millisecond arithmetic, so
  proposed cut points get snapped onto REAL word-boundary timestamps from the
  transcript (~0.35s lead / 0.45s tail padding into silence) before anything
  is cut. Every other source assumed raw LLM timestamps were safe. They are
  not. Source: reference/deep_dive_openshorts.md

KNOWN REAL DEFECT, UNFIXED: chat_downloader's Twitch GraphQL path throws a
reproducible KeyError: 'data'. Needs defensive .get() chaining plus retry
backoff before Stage 1 depends on chat.

=== SOURCES AND DESTINATIONS (confirmed 2026-08-06) ===

IN — Twitch, PRIMARY for V1, all verified reachable by yt-dlp, no auth:
    https://www.twitch.tv/lacy/
    https://www.twitch.tv/lacy/videos
    https://www.twitch.tv/lacy/clips?range=24hr
    https://www.twitch.tv/lacy/clips?range=7d      <- 964 clips pulled here
IN — Kick, secondary, nearly empty. DO NOT PULL without asking:
    https://kick.com/lacy   ·   https://kick.com/lacy/videos
    https://kick.com/lacy/clips?sort=date&range=week
    https://kick.com/lacy/clips?sort=view&range=week
    (note: Kick exposes sort=view, which Twitch does not surface as cleanly)
OUT — my own channels, so Stage 5 auth is straightforward:
    https://x.com/CoreCrashOuts
    https://www.youtube.com/@CORECrashOUTS
    (verified: UCtHsW7-LqxK5mUiQcxAxqRg, public, 2 followers, ZERO videos)

@LacyCrashOuts was ALWAYS the output channel; it is now @CoreCrashOuts. Some
older docs wrongly call it a "target streamer" — it never was. Raw records
keep the old name deliberately (Rule 16) and carry correction banners.

SCOPE: V1 = Lacy only, to prove the pipeline end to end.
       V2 = the whole CORE group, after V1 is a working proof of concept.

=== THE DATA — everything measured, with its caveats ===

A) 964 REAL TWITCH CLIPS, 7 days (research/twitch_clips/, 2026-08-06)
   Duration: median 30s, mean 35.5s, p25 29s, p75 49s, range 4-60s.
   ⚠️ 71% sit at EXACTLY 30/59/29s — those are Twitch's clip-tool UI presets.
   Twitch durations measure THE TOOL, not the moment. Do not derive a target
   length from them.
   Views: median 5. Mean 35. Max 7,073. All 964 together = 33,624.
     >=5,000 views: 1 clip (0.1%)   >=1,000: 6 (0.6%)   >=100: 34 (3.5%)
   Top ÷ median ≈ 1,400x.
   ⚠️ NOT a payout prediction — Twitch views are a different audience from
   reposted X/Shorts. What it establishes: SELECTION is where all the value
   is. An average moment earns nothing.

B) 25 REAL REPOSTS ON X (reference/research_2026-08-06_core_clippers_named_
   VERBATIM.md, 2026-08-06). Accounts: @yoxics, @scubaryan_, @coresculture.
   ACCESS METHOD WORTH KEEPING: x.com and Nitter are gated, but
   api.fxtwitter.com serves public JSON UNAUTHENTICATED — verbatim captions,
   views, likes, reposts, exact duration and pixel dimensions.
   LENGTH — the decisive answer: median 51.4s, 44% cluster at 55-61s, and
   0 OF 18 land on Twitch's presets. Durations are irregular decimals
   (38.483, 45.616, 57.416) => these accounts HAND-TRIM.
   => TARGET ~55-60s, NOT 30s.
   FORMAT, from frames actually viewed: 16:9 landscape dominates, NOTHING is
   9:16. NO added subtitles. Chat left BURNED IN, not blurred. No watermark.
   ZERO hashtags across all 25 captions; captions state the payoff rather
   than teasing it.
   SCALE: @coresculture 6,540 followers, median 7,017 views on sampled posts.
   ⚠️ Sample came from search, which favours winners — medians are
   overestimates. The agent flagged this itself.

C) 50 HUMAN-CURATED MOMENTS (reference/mining_2026-08-04_cVkFMpDLQrM_
   VERBATIM.md). Weight: the source is a curated best-of, so a human editor
   already decided what was worth keeping — every segment is a positive
   example, not an opinion.
   Moment types: physical escalation 28% · verbal roast 20% · authority 12% ·
   quiet reveal 12% · romance/social-stakes 12% · heist 10% · one-liner 6%.
   Hook openings: 36% direct question · 22% shouted name/imperative ·
   0% narration. 21 of 50 open with Hey/Yo/Wait/Okay/All right.
   ⭐ THE BEST FIND — A TEXT-ONLY DETECTOR: verbal repetition in 22 of 50
   moments (FOCUS x10, Come on x12, WAIT x8, bully x7). Rule: >=3 repeats of
   a short phrase within 10s. It needs ONLY the transcript — no audio, no
   model, no API call — so it drops straight into the free pre-filter.
   CORROBORATION: G2 proposed a 20-70s band from editorial judgement; 89%
   (862/964) of real Twitch clips fall inside it. Two independent methods,
   same range. Build on the BAND, not on a single target.

D) COMPETITIVE CONTEXT: ~60M monthly views on #Lacy across 1,598 clippers,
   growing ~100% month over month. Context, not a threshold — but 1,598
   competitors chasing the same moments is exactly the condition that
   produces sub-threshold posts.

=== ⚠️ WHERE THE EVIDENCE CONTRADICTS THE PLAN ===
ALL FLAGGED, NONE APPLIED. Changing a design off one source is forbidden here.

From the X repost data:
  1. Outline says 9:16 vertical split-screen with facecam over gameplay.
     Reality: 16:9 landscape dominates; nothing is 9:16.
  2. Outline says karaoke captions. Reality: NO added subtitles anywhere.
  3. Outline says chat boxblur for TOS safety. Reality: chat burned in.
  4. Recorded campaign rules say a #lacy hashtag is MANDATORY. Reality: zero
     hashtags in 25 successful posts. Either the rules are stale or these
     accounts don't operate under them. UNRESOLVED.
From the curated-moments data:
  5. Outline treats audio-RMS spikes as a PRIMARY pre-filter. Reality: ~20%
     of curated moments contain NO shouting — misses 1 in 5.
  6. Long silences are POSITIVE (physical gags). A low speech-density filter
     would delete the best set-pieces.
  7. Clip length cannot be derived from caption-cue gaps (1-2s ASR cadence).
Corroborate against a second source before rewriting Stage 3 or 4. G4-G6 and
workstream A are the natural check.

=== OPEN CHECKLIST ===
  [ ] ⚡ K1 — PRIVACY, sibling repo. Verify first (TASK #2). K2-K8 after.
  [ ] ⚡ J1 — BUILD THE DETECTOR EVAL HARNESS. Clips carry view counts and
      point back into VODs, so a detector can be scored on whether it picks
      the moments that actually earned views. NOTHING in this project can
      currently measure detector quality AT ALL. Highest-value item.
  [ ] G4 — mine PafYu69s5NA (transcript already on disk). It opens describing
      a clip "found, analyzed, cut, and captioned automatically and
      completely for free with Claude." Someone solved this exact problem and
      left a walkthrough. One agent, one file.
  [ ] G5/G6 — mine mFOoNPFylLI and QqwNue_KL-4
  [ ] J2 — cross-reference clip titles against the moment taxonomy
  [ ] J3 — pull the 24hr clip window, compare to the 7d distribution
  [ ] J4 — fix the Stage 3 length default: ~55-60s, NOT 30s
  [ ] J5 — re-check Kick before V2
  [ ] J6 — re-examine the payout maths against the real view distribution
  [ ] Resolve the 7 contradictions above
  [ ] A: Rule 20 retroactive review — 1 of 6
  [ ] B: 12-item source mining — 1 of 12
  [ ] D: Platform / free-inference / hosting research — not started
  [ ] F: the AI\ folder — PUT OFF, waits on ME. Too big; I triage it and hand
      you what matters. DO NOT sweep it unprompted.
  [ ] Run validate_environment.py in Colab — settles the credentials blocker
  [ ] Fix chat_downloader's KeyError: 'data' before Stage 1 depends on chat
  [ ] Verify whether the sibling project's video code still runs
  [ ] Answer the 5 questions in reference/DISCUSS_next_phase_autonomy_
      prompt_2026-08-02.md
  [ ] WRITE THE FIRST LINE OF ACTUAL PIPELINE CODE
  [x] Stage 1 source confirmed and PROVEN WORKING
  [x] C: 6 transcripts fetched · G1/G2/G3 mined · H1 and H2 both done
  [x] All docs corrected to the real links; raw records preserved
  [x] Rule 22 adopted; Rules 8 & 9 dropped; save_check.sh gates the save

=== ⚠️ UNVERIFIED: 8 FINDINGS AGAINST THE SAVE SYSTEM ===
An adversarial workflow ran 2026-08-06. 14 of 15 agents died on a session
limit; ONE survived and produced 8 findings. EVERY skeptic assigned to refute
them also died, so NOTHING was verified. Rule 12 applies fully — these are
LEADS, not facts. Verbatim: reference/research_2026-08-06_save_system_
attack_VERBATIM.md. Summary: HANDOFF_REPORT Part 11. Agenda: PENDING §K.
  K1 CRITICAL  privacy leak into the sibling repo (TASK #2)
  K2 CRITICAL  the live-handoff stopped tracking inside its own build session
  K3 HIGH      tail -40 drops 74% of session-state.md and cuts mid-entry
  K4 HIGH      tail -40 is a LINE bound not a BYTE bound — a sandbox test
               produced 801 KB of context injection (~200K tokens)
  K5 HIGH      nothing on the save path ever READS session-state.md
  K6 MEDIUM    hooks_backup/ lacks settings.json — the only thing registering
               the hooks. Restoring it yields inert scripts that fail silently
  K7 MEDIUM    save_check check 7 greps only BROKEN, but check_links reports a
               missing file as "MISSING DOC:" — deleting a doc still PASSES
  K8 MEDIUM    both context-injecting hooks are unscoped across all projects

=== THE METHOD — HOW THIS PROJECT IS BUILT, AND WHY ===
This is the owner's governing approach. It is not a phase we are stuck in; it
is deliberate, and a fresh model that ignores it will rebuild the project
wrongly.

1. RESEARCH NEW TECH FIRST, THEN APPLY IT, THEN CODE.
   Owner's words: "we stay in research till i say to move on im the overall
   director here" and "we dont know the best service and model cuz we are in
   the research stage."
   The order is: find what exists -> verify it is real -> evaluate it against
   the five roles (Rule 20) -> only then write code that uses it. Writing
   code before knowing the best available tool means writing it twice, and
   the second write is against a codebase that already assumed the wrong
   tool.
   Concretely, this is why there is a ~110-tool catalogue with verification
   status, why every tool claim is independently checked against GitHub/PyPI,
   and why 964 real clips were measured before a single detection threshold
   was written down. The Stage 3 numbers exist BECAUSE research came first.
   DO NOT propose "let's just start coding and fix it later." That has been
   considered and rejected by the owner.

2. THE PHASE TRANSITION IS THE OWNER'S CALL, NOT YOURS (Rule 10).
   Research -> build is a transition. You may recommend it. You may not
   declare it. Same for calling anything "complete."

3. UPSCALING PATH — build small, prove it, then widen.
   V1  ONE source (twitch.tv/lacy), ONE destination pair, prove the pipeline
       end to end. Owner: "we will start with lacys clips only then scale up
       once the project works and is poc."
   V2  The whole CORE group. Multiple streamers, same pipeline. The
       architecture already supports a multi-creator config; only Lacy is
       scoped today.
   V3+ More platforms in and out. Kick is the known second INPUT (empty
       today, re-check before V2). Stage 5 outputs stay a LIST behind ONE
       interface so adding an outlet is config, not code - that shape exists
       specifically because Facebook was lost mid-project and a hard-coded
       Stage 5 would have needed a rewrite.
   The scaling constraint is NOT technical, it is economic: 1,598 clippers
   already compete for the same moments, and posts under the view minimum pay
   $0. Widening scope multiplies cost immediately and revenue only if
   selection quality holds.

4. CHECKS AND BALANCES — the layered system, and what each layer catches.
   Nothing here is decoration; every layer exists because a specific failure
   happened.
   a) HUMAN APPROVAL GATE in the pipeline. The bot never posts unsupervised.
   b) FAIL-CLOSED on AI judgement calls. Any exception or unparseable
      response from a hook-quality score, TOS/content check, or Ollama
      context-check = REJECT, never a silent pass. Explicitly NOT extended to
      pre-flight checks or human-gate timeouts, which keep their own logic.
   c) VERIFY BEFORE TRUSTING (Rule 12). Nothing is factual unless confirmed
      this session or the owner OK'd it. Four hallucinated GitHub repo
      attributions were caught this way; so was a fabricated dossier.
   d) RAW AND EVALUATION SEPARATED (Rules 15/16). Source material is saved
      word-for-word in its own file and NEVER edited to reflect a later
      finding. Three files were once "saved" as condensed paraphrases and had
      to be replaced with the originals.
   e) save_check.sh - 12 mechanical checks GATING the save. Non-zero exit
      means the save is not done. It has caught real staleness every session
      since it existed, including its own false-alarm bug.
   f) check_links.sh - link rot across 119 links.
   g) COLD-START TESTING. Seven passes so far, every one found real bugs.
      A pass that finds nothing is a weak test, not a clean bill of health.
   h) ONE AGENT PER SOURCE FILE + commit on arrival. Bounds the blast radius
      when a session limit hits mid-run.
   The through-line: prefer a MECHANICAL check over a remembered one. A
   protocol that depends on remembering fails the same way a file nothing
   points at does.

=== THE RULES — apply them, don't just read them ===
CLAUDE.md holds 21 numbered rules, 16 active. Each exists because a specific
failure happened. Strict defaults; deviating from one requires asking me
first. The load-bearing ones:
  Rule 1   PORT, DON'T RE-DERIVE. Check SALVAGE_INVENTORY.md and the sibling
           pipeline.py before writing ANY new function. Three days were lost
           building a save system from scratch when a working implementation
           had already been pointed out.
  Rule 10  I decide what is "complete." Never self-stamp. When I authorize
           it, mark it "COMPLETE — authorized by user YYYY-MM-DD".
  Rule 12  Verified means checked THIS session. File existence is not content
           verification. Past notes, other AI output, and your own earlier
           conclusions are leads to verify, not facts to build on.
  Rule 14  No rule is adopted without my explicit confirmation.
  Rule 15  Source material word-for-word. NEVER condense, summarize, or
           placeholder. Applies to agent reports too.
  Rule 16  Raw records and evaluation live in SEPARATE files. NEVER rewrite a
           raw record to reflect a later finding.
  Rule 20  Evaluate every tool against five roles — primary / fail-safe /
           cross-check / assist / feature. Never dismiss a working free tool.
  Rule 21  Run EVERY check BEFORE reporting, not after I ask.
  Rule 22  Updating START_HERE.md is the LAST action of every session, before
           the final push, even when a usage limit is cutting things short.
Removed at my direction: Rules 2, 4, 6 (08-01); Rules 8, 9 (08-03 — they were
Gemini-sourced and adopted without authorization; that, not their technical
merit, is why they went).

=== BEFORE STARTING ANYTHING ===
  - Confirm the checkpoint: git log, git status, synced with origin.
    Last known good is f074a33 or later. HEAD one ahead of START_HERE.md's
    header is NORMAL and documented; two or more means work landed after it
    was updated (§0 explains why).
  - CONFIRM MY USAGE HEADROOM BEFORE LAUNCHING AGENTS. I hit 100% on 08-04
    and again on 08-06. I am on paid usage. TELL ME THE COST BEFORE launching
    a workflow — the 08-06 one took the session from 49% to 82% in one run,
    spent ~518K subagent tokens, and returned 1 of 15 agents' output because
    the rest died on the limit.
  - ONE AGENT PER SOURCE FILE. Single-file agents have succeeded every time;
    broad-scope agents covering many files have died producing nothing, twice.
  - COMMIT EACH AGENT REPORT THE MOMENT IT LANDS — never batch. On 08-04 a
    session limit killed 3 agents mid-write; that practice cost one report
    instead of three.
  - Read INDEX.md before hunting for anything, and
    reference/MASTER_TOOLS_CATALOG_2026-08-02.md (~110 tools with URLs, each
    with a verification status and a five-role classification) before picking
    any tool for a stage.
  - When I say "save everything": follow SAVE_PROTOCOL.md exactly AND run
    save_check.sh. Non-zero exit means the save is NOT done and you do not
    report it as done.

=== CONTEXT I'LL FORGET ===
  - Budget is a live constraint: metered, hard weekly reset Monday 1pm, hit
    repeatedly, and I am on paid usage now. Documentation work is not cheap.
  - Drive: you cannot write to it. You push to GitHub, I pull in Colab. A
    fresh Colab runtime needs drive.mount() before any git pull will work.
    Folder: /content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt
  - THIS IS A PUBLIC REPO. .claude/ holds my raw prompts
    (session-prompts.log) and durable facts (session-state.md) and is
    gitignored. Never commit it. See K1.
  - Raw transcripts back up to AI\claude_transcripts_backup_<date>\ (~68MB).
  - NEVER use `git checkout <file>` to undo an edit — it reverts the WHOLE
    file and destroyed real work on 08-03. Use sed, or commit first.
  - Real Python is C:\Users\AwBro\AppData\Local\Programs\Python\Python312\
    python.exe — "python" and "py" do NOT resolve (Windows Store stub).
  - Windows Python cannot see git-bash's /tmp. Use a shared absolute path.
  - I was BANNED ON FACEBOOK for failing a bot check; Instagram is pending.
    Stage 5 stays platform-agnostic — publish targets behind ONE interface,
    config not code, so adding or dropping an outlet is not a rewrite.
  - STILL ZERO PIPELINE CODE. That is the honest headline. Everything so far
    is restoration, research, rules, and — as of 08-06 — the first real
    detection data. The fastest path to a working bot is G4, then J1, then
    the first real Stage 1→2 code using the proven yt-dlp path.
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
