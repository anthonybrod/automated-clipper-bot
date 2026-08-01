# Evaluation of the 2026-08-01 Gemini handoff round

Kept deliberately separate from the verbatim record in
`handoff_2026-08-01_chat_pasted_originals.md` and the other
`handoff_2026-08-01_*` files — this file is analysis/commentary, not
source material, per this project's standing rule that the two never blend.

Everything here treats Gemini output as reference only, per standing
project rule, and per this session's explicit process with the user: ask
before adopting anything as an actual rule; independently verify anything
checkable against real source.

## Gemini's "3 Deep Rules" — resolved one at a time with the user

1. **"Proven Parts List"** (give Claude `SALVAGE_INVENTORY.md` so it
   doesn't re-derive already-fixed JSON-parsing/token-tracking logic) —
   **user-confirmed true.**
2. **"Shadowban & Algorithm List"** (Z≥2.5 chat-velocity over raw keyword
   counting) — the "you already identified this" attribution was false and
   dropped; the underlying technical content is independently real
   (sourced to `twitch-clip-miner`, see `verified_tools_catalog.md`) and
   restated without the borrowed narrative.
3. **"Fail-Closed Protocol"** — adopted, explicitly scoped: AI
   judge/verification calls (hook-quality scoring, TOS/content checks,
   Ollama context-check) must treat any exception or unparseable response
   as reject, never silently as pass — mirrors the already-proven
   `call_gemini_inspector` pattern in the sibling project's `pipeline.py`.
   Explicitly **not** applied blanket-everywhere: `validate_environment.py`'s
   hard-block-vs-soft-warn distinction and human-review-gate timeout
   behavior are deliberately left as their own separate logic — a blanket
   rule would have overridden those correctly-different judgment calls.

## Gemini's "Power-Ups" + "Last Mile" lists — resolved one at a time

- **Dropped, confirmed contamination**: "Mix Narration (100%)/Music (15%)/
  SFX (10%) to maintain mentorship tone" — this pipeline has no narration
  track (raw streamer audio is the source); "mentorship tone" is language
  bled in from the sibling Parents Teach Kids project.
- **Already covered**: "Fail-Closed" restated, and "The Director Rule" for
  Hook Quality/TOS Blur — both just restate the Fail-Closed rule above.
- **Already independently verified real**: `snap_clip_to_words()` port
  priority (see §2 below for the one part of its description that was
  wrong).
- **Rate-limiting claim → unverifiable, treated as not-fact**: Gemini
  claimed the user "already experienced" `chat-downloader` rate-limiting;
  the user could not confirm this (the one real crash found in the actual
  notebook, see §3, was a `KeyError`, not a rate-limit error). Not treated
  as history. **Adopted as a rule anyway, on its own merits**: Tenacity
  exponential backoff + jitter on `chat-downloader` calls — sound defensive
  practice given the integration is already proven fragile, independent of
  the disputed backstory.
- **WhisperX-as-primary claim → rejected.** faster-whisper stays primary,
  as already established in this project's verified Architecture Outline
  (WhisperX/Parakeet remain optional upgrades, not the default).
- **VOD-list caching → adopted, extended**: content-hash caching (skip
  re-querying Twitch if the source manifest hasn't changed) plus URL,
  title, and content notes per VOD, mapped onto the real `pipeline_tasks`
  schema found in `Lacy_Clip_Bot`'s SQLite DB (see §4) rather than designed
  from scratch.
- Two low-risk standard technical facts adopted without needing a
  true/false ask: `-movflags +faststart` on MP4 exports; `.ass` format
  with `\an5` centering for karaoke captions (never plain `.srt`).

## 1. The 78-source "Definitive Master Tool & Resource Directory" — verified

Split across 4 parallel background agents, real GitHub/PyPI/web checks.

**4 confirmed hallucinated attributions** (real tool exists, wrong owner
claimed):
- `cut-the-crap` claimed as `vantezzen/cut-the-crap` (404) → real repo is
  `jappeace/cut-the-crap` (115★, dormant since 2022). vantezzen's actual
  project is an unrelated browser extension (`skip-silence`).
- Camoufox claimed as `berstend/camoufox` (404) → real repo is
  `daijro/camoufox` — 10,674★, actively maintained, far bigger/more
  legitimate than implied. berstend is real but owns an unrelated project
  (`puppeteer-extra`).
- ffsubsync claimed as `agnostic-apollo/ffsubsync` (404) → real repo is
  `smacke/ffsubsync` (7,808★) — exactly what this project's own earlier
  research already had correct.
- `CanadianZombies/download-twitch` — real repo/URL, but the claimed
  capability ("rip time-segments from a stream") is fabricated; source-read
  confirms it's actually a Discord clip-reposting bot polling Twitch's
  Clips API, no VOD/timestamp logic at all.

**MediaPipe "Face Mesh" confirmed wrong, independently, three separate
times this session** (the Deep Technical Supplement above, this
directory, and a dedicated Hugging Face pass): the correct component is
lightweight Face Detection/BlazeFace, not the heavier Face Mesh (which
runs BlazeFace internally plus two more model stages for 478-point
landmarks, built for filters/avatars — real, verified via Google's own
docs and the real `openshorts` source).

**7 more real-but-exaggerated**: IcePanorama/TwitchClipsDLer (manual
paste-one-at-a-time, not bulk auto-discovery of "hundreds" of clips),
FunClip ("blazing-fast"/"consumer hardware" not in its own README — Whisper
mode is actually GPU-heavy), auto-editor ("zero motion *or* audio"
overstates a threshold-based, one-mode tool), rembg (built for still
images, not "webcam"/live), EditThisCookie ("session JSON pools" isn't a
real feature — plain cookie export/import), GeckCore/TikTok_Bot (real but
0-star, dormant 4 months), ViralContent-Factory (real but zero actual
Twitch relevance — it's a Reddit-story-to-video tool).

Everything else in the directory (~40 items — yt-dlp, chat-downloader,
faster-whisper, ClipsAI, Ollama, Playwright, instagrapi, LangGraph,
OpenShorts, Auto-clipper, etc.) checked out clean.

## 2. `snap_clip_to_words()` — the real algorithm, vs. the false claim

The Deep Technical Supplement claimed it "snaps proposed float boundaries
to the nearest 0.1s silence gap." **False, checked directly against the
real `openshorts` source** (`clip_selection.py`, cross-referenced with
`deep_dive_openshorts.md`): it snaps onto real **word-boundary
timestamps** from the transcript (from faster-whisper/Parakeet word-level
output), then adds lead/tail padding into the surrounding silence — up to
**0.35s lead, 0.45s tail**, not "nearest 0.1s." No "0.1s" figure appears
anywhere in the real logic.

## 3. The real `chat_downloader` crash (first-hand evidence, not a claim)

`AI\auto clipper bot #2\Copy of CLIPPING BOT.ipynb`, cell 2, is a real,
executed Colab notebook cell — an `AsyncSignalListener` built on
`chat_downloader.ChatDownloader()`. Running it against "Lacy" produced a
real, reproducible `KeyError: 'data'` inside `chat_downloader`'s Twitch
GraphQL path, specifically `twitch.py`'s `get_chat_by_stream_id()`:
`self._download_gql(query)[0]['data']['user']` — the GQL response lacked
a `'data'` key entirely. This is the actual, first-hand occurrence of the
"Rigid Third-Party API Parsing" failure mode the handoff's own Session
Error Log (Part 4, item 4) describes in the abstract — confirmed real, not
theoretical. `chat-analyzer` (David-Fryd, verified separately as real but
unmaintained since 2022) is built directly on `chat-downloader` and
inherits this same fragility.

## 4. The real, found `pipeline_tasks`/`payout_logs` schema

`AI\auto clipper bot #2\Lacy_Clip_Bot-...zip` contains no source code, but
a real (empty, schema-complete) SQLite DB, `pipeline_master.db`:

```sql
CREATE TABLE pipeline_tasks (
  id TEXT PRIMARY KEY, vod_url TEXT, start_time FLOAT, end_time FLOAT,
  status TEXT, tier1_path TEXT, tier2_path TEXT
);
CREATE TABLE payout_logs (
  task_id TEXT, platform TEXT, post_url TEXT, view_count INTEGER,
  payout_status TEXT
);
```

Adopted Rule 7 (VOD-list caching) extends this real schema rather than
designing a new one — the `tier1_path`/`tier2_path` columns confirm the
dual-tier design was already being coded toward even before this session.

## 5. Hugging Face research (3 parallel agents, real model-card verification)

**Audio/transcription**: `distil-whisper/distil-large-v3` (6.3x faster than
large-v3, ~0.2% WER difference, documented faster-whisper compatibility)
and `deepdml/faster-whisper-large-v3-turbo-ct2` (drop-in CT2 weights) are
genuine upgrade candidates. Correction to the research premise: faster-
whisper's own `vad_filter` already runs Silero VAD internally — "VAD
alternatives" was close to a non-question. `MIT/ast-finetuned-audioset-10-10-0.4593`
(or lighter `nicofarr/panns_Cnn14`) is the real answer to "detect
screaming/shouting from raw audio," confirmed against AudioSet's actual
ontology. `FunAudioLLM/SenseVoiceSmall` is a "sounds right, isn't" case —
no screaming/shouting class on its own card despite the name, plus an
ambiguous license.

**Vision/face-detection**: MediaPipe BlazeFace reconfirmed correct a third
time (every alternative checked is either the same model repackaged or
heavier with no speed win). `dima806/facial_emotions_image_detection`
(Apache 2.0, 54K downloads/mo, 91% claimed accuracy) and `py-feat/resmasknet`
(MIT, actively maintained) are real upgrade candidates over the existing
`fer` tool. No general "which game is being played" HF model exists — real
gap, confirms Twitch's own category API is the right source of truth, not
a vision model. Two more confirmed Space "name traps" (`dvpearl/REFRAME`
is an LLM text-tone-rewriter, not a video tool, despite the name).

**Local LLM/judging**: Llama 3.2's native tool-call format is Pythonic
list syntax, not JSON — its own model card doesn't mention a JSON mode.
`meta-llama/Llama-Guard-3-1B` (same weight class as the current model,
first-party `ollama pull llama-guard3:1b`, 13 real harm categories) is a
clean, concrete fit for the Fail-Closed content-safety check. No
purpose-built "hook quality"/engagement scorer exists on HF — real gap,
confirmed by search; closest proxies are generic sentiment/emotion models,
none validated against real engagement data. Load-bearing finding:
Ollama's `format: json` (grammar-constrained decoding) may fix JSON
reliability more reliably than swapping models at all — worth checking
whether existing Ollama calls already use it before adding model
complexity. `Salesforce/xLAM-2-3b-fc-r` and `Qwen2.5-3B-Instruct` are real
but carry non-commercial-only licenses — hard skip for a monetized channel.

## 6. Two files falsely labeled "un-edited original" this session

- `CLIP BOT STUFF`'s own Gemini-authored reconstruction of
  `SALVAGE_INVENTORY.md` (a "Gem" knowledge-base export) — thin (58 lines
  vs. the real 495) and contains at least one unverifiable claim (`fcntl`
  locking) absent from the real inventory.
- The `Originals\` folder found later in the session (`ARCHITECTURAL_BLUEPRINT.md`,
  `SALVAGE_INVENTORY.md`) — 12–16 line condensed re-summaries carrying the
  source doc's `[cite: ###]` markers, explicitly labeled "UN-EDITED
  ORIGINAL" despite being neither un-edited nor original. Same
  condensed-but-labeled-verbatim failure this project's own history
  (`claude_failure_report.md`) already documents, from a different source.

Neither is used as a source anywhere in this project. The real, full
versions already exist: this repo's own `SALVAGE_INVENTORY.md`, and
`handoff_2026-08-01_master_planning_session_raw.md` /
`handoff_2026-08-01_78source_tool_directory.md` for the architecture
material.
