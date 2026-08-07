# Automated Clipper Bot — PROJECT.md

Single source of truth for this project's status, architecture, and backlog.
See [CLAUDE.md](CLAUDE.md) for the working rules. Chat history is not
authoritative; this file is — if a conversation conflicts with this file,
this file wins unless the code has since changed.

**Looking for a specific document?** [`INDEX.md`](INDEX.md) catalogues every
file in this repo — what is in it, its verification status, and when to read
it. It exists because a 2026-08-04 audit found **12 of 30 source documents
referenced by nothing a session actually reads**, including three verbatim
research reports that had already been nearly lost once. Finished work that
nothing points at is functionally lost. Add a row there whenever you add a
file.

## Current status (updated 2026-08-07)

> ## 📍 SOURCES AND DESTINATIONS — confirmed by the user 2026-08-06
>
> **`@LacyCrashOuts` was always the OUTPUT channel. It is now
> `@CoreCrashOuts`. That is the whole change** — the user's words:
> *"lacyscrashouts was always the output channel now its core thats it"*.
> Older docs that call it "the target streamer" were never accurate; the
> setup itself did not change, only the channel's name.
>
> ### IN — where clips are sourced from
>
> | Platform | URL | Status |
> |---|---|---|
> | **Twitch — channel** | `https://www.twitch.tv/lacy/` | **PRIMARY for V1** |
> | Twitch — VODs | `https://www.twitch.tv/lacy/videos` | ✅ `yt-dlp` reaches it, no auth |
> | Twitch — clips, 24h | `https://www.twitch.tv/lacy/clips?range=24hr` | ✅ works |
> | Twitch — clips, 7d | `https://www.twitch.tv/lacy/clips?range=7d` | ✅ **964 clips pulled 2026-08-06** |
> | Kick — channel | `https://kick.com/lacy` | secondary, nearly empty |
> | Kick — VODs | `https://kick.com/lacy/videos` | secondary |
> | Kick — clips, recent | `https://kick.com/lacy/clips?sort=date&range=week` | secondary |
> | Kick — clips, best | `https://kick.com/lacy/clips?sort=view&range=week` | secondary — note it exposes `sort=view`, which Twitch does not surface as cleanly |
>
> **Kick was deliberately NOT pulled** — the user: *"there is barely any
> content on there right now"*, then *"dont pull anything"*. Re-check before
> V2; a second platform means a second ingestion adapter.
>
> ### OUT — where finished clips get posted
>
> | Platform | URL | Notes |
> |---|---|---|
> | **X** | `https://x.com/CoreCrashOuts` | the user's own account |
> | **YouTube** | `https://www.youtube.com/@CORECrashOUTS` | the user's own channel. Verified via `yt-dlp`: `UCtHsW7-LqxK5mUiQcxAxqRg`, public, 2 followers, **zero videos**, described *"WILD out of pocket Core boys moments and CrashOuts"* — a brand-new clipper channel |
>
> Because the user **owns both destinations**, Stage 5 auth is
> straightforward — no permissions problem. But which platforms to actually
> target stays an **open research question** (workstream D); the user:
> *"we will sort that out later we are in research stage."*
>
> ⚠️ **Meta is a live risk, not a plan.** The user was **banned on Facebook**
> for failing a bot check, with **Instagram pending**. Do not design Stage 5
> around Meta.
>
> ### Scope
>
> **V1 = Lacy only** — *"we will start with lacys clips only then scale up
> once the project works and is poc"*. **V2 = the whole CORE group.** This
> makes the three mined Lacy transcripts (G1/G2/G3) directly on-target for
> V1 rather than background research.
>
> Raw records and verbatim agent reports keep the old name and are **not
> edited** (Rule 16); each now carries a correction banner instead.

**Zero pipeline code still exists.** That remains the honest headline. What
changed on 2026-08-04 is that **Stage 3 now has real measured numbers
instead of generic advice** — the first findings in this project that a
build decision can actually rest on.

### The Stage 3 findings

Source: [`reference/mining_2026-08-04_cVkFMpDLQrM_VERBATIM.md`](reference/mining_2026-08-04_cVkFMpDLQrM_VERBATIM.md).
It carries disproportionate weight because the source video is a **curated
best-of** — a human editor already decided which moments were worth keeping,
so all 50 segments are positive examples rather than opinions about what
might work.

| Finding | Measured value |
|---|---|
| Clip length | median **39.5s**, mean 42.7s, p25 29s, p75 52s; 78% fall in 20–70s |
| **Recommended defaults** | **target 40s, accept 20–70s, hard floor 11s** |
| Hook openings | 36% direct question · 22% shouted name/imperative · **0% narration** |
| Moment types | physical escalation 28% · verbal roast 20% · authority 12% · reveal 12% · romance 12% · heist 10% · one-liner 6% |

**The most useful single finding — a text-only detector.** Verbal repetition
appears in **22 of 50 curated moments**: `FOCUS` ×10, `Come on` ×12,
`WAIT` ×8, `bully` ×7. Proposed rule: **≥3 repeats of a short phrase within
10 seconds.** It matters out of proportion to its simplicity because it
needs *only the transcript* — no audio analysis, no model, no API call. It
drops directly into Stage 3's free statistical pre-filter, the stage whose
entire purpose is keeping most of a VOD away from any paid call.

### ⚠️ Three corrections that contradict the Architecture Outline

**Flagged, deliberately not applied.** Changing a design off one source is
what this repo's rules forbid; these need corroboration first (G4–G6 and
workstream A remain unmined).

1. **~20% of curated moments contain no shouting at all.** The Architecture
   Outline lists audio-RMS spikes as a *primary* pre-filter signal. As
   written it would miss one moment in five. Volume needs to be one signal
   among several, not the trigger.
2. **Long silences are positive, not negative** — they are physical gags. A
   low speech-density filter would delete the best set-pieces.
3. **Clip length cannot be derived from caption-cue gaps** — those are 1–2s
   ASR cadence, not clip boundaries.

### Competitive context (not a threshold)

~**60M monthly views** on the `#Lacy` hashtag across **1,598 clippers**,
growing ~100% month over month (source: G3). This is the field the bot would
enter — directly relevant because the payout model pays **$0** below a
per-post view minimum, and 1,598 competitors chasing the same moments is
exactly the condition that produces sub-threshold posts.

### ⚠️ Open, load-bearing: the target handle

The CORE discovery agent **could not find `@CoreCrashOuts`**
([`research_2026-08-04_core_clippers_discovery_VERBATIM.md`](reference/research_2026-08-04_core_clippers_discovery_VERBATIM.md) §6).
The entire project targets that account. Either the handle is wrong, it was
renamed or removed, or it is not discoverable logged-out. **Only the user can
settle this** — recorded as a question rather than resolved by guessing.

### What else landed 2026-08-04

- **Workstream C closed** — all 6 missing transcripts fetched, 6/6, verified
  to contain real timestamped text. 23 transcripts now on disk, each with
  its source URL on line 2 and per-line timestamps, so any quote is
  checkable at the exact second.
- **G1/G2/G3 mined** — one agent per file, ~192KB of verbatim reports with
  2,650+ timestamp citations between them. Both G1 and G3 carry explicit
  source-reliability warnings: G1 is a hostile secondary source whose
  narrator admits prior errors, and G3 is third-party commentary that
  contradicts its own thesis at `[14:35]`.
- **H2 delivered** — CORE clipper discovery, 22 VERIFIED / 2 UNVERIFIED,
  full source list, no invented handles.
- **H1 lost** to a session limit mid-write — must be re-run; prompt is
  preserved in PENDING §H.
