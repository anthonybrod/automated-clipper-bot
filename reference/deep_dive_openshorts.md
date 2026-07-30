# Deep dive: [`mutonby/openshorts`](https://github.com/mutonby/openshorts) — read directly from source, 2026-07-29

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

## 15. `main.py` — the real top-level orchestration (lines 361-1553)

Everything below `SmoothedCameraman`/`SpeakerTracker` (already covered in §7)
is the glue that turns those classes, plus `reframe_v2`, `gemini_worker`,
`transcribe_backends`, `subtitles`, and `security_utils`, into an actual
runnable CLI pipeline.

### 15.1 Detection helpers: `_detection_frame`, `detect_face_candidates`, `detect_person_yolo`

```python
def _detection_frame(frame):
    """Downscaled copy for detectors. Returns (small_frame, scale) with
    scale mapping small-frame pixel coords back to the original frame."""
    h, w = frame.shape[:2]
    if w <= DETECT_MAX_WIDTH:
        return frame, 1.0
    scale = w / DETECT_MAX_WIDTH
    small = cv2.resize(frame, (DETECT_MAX_WIDTH, max(int(h / scale), 2)),
                       interpolation=cv2.INTER_AREA)
    return small, scale
```
Single shared downscale used by both the MediaPipe face path and the YOLO
fallback. `detect_face_candidates(frame)` runs MediaPipe's `FaceDetection`
on the downscaled RGB frame under a `DETECT_LOCK` (MediaPipe's C++ backend
isn't thread-safe, so this serializes detector calls even when clip
rendering is otherwise parallelized across `CLIP_WORKERS`). Score is simply
`w * h` — box area. Coordinates are computed directly against the
*original* frame's `height, width` using MediaPipe's relative (0-1)
bounding box: *"Boxes are in ORIGINAL frame coordinates (detection runs
downscaled; MediaPipe's relative coords make the mapping exact)."*

`detect_person_yolo(frame)` is the fallback for when face detection finds
nothing (turned-away subject, side profile, motion blur). It runs YOLO
filtered to `classes=[0]` (COCO person class only), and keeps only the top
40% of the largest detected person's box:
```python
face_h = int(h * 0.4)
best_box = [x1, y1, w, face_h]
```
*"Focus on the top 40% of the person (head/chest) for framing — this
approximates where the face is if we can't detect it directly."* Coordinates
are scaled back to full-res explicitly here (`int(i * scale) for i in
box.xyxy[0]`), unlike the MediaPipe path, since YOLO's box format isn't
resolution-relative the way MediaPipe's is.

### 15.2 `create_general_frame` — the blurred-backdrop GENERAL layout

The actual rendering function behind the "GENERAL vs TRACK scene strategy"
described at a design level in §7. Background: resize source to fill output
height, center-crop to output width, then blur at **quarter resolution**
(`cv2.GaussianBlur(small_bg, (13, 13), 0)`) before scaling back up —
*"visually identical for a defocused backdrop, an order of magnitude
cheaper than a 51px Gaussian at full size."* Foreground: resize to fit
output width exactly, vertically centered over the blurred background. The
"blurred sidebar" look every short-form editor uses for wide shots.

### 15.3 A real negative result: the abandoned text-heavy-scene router

```
# NOTE: a "route text-heavy scenes to GENERAL" rule was tried here and removed
# on 26-jul-2026. The problem it targets is real — a screencast that happens to
# contain one face gets cropped to the face and its headlines come out cut
# mid-word — but edge density is the wrong signal for it. Measured: a
# constructed talking-head-beside-a-chart scored 0.012 while the SAME shot
# without the panels scored 0.029, because a flat panel of text has far fewer
# edges than ordinary scene detail. Canny measures visual busyness, not text.
# A real fix needs an actual text detector (MSER/EAST) validated against clips
# that contain the failure mode; this corpus has almost none.
```
Canny edge-density was tried as a cheap proxy for "this frame has important
text/UI a face-crop would cut off," and it measured **backwards** on the
constructed test case (0.012 vs 0.029) because flat text blocks have fewer
edges than natural scene detail. A documented dead end worth remembering:
the right tool for this is a real text detector (MSER/EAST), not an
edge-density proxy.

