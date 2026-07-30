# Deep dive: `mutonby/openshorts` — read directly from source, 2026-07-29

2,784 stars, actively developed (commits same day as this read), Python
backend + React dashboard + TypeScript render service. The strongest,
most production-hardened reference found across all research this project
has done. Read directly via `gh api` (not paraphrased from the README) —
`gemini_worker.py`, `clip_selection.py`, `reframe_v2.py`,
`transcribe_backends.py`, and the `SmoothedCameraman`/`SpeakerTracker`
classes in `main.py`. This is real, shipped code with dated comments citing
measured A/B results on real user footage — genuinely professional-grade,
not a tutorial project.

**Licensing — checked directly against the repo's actual LICENSE files,
2026-07-30:** the root `LICENSE` is plain MIT (free to use/copy/modify/sell,
just keep the copyright notice) for everything **except** the `cloud/`
directory, which carries a separate "OpenShorts Commercial License"
(`cloud/LICENSE`). That directory is Stripe billing, OAuth, metering,
managed API keys, social-profile linking, alerts, database models — the
SaaS-specific commercial layer, not the video pipeline. Its terms permit
viewing/studying/modifying/self-hosting for personal or internal use, but
prohibit reselling it (or a derivative of it) as a competing hosted
service, or stripping its billing/metering when giving third parties
access. **None of this applies to anything actually recommended for
porting in this document** — `clip_selection.py`, `gemini_worker.py`,
`reframe_v2.py`, `transcribe_backends.py`, `ffmpeg_utils.py`,
`edit_builder.py`, `scene_detection.py`, `security_utils.py`, and the
camera-tracking classes in `main.py` are all at the repo root, all MIT.
The `cloud/` restriction only matters if we ever wanted to clone
openshorts's own paid multi-tenant SaaS product specifically — not our
plan (self-hosted, single-channel use).

**Standing rule applies**: this is a real, verified-real repo — but "real
and popular" is not "beyond scrutiny." Read it, learn from it, port the
ideas that fit. Don't clone-and-run it wholesale.

---

## 1. Two-stage moment scoring (the core cost/quality trick)

Instead of asking Gemini to write full viral copy for every candidate
moment (expensive, slow), openshorts splits scoring into two passes:

1. **Score stage** — the transcript is chopped into ~90-second windows
   *aligned to real transcript segment boundaries* (never splits a
   sentence), with ~30s overlap between windows so a moment spanning a
   window edge isn't lost. Each batch of windows gets a cheap, fast
   `score` call: an integer 0-100 plus a one-line reason, using a strict
   rule called **"the 2-second test"**: *"would the first 2 seconds of
   this moment force a cold viewer (no context) to keep watching?"*
   Windows that only work with prior context score low. This is a real,
   concrete, reusable prompt-engineering rule — worth adopting verbatim.
2. **Detail stage** — only the shortlisted, highest-scoring windows go
   through a second, more expensive call that generates the actual clip
   boundaries plus title/hook/description copy. This second call also
   enforces a **diversity rule**: *"never return two clips that make the
   same point, tell the same story, or land the same joke — even across
   different windows. Pick the stronger one and drop the other."*

**Why this matters for us:** this is a direct, provable answer to "how do
we not burn budget scoring every single moment at full cost" — exactly the
kind of cost discipline `pipeline.py`'s budget-enforcement work already
cares about. Port the two-stage shape directly.

## 2. The "Hook Playbook" — a real, named pattern library

The detail-stage prompt gives Gemini five explicit hook patterns to choose
from (paraphrased categories, not verbatim marketing copy):
open question, hot take/controversy, number/fact shock, story loop,
POV/pattern-interrupt. Each has a short example format. This is a concrete,
reusable few-shot technique for generating clip hooks — worth borrowing the
*structure* (a small named list of hook archetypes fed to the LLM as
options) even if we write our own examples.

## 3. `snap_clip_to_words()` — fixes LLM timestamp imprecision

**This is the single most valuable, non-obvious technique found in this
whole research effort.** LLMs are bad at millisecond-precise arithmetic —
Gemini proposes a clip's start/end in seconds, but those numbers are
approximate. `clip_selection.py`'s `snap_clip_to_words()` takes the
LLM-proposed boundaries and **snaps them onto real word-boundary timestamps
from the transcript** (from faster-whisper/Parakeet word-level output),
then adds a small lead/tail padding into the surrounding silence (max 0.35s
lead, 0.45s tail) so cuts land in natural pauses instead of mid-word or
mid-syllable. It also repairs duration bounds (clips must be 15-60s) by
searching for the nearest valid word boundary that satisfies the length
constraint, falling back to the original LLM timestamps only if no good
snap point exists.

**Concrete recommendation: port this technique directly.** We were not
planning for this failure mode at all — every dossier and every video
research finding assumed "the LLM gives you a timestamp, you cut there."
This is proof from a real, shipped 2,784-star project that raw LLM
timestamps need a correction pass against real ASR word timings before
they're safe to cut on.

## 4. Real, current Gemini pricing table (useful for our own budget model)

