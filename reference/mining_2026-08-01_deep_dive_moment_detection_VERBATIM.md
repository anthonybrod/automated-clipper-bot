<!-- CORRECTION BANNER added 2026-08-06. The body below is UNCHANGED. -->
> ## ⚠️ RENAMED — `@LacyCrashOuts` is now `@CoreCrashOuts`
>
> This file predates 2026-08-06 and uses the old name. **It was always the
> OUTPUT channel** — where finished clips get posted — and it has simply
> been renamed. Some passages below describe it as a "target streamer";
> that was never accurate.
>
> | | Now |
> |---|---|
> | Output | **`x.com/CoreCrashOuts`** + **`youtube.com/@CORECrashOUTS`** |
> | Source (V1) | **`twitch.tv/lacy`** — VODs and `/clips?range=7d` |
> | Scope | V1 = Lacy only → V2 = the whole CORE group |
>
> **The body is deliberately left uncorrected** (Rule 16 — a raw record is
> never rewritten to reflect a later finding).

# Mining report — `deep_dive_moment_detection.md` (VERBATIM AGENT REPORT)

**Source**: background mining agent, 2026-08-01. Scope: one file,
`AI\automated clipper bot\sample reference\deep_dive_moment_detection.md`,
read in full (1,230 lines). Extraction lenses: (A) complete/portable code,
(B) fixable code, (C) free/unutilized tools, (D) efficiency paths,
(E) corrections/gotchas.

**VERIFIED before saving** — 9 independent spot-checks run against the real
source file, all passed: the Twitch GQL persisted-query SHA-256 hash, the
`Clusterer.cluster` reference, the `fps != fps` NaN guard, the
`.min()`/`.max()` bug quoted exactly, `concurrent_fragment_downloads=16`,
`signals_active`, `arc_cv_pipeline` (8 occurrences), the 762-annotated-frames
figure, and its structural claim that two sections share an identical
"Audit pass" heading (confirmed: exactly 2). Only discrepancy found: the
report says 1231 lines, actual is 1230 — an off-by-one, not a fabrication.

**This is the agent's complete report, word for word, uncondensed**, per
this project's standing rule that raw reports are preserved in full and
never summarized away.

---

# Mining Report — `deep_dive_moment_detection.md`

**Source file (read in full, 1231 lines, three passes covering lines 1–780, 780–1019, 1019–1231):**
`C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\deep_dive_moment_detection.md`

**Repos the document covers (all read from source via `gh api`, dated 2026-07-29):**
- `ClipsAI/clipsai` — https://github.com/ClipsAI/clipsai (522 stars, MIT)
- `jamesbaughnd/twitch-clip-miner` — https://github.com/jamesbaughnd/twitch-clip-miner (6 stars)
- `bendawg2010/Auto-clipper` — https://github.com/bendawg2010/Auto-clipper (3 stars; **default branch is `claude/twitch-clip-analyzer-MPT08`, not `main`**)
- Cross-referenced: `lay295/TwitchDownloader` — https://github.com/lay295/TwitchDownloader
- Cross-referenced: `metaleey/AI-auto-segment-edit-video-pipeline` — https://github.com/metaleey/AI-auto-segment-edit-video-pipeline (documented in the sibling file `deep_dive_ingestion_and_pipelines.md`)

The document has **four structural sections that are easy to miss on a skim**, because two of them share the identical heading text `## Audit pass — additional files read [2026-07-29]` (one at line ~280 covering Repos 1–2, one at line ~654 covering Repo 3), plus a `### ClipsAI completion note` at line ~445 and the `## Cross-repo synthesis` at line ~1189. **Roughly 60% of the file's substance is in those audit passes, after the three "Repo N" sections most readers would treat as the whole document.** The audit passes explicitly correct the earlier sections.

---

## A. Complete / portable code or config

### A1. TextTiling depth-score computation (the mathematical core of "is there a story break here")
**Grep:** `# clipsai/clip/texttiler.py — TextTiler._calc_depth_scores` (line ~91)
Complete, self-contained ~18-line Python loop. For every gap, walk backward and forward until the gap-score curve stops rising to find local peaks, then `depth_score = (left_peak - gap_score) + (right_peak - gap_score)`.
**How it helps:** This is a drop-in function. It has no dependency on the embedding model, on WhisperX, or on ClipsAI's class structure — it takes a 1-D array of similarity scores and returns a 1-D array of depth scores. We can feed it *any* time-series similarity curve, not just sentence embeddings (e.g. an audio-loudness curve or a chat-velocity curve), and get "deep valley between two peaks" boundary candidates out. It solves the specific problem that a clip shouldn't open or close mid-sentence.

### A2. TextTiling boundary cutoff with the "must beat both neighbors" guard
**Grep:** `# clipsai/clip/texttiler.py — TextTiler._identify_boundaries` (line ~116)
```python
cutoff = avg + stdev  # cutoff_policy == "high" (the default)
```
plus the check that `depth_scores[i]` must exceed **both** `left_neighbor` and `right_neighbor` to count as a boundary.
**How it helps:** The doc explicitly flags *why* this matters — "this is what keeps boundaries sparse instead of firing on every dip above the mean" and "prevents doubled-up boundaries at the same topic shift." Any thresholding we do on any signal curve should copy this two-part shape (absolute cutoff AND true local maximum). Selectable policies are `"high"` / `"average"` / `"low"`.

### A3. The multi-resolution `k` schedule for TextTiling
**Grep:** `Multi-resolution passes with different` (line ~49)
Concrete parameters: `k = [5, 7]` for candidate clips under 3 minutes; `k = [11, 17]` for 3+ minute clips; `k = [37, 53, 73, 97]` for 10+ minute clips. Recursively re-segments already-merged super-clips, `_text_tile_multiple_rounds`, `looping while len(clip_embeddings) > 8`. Dedupe rule: `_is_duplicate` — two clips are the same if the **sum of their start-time and end-time deltas is under 15 seconds**.
**How it helps:** The doc's own recommendation is to "reuse the same tiered `k` schedule ... rather than inventing our own." These are tuned constants from a 522-star production library — free calibration we would otherwise have to discover by trial and error. The 15-second sum-of-deltas dedupe rule is directly portable to our own clip de-duplication.

### A4. Audio loudness peak-finding parameters (the candidate-seeding stage)
**Grep:** `Loudness peak-finding is the seed step` (line ~147)
Full recipe: 16 kHz mono extraction → `librosa.feature.rms()` → z-score (`_normalize_signal`, zero-mean/unit-variance) → `gaussian_filter1d(sigma=1.0)` → `scipy.signal.find_peaks()` with `peak_prominence` = **0.6 std devs** and `peak_distance` = **1.0s** minimum spacing → pad `± clip_padding` (**default 15s**) around each peak.
**How it helps:** This is the entire stage-1 free pre-filter, with real defaults, ready to implement. Note the documented caveat that the window is "**not** derived from how long the loud moment actually lasts, it's always a fixed-width window centered on the peak" — a known limitation to improve on, not copy blindly.

### A5. The four-signal weighted-sum combiner (kept as a *shape* reference)
**Grep:** `# src/detector.py — _score_candidate` (line ~249)
```python
combined = (
    det_cfg["weight_loudness"] * loudness_score
    + det_cfg["weight_transcript"] * trans_score
    + det_cfg.get("weight_chat", 0.0) * chat_score
    + det_cfg.get("weight_visual", 0.0) * visual_score
)
```
Default weights `{loudness: 0.4, transcript: 0.6, chat: 0.4, visual: 0.4}`; keep if `combined >= min_score` (**default 0.7**); greedy NMS `_merge_clips` sorts by score descending and keeps a window only if its start isn't within `min_distance` (**10s**) of an already-kept window.
**How it helps:** The formula shape and the NMS dedup are directly reusable. **See B5 — the normalization is broken and must be fixed before reuse.**

### A6. Chat-velocity time-series construction from raw Twitch chat replay JSON
**Grep:** `# src/chat_parser.py — compute_chat_velocity` (line ~262)
```python
bins = np.arange(t_min, t_max + bin_width, bin_width)
counts, _ = np.histogram(df["time"], bins=bins)   # messages per second-bin
times = (bins[:-1] + bins[1:]) / 2
return times, counts.astype(float)
```
Default `bin_width=1.0s`. Paired normalization step, deliberately done in `main.py` not inside the function:
**Grep:** `if chat_vel_global is not None and chat_vel_global.std() > 0` (line ~274)
**How it helps:** Four lines gets a chat log to a comparable time-series signal. The doc explicitly flags the placement as instructive: normalizing in the caller, not the extractor, is "the 'right' place to normalize." **See B1 for the bug in the same file.**

### A7. The cluster → pad → clamp → discard-short skeleton (the single strongest architectural finding in the file)
**Grep:** `# analysis/arc_clip_detector.py — Clusterer.cluster` (line ~612)
Full ~25-line function quoted verbatim. Filter to hot frames (`final_score >= self.thresh`), sort by timestamp, greedily group if within `self.gap` seconds of the cluster's last frame, then per cluster: `s = max(0, cf[0].timestamp_seconds - self.pad)`, `e = cf[-1].timestamp_seconds + self.pad`; if `(e - s) > self.max_d` re-center on the peak-scoring frame and take a fixed `max_d`-wide window; if `(e - s) < self.min_d` **discard the cluster entirely**.
Real defaults, from the doc: threshold **30–45** on a 0–100 scale (**35 for `v3_temporal`**, the default scoring version), `merge_gap` **5s**, `pad` **2s** (CLI) / **2.0s** hardcoded in the web-adapter path, `max_d` **60s**, `min_d` **3s**. Then a *second*, separate clamp for export: `[min_clip_duration, max_clip_duration]` **default 20–60s with a flat `+10s` extension added**.
**How it helps:** The doc's bottom line calls this "the piece most directly reusable *as code*, not just as inspiration," because "it only depends on `(timestamp, score)` pairs, not on how the score was produced." This is the exact mechanism that converts "Gemini says this window is exciting" into a real clip boundary. The two-stage clamping (clustering window vs. exported window, export biased longer for watchability) is a non-obvious design decision worth copying deliberately.

