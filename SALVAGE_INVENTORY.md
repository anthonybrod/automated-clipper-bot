# Salvage inventory — verified-working code from `youtube-auto-videos`

**Full re-read completed 2026-07-30**: every one of `pipeline.py`'s 4,059
lines was read top to bottom, in sequential ~500-line chunks, start to
finish — not sampled, not recalled from memory, not re-derived from the
first pass's summary. Every line number below was re-verified against the
current file (via direct `Read` + a structural grep of every `def`/`class`/
top-level constant) on this date, superseding the previous version of this
document's citations. Where a citation is unchanged from the prior pass,
that's because the file genuinely hasn't shifted at that location, not
because it went unchecked.

Source repo: `C:\Users\AwBro\Desktop\youtube auto videos\pipeline.py`
(4,059 lines, single file, LangGraph `StateGraph` pipeline for a
completely different domain — automated kids'-education DIY videos, no
Twitch/clip logic anywhere in it).

Now cross-referenced against the clipper-bot's actual target architecture
(`PROJECT.md`'s Architecture Outline: 6-stage pipeline — ingestion,
transcription, three-stage highlight-detection funnel, assembly/rendering,
distribution, orchestration) — the first salvage pass predates that outline
being fully worked out, so several real, useful patterns in `pipeline.py`
weren't yet recognized as applicable. This pass adds them.

**Net result of this pass: 30 real, distinct patterns beyond what the
previous version of this document had** — most significantly the full
`cognitive_ai_supervisor` retry/dead-letter/budget state machine (only its
budget check was previously documented), the entire human-review-gate
system (not mentioned at all previously), the LangGraph checkpointer setup
with a real confirmed async-vs-sync gotcha, `bootstrap_workspace()` itself
(the user asked specifically about this one and it was missing from the
prior document entirely), the tiered-fallback-chain shape that directly
maps onto the architecture outline's own planned yt-dlp→
TwitchDownloader-technique and faster-whisper→Parakeet fallbacks, and the
post-assembly video-corruption QA pattern. Details below, organized the
same way as before (directly portable / portable with adaptation /
conceptually relevant / not salvaged), with every new find marked **NEW**.

---

## Directly portable (small, self-contained, no project-specific coupling)