```python
MODEL_PRICES = {  # (input $/1M tokens, output $/1M tokens incl. thinking)
    "gemini-3.5-flash": (1.50, 9.00),
    "gemini-3.1-flash-lite": (0.25, 1.50),
    "gemini-3-flash-preview": (0.50, 3.00),
    "gemini-2.5-flash-lite": (0.10, 0.40),
    "gemini-2.5-flash": (0.30, 2.50),
    "gemini-2.0-flash": (0.10, 0.40),  # deprecated (shut down 2026-06-01)
}
```
Thinking tokens are billed at the **output** rate even though they're
invisible in the response — a real cost detail worth remembering for our own
`COST_PER_TOKEN` budget math, which currently uses one flat rate
(`pipeline.py`'s `COST_PER_TOKEN = 0.0000025`). openshorts' per-model table
is more accurate than a single flat constant.

## 5. `GeminiBlockedError` — a real production incident, documented

```
Deterministic: the same payload is rejected every time (verified in prod,
23-jul-2026 — a stand-up video came back PROHIBITED_CONTENT in ~300ms on
every attempt), and BLOCK_NONE safety settings do NOT lift it. Retrying is
pointless, so callers must fail fast with a message that tells the user the
video's content is the problem, not the service.
```
Checks both `response.prompt_feedback.block_reason` and each candidate's
`finish_reason` against a set of known-blocked reasons (`SAFETY`,
`PROHIBITED_CONTENT`, `BLOCKLIST`, `SPII`, `IMAGE_SAFETY`, `RECITATION`) and
raises immediately instead of retrying. **This is a different failure mode
than the `content=None` crash we already fixed in `pipeline.py`** (that one
was about a missing `.parts` attribute; this one is about a real response
that arrived but was policy-blocked) — complementary lesson, worth adding
the same fail-fast-don't-retry logic to our own Gemini call wrapper.

## 6. Structured output with a 3-tier fallback strategy

`structured-schema` (primary — a real Pydantic `response_schema` passed to
`generate_content`, same pattern we already use via `call_gemini_inspector`)
→ `json-text-recovery` → `strict-json` (looser prompting, manual JSON
extraction/repair as a last resort). Also strips markdown code fences and
repairs invalid `\u` escape sequences before parsing — a more thorough
repair pass than our own `safe_json_parse`, worth comparing against it.

## 7. Face-tracking vertical crop (`reframe_v2.py` + `SmoothedCameraman`/`SpeakerTracker`)

Far more sophisticated than the static `crop=ih*9/16:ih` we currently have.
Two-pass architecture: (1) analyze a downscaled (≤640px) decode with
OpenCV/MediaPipe/YOLO to compute a camera trajectory (crop x-position per
frame), (2) render natively in ffmpeg using the `sendcmd` filter to feed
that trajectory into a single real-resolution encode pass — no raw-frame
piping, no second full-res decode.

Key sub-components, with real tuned constants and cited measurements:
- **`SmoothedCameraman`** — "heavy tripod" logic: a 25%-of-crop-width safe
  zone where the camera doesn't move at all; outside it, pans slowly (3px/
  frame) or fast (15px/frame) toward the target. A detected jump bigger than
  the safe zone must **repeat for `JUMP_CONFIRM_FRAMES` consecutive
  detections** before the camera commits to it — a single outlier detection
  (false positive, wrong body part) is ignored. Measured on real footage
  (26-jul-2026): raising confirm-frames from 1 to 3 cut in-scene camera
  reversals 69% and camera travel 34%, with only 7 of 84 scenes getting
  busier as a tradeoff.
- **`SpeakerTracker`** — ID-based face tracking (distance-matched across
  frames) with score decay (0.85/frame) and a **3x "sticky" hysteresis
  bonus** for the currently-active speaker, so the camera doesn't
  flicker between two similarly-sized faces. A switch-cooldown holds the
  camera on the current speaker through brief occlusions (a blink, head
  turn, motion blur) instead of jump-cutting — a real bug fix, documented:
  "3 of 7 target switches measured on a 12s clip (25-jul-2026) jumped the
  cooldown this way, and every jump drags the camera across frame."
- **GENERAL vs TRACK scene strategy** — group shots/landscapes get a
  blurred-background centered layout instead of a face-crop (cropping the
  sides would cut someone out of frame). The exact content-height ratio
  (0.42, not the more space-filling 0.55 that was tried and rejected) is
  tuned from auditing real delivered clips, with the reasoning documented
  inline.
- Detectors run on downscaled (≤640px) frames, every 4th frame only
  (`DETECT_STRIDE`), with `SmoothedCameraman` interpolating between
  detections — real perf discipline, detection is the expensive part on
  CPU-only rendering.

**Concrete recommendation:** this is real, valuable prior art for a feature
we don't have designed at all yet (dynamic face-tracked cropping vs. our
current static center-crop). Not a v1 priority (static crop is fine to
ship first), but when we do build this, don't reinvent it — this is a
proven, tuned design worth adapting rather than designing from scratch.

## 8. Transcription backend with real fallback discipline (`transcribe_backends.py`)

- **Primary/fallback split**: NVIDIA Parakeet (`nemo-parakeet-tdt-0.6b-v3`,
  via `onnx_asr`, GPU-accelerated) as primary, falling back to
  faster-whisper automatically when Parakeet errors, produces zero usable
  words, **or the detected language falls outside Parakeet's 25 supported
  European languages** (real, specific list of ISO codes in the source).
- **A real "is this transcript actually trustworthy" heuristic**, not just
  exception-catching: `_parakeet_fallback_reason()` rejects a
  successfully-returned transcript if word-count-per-second implies less
  than ~12 words/minute over 60+ seconds of audio — real speech averages
  >100 wpm, so a suspiciously low count means the audio mostly wasn't
  recognized (wrong language, mostly music, etc.) even though the backend
  didn't technically error.
- **GPU semaphore gating** (`ASR_GPU_CONCURRENCY`, default 1) — serializes
  GPU transcription jobs so concurrent jobs can't stack multiple model
  contexts in VRAM at once; CPU whisper stays ungated since CTranslate2
  models are thread-safe.
- **GPU→CPU degradation with a sticky flag** — a CUDA OOM triggers one
  retry on CPU, then pins CPU for the rest of the process (doesn't keep
  re-attempting GPU and re-failing).
- **Pre-check for silent video**: `ffprobe`-checks for an audio stream
  before attempting transcription at all, because every ASR backend
  otherwise crashes deep inside libav with an opaque "tuple index out of
  range" — a real, specific failure mode caught and given a clear message
  instead.