### 15.4 `analyze_scenes_strategy` — the real TRACK/GENERAL decision logic

Samples 5 frames per scene, clamped away from scene edges (fixing a bug
where "the old start+5/end-5 samples landed outside scenes shorter than ~10
frames"), skips near-black frames (`frame.mean() < 16`), averages face count:
```python
# 0 faces -> GENERAL (Landscape/B-roll)
# 1 face -> TRACK
# > 1.2 faces -> GENERAL (Group)
if avg_faces > 1.2 or avg_faces < 0.5:
    strategies.append('GENERAL')
else:
    strategies.append('TRACK')
```
Then a **hysteresis pass**: a short scene (under 2s) whose strategy
disagrees with both neighbors (which agree with each other) gets overwritten
to match them — *"a short scene whose two neighbors agree on the opposite
strategy is almost always a sampling miss... flapping is worse than an
occasional wrong-but-stable choice."* A reusable principle: when a
per-segment classifier drives a visually disruptive layout change, bias
toward stability over local accuracy.

### 15.5 Filename byte-budget discipline: `MAX_TITLE_BYTES`, `truncate_bytes`, `sanitize_filename`

```python
# Byte budget for the sanitized video title used as the stem of every derived
# file. Filesystems cap a name in BYTES (255 on ext4), not characters...
# The old cap was 100 CHARACTERS, which is 300 bytes of Bengali or Arabic — over
# the limit before any decoration. It surfaced as OSError 36 killing the hook
# endpoint in prod on 26-jul-2026.
MAX_TITLE_BYTES = 120
```
`truncate_bytes` encodes to UTF-8 and hard-slices with `errors="ignore"` so
a truncated multi-byte character doesn't raise or corrupt. **The single
clearest, most portable bug-class finding in this file**: the bug is
specifically about non-Latin scripts (a 100-char English title is fine; a
100-char Bengali/Arabic title is ~300 bytes and blows the limit). Directly
relevant to us — Twitch titles are just as likely to be non-Latin as
YouTube ones. **Port this pattern verbatim.**

### 15.6 `download_youtube_video` — production-hardened downloader, real incident history

SSRF guard first (`security_utils.assert_public_url`), cookies from env var
written to a container-local file (never logging content: *"this would leak
live YouTube session cookies to logs"*), optional `PROXY_URL`, an HD-then-
fallback download ladder. A real quantified regression:
```
# Cap at 720p ONLY when the bytes actually go through the paid proxy...
# This is per-attempt on purpose. Deciding it once from `_proxy` capped the
# DIRECT attempt too, so with DIRECT_FIRST=1 (which serves most downloads)
# every YouTube source arrived at 720p ... 80% of delivered clips came out
# 406x720 (audited 25-jul-2026).
```
The bug: resolution cap was decided once from whether a proxy was
*configured*, not per-attempt from whether it was actually *used* — 80% of
delivered clips measured 406×720 before the fix. Bounded 403-retry
(*"3 of 62 downloads hit this on 22-jul-2026"*), `DIRECT_FIRST=1` needs
cookies+PO-token or "YouTube flags the datacenter IP after the first
request (verified in prod, 21-jul-2026)." **Recommendation**: YouTube-specific,
doesn't port as-is (we're on yt-dlp/Twitch per Stage 1), but three patterns
generalize: per-attempt (not per-config) cost/quality capping, narrow
string-matched retry conditions, and a concrete actionable failure message.

### 15.7 `finalize_clip_passthrough`, `render_clip` — format routing

Stream-copy remux (`-c copy`) for horizontal output, no re-encode. `render_clip`
is a thin router: horizontal→passthrough, square→1:1 reframe, else→configured
`ASPECT_RATIO` reframe.

### 15.8 `auto_caption_clip` — captions on by default, and why

*"Captions are mandatory for short-form to land, but they were opt-in
behind a modal and only 9% of delivered clips ever got them (prod audit,
25-jul-2026). So every clip now ships captioned by default."* The `.ass`
file gets a neutral name (never derived from the clip title) because it's
interpolated into an ffmpeg filter string where a literal apostrophe breaks
quoting — same bug family as `subtitles.py`'s `_escape_ffmpeg_filter_value`
(§17.3), dated the same day as this research pass (29-jul-2026). The output
filename, by contrast, safely carries the real stem since it's only ever an
argv element. `generation_id=int(time.time())` alone isn't unique enough
across parallel `CLIP_WORKERS`, so a `uuid4` hex is appended. Failure is
silent-degrade (`return None`): *"a caption problem must never cost the user
the clip they already paid for."*

### 15.9 Watermark geometry — `apply_watermark`

```python
WATERMARK_WIDTH_RATIO = 0.30
WATERMARK_MARGIN_RATIO = 0.05
WATERMARK_Y_RATIO = 0.40
WATERMARK_OPACITY = 0.85
```
`WATERMARK_Y_RATIO = 0.40` is deliberately anti-crop: top/bottom strips of a
9:16 clip are black bars/blur (no real content), so a mark there is
trivially cropped out. At 40% height it sits inside the real 16:9-into-9:16
content band (~34%-66%), so cropping the mark means cropping real footage
too — a genuinely clever anti-tamper design for a free-plan watermark.

### 15.10 `process_video_to_vertical` — the v1 frame-loop fallback engine

```python
if os.environ.get("REFRAME_ENGINE", "v2").strip().lower() != "v1":
    try:
        import reframe_v2
        result = reframe_v2.render(input_video, final_output_video, aspect_ratio)
        return result
    except Exception as e:
        print(f"   ⚠️ Reframe v2 failed ... falling back to v1 frame loop")
```
A genuinely good resilience shape independent of the v1/v2 specifics: the
newer, more sophisticated engine is tried first, but *any* exception falls
through to an older, simpler, battle-tested implementation — a v2 edge case
degrades render quality rather than failing the job. The v1 path itself
pipes raw `bgr24` frames to an ffmpeg subprocess's stdin (the "old way" v2's
`sendcmd` approach replaced), resets the cameraman to dead-center during
GENERAL scenes so it doesn't drift while inactive, and force-snaps the
camera on every scene's first frame.