| Function | Location | What it does | Why we need it here |
|---|---|---|---|
| `get_secret(key)` | `pipeline.py:74` | Reads `google.colab.userdata` first if running in Colab, falls back to `os.environ`. | Every credential (Google/LLM API key, Twitch Client ID/Secret) needs this exact pattern. |
| `safe_json_parse(text, model=None)` | `pipeline.py:319-363` | Repairs/parses LLM JSON output through a chain of increasingly aggressive passes: raw parse → strip markdown fences → un-escape stray `\'` → strip trailing commas → extract the outermost `{...}` if trailing junk follows it. | Directly needed for the cheap/expensive LLM score+detail stages' JSON output (stage 3). |
| `_track_tokens(resp)` / `get_session_tokens()` | `pipeline.py:383` / `pipeline.py:389` | Accumulates real token usage from `usage_metadata` across a run via a module-level running total, read cumulatively by every supervisor pass instead of each node computing its own delta. | Needed for real cost tracking from day one — this is the actual mechanism behind the "port budget enforcement from day one" instruction in the Architecture Outline. |
| `_new_temp_path(suffix)` / `cleanup_temp_files()` | `pipeline.py:400` / `pipeline.py:405` | Temp-file hygiene: every temp path handed out gets tracked in a module-level list; one call at the very end (in `__main__`'s `finally`, see below) sweeps all of them regardless of success/failure/exception. | Same need here — downloaded VOD segments, intermediate ffmpeg outputs, extracted QA frames. |
| **NEW** `bootstrap_workspace()` | `pipeline.py:153-216`, called unconditionally at module load (`pipeline.py:216`) | The user asked specifically about this one. Idempotent workspace scaffolding: a fixed list of directories gets `Path(d).mkdir(parents=True, exist_ok=True)` plus a `.canary` file written into each (a cheap real-write-permission check, not just an existence check — catches a read-only-mount failure mode `exist_ok=True` alone wouldn't). Then seeds a handful of config/state JSON files **only if they don't already exist** (`if not rubric.exists(): rubric.write_text(...)`, repeated per file) — a QA-rubric-style criteria file, an episodic-memory file, an evolution-log file, a dead-letter queue file (seeded as `"[]"`), and a curated-topic-rotation fallback file. Never overwrites a file a previous run already created/modified. | Directly reusable shape for the clipper bot's own workspace: `candidates/`, `transcripts/`, `clips_out/`, `dead_letter/`, `checkpoints/`, plus first-run-only seed files for a clip-scoring rubric (thresholds for the statistical pre-filter and the cheap/expensive LLM stages) and a dead-letter queue. The "write a canary file to prove real write access, not just directory existence" detail is a real, cheap defensive habit worth keeping, not just decoration. |
| **NEW** Colab conditional-bootstrap block | `pipeline.py:20-58` (`if "google.colab" in sys.modules:` ... ) | Runs *before* any third-party imports (a real ordering bug was fixed here — confirmed by an actual `ModuleNotFoundError` on a fresh Colab runtime when this block previously sat later in the file): installs `ffmpeg` + pip packages only when actually running in Colab, then applies `nest_asyncio.apply()` so the rest of the file's plain `asyncio.run(...)` call sites (used throughout `__main__`) work unmodified both inside Colab's own already-running event loop and as a normal standalone script outside it. Also attempts a Google Drive mount, wrapped in `try/except` so a declined/failed mount degrades to local-only artifacts rather than aborting the run. | If the clipper bot ever runs a Colab-hosted GPU path (already noted in the Architecture Outline for Parakeet transcription), this exact block — env-conditional dependency bootstrap, placed before any third-party import, plus the `nest_asyncio` patch for `asyncio.run()` compatibility inside Colab's own loop — is the proven fix for a real, previously-hit bug class, not a guess. |
| **NEW** `get_ffmpeg_codec()` / `GPU_CODEC` | `pipeline.py:218-224` | Real hwaccel detection: runs `ffmpeg -hwaccels`, checks for `"cuda"` in stdout, returns `"h264_nvenc"` if present else `"libx264"`. Paired with a codec-fallback loop at the actual encode call site (`assembly_agent`, `pipeline.py:3514`: `for codec in [GPU_CODEC, "libx264"]:` — tries the detected codec first, falls back to software encode on failure, rather than trusting detection alone). | Stage 4 (rendering) should detect-and-use GPU encode when available (relevant given the architecture outline's own GPU-Parakeet discussion) but must never *only* trust detection — always have a working software-encode path in the actual command. |
| **NEW** `log_event(etype, data)` | `pipeline.py:371-373` | One-line structured audit-log append: `{"timestamp":..., "event_type":..., **data}` as a JSONL line. | Trivial but real — the same shape belongs in Stage 6's orchestration/audit trail (which VOD was processed, which clips were dropped by the diversity guard, why a stage retried). |
| **NEW** `validate_vault_path(p)` | `pipeline.py:368-369` | Path-traversal guard: confirms an output path actually resolves to somewhere inside the workspace root before writing to it. | Any pipeline that constructs output paths from LLM-influenced or otherwise dynamic strings (a proposed clip filename, a downloaded VOD path) should validate the resolved path stays inside the intended output tree before writing/moving. |
| **NEW** `sanitize_text(text)` | `pipeline.py:365-366` | Strips control characters, backtick code-fences, and the literal phrase `"Ignore all previous"` from any text before it's used. | **More directly relevant here than in the source project.** The source project only ever runs this on its own YouTube-transcript ingestion. The clipper bot's Stage 1 ingests Twitch **chat messages** — literally attacker-controlled, untrusted text — before any of it reaches an LLM prompt in the highlight-detection funnel (stage 3). A basic injection-guard sanitizer on all ingested chat/transcript text before it's embedded in a scoring prompt is a real, cheap, appropriate defensive step; this is the exact function to start from. |

---

## Portable with adaptation (real pattern, needs a new schema/domain)

### Model discovery, validation, and structured-output enforcement

| Function | Location | Pattern to reuse | Adaptation needed |
|---|---|---|---|
| `call_gemini_inspector(...)` | `pipeline.py:736-816` | Real `response_schema=` passed into `generate_content` config for **server-side JSON schema enforcement** (`pipeline.py:763-769`) — stronger than `response_mime_type: application/json` alone. **Beyond what was previously documented**: this function has a **third repair tier** beyond `safe_json_parse`'s own chain — if every parse attempt still fails, it regex-extracts just `"pass"` and `"reason"`/`"critique"` directly out of the raw text (`pipeline.py:789-808`) rather than discarding a response that contains a real verdict but has one malformed field elsewhere in it. It also **fails closed**: any exception in the whole call is reported as `(False, "...", {"pass": False, "error": True})`, never silently treated as a pass (`pipeline.py:810-816`) — a broken/unreachable judge call must never let bad content through a gate. | Swap `InspectorVerdict` for a `HighlightCandidate`/`ClipTarget`-style Pydantic model (start_time, end_time, score, hook_reason, hook_pattern) for the LLM score/detail stages. Keep the 3-tier repair chain and fail-closed default as-is — both are domain-agnostic. |
| **NEW** — `response_schema` generalizes beyond `InspectorVerdict` | `pipeline.py:2163`, `2206` | `script_team_leader` passes a completely different Pydantic model (`MentorScriptVariants`, `MentorScript`) as `response_schema` directly on a raw `client.models.generate_content(...)` call, not through `call_gemini_inspector` at all. | Confirms the technique isn't tied to the inspector helper — any `generate_content` call, including the cheap-score and expensive-detail LLM calls in stage 3, can pass its own schema directly the same way. |
| `get_working_model(capability, default)` / `discover_best_working_models(...)` | `pipeline.py:601-608` / `pipeline.py:674-734` | Tests real candidate models against the actual account/quota before committing, ranked best-first, caches result to a JSON file read by generation code automatically. | Directly reusable concept for picking which LLM handles the cheap-score vs. expensive-detail calls — avoids repeating the zero-quota-model mistake. |
| **NEW** `_model_quality_rank(name)` | `pipeline.py:610-618` | The actual sort key behind "best-first": tier 0 if `"pro"` in the name, 1 if not `"lite"`, else 2; a `preview_penalty` of 1 if `"preview"` in the name (non-preview preferred, less likely to be deprecated mid-project — happened twice already in the source project). | Reusable heuristic for ranking candidate models within a tier when picking which cheap-scoring or expensive-detail model to prefer. |
| **NEW** `_test_image_model_candidate` / `_test_tts_model_candidate` | `pipeline.py:620-649` / `pipeline.py:651-672` | **This is the actual mechanism**, not just the wrapper: one real, minimal generation call per candidate model, checking for the real non-exception failure mode (`candidate.content is None`, with a real `finish_reason`) before declaring success. This is the concrete implementation behind "prove every hard dependency before writing a real pipeline stage" — the discipline the clipper bot's own `CLAUDE.md`/`PROJECT.md` explicitly cites as the standard to match. | Write an equivalent `_test_llm_candidate(model_name)` that does one cheap real scoring call and checks for a genuine response before either the cheap-score or expensive-detail stage model is locked in for a real run. |

### Asset/reference reuse — locked-once, hash-invalidated caching

The previous version of this document only had a vague one-line mention
("cache a broadcaster's VOD list instead of re-querying"). The actual
mechanism is fully worked out in the source and worth citing precisely:

| Function | Location | Pattern |
|---|---|---|
| `get_style_anchor_images()` / `get_music_anchor_audio()` / `get_sfx_anchor_audio()` / `get_voice_anchor_audio(_all)` | `pipeline.py:1013-1080` | **Folder auto-discovery**: drop a file in a well-known folder, the pipeline picks it up automatically with zero code change; returns `None`/`[]` cleanly if the folder is empty or absent, degrading to today's exact behavior. |
| `_bible_visual_hash` / `_anchor_images_hash` / `_object_visual_hash` | `pipeline.py:1082-1088`, `2342-2353`, `2566-2567` | **Content-hash cache invalidation**: a locked/generated artifact is cached keyed on a hash of the *inputs that produced it* (bible text + a cheap mtime+size fingerprint of every anchor file), not just presence-on-disk — so changing the underlying source (a rewritten prompt, a swapped reference image) invalidates the cache instead of silently reusing a now-mismatched artifact. |
| `load_object_library` / `save_object_to_library` / `get_object_sheet_paths` | `pipeline.py:2534-2634` | A **named library** of persistent, reusable entities in one JSON file per channel, with an `always_present` flag for a fixed recurring set vs. dynamically-added per-topic entries, each independently hash-invalidated. |

This is the concrete, reusable implementation behind the "asset reuse
strategy" already in cross-session memory
(`project_asset_reuse_strategy`). Directly applicable to caching a locked
per-streamer profile (recurring bits/catchphrases, or — as the
Architecture Outline already separately proposes for `Auto-clipper` — a
per-game YOLO model selection), invalidated by content hash rather than by
presence alone, instead of re-deriving it every run.

### Rule-of-3: generate N, score differentiated, synthesize if none pass

Previously listed only as "conceptually relevant, not literally
reusable." On this full re-read, it's a repeated, consistently-applied
pattern across **five** independent call sites, and it maps onto a real
Architecture Outline requirement — stage 3's expensive-detail LLM call is
specified to produce "title/hook/description copy" using "a named hook
pattern library... fed to the LLM as options." Rule-of-3 is the direct,
already-proven mechanism for exactly that: generate N hook/title
candidates, have the LLM score each 1-10 with real differentiation
(explicitly instructed not to give every option the same score), take the
highest, or synthesize one improved version from all N if none clears a
minimum bar.

| Function | Location |
|---|---|
| `select_delivery_style_variant` | `pipeline.py:1124-1171` |
| `select_visual_style_variant` | `pipeline.py:2476-2521` |
| `supervisor_score_script_variants` / `_synthesize_improved_script` | `pipeline.py:1926-1947` / `1949-1981` |
| `_synthesize_improved_variant` (shared single-field synthesis helper) | `pipeline.py:2433-2461` |
| `select_distribution_copy_variant` | `pipeline.py:3638-3692` |

Upgraded from "conceptual" to portable-with-adaptation: this is the
concrete design for scoring multiple candidate clip titles/hooks per
moment in stage 3, gated by the same kind of `rule_of_three_min_score`
threshold already implemented, at a real, controllable cost (only the
short text scoring call, not the actual video render).

### Orchestration state machine — the full thing, not just budget

The previous version of this document only cited the budget-enforcement
lines. The user specifically asked for the whole retry-decision state
machine — here it is, verified line-by-line:

**`cognitive_ai_supervisor`** — `pipeline.py:1651-1723`:
1. **State validation gate** (`1654-1656`): hard-fails immediately if
   `project_id`/`channel_name`/`channel_id`/`status` are missing from state.
2. **Real budget enforcement** (`1658-1674`): `current_cost =
   get_session_tokens() * COST_PER_TOKEN` (`577`), compared against
   `state.get("budget_limit") or DEFAULT_BUDGET_LIMIT` (`585`) — checked
   before *both* the retry path and the advance-to-next-stage path, so a
   blown budget stops the run either way, not just mid-retry. Skipped only
   at `status == "INIT"` (nothing spent yet). On exceed: writes a
   dead-letter entry and returns `status: "FAILED"` with the real
   overspend amount in `error`.
3. **Retry/dead-letter decision** (`1676-1691`): reads
   `state["verification_reports"][-1]`; if it failed, checks
   `state.get("fallback_count", 0) < 3` — under 3, returns
   `status: f"RETRY_{agent_name.upper()}"` with `fallback_count+1`; at 3,
   writes a dead-letter entry (`_write_dead_letter`, `1633-1649`) and
   returns `FAILED`.
4. **Degraded-mode tracking** (`1677-1678`): `degraded_mode` is set True
   for the run if *any* prior report had `fallback_used: True` — a
   run can "succeed" while flagged as having used a lower-quality fallback
   somewhere.
5. **Success-path routing table** (`1693-1723`): a flat
   `{current_status_string: next_status_string}` dict driving every
   forward transition (`INIT`→`ALGORITHM_EVOLUTION`→...→`DONE`), and
   `fallback_count` resets to 0 whenever a stage genuinely advances.

**`build_graph`** — `pipeline.py:3822-3885` — the actual wiring: one
`supervisor` node; every real agent node has a plain edge back to
`supervisor` (`wf.add_edge(name, "supervisor")`, `3882-3883`); a single
`wf.add_conditional_edges("supervisor", lambda s: s["status"], {...})`
dict handles *both* the forward-routing table and a parallel
`RETRY_<NODE>` entry for every node — the generic `RETRY_` prefix +
`agent_name.upper()` convention (produced by step 3 above) means any node
becomes retryable with just one more dict entry, no bespoke retry-routing
logic per stage.

This is the concrete "deterministic supervisor router" architecture
`CLAUDE.md` describes for the sibling project, and it is a genuinely
strong fit for the clipper bot's Stage 6 (orchestration/budget/retry) —
applicable at the fine grain of every node transition (ingest → transcribe
→ pre-filter → cheap-score → expensive-detail → snap-to-words → render →
distribute), not just a single coarse per-run budget check.

### Human review gates — entirely missing from the previous document

`pipeline.py:1454-1631` — a full, generic, reusable human-in-the-loop gate
system, never mentioned in the prior salvage pass:

- `get_review_dir` / `get_drive_review_dir` (`1463-1479`): a predictable
  per-run review folder, optionally mirrored to a persistent location
  (Google Drive in the source) if mounted/available, degrading to
  local-only otherwise.
- `deliver_artifacts_to_review` (`1481-1507`): copies (not moves) any
  named artifact into that folder, tolerating missing files/copy failures
  without crashing the run.
- `_render_preview` (`1512-1537`): inline preview when running somewhere
  that supports it (IPython display for image/audio/video in the source's
  Colab case), falling back to a plain path+size print otherwise.
- `_prompt_approval` (`1539-1547`): loops on `input()` until a valid
  y/n is given, optionally captures a rejection reason.
- `human_review_gate` (`1549-1580`): the generic entry point —
  `(state, stage_name, artifact_paths, approved_status, review_note)` →
  delivers artifacts, previews them, prompts, and **returns a
  `VerificationReport`** — meaning a human rejection draws from the
  *exact same* 3-attempt retry/dead-letter budget as an AI QA failure
  (`cognitive_ai_supervisor`'s `RETRY_<AGENT>` path), rather than being a
  second, parallel gating mechanism.
- Four call sites (`script_review_gate`, `image_review_gate`,
  `voiceover_review_gate`, `final_review_gate`, `1599-1631`) show the
  pattern applied per-stage.

**Why this matters here**: the clipper bot's own action-safety rules
require explicit permission before publishing/posting content, and before
any irreversible action. A gate built on exactly this shape — before
Stage 4's expensive render, or before Stage 5's actual multi-platform
post — is a directly reusable, already-proven design for a real go/no-go
checkpoint, not something to design from scratch.

### Tiered fallback chains — a shape, not just individual fallbacks

Two real implementations of the same shape, worth citing together since
the Architecture Outline has *already independently chosen* to build the
identical shape for two different stages without yet having a reference
implementation to build from:

- `_synthesize_speech_segment` (`pipeline.py:3078-3135`): a real
  multi-tier fallback chain (ElevenLabs → Gemini TTS → Google Cloud TTS →
  gTTS), each tier degrading to the next on failure, an env var
  (`VOICEOVER_SERVICE`) can force a specific starting tier, and only the
  final tier's failure is treated as fatal.
- `ingest_agent` (`pipeline.py:3324-3403`): an even longer real chain —
  structured RSS queue → YouTube Data API lookup → Gemini native-video
  transcript → `youtube-transcript-api` scrape (wrapped in a hard
  15-second timeout, see below) → curated static fallback content as the
  absolute last resort. Never raises; always produces *some* usable
  content.

**Direct mapping to the Architecture Outline**: Stage 1 already plans
yt-dlp as primary with `TwitchDownloader`'s lower-level
GraphQL/`usher.ttvnw.net` technique as a documented fallback "if yt-dlp
ever breaks against a Twitch API change"; Stage 2 already plans
faster-whisper as primary with NVIDIA Parakeet as an optional GPU-primary
alternative. Both are exactly this shape — port the *structure*
(try tier 1 → on failure, log why, try tier 2 → ... → only the last
tier's failure is fatal, with an env var/config to force a starting tier
for testing) from `_synthesize_speech_segment`/`ingest_agent`, not their
specific TTS/transcript logic.

- **NEW** `asyncio.wait_for(loop.run_in_executor(...), timeout=15.0)` —
  `pipeline.py:3386-3390`: a real, concrete fix for a blocking sync call
  with no timeout of its own hanging the whole pipeline (confirmed by a
  real run needing a manual `KeyboardInterrupt`). Directly reusable
  wherever the clipper bot wraps a blocking library call with no native
  timeout (a `yt-dlp` download, a `faster-whisper` transcription call,
  a Twitch API request) — enforce a hard ceiling with exactly this
  wrapper rather than trusting the library's own timeout handling.
- **NEW** `_normalize_audio_segment` — `pipeline.py:3137-3152`: documents
  a real, non-obvious ffmpeg gotcha — the **concat demuxer** (unlike the
  concat *filter*) requires matching codecs/timebases across every input,
  so segments produced by different fallback tiers (different encoders)
  must be re-encoded to one fixed spec before concatenation, or the
  result silently breaks with no error until playback. Worth knowing if
  the clipper bot ever concatenates clips/audio pulled from different
  sources or fallback tiers.

### Post-assembly / pre-publish QA — a distinct, missing check

**NEW** `multimodal_qa_agent` — `pipeline.py:3549-3604`: extracts real
frames from the **final, fully assembled** output (via `ffmpeg -ss 2
-frames:v 1` for an early frame, `-sseof -3` for a late one — not from the
generation ingredients) and judges them for a class of problem earlier
per-ingredient QA structurally cannot catch: corruption, blank/black
frames, and encoding artifacts introduced by the assembly/encode step
itself. This is a genuinely distinct QA layer from Stage 3's content
judgment (is this a good highlight) — it's "did the actual render come
out intact." Directly portable to Stage 4: after ffmpeg produces the
final vertical-crop clip, extract 1-2 real frames from it and verify
they're not corrupted before handing off to Stage 5, using the identical
seek/extract command shape.

### Distribution metadata validation against real platform limits

**NEW** `validate_distribution_metadata` — `pipeline.py:3615-3630`, with
real constants `YOUTUBE_TITLE_MAX = 100`, `YOUTUBE_DESCRIPTION_MAX =
5000`, `SOCIAL_CAPTION_MAX = 2200` (`3611-3613`). Checks real,
documented platform limits and empty-field cases *before* a publish call,
rather than reporting success unconditionally regardless of what's
actually in the metadata (which the source pipeline used to do). Directly
applicable to Stage 5 — re-verify the actual current numeric limits for
whichever platforms the clipper bot targets (YouTube Shorts, TikTok,
Instagram Reels) rather than assuming these exact numbers are still
current, but the validate-before-publish *pattern* is real and worth
copying as-is.

### Checkpointer / state-persistence setup — full detail

The user specifically flagged this as something to verify in depth.
Full detail, confirmed against the current file:

**`get_checkpointer`** — `pipeline.py:3757-3803`: tries a real
`AsyncSqliteSaver` (`langgraph.checkpoint.sqlite.aio`, needs the
`aiosqlite` package) pointed at a persistent-storage directory if
available (Google Drive mount, in the source project's case), else a
local `./enterprise_workspace/checkpoints` directory. Falls back to
`MemorySaver()` with an explicit, visible warning if the package/
connection setup fails for any reason — a missing/incompatible package
degrades gracefully rather than crashing the whole pipeline.

**The real, confirmed gotcha** (documented in the function's own
docstring, backed by an actual mocked full-graph-run test): the
**synchronous** `SqliteSaver` (`langgraph.checkpoint.sqlite`, not the
`.aio` variant) exposes `aget_tuple`/`aput` as attributes — `hasattr()`
returns `True` — but *calling* them raises `NotImplementedError` at
runtime, because this pipeline drives the graph via `ainvoke()`.
`AsyncSqliteSaver` is the actually-correct async-capable saver; the sync
one silently looks compatible until it's actually invoked. This is
exactly the kind of gotcha worth pre-empting rather than rediscovering —
if the clipper bot adopts LangGraph for orchestration, use
`AsyncSqliteSaver` from the start if the graph is driven by `ainvoke()`.

**`close_checkpointer`** — `pipeline.py:3805-3821`: must be called before
the async event loop tears down — a real full-run test confirmed skipping
this produces a harmless-but-alarming `RuntimeError: Event loop is
closed` traceback from `aiosqlite`'s background worker thread on
interpreter shutdown (exit code 0, result unaffected, but noisy).

Directly relevant to the clipper bot's own planned SQLite-based
idempotent VOD tracking (Stage 6) *and*, if it adopts LangGraph, to
resuming a run after a crash — this is one of the more concretely
valuable, fully-verified findings in the whole file.

**One honest gap worth carrying over, not just the win**: `pipeline.py`'s
own `__main__` (below) never actually wires up "detect a previous
incomplete run and resume its `thread_id`" — it mints a fresh `thread_id`
every invocation (`f"run_{int(time.time())}"`), so despite having a real
durable checkpointer, the source project hasn't itself finished the part
that gets actual resume value out of it. Don't assume this piece is done
just because the checkpointer plumbing is real — it still needs a
"was there an incomplete run for this VOD? reuse its thread_id" lookup on
top of what's here.

### Pre-flight validation — differential hard-block vs. soft-warn

`validate_api_keys` — `pipeline.py:3888-3992` (previously cited only in
summary; the differential treatment is the real design worth naming):
tests each credential with one real, minimal, cheap call — but treats
failures differently based on whether that stage has a real fallback
chain. The image-generation model check is a **hard block** (`sys.exit(1)`
via the collected `errors` list) because the source pipeline has no
non-Gemini image fallback; the TTS model check is a **soft warning**
because a real fallback chain exists (ElevenLabs/Cloud TTS/gTTS). The
initial Gemini text-model ping additionally retries 3 times with a fixed
`asyncio.sleep(2)` between attempts (`3894-3931`) specifically to
distinguish a transient network blip on the *validation ping itself* from
an actually-broken key — this is the only real sleep-based backoff
anywhere in the file (see the honest gap noted below). The ElevenLabs key
check (`3976-3985`) hits `GET /v1/user`, documented as ElevenLabs'
lightweight account-info endpoint — the general technique ("find the
provider's cheapest real read-only endpoint and call it once, don't spend
real quota just to validate a key") is the same one
`validate_environment.py` already applies to Twitch's `client_credentials`
exchange; worth extending to whichever LLM provider the clip-scoring
stages use.

**Honest gap, not a find to oversell**: beyond that one fixed 2-second
sleep, this file has **no real exponential backoff anywhere** — every
other retry loop (`script_team_leader`'s 3-attempt generation loop,
`cognitive_ai_supervisor`'s 3-retry count) is pure count-based retry with
zero delay between attempts. If the clipper bot needs genuine
exponential backoff (plausible for Twitch API rate limits or repeated
`yt-dlp` failures), there isn't a mature implementation here to copy —
only "retry N times, no delay" and "retry N times, one fixed delay."
Worth knowing before assuming this file already solved that problem.

### Top-level `__main__` invocation shape

**NEW** — the user specifically asked about this; previously undocumented.
`pipeline.py:3995-4059`:
1. `asyncio.run(validate_api_keys())` — hard pre-flight gate, exits before
   anything else runs if any hard-blocking check failed.
2. `app = asyncio.run(build_graph())` — build/compile the graph once.
3. Reads a `CHANNEL_NAME` env var (default fallback) to select which
   target config drives this run — directly analogous to the clipper
   bot needing a "which broadcaster/VOD" selector for a given invocation.
4. Constructs one full `initial` state dict with every field explicitly
   defaulted, including a fresh, real, unique `project_id`
   (`f"live_{int(time.time())}"`) and `budget_limit`.
5. An inner `async def run()` calls `app.ainvoke(initial, {"configurable":
   {"thread_id": f"run_{int(time.time())}"}})` inside `try/finally` that
   always calls `close_checkpointer(app)`.
6. An outer `try/finally` always calls `cleanup_temp_files()` regardless
   of success, `FAILED` status, or a raised exception.
7. Prints a final human-readable summary: total tokens, estimated cost,
   `degraded_mode` flag, fallback count, final status, every output path,
   and a per-agent verification-report breakdown including any
   `failed_reasons` metrics.

This is a clean, reusable top-level shape for the clipper bot's own
entrypoint: pre-flight-validate → build graph once → one big initial-state
dict with a fresh run id → `ainvoke` wrapped for checkpointer cleanup →
outer wrap for temp-file cleanup → final cost/status summary. (Remember
the checkpointer gap noted above: this shape doesn't itself implement
resuming a prior incomplete run — that's still a gap to close, not
something already solved here.)

---

## Conceptually relevant, not literally reusable

- **Asset-reuse/lock-once pattern** (see project memory
  `project_asset_reuse_strategy`) — now backed by a concrete mechanism
  (content-hash cache invalidation, see above) rather than just a general
  idea. Analogous use here: cache a broadcaster's VOD list / already-
  scored clip metadata, invalidated by a hash of the actual query
  parameters or Get Clips response, not just presence-on-disk.
- **"Team leader" stage-agent shape** (e.g. `script_team_leader`,
  `pipeline.py:1983-2268`; `animation_team_leader`,
  `pipeline.py:2636-2836`) — every stage in the source pipeline follows:
  primary generation attempt → bounded retry loop → graceful hardcoded/
  simplified fallback → N QA sub-checks → one aggregated
  `VerificationReport` returned to the supervisor. A reasonable structural
  template for each clipper-bot stage's own top-level function, independent
  of any specific content logic.
- **Graceful degradation to hardcoded fallback content**
  (`robust_transcript_script`/`enhanced_fallback_script`,
  `pipeline.py:1736-1815`) when source data is too thin to work with,
  rather than failing the whole run — e.g., if a VOD genuinely has too
  little chat/audio signal for real highlight detection, falling back to
  evenly-spaced candidate segments rather than hard-failing the run.
- **Post-run smoke test on expected output artifacts**
  (`test_suite_agent`, `pipeline.py:3734-3754`) — the last node before
  `DONE`: checks the final video/thumbnail/short files actually exist,
  the video is above a trivial size floor (not a 0-byte/near-empty
  encode failure that other checks missed), and at least one metadata
  file was written — a final sanity net after every content-specific QA
  gate already ran. Worth an equivalent final check for the clipper bot
  (does the rendered clip file exist and clear a minimum size, does its
  metadata/description file exist) before considering a VOD's run
  complete, though this exact check list is trivial enough to be closer
  to "obviously good practice" than a distinctive pattern worth deep
  study.
- **Standalone, human-run audit utility, non-destructive, report-only**
  (`check_voice_anchor_accuracy`/`run_voice_anchor_accuracy_check`,
  `pipeline.py:1347-1427`) — a Colab-cell utility that audits hand-curated
  reference assets and writes a pass/fail report, never deletes/moves
  anything itself. A loose analog if the clipper bot ever wants a
  by-hand "audit these downloaded chat logs / candidate clips" utility,
  though this is a stretch, not a close match.
- **`analytics_feedback_agent` — precision correction, not a new find**:
  `pipeline.py:3726-3732` is a **minimal stub** — it writes a static
  `{"last_run": ..., "directive": "maintain hooks and pacing"}` to a JSON
  file. It is *not* a built analytics-feedback system, does no real
  YouTube Analytics OAuth call, and computes no retention curve. The
  Architecture Outline's own framing ("a ready-made design... needs real
  YouTube Analytics OAuth for retention-curve data") is already honest
  about this being unbuilt — worth stating precisely here too so nobody
  mistakes the *file-based memory-persistence pattern*
  (`load_episodic_memory`, `pipeline.py:544-548`, and this stub) for an
  actual analytics implementation worth porting wholesale. Only the
  memory-persistence shape (a per-channel JSON file recording a directive
  that future runs read back) is real and reusable; the analytics logic
  itself doesn't exist yet in either project.
- **`fetch_transcript_via_gemini_video`** (`pipeline.py:3291-3322`) —
  considered and explicitly **not a fit**, noted here so it isn't
  rediscovered and re-proposed later: it uses a paid Gemini call for
  video/audio transcription specifically to avoid IP-blocking problems
  with scraping. The clipper bot's Architecture Outline has already
  deliberately chosen `faster-whisper` (free, local) over any paid
  transcription call for cost-philosophy reasons (see "Explicit cost
  philosophy" in `PROJECT.md`) — this function's approach directly
  contradicts that choice and shouldn't be revisited without a specific
  reason cost isn't the deciding factor anymore.

---

## Explicitly NOT salvaged (confirmed project-specific, no crossover)

- Anything under `RESEARCH TOOLS/` in the other repo (Master Voice
  Library, animation style refs) — Parents Teach Kids character/voice
  assets, unrelated to this project.
- `MentorScript` / `Scene` / `KeyObject` / child-character / mentor-persona
  logic, the creative bible system (`load_creative_bible`,
  `pipeline.py:819-963`), `MENTOR_PALETTE`, `ANIMATION_STYLE_REFERENCE`,
  `PRONUNCIATION_MAP` — entirely specific to the kids'-education cartoon
  format.
- All image-generation code (`generate_image_with_imagen`,
  `pipeline.py:2277-2338`, and everything built on it: character/
  environment/object reference-sheet generation and their QA validators,
  `pipeline.py:2355-2634`, `2839-2904`) — the clipper bot has no image-
  generation stage.
- All TTS/voice-cloning code (`generate_voiceover_via_elevenlabs`,
  `generate_voiceover_via_gemini_tts`, `audio_team_leader`,
  `pipeline.py:2905-3271`) — no synthesized voiceover in this pipeline;
  original stream audio is the source. (The *tiered-fallback-chain shape*
  underlying `_synthesize_speech_segment` is salvaged separately above —
  it's the structure, not the TTS-specific content, that's reusable.)
- `caption_agent`'s `ffsubsync`-based re-timing of a fake one-word-per-
  second SRT (`pipeline.py:3409-3452`) — the clipper bot gets real
  word-level timestamps directly from `faster-whisper`, which is strictly
  better than resyncing a synthetic timing track; `ffsubsync` is at most a
  last-resort fallback here, not a primary technique to port.
- `MUSIC_VOLUME`/`SFX_VOLUME`/`_build_assembly_ffmpeg_cmd`'s background-
  music-under-narration mixing (`pipeline.py:3454-3496`) — no narration to
  mix under in this pipeline; the `filter_complex`/`amix` technique itself
  is generic ffmpeg knowledge, not something distinctive enough to cite as
  a salvage item on its own.
- `algorithm_evolution_agent`, `creative_evolution_agent`,
  `thumbnail_agent` (placeholder-text-on-solid-background thumbnail
  generation) — content-specific to the source channel's format.