- **A defined transcript contract** every downstream consumer relies on:
  words carry a leading space on true word-starts (continuation subword
  fragments get merged in), all timestamps are native floats, everything
  sorted chronologically. Worth adopting as our own internal transcript
  schema regardless of which ASR backend we pick.

**Concrete recommendation, corrected 2026-07-30:** originally written here
as "don't need Parakeet since faster-whisper is already chosen" — that was
the same too-quick-to-discard mistake made with the Auto-clipper YOLO
model (see `PROJECT.md`'s Stage 3 correction note). Parakeet is free,
open-weight, and openshorts uses it as *primary* specifically because it's
faster than whisper on GPU. Keep it documented as a real, ready-to-use
optional swap for whenever this pipeline runs somewhere with real GPU
access, not something already ruled out. Also keep, regardless of ASR
choice: the *quality-heuristic fallback* pattern (not just catching
exceptions, but validating the transcription *output* actually looks
sane — the words-per-minute sanity check) and the GPU-concurrency-gating
pattern (a semaphore so concurrent jobs can't stack multiple model
contexts in VRAM at once).

## 9. Visual-only fallback path

For videos with no useful transcript (or none at all), a separate
`VISUAL_PROMPT_TEMPLATE` has Gemini watch the raw video directly (native
video understanding, no frame extraction) and pick moments purely from
visual content — action, reveals, transformations, striking/funny shots.
Confirms and extends what the tool-verification pass already found
independently (`research/tool_verification.md`): Gemini's native video
input is real and works without a separate frame-extraction step.

## 10. `s3_uploader.py` (446 lines, fully read) — two-tier storage, not one

Two entirely separate S3 buckets serve two different purposes, and the
distinction matters:

- **`AWS_S3_BUCKET`** (private) — a silent, best-effort backup of finished
  job clips + metadata. In `app.py`'s `run_job()`, this only fires
  `if not BILLING_ENABLED` (self-host path only — cloud mode uses R2
  archival instead, documented in section 13). `upload_file_to_s3()` is a
  pure no-op if `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` aren't set
  (`return False`, never raises), and every call site swallows exceptions —
  so a self-host user gets a zero-configuration-required off-site backup of
  their clips with no failure mode that can break the pipeline.
- **`AWS_S3_PUBLIC_BUCKET`** (public) — used only by the SaaSShorts feature
  (section 12) for actor portrait images and the public UGC video gallery
  (`/gallery`, `/video/{id}` SEO pages in `app.py`). Public URLs are
  constructed directly (`https://{bucket}.s3.{region}.amazonaws.com/{key}`,
  no signing) since the bucket is meant to be publicly browsable.
- **In-memory 5-minute TTL cache** (`CACHE_TTL_SECONDS = 300`) on both
  `list_all_clips()` and `list_video_gallery()` — avoids re-listing S3 and
  regenerating hundreds of presigned URLs (`generate_presigned_url`,
  2-hour expiry for clips) on every page load. Simple `{"data":..., "timestamp":...}`
  dict, no external cache dependency.
- **Small hardening details worth noting**: `upload_actor_to_s3()` skips
  files under 1000 bytes (broken/truncated renders) before uploading; a
  JSON metadata sidecar is written next to each actor image so the gallery
  can show a caption without a database.
- **A real, self-flagged unaddressed limitation**: `list_all_clips()` scans
  the *entire* bucket for `*_metadata.json` keys before doing any
  limit-based early exit on the signed-URL-generation loop — cost scales
  with total bucket size regardless of how small `limit` is. The source
  comment admits it outright: *"Note: For very large buckets, pagination is
  needed. Assuming reasonable size for now, but adding continuation token
  support is best practice."* Even in a 2,784-star, "production-hardened"
  repo, a known scaling gap can ship and sit undocumented anywhere except a
  code comment — a concrete reminder to actually read comments, not just
  function signatures, when judging whether ported code is production-ready.

**Recommendation:** skip the SaaS public-gallery/actor-upload code — not
relevant unless we build a public gallery. **Port directly**: the
"silent best-effort backup, zero-config no-op if keys are unset" pattern
for self-host — this is exactly the shape a single-operator Colab pipeline
needs for an optional, free off-site clip backup with no added failure
surface.

## 11. `editor.py` (506 lines, fully read) — a *second*, on-demand AI editing pass, and its relationship to `edit_builder.py`

**This confirms the relationship the parent task asked about**: `editor.py`
is the caller, `edit_builder.py` (already read/documented separately) is
the deterministic renderer it calls. `editor.py` imports
`build_filter_string` from `edit_builder` and never constructs `-vf` syntax
itself — Gemini proposes a structured `EditDecision` list (Pydantic model:
`type/start/end/strength/reason`, one of 7 named effect types —
`zoom_in`, `punch_in`, `zoom_pulse`, `color_pop`, `bw_moment`, `flash`,
`vignette` — each with a strength/duration range baked into the prompt),
and `edit_builder.build_filter_string()` turns that into an actual, safe
filter string. Quote from the prompt itself: *"You do NOT write FFmpeg —
you return an edit decision list, and a deterministic renderer applies it
safely."* Clean "LLM proposes structured decisions, code renders"
separation, worth keeping as a design principle anywhere we hand an LLM
authority over rendering.

Critically, **`editor.py` is not part of the core clip-generation pipeline
at all** — per `app.py` (section 13), `VideoEditor` is only invoked from
two *opt-in, post-hoc* endpoints (`/api/edit`, `/api/effects/generate`)
that a user triggers manually on a clip main.py already produced. It has
two independent capabilities on the same class:

1. **`get_ffmpeg_filter()`** — the ffmpeg path described above.
2. **`get_effects_config()`** — a completely different prompt asking Gemini
   for a *continuous, gap-free* `EffectsConfig` JSON
   (`startSec/endSec/zoom/zoomCenterX/zoomCenterY/brightness/contrast/saturate`)
   that maps 1:1 onto the Remotion `EffectsConfig`/`EffectSegment` TypeScript
   types (section 14) — this is the literal bridge between the Python/Gemini
   side and the React/Remotion renderer, proxied through `app.py`'s
   `/api/render` to a separate Node service. The prompt explicitly demands
   *"Segments MUST cover the entire video duration from 0 to {duration}
   seconds with no gaps"* and *"Prefer fewer, longer segments with gradual
   changes over many rapid short segments"* — the opposite instinct from
   `get_ffmpeg_filter`'s sparse "2-6 edits per 30s" decision list, because
   the two renderers need different input shapes (ffmpeg needs discrete
   edit events; the React interpolator in section 14 needs a segment
   timeline it can always resolve a value from).

**A real, directly portable resilience pattern**: `apply_edits()` dry-runs
the Gemini-generated filter string on just the first 2 seconds
(`ffmpeg -t 2 ... -f null -`, no output file) before committing to a full
encode. On failure, it does **exactly one** self-repair round-trip — sends
the failing filter string plus the real ffmpeg stderr back to Gemini,
asking for a corrected filter under the same constraints (exact output
resolution, no bare comparison operators, quoted expressions), dry-runs
the repair once more, and only then either proceeds or raises
`RuntimeError("AI filter failed validation even after self-repair")`. This
is a genuinely different, complementary layer to `edit_builder`'s
deterministic construction — a second line of defense for whatever
free-form expression syntax the deterministic builder doesn't fully
constrain. Two supporting narrow-but-real fixes ship alongside it:
`_sanitize_filter_string()` rewrites bare comparison operators (`t<3`,
`on>=75`) into ffmpeg's `lt()/gte()` expr functions before ever running the
filter (raw `<`/`>` parse unreliably across ffmpeg builds), and
`_enforce_zoompan_output_size()` regex-forces any `zoompan` filter's `:s=`
parameter to match the real probed input resolution (Gemini-authored
zoompan filters can silently drift aspect ratio otherwise), appending
`setsar=1` when missing.

One more portable detail: because job/clip filenames can contain non-ASCII
characters and the code has to survive minimal Docker images with a broken
locale, `apply_edits()` manually encodes every subprocess argument to UTF-8
bytes rather than trusting Python's default `fsencode()` — worth keeping in
mind for our own pipeline if job IDs or titles ever carry non-ASCII text.

**Recommendation:** **port directly** — the dry-run-before-full-encode +
one-shot Gemini self-repair loop is immediately reusable in `pipeline.py`
anywhere we hand ffmpeg filter-string authority to an LLM (we don't
currently, but if we ever do, this is the exact pattern to copy). The
comparison-operator sanitizer and zoompan-size enforcement are small,
concrete checklist items for the same scenario. `get_effects_config()` /
the Remotion bridge is SaaS/Remotion-specific — skip unless we adopt
Remotion (see section 14's recommendation, which we don't).

## 12. `saasshorts.py` (1,491 lines, fully read) — a genuinely different product, not a pipeline variant

This is **not** a variant of the clip-extraction pipeline in `main.py` — it
takes a SaaS product URL (or a manual text description) as input, not a
source video, and outputs a synthetic UGC-style ad: an AI-generated
"actor" narrating a script over talking-head + b-roll footage. Zero
input/output overlap with our project's use case; it only shares
infrastructure (the Gemini client, `ffmpeg_utils` helpers, and — per
`app.py` — the same job-queue concurrency semaphore).

Full pipeline, stage by stage:

1. **Research**: `scrape_website()` (BeautifulSoup, SSRF-guarded via
   `security_utils.assert_public_url` re-validated on *every* redirect hop
   — same guard already documented from `security_utils.py`) plus
   `research_saas_online()`, which uses **Gemini's Google Search grounding
   tool** (`types.Tool(google_search=types.GoogleSearch())`) to pull real
   reviews/Reddit/Twitter sentiment and extracts citation URLs from
   `response.candidates[0].grounding_metadata.grounding_chunks` — a real,
   concrete, working example of Gemini search-grounding in production,
   worth knowing about independent of this SaaS-specific use case (we don't
   currently use grounding anywhere).
2. **Analysis**: `analyze_saas()` merges scraped site content + web
   research into structured pain-points/USPs/viral-angles JSON.
3. **Script generation**: `generate_scripts()` enforces a rigid, explicitly
   numbered 5-segment structure (hook/broll/body/broll/cta with exact
   second ranges) via prompt. **Real, minor authoring bug worth knowing
   exists**: the prompt text is internally inconsistent about duration —
   one block states duration *"MUST be 20-25 seconds. NEVER longer than 25
   seconds"*, and the RULES block further down the same prompt states
   *"Total duration MUST be 18-22 seconds, never more."* Two different,
   contradictory numeric constraints, both shipped in the same live prompt.
   Not a functional bug (Gemini just picks one), but a concrete reminder
   that "professional-grade and shipped" does not mean "internally
   consistent" — verify prompts we port, don't assume they're clean because
   the repo is popular.
4. **Asset generation via fal.ai** (a third-party model-hosting/queue API,
   distinct from Gemini): Flux 2 Pro for actor portraits and b-roll stills;
   then either Kling Avatar v2 (premium, ~$1.69) or a documented cheaper
   path — Hailuo 2.3 Fast image-to-video ($0.19) piped into VEED Lipsync
   ($0.20) for a stated **~$0.39 vs ~$1.69** total cost, per the source
   comment: *"Low-cost talking head: Hailuo 2.3 Fast img2video → VEED
   Lipsync. ~$0.39 vs ~$1.69 for Kling Avatar v2."* Real, dated, priced
   comparison data for AI-avatar generation — useful reference even though
   we have no current avatar use case.
5. **`_fal_run()`** implements fal.ai's generic submit → poll → fetch queue
   pattern for any `model_id`, and deliberately derives its poll/fetch URLs
   from the submit response rather than constructing them by convention
   (comment: *"Uses the URLs returned by the submit response (as per
   fal.ai docs)"*) — the more defensive of two common approaches, worth
   copying verbatim if we ever integrate a fal.ai-hosted model.
6. **B-roll is not video generation** — it's a single still image (Flux 2
   Pro) plus a hand-written ffmpeg Ken Burns `zoompan` filter (1.0x→1.15x
   zoom with a slight pan: `z='1+0.15*on/{total_frames}'`). "B-roll clips"
   in this pipeline are animated stills, not real video-model output — a
   deliberate cost-saving substitution worth remembering as a cheap
   fallback pattern for synthetic b-roll anywhere we'd otherwise pay for
   real video generation.