### 15.11 `_run_gemini_stage` — the actual retry wrapper

```python
except gemini_worker.GeminiBlockedError:
    raise  # deterministic policy block — never retry
except Exception as e:
    msg = str(e)
    transient = any(tok in msg for tok in (
        '503', 'UNAVAILABLE', '429', 'RESOURCE_EXHAUSTED',
        '500', 'INTERNAL', 'overloaded', 'Deadline',
        'empty response body', 'did not contain a JSON object',
        'Failed to parse Gemini JSON response'))
    if attempt == max_attempts or not transient:
        raise
    wait = 5 * (2 ** (attempt - 1))
```
`GeminiBlockedError` is re-raised *before* the generic handler runs, so a
policy block can never accidentally match a transient-error substring. The
transient list includes strings *this codebase's own parsing code* raises,
not just transport errors — *"Gemini sometimes returns 200 with an empty
body... Retrying that recovered every occurrence seen in prod
(22-jul-2026)."* Backoff: `5 * (2 ** (attempt-1))` across 3 attempts (5s,
10s).

### 15.12 `get_viral_clips` — the real two-pass implementation (concrete parameters)

`SCORE_BATCH = 8` windows per call; shortlist size
`target = max(3, min(10, int(video_duration // 90) + 2))`; falls back to
`windows[:target]` unscored if scoring returns nothing; **every** returned
clip is run through `snap_clip_to_words()` unconditionally; cost is summed
across every call in both passes into one `cost_analysis`; `GeminiBlockedError`
is re-raised (not swallowed) so a content-policy block propagates as a real
failure rather than "found zero clips."