- **[`INDEX.md`](INDEX.md) created** after an audit found 12 of 30 source
  documents referenced by nothing a session actually reads.

### Still not started

Zero pipeline code. Workstream A 1/6, B 1/12, D not started, G4–G6 pending,
H1 to re-run. Workstream F (the `AI\` folder) is **put off at the user's
direction** — they triage it and hand over what matters; do not sweep it
unprompted.

---

> **⚠️ RULE COUNT, authoritative as of 2026-08-07:** `CLAUDE.md` has
> **21 numbered rules, 16 active**. Removed at the user's direction: 2, 4, 6
> (2026-08-01) and **8, 9 (2026-08-03)**. **There is no Rule 17** — it was
> never written. Older text in this file describing 8 and 9 as "provisional
> and still unauthorized" is SUPERSEDED; they were dropped.

## The method — how this project is built, and why

**This is the owner's governing approach, not a phase we are stuck in.** A
contributor who ignores it will rebuild the project wrongly.

### 1. Research new tech first, then apply it, then code

The owner's words: *"we stay in research till i say to move on im the overall
director here"* and *"we dont know the best service and model cuz we are in the
research stage."*

The order is **find what exists → verify it is real → evaluate against the five
roles (Rule 20) → only then write code that uses it.** Writing code before
knowing the best available tool means writing it twice, and the second write is
against a codebase that already assumed the wrong tool.

This is why there is a ~110-tool catalogue with verification status, why every
tool claim is independently checked against GitHub/PyPI, and why 964 real clips
were measured before a single detection threshold was written down. **The
Stage 3 numbers exist because research came first.**

**Do not propose "let's just start coding and fix it later."** It has been
considered and rejected by the owner.

### 2. The phase transition is the owner's call (Rule 10)

Research → build is a transition. You may *recommend* it. You may not *declare*
it. The same applies to calling anything "complete."

### 3. Upscaling path — build small, prove it, then widen

| Version | Scope |
|---|---|
| **V1** | **One** source (`twitch.tv/lacy`), one destination pair. Prove the pipeline end to end. Owner: *"we will start with lacys clips only then scale up once the project works and is poc."* |
| **V2** | The whole **CORE group** — multiple streamers, same pipeline. The architecture already supports a multi-creator config; only Lacy is scoped today. |
| **V3+** | More platforms in and out. Kick is the known second **input** (empty today; re-check before V2). Stage 5 outputs stay a **list behind one interface** so adding an outlet is config, not code — a shape adopted specifically because Facebook was lost mid-project. |

**The scaling constraint is economic, not technical.** 1,598 clippers already
compete for the same moments and posts under the view minimum pay $0. Widening
scope multiplies cost immediately, and revenue only if selection quality holds.

### 4. Checks and balances — the layered system

Every layer exists because a specific failure happened.

| Layer | Catches |
|---|---|
| **Human approval gate** | The bot never posts unsupervised |
| **Fail-closed AI judgement** | Any exception or unparseable response from a hook-quality score, TOS check, or context-check = **reject**, never a silent pass. Explicitly *not* extended to pre-flight checks or human-gate timeouts |
| **Verify before trusting** (Rule 12) | Four hallucinated GitHub repo attributions; one fabricated dossier |
| **Raw ≠ evaluation** (Rules 15/16) | Three files once "saved" as condensed paraphrases, replaced with originals |
| **`save_check.sh`** | 12 mechanical checks gating the save. Has caught real staleness every session since it existed — including its own false-alarm bug |
| **`check_links.sh`** | Link rot across 119 links |
| **Cold-start testing** | Seven passes, every one found real bugs. A clean pass is a weak test, not a pass |
| **One agent per file + commit on arrival** | Bounds the blast radius when a session limit hits mid-run |

**The through-line: prefer a mechanical check over a remembered one.** A
protocol that depends on remembering fails the same way a file nothing points
at does.

---

## One-line description

Pulls the best clips from Twitch VODs/streams, adds captions, produces
YouTube Shorts + long-form compilations, cross-posts to multiple platforms.
Separate project from `youtube-auto-videos` (Parents Teach Kids), kept in
its own folder/repo, but actively salvaging verified-working code from it.

## Current status (updated 2026-08-03 — read this first if resuming)

**⚠️ Read [`START_HERE.md`](START_HERE.md) first** — it is the session
entry point (scope, state, next action, blockers, open questions). This
file holds durable project state and architecture.

**Still zero pipeline code.** Unchanged, and stated first so the list below
doesn't imply otherwise.

2026-08-03 was spent building the session-continuity system, after a
cold-start test showed the resume path was one mechanism deep rather than
the three it claimed:

- **[`START_HERE.md`](START_HERE.md)** — single entry point. Opens with §0,
  a self-validation checklist (commit hash / rule count / link rot / dirty
  tree) because the file goes stale by design. Now also carries project
  scope, the 6-stage pipeline, campaign rules, per-workstream cost
  estimates, and §3b — questions only the user can answer.
- **[`SAVE_PROTOCOL.md`](SAVE_PROTOCOL.md)** — the 9 ordered steps that run
  when the user says "save everything." Previously improvised, which
  degrades silently and can't be audited. The user's governing definition:
  *"save everything means what u need to pick up where we left off."*
- **[`SESSION_HANDOFF_PROMPT.md`](SESSION_HANDOFF_PROMPT.md)** — the
  ready-to-paste catch-up block plus its template. Regenerated every save;
  a stale one sent a session to rebuild finished work.
- **[`check_links.sh`](check_links.sh)** — link-rot detection across the
  key docs (46 links, all resolving).
- **Four lifecycle hooks**, wired globally in `~/.claude/settings.json`:
  `SessionStart` (injects context — makes auto-load structural rather than
  conditional), `UserPromptSubmit` (logs the user's prompts verbatim),
  `PreCompact` (snapshots before context is lost — the sudden-death case),
  `Stop` (reminds if `START_HERE.md` wasn't updated). All exit 0
  unconditionally; tested 10 ways before wiring.
- **A user-level `~/.claude/CLAUDE.md`** — the only instruction path that
  fires regardless of working directory. The root cause: this repo's
  `CLAUDE.md` only auto-loads when a session is rooted here, and sessions
  were repeatedly rooted in the sibling project instead.
- **Rule 21** — run every check *before* reporting done, not after being
  asked. **Rule 10** gained a marking convention: nothing is written as
  complete until the user says so, then stamped
  `✅ COMPLETE — authorized by user YYYY-MM-DD`.
- **Privacy fix** — `.claude/` gitignored after testing revealed the prompt
  log was one `git add -A` from a **public** repo.
- **66MB of raw session transcripts** backed up outside the repo.

**Still blocked on the user:** Rule 22 (make the `START_HERE.md` update
non-skippable), and provisional Rules 8 & 9 (Gemini-sourced, never
authorized).

## Current status (updated 2026-08-02 — read this first if resuming)

**⚠️ Read [`START_HERE.md`](START_HERE.md) first** — it is the single
session entry point (state now, next action, blockers, where things are),
updated every session. This file holds durable project state;
`START_HERE.md` holds what's in flight, with
[`reference/PENDING_agent_prompts_resume_2026-08-01.md`](reference/PENDING_agent_prompts_resume_2026-08-01.md)
carrying the detailed per-item agenda behind it.

**Headline, stated plainly: still zero pipeline code.** Everything to date
is restoration, research, verification, and operating rules. That is the
failure report's §14 finding and it remains true. Worth saying before the
list of genuine progress below, not after it.

What happened 2026-08-02:

- **Rule 20 adopted — don't dismiss free tools.** The user reviewed saved
  research and found working free tools had been discarded for losing the
  "primary pick" slot. Every tool is now evaluated against **five roles**:
  primary, backup/fail-safe, cross-check, assist (free pre-filter), and
  feature/quality-add. Plus: free changes the math; never judge on star
  count, README tone, or age; a set-aside must record *why* and *what
  would bring it back*. See [CLAUDE.md](CLAUDE.md).
- **Retroactive Rule 20 review started** —
  [`reference/retroactive_rule20_review_2026-08-02.md`](reference/retroactive_rule20_review_2026-08-02.md),
  1 of 6 completed reports re-checked. Biggest find so far: **Kyutai STT**
  was dismissed as "not a clear fit" because it was measured against batch
  VOD transcription — but this project's stated Phase 1 is *live stream
  monitoring*, which is exactly what it's built for and exactly what
  faster-whisper (a batch transcriber) doesn't serve. Four others re-opened
  with roles assigned. Nothing adopted — re-opened candidates only.
- **Master tools catalog created** —
  [`reference/MASTER_TOOLS_CATALOG_2026-08-02.md`](reference/MASTER_TOOLS_CATALOG_2026-08-02.md).
  **~110 tools with real URLs**, organized by pipeline stage, each with
  verification status, how it helps, and its Rule 20 role. Consolidates
  findings previously scattered across 5+ documents and adds the URLs they
  lacked. **Start here when picking a tool for a stage.** Additive — the
  earlier `verified_tools_catalog.md` and all `*_VERBATIM.md` reports are
  untouched.
- **Platform/hosting research scoped** —
  [`reference/research_targets_platforms_2026-08-02.md`](reference/research_targets_platforms_2026-08-02.md).
  The user supplied a target list as a *method* instruction: widen from
  "models within Hugging Face" to model hubs beyond it (ModelScope,
  Civitai), hosted inference with free tiers (Replicate, Modal, Together
  AI), app galleries as prior art (Streamlit), and hosting routes.
  Highest-leverage lead: **Ollama on a free Oracle ARM VM** — moves
  local-LLM judging to always-on free cloud, which a bot meant to watch
  live streams needs. All ❓ unverified.
- **Two real gaps recorded honestly** (searched and confirmed, not
  assumed): no purpose-built **hook-quality/engagement scorer** exists on
  HF, and no general **"which game is being played"** model exists —
  Twitch's own category API metadata is the correct free source.
- **Rules audited and corrected.** 15 active (3, 5, 7, 10–21); 3 removed
  at the user's direction (2, 4, 6) because they pre-committed
  tool/threshold decisions the research hasn't made — *"we dont know the
  best service and model cuz we are in the research stage"*; 2 provisional
  and still unauthorized (8, 9); 1 inherited (1). Governing principle now
  recorded: **rules describe how we work, not which library wins.**
- **Cold-start resume proven in production.** The 2026-08-01 session was
  cut off at 95% usage; 2026-08-02 resumed from the notes alone, cleanly,
  with nothing lost and no re-derivation. The save-per-item discipline
  (Rules 13/18) is validated under real failure, not just in principle.

## Current status (updated 2026-08-01 — read this first if resuming)

**A second, much larger research/verification pass happened, driven by a
new round of Gemini planning material the user handed off (multiple
versioned "Step 8 Gateway" handoffs, a 920-line full planning-session
transcript, a 78-source tool directory) plus a "numerous attempts"
archaeology exercise across scattered Drive exports.** Full detail lives in
`reference/handoff_2026-08-01_*.md` (verbatim source material,
`handoff_2026-08-01_chat_pasted_originals.md`; evaluation/synthesis,
`handoff_2026-08-01_evaluation.md`; the raw 920-line planning transcript and
the raw 78-source directory, saved as their own files). Headline results:

- **`validate_environment.py`'s 8 previously-logged defects (below) are now
  fixed** — a newer local version (retry/backoff, token tracking, single-
  token-exchange reuse, incremental print-as-you-go, `get_secret()`
  throughout) was found to already exist locally, diff-confirmed superior
  to what GitHub had, and swapped in for real this session. Still not yet
  run end-to-end against real Twitch credentials (below).
- **4 more hallucinated tool-owner attributions caught** in the new
  78-source directory (`cut-the-crap`, Camoufox, `ffsubsync`, plus a
  fabricated capability claim on `CanadianZombies/download-twitch`) — same
  shape as the earlier `samyaksgupta/Clips`/"Biro" catches. Real
  alternatives identified for each; see the evaluation file.
- **MediaPipe "Face Mesh" confirmed wrong a third time**, independently,
  across three different sources this session (a Gemini technical
  supplement, the 78-source directory, and a dedicated Hugging Face
  verification pass) — the correct component remains lightweight Face
  Detection/BlazeFace, as this file's own Stage 4 notes already had it.
- **A real crash was found and diagnosed**: an actually-executed Colab
  notebook (`Copy of CLIPPING BOT.ipynb`, outside this repo) produced a
  real `KeyError: 'data'` inside `chat_downloader`'s Twitch GraphQL path —
  first-hand confirmation of the "Rigid Third-Party API Parsing" failure
  mode, not a hypothetical. Needs defensive `.get()`-chaining before Stage 1
  relies on `chat_downloader`/`chat-analyzer`.
- **A real, if empty, `pipeline_tasks`/`payout_logs` SQLite schema was
  found** (in a code-less `Lacy_Clip_Bot` Drive export) and adopted as the
  basis for Stage 6's idempotent VOD tracking rather than designing one
  from scratch — see the evaluation file for the schema.
- **Operating rules adopted, then audited and pruned to 6 active** — see
  [CLAUDE.md](CLAUDE.md) for the full list with provenance. Active: AI
  judge calls fail closed (scoped); Tenacity backoff on flaky third-party
  API wrappers; VOD-list caching (content-hash + URL/title/notes); user
  has final say on phase transitions and completion claims; default to
  parallel background agents for multi-source research; nothing is
  factual unless confirmed in-session or user-OK'd.
  **Three were removed on user direction** (chat-spike Z-threshold,
  narration audio-mixing prohibition, faster-whisper-as-primary) because
  they pre-committed tool/threshold decisions that the research hasn't
  made yet — *"we dont know the best service and model cuz we are in the
  research stage."* Two more (ffmpeg `+faststart`, `.ass`/`\an5`
  captions) are flagged **provisional**: Gemini-sourced and adopted
  without authorization. The findings behind all five still live in the
  Architecture Outline and reference docs — they're just not binding
  rules. Governing principle: rules describe **how we work**, not which
  library or threshold wins.
- **Hugging Face explored as a new source** (3 parallel agents, real
  model-card verification): concrete upgrade candidates found for
  transcription (`distil-whisper/distil-large-v3`), scream/shout detection
  (`MIT/ast-finetuned-audioset-10-10-0.4593`), emotion detection
  (`dima806/facial_emotions_image_detection`), and local content-safety
  judging (`meta-llama/Llama-Guard-3-1B`, first-party Ollama-pullable) —
  none yet adopted as defaults, flagged as real candidates to evaluate. See
  Backlog for what's still queued on this front.
- **Tier 2** (a second "burner" channel for gambling-affiliate promotion,
  per the new planning material's Section 11) **is explicitly out of scope
  — deferred as a future expansion, not built.** Its own design builds
  anti-shadowban/hash-randomization infrastructure specifically because it
  expects to get flagged/banned — Claude flagged this as evasion tooling
  for anticipated platform enforcement and declined to build it without
  further explicit direction; only Tier 1 (the compliant clipper) is active
  scope.
- **Real progress on the credentials blocker**: the user is setting up a
  fresh Colab notebook (`Claude's AI clip bot v1.ipynb`, targeting a Drive
  location the bootstrap cell below clones into) and entering
  `GOOGLE_API_KEY`/`TWITCH_CLIENT_ID`/`TWITCH_CLIENT_SECRET` as real Colab
  secrets — not yet confirmed run end-to-end, but actively in progress
  rather than fully blocked.