7. **Compositing**: talking-head + b-roll inserts + burned ASS subtitles,
   spliced via an ffmpeg `filter_complex` trim/concat graph keyed to each
   segment's start/end, with a simpler fallback path (subtitles burned
   directly onto the talking head) when there's no b-roll.
8. **Subtitles are re-transcribed from the actual generated audio**
   (`transcribe_audio_for_subs()` calls the already-documented
   `transcribe_backends.transcribe_media()` on the TTS output), not derived
   from the script text directly — i.e. even fully-scripted, synthetic
   narration isn't trusted to match burned captions to real TTS
   timing/pronunciation without re-running ASR on what was actually
   produced.

**A real, confirmed dead-code bug**, new (not previously documented from
other files): in `generate_actor_images()`, the function returns at
`return sorted(paths)` (~line 751), immediately followed by ~10 more lines
of unreachable code — a second, differently-shaped `paths = []` loop
reading from a `result` variable that isn't even in scope there (it was a
per-thread local inside the nested `_gen_one()` closure used by the
`ThreadPoolExecutor` above it). Reads exactly like debris left over from a
pre-parallelization single-threaded version that was never deleted once
the function was rewritten to use threads. Completely harmless (dead,
unreachable), but a concrete data point for the project's standing rule
that "real and popular" isn't "beyond scrutiny" — this is exactly the kind
of thing that only turns up from an actual line-by-line read, never from a
summary.