### 15.13 `get_visual_clips` — vision-only fallback, concretely

Uploads the raw video, polls `client.files.get` every 2s for up to a
**180-second deadline**, calls `generate_content` with
`contents=[file_upload, prompt]` and a `VisualResponse` schema. Clips are
clamped to real video duration and anything under 1s dropped. **Always**
cleans up the uploaded file in a `finally` block, even on every failure path.

### 15.14 The CLI entrypoint — fail loud, not fake-success

```python
if not clips_data or 'shorts' not in clips_data:
    # Deliberately fail instead of reframing the whole video: that path
    # wrote no metadata.json, so app.py marked the job failed anyway
    # (app.py:1087) after burning GPU on a render nobody could see.
    raise RuntimeError(
        "Clip detection failed — Gemini did not return usable clips for this video.")
```
A real prior failure mode: an earlier "just reframe the whole video on
failure" fallback *looked* like graceful degradation but burned a full GPU
render for output nobody ever saw, since `app.py` still required
`metadata.json` to mark success. The fix is "fail loud immediately," not
"handle the failure better" — a specific instance of "don't degrade into a
fake-success state that still costs full price." Clips render in parallel
via `ThreadPoolExecutor` (`CLIP_WORKERS`, default 3), with each clip's
cut/render/watermark/caption steps allowed to fail independently
(`as_completed` catches+logs per-clip exceptions).

**Recommendations for §15**: (1) the try-v2-fallback-to-v1 wrapper (§15.10)
is worth copying verbatim for our own reframe engine if we ever build a
face-tracked v2 on the static-crop v1; (2) the fail-loud-not-fake-success
lesson (§15.14) directly matters for our budget-enforcement work — don't
let a soft-degrade path burn Gemini/GPU budget for output nobody sees;
(3) the byte-budget filename pattern (§15.5) should be ported before it
bites us on a non-Latin Twitch title; (4) per-clip independent failure
handling in a `ThreadPoolExecutor` batch (§15.14) is worth adopting directly
once we parallelize our own multi-clip rendering.

## 16. `hooks.py` — hook text/image overlay generation (408 lines, read in full)

Generates the hook-card images composited onto clips — the visual
counterpart of the hook *text* copy from §2's prompts.

**`HOOK_STYLES`** — six named looks (classic/dark/yellow/red/outline/
outline_yellow), one flag (`has_box = box_fill[3] > 0`) steering both the
shadow-drawing and text-drawing branches, so a 7th style is just one dict
entry.