### A8. Blend-with-safety-floor combiner
**Grep:** `# analysis/arc_clip_detector.py — ScoringEngine.combine` (line ~643)
```python
blended = yolo * 0.65 + pixel * 0.35
f = max(blended, pixel * 0.8) if pixel >= 60 else blended
if boss:
    f = max(f, 85)
return min(100, f)
```
**How it helps:** Six lines encoding a real design principle: an expensive ML channel must not be able to *suppress* an unambiguous cheap-channel hit. Direct analogue for us: a Gemini score of 20 should not be allowed to bury an audio-RMS peak that's 4 sigma above baseline. The `boss` floor is the template for our own must-clip conditions — the doc suggests "a detected donation/subscription alert, a clear on-screen 'NEW RECORD' type overlay."

### A9. LLM-vision request payload (OpenAI-compatible, trivially portable to Gemini)
**Grep:** `# analysis/ai_analyzer.py — GrokVisionAnalyzer._call_grok` (line ~721)
Full payload dict with system prompt, `image_url` as `data:image/jpeg;base64,{image_b64}`, `"max_tokens": 150`, `"temperature": 0.3`.
Encoding: `cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])` then base64. Sampling: one frame every `sample_interval_sec` = **8s** at the `app.py` call site (class docstring default is 10s).
**How it helps:** This is prior art for the exact thing our project plans to build, already working end to end against a different vendor. The doc explicitly says it is "trivially portable to Gemini's `generateContent` with an inline image part, which is the project's actual target." The concrete numbers (quality 60, max_tokens 150, temp 0.3, 8s interval) are a real starting calibration for cost-per-analyzed-second. **See E9 for the failure mode this file also demonstrates.**

### A10. The structured 0.0–1.0 scoring rubric for an LLM vision prompt
**Grep:** `Prompting is entirely game-profile-driven` (line ~702)
The written scale, quoted from the doc: "0.0 = menu/nothing, 0.3 = minor action, 0.6 = good combat, 0.8 = kill/major moment, 1.0 = insane play", with categories kills / combat / Arc encounters / explosions / close calls / loot / deaths.
**How it helps:** The doc calls this "a genuinely good example of a structured scoring rubric to steal the *shape* of for a Gemini prompt." Anchored numeric scales with named exemplars at each rung are what make LLM scores comparable across calls — critical if we're going to threshold them downstream in A7's clusterer. The architectural point matters too: the rubric lives in a *data file* (`game_profiles.py`), so "what counts as exciting" changes per streamer/game without touching detector code.

### A11. Direct Twitch GQL chat fetch — no external binary, pure stdlib
**Grep:** `# analysis/chat_detector.py — ChatSpikeDetector._fetch_chat` (line ~846)
```python
body = [{
    "operationName": "VideoCommentsByOffsetOrCursor",
    "variables": {"videoID": vod_id},
    "extensions": {"persistedQuery": {"version": 1,
        "sha256Hash": "b70a3591ff0f4e0313d126c6a1502d79a1c02baebb288227c582044571e9e5a4"}}
}]
req = urllib.request.Request("https://gql.twitch.tv/gql", data=json.dumps(body).encode("utf-8"),
    headers={"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko", "Content-Type": "application/json"},
    method="POST")
```
Paginates via GQL cursors up to a **200-page safety cap**; offset field is `contentOffsetSeconds` per comment node; bucketed into fixed **5-second** windows in `_build_histogram`.
**How it helps:** This is the highest-value single artifact in the file for our project. It gets full VOD chat replay with zero dependencies (`urllib` + `json`), no subprocess, no external `.exe`, no Twitch API key/OAuth. The persisted-query SHA-256 hash and the public web Client-ID are both recorded verbatim, so this is copy-pasteable today. The doc's explicit reversal: this is "arguably *more* portable for our project than twitch-clip-miner's `TwitchDownloaderCLI` dependency ... worth using this file's persisted-query pattern **instead of the Repo 2 approach previously recommended**."