**Recommendation:** skip wholesale — different product, no input/output
overlap with our slice-existing-video pipeline. Two narrow techniques worth
stealing regardless of that: (a) the generic fal.ai submit/poll/fetch
helper shape, if we ever integrate any fal.ai-hosted model; (b) "b-roll via
still image + local Ken Burns zoompan" as a cheap synthetic-b-roll fallback
if that need ever comes up. General caution: don't port any prompt text
from this file without checking it for internal consistency first (see the
20-25s/18-22s contradiction above).

## 13. `app.py` (3,849 lines — read in full, all lines, no gaps)

**Honesty check on completeness, since this project has an explicit rule
against overclaiming verification**: this file was read completely,
top to bottom, via eight sequential chunked reads with deliberate
line-number overlap at each boundary to guarantee no gap — every one of
the 3,849 lines was actually read, not sampled or inferred from
docstrings/route names. This is the largest file in the repo and the one
most directly relevant to "how does the orchestration layer work," so full
coverage mattered enough to spend the time on.

**Job lifecycle / state machine**: `queued → processing → completed|failed`,
held in a plain in-memory dict `jobs: Dict[str, Dict]` keyed by a `uuid4`
job_id — no database in self-host mode. An optional cloud/billing layer
(multi-tenant ownership, quota metering, Stripe) sits entirely behind one
`BILLING_ENABLED` env flag; when it's off, every gate function
(`resolve_gemini`, `reserve_process_minutes`, `_assert_job_owner`, etc.)
degrades to a documented no-op, so the self-host code path is genuinely
unaffected rather than laced with scattered conditionals. Confirms and
supersedes the "billing is a separate `cloud/` package under a commercial
license" note already added near the top of this document — this is the
call-site side of that same boundary.

**Queueing/concurrency — the actual mechanism**: `job_queue =
asyncio.PriorityQueue()` holds `(priority, seq, job_id)` tuples (priority
0 = pro plan, 1 = starter/creator, 2 = BYOK/anonymous/self-host — so
self-host is always plain FIFO, since every job enqueues at the same
priority). `_job_seq = itertools.count()` supplies a monotonic tiebreaker
so equal-priority tuples always compare deterministically (without it,
`PriorityQueue` would fall through to comparing job_id strings on a tie —
still functional, but not intentionally FIFO). A single
`asyncio.Semaphore(MAX_CONCURRENT_JOBS)` (env var, default 5) is the actual
throttle: `process_queue()` dequeues an item, **then blocks on acquiring a
semaphore slot** before spawning the job as a background `asyncio.create_task`
and immediately looping back to dequeue the next item — so the dequeue loop
itself never blocks on job duration, only on available slots.