- **Explicitly not done this session** (deliberately, to keep to a
  budget-conscious stopping point): no pipeline code was fixed or built —
  the `pipeline_transcription_engine.py` gaps documented in the prior
  session's plan are still open; see Backlog.

## Current status (updated 2026-07-30, end of research push — read this first if resuming)

**Research and verification phase is fully complete.** Everything below is
done, checked, and committed:
- Repo scaffold, `SALVAGE_INVENTORY.md`, `validate_environment.py` (written,
  compile/lint clean, **still untested against real Twitch creds** — the
  one real remaining gap).
- All 17-video research: full real transcripts + two independent re-reads.
  Definitive finding: no tool in this space closes the loop on real
  post-publish analytics feedback (see Research index below).
- All 6 Gemini dossiers saved **true-verbatim** (corrected after an initial
  condensing error caught mid-session — see git history).
- Every named claim across all 6 dossiers independently verified: ~34+
  GitHub repos (~85% clean-match rate), Reddit threads (0/5 confirmable),
  YouTube devlogs (1/10 confirmed), and every named SaaS product's real
  domain (NexusClips, Submagic, Repurpose.io, Nuelink, Pabbly Connect,
  Blotato, Metricool, Headliner, Vyro, Opus Clip — all confirmed real with
  real pricing). One notable finding: **"Biro"**, repeated across the
  video research as a real paid-clipper marketplace, could not be
  independently confirmed to exist — strong evidence from re-checking the
  actual source transcript that it's a mis-transcription of "Vyro," not a
  second real company.