### A12. Chat-spike threshold that a sensitivity setting can bend
**Grep:** `# analysis/chat_detector.py — ChatSpikeDetector._find_spikes` (line ~866)
```python
spike_threshold = avg + std_dev * (2.0 - self.intensity_threshold * 2)
spike_threshold = max(spike_threshold, avg * 1.5)   # at least 1.5x average, regardless
```
**How it helps:** Better than a flat z-score cutoff (Repo 2's approach) because the sigma multiplier is a tunable knob and the `avg * 1.5` floor prevents a low-variance chat (a quiet stream) from producing spurious spikes from tiny absolute movements. Directly applicable to @LacyCrashOuts's chat, whose baseline rate we don't know in advance.

### A13. ffmpeg-native per-second peak loudness — no numpy/scipy/librosa at all
**Grep:** `astats=metadata=1:reset=48000` (line ~887)
```python
cmd = ["ffmpeg", "-i", video_path,
       "-af", "astats=metadata=1:reset=48000,"
              "ametadata=print:key=lavfi.astats.Overall.Peak_level:file=-",
       "-f", "null", "-"]
```
Then a per-second max plus a linear dB-to-0..1 scale between `audio_threshold_db` (**-15dB** for Arc Raiders) and `audio_ceiling_db` (**-3dB**).
**How it helps:** A complete alternative to A4 with a "strictly lighter dependency footprint." The doc recommends preferring it "for a v1 if we don't already have scipy in the pipeline for another reason." We already ship ffmpeg. This eliminates librosa (a heavy, slow-importing dependency) from the critical path entirely. Note it is copy-pasted verbatim three times in that repo (`audio_detector.py`, `detector.py`, `hybrid_detector.py`) — write it once, shared.

### A14. Verbal "clip that" trigger detection — a whole detection paradigm in ~2 constants
**Grep:** `DEFAULT_TRIGGER_PHRASES` (line ~914)
```python
DEFAULT_TRIGGER_PHRASES = ["clip that", "clip this", "clip it", "clip me", "clip"]
CLIP_FALSE_POSITIVES = {"ping", "ped", "per", "board", "s", "ping", "art"}
```
**Grep:** `# analysis/clip_trigger_detector.py — _triggers_to_highlights` (line ~930)
```python
clip_start = max(0, t - self.clip_duration)          # duration BEFORE the trigger
clip_end = min(t + self.pre_pad, duration) if duration else t + self.pre_pad
```
Uses **word-level** Whisper timestamps, not segment-level, to anchor precisely on the trigger word.
**How it helps:** The doc rates this "directly reusable for our project regardless of what other signals we build — verbal clip triggers are a free, zero-inference-cost signal once we're transcribing anyway." The retroactive windowing is the genuinely clever bit: "clip that" is said *after* the exciting thing, so the clip must extend backward. For a reaction streamer like @LacyCrashOuts this is likely a very high-precision signal. **See B7 for the flaw in the false-positive list.**

### A15. Universal sensitivity slider → threshold multiplier
**Grep:** `sensitivity_multiplier = 1.6 - (sensitivity / 100) * 1.3` (line ~800)
0 = very selective (`threshold*1.6`), 50 = default (`*1.0`), 100 = catch everything (`*0.3`). Applied to `intensity_threshold`, plus a separate linear dB shift for audio: `audio_adjust = (sensitivity/100 - 0.5) * 8`. Applied through a generic `_apply_sensitivity(det)` helper that duck-types on `hasattr(det, 'profile')` / `hasattr(det, 'intensity_threshold')`.
**How it helps:** One continuous knob that works across every detector class without bespoke wiring per detector. For a Colab pipeline this becomes a single top-of-notebook cell variable that meaningfully changes clip yield without touching any detector's internals.

### A16. Discrete named scoring presets as the alternative sensitivity mapping
**Grep:** `# 0-19: v1_strict | 20-39: v5_combat_only` (line ~813)
Full ladder: `0-19: v1_strict | 20-39: v5_combat_only | 40-59: v3_temporal (DEFAULT) | 60-79: v2_balanced | 80-100: v4_aggressive`.
**How it helps:** Shows the other viable UX shape — named tiers instead of a continuous multiplier. The doc flags this was invisible when reading `arc_clip_detector.py` in isolation. Useful for us as a "preset" concept: `strict` / `balanced` / `aggressive` runs over the same VOD.

### A17. The `detection_overrides` escape-hatch allow-list
**Grep:** `A free-form ` + `detection_overrides` (line ~820)
Exact allow-listed keys: `intensity_threshold, audio_weight, audio_threshold_db, merge_gap, min/max_clip_duration, fallback_threshold_ratio, window_seconds, brightness_threshold, sample_fps, peak_weight, menu_suppress, trigger_phrases`. Applied **after** the sensitivity multiplier so overrides always win.
**How it helps:** This list *is* the complete tunable-parameter surface of a working clipper — a ready-made schema for our own config file. The ordering rule (overrides applied last) is the correct precedence design.

### A18. Max-of-signals-with-agreement-bonus fusion (the better combiner)
**Grep:** `# analysis/hybrid_detector.py — _analyze_video_pass` (line ~977)
```python
max_score = max(audio_score, motion_score, scene_score)
signals_active = sum(1 for s in [audio_score, motion_score, scene_score] if s >= 0.2)
if signals_active >= 3:
    fused = min(max_score * 1.3, 1.0)
elif signals_active >= 2:
    fused = min(max_score * 1.15, 1.0)
else:
    fused = max_score
```
**How it helps:** The doc's own late-breaking recommendation, arguing this is "arguably better-motivated" than every weighted sum in the research: "a moment only needs one strong signal to qualify" but agreeing signals boost confidence multiplicatively. Critically: "it naturally handles the 'we don't have all signals available every run' case (audio-less clips, chat-less clips) **without needing to re-tune weights per available-signal-set**." That is exactly our situation — we will add chat, then vision, then transcript signals incrementally. A weighted sum would need re-tuning at every step; this doesn't.

### A19. The production clip-extraction ffmpeg command
**Grep:** `# clip_manager.py — extract_clips` (line ~1082)
```python
# -ss after -i = frame-accurate (decode from nearest keyframe); before -i is fast but off by 1-5s
cmd = ["ffmpeg", "-y", "-i", video_path, "-ss", str(start_time), "-to", str(end_time),
       "-c:v", "libx264", "-preset", "fast", "-crf", "23",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", clip_path]
```
Naming: `{job_id}_{clip_id}.mp4` with an 8-char UUID prefix. Thumbnail grabbed at the clip's temporal midpoint, falling back to the clip's first frame.
**How it helps:** Copy-paste-ready export command with the accuracy-vs-speed tradeoff documented inline (`-ss` placement is off by 1–5s if it precedes `-i` — a real precision loss for short reaction clips). `+faststart` matters for web/social upload. The `clip_info` record shape is also given verbatim: `id`, `filename`, `thumbnail`, `start_time`, `end_time`, `duration`, `label`, `confidence`, `timestamp_display` — "the canonical 'highlight → clip' record shape every detector's output eventually flows into."

### A20. Naive centered 9:16 crop (the baseline to beat)
**Grep:** `crop=ih*9/16:ih` (line ~399)
`crop=ih*9/16:ih,scale=1080:1920` plus fixed 0.5s fade-in/out on both video and audio.
**How it helps:** Two-filter one-liner that gets a vertical clip out the door on day one. The 0.5s A/V fades are a small polish detail worth keeping. The doc deliberately contrasts this against the better options below.

### A21. Dual-region vstack vertical composition (gameplay + webcam)
**Grep:** `make_tiktok()` (line ~1102)
A single `-filter_complex` that crops independent gameplay and webcam regions (passed as 0–1 ratios so a user visually selects both boxes), scales/pads each to a 1080-wide strip, and `vstack`s them into **1080×1920**. YouTube Shorts variant additionally reserves an **80px black `safezone` bar at the top** for the platform's own UI overlay before stacking.
**How it helps:** This is the actual format Twitch clips get reposted in — facecam stacked over gameplay. The 80px Shorts safezone is exactly the kind of platform detail that costs a day to discover empirically. Ratio-based (not pixel-based) region specification means one config works across VOD resolutions.

### A22. Three-step ffmpeg watermark recipe
**Grep:** `watermark_and_crop_video()` (line ~469)
`colorchannelmixer=aa={opacity}` to make the logo translucent → `scale2ref` to size the logo *relative to the video* (not a fixed pixel size) → `overlay=(x):(y)`.
**How it helps:** "A clean, reusable three-step ffmpeg watermark recipe if this project ever wants to burn in a logo/CTA overlay." `scale2ref` is the non-obvious part — it's what makes one watermark config work at any input resolution.

### A23. Two-tier video-duration probe with a real fallback
**Grep:** `get_video_duration()` (line ~401)
Try `ffprobe -show_entries format_duration` first; on exception, regex-parse the human-readable `Duration: HH:MM:SS.ff` line out of `ffmpeg -i`'s **stderr**.
**How it helps:** The doc calls it "a robustness pattern for any pipeline that can't assume `ffprobe` is present/working." Relevant for Colab/Windows environments where the ffmpeg build may not ship ffprobe.

### A24. Cheap no-ML smart thumbnail selection
**Grep:** `get_smart_thumbnail()` (line ~1110)
Sample N evenly-spaced candidate frames, score each via `ffprobe … signalstats` using `YMAX - YMIN` for contrast, penalized by distance of `YAVG` from mid-gray **128**; keep the highest-contrast, most-mid-toned frame.
**How it helps:** "A genuinely useful, cheap (no ML) 'pick a good thumbnail' heuristic." Zero API cost, ffmpeg-only, and directly usable for clip thumbnails or for choosing which frame to send to a vision model.

### A25. Menu / loading-screen suppression as a hard gate
**Grep:** `Menu/loading-screen suppression is a hard gate` (line ~953)
`_is_menu_frame` checks for near-black frames (`mean_brightness < 0.04`) or a uniform dim center region (`std < 10 and brightness < 0.25`) and forces `score = 0.0` **unconditionally** — the override fires "even when audio is loud, explicitly to stop a gunshot playing over a loading screen from producing a false highlight (`if label == "Menu/Lobby": score = 0.0` regardless of `audio_score`)."
**How it helps:** Direct analogue for Twitch: starting-soon screens, BRB screens, ad breaks, and stream-transition scenes. These are the classic false-positive source for an audio-driven clipper (loud music over a BRB screen). Three cheap OpenCV numbers kill the whole class. `hybrid_detector.py` reimplements the same guard with an extra low-saturation check and optional `menu_suppress_colors`.

### A26. FER visual-engagement sampling config
**Grep:** `Facial-emotion recognition is real, working code` (line ~180)
`max_samples: 8`, one every `sample_rate: 2.5s`, score = mean of `happy + surprise` intensity across evaluated frames (capped at 1.0 per frame), results **cached to disk per `(video, start, end)`**. Gated off by `visual_enabled: false` in `config.yaml`. Defensively coded: graceful `ImportError` fallback, a `VISUAL_AVAILABLE` flag threaded through the whole pipeline, stderr-suppression around noisy OpenCV/FFmpeg logging.
**How it helps:** "A 30-second window only ever gets ~8 real inference calls, not a dense per-frame scan." Complete config for a free local facecam-reaction signal. See C3 and D8 for why the doc later reverses its position on this.

### A27. Pluggable transcription backend + GPU/CPU auto-detection
**Grep:** `transcribe_audio_auto()` (line ~414) and `src/transcriber.py` uses faster-whisper (line ~406)
`ctranslate2.get_cuda_device_count() > 0` picks `small` + `cuda` + `float16`, else `base` + `cpu` + `int8` (the check also covers ROCm on AMD per the code's own comment). `transcribe_audio_auto()` is driven by `config.yaml`'s `transcription.backend` (`auto` / `whisper-cpp` / faster-whisper); in `auto` mode it checks whether a whisper.cpp binary **and** ggml model file both exist on disk and prefers that (citing Vulkan GPU acceleration).
**How it helps:** "A real, reusable pattern for a transcription module that has to work across heterogeneous end-user hardware without requiring a specific backend to be installed." Directly relevant: our sister project runs in Colab (GPU available, varies by session), and this project may run locally on Windows. One module, both environments, no code change.

### A28. whisper.cpp CLI flags for word-level timestamps
**Grep:** `--word-thold 0.01 --split-on-word --max-len 0 --best-of 5` (line ~421)
**How it helps:** The exact flag set to get word-level timestamps out of whisper.cpp — required for A14's verbal-trigger anchoring and for any caption burn-in. `--max-len 0` disables segment length limiting; `--split-on-word` prevents mid-word splits.

### A29. NaN-safe fps guard, consolidated
**Grep:** `# analysis/video_utils.py` (line ~1059)
`probe_video()` / `safe_fps()` / `frame_interval_for()`, extracted specifically because `cap.get(cv2.CAP_PROP_FPS)` returns NaN on some codec/container combinations.
**How it helps:** Three tiny functions that every frame-sampling code path needs. See E17 for the specific broken idiom to avoid.

### A30. Long-VOD chunking parameters
**Grep:** `Long VODs (>30 min) are processed in overlapping 15-minute chunks` (line ~205)
`src/chunker.py`, `process_video_in_chunks`: VODs over 30 min → **15-minute chunks with 30s overlap**; each chunk independently re-runs the full detect pipeline on chunk-local timestamps; results shifted back to global VOD time; merged/deduplicated with the same NMS across the whole VOD.
**How it helps:** Twitch VODs are routinely 4–8 hours. This is the memory-safety and progress-checkpointing pattern with real numbers. The 30s overlap is what prevents a moment straddling a chunk boundary from being lost.

### A31. ClipsAI face-tracking / active-speaker crop mechanics
**Grep:** `How the crop position is actually chosen` (line ~306)
Full pipeline: speaker diarization + scene-change timestamps merged (`_merge_scene_change_and_speaker_segments`) so a crop segment never spans a hard cut → face search starting **an eighth of the way into the segment** (skipping likely-silent lead-in) with `facenet_pytorch.MTCNN` → face boxes clustered with `sklearn.cluster.KMeans` (k = number of distinct faces) into per-person tracks → **MediaPipe FaceMesh** computes mouth-aspect-ratio (`avg_mouth_height / mouth_width`, using specific landmark index sets for upper/lower inner lip) per frame per track → **ROI is whichever tracked face's MAR *changes the most* across frames** (i.e. whoever is actually talking, not who's biggest/most-centered). Fallbacks: no mouth movement → the face appearing in the most sampled frames; no face at all → center 50%×50% box. `_merge_identical_segments` collapses adjacent segments whose crop centers differ by less than **4% of width/height** (`max_position_difference_ratio = 0.04`) to prevent micro-jitter.
**How it helps:** This is the concrete answer to "how do you reframe 16:9 to 9:16 without cutting off the speaker," and the doc rates it "a substantially better reframing technique than a naive centered crop." The MAR-delta active-speaker trick is the genuinely novel part. The 0.04 anti-jitter threshold is a real tuned constant.

### A32. Character-index resync for sentence alignment
**Grep:** `# clipsai/transcribe/transcription.py — _realign_char_idx_with_sentence` (line ~364)
```python
for offset in range(1, search_window_size * 2):
    offset *= -1
    if char_info[char_idx + offset]["char"] == correct_char:
        return char_idx + offset
# realignment failed -> raise TranscriptionError
```
A ±3-character fuzzy search window.
**How it helps:** Required glue if we port TextTiling. WhisperX returns character-level alignments (`return_char_alignments=True`); NLTK's `sent_tokenize()` normalizes whitespace/quotes, so the two drift. Without this resync, sentence timestamps silently go wrong. **See E3 for why this is also a fragility warning.**

### A33. yt-dlp VOD download configuration
**Grep:** `concurrent_fragment_downloads=16` (line ~1096) and `src/downloader.py` (line ~390)
The simple version: a 29-line `yt-dlp` wrapper with `format: 'best[height<=1080]'`, hardcoded. The tuned version: `concurrent_fragment_downloads=16` with the code's own comment — "Twitch HLS has 4-10s fragments; pulling 16 at a time saturates home broadband and cuts 1h-VOD downloads from ~8 min to ~2 min" — plus a 5-tier progress-percentage cascade (total-bytes → fragment-index → `_percent_str` parsing → elapsed-time estimate → file-size-growth estimate) and exponential-backoff retry (up to 3 attempts) on network-class errors.
**How it helps:** See D9 — this is a 4× real speedup on the single slowest non-API step in the whole pipeline, and it's a one-line option.

### A34. Fast frame-skip during sampling
**Grep:** `cap.grab()` (line ~549)
Non-sampled frames call `cap.grab()` (advances the decoder without the color-convert + numpy copy that `cap.read()` does) instead of decoding frames that will be thrown away. Default `SAMPLE_INTERVAL = 1.0` (1 fps), overridable via `sample_fps`.
**How it helps:** A one-token change (`grab` vs `read`) that removes the dominant CPU cost of scanning a multi-hour VOD at 1 fps. Free speedup, no accuracy loss.

### A35. Combination-rules-as-lambdas pattern
**Grep:** `COMBINATION_RULES` (line ~531)
A list of `{name, cond: lambda counts: ..., bonus, category}` entries — e.g. `"pvp_kill": raider>=1 and raider-down>=1 → +55`, `"squad_wipe": raider-down>=2 → +65`. Plus: `base` score and `count_bonus` per entity class; **1.3× multiplier** if any bounding box exceeds **20% of frame area**; hard floor of **90** if a boss-class entity is present; **1.2× multiplier** if multiple detected entities are spatially close (mean pairwise normalized distance **< 0.3**).
**How it helps:** "A clean, easily-extensible way to encode 'these signals together mean something special' without a tangle of nested if/elif." Our version: `"loud audio peak + chat velocity spike + Gemini-reported laughter"`. The spatial-proximity multiplier is a transferable idea — co-occurrence *in time* rather than in space, for our signals.

### A36. LLM retry / circuit-breaker policy
**Grep:** `Retry/failure handling is real, not aspirational` (line ~708)
`_analyze_single` retries transient errors (429/500/503/timeout) twice with `2**(attempt+1)`s backoff; the whole `analyze_frames` run **aborts early after 5 consecutive failures** (`"AI API failing consistently"`).
**How it helps:** The circuit breaker is the budget-protection mechanism — it stops a dead API key or an outage from burning the entire run's quota producing zero output. Directly applicable given this project's documented budget sensitivity.

### A37. Highlight-assembly fallback when nothing clears the bar
**Grep:** `Highlight assembly mirrors the same cluster-and-pad shape` (line ~712)
Keep frames with `exciting=True` and `score>=0.4`; **fall back to the top 5 scored frames with `score>=0.2`** if nothing clears the bar; merge if within `merge_gap` (profile-driven, **default 15s**); clamp to `[min_clip_duration, max_clip_duration]` plus a flat `clip_extension`.
**How it helps:** Prevents the worst UX outcome — a full paid analysis run that returns zero clips. Always return *something*, ranked. Trivially cheap to implement, high practical value.

### A38. `ClipMode` enum as a signal-mix switch
**Grep:** `**`ClipMode` enum (`clip_modes.py`)**` (line ~575)
`CV`, `YOLO`, `VOICE`, `HYBRID` (= CV+YOLO), `ALL` — gates which detectors run from a single config value.
**How it helps:** "A useful pattern if we want a similar 'pick your signal mix' switch" rather than hardcoding a fixed pipeline. Lets us A/B signal combinations on the same VOD from one config value.

### A39. Scene detection and efficient frame extraction (ClipsAI `vid_proc.py`)
**Grep:** `Scene detection (`vid_proc.py`) uses PySceneDetect's `AdaptiveDetector`` (line ~337)
`AdaptiveDetector` with `min_scene_len` tied to `min_scene_duration * fps`. `extract_frames` uses **PyAV**, seeking to the nearest keyframe then decoding forward to the exact target PTS, parallelized via `ThreadPoolExecutor` for the post-decode numpy/downsample/grayscale step.
**How it helps:** Real efficient random-access frame pulling — much faster than OpenCV sequential decode when you need scattered timestamps (exactly the access pattern for "score these 40 candidate windows"). `AdaptiveDetector` is a maintained third-party library, not custom code.

---

## B. Fixable code — start from it, but fix the documented defect first

### B1. `compute_chat_velocity(df, time_range=...)` — `.min()` where `.max()` belongs
**Grep:** `**Caveat found in the code:**` (line ~173)
Exact defect quoted in the doc: `t_max = df["time"].min() if time_range else df["time"].max()` — uses `.min()` instead of `.max()` when a range is supplied, "which would silently collapse the bin range to near-zero width."
**Status:** Latent, not firing. "Both `main.py` and `chunker.py` avoid passing `time_range` and slice the arrays by boolean mask instead."
**How it helps:** The rest of the function (A6) is exactly right. Copy it, change one `.min()` to `.max()`. The doc is explicit: "this exact function is not safe to reuse verbatim without fixing that line first." Note also the workaround the original authors used — boolean-mask slicing instead of the `time_range` parameter — is itself a valid path.

### B2. `src/transcriber_whisper_cpp.py` — two real bugs, one of which masks all errors
**Grep:** `**`src/transcriber_whisper_cpp.py` shells out to a `whisper-cli.exe` binary**` (line ~420)
1. Default `whisper_cli` path is hardcoded to the original author's personal machine: `C:/Programming/Projects/Python/twitch-clipper/tools/whisper-cli.exe`. Harmless in-repo because `transcribe_audio_auto()` always overrides it, but "calling this function directly with defaults silently fails on any other machine."
2. `subprocess.run(cmd, shell=True, check=False)` **without** `capture_output=True`, so `proc.stderr`/`proc.stdout` are always `None` — meaning its own error-logging path `logger.error(proc.stderr[-1000:])` would raise `TypeError: 'NoneType' object is not subscriptable`. "The failure-handling code is broken and would mask the real error with a crash."
**How it helps:** Both fixes are one-liners (path from config; add `capture_output=True`). The rest of the file is worth keeping — its output parser "does defensively handle two different whisper.cpp JSON schema shapes (a newer segment-based format with millisecond offsets, and an older word-based format)," which is real evidence whisper.cpp's output format has changed across versions.

### B3. faster-whisper `vad_filter` — documentation and shipped default disagree
**Grep:** `**Real inconsistency found**` (line ~408)
"The module docstring explicitly recommends `vad_filter=True` ('great for VODs with long silences/quiet gameplay') but the actual shipped call hardcodes `vad_filter=False`."
**How it helps:** Flip it to `True`. The docstring is correct and the rationale is exactly our use case — Twitch VODs are full of dead air. This is a straight speed win on the transcription step (see D11). Note `clip_trigger_detector.py` in the *other* repo does use `vad_filter=True` "to skip silence for speed" — so the two repos disagree and the doc records which one is right.

### B4. Transcript cache keyed only on filename stem
**Grep:** `keyed only by filename stem with no content hash` (line ~412)
Transcripts cached to `{audio_stem}_words.json`, so "a same-named-but-different audio file with `force=False` would silently return a stale cached transcript."
**How it helps:** Caching transcripts is the right idea (D10) — just key on a content hash, not a filename. This is the exact class of silent-wrong-output bug that costs hours to diagnose, pre-identified.

### B5. The un-normalized weighted-sum combiner
**Grep:** `**Combining the signals is a flat, un-normalized weighted sum**` (line ~194)
Loudness and chat are pre-normalized (z-scored); transcript score is **raw/unbounded**; visual score is bounded 0–1. "Mixing normalized and unnormalized channels in one linear sum is a real weakness — a big transcript-score outlier can dominate regardless of weight." Separately, weights don't sum to 1.0: "the comment literally says 'adjust so total roughly 1.0' and the shipped defaults don't."
**How it helps:** The doc names this "the one clear mistake worth not repeating." Fix = z-score or min-max **every** channel before summing. Note the identical mistake appears **independently** in `detector.py`'s `GameDetector` — "the same 'un-normalized weighted sum' pattern flagged as a weakness in twitch-clip-miner's combiner (Repo 2) shows up here too, independently" (line ~961). Two separate authors made the same error; we should not be the third. A18 sidesteps it entirely.

### B6. `chat_spikes` VOD-ID extraction fails for library/watch-folder jobs
**Grep:** `**A real, if minor, bug:**` (line ~830)
`chat_spikes` reads the VOD URL from `job.get("url", "")`. Works for `/api/analyze` with a live URL, but a job re-analyzed from the saved library has `job["url"] = f"library:{filename}"`, and `ChatSpikeDetector._extract_vod_id`'s regex won't match — "chat-spike detection silently returns zero highlights (logged, not crashed) for any library re-analysis. Same class of bug for `watch:{filename}` jobs."
**How it helps:** Design lesson we get for free: store the **VOD ID as a first-class field on the job record** from the moment of ingestion, rather than re-deriving it from a URL string that gets rewritten by other code paths. Silent-zero-results is the worst failure mode for a detector.

### B7. `CLIP_FALSE_POSITIVES` implements suffix exclusion as next-word exclusion
**Grep:** `The false-positive set is a negative lookahead` (line ~918)
The doc's own analysis: it's "matching the word *following* 'clip', so 'clip ping' would need to actually be spoken, which doesn't obviously correspond to any of those words appearing as suffixes; this looks like an attempt at suffix exclusion implemented as next-word exclusion and **may not actually catch 'clipping' the way intended, since 'clipping' is one token, not 'clip' + 'ping'**." Also note `"ping"` appears twice in the set.
**How it helps:** The intent is right and the fix is straightforward — do the exclusion as a suffix/word-boundary regex on the token itself (`\bclip\b` not matching inside `clipping`/`clipboard`/`clipper`) rather than as a next-word blacklist. Everything else about A14 is sound.

### B8. ClipsAI `resize_video()` — N+1 ffmpeg subprocesses and N temp files
**Grep:** `**The concrete, previously-missing answer to "how does ClipsAI actually render` (line ~454)
It loops over every segment, calls `crop_video()` once per segment (a separate `ffmpeg -ss/-to -vf crop=...` subprocess writing a real temp `.mp4` per segment), then `concatenate()` at the end, then deletes temps. Additionally: `crop_video()` "doesn't fast-seek (no `-ss` before `-i`; it's placed after `-i`, meaning it **decodes from the start of the file up to the seek point every time**)" and re-encodes with `-preset veryfast -crf 18`.
**How it helps:** The doc states the fix explicitly: "**metaleey's single-pass multi-input-seek+concat-filter technique (already recommended in the ingestion/pipelines file) is a strict efficiency improvement over what ClipsAI itself does** — N+1 ffmpeg subprocess invocations plus N temporary files on disk, versus one ffmpeg process with no intermediate files." So: take ClipsAI's *crop-position algorithm* (A31), but render it with metaleey's *execution* pattern (https://github.com/metaleey/AI-auto-segment-edit-video-pipeline, `merge_segments_direct`, documented in `deep_dive_ingestion_and_pipelines.md`). On a long VOD with many segments, the repeated decode-from-start is quadratic-ish in wall time.

### B9. ClipsAI diarization hard-drops short segments, losing speakers entirely
**Grep:** `hard-drops any segment under `min_segment_duration`` (line ~349)
`_adjust_segments` resolves overlap by cutting the *earlier* speaker's segment short at the next speaker's start, and hard-drops any segment under `min_segment_duration` (**default 1.5s**) "rather than merging it into a neighbor — speakers who only ever get short segments can end up entirely absent, which is why `_relabel_speakers` exists."
**How it helps:** For Twitch, short interjections *are* the content (a one-word reaction from a co-streamer). If we ever use diarization, merge short segments into neighbors instead of dropping them, or lower the 1.5s floor. The doc surfaces this as a real behavioral consequence, not a style nit.

### B10. `src/utils.py` is an empty stub
**Grep:** `**`src/utils.py` is confirmed to be an empty 4-line stub**` (line ~434)
Comment says "Shared helpers (time formatting, logging)", no code. "Not a coverage gap, just unused/aspirational scaffolding."
**How it helps:** Purely a negative finding — don't go looking for shared helpers there. Included for completeness so a future reader doesn't re-investigate.

### B11. `game_profiles.py` — corrections written, sourced, and never applied
**Grep:** `===== ARC RAIDERS V2 — Research-based detection =====` (line ~1041)
An orphaned comment block sits immediately above the `"war_thunder"` entry, containing real corrections to the `"arc_raiders"` profile directly above it — "NO kill feed — deaths emit a RED FLARE skyward", "NO hit markers — crosshair is dynamic", "THIRD-PERSON shooter — muzzle flash on character model, not center screen" — sourced inline (ARC Raiders Wiki, GameRant, GamingBolt, Steam Community). But "the live `"arc_raiders"` profile (lines 16–113) still defines `kill_feed` and `hit_marker` HSV detectors as if the corrections never happened ... no corresponding `arc_raiders_v2` key anywhere in the 4016-line file."
**How it helps:** If we ever reuse any HSV profile from that file, **do not trust the profile entries as validated**. More importantly this is a process warning that mirrors our own project's documented failure mode: research produced, never applied to the code. Worth a real check in our own repo.

---

## C. Free / unutilized tools (real, free, and not the current primary pick)

### C1. `lay295/TwitchDownloader` — https://github.com/lay295/TwitchDownloader
**Grep:** `TwitchDownloaderCLI.exe chatdownload` (line ~164)
Pulls a VOD's actual replay chat log as JSON with `content_offset_seconds` + message body per comment — "the real per-message timestamp Twitch stores against the VOD, the same data Twitch's own web player uses to render chat replay."
**Status in doc:** Recommended in Repo 2's section, then **superseded** by C2 in the later audit pass.
**How it could still help:** It's a fully maintained, battle-tested tool that also does VOD download and chat *rendering* (burned-in chat overlay video), which the raw GQL approach does not. Keep as the fallback if the GQL persisted-query hash goes stale, and as the path of least resistance if we ever want a rendered chat overlay in a clip.

### C2. Twitch's own GraphQL endpoint, direct — `https://gql.twitch.tv/gql`
**Grep:** `# analysis/chat_detector.py — ChatSpikeDetector._fetch_chat` (line ~846)
Public web Client-ID `kimne78kx3ncx6brgo4mv6wki5h1ko`; persisted query `VideoCommentsByOffsetOrCursor`, sha256 `b70a3591ff0f4e0313d126c6a1502d79a1c02baebb288227c582044571e9e5a4`. Pure stdlib `urllib` + `json`.
**How it helps:** Free, keyless, dependency-free, no external binary, no OAuth. This is now the doc's preferred chat source. Full code in A11.

### C3. `fer` (PyPI) + MTCNN / Haar-cascade face detection
**Grep:** `src/vision.py` wraps the `fer` PyPI package (line ~181) and the correction at `don't drop `fer`/MTCNN in favor of Gemini outright` (line ~1215)
A real FER2013-based CNN emotion classifier. Old/unmaintained, but working.
**Status:** `visual_enabled: false` by default in twitch-clip-miner; the doc's *first* pass recommended dropping it in favor of Gemini; the doc then **explicitly reverses that on 2026-07-30**.
**How it helps:** Quoting the correction directly: "`fer`/MTCNN are free, open, and run locally with zero API cost. That makes them a real candidate for the free **statistical pre-filter stage** (stage 1 of the funnel, alongside audio-RMS peaks) — flag high-facial-expressivity windows for free, *before* any Gemini call ... the two aren't actually competing for the same role once cost is accounted for." For a reaction streamer this is arguably the single most on-target free signal available.

### C4. `facenet_pytorch.MTCNN` — face detection
**Grep:** `using **MTCNN**` (line ~313). Free, pip-installable, GPU-capable. Used by ClipsAI for crop targeting; usable by us standalone for "is the facecam showing a face at all / how many faces."

### C5. MediaPipe FaceMesh — mouth-aspect-ratio / active-speaker detection
**Grep:** `**MediaPipe FaceMesh** computes a mouth-aspect-ratio (MAR)` (line ~320). Free, Google, CPU-fast, no API cost. Beyond reframing, MAR-delta is a cheap free proxy for "is the streamer talking/shouting right now."

### C6. `sklearn.cluster.KMeans` for face-track grouping
**Grep:** `clustered with **KMeans**` (line ~317). Free. The specific trick — cluster bounding boxes across sampled frames with k = number of distinct faces seen, to build per-person tracks — is a lightweight alternative to a real tracking library.

### C7. PySceneDetect `AdaptiveDetector`
**Grep:** `PySceneDetect's `AdaptiveDetector`` (line ~337). Free, maintained, "a real, maintained third-party library, not custom code." Not currently a chosen signal for us. Scene cuts are directly useful for Twitch (game↔BRB↔just-chatting transitions) as clip-boundary candidates and as menu-screen detectors.

### C8. PyAV — keyframe-seek frame extraction
**Grep:** `Frame extraction (`extract_frames`) uses PyAV` (line ~339). Free. "Real efficient random-access frame pulling" — meaningfully faster than OpenCV for scattered-timestamp access.

### C9. ffmpeg `astats` + `ametadata` filters (audio analysis with zero Python audio deps)
**Grep:** `astats=metadata=1:reset=48000` (line ~887). Free, already installed. See A13/D5.

### C10. ffmpeg/ffprobe `signalstats` for frame quality scoring
**Grep:** `ffprobe … signalstats` (line ~1111). Free. `YMAX - YMIN` contrast + `YAVG` distance from 128. Not currently used anywhere in our plan.

### C11. `librosa` + `scipy.signal.find_peaks` + `gaussian_filter1d`
**Grep:** `librosa.feature.rms()` (line ~148). Free. The heavier alternative to C9 — worth keeping as the option when we need a real RMS *curve* (for prominence-based peak-finding) rather than just per-second peak dB.

### C12. NLTK `sent_tokenize()`
**Grep:** `**NLTK's `sent_tokenize()`**` (line ~356). Free. The sentence splitter TextTiling runs on.

### C13. `sentence-transformers` / `all-roberta-large-v1`
**Grep:** `SentenceTransformer("all-roberta-large-v1").encode(sentences)` (line ~26). Free and local — "a generic sentence-embedding model, not a custom-trained one."
**How it helps:** Free local embeddings mean the TextTiling boundary layer costs **zero API budget**. The doc notes it's heavyweight and a smaller model or Gemini's embedding endpoint would substitute "without changing the algorithm" — but for budget purposes the free local option is the point.

### C14. WhisperX (with `return_char_alignments=True`)
**Grep:** `WhisperX's alignment step is called with `return_char_alignments=True`` (line ~355). Free. The character-level alignment is what makes precise sentence timestamps possible.

### C15. `faster-whisper` / CTranslate2
**Grep:** `**`src/transcriber.py` uses faster-whisper (CTranslate2)** ` (line ~406). Free, local, GPU or CPU.

### C16. `whisper.cpp` (`whisper-cli.exe`, ggml models) — Vulkan GPU acceleration
**Grep:** `citing Vulkan GPU acceleration` (line ~417). Free. **The Vulkan path is the notable bit** — it gets GPU acceleration on hardware where CUDA isn't available (AMD, integrated Intel), which matters for a Windows machine without an NVIDIA card.

### C17. `openai-whisper` (reference implementation) as a second fallback
**Grep:** `(`faster-whisper` preferred, `openai-whisper` fallback` (line ~908). Free.

### C18. `pyannote/speaker-diarization-3.1`
**Grep:** `pretrained `pyannote/speaker-diarization-3.1`` (line ~343). Free but **HuggingFace-gated (requires an auth token)** — the doc flags this as "a real external dependency/friction point." Relevant only if we do multi-person VODs. Performance number in E5.

### C19. `yt-dlp`
**Grep:** `thin, literal `yt-dlp` wrapper` (line ~390). Free. Confirmed as the VOD ingestion path in both relevant repos.

### C20. YOLOv11n + the Arc Raiders Roboflow dataset
**Grep:** `the bundled `models/best.pt` is a real YOLOv11n checkpoint, ~5.4 MB` (line ~514)
Fine-tuned on the Arc Raiders v0.11 Roboflow dataset (**2,880 training frames**), 13 shipped classes.
**How it helps:** Not directly reusable (wrong game), but it's a concrete, verified data point on what it costs to make a working per-game detector: **~2,880 labeled frames and a 5.4 MB nano model**. If we ever want a bespoke detector for @LacyCrashOuts's main game, that's the real order of magnitude.

### C21. Roboflow hosted workflow + hosted model (not free — flagged as the paid alternative)
**Grep:** `roboflow_analyzer.py` and `roboflow_model_analyzer.py` (line ~996)
`RoboflowWorkflowAnalyzer` streams video over **WebRTC** to a hosted workflow (`workspace="beanies-workspace"`, `workflow="detect-and-classify-3"`, `"webrtc-gpu-medium"` compute in the `"us"` region, via `inference_sdk.webrtc.VideoFileSource`/`StreamConfig`); `RoboflowModelAnalyzer` calls `InferenceHTTPClient.infer()` against `https://detect.roboflow.com` per frame, model ID `"arc-raiders-05arl-bgcvo/1"`.
**How it helps:** Two things. (1) The **WebRTC video-streaming** pattern is genuinely different from per-frame HTTP and is the closest analogue in this research to "send video, not stills" — relevant when comparing Gemini's video-native input. (2) The doc notes both "confirm 'cloud inference API called per-sampled-frame, scored by confidence/count, bucketed into windows' is a viable, previously-implemented pattern for exactly the kind of external-vision-API integration this project intends to build with Gemini instead of Roboflow." Caveat: the hosted workflow depends on a specific third party's named pipeline continuing to exist.

### C22. xAI Grok vision API — `https://api.x.ai/v1/models`, `grok-4-1-fast-non-reasoning` etc.
**Grep:** `_resolve_vision_model()` (line ~687). Not free, but a real, working **alternative vendor** to Gemini for the vision-scoring stage, with a documented cheapest-first model ladder (full list in E10). Worth keeping as a price-comparison and as a fallback if Gemini quota is exhausted mid-run.

### C23. `pywebview` + Flask
**Grep:** `desktop.py` (52 lines) is a thin `pywebview` wrapper` (line ~1127). Free. "Runs the same Flask server in a background thread and opens it in a native OS window instead of a browser tab, falling back to `webbrowser.open()` if `pywebview` isn't installed." 52 lines to turn a local web tool into a double-clickable desktop app — a genuinely cheap distribution path if this project ever wants a UI.

---

## D. Efficiency paths (cost / time / API budget / compute)

### D1. Audio-peak seeding as a free pre-filter before any paid call — **the core cost architecture**
**Grep:** `**Borrow the "loudness peaks seed candidate windows, then score each with cheap secondary signals" architecture wholesale**` (line ~212)
Quoting the rationale: "it's a sound way to avoid running expensive signals (transcript keyword scan, and especially any vision model) over the entire VOD; you only pay for them at the ~handful of candidate timestamps that already look interesting acoustically ... use RMS-peak-finding (cheap, no API calls) to generate candidate windows, then send only those windows' audio/frames to Gemini for understanding/verification, **instead of paying for full-VOD multimodal analysis**."
**How it helps:** This is the single highest-leverage cost decision in the entire document. For a 4-hour VOD, dense 1-fps analysis is 14,400 frames; audio-peak seeding reduces that to tens of windows. Order-of-magnitude(s) of API budget.

### D2. `cap.grab()` instead of `cap.read()` for skipped frames
**Grep:** `call `cap.grab()` (advances the decoder without the costly color-convert + numpy copy` (line ~549). Free CPU savings at 1-fps sampling over multi-hour video, zero accuracy cost.

### D3. Disk-cache expensive per-window analysis, keyed on `(video, start, end)`
**Grep:** `Results are cached to disk per `(video, start, end)` so re-runs are free.` (line ~187). The single most valuable habit for iterative tuning: re-running a pipeline after a threshold tweak should not re-pay for inference on windows already analyzed. Applies equally to Gemini calls. **Key on content, not filename** (see B4).

### D4. Sparse frame sampling budgets, with real numbers
- FER: `max_samples: 8`, `sample_rate: 2.5s` — "a 30-second window only ever gets ~8 real inference calls, not a dense per-frame scan" (line ~185).
- Auto-clipper CV: `SAMPLE_INTERVAL = 1.0` (1 fps) (line ~547).
- LLM vision: one frame every **8s** (line ~696).
**How it helps:** Three tiers of sampling density matched to three tiers of per-call cost. Pattern: the more expensive the analyzer, the sparser the sampling — and only *after* a cheaper stage has narrowed the candidates.

### D5. ffmpeg `astats` instead of librosa/scipy/numpy for audio
**Grep:** `This is a strictly lighter dependency footprint` (line ~896). Removes three heavy Python dependencies from the critical path. In Colab, dependency install time is real wall-clock cost on every session start.

### D6. Super-linearly growing search batches for rare-event scanning
**Grep:** `batch_period = (batch_period + 3) * 2` (line ~314)
Expands 1s → 8s → 22s → 50s... "so segments with an early face are cheap to resolve and only segments with a late/rare face pay for a wider scan."
**How it helps:** A general search strategy: start cheap, escalate only for the hard cases. Applies to any "find the first frame satisfying X" scan we write.

### D7. Dynamic batch sizing from actual free memory + explicit GPU cleanup
**Grep:** `pytorch.get_free_cpu_memory()` (line ~332) and `cleanup()` explicitly deletes the MTCNN model object and calls `torch.cuda.empty_cache()` (line ~334)
"A real memory-safety technique for processing arbitrarily long VODs without OOMing" — and ClipsAI "takes GPU memory hygiene seriously enough to make it a public API method."
**How it helps:** Directly relevant to Colab, where OOM kills the whole session and loses all intermediate state. Both patterns are cheap to adopt.

### D8. `fer`/MTCNN as a **free stage-1 pre-filter**, not a Gemini competitor
**Grep:** `corrected 2026-07-30, same too-quick-to-discard mistake as elsewhere in this research` (line ~1214)
See C3 for the full quote. The architectural point: high-facial-expressivity windows get flagged for free, locally, *before* any paid call, "which directly serves the funnel's whole point (spend LLM budget only on windows that already look promising)."

### D9. `concurrent_fragment_downloads=16` — 4× faster VOD download
**Grep:** `concurrent_fragment_downloads=16` (line ~1096)
Verbatim from the source: "Twitch HLS has 4-10s fragments; pulling 16 at a time saturates home broadband and cuts 1h-VOD downloads from ~8 min to ~2 min."
**How it helps:** One yt-dlp option, ~4× on the slowest non-API step. For a 4-hour VOD this is roughly half an hour of wall clock per run.

### D10. Cache transcripts to disk
**Grep:** `Transcripts are cached to `{audio_stem}_words.json`` (line ~412). Transcription is the most expensive *local* step. Cache it, key on content hash (B4). Every downstream signal (verbal triggers, TextTiling boundaries, keyword scanning, captions) reads from the same cached artifact — one transcription pass funds four signals.

### D11. `vad_filter=True` to skip silence during transcription
**Grep:** `with `vad_filter=True` to skip silence for speed` (line ~909) and the docstring quote `great for VODs with long silences/quiet gameplay` (line ~409). Twitch VODs have enormous dead-air fractions. See B3.

### D12. Single-pass `filter_complex` instead of N+1 ffmpeg subprocesses
**Grep:** `is a strict efficiency improvement over what ClipsAI itself does` (line ~464). See B8. "One ffmpeg process with no intermediate files" vs. "N+1 ffmpeg subprocess invocations plus N temporary files on disk." Also avoid `-ss` after `-i` for coarse seeking, which "decodes from the start of the file up to the seek point every time."

### D13. Verbal clip triggers = a signal with literally zero marginal cost
**Grep:** `verbal clip triggers are a free, zero-inference-cost signal once we're transcribing anyway` (line ~936). If the transcript already exists (D10), a regex over it costs microseconds and may be the highest-precision signal available.

### D14. TextTiling's recursion terminator
**Grep:** `looping while `len(clip_embeddings) > 8`` (line ~53). Bounds the multi-resolution sweep's cost — stop recursing once you're down to 8 segments. Prevents unbounded re-segmentation work on long inputs.

### D15. Chunked processing of long VODs
**Grep:** `Long VODs (>30 min) are processed in overlapping 15-minute chunks with 30s overlap` (line ~205). Bounds peak memory, enables progress checkpointing and partial-result recovery after a crash — important in Colab where sessions die.

### D16. Backend auto-detection so the same code runs fast on any hardware
**Grep:** `a real, reusable pattern for a transcription module that has to work across heterogeneous end-user hardware` (line ~418). See A27. Avoids the two failure modes of either forcing a CUDA-only stack or defaulting everyone to slow CPU.

### D17. Circuit-break on consecutive API failures
**Grep:** `aborts early after 5 *consecutive* failures` (line ~710). Budget protection: stops a dead key or outage from "silently producing zero highlights after burning the whole budget."

### D18. JPEG quality 60 + `max_tokens: 150` for vision calls
**Grep:** `cv2.IMWRITE_JPEG_QUALITY, 60` (line ~697) and `"max_tokens": 150` (line ~731). Both are direct token-cost levers: image tokens scale with resolution/quality, and capping output tokens at 150 forces a terse scored verdict rather than an essay.

### D19. Always keep a model-optional degradation path
**Grep:** `Keep the **pixel-only fallback pattern** as a design principle` (line ~593) and `yolo_local` degrades gracefully to `arc_cv_pipeline` (line ~826)
"Always have a cheap, model-optional signal path ... so the pipeline degrades gracefully instead of hard-failing when a heavier model call is unavailable/**rate-limited/too expensive for a given run**." Confirmed to operate at both the detector level and the orchestration level.
**How it helps:** Given documented budget constraints, "too expensive for this run" is a real runtime state, and the pipeline should have a defined free-only mode rather than failing.

### D20. Write the cluster/pad/clamp builder **once**
**Grep:** `our own implementation should write this once, shared, rather than reproduce this repo's own duplication` (line ~1165). Auto-clipper hand-duplicated this skeleton across 8–9 files, and separately duplicated the ffmpeg `astats` command 3× and the menu-suppression guard 2×. The `video_utils.py` docstring (E17) is that repo's own evidence of what duplication costs. Pure engineering-time savings.

---

## E. Material corrections, caveats, gotchas, and justified numbers

### E1. ClipsAI's clip-finding uses **only** transcript semantics — no audio, no chat, no speaker change
**Grep:** `**pure topic/semantic-shift detection on the transcript — nothing else**` (line ~20) and `**No diarization in clip-finding.**` (line ~59)
The doc explicitly corrects a common misreading: pyannote diarization exists in the library but "is never imported by `clipfinder.py` or `texttiler.py`. Speaker change is not a signal in the boundary-finding step at all — this is worth being precise about, since the one-line description ('speaker diarization... finds story breaks') **conflates two separate subsystems that don't share a signal**."
**Why it matters:** Prevents us from selecting ClipsAI expecting a multi-signal detector. It finds *edges*, not *moments* — "the only one of the three techniques that's about clip *edges* rather than clip *existence*."

### E2. ClipsAI has **no CLI entry point at all**
**Grep:** `**CLI entry points: there are none.**` (line ~380). `setup.py` defines no `console_scripts`/`entry_points`; the only runnable things are three Jupyter notebooks under `sandbox/`. It is a pure importable library. Plan to import it, not shell out to it.

### E3. TextTiling silently depends on a fragile NLTK↔WhisperX character resync
**Grep:** `This is a real, non-obvious dependency` (line ~372)
"TextTiling's sentence-level boundaries only work because this NLTK-tokenize-then-realign step successfully keeps NLTK's sentence splits in sync with WhisperX's raw character timings — **an unusual transcript (heavy non-English punctuation, unusual quote glyphs) is a plausible real failure point**," and the fuzzy search raises a hard `TranscriptionError` if a ±3-character window doesn't resolve it.
**Why it matters:** Twitch speech transcripts are full of exactly the pathological content that breaks sentence tokenizers — emote names, gamer tags, stutters, all-caps shouting, no punctuation. If we port TextTiling, this is the first place it will break, and it fails **loudly with an exception**, not gracefully.

### E4. ClipsAI hard-allow-lists only 10 languages
**Grep:** `hard-allow-lists only 10 languages (en, fr, de, es, it, ja, zh, nl, uk, pt)` (line ~376). A ClipsAI-specific config-validation limitation layered on top of Whisper, "which itself supports far more languages." Not a blocker for English content, but a real constraint on the library.

### E5. Real measured diarization performance
**Grep:** `~2.5% real-time factor on one Nvidia V100 + one Intel Cascade Lake CPU — i.e., about 1.5 minutes to diarize a 1-hour recording` (line ~345). Sourced from the file's own header comments.
**Why it matters:** Concrete planning number. Diarizing a 4-hour VOD ≈ 6 minutes on a V100. That is cheap enough to not rule out on performance grounds — the real friction is the HuggingFace token gate (C18).

### E6. ClipsAI's own config layer accepts clips up to **900 seconds (15 minutes)**
**Grep:** `max_clip_duration` up to **900 seconds (15 minutes)** (line ~478). From `test_clip.py`'s valid-config fixture (`min_clip_duration: 15, max_clip_duration: 900` passes validation). Context for the `k=[37,53,73,97]` "10+ minute clip" bucket. Also: `test_clip.py` and `test_resize.py` are "genuine regression tests with real expected values, not placeholder/smoke tests, so they're a trustworthy secondary confirmation source for the algorithms documented above" — including concrete cases like 1920×1080 → 607×1080 for a 9:16 target.

### E7. twitch-clip-miner's candidate window is fixed-width, not event-length-derived
**Grep:** `note the window is **not** derived from how long the loud moment actually lasts, it's always a fixed-width window centered on the peak` (line ~154). A known weakness: a 3-second laugh and a 45-second escalating meltdown produce identical 30s windows. Auto-clipper's clusterer (A7) solves this properly by grouping *runs* of hot frames.

### E8. Raw chat message count is a weak proxy — the critique survives both implementations
**Grep:** `a single person spamming inflates raw counts identically to a genuine chat explosion` (line ~231), restated at line ~874 for the GQL implementation.
The doc's recommended v1 upgrade: "normalize by a **rolling baseline chat rate** (this streamer's chat is fast or slow in general) rather than a single global z-score, and would consider **unique-chatter count or emote-spam detection**, not just message count."
**Why it matters:** Both independent implementations found in this research make the same mistake. For @LacyCrashOuts specifically, a rolling baseline matters because chat rate varies enormously between early-stream and peak-viewership hours within one VOD.

### E9. The concrete failure mode to avoid when porting LLM-vision detection
**Grep:** `sent **one frame per HTTP request** — there is no multi-image batching and no video-native upload` (line ~698), and the synthesis at line ~1153
"This is meaningfully more expensive per-analyzed-second than a true video-understanding call would be, and it means **the model never sees temporal context across frames, only the single still**." Restated: "it also shows the concrete failure mode to avoid: per-frame-only calls with no temporal/video context and no batching. If Gemini's native video understanding (multi-frame or true video input) is available to us, it should be used instead of naively porting this file's one-request-per-frame approach, **which is the weakest part of an otherwise well-built detector**."
**Why it matters:** Both a cost finding and an accuracy finding. A still frame cannot show a *reaction* — reactions are temporal. This is the specific thing to get right in our stage-2 design.

### E10. The "probe `/models`, pick from a ranked candidate list, degrade gracefully" pattern
**Grep:** `**Dynamic model selection.**` (line ~686)
`GET https://api.x.ai/v1/models` at init, pick the first available from a hardcoded **cheapest-first** priority list: `grok-4-1-fast-non-reasoning`, `grok-4-1-fast-reasoning`, `grok-4.20-beta-0309-non-reasoning`, `grok-4.20-beta-0309-reasoning`, `grok-2-vision-latest`, `grok-2-vision-1212` → fall back to any model with `"vision"` in its name → then any `"fast"` + `"non-reasoning"` model → then a hardcoded string if the endpoint call fails.
**Why it matters:** "Worth copying regardless of vendor — it's a real defense against a hardcoded model ID going stale." This is a directly relevant lesson: the sister project's recent commit history includes "Add real model discovery + expand pre-flight validation to image/TTS models," i.e. we already learned this lesson the hard way. Note the ordering principle: **cheapest-first**, not best-first.

### E11. **Major structural correction:** Auto-clipper has 13 peer detection strategies; `arc_clip_detector.py` is one of them
**Grep:** `The single biggest correction to the prior write-up` (line ~675)
"**Neither `arc_clip_detector.py` nor `hybrid_detector.py` is 'the' pipeline**" — `app.py` exposes 13 independent, mutually-exclusive strategies behind one dropdown. The full list, confirmed by grepping `templates/index.html`: `arc_cv_pipeline` (labelled "Auto-Clipper CV — HUD + VFX analysis (recommended)", and marked `selected` as the **UI default**), `audio_cv`, `clip_triggers`, `audio_only`, `cv_only`, `motion`, `scene_change`, `hybrid`, `chat_spikes`, `ai_vision`, `roboflow_workflow`, `roboflow_model`, `yolo_local`. The complete import→method mapping is quoted verbatim at line ~761.
**Also:** "**`hybrid_detector.py` does not call `arc_clip_detector.py`, `chat_detector.py`, `ai_analyzer.py`, or any other detector module — none of these files import each other.**" Every detector is a standalone class with its own `analyze_video(video_path, progress_callback)` contract.
**Note the default discrepancy:** `arc_cv_pipeline` is the **UI** default; `audio_cv` is only the **code's** fallback when the value is missing/unrecognized.
**Why it matters:** Corrects the mental model of the repo entirely. Also gives us a clean interface contract to copy — `analyze_video(video_path, progress_callback)` — and the observation that the author's UI default reveals which detector he trusts most.

### E12. The "hybrid" naming collision
**Grep:** `**A genuinely confusing naming collision worth flagging explicitly:**` (line ~783)
`detection_method="hybrid"` → `HybridDetector` fuses **audio + motion + scene-histogram**. But `arc_clip_detector.py` has its own `ClipMode.HYBRID` meaning **CV pixel-analysis + YOLO** fused *inside* the `arc_cv_pipeline` option. "A user picking 'Hybrid — all signals combined' from the UI dropdown is not getting YOLO or pixel-HUD-analysis at all." Naming lesson for our own config vocabulary.

### E13. Auto-clipper's scope is 31 games, not one — plus user-definable profiles
**Grep:** `**31** complete per-game detection profiles` (line ~1024)
Full list given in the doc (Arc Raiders, War Thunder, Fortnite, Apex Legends, Valorant, Call of Duty, League of Legends, Counter-Strike, Minecraft, GTA V, Overwatch, Rocket League, Dead by Daylight, Escape from Tarkov, PUBG, Elden Ring, Rainbow Six Siege, Rust, The Finals, Marvel Rivals, Fall Guys, Lethal Company, Among Us, Path of Exile, Warframe, Halo Infinite, Palworld, Monster Hunter World, Deadlock, Sea of Thieves, Hunt: Showdown, Genshin Impact, Final Fantasy XIV, Naraka Bladepoint), each with HSV detector regions, audio/motion/brightness thresholds, **and a full bespoke Grok system prompt** for that game. `get_profile()` supports user-defined profiles from a `custom_profiles.json` merged over the `arc_raiders` defaults so unset keys still work, editable via the UI at `/api/custom-profiles`.
**Why it matters:** If @LacyCrashOuts plays any of those 31 titles, there is an existing tuned profile *and an existing LLM prompt* for it. The merge-over-defaults pattern for custom profiles is directly worth copying — per-streamer profiles that only override what differs.

### E14. "13 classes" vs "19" — and 3 classes that are pure YOLO artifacts
**Grep:** `13 shipped entity classes` (line ~516)
Active shipped classes: `raider, raider-down, rocketeer, bastion, leaper, bombardier, hornet, wasp, snitch, pop, fireball, probe, turret`. The scoring table additionally knows `queen`, `sentinel`, `tick` (not output by the shipped model) **plus 3 inert HUD-digit-artifact classes (`"0"`, `"1"`, `"5"`) that show up as YOLO false-positive labels in the raw dataset and are explicitly zeroed out**.
**Why it matters:** The HUD-digit false-positive classes are a real, non-obvious gotcha of training an object detector on gameplay footage — the model learns HUD numerals as objects. Explicitly zeroing them in the scoring table is the pragmatic fix.

### E15. There are **two different** Arc Raiders YOLO models in one repo
**Grep:** `meaning there are at least two distinct Arc-Raiders-tuned YOLO models referenced across this repo` (line ~1012). One shipped as local `models/best.pt`, one hosted on Roboflow as `"arc-raiders-05arl-bgcvo/1"`. A provenance caveat if anyone ever tries to reproduce that repo's results.

### E16. The cluster/pad/clamp skeleton was independently reinvented **8–9 times in one repo**
**Grep:** `this repo converged on that *exact same* skeleton independently, at least 8 separate times` (line ~1159)
Named files: `ai_analyzer.py`, `audio_detector.py`, `chat_detector.py`, `detector.py`, `hybrid_detector.py`, `motion_detector.py`, `scene_detector.py`, `roboflow_analyzer.py`, `roboflow_model_analyzer.py` — the same `duration = max(min_dur, min(max_dur, duration + extension))` idiom hand-duplicated in each.
**Why it matters:** The doc's read: "That's **stronger** evidence for the pattern than a single well-built file, not weaker." Nine independent implementations converging on one shape is the strongest architectural validation in the whole document — it's why A7 is the recommended skeleton. (And why D20 matters: write it once.)

### E17. OpenCV `CAP_PROP_FPS` returns NaN, and the obvious guard is broken
**Grep:** `# analysis/video_utils.py` docstring (line ~1059), quoted verbatim in the doc:
> "Extracted after the review caught 7+ copies of the NaN-safe fps guard drifting apart (two files used `math.isnan`, five used `fps != fps`, one used `or 30.0` which misses NaN entirely)."

The doc's expansion: "`fps or 30.0` doesn't catch NaN, since `NaN or 30.0` evaluates to `NaN`."
**Why it matters:** This is a specific, subtle, silently-wrong-output bug we would otherwise write ourselves. `cap.get(cv2.CAP_PROP_FPS)` returns NaN on some codec/container combinations — plausible for Twitch VOD containers. Use `fps != fps` or `math.isnan`, never `or`.

### E18. Auto-clipper's default branch is itself a Claude Code output
**Grep:** `default branch is `claude/twitch-clip-analyzer-MPT08`, not `main`` (line ~503)
"This repo appears to itself be a Claude Code output/branch, not a hand-written project, which is worth flagging given the source." Reinforced at line ~1073: the `video_utils.py` consolidation is "evidence this repo has gone through at least one real self-correction pass, consistent with the repo's default branch itself being a Claude Code output."
**Why it matters:** Provenance caveat on every finding sourced from that repo. It's still real, running code with real ffmpeg calls and real API integrations — but its design decisions carry less independent authority than a human-maintained project with users would. Weigh it accordingly. (The counterpoint: E16's ninefold convergence is meaningful *regardless* of authorship.)

### E19. Menu suppression must override a loud audio signal, not merely penalize it
**Grep:** `and this override happens **even when audio is loud**` (line ~955). See A25. The gotcha is the *precedence*: a score-penalty implementation would still let a loud enough moment through. It has to be a hard gate.

### E20. "Clip that" is said *after* the moment — the window must extend backward
**Grep:** `**`clip_duration` seconds *before* the trigger**, not after` (line ~923). "Correctly modeling how 'clip that' is actually used live (reacting after the exciting thing already happened)." Easy to get backwards; the doc records the right answer.

### E21. The document's own meta-finding: first passes systematically under-read
**Grep:** `This section answers "did you actually read every file" honestly` (line ~282) and `The prior Repo 3 pass read 4 of bendawg2010/Auto-clipper's 69 files` (line ~660)
Recorded coverage: ClipsAI first pass read **4 of 93 files**; twitch-clip-miner **8 of 24**; Auto-clipper **4 of 69**. The Auto-clipper audit pass then read 16 files / ~10,900 lines and produced E11, E13, and the entire `ai_analyzer.py` finding. The Repo-3 note is explicit: "The user pushed back that this was surface-level and asked directly whether every line/word had actually been read — it had not."
**Why it matters:** The largest single correction in the file (E11 — that the documented "pipeline" was actually one of 13 peer options) came only from the audit pass. This is the exact failure mode named in the task brief, documented in-place with numbers. **Any future work sourced from this document should read the audit-pass sections, not just the three "Repo N" sections.**

### E22. Explicitly listed as *not* read, with justification
**Grep:** `Remaining unread files` (line ~491) — ClipsAI: `filesys/*.py`, the rest of `media/*.py`, `utils/*.py`, `clip/exceptions.py` and siblings, 4 other test files, `sandbox/*.ipynb`. **Grep:** `Test files, CHANGELOG/CONTRIBUTING, install scripts, and `models/README.txt` were skipped` (line ~671) — Auto-clipper; `templates/index.html` was grep-spot-checked only, not fully read.
**Why it matters:** Tells a future reader exactly where the remaining unmined surface is, so nobody re-derives what's already covered or assumes coverage that doesn't exist.

### E23. Auto-clipper is a full Flask product, not a script — with features worth knowing exist
**Grep:** `The original pass didn't establish that this repo is a Flask web app at all.` (line ~1125)
`app.py` (2339 lines), ~50 REST routes, **10 GB max upload**. Features documented: custom game profiles built through a form; a **watch-folder mode** that auto-analyzes new VODs dropped into a directory (`_watch_folder_loop`, polling every **5s**); stitching selected clips into one highlight reel via an ffmpeg concat filter with selectable resolution/quality; **near-duplicate clip detection by >50% time-range overlap**; sort/filter by confidence/duration/time or tag/review-status; export presets and usage analytics in local JSON; manual arbitrary-timestamp cutting (`/api/manual-clip`). `clip_manager.py` (1501 lines) also implements `split_clip`, `extend_clip`, `merge_clips` (configurable transitions), `add_captions`, `add_zoom_pan`, `add_sound_effect`, `add_watermark`, `batch_tiktok` — "all real ffmpeg-subprocess implementations."
**Why it matters:** "It's a small SaaS-shaped product wrapped around the 13 detectors." If we need any post-production operation (captions, zoom/pan, SFX, reel stitching), there is a real working ffmpeg implementation to read rather than derive. The **>50% time-range overlap** near-duplicate rule is a concrete reusable heuristic. The watch-folder pattern is directly applicable to an automated bot that should process new @LacyCrashOuts VODs unattended.

### E24. `detect_volume_spikes()` — within-clip spike markers, a distinct use case
**Grep:** `**`detect_volume_spikes()`**` (line ~1114). A general-purpose version of the `astats` extraction exposed as its own endpoint "for spike markers *within* an already-cut clip (e.g. for **caption/SFX timing**), not for whole-VOD highlight detection." Same technique, different pipeline stage — useful downstream if we auto-place captions or sound effects.

### E25. `GameDetector` is not `ArcClipDetectorAdapter` — and carries a backwards-compat alias revealing its history
**Grep:** `**not** `ArcClipDetectorAdapter`` (line ~944). `GameDetector` (`detector.py`, the `audio_cv` option and the code-level fallback default) is "a purely declarative, per-game HSV-color-threshold system driven entirely by `game_profiles.py`'s `"detectors"` dict (`kill_feed`, `damage`, `hit_marker`, `explosion`, `special`, each with a `region`, HSV `lower`/`upper` bounds, a `weight`, and a `multiplier`) — there is no YOLO, no PixelAnalyzer, no bundled model weights involved at all." It carries the alias `ArcRaidersDetector = GameDetector`, "confirming it used to be Arc-Raiders-specific before being generalized to the 31-game profile system."
**Why it matters:** The declarative-detectors-as-config shape (region + HSV bounds + weight + multiplier) is a clean data model for any rule-based visual signal, entirely independent of the game. Also confirms the generalization path this codebase actually took: one game hardcoded → config-driven → 31 games.

### E26. `PixelAnalyzer`'s HSV thresholds were hand-measured from 762 annotated frames
**Grep:** `literally measured pixel-by-pixel from 762 annotated frames of the dataset` (line ~536)
Regions measured: health-bar white-pixel fraction, blue teammate-status bars, red damage vignette on screen edges, orange/yellow fire-color detection, death-screen brightness/saturation thresholds, inventory-screen detection.
**Why it matters:** A real effort estimate for hand-tuned HUD detection (762 annotated frames of manual measurement), and it "works **even with zero YOLO model present** — a genuine no-ML fallback path." That effort number is what makes the LLM-vision approach attractive by comparison: no per-game annotation labor at all.

### E27. `MotionDetector` / `SceneChangeDetector` / `HybridDetector` are the same math, three times
**Grep:** `These three are structurally the same file duplicated with different subsets of signals` (line ~968)
Underlying math named explicitly: **frame-diff mean for motion**, **`cv2.compareHist` correlation + chi-square for scene change**, **brightness-delta "flash" detection** for both. "None of the three imports either of the other two; each recomputes its slice of the same formulas from scratch."
**Why it matters:** Three cheap, free, no-ML frame signals with the exact OpenCV functions named. Brightness-delta flash detection is a notably good fit for gaming/reaction content (explosions, jumpscares, alert overlays).

### E28. The bottom-line recommendation, and what the audit passes did and didn't change
**Grep:** `**Bottom line recommendation:**` (line ~1225)
Verbatim: "build the v1 moment-detector as Auto-clipper's cluster/pad skeleton, driven by a Gemini-video-understanding score per sampled window (replacing YOLO) with cheap audio-RMS peak-finding (from twitch-clip-miner) as a free pre-filter to cut down how many windows we pay Gemini to look at, chat velocity added as a second cheap signal once we have a chat-log source wired up, and every clip's final start/end snapped to the nearest ClipsAI-style transcript topic boundary so clips read as complete thoughts instead of arbitrary windows."
**Grep:** `This does **not** overturn the existing "Bottom line recommendation"` (line ~1180)
The audit pass's own verdict on what changed: it reinforces the cluster/pad skeleton choice (E16), **adds the per-frame-vs-video-native caveat** to the Gemini piece (E9), and adds **two new additive ideas** — the sensitivity-slider + override-dict control surface (A15/A17) and the agreement-bonus fusion shape (A18). Separately, the 2026-07-30 correction (D8/C3) changes the `fer`/MTCNN disposition from "drop it" to "use it as a free stage-1 pre-filter."
**Also revised since the original synthesis:** chat fetching should use the direct GQL persisted-query approach (A11/C2), **not** the `TwitchDownloaderCLI` dependency originally recommended.

---

## Items with genuinely nothing new

- `src/utils.py` (B10) — a 4-line empty stub; recorded only so it isn't re-investigated.
- `analysis/__init__.py` — noted as empty in the audit pass file list.
- `AudioDetector` as a standalone class — "nothing new architecturally, just confirmation the pattern is used consistently across all ~8 CV/audio detector classes" (line ~899). The confirmation itself is the value (E16); the class adds nothing beyond A13 + A7.
- The Roboflow analyzers' highlight builders — "again independently reimplemented, not shared" into the same 3-second-bucket → threshold → merge-gap → clamp pipeline. Nothing new beyond A7.