**Subprocess vs in-process — the real answer, and it's "both, split by
workload"**: the primary `/api/process` endpoint that runs the actual
clip-generation pipeline builds `cmd = ["python", "-u", "main.py", "-i"/"-u", ..., "-o", job_output_dir]`
and launches it via `subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT, env=env)`
— full process isolation, so a crash or hang inside `main.py` cannot take
down the API server and the job is independently killable. A daemon thread
(`enqueue_output`) reads the subprocess's stdout line-by-line, scrubs
credential URLs (`_scrub_secrets`, a regex specifically for masking proxy
`user:pass@host` strings echoed by yt-dlp's debug output) and appends each
line to the job's in-memory log; the async `run_job()` polls
`process.poll()` every 2 seconds and **opportunistically parses any partial
`*_metadata.json` it finds on disk**, surfacing already-finished clips to
the frontend while later clips in the same job are still rendering — a
progress signal built entirely from filesystem polling, with no explicit
progress-report channel from `main.py` itself.

By contrast, **every secondary/on-demand feature is in-process**: edit,
subtitle, hook, translate, effects-generate, all three thumbnail-studio
steps, and every SaaSShorts step import their target functions directly
(`from editor import VideoEditor`, `from hooks import add_hook_to_video`,
`from main import download_youtube_video, transcribe_video`, `from
saasshorts import generate_full_video`, ...) and invoke them synchronously
inside `loop.run_in_executor(None, fn, ...)` — a thread-pool call, not a
new process. This is a deliberate, real split: the one long-running,
resource-heavy, must-not-crash-the-server job gets full process isolation;
every cheaper, faster, single-clip operation reuses the running server's
warm imports and skips subprocess overhead. This directly answers the
parent task's "subprocess vs in-process" question — it is not a single
answer, the repo genuinely does both, chosen per workload.

**No websockets or SSE anywhere** — confirmed by grepping every `@app.`
route in the file (69 total). Every status surface
(`/api/status/{job_id}`, `/api/saasshorts/status/{job_id}`,
`/api/thumbnail/publish/status/{publish_id}`) is a plain polled GET
returning current in-memory state. The "partial metadata.json" polling
trick above is how progressive results are achieved without ever adding a
push channel.

**Error/retry handling, four distinct layers**:

1. **Per-request**: every mutating endpoint wraps its work in try/except,
   translates failures to `HTTPException(500)`, and — consistently, across
   roughly ten different endpoints — releases any provisional metering
   reservation on failure (`_metering.release_reservation`) so a failed
   managed action never costs the user quota.
2. **Per-job success verification that doesn't trust the exit code alone**:
   a non-zero subprocess return code marks the job `'failed'`
   (`"Process failed with exit code {returncode}"`), but a **zero**-exit
   subprocess with no `*_metadata.json` on disk is *also* marked
   `'failed'` (`"No metadata file generated."`) — main.py exiting cleanly
   isn't itself treated as proof of success, real output has to exist.
   There's also `_relocate_root_job_artifacts()`, a defensive
   "backward-compat rescue" that recovers metadata/clips if `main.py` ever
   writes to `OUTPUT_DIR` root instead of the job subdirectory — evidence
   this actually happened in some prior version and got patched around
   rather than fixed at the source.
3. **Server-restart resilience, two independent mechanisms**:
   - `_recover_jobs_from_disk()` rebuilds `'completed'` job records on
     startup from any output directory with a metadata JSON not already in
     memory, so a restart after a job finished doesn't 404 the frontend
     (which still holds the job_id from localStorage).
   - **The more interesting one**: `_write_resume_manifest()` /
     `_resume_interrupted_jobs()` / `_clear_resume_manifest()` handle jobs
     killed *mid-flight* (container restart while `main.py` was still
     running, no metadata.json yet). A tiny `.resume.json` manifest (cmd,
     priority, user_id, reservation_id, watermark flag, attempts counter —
     explicitly documented as holding *no secrets*, since "the env is
     rebuilt from `os.environ` on resume") is written before a job starts;
     on the next startup, any manifest without a completed metadata.json is
     automatically re-enqueued with its attempt counter incremented.
     Bounded by **`MAX_RESUME_ATTEMPTS = 2`** — a job that fails to
     complete twice running is treated as poison and never resumed a third
     time (its reservation instead flows into the normal orphan-refund
     sweep instead), explicitly so "a video that reliably crashes the
     worker can't crashloop the service." **This bounded-auto-resume +
     poison-job-giveup shape is genuinely reusable outside a multi-tenant
     web service** — it's exactly the pattern a long, unattended Colab run
     would need if we ever want a session that dies partway through to
     resume automatically instead of silently losing all progress.
4. **Failure classification that doesn't naively grab the log tail**:
   `_job_error_text()` explicitly avoids just taking the last N log lines
   for alerting, because the tail of a pipeline log is normally progress
   noise (ffmpeg banners, scene-detection chatter). The source comment is
   explicit about a real, dated misdiagnosis incident this caused: *"a
   silent upload got reported as a broken download path, and a Gemini blip
   as an ffmpeg problem."* The fix filters for lines containing actual
   error markers (`❌`, `ERROR:`, `Traceback`, `FATAL`, `Exception`,
   `Process failed with exit code`, `No metadata file generated`,
   `Execution error:`) and takes the last 6 *of those*, falling back to a
   raw tail only if nothing matches. A concrete, dated lesson about how
   naive "grab recent logs" alerting silently misattributes root cause —
   directly relevant the moment we build any failure summarization on top
   of `pipeline.py`'s own logs.

**Two real, cited production numbers** (both from prod audits dated
25/26-jul-2026, i.e. days before this read): *"only 9% of delivered clips
had captions"* before caption-burning was made a free action (used to
justify removing it from the metered/paid action list — charging for a
table-stakes feature was suppressing its use); and *"491 of 564 users who
ever processed a video did it exactly once"* — the retention number that
justified adding a `job_index`-based analytics event
(`ClipsDelivered`/`JobFailed`) specifically because *"a render finishes
minutes later, often after the tab is closed, and ad-blockers eat a share
of the rest"* of any client-side analytics. Not directly portable
(SaaS-business metrics), but a preview of the kind of instrumentation this
pipeline needed once real users showed up — worth remembering if this
project ever moves past single-operator use.

**Security/defensive details consistent with the already-documented
`security_utils.py`**: `_safe_under()` (path-traversal guard) is reused
repeatedly for every client-supplied relative path that touches the
filesystem (`thumbnail_url`, `retry_job_id`, `selected_actor_url`);
`_CREDENTIAL_URL_RE` masks `user:password@host` patterns in *any*
subprocess output line before it's printed or stored, specifically because
yt-dlp's verbose debug output can echo a residential proxy URL with
embedded credentials; actor image uploads are capped at a hard 25 MB read
to block an anonymous-caller OOM-via-multipart-body attack; and SSRF
re-validation on every redirect hop is applied again here (downloading a
user-selected actor image from an external URL), reusing the same
`assert_public_url` guard from `security_utils.py` that `saasshorts.py`
also uses.

**Disk management — two independent axes, deliberately combined**: an
age-based sweep (`JOB_RETENTION_SECONDS`, default 3600s) *and* a hard size
cap (`OUTPUT_MAX_GB` / `UPLOADS_MAX_GB`, oldest-first deletion once total
directory size exceeds the cap). The comment explains why both are needed
together rather than just one: *"The time-based sweep above bounds the
*age* of what we keep, not its size: a burst of long videos can fill the
volume inside one retention window."* A simple, real, two-axis disk-quota
pattern worth adopting if our own output directory ever needs pruning
across repeated runs.

**Recommendation**: we're a single-process, single-operator Colab
pipeline, not a multi-tenant web service, so most of this file (billing/
metering, ownership guards, priority queue, R2 archive-and-restore, email/
Telegram notifications) should be skipped wholesale — it solves problems we
don't have. Four ideas are worth porting regardless of scale: (1) the
bounded auto-resume-with-poison-job-detection pattern (relevant the moment
we care about a Colab session dying mid-run being resumable); (2) "don't
trust exit code alone, verify real output exists" as the actual success
check; (3) the error-marker-filtered log classification technique instead
of naive tail-grabbing, if we ever build failure summarization on top of
our own logs; (4) the two-axis (age + size) disk cleanup, if disk ever
becomes a concern across repeated runs.

## 14. Remotion rendering stack (`remotion/src/`) — a second renderer, and whether it's relevant to us

**Two parallel rendering paths exist in this repo for the same category of
output** (post-hoc visual polish: zoom/color effects, animated captions,
hook text overlay): the ffmpeg path we already have and use
(`editor.py` → `edit_builder.py`, a real `-vf` filter string burned
directly by ffmpeg), and this Remotion (React-based video composition)
path. The two are explicitly bridged in code, not just conceptually
similar: the *same* `VideoEditor` class in `editor.py` (section 11) has
`get_ffmpeg_filter()` feeding the ffmpeg path and `get_effects_config()`
feeding this one — the repo runs both renderers depending on which
endpoint the user hits (`/api/edit` → ffmpeg; `/api/effects/generate` +
`/api/render` → Remotion, proxied by `app.py` via `httpx` to a *separate
Node.js render service*, default `http://renderer:3100` — `app.py` itself
never renders anything with Remotion, it's purely a proxy).

- **`Root.tsx`** registers one Remotion `<Composition id="ShortVideo">`
  with a Zod-validated `shortVideoPropsSchema` (from `lib/types.ts`) and a
  fully worked DEFAULT_PROPS example — a living, executable spec of the
  exact JSON shape the whole pipeline (Gemini effects config, word-level
  transcript captions, hook config) has to produce to drive this renderer.
- **`ShortVideo.tsx`** is a thin 3-layer composition — base video (wrapped
  in `VideoEffects`) → `Subtitles` → `HookOverlay` — using `@remotion/media`'s
  `<Video>` component, noted in-source as chosen specifically "for
  browser-side rendering compatibility" (distinct from the older
  `<OffthreadVideo>`).
- **`VideoEffects.tsx`** applies the Gemini-authored `EffectsConfig` as
  live, per-frame CSS `transform: scale()` + `filter:
  brightness/contrast/saturate()` — not ffmpeg zoompan, this runs inside
  the browser/headless-Chromium render itself. It implements **three
  distinct interpolation cases** for a sparse segment timeline that are
  worth remembering as a general technique independent of React/CSS: (a)
  inside an active segment, ease in/out over `min(0.3s, 15% of segment
  length)` at the segment's own boundaries; (b) between two segments with a
  gap under 1.0s, linear cross-blend directly from segment A's end values
  to segment B's start values; (c) for a gap of 1.0s or more (or before the
  first / after the last segment), fade to/from neutral defaults (zoom 1.0,
  no filters) over a fixed 0.3s. This active/short-gap/long-gap three-case
  shape is directly reusable for driving ffmpeg `zoompan` `x`/`y`/`z`
  expressions from a similarly sparse LLM-authored segment list — the
  underlying interpolation problem (a sparse timeline needing smooth,
  bounded transitions) doesn't depend on which renderer consumes it.