- Full source-level deep-dive of all 7 strongest repos found: `openshorts`
  fully (sections 1-19, every core Python file, licensing checked);
  `ClipsAI`, `twitch-clip-miner`, `Auto-clipper`, `TwitchDownloader`,
  `stream-clipper`, `metaleey` all audited file-by-file with real
  self-corrections and bugs caught along the way.
- The cost-philosophy correction pass (don't discard free resources just
  because they're not the primary pick — see
  `feedback_dont_dismiss_free_resources` in cross-session memory).
- Real URLs added throughout every reference document (47 tool mentions
  in this file alone) — nothing left as a bare name where a confirmed URL
  exists. A short, honest list of names that still have no confirmed URL
  (because no reference file has one, not because anyone guessed) lives in
  the relevant sections below.

**⏳ Blocked on the user:** Twitch Developer Console app (Client ID +
Secret) — guidance given in chat, not yet confirmed done. Nothing in
Stage 1 (ingestion) can be tested for real without this.

**Not started at all:** any actual pipeline code. Still deliberately in
the pre-flight/research phase — this was always the plan, not a delay.

**To resume after a break:** get the Twitch credentials, then run
`validate_environment.py` for real, then start writing the first pipeline
stage per the Architecture Outline below. All work is committed locally in
small, atomic commits (`git log`) — safe to pick up from any point without
re-deriving anything from chat.

**Pre-flight phase. No pipeline code has been written yet — by design.**
Per explicit instruction: prove out every hard dependency before writing any
real pipeline stage, the same discipline `validate_api_keys()` and
`discover_best_working_models()` enforce in the other project, learned there
the hard way (a real $2.57 overspend from retrying against a model with zero
quota).

Built so far:
- Repo scaffolded (this file, `CLAUDE.md`, `.gitignore`, `requirements.txt`).
- [`SALVAGE_INVENTORY.md`](SALVAGE_INVENTORY.md) — verified-working
  functions/patterns from `pipeline.py`, each confirmed to actually exist at
  the stated file:line before being listed.
- [`reference/gemini_suggestions.md`](reference/gemini_suggestions.md) — a
  Twitch-clipping architecture and reference script the user got from
  Gemini, evaluated: the 4-stage workflow shape and streamer-economy context
  are useful, but the actual code has real bugs (no Colab-secrets support,
  an unused Pydantic schema, no response_schema enforcement, no JSON repair,
  claims caption-burning it doesn't implement, no real VOD-ingestion
  function). Treated as inspiration only, per standing rule — see
  `CLAUDE.md`.
- [`validate_environment.py`](validate_environment.py) — pre-flight checks
  for ffmpeg, `GOOGLE_API_KEY` (real `generate_content` call), Twitch
  `TWITCH_CLIENT_ID`/`TWITCH_CLIENT_SECRET` (real `client_credentials` token
  exchange), and an optional real Get Clips endpoint check once a target
  broadcaster is configured. Compile/lint-checked clean
  (`py_compile` + `pyflakes`, both passed 2026-07-29). **Not yet run
  end-to-end with real Twitch credentials** — blocked on the user creating a
  Twitch Developer Console app (Client ID + Secret); guidance given in chat,
  not yet confirmed done.
- `research/` — deep re-study of 17 YouTube videos on clipping automation,
  in progress (see below).

## Research & reference material index

Everything below is real material, independently checked where checkable —
not taken at face value. Start here before re-deriving anything from scratch.

**Video research** (17 YouTube videos on clipping automation):
- [`research/RESEARCH_YOUTUBE_SOURCES.md`](research/RESEARCH_YOUTUBE_SOURCES.md)
  — recovered original synthesis (both research batches, verbatim) + a
  raw-source mining pass. Confirms a real open-source reference pipeline
  (`COMMAND-LABS/step-by-step-video-clipping-demo`) and a well-corroborated
  tool landscape.
- `research/transcripts/*.txt` — **full, real, timestamped transcripts for
  all 17 videos**, fetched directly via `youtube_transcript_api` (17/17
  succeeded) rather than relying on flaky browser scraping. See
  `research/fetch_transcripts.py`.
- `research/fresh_pass_videos_1-9.md` / `research/fresh_pass_videos_10-17.md`
  — **complete.** Exhaustive re-read of every video's full real transcript,
  requested after the user flagged that real useful content
  (analytics-driven self-adjustment of content based on performance data,
  and other tools) was likely missed/compressed away in the first pass.
  **Definitive finding: across all 17 videos, checked via full spoken
  transcripts (not just titles/descriptions), zero genuine
  analytics-feedback / self-adjusting-content loops exist anywhere in this
  space.** What does exist: pre-publish "virality score" predictions (Klap,
  Submagic, Opus Clip, Riverside) and a posting-cadence ramp schedule tied
  to platform-flagging risk — neither is closed-loop against real measured
  post-publish outcomes. This is a real, well-evidenced gap, not a research
  miss — worth treating as a genuine differentiation opportunity (see
  `pipeline.py`'s already-scoped-but-unbuilt `analytics_feedback_agent` /
  real YouTube Analytics OAuth backlog item, noted in
  `research/RESEARCH_YOUTUBE_SOURCES.md`, as a ready-made design to build
  from instead of starting blank).

**Gemini reference dossiers** (external-AI-sourced tool/architecture lists —
reference/inspiration only per standing project rule, see `CLAUDE.md`):
- [`reference/gemini_suggestions.md`](reference/gemini_suggestions.md) — the
  first architecture + reference-script dump, evaluated (real bugs found in
  the code, useful architecture shape kept).