**Emoji handling** — a real cross-platform problem solved by degrading, not
crashing: the hook font (`NotoSerif-Bold.ttf`) has no emoji glyphs, so the
code probes hardcoded platform-specific emoji-font paths (Windows
`seguiemj.ttf`, WSL's mount of it, two Linux/Docker Noto paths) and, if none
load, **strips emoji from the text entirely** rather than rendering tofu
boxes, collapsing the resulting double-space.

**Pixel-based text wrapping** — measures actual rendered width per
candidate line, and hard-wraps character-by-character
(`_break_long_word`) when a single word is wider than the box on its own,
"so the word can't get cut off at the edges." Font size is `int(target_width
* 0.05)` — 5% of the target box width, "tuned to match Noto Serif Bold
metrics in browser" — so it scales correctly across resolutions, not a fixed
pixel size.

**Byte-budget filename discipline again**: `add_hook_to_video`'s temp
overlay filename is trimmed by the *same* dated incident as `MAX_TITLE_BYTES`
(§15.5) — *"Embedding it untrimmed raised OSError 36 and killed the endpoint
in prod on 26-jul-2026"* — confirming one real bug surfaced through at least
two call sites, fixed identically at both (truncate by UTF-8 byte count, via
a locally-duplicated `_truncate_bytes` so this module "stays free of main's
heavy imports (cv2, mediapipe, torch)").

**Recommendation**: port the pixel-wrap-with-hard-fallback and the
emoji-strip-if-no-font logic directly if we ever build our own hook-card
generator — both are real, non-obvious, easy-to-get-wrong-the-first-time
problems already solved correctly here.

## 17. `subtitles.py` — caption/subtitle generation and burning (561 lines, read in full)

**`merge_continuation_words`** — short enough to quote in full, and it's
the actual reference implementation of the transcript contract (leading
space = true word start) already committed to in our Architecture Outline
(Stage 2):
```python
def merge_continuation_words(words):
    merged = []
    for word in words:
        text = word.get("word", "")
        if merged and isinstance(text, str) and text and not text.startswith(" "):
            prev = merged[-1]
            prev["word"] = f"{prev.get('word', '')}{text}"
            if word.get("end") is not None:
                prev["end"] = word["end"]
        else:
            merged.append(dict(word))
    return merged
```
Called defensively a *second* time inside `_collect_word_blocks` even for
already-merged transcripts, because "transcripts from old jobs on disk store
unmerged tokens" — i.e. deliberately idempotent-safe.

**`_escape_ffmpeg_filter_value` — the apostrophe bug, dated the same day as
this research pass (29-jul-2026)**:
```
NOTE: an apostrophe in the path cannot be made safe here. ffmpeg's
filtergraph parser is not a shell — the shell idiom `'\''` was tried on
29-jul-2026 and is worse than doing nothing: it drops the apostrophe AND
swallows the following option, so `ass='…Earth'\''s.ass':fontsdir='…'`
resolved to a filename of "…Earths.ass:fontsdir=…" and failed to open.
```
A documented *failed* fix attempt: the classic POSIX shell trick for
embedding a literal quote doesn't work against ffmpeg's filtergraph parser —
it corrupts the *following* filter option too. The real fix is
architectural: never let an apostrophe-bearing path reach this function;
always generate a neutral filename. **Directly actionable**: any subtitle
file we burn via an ffmpeg `-vf ass=...`/`subtitles=...` filter must get a
UUID/counter-based name, never one derived from a video/creator title.

**`SAFE_MARGIN_V = 43`** (was 25): *"The old hardcoded 25 (8.7%) put
captions underneath TikTok's and Reels' own bottom UI — the caption/username
block and the music ticker — where they were partly covered on the platform
even though the exported file looked fine."* A real category of bug — looks
fine in isolation, breaks under the platform's own persistent UI chrome —
worth a QA checklist item once we post to TikTok/Reels/Shorts for real.

**`AUTO_CAPTION_STYLE`** — real A/B-tested defaults, not guesses: white
Anton uppercase, `#FFE500` yellow active-word highlight chosen "because it
is the one colour that almost never occurs in footage," `"pop"` scale effect
tuned from 75→112% down to a gentler 90→108% after the wider range "started
the word so small that any frame caught mid-animation read as a sizing bug
rather than a beat," `max_chars: 16` / `max_duration: 1.4`. Dimming
inactive words uses **RGB scaling, not alpha** — libass draws the outline
*under* the fill, so a semi-transparent fill blends into muddy grey with its
own outline; scaling toward black instead keeps text crisp.

**Recommendation**: port `merge_continuation_words` near-verbatim (it's our
already-committed transcript schema); adopt the neutral-filename-for-
ffmpeg-filter rule as a hard project rule, not a suggestion; the complete
karaoke-word-highlight ASS generator (one `Dialogue` event per word, `{\r}`
reset, RGB-scaled dimming) is a fully-working, tuned implementation of
exactly the "TikTok-style" caption look every source in our video research
called table-stakes — no reason to design it from scratch.

## 18. `thumbnail.py` — thumbnail/title/description generation (339 lines, read in full)

Metadata layer (titles, thumbnails, description+chapters) for the *source*
video, not clip extraction. No dated bug-fix comments anywhere in this file
— unlike every other file read, this one reads as comparatively
un-battle-tested.

**`analyze_video_for_titles`** uploads the actual video (not just
transcript text) and asks for 10 titles plus a self-selected top-2 with
justification in the *same* call — a real, distinct prompting pattern from
the two-stage score/detail split (§1): ask for candidates and a
self-critique together, trading independent re-scoring rigor for one fewer
round-trip. **No `response_schema` enforcement anywhere in this file** —
manual markdown-fence-strip + `find('{')`/`rfind('}')` JSON extraction
instead, a real regression relative to the schema-enforced pattern used
throughout `gemini_worker.py`/`main.py`.

**`generate_thumbnail`** composes actual reference images (face/background)
directly into a multimodal `contents` list alongside text, with an
`"⚠️ MANDATORY USER INSTRUCTIONS (MUST follow these exactly — they override
any default behavior)"` block — a real technique for making user overrides
reliably beat a function's own prompt defaults. `image_config=
types.ImageConfig(aspect_ratio="16:9", image_size="2K")`, `count` (default
3) independent try/excepted attempts, hard-fails only if *all* attempts
failed — the same "collect partial successes, only hard-fail if the whole
batch is empty" shape used elsewhere in this codebase.

**`generate_youtube_description`** generates YouTube chapter markers from
*real* transcript timestamps, not model-guessed ones — the model only picks
which existing timestamps deserve a chapter break, sidestepping the
"LLM is bad at precise numbers" problem `snap_clip_to_words` (§3) exists to
fix elsewhere.

**Recommendation**: our output is explicitly "YouTube Shorts + long-form
compilations" (Architecture Outline Stage 5), so this is directly relevant,
not a tangent. Port the chapter-generation-from-real-timestamps technique
directly. Treat the missing `response_schema` enforcement here as a real
inconsistency in openshorts itself, not something to copy — apply our own
schema-enforced pattern uniformly, including to title/description
generation.

## 19. `translate.py` — ElevenLabs dubbing/translation (285 lines, read in full)

A complete, small, self-contained ElevenLabs **Dubbing API** wrapper (full
audio-track translation via voice cloning, not just subtitle translation).
30 real supported language codes. `_with_retry` — a clean, generic
exponential-backoff wrapper (2s/4s over 3 attempts), retrying only a
self-raised `_TransientHTTPError` (429/500/502/503/504) or a raw
`httpx.TransportError`, everything else fails fast — the same "classify by
whether retrying could help" philosophy as `_run_gemini_stage` (§15.11), just
for generic HTTP. `create_dubbing_project` re-opens the video file *inside*
the retried closure so a retry doesn't resend a partially-consumed stream.
`download_dubbed_video` streams to disk in 8KB chunks, correctly calling
`response.read()` before `.text` on a non-200 streamed response.

**Recommendation**: multi-language dubbing isn't in our current Architecture
Outline (Stage 5 is YouTube/Reels distribution, not localization) — lower
priority, but keep this filed as a complete, ready-to-port reference if that
changes. The generic retry wrapper (§19's `_with_retry`) is worth lifting
for *any* of our own outbound HTTP integrations (YouTube Data API, Twitch
Helix, cross-posting APIs), not just ElevenLabs.

---

## Bottom line: what to actually take from this repo

1. **Port directly**: `snap_clip_to_words()`-style timestamp correction
   against real ASR word boundaries (section 3) — this is a real bug in our
   own plan we didn't know we had. Also port `editor.py`'s dry-run-before-
   full-encode + one-shot Gemini self-repair loop (section 11) for any
   future case where we hand an LLM authority over ffmpeg filter syntax.
   From the `main.py`/`hooks.py`/`subtitles.py` pass (sections 15-17): the
   byte-budget (not character-budget) filename-truncation pattern behind
   `MAX_TITLE_BYTES` (§15.5, §16) — a real, dated `OSError 36` incident,
   specifically about non-Latin-script titles, that applies just as much to
   Twitch stream/VOD titles as YouTube ones; `merge_continuation_words()`
   (§17), the actual short reference implementation of the transcript
   contract already committed to in Stage 2 of our Architecture Outline;
   the hard rule that any filename interpolated into an ffmpeg filter string
   must be neutral/UUID-based, never derived from user- or creator-supplied
   text (§17 — a proven, not hypothetical, apostrophe-breaks-the-filtergraph
   failure mode); and the complete karaoke-style per-word-highlight ASS
   caption generator (§17, RGB-scaled dimming + `{\r}`-reset inline color
   overrides) — a working, tuned implementation of exactly the TikTok-style
   animated-caption look every source in our video research named as
   table-stakes, with no reason to design it from scratch.
2. **Adopt the prompting patterns**: the 2-second test, the diversity rule,
   the named hook-pattern list, the two-stage cheap-score/expensive-detail
   split (sections 1-2) — but verify any prompt text we port for internal
   consistency first; even this repo ships at least one self-contradictory
   prompt (section 12's duration-bounds conflict in `saasshorts.py`).
   `thumbnail.py` (§18) adds two more real prompting techniques: "generate a
   batch, then have the same call self-select and justify its top picks,"
   and a "⚠️ MANDATORY USER INSTRUCTIONS... override any default behavior"
   block for making user-supplied overrides reliably beat a function's own
   prompt defaults — plus the chapter-generation-from-real-timestamps
   technique, a clean way to keep an LLM constrained to ground-truth
   numbers instead of inventing new ones.
3. **Adopt the resilience patterns**: fail-fast on content-policy blocks
   instead of retrying (section 5), a real per-model pricing table instead
   of one flat rate (section 4), an output-quality heuristic for ASR
   results instead of only catching exceptions (section 8), the bounded
   auto-resume-with-poison-job-giveup shape for surviving a killed-mid-run
   process (section 13), "verify real output exists, don't trust exit code
   alone" as a success check (section 13), and error-marker-filtered log
   classification instead of naive tail-grabbing for any failure
   summarization we build (section 13). From sections 15-19: the
   try-the-newer-engine-fall-back-to-the-older-one-on-any-exception wrapper
   shape around `process_video_to_vertical`'s v2/v1 reframe engines
   (§15.10); the "fail loud instead of a fake-success degrade that still
   burns full cost" lesson from `main.py`'s own documented prior incident of
   reframing whole videos nobody could see (§15.14); per-item independent
   failure handling inside a `ThreadPoolExecutor` batch, used consistently
   for both parallel clip rendering (§15.14) and multi-attempt thumbnail
   generation (§18); the captions-shipped-by-default product decision,
   backed by the same 9%-opt-in-rate stat independently cited in both
   `main.py` (§15.8) and `app.py` (section 13); and `translate.py`'s small,
   clean, generic HTTP exponential-backoff wrapper (§19), reusable for any
   of our own outbound HTTP calls (YouTube Data API, Twitch Helix,
   cross-posting APIs), not just Gemini.
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
   repeated runs. Also skip for now: `translate.py`'s ElevenLabs dubbing
   integration (section 19) — multi-language localization isn't in our
   current Architecture Outline — but keep it filed as a complete,
   ready-to-port reference for whenever that changes.
6. **A meta-lesson, not a technique**: multiple close reads of this repo
   (sections 1-19) each turned up at least one concrete, real bug or rough
   edge in "production-hardened, 2,784-star" code — unreachable dead code
   in `saasshorts.py` (section 12), a self-contradictory prompt in the same
   file, an unaddressed scaling gap admitted only in a code comment in
   `s3_uploader.py` (section 10), a documented-and-abandoned Canny-edge-
   density heuristic that measured backwards on its own test case (§15.3),
   a live, dated (29-jul-2026 — the same day as this research pass) failed
   fix attempt for an ffmpeg apostrophe-escaping bug (§17), and
   `thumbnail.py`'s complete absence of the schema-enforced JSON parsing
   pattern used everywhere else in the codebase (§18). None of these are
   damning, and none change the recommendation to learn from this repo —
   but they're concrete evidence for the project's own standing rule that
   "real and popular" is not "beyond scrutiny," gathered specifically
   because we read the actual code line-by-line instead of trusting star
   count or README claims.