- **`Subtitles.tsx` / `lib/captions.ts`**: the word-grouping logic is
  explicitly, deliberately mirrored from the Python side — the code
  comment states outright: *"Same logic as OpenShorts' generate_srt: max
  chars per block, max duration per block,"* with matching constants
  (`maxChars = 20`, `maxDurationMs = 2000`). Word outline/stroke uses a
  4-direction `textShadow` trick (`${px}px 0 0 color`, `-${px}px 0 0
  color`, `0 ${px}px...`, `0 -${px}px...`) instead of CSS
  `-webkit-text-stroke`, with the reason stated directly in a comment:
  *"Text stroke via textShadow (CSS paint-order not reliable in
  Remotion)."* A real, reusable gotcha for any Chromium-based renderer
  (Remotion, Puppeteer, any headless-browser video pipeline) — not relevant
  to ffmpeg's own `ass`/`drawtext` filters, which have native, reliable
  outline support already.
- **`HookOverlay.tsx`**: the `HOOK_LOOKS` style table (classic/dark/
  yellow/red/outline/outline_yellow — box color, text color, outline
  px/color, shadow on/off) carries an explicit synchronization comment:
  *"Must mirror hooks.py HOOK_STYLES so preview == burned output."* The
  same visual style constants are deliberately duplicated in Python
  (ffmpeg burn) and TypeScript (Remotion live preview) specifically so a
  browser preview matches what actually gets burned into the final
  ffmpeg-rendered video. **This preview/final-render parity problem — and
  its blunt solution of duplicating constants with a loud comment
  explaining why — is a genuinely general lesson** for any pipeline that
  ever offers a live preview of an operation ultimately executed by a
  different renderer than the preview itself. Uses the same manual
  8-direction pixel-shadow loop (`textStroke()`, one shadow per `(dx,dy)`
  offset within the outline radius) for the same CSS-limitation reason as
  `Subtitles.tsx`.