- [`reference/gemini_dossier_1_raw.md`](reference/gemini_dossier_1_raw.md)
  through [`_6_raw.md`](reference/gemini_dossier_6_raw.md) — six "50
  sources" / architecture tool lists, saved verbatim (dossiers 4 and 5 are
  mostly generic technique descriptions rather than specific repo claims;
  the middle two blocks of the message that produced 4/5 were exact repeats
  of dossiers 1 and 2 and were not re-saved as duplicates). **Dossier 6 is
  not yet verified** — see Current Status above for its specific new claims
  and owner conflicts.
- [`research/tool_verification.md`](research/tool_verification.md) — the
  full independent-verification audit trail for every specific claim across
  all five dossiers (real GitHub API lookups, PyPI checks, search
  cross-references, real Gemini API docs checks). **Headline (dossiers 1-3):
  of 25 named GitHub repos, 19 clean matches, 5 real-but-mismatched
  (including one dangerous one — [`meitarbe/cognetivy`](https://github.com/meitarbe/cognetivy) is real and popular
  but is an AI-coding-agent state-tracker, nothing to do with video), 1
  confirmed hallucinated attribution (`samyaksgupta/Clips` → real project is
  actually [`tryvinci/vinci-clips`](https://github.com/tryvinci/vinci-clips)). Reddit citations: 0/5 confirmable.
  YouTube "devlog" citations: 1/10 confirmed real.** Dossiers 4/5's new
  claims verification in progress. Treat anything from this source as
  unverified until it appears in this file with a ✅.
- **Strongest reference-implementation candidate found across all research:
  [`mutonby/openshorts`](https://github.com/mutonby/openshorts)** (openshorts.app) — 2,784 stars, actively developed,
  confirmed real Gemini 3.0 Flash + YOLOv8/MediaPipe + [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
  pipeline. **Fully read directly from source** (not just README) — see
  [`reference/deep_dive_openshorts.md`](reference/deep_dive_openshorts.md).
  Real, portable findings: a two-stage cheap-score/expensive-detail moment
  scoring split, a "2-second test" hook-scoring rule, a diversity guard
  against duplicate clips, a real per-model Gemini pricing table, fail-fast
  handling for content-policy-blocked responses, and — the single most
  valuable find — `snap_clip_to_words()`, which corrects LLM-proposed clip
  timestamps against real ASR word-boundary timestamps before cutting. This
  is a real gap in what we'd planned to build; porting it directly.
- [`reference/deep_dive_moment_detection.md`](reference/deep_dive_moment_detection.md)
  and [`deep_dive_ingestion_and_pipelines.md`](reference/deep_dive_ingestion_and_pipelines.md)
  — real source-level reads of the other strongest verified repos
  ([`ClipsAI/clipsai`](https://github.com/ClipsAI/clipsai), [`jamesbaughnd/twitch-clip-miner`](https://github.com/jamesbaughnd/twitch-clip-miner),
  [`bendawg2010/Auto-clipper`](https://github.com/bendawg2010/Auto-clipper), [`lay295/TwitchDownloader`](https://github.com/lay295/TwitchDownloader),
  [`nirvagold/stream-clipper`](https://github.com/nirvagold/stream-clipper), [`metaleey/AI-auto-segment-edit-video-pipeline`](https://github.com/metaleey/AI-auto-segment-edit-video-pipeline)).
  **In progress.**
- [`reference/verified_tools_catalog.md`](reference/verified_tools_catalog.md)
  — **the decision-ready version**: every confirmed-real tool from both the
  video research and the dossiers, organized by pipeline stage (ingestion,
  transcription, moment-detection, editing/captioning, distribution,
  orchestration), each tagged with real status. Start here when picking a
  tool for a pipeline stage.

Status: **all research and verification complete** — 17 videos (full real
transcripts), 5 Gemini dossiers (34 named repos independently verified),
and source-level deep-reads of the 7 strongest real repos found
(`openshorts`, `ClipsAI`, `twitch-clip-miner`, `Auto-clipper`,
`TwitchDownloader`, `stream-clipper`,
`AI-auto-segment-edit-video-pipeline`). See the Architecture Outline below.

## Architecture outline (2026-07-29, cost philosophy added 2026-07-30)

Every stage below is a concrete, justified decision — grounded in real,
verified source material, not a guess. Where multiple real projects
converged on the same technique independently, that's called out, since
independent convergence is a stronger signal than any single source.

**Explicit cost philosophy — budget is a first-class constraint here, not
an afterthought.** This was learned the hard way on the sibling
`youtube-auto-videos` project (a real $2.57 overspend from retrying against
a zero-quota model) and confirmed again this session (this account's own
Claude spend limit was hit mid-research). Concretely, that means: **prefer
a free/local tool over a paid API call wherever one genuinely covers the
need**, and use paid Gemini calls only where nothing free does the job as
well. This is *why* `fer`/MTCNN (facial-expressivity), [Parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)
(GPU transcription), and the Arc-Raiders YOLO model are kept as real,
documented, zero-cost optional components in this outline rather than
being waved off in favor of "Gemini can do that too" — Gemini genuinely
can, but it costs real tokens, and those three don't. The statistical
pre-filter stage (below) exists specifically to keep as much of a
multi-hour VOD as possible from ever reaching a paid LLM call at all. Port
`pipeline.py`'s real budget-enforcement pattern (stage 6) from day one of
actual implementation, not after a first overspend.

### Stage 1 — Ingestion

- **VOD download**: [`yt-dlp`](https://github.com/yt-dlp/yt-dlp). Real, well-known, already handles Twitch's
  HLS extraction internally — no need to reimplement
  [`TwitchDownloader`](https://github.com/lay295/TwitchDownloader)'s lower-level technique (impersonating Twitch's web
  player via hardcoded GraphQL Client-IDs to get a signed playback token,
  then pulling the m3u8 manifest from `usher.ttvnw.net`), though that
  technique is documented in full in `deep_dive_ingestion_and_pipelines.md`
  as a fallback if `yt-dlp` ever breaks against a Twitch API change.
- **Chat log format**: adopt `TwitchDownloader`'s real chat JSON schema
  (`content_offset_seconds`, `commenter`, `message.fragments[].emoticon`,
  `bits_spent`) as our own internal format — it's already a de facto
  standard ([`stream-clipper`](https://github.com/nirvagold/stream-clipper)'s own chat parser comments that it expects
  "Twitch JSON format (from TwitchDownloader)"), so adopting it means any
  future tool swap stays compatible.
- **Primary highlight signal**: Twitch Helix [`Get Clips`](https://dev.twitch.tv/docs/api/reference/#get-clips) (viewer-curated,
  needs only an app access token — `client_credentials`, Client ID +
  Secret, no user login). [`Create Clip`](https://dev.twitch.tv/docs/api/reference/#create-clip) (self-directed cutting at an exact
  timestamp) needs real user OAuth with `clips:edit` scope — deferred to a
  later phase; start with Get Clips.

### Stage 2 — Transcription

- **[`faster-whisper`](https://github.com/SYSTRAN/faster-whisper)**, local, free, word-level timestamps. Confirmed as
  the primary choice by both the video research (video 1's real repo uses
  it) and independent library verification (24.6k stars, actively
  maintained).
- **Adopt [`openshorts`](https://github.com/mutonby/openshorts)'s transcript contract** as our internal schema:
  words carry a leading space on true word-starts (continuation subword
  fragments merged in), all timestamps are native floats, everything
  sorted chronologically. This isn't just tidiness — `snap_clip_to_words()`
  (stage 3) depends on exactly this shape.
- **Correction, 2026-07-30 — keep [NVIDIA Parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) (`nemo-parakeet-tdt-0.6b-v3`)
  as a documented optional GPU path, don't just dismiss it.** Originally
  written off here as unnecessary since faster-whisper was already chosen —
  same mistake as the [Auto-clipper](https://github.com/bendawg2010/Auto-clipper) YOLO model above. Parakeet is free,
  open-weight, and `openshorts` uses it as *primary* specifically because
  it's faster than whisper on GPU (falling back to whisper only on error,
  zero usable words, or a language outside its 25 supported European
  languages — see `deep_dive_openshorts.md` §8). If this pipeline ever runs
  somewhere with real GPU access (a paid Colab GPU runtime, a dedicated
  box) rather than CPU-only, swapping in Parakeet-primary/whisper-fallback
  costs nothing and could meaningfully cut transcription time on long VODs.
  Not a v1 requirement, but keep the door open — document it as a real,
  ready-to-use option, not something already ruled out.

### Stage 3 — Highlight / moment detection (the core design decision)

A **three-stage funnel**, not "ask an LLM to score everything" — this
specific refinement is the convergent recommendation across
[`metaleey/AI-auto-segment-edit-video-pipeline`](https://github.com/metaleey/AI-auto-segment-edit-video-pipeline), [`nirvagold/stream-clipper`](https://github.com/nirvagold/stream-clipper),
and [`bendawg2010/Auto-clipper`](https://github.com/bendawg2010/Auto-clipper)'s architectures, all read at the source
level:

1. **Statistical pre-filter (free, no LLM cost)** — narrow a multi-hour VOD
   down to a candidate shortlist before spending any LLM budget:
   - Audio-RMS spikes, VAD-filtered to distinguish voice reactions from
     game sound effects (`stream-clipper`'s real technique).
   - Chat velocity / keyword-emote-density spikes ([`twitch-clip-miner`](https://github.com/jamesbaughnd/twitch-clip-miner)'s
     real, working implementation — histogram + z-score over real chat
     replay data; one real bug found and documented in
     `deep_dive_moment_detection.md`, fix before porting).
   - A **"combo bonus"** (stream-clipper: 1.5x score) when audio and chat
     signals spike at the same time — a real, simple, effective
     multi-signal fusion technique.
   - Twitch [`Get Clips`](https://dev.twitch.tv/docs/api/reference/#get-clips) data folded in as a third signal (viewer-curated,
     free).
   - **`fer`/MTCNN facial-expressivity detection** (from
     `twitch-clip-miner`) as a fourth, free, local signal — flags
     high-reaction facecam moments at zero API cost, before any Gemini call
     happens. Corrected 2026-07-30: originally reasoned out entirely in
     favor of Gemini's native video understanding, which was the same
     too-quick-to-discard mistake as the YOLO/Parakeet cases below — Gemini
     does richer work (detect *and explain* a reaction) but costs real
     tokens, so the free local detector belongs in the pre-filter stage,
     not competing with Gemini for the same role.
2. **LLM score stage (cheap)** — only candidate windows that survive stage
   1 get scored by Gemini, batched, using `openshorts`'s **"2-second
   test"**: would the first 2 seconds of this moment stop a cold viewer
   from scrolling? Integer 0-100 score plus a one-line reason. This is the
   real cost-control mechanism — most of a multi-hour VOD never reaches an
   LLM call at all.
3. **LLM detail stage (more expensive, top-N only)** — only the
   highest-scoring windows get the expensive call that generates actual
   clip boundaries plus title/hook/description copy, enforcing
   `openshorts`'s **diversity rule** (never return two clips making the
   same point — pick the stronger one, drop the other) and a **named hook
   pattern library** (open question / hot take / number shock / story loop
   / POV pattern-interrupt) fed to the LLM as options.

Then, regardless of which stage flagged a moment, **two boundary-correction
passes before anything gets cut**:
- **`snap_clip_to_words()`** (`openshorts`) — LLMs are bad at
  millisecond-precise arithmetic; snap proposed start/end onto real
  word-boundary timestamps from the transcript, with small lead/tail
  padding into silence, and repair duration bounds (15-60s) by searching
  for the nearest valid word boundary. **This is the single most important
  concrete finding of this entire research effort** — every other source
  assumed raw LLM timestamps were safe to cut on; they aren't.
- **Topic-boundary snapping** ([`ClipsAI`](https://github.com/ClipsAI/clipsai)'s real TextTiling algorithm —
  cosine-similarity gap/depth scoring across multiple window sizes,
  independently confirmed, NOT diarization-based despite what one dossier
  implied) as a secondary check that a clip doesn't start/end mid-topic.
  `metaleey`'s pipeline independently arrived at a similar
  speech-pause-snapping technique — two unrelated real projects converging
  on "don't trust the LLM's raw cut point" is a strong signal this is a
  real, non-optional step, not a nice-to-have.

Finally, **cluster and pad** using `Auto-clipper`'s real `Clusterer.cluster()`
pattern — score → threshold → temporal-cluster-by-gap → pad → clamp/discard
if too short. It's fully decoupled from YOLO in the source (it just
consumes `(timestamp, score)` pairs), so it works unmodified with our
Gemini-based scores instead.

**Correction, 2026-07-30 — don't discard the actual bundled YOLO model,
keep it as a free optional plug-in.** Initially written off as "not
directly reusable" here — wrong call. Checked directly: `Auto-clipper` is
MIT licensed (confirmed via its real `LICENSE` file), the bundled
`best.pt` weights are real, ~5MB, work with zero setup (no API key, no
manual download), and cost nothing to keep. Its 13 classes (`raider`,
`raider-down`, `rocketeer`, `bastion`, `leaper`, `bombardier`, `hornet`,
`wasp`, `snitch`, `pop`, `fireball`, `probe`, `turret`) are entities from
one game, *Arc Raiders*, so that specific bundled model produces zero
signal outside that game. Since `Clusterer.cluster()` already treats the
score source as swappable, keep the real model wired in as an optional,
free bonus signal that activates automatically when a stream is detected
as Arc Raiders (Twitch's stream metadata reports the game category),
stacking with the Gemini/statistical signals rather than replacing them.

**Second correction, from the full 6-repo audit (2026-07-30) — this repo
is far more valuable than the single-game framing above suggested.** A
genuinely thorough file-by-file read (not just the bundled model's own
README) found `Auto-clipper` actually ships **13 selectable detection
strategies** — including undocumented xAI Grok LLM-vision detection,
direct-GraphQL chat-spike detection, and voice-triggered ("clip that")
clipping — and supports **31+ games via a profile system**, not just Arc
Raiders. The single-game YOLO model was only the most visible piece; the
underlying architecture (pluggable detection strategies + per-game
profiles + the same decoupled `Clusterer`) is a real, general framework
worth studying as a whole, not just mining for one bundled model. Also
worth remembering: `models/README.md` documents exactly how to train a
same-shaped model on any additional game via a Roboflow dataset +
`yolo detect train`, if a target streamer plays something outside the 31+
already covered.

**Deferred, not designed for v1**: `metaleey`'s external-behavioral-data
rescoring (cross-referencing real-time viewer/chat time-series against
found segments) is a related but distinct technique from the
analytics-feedback question below — real-time engagement during the
stream, not post-publish performance feedback. Worth a v2 look.

### Stage 4 — Assembly / rendering

- **v1: static vertical crop** — `crop=ih*(9/16):ih,scale=1080:1920`,
  already proven working in `pipeline.py:3522`. Port directly, don't
  rewrite.
- **v2 (deferred, designed, not built): face-tracked dynamic crop** —
  [`openshorts`](https://github.com/mutonby/openshorts)'s `SmoothedCameraman`/`SpeakerTracker` state machines are a
  real, tuned, production design (safe-zone stillness, jump-confirmation
  against detector false-positives, speaker-switch hysteresis+cooldown,
  GENERAL-vs-TRACK scene strategy for group shots). Fully documented in
  `deep_dive_openshorts.md` §7 — build from that design when this becomes
  a priority, don't design from scratch.
- **Captioning**: [No-Code Architects Toolkit](https://github.com/stephengpope/no-code-architects-toolkit) (self-hosted, free, 2.3k
  stars, confirmed via both video research and independent verification)
  or [`ffsubsync`](https://github.com/smacke/ffsubsync) + [`MoviePy`](https://github.com/Zulko/moviepy)/raw ffmpeg for DIY.
- **Audio normalization**: `loudnorm` to -14 LUFS — simple, standard,
  real, include from day one.
- **Fail-fast on content-policy blocks**: port `openshorts`'s
  `GeminiBlockedError` pattern (checks `prompt_feedback.block_reason` and
  per-candidate `finish_reason` against known-blocked values, raises
  immediately instead of retrying — a documented real production incident
  showed retries are pointless here).

### Stage 5 — Distribution

- [YouTube Data API v3](https://developers.google.com/youtube/v3) (real, standard) for Shorts + long-form.
- [`instagrapi`](https://github.com/subzeroid/instagrapi) (now `subzeroid/instagrapi`) for Reels — sandbox carefully,
  its own docs warn private-API automation is fragile.
- Real cross-posting SaaS alternatives if DIY posting becomes too much
  overhead: Repurpose.io, Nuelink, or Pabbly Connect (all confirmed real
  via video research, all literally used by their own creators in the
  research set).
- Discord webhook notifier if pursuing the bounty/submission-channel
  monetization path (see business-model note below).

### Stage 6 — Orchestration / infrastructure (port directly from `pipeline.py`)

- `get_secret()` — Colab userdata + env fallback.
- `safe_json_parse()` + `call_gemini_inspector`'s real `response_schema`
  enforcement pattern (compare against [`openshorts`](https://github.com/mutonby/openshorts)'s 3-tier fallback —
  `structured-schema` → `json-text-recovery` → `strict-json` — which is
  more thorough; worth adopting the extra tier).
- Real budget enforcement (`COST_PER_TOKEN`, `DEFAULT_BUDGET_LIMIT`,
  supervisor check between stages) — **upgrade the flat `COST_PER_TOKEN`
  rate to `openshorts`'s real per-model pricing table** (different models
  have very different input/output rates; thinking tokens bill at the
  output rate even though invisible — see `deep_dive_openshorts.md` §4).
- Retry/dead-letter supervisor pattern (`_write_dead_letter`).
- [SQLite](https://www.sqlite.org/) for idempotent VOD tracking (never reprocess the same VOD twice
  across restarts) — real, standard, multiple sources converge on this.

### The differentiation opportunity: real analytics feedback

**Confirmed via full-transcript research across all 17 videos: nobody in
this space closes the loop on real post-publish performance data.** What
exists is pre-publish prediction (virality scores) or aggregate
cross-creator pattern-matching — never "check what actually happened to
MY last 10 clips and adjust." `pipeline.py` already has a scoped-but-unbuilt
design for exactly this (`analytics_feedback_agent` /
`algorithm_evolution_agent`, needs real YouTube Analytics OAuth for
retention-curve data) — a ready-made starting point rather than a blank
page, documented in `research/RESEARCH_YOUTUBE_SOURCES.md`. Not a v1
requirement, but the single clearest way this project could do something
genuinely novel rather than replicating the existing SaaS landscape.

### Business-model fork (decide before scaling)

Two distinct paths, confirmed real via research, with different
legal/rights implications:
1. **Run your own channel** — clip your own or licensed content, build a
   compilation channel. What this whole architecture assumes by default.
2. **Paid clip-farming** — clip *other* streamers' content for
   bounty/marketplace payouts ([Whop Clipping](https://whop.com/), Biro, Discord submission
   economies, all confirmed real). Different rights situation (clipping
   someone else's stream under a bounty program's terms, not your own
   content) — worth a deliberate choice, not a default.

## Pre-flight checklist (must pass before writing pipeline code)

- [x] `ffmpeg` dependency plan (auto-installs in Colab, checked locally too)
- [x] `GOOGLE_API_KEY` real-call check
- [ ] Twitch Developer Console app created by user (Client ID + Secret) —
      **blocked on user**
- [ ] `validate_environment.py` actually run successfully end-to-end with
      real credentials
- [ ] Confirm the Get Clips endpoint returns real data for at least one
      target broadcaster (decide which channel(s) to target first)
- [x] Primary highlight-detection signal decided — see Architecture Outline
      (three-stage funnel: statistical pre-filter → cheap LLM score →
      expensive LLM detail)

## Open decisions / blockers

- **Twitch Developer credentials** — only the user can create these
  (requires their own Twitch login). Guidance given; not yet confirmed done.
- **Target broadcaster(s)** — not yet chosen. Needed to test Get Clips for
  real and to scope the first end-to-end run.
- **Primary highlight-detection signal — resolved by the architecture
  outline above**: a three-stage funnel (statistical pre-filter → cheap LLM
  score → expensive LLM detail), not a single signal. Get Clips, audio-RMS
  spikes, and chat velocity all feed the pre-filter stage.
- **[Get Clips](https://dev.twitch.tv/docs/api/reference/#get-clips) vs. [Create Clip](https://dev.twitch.tv/docs/api/reference/#create-clip) — real auth difference, confirmed 2026-07-29
  via Twitch's own docs:**
  - `GET /helix/clips` (read viewer-made clips) only needs an **app access
    token** (`client_credentials` grant, just Client ID + Secret) — this is
    what `validate_environment.py`'s `check_twitch_credentials()` already
    tests.
  - `POST /helix/clips` (**Create Clip** — programmatically cut a brand-new
    clip at an exact self-detected timestamp, not just read what viewers
    already made) requires a **user access token with the `clips:edit`
    scope** — i.e., real OAuth authorization-code flow with the
    broadcaster's login/consent, not just a Client ID + Secret. Materially
    bigger scope of work if we ever want self-directed clipping instead of
    only surfacing viewer-curated clips.
  - Decision not yet made: start with Get Clips only (simpler, no user
    login needed, viewer-curated signal) and treat Create Clip as a later
    capability, or build the OAuth flow now. Leaning toward starting with
    Get Clips per the "prove the simple thing works first" discipline.

## Backlog

### Queued for a future session (explicitly deferred 2026-08-01, budget-conscious stopping point)

- **Continue the Hugging Face deep dive.** 3 agents already covered audio/
  transcription, vision/face-detection, and local-LLM/judging (see Current
  Status above and `reference/handoff_2026-08-01_evaluation.md` §5 for
  full findings) — user asked to continue this further; scope for the next
  pass not yet defined (candidates: datasets, more Spaces, TTS/voice-clone
  models for the deferred multi-language scaling idea, or actually
  prototyping the concrete candidates already found).
- **THIS WAS THE MAIN TASK of this session's second half — re-run it
  first, before anything else, next session.** 3 background agents were
  launched 2026-08-01 to re-mine material not yet personally re-read (the
  3 `deep_dive_*.md`/`verified_tools_catalog.md`/`gemini_suggestions.md`
  docs; the 5 trustworthy Gemini dossiers + `RESEARCH_YOUTUBE_SOURCES.md` +
  `tool_verification.md`; the two `fresh_pass_videos` 17-video re-reads)
  for complete/portable code, fixable code, unutilized free tools,
  efficiency paths, and corrections — same 5-lens criteria already applied
  successfully to the Hugging Face pass. **They produced zero output.**
  Confirmed via direct `SendMessage` attempts that all 3 were stopped —
  not a session-limit failure like the separate Hugging Face batch — and a
  full search of the session temp directory found no partial transcript
  for any of them anywhere. Real, unrecovered lost work; not spun otherwise.
  **The exact original prompts (verbatim, ready to paste, no edits) are
  saved in
  [`reference/PENDING_agent_prompts_resume_2026-08-01.md`](reference/PENDING_agent_prompts_resume_2026-08-01.md)
  — resume from that file, not from memory of what these were about.**
  Categories A-E of the Master Source Index in the prior session's plan
  file are NOT agent-dependent (built from material already read directly)
  and remain valid regardless of when this pass gets redone — but the
  user's own priority is this specific re-mine, not a substitute for it.
- **Opal, Vercel, and Claude Cowork** — user asked about these as
  "tools like this" for loading modules/extending Claude. Findings so far:
  **Opal** is real — Google's free no-code AI app builder (Gemini-powered,
  US beta), not a strong fit for this pipeline's actual automation (built
  for simple prototyping), but a real option for a throwaway UI without
  code. **Vercel** is a real, well-known app-hosting platform, relevant
  only if a web-based review dashboard ever gets built. **Claude Cowork**
  is real but is a *different Claude product surface* than this one
  (Claude Code CLI) — plugins/skills can't be installed or loaded into
  this session from here. User pasted real documentation on how Cowork's
  plugin system works, preserved verbatim since it's useful if this
  project (or its patterns) ever gets packaged as a Cowork skill/plugin
  later:

  > 1. Manual Plugin Upload
  > For individual users or teams, you can install custom plugins directly:
  > * Navigate to the Cowork tab in Claude Desktop.
  > * Open the Customize menu and select the Plugins tab.
  > * Click "Upload plugin" and select a valid `.plugin` file (a `.zip` archive containing skill and command markdown files).
  > * Once uploaded, the skills appear in your session, and you can trigger them using commands like `/skill-name`.
  >
  > 2. GitHub Syncing (Organization/Team)
  > For teams using Team or Enterprise plans, you can automate plugin management:
  > * Go to Organization settings > Plugins and click "Add plugin".
  > * Select "GitHub" as the source and connect a private repository.
  > * Cowork will automatically sync plugins from the repository. You can enable automatic updates via webhooks for real-time propagation.
  > * Admins can set installation preferences: Installed by default, Available for install, or Required.
  >
  > 3. Using the Skills Toolkit (Open Source)
  > For automating the loading of skills from GitHub repositories mid-session:
  > * The community-developed Claude Cowork Skills Toolkit provides commands like `/skills-load` to clone, discover, and install skills from any GitHub repo without restarting the session.
  > * Install the toolkit by downloading the `.zip` and uploading it as a personal plugin via Customize > Personal Plugin.
  >
  > 4. Skill Configuration
  > Skills are defined in Markdown files with YAML frontmatter:
  > * The frontmatter includes a `description` field using natural language triggers that help Cowork decide when to load the skill.
  > * To ensure consistent loading, add instructions to your `CLAUDE.md` file to explicitly load specific skills at the start of tasks, as relying solely on auto-trigger descriptions can be unreliable.
  >
  > Note: In Cowork, connectors reach external services through Anthropic's cloud, not your local network. Ensure any custom connectors point to publicly reachable servers.

  (Independently confirmed real via web search: Anthropic did launch
  Cowork plugin support, includes GitHub-sync and an official/community
  marketplace — see `support.claude.com` and `github.com/anthropics/
  claude-plugins-community`/`knowledge-work-plugins`.)
- **Phase 2/3 code work** (fixing `pipeline_transcription_engine.py`'s 4
  documented gaps, building the transcription engine for real, testing
  against a local sample file) — explicitly held out of this session's
  scope; see the prior session's plan file for the exact gap list.
- **Re-evaluate `chat_downloader`/`chat-analyzer`** for Stage 1 given the
  real crash found this session — either wrap defensively or pick a
  different primary chat-mining tool before relying on it.

### `validate_environment.py` — 8 real defects found by audit 2026-07-30, FIXED 2026-08-01

**Status: fixed.** A newer local version already had all 8 addressed
(retry/backoff, treats "returned without raising" as success, token cap +
tracking, incremental print-as-you-go with early short-circuit, uses
`get_secret()` throughout, single shared token exchange, guards against a
`None` token) — diff-confirmed against this description, swapped in for
real this session. Kept below for the historical record of what was wrong.

Found by reviewing the file against `pipeline.py`'s `validate_api_keys`
(pipeline.py:3888). None are syntax errors — the file compiles and lints
clean. All are behavioral regressions or design flaws.

**Behaviors that exist in `validate_api_keys` and were dropped here:**
1. **No retry.** `pipeline.py:3894-3898` documents this exact bug being
   fixed there: a single call hard-exits the whole run on a transient
   network blip during the validation ping itself. Fixed there with 3
   attempts + `sleep(2)`. Reintroduced here.
2. **Empty reply treated as failure** (`_test_text_model_candidate`,
   line 67-69). `pipeline.py:3909-3919` documents this causing **two real
   false failures in one session** — `resp.text` came back `None` on one
   model and `""` on another, neither meaning the key was broken. Fixed
   there by treating "returned without raising" as success. Reintroduced
   here.
3. **No `max_output_tokens` cap** on the validation ping. Original caps at
   50. Combined with defect 4 below, this made pre-flight cost *worse*.
4. **No `_track_tokens()`** — the pre-flight's own cost is invisible.

**Design flaws introduced here:**
5. **All checks execute before anything prints** (line 177-182): the list
   is built by calling all four functions, so you wait through every API
   call and network timeout with zero output. Also means
   `check_twitch_get_clips` fires even when `check_twitch_credentials`
   already failed — wasted calls, confusing cascading error.
6. **Line 181 bypasses `get_secret()`** — reads `os.environ` directly for
   `TARGET_BROADCASTER` while every other credential goes through
   `get_secret()`. Setting it as a Colab secret silently does nothing, in
   a script written specifically for Colab.
7. **Duplicated token exchange** (lines 150-155) — re-implements the
   identical POST from `check_twitch_credentials` instead of calling it.
8. **Unhandled `token is None`** (line 155) — if the token fetch fails,
   builds a `Bearer None` header and fires two more requests, producing a
   confusing 401 instead of a clear "token exchange failed."
   Related: line 35's `apt-get install` discards output with
   `check=False`, so a failed ffmpeg install gives no signal.

**Also worth fixing in `validate_api_keys` itself** (the "working" version
is not clean either): line 3965 `requests.get(url)` has no timeout while
the ElevenLabs call three lines down does; line 3964 puts the API key in a
URL query string rather than a header; line 3904 uses a hardcoded `MODEL`
while the same function calls `get_working_model()` for image and TTS.

**Recommended fix:** keep `validate_environment.py`'s structure (decomposed
functions returning `(bool, str)`, data-driven hard/soft flag — genuinely
better than the 105-line monolith), port the four dropped behaviors into
it, fix defects 5-8. Do not rewrite either file from scratch.
