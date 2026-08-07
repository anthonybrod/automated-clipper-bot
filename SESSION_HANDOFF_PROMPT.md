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

## §1 — READY TO PASTE (FINAL HANDOFF, regenerated 2026-08-07)

```
FINAL HANDOFF — @CoreCrashOuts automated clipping bot.
Repo: C:\Users\AwBro\Desktop\automated clipper bot
GitHub: github.com/anthonybrod/automated-clipper-bot (master)

═══ READ IN THIS ORDER. Do not reconstruct from memory or chat history ═══
  1. HANDOFF_REPORT_2026-08-06.md — the full transfer document, 13 parts.
     START HERE IF YOU ARE NEW. Scope, architecture, every measured number
     with its caveats, open questions, where evidence contradicts the plan,
     and an honest accounting of what went wrong.
  2. START_HERE.md — session entry point. §0 SELF-VALIDATES; run it before
     trusting anything in it.
  3. THE THREE INDEXES — different questions, all three needed:
       FILE_MAP.md   WHERE is it?  Every folder and file, real sizes, which
                     files may NEVER be edited, what lives outside the repo,
                     and a "where do I find…?" lookup table.
       INDEX.md      WHEN do I read it? Purpose and reading order, ~35 docs.
       HANDOFF_REPORT WHAT does it mean? Findings and status.
  4. CLAUDE.md — 21 numbered rules, 16 active. Strict defaults.
  5. reference/PENDING_agent_prompts_resume_2026-08-01.md — the live agenda,
     workstreams A–K, 1,037 lines, with FULL REUSABLE AGENT PROMPTS.

TASK #1 — before anything else:
  bash save_check.sh
  It is the GATE: 11 mechanical checks. Non-zero exit means the last save was
  NOT complete — fix what it names before trusting anything. Then present the
  checklist, progress report and to-do list, then SUGGEST a starting point.
  DO NOT pick a workstream; that is mine (Rule 10).
  TEN cold-start/audit passes have run and EVERY ONE found real bugs — the
  last three found 50 between them, including data loss and a dependency file
  that covered none of the project's tools. Assume this one will too. A pass
  that finds nothing is a weak test, not a clean bill of health. Report what
  you find BEFORE telling me it's fine.

TASK #2 — the blocking question, ask me early:
  Workstream K1, a CONFIRMED privacy issue in a DIFFERENT repo. The
  user-level UserPromptSubmit hook fires in EVERY project and its directive
  names a bare relative path, while C:\Users\AwBro\Desktop\youtube auto videos
  does NOT gitignore .claude/ and has a public GitHub remote. Verify:
     cd "C:\Users\AwBro\Desktop\youtube auto videos"
     git check-ignore -v .claude/session-state.md ; echo "exit=$?"
  exit=1 means NOT ignored. Containment is one line — add `.claude/` to that
  repo's .gitignore. ASK ME BEFORE TOUCHING THAT REPO.

TASK #3 — verify before building on any of it:
  Workstream K's other 7 findings are UNVERIFIED. Every skeptic assigned to
  refute them died on a session limit. Rule 12: leads, not facts. Full
  verbatim in reference/research_2026-08-06_save_system_attack_VERBATIM.md,
  reproduce-commands in PENDING §K.

═══ THE GOAL — MY WORDS, VERBATIM. THIS IS THE NORTH STAR ═══
"A mostly fully auto mated social media clipping bot that is free and that
cross posts and checks its analytics and corrects to align with the most
profitable algorithms per platform. It produces top quality the best it can
be it and then it constantly ups the quality out of intern into top talent
professional industry titans level work that would make real life coders and
his peers jealous contaning no ai slop and checks and balances with
failsafe's built along the way."

READ WHAT THAT ACTUALLY DEMANDS — it is more than the 6 stages describe:
  1. MOSTLY fully automated — not fully. The human approval gate stays.
  2. FREE — $0 stack. Every recurring cost is a defect, not a tradeoff.
  3. CROSS-POSTS — multi-platform is core, not a later nice-to-have.
  4. ⚠️ CHECKS ITS OWN ANALYTICS AND SELF-CORRECTS toward the most
     profitable algorithm PER PLATFORM. THIS IS A 7TH STAGE AND IT IS NOT
     IN THE ARCHITECTURE OUTLINE. Nothing in this repo currently reads back
     post performance, and nothing feeds it into the next decision. Per
     platform matters: what wins on Shorts is not what wins on X. This is
     the single largest gap between the documented design and the stated
     goal. J1 (the eval harness) is the first half of it — scoring the
     detector against real view counts — but the closed loop, where
     published results change future selection, does not exist even on paper.
  5. QUALITY THAT COMPOUNDS — "out of intern into top talent professional
     industry titans level." The bar rises over time; a working V1 is a
     floor, not a finish line.
  6. NO AI SLOP — generic, obviously-machine output is a failure even if it
     runs. This is why the research measured REAL successful clips rather
     than accepting generic "make a good hook" advice.
  7. CHECKS AND BALANCES WITH FAILSAFES BUILT ALONG THE WAY — not bolted on
     after. Fail-closed AI judgement, the human gate, save_check, cold-start
     testing. Build the guardrail with the feature, never after it.

Judge every proposal against this paragraph. If a design makes the bot
cheaper to build but produces sloppier output, or removes a failsafe, or
skips the analytics loop — it is the wrong design for this project.

═══ THE PROJECT ═══
An automated Twitch clipping bot on a $0 open-source stack. It watches a
stream, detects clip-worthy moments STATISTICALLY rather than by watching
everything, transcribes and captions locally, cuts to format, and posts to my
channels — with a HUMAN APPROVAL GATE, never unsupervised.

MONEY: Clipping.net-style bounties, paid per 1,000 views with a MINIMUM VIEW
THRESHOLD per post. A clip under the minimum pays $0. That single fact drives
everything — it is why hook quality is load-bearing rather than cosmetic, why
SELECTION matters more than volume, and why every recurring API cost eats the
margin directly. Payouts run roughly $0.50–$3.00 per 1,000 views.
⚠️ ALL of those figures trace to ONE external-AI planning transcript which
itself says "e.g." about the threshold. There is NO primary Clipping.net
source, no terms page, no campaign ID. Treat the economics as UNPROVEN.

═══ SOURCES AND DESTINATIONS (confirmed 2026-08-06) ═══
IN — Twitch, PRIMARY for V1. All verified reachable by yt-dlp, NO auth:
    https://www.twitch.tv/lacy/
    https://www.twitch.tv/lacy/videos
    https://www.twitch.tv/lacy/clips?range=24hr
    https://www.twitch.tv/lacy/clips?range=7d      ← 964 clips pulled here
IN — Kick, secondary, nearly empty. DO NOT PULL without asking:
    https://kick.com/lacy · /videos
    https://kick.com/lacy/clips?sort=date&range=week
    https://kick.com/lacy/clips?sort=view&range=week
    (Kick exposes sort=view; Twitch does not surface that as cleanly)
OUT — MY OWN channels, so Stage 5 auth is straightforward:
    https://x.com/CoreCrashOuts
    https://www.youtube.com/@CORECrashOUTS
    (verified UCtHsW7-LqxK5mUiQcxAxqRg, public, 2 followers, ZERO videos)

@LacyCrashOuts was ALWAYS the output channel; it is now @CoreCrashOuts. Older
docs calling it a "target streamer" were never accurate. Raw records keep the
old name deliberately (Rule 16) and carry correction banners.

SCOPE: V1 = Lacy only, prove the pipeline end to end.
       V2 = the whole CORE group, after V1 is a working proof of concept.

═══ THE METHOD — how this is built, and why ═══
1. RESEARCH NEW TECH FIRST, THEN APPLY IT, THEN CODE.
   My words: "we stay in research till i say to move on im the overall
   director here". Order: find what exists → verify it is real → evaluate
   against the five roles (Rule 20) → only then write code using it. Writing
   code before knowing the best tool means writing it twice, and the second
   write fights a codebase that already assumed wrong. This is why there is a
   ~110-tool catalogue and why 964 clips were measured before any threshold
   was written. DO NOT propose "let's just start coding and fix it later" —
   considered and rejected.
2. THE PHASE TRANSITION IS MINE, NOT YOURS (Rule 10). Recommend; never declare.
3. UPSCALING — build small, prove it, widen:
   V1  one source, one destination pair, pipeline proven end to end
   V2  the whole CORE group; architecture already supports multi-creator
   V3+ more platforms in and out. Kick is the known second INPUT. Stage 5
       outputs stay a LIST BEHIND ONE INTERFACE so adding an outlet is
       config, not code — that shape exists because Facebook was lost
       mid-project and a hard-coded Stage 5 would have needed a rewrite.
   The constraint is ECONOMIC, not technical: 1,598 clippers already compete
   for the same moments and sub-threshold posts pay $0.
4. CHECKS AND BALANCES — each layer exists because something failed:
   a) HUMAN APPROVAL GATE — the bot never posts unsupervised.
   b) FAIL-CLOSED on AI judgement: any exception or unparseable response from
      a hook-quality score, TOS check or context-check = REJECT, never a
      silent pass. NOT extended to pre-flight checks or human-gate timeouts.
   c) VERIFY BEFORE TRUSTING (Rule 12) — caught 4 hallucinated GitHub repos
      and one fabricated dossier.
   d) RAW ≠ EVALUATION (Rules 15/16) — three files were once "saved"
      condensed and had to be replaced with the originals.
   e) save_check.sh — 11 checks GATING the save.
   f) check_links.sh — 121 links. ⚠️ K7: it always exits 0.
   g) COLD-START TESTING — ten passes, ten bug-finds.
   h) ONE AGENT PER SOURCE FILE + commit on arrival.
   Through-line: PREFER A MECHANICAL CHECK OVER A REMEMBERED ONE.

═══ THE 6 STAGES ═══
 1 Ingestion     yt-dlp; chat via Twitch GQL (keyless) or chat-downloader
                 ✅ PROVEN WORKING, no auth, no API key.
                 ⚠️ chat_downloader throws a reproducible KeyError:'data' —
                 needs defensive .get() chaining + Tenacity backoff first.
 2 Transcription local, word-level timestamps.
                 ⚠️ ENGINE NOT DECIDED. Rule 6 REMOVED faster-whisper as
                 default: "delete 6 we will find the best free service after
                 research". Researched alternatives: distil-large-v3 (6.3x
                 faster, ~0.2% WER cost), faster-whisper-large-v3-turbo-ct2.
                 PICKING ONE IS RESEARCH WORK.
 3 Detection     THREE-STAGE FUNNEL: free statistical pre-filter → cheap LLM
                 score → expensive LLM detail on top-N. The funnel IS the
                 cost control. Now has real numbers (below).
 4 Assembly      ffmpeg. ⚠️ THREE ASSUMPTIONS CONTRADICTED (below).
 5 Distribution  human approval gate; platform list deliberately OPEN.
                 ⚠️ NO documented auth path — YouTube Data API and X API
                 scopes, app registration and validation are all unwritten.
 6 Orchestration LangGraph + AsyncSqliteSaver. PORT the proven retry /
                 dead-letter / budget machinery from the sibling project.

MOST IMPORTANT TECHNIQUE FOUND IN ALL RESEARCH:
  snap_clip_to_words() — LLMs are unreliable at millisecond arithmetic, so
  proposed cut points get snapped onto REAL word-boundary timestamps from the
  transcript (~0.35s lead / 0.45s tail into silence) before anything is cut.
  Every other source assumed raw LLM timestamps were safe. They are not.
  Source: reference/deep_dive_openshorts.md

═══ THE DATA — all of it, with caveats stated inline ═══
A) 964 REAL TWITCH CLIPS, 7 days (research/twitch_clips/)
   Duration median 30s, mean 35.5s, p25 29s, p75 49s, range 4–60s.
   ⚠️ 71% sit at EXACTLY 30/59/29s = Twitch's clip-tool UI PRESETS. Twitch
   durations measure THE TOOL, not the moment. No target length from them.
   Views: median 5 · mean 35 · max 7,073 · all 964 together = 33,624.
     ≥5,000: 1 clip (0.1%) · ≥1,000: 6 (0.6%) · ≥100: 34 (3.5%)
   Top ÷ median ≈ 1,400x.
   ⚠️ NOT a payout prediction — Twitch views ≠ reposted X/Shorts audience.
   What it establishes: SELECTION is where all the value is.
   Reproduce (this command exists ONLY in FILE_MAP — it was nearly lost):
     "…\Python312\python.exe" -m yt_dlp --flat-playlist \
       --print "%(duration)s|%(view_count)s|%(title)s" \
       "https://www.twitch.tv/lacy/clips?range=7d"

B) 25 REAL X REPOSTS (reference/research_2026-08-06_core_clippers_named_
   VERBATIM.md). Accounts @yoxics, @scubaryan_, @coresculture.
   ACCESS METHOD WORTH KEEPING: x.com and Nitter are gated, but
   api.fxtwitter.com serves public JSON UNAUTHENTICATED — captions, views,
   likes, reposts, exact duration and pixel dimensions.
   LENGTH: median 51.4s, 44% cluster 55–61s, 0 OF 18 on Twitch presets.
   Durations are irregular decimals (38.483, 57.416) → they HAND-TRIM.
   FORMAT from frames actually viewed: 16:9 landscape dominates, NOTHING is
   9:16. NO added subtitles. Chat left BURNED IN. No watermark. ZERO hashtags
   in all 25 captions.
   ⚠️⚠️ TWO SAMPLING PROBLEMS, BOTH MATTER FOR J4:
     (a) sample came from search → favours winners → medians overestimate.
     (b) THE CLIPS ARE MOSTLY NOT LACY. Counted 2026-08-07: Jynxzi 12, Kai
         Cenat 9, IShowSpeed 5, Adin Ross 3, Peterbot 3, ClarenceNYC 1 vs
         Lacy 28. So ~55–60s is the convention for GENERAL streamer-drama
         reposts, not a measured Lacy number. @coresculture's 7,017 median
         rests on FIVE posts with one 344K outlier; 3 of 11 are photo posts.
         DO NOT bake 55–60s in as a Lacy target without corroboration.

C) 50 HUMAN-CURATED MOMENTS (reference/mining_2026-08-04_cVkFMpDLQrM_
   VERBATIM.md) — the best detection source in the repo, because the source
   is a curated best-of: a human editor already decided what was worth
   keeping, so every segment is a positive example.
   Moment types: physical escalation 28% · verbal roast 20% · authority 12% ·
   quiet reveal 12% · romance 12% · heist 10% · one-liner 6%.
   Hooks: 36% direct question · 22% shouted name/imperative · 0% NARRATION.
   21 of 50 open with Hey/Yo/Wait/Okay/All right.
   ⭐ BEST FIND — A TEXT-ONLY DETECTOR: verbal repetition in 22 of 50 moments
   (FOCUS x10, Come on x12, WAIT x8, bully x7). Rule: ≥3 repeats of a short
   phrase within 10s. Needs ONLY the transcript — no audio, no model, no API
   call — so it drops straight into the free pre-filter.
   CORROBORATION: C proposed a 20–70s band from editorial judgement; 89%
   (862/964) of real Twitch clips fall inside it. Two independent methods,
   same range. BUILD ON THE BAND, not on a single target.

D) COMPETITIVE CONTEXT: ~60M monthly views on #Lacy across 1,598 clippers,
   growing ~100% month over month.

═══ ⚠️ WHERE EVIDENCE CONTRADICTS THE PLAN — flagged, NOT applied ═══
From the X data:  1. Outline says 9:16 vertical split-screen → reality 16:9.
                  2. Outline says karaoke captions → reality NO subtitles.
                  3. Outline says chat boxblur for TOS → reality burned in.
                  4. Recorded rules say #lacy hashtag MANDATORY → reality
                     zero hashtags in 25 successful posts. UNRESOLVED.
From the curated: 5. Outline treats audio-RMS spikes as a PRIMARY pre-filter
                     → ~20% of curated moments have NO shouting. Misses 1 in 5.
                  6. Long silences are POSITIVE (physical gags). A low
                     speech-density filter deletes the best set-pieces.
                  7. Clip length can't come from caption-cue gaps (1–2s ASR).
Corroborate against a second source before rewriting Stage 3 or 4.

═══ OPEN CHECKLIST ═══
  [ ] ⚡ K1 — PRIVACY, sibling repo. CONFIRMED. Ask me first (TASK #2)
  [ ] ⚡ K2–K8 — 7 more save-system findings, ALL UNVERIFIED (TASK #3)
  [ ] ⚡ J1 — BUILD THE DETECTOR EVAL HARNESS. Clips carry view counts and
      point back into VODs, so a detector can be scored on whether it picks
      the moments that actually earned views. NOTHING in this project can
      currently measure detector quality AT ALL. Highest-value item.
  [ ] G4 — mine research/transcripts/PafYu69s5NA.txt. One agent, one file,
      already on disk. It opens describing a clip "found, analyzed, cut, and
      captioned automatically and completely for free with Claude" — this
      project's exact problem, already solved by someone else.
  [ ] G5/G6 — mine mFOoNPFylLI and QqwNue_KL-4
  [ ] J2 — cross-reference clip titles against the moment taxonomy
  [ ] J3 — pull the 24hr clip window, compare to 7d
  [ ] J4 — fix the Stage 3 length default (see the two sampling problems)
  [ ] J5 — re-check Kick before V2
  [ ] J6 — re-examine the payout maths against the real view distribution
  [ ] Resolve the 7 contradictions above
  [ ] A: Rule 20 retroactive review — 1 of 6. The five remaining, NAMED:
      A2 HF-vision · A3 HF-LLM/judging · A4 the mining report · A5 the
      78-source audit · A6 the 17-video fresh-pass (2 big files — SPLIT IT).
      ⚠️ A2–A6 prompts DO NOT EXIST; you must author them.
  [ ] B: source mining — 1 of 12. B2–B12 prompts ARE written and pasteable.
  [ ] D: platform / free-inference / hosting research — not started.
      ⚠️ D has a 5-agent SCOPE SPLIT, not prompts. You must author them.
  [ ] E: the failure report — what's fixed, what isn't. Defined in PENDING,
      absent from every status table. Barely started.
  [ ] F: the AI\ folder — PUT OFF, waits on ME. Too big; I triage and hand
      you what matters. DO NOT sweep it unprompted.
  [ ] Run validate_environment.py in Colab — settles the credentials blocker.
      It has NEVER run green.
  [ ] Fix chat_downloader's KeyError:'data' before Stage 1 depends on chat
  [ ] Answer the 5 open questions in
      reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md
  [ ] WRITE THE FIRST LINE OF ACTUAL PIPELINE CODE
  [x] Stage 1 source CONFIRMED AND PROVEN WORKING (workstream I)
  [x] C: 6 transcripts fetched and verified (2026-08-04)
  [x] G1/G2/G3 mined · H1 and H2 both done
  [x] All docs corrected to the real links; raw records preserved
  [x] Rule 22 adopted; Rules 8 & 9 dropped; save_check.sh gates the save
  [x] FILE_MAP.md, INDEX.md, HANDOFF_REPORT written
  [x] requirements.txt rebuilt (it covered NONE of the project's tools)

═══ WHAT A NEW CONTRIBUTOR STILL CANNOT DO ═══
  1. JUDGE THE BUSINESS CASE. Every dollar figure traces to one external-AI
     transcript that says "e.g." about the threshold. No primary source. Only
     I or Clipping.net can settle it.
  2. AUTHENTICATE STAGE 5. YouTube/X API scopes, registration, validation —
     all unwritten.
  3. AUTHOR A2–A6 AND D PROMPTS. They do not exist.
  4. RECOVER .claude/ IF THE MACHINE DIES. session-state.md and
     session-prompts.log are gitignored and backed up nowhere (K6), and
     settings.json — the only thing that REGISTERS the hooks — is not in
     hooks_backup/. Restoring the backup alone yields four inert scripts that
     fail silently.
  5. FIND THE COLAB NOTEBOOK. "Claude's AI clip bot v1.ipynb" exists only on
     Drive, not in git.
  Note: TARGET_BROADCASTER is a fourth env var validate_environment.py reads
  and it is documented almost nowhere.

═══ THE RULES — apply them, don't just read them ═══
CLAUDE.md, 21 numbered, 16 active. Each exists because a specific failure
happened. Strict defaults; deviating requires asking me first.
  Rule 1   PORT, DON'T RE-DERIVE. Check SALVAGE_INVENTORY.md and the sibling
           pipeline.py before writing ANY function. THREE DAYS were lost
           building a save system from scratch when a working implementation
           (Sonovore/claude-code-handoff) had already been pointed out.
  Rule 10  I decide what is "complete." Never self-stamp. When I authorize
           it, mark exactly "✅ COMPLETE — authorized by user YYYY-MM-DD".
           Until then the only honest statuses are "in progress", "awaiting
           user approval", "blocked".
  Rule 12  Verified means checked THIS session. File existence is not content
           verification. Past notes, other AI output, and your own earlier
           conclusions are LEADS TO VERIFY, not facts to build on.
  Rule 14  No rule adopted without my explicit confirmation.
  Rule 15  Source material WORD-FOR-WORD. Never condense or placeholder.
  Rule 16  Raw records and evaluation in SEPARATE files. NEVER rewrite a raw
           record to reflect a later finding.
  Rule 18  ⚠️ HALF NOT EXECUTABLE — it says save to GitHub AND Drive. You
           cannot write Drive. GitHub half is binding; I pull in Colab.
  Rule 20  Five roles per tool: primary / fail-safe / cross-check / assist /
           feature. Never dismiss a working free tool.
  Rule 21  Run EVERY check BEFORE reporting, not after I ask.
  Rule 22  Update START_HERE.md LAST, before the final push, even when a
           usage limit is cutting things short.
  ⚠️ THERE IS NO RULE 17 — the list runs 1–16 then 18–22. It was never
  written. Removed at my direction: 2, 4, 6 (08-01); 8, 9 (08-03).

═══ BEFORE STARTING ANYTHING ═══
  - Confirm the checkpoint: git log, git status, synced with origin.
    Last known good is b3fa9c2 or later. HEAD one ahead of START_HERE.md's
    header is NORMAL and documented; two or more means work landed after it
    was written (§0 explains why).
  - CONFIRM MY USAGE HEADROOM BEFORE LAUNCHING AGENTS. I hit 100% on 08-04
    and 08-06 and I am on paid usage. TELL ME THE COST BEFORE launching a
    workflow — the 08-06 one took a session from 49% to 82% in one run, spent
    ~518K subagent tokens, and returned 1 of 15 agents because the rest died.
  - ONE AGENT PER SOURCE FILE. Single-file agents have succeeded every time;
    broad-scope agents have died producing nothing, twice. COMMIT EACH REPORT
    THE MOMENT IT LANDS — never batch. On 08-04 a session limit killed 3
    agents mid-write; that practice cost one report instead of three.
  - TWO UNVERIFIED LEADS in START_HERE.md §3 — check BEFORE related build
    work: (a) does the sibling project's video code still run? Two .mp4 files
    dated 2026-07-27 exist; their EXISTENCE is verified, whether the current
    code produced them is NOT. (b) is validate_environment.py one auth fix
    from passing? One Colab cell settles it.
  - A no-op re-run of fetch_transcripts_batch2.py once OVERWROTE
    _summary_batch2.txt with zeros, destroying the evidence for workstream C.
    Recovered from git. Be careful what you re-run.

═══ HOW TO REGENERATE THIS PROMPT ═══
  BUILD IT FROM THE PREVIOUS PROMPTS. IT MUST GROW, NOT SHRINK. My words:
  "dont make me ask u 3 times to reference the original prompts and include
  more detail just do it." A diff against my three older prompts found SEVEN
  details silently dropped, including the names of workstream A's sub-items,
  without which A cannot be started. Every regeneration: diff against the
  previous version and justify every removal.
  The design principle, from Sonovore/claude-code-handoff — the shipped
  implementation this mechanism came from: A HANDOFF SHOULD PRIORITISE
  FORWARD-LOOKING DIRECTION OVER A RECORD OF FINISHED WORK. Cut history
  before you cut instructions, never the reverse.

═══ CONTEXT I'LL FORGET ═══
  - Budget is a live constraint, metered, and I am on paid usage.
    ⚠️ THE RESET MECHANIC IS UNCONFIRMED — docs long claimed "hard weekly
    reset Monday 1pm" and I NEVER SAID THAT. What I actually report is a
    ~5-HOUR ROLLING SESSION WINDOW plus a MONTHLY credit reset. Pace against
    the 5-hour window; ask me to confirm.
    DOCUMENTATION WORK IS NOT CHEAP — one session went fresh to 100% on a
    SINGLE agent plus note-keeping.
  - Drive: you CANNOT write to it. You push to GitHub, I pull in Colab, and a
    fresh Colab runtime needs drive.mount() before any git pull works.
    Folder: /content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt
  - THIS IS A PUBLIC REPO. .claude/ holds my raw prompts (session-prompts.log,
    1,085 lines) and durable facts (session-state.md). Gitignored. See K1.
  - Raw transcripts back up to AI\claude_transcripts_backup_<date>\ (~66MB).
  - I CAN PULL WORD-FOR-WORD TRANSCRIPTS FROM GEMINI by pasting a YouTube
    link. Zero cost, no API. Role: fail-safe and cross-check when
    youtube_transcript_api fails (captions disabled, age-gated). Caution:
    Gemini output labelled verbatim has been condensed here before — spot
    check one against the API first.
  - NEVER use `git checkout <file>` to undo an edit — it reverts the WHOLE
    file and destroyed real work on 08-03. Use sed, or commit first.
  - Real Python: C:\Users\AwBro\AppData\Local\Programs\Python\Python312\
    python.exe — "python" and "py" do NOT resolve (Windows Store stub).
    Windows Python cannot see git-bash's /tmp; use a shared absolute path.
  - I was BANNED ON FACEBOOK for failing a bot check; Instagram pending. Two
    of four originally planned Stage 5 outlets are gone or at risk.
  - STILL ZERO PIPELINE CODE. That is the honest headline. Everything so far
    is restoration, research, rules, and the first real detection data. The
    fastest path to a working bot: G4 → J1 → the first real Stage 1→2 code
    using the proven yt-dlp path.
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
- Budget is live — metered. ⚠️ THE RESET MECHANIC IS UNCONFIRMED — docs long said "hard weekly reset Monday 1pm" but the user NEVER SAID that. What they actually report is a ~5-HOUR ROLLING SESSION WINDOW plus a MONTHLY credit reset ("Resets Sep 1"). Pace against the 5-hour window. Ask them to confirm, hit repeatedly
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