- **`lib/fonts.ts`**: bundles one custom font (`NotoSerif-Bold.ttf`) via
  Remotion's `staticFile()` + an injected `@font-face`, used only for the
  hook overlay; the subtitle track instead maps to a fixed allow-list of
  common system/web-safe fonts (Verdana, Arial, Impact, Helvetica, Georgia,
  Courier New) matching what the existing `SubtitleModal.jsx` UI exposes.
- **`lib/types.ts`**: the Zod schemas are explicitly noted as *"used by
  render service"* — the Node render service validates incoming render
  requests against these same schemas before rendering, so malformed props
  fail fast with a clear validation error instead of crashing deep inside
  a React render tree.

**Recommendation: skip adopting Remotion itself.** It requires a Node.js
service, a Chromium rendering backend, and a whole parallel schema system —
none of which fits our single-Python-file, ffmpeg-based Colab pipeline, and
we already have a working ffmpeg captioning/effects path with no reason to
replace it. Two *concepts* are worth porting even though the
implementation (React/CSS) isn't: (1) the three-tier gap-interpolation
logic (active-segment ease / short-gap cross-blend / long-gap
settle-to-neutral) for animating a sparse, Gemini-authored effects
timeline — directly applicable to driving ffmpeg `zoompan` expressions from
a similarly sparse segment list, which is a real gap in our own dynamic-
effects design if we ever build it; (2) the "duplicate any preview-facing
visual constant and comment loudly that it must mirror the burn-time
source" discipline, worth remembering if we ever build a live preview UI
ahead of an ffmpeg burn (not applicable today — we have no preview UI).
The CSS text-stroke-via-shadow trick is a Chromium-only workaround with no
ffmpeg equivalent needed — `ass`/`drawtext` already do outlines natively
and correctly.

---

## Bottom line: what to actually take from this repo

1. **Port directly**: `snap_clip_to_words()`-style timestamp correction
   against real ASR word boundaries (section 3) — this is a real bug in our
   own plan we didn't know we had. Also port `editor.py`'s dry-run-before-
   full-encode + one-shot Gemini self-repair loop (section 11) for any
   future case where we hand an LLM authority over ffmpeg filter syntax.
2. **Adopt the prompting patterns**: the 2-second test, the diversity rule,
   the named hook-pattern list, the two-stage cheap-score/expensive-detail
   split (sections 1-2) — but verify any prompt text we port for internal
   consistency first; even this repo ships at least one self-contradictory
   prompt (section 12's duration-bounds conflict in `saasshorts.py`).
3. **Adopt the resilience patterns**: fail-fast on content-policy blocks
   instead of retrying (section 5), a real per-model pricing table instead
   of one flat rate (section 4), an output-quality heuristic for ASR
   results instead of only catching exceptions (section 8), the bounded
   auto-resume-with-poison-job-giveup shape for surviving a killed-mid-run
   process (section 13), "verify real output exists, don't trust exit code
   alone" as a success check (section 13), and error-marker-filtered log
   classification instead of naive tail-grabbing for any failure
   summarization we build (section 13).
4. **Defer, but don't forget**: face-tracked dynamic cropping (section 7) —
   real, tuned, valuable design, but a v2 feature, not a v1 blocker. Ship
   the static crop first (already proven working in our own `pipeline.py`).
   Same treatment for the three-tier gap-interpolation logic behind
   Remotion's dynamic effects (section 14) — worth adapting to drive ffmpeg
   `zoompan` from a sparse LLM-authored segment list *if* we ever build
   dynamic (non-static) effects, but not a v1 blocker either.
5. **Skip wholesale, confirmed not relevant to a self-hosted single-operator
   pipeline**: `saasshorts.py`'s entire UGC-ad-generation product (section
   12, different inputs/outputs entirely — two narrow techniques aside:
   the generic fal.ai submit/poll/fetch shape and "b-roll via still image +
   Ken Burns zoompan" as a cheap synthetic-b-roll fallback, both worth
   remembering even though the product isn't), the Remotion rendering stack
   itself (section 14 — the underlying interpolation *concept* is worth
   keeping, the React/Node implementation is not), and essentially all of
   `app.py`'s billing/metering/multi-tenancy/R2-archival layer (section 13)
   — real, well-built code, solving problems a single-operator Colab
   pipeline doesn't have. What IS worth keeping from `app.py` despite that:
   the subprocess-for-the-heavy-job / in-process-for-cheap-on-demand-ops
   split (a real answer to "how do we isolate the expensive part without
   paying subprocess overhead everywhere"), and the two-axis (age + size)
   disk cleanup if our own output directory ever needs pruning across
   repeated runs.
6. **A meta-lesson, not a technique**: two separate close reads of this
   repo (this one and the parallel pass over `main.py`/`hooks.py`/
   `subtitles.py`/`thumbnail.py`/`translate.py`) each turned up at least one
   concrete, real bug or rough edge in "production-hardened, 2,784-star"
   code — unreachable dead code in `saasshorts.py` (section 12), a
   self-contradictory prompt in the same file, and an unaddressed
   scaling gap admitted only in a code comment in `s3_uploader.py`
   (section 10). None of these are damning, and none change the
   recommendation to learn from this repo — but they're concrete evidence
   for the project's own standing rule that "real and popular" is not
   "beyond scrutiny," gathered specifically because we read the actual
   code line-by-line instead of trusting star count or README claims.
