# Deep dive: how three real repos actually decide "this is the moment"

Read directly from source via `gh api repos/<owner>/<repo>/contents/...` (not READMEs, not
descriptions) on 2026-07-29. This supplements `research/verified_tools_catalog.md` — that file
says a repo is real and what it claims to do; this file explains *how the code actually works*,
with real function names and short verbatim excerpts, for the three repos most relevant to the
core open question: how do you programmatically decide a moment is worth clipping.

---

## Repo 1 — ClipsAI/clipsai

- **Stars:** 522 (as of 2026-07-29)
- **Link:** https://github.com/ClipsAI/clipsai
- **Files read in full:** `clipsai/clip/clipfinder.py`, `clipsai/clip/texttiler.py`,
  `clipsai/clip/clip.py`, `clipsai/clip/text_embedder.py`, `README.md`

### Real technique

ClipsAI's clip-boundary detection is **pure topic/semantic-shift detection on the transcript —
nothing else**. It does not use pause length, speaker changes, audio energy, or chat. Concretely:

1. **Transcribe first.** WhisperX produces word-level timestamps; `Transcription.get_sentence_info()`
   groups words into sentences.
2. **Embed every sentence** with `TextEmbedder.embed_sentences()`, which is just
   `SentenceTransformer("all-roberta-large-v1").encode(sentences)` — a generic sentence-embedding
   model, not a custom-trained one.
3. **Run the TextTiling algorithm** (`clipsai/clip/texttiler.py`, `TextTiler.text_tile()`) —
   this is a 1997 NLP algorithm (Hearst, "TextTiling: Segmenting Text into Multi-Paragraph
   Subtopic Passages") ClipsAI adapted to run on sentence embeddings instead of word-frequency
   vectors (citing a 2021 paper on BERT-based TextTiling). The steps, in
   `TextTiler.text_tile()`:
   - **Gap scores** (`_calc_gap_scores`): slide a window of size `k` sentence-embeddings on each
     side of every adjacent-sentence "gap," pool each side (mean or max), and compute cosine
     similarity between the two pooled window embeddings. Low similarity = topic likely changed
     across that gap.
   - **Smoothing** (`_smooth_scores`): a moving-average smoother (SciPy Cookbook `smooth()`,
     copied verbatim into the file) removes micro-noise from the gap-score curve.
   - **Depth scores** (`_calc_depth_scores`): for every gap, walk left and right until the curve
     stops rising to find the nearest local peaks on both sides, then
     `depth = (left_peak - gap_score) + (right_peak - gap_score)`. This is the classic
     TextTiling "valley depth" — a gap that's a deep local dip between two similarity peaks is a
     strong boundary candidate, even if its absolute similarity isn't the lowest in the video.
   - **Boundary decision** (`_identify_boundaries`): compute `cutoff = mean(depth) + stdev(depth)`
     (for the default `cutoff_policy="high"`; `"average"` and `"low"` are also selectable). A
     gap becomes a boundary only if its depth score exceeds the cutoff **and** exceeds both
     neighboring depth scores (true local maximum, not just above threshold) — this is what
     prevents doubled-up boundaries at the same topic shift.
4. **Multi-resolution passes with different `k`:** `ClipFinder.find_clips()` doesn't run TextTiling
   once. It runs it repeatedly with increasing window sizes — `k = [5, 7]` for candidate clips
   under 3 minutes, `k = [11, 17]` for 3+ minute clips, `k = [37, 53, 73, 97]` for 10+ minute
   clips — recursively re-segmenting the *already-merged* super-clips from the previous round each
   time (`_text_tile_multiple_rounds`, looping while `len(clip_embeddings) > 8`). A bigger `k`
   means each embedding windowspans more sentences, so bigger `k` finds coarser (longer,
   higher-level) topic boundaries, smaller `k` finds finer ones. Every round's surviving segments
   are deduplicated against already-chosen clips (`_is_duplicate`: two clips are the same if the
   sum of their start-time and end-time deltas is under 15 seconds) and filtered to the
   `min_clip_duration`/`max_clip_duration` window for that pass.
5. **No diarization in clip-finding.** Pyannote speaker diarization exists in the library
   (`clipsai/diarize/pyannote.py`) but per the README it is used *only* for the separate
   `resize()` function that reframes 16:9 video to 9:16 by dynamically cropping to whichever
   speaker is currently talking. It is never imported by `clipfinder.py` or `texttiler.py`. Speaker
   change is not a signal in the boundary-finding step at all — this is worth being precise about,
   since the one-line description ("speaker diarization... finds story breaks") conflates two
   separate subsystems that don't share a signal.

### Concrete reusable pattern for our project

**Port the TextTiling-on-embeddings idea directly** — it's the single most transferable piece of
real, working, licensed-permissively (MIT) code found across all three repos, and it solves a
different (complementary) problem than YOLO/audio/chat scoring: those tell you *when something
exciting happened*; TextTiling tells you *where a coherent, self-contained narrative segment
begins and ends* so a clip doesn't start or end mid-thought. For Twitch VODs specifically:
- Use it as a **boundary snapper**, not a standalone clip-finder: run our excitement-scoring signal
  (audio/chat/vision, however we build it) to find candidate moments, then snap the clip's start/end
  to the nearest TextTiling boundary from the transcript so clips don't cut off a sentence or a
  punchline setup.
- The multi-resolution `k`-value sweep is a good default even in isolation — reuse the same
  tiered `k` schedule (small k for short reaction clips, large k for long-form segment discovery)
  rather than inventing our own.
- `all-roberta-large-v1` via `sentence-transformers` is a heavyweight embedding model; a smaller/
  faster embedding model (or reusing Gemini's own text-embedding endpoint, since we're already a
  Gemini-native project) is a reasonable substitution without changing the algorithm.

### Code excerpts worth keeping verbatim

The depth-score computation — this is the actual mathematical core of "how do you decide a story
break exists," and it's compact enough to port directly:

```python
# clipsai/clip/texttiler.py — TextTiler._calc_depth_scores
for gap in range(num_gaps):
    gap_score = gap_scores[gap]
    # find left peak by iterating backward through gap scores
    left_peak = gap_score
    for i in range(gap, -1, -1):
        if gap_scores[i] >= left_peak:
            left_peak = gap_scores[i]
        else:
            break
    # find right peak by iterating forward through gap scores
    right_peak = gap_score
    for i in range(gap, len(gap_scores), 1):
        if gap_scores[i] >= right_peak:
            right_peak = gap_scores[i]
        else:
            break
    depth_score = (left_peak - gap_score) + (right_peak - gap_score)
    depth_scores[gap] = depth_score
```

The boundary cutoff — note the "must beat both neighbors" check, which is what keeps boundaries
sparse instead of firing on every dip above the mean:

```python
# clipsai/clip/texttiler.py — TextTiler._identify_boundaries
avg = torch.mean(depth_scores)
stdev = torch.std(depth_scores, unbiased=False)
cutoff = avg + stdev  # cutoff_policy == "high" (the default)

for i in range(len(depth_scores)):
    is_boundary = True
    if depth_scores[i] <= cutoff:
        is_boundary = False
    left_neighbor = depth_scores[max(0, i - 1)]
    right_neighbor = depth_scores[min(i + 1, len(depth_scores) - 1)]
    if depth_scores[i] < left_neighbor or depth_scores[i] < right_neighbor:
        is_boundary = False
```

---

## Repo 2 — jamesbaughnd/twitch-clip-miner

- **Stars:** 6 (as of 2026-07-29)
- **Link:** https://github.com/jamesbaughnd/twitch-clip-miner
- **Files read in full:** `main.py`, `src/detector.py`, `src/chat_parser.py`, `src/vision.py`,
  `src/audio.py`, `src/chunker.py`, `src/summarizer.py`, `config.yaml`

### Real technique

This is a genuine multi-signal weighted-fusion scorer, built around **audio loudness peaks as the
anchor signal**, with transcript/chat/visual score added on top of each peak-derived window — it
does not independently score every second of video on all four signals; it finds candidate windows
from audio first, then scores each candidate.

1. **Loudness peak-finding is the seed step** (`src/audio.py` + `detector._find_audio_peaks`).
   `librosa.feature.rms()` computes short-time RMS energy of a 16 kHz mono extraction of the VOD.
   The RMS curve is z-scored (`_normalize_signal`, zero-mean/unit-variance) then lightly Gaussian-
   smoothed (`gaussian_filter1d(sigma=1.0)`), and `scipy.signal.find_peaks()` finds local maxima
   using two config-driven controls: `peak_prominence` (0.6 std devs by default — how much a peak
   must stick out above its surrounding baseline) and `peak_distance` (1.0s minimum spacing). Each
   peak becomes a candidate clip window by padding `± clip_padding` seconds (default 15s) around
   the peak time (`_build_clip_windows`) — note the window is **not** derived from how long the loud
   moment actually lasts, it's always a fixed-width window centered on the peak.
2. **Transcript score** (`_compute_transcript_score`) is a config-driven keyword/regex-style scan:
   for every transcribed word falling inside the window, check substring membership against a
   configurable `hype_words` list (e.g. "let's go," "bro," "AHHHH" — +1.5 each) and a
   `laughter_patterns` list ("haha," "lol," "kek," "xd" — +1.0 each), plus a small bonus for raw
   speech density (words/second × 0.2). It's a hand-tuned lexicon, not a classifier or sentiment
   model.
3. **Chat velocity is real and does work end to end** — this directly answers whether it's a real
   implementation worth learning from: yes. `src/chat_parser.py` shells out to
   `TwitchDownloaderCLI.exe chatdownload` to pull the VOD's actual replay chat log as JSON
   (`content_offset_seconds` + message body per comment — this is the real per-message timestamp
   Twitch stores against the VOD, the same data Twitch's own web player uses to render chat replay).
   `compute_chat_velocity()` then does exactly what "chat velocity" means in practice: bucket
   message timestamps into fixed-width bins (`np.histogram`, default `bin_width=1.0s`) and use the
   **raw per-second message count** as the velocity signal — no dedup, no dedup-per-user, no
   sentiment or emote-specific counting. In `main.py` this raw count array is z-scored exactly like
   the loudness signal before being handed to the detector, so the two signals live on comparable
   scales. The per-window feature used for scoring (`_avg_chat_vel`) is simply the mean of that
   z-scored velocity inside the candidate window. **Caveat found in the code:** the lower-level
   `compute_chat_velocity(df, time_range=...)` function has a real bug in its optional-`time_range`
   branch — `t_max = df["time"].min() if time_range else df["time"].max()` uses `.min()` instead of
   `.max()` when a range is supplied, which would silently collapse the bin range to near-zero width.
   It happens not to fire in this codebase's own call sites (both `main.py` and `chunker.py` avoid
   passing `time_range` and slice the arrays by boolean mask instead), but it means this exact
   function is not safe to reuse verbatim without fixing that line first.
4. **Facial-emotion recognition is real, working code, but disabled by default and framed as
   optional.** `src/vision.py` wraps the `fer` PyPI package (a real, if old/unmaintained,
   FER2013-based CNN emotion classifier with either Haar-cascade or MTCNN face detection as a
   front end). It samples a handful of frames per window (`max_samples: 8`, one every
   `sample_rate: 2.5s` by default — so a 30-second window only ever gets ~8 real inference calls,
   not a dense per-frame scan), runs `detector.detect_emotions(frame)` per sampled frame, and scores
   the window as the mean of `happy + surprise` emotion intensity across evaluated frames (capped at
   1.0 per frame). Results are cached to disk per `(video, start, end)` so re-runs are free. This is
   not aspirational vaporware — it's a complete, defensively-coded (graceful `ImportError` fallback,
   `VISUAL_AVAILABLE` flag threaded through the whole pipeline, stderr-suppression around noisy
   OpenCV/FFmpeg logging) implementation. It is, however, gated off by default
   (`visual_enabled: false` in `config.yaml`) and its accuracy is bounded by how much a Twitch
   facecam is even in frame/well-lit — nothing in the code addresses "no facecam in this VOD," it
   just silently returns 0.0 for windows with no detected face.
5. **Combining the signals is a flat, un-normalized weighted sum**
   (`_score_candidate`/`detect_clips` in `src/detector.py`):
   `combined = w_loud*loudness + w_trans*trans_score + w_chat*chat_score + w_visual*visual_score`,
   with default weights `{loudness: 0.4, transcript: 0.6, chat: 0.4, visual: 0.4}` (they don't sum
   to 1.0 — the comment literally says "adjust so total roughly 1.0" and the shipped defaults
   don't). Loudness and chat are pre-normalized (z-scored) before this sum; transcript score is
   raw/unbounded; visual score is bounded 0–1. Mixing normalized and unnormalized channels in one
   linear sum is a real weakness — a big transcript-score outlier can dominate regardless of weight.
   Windows are kept if `combined >= min_score` (default 0.7), then de-duplicated with a simple
   greedy NMS (`_merge_clips`): sort by score descending, keep a window only if its start time isn't
   within `min_distance` (10s) of an already-kept window's start.
6. Long VODs (>30 min) are processed in overlapping 15-minute chunks with 30s overlap
   (`src/chunker.py`, `process_video_in_chunks`) — each chunk independently re-runs the whole
   detect_clips pipeline on chunk-local timestamps, results are shifted back to global VOD time,
   then merged/deduplicated with the same NMS logic across the whole VOD.

### Concrete reusable pattern for our project

- **Borrow the "loudness peaks seed candidate windows, then score each with cheap
  secondary signals" architecture wholesale** — it's a sound way to avoid running expensive
  signals (transcript keyword scan, and especially any vision model) over the entire VOD; you only
  pay for them at the ~handful of candidate timestamps that already look interesting acoustically.
  This is directly adaptable to a Gemini-native pipeline: use RMS-peak-finding (cheap, no API calls)
  to generate candidate windows, then send only those windows' audio/frames to Gemini for
  understanding/verification, instead of paying for full-VOD multimodal analysis.
  ClipsAI's TextTiling boundary output, from repo 1, is a natural additional gate here: it would
  come for free from the same transcript text this project already has.
- **Adapt, don't port, the chat-velocity implementation.** The download mechanism
  (TwitchDownloaderCLI → JSON → `content_offset_seconds`) is the correct and simplest real way to
  get chat replay data — reuse that tool and JSON schema directly rather than reinventing chat
  fetching. But raw per-second message count is a weak proxy; a real v1 upgrade would normalize by
  a rolling baseline chat rate (this streamer's chat is fast or slow in general) rather than a
  single global z-score, and would consider unique-chatter count or emote-spam detection, not just
  message count, since a single person spamming inflates raw counts identically to a genuine
  chat explosion. Fix the `time_range` `.min()`/`.max()` bug before reusing the function.
  For v1, given we don't currently have a chat-log source wired up, it's reasonable to skip this
  signal rather than build it from scratch — but if/when we do add Twitch chat, this project proves
  the "chat velocity = highlight signal" pattern is real and cheap to implement (a few dozen lines,
  no ML), so it should be a near-term addition rather than a deferred one.
- **Do not copy the un-normalized weighted-sum combiner.** If we fuse multiple signals, z-score (or
  min-max) every channel first, the way ClipsAI does for its own gap scores and the way this
  project only half-does (loudness/chat yes, transcript/visual no).
- The FER visual-engagement approach (sparse frame sampling + happy/surprise intensity + disk
  caching) is a reasonable pattern if we ever want a cheap non-LLM engagement signal, but given this
  project already plans to use Gemini's native video understanding (confirmed real), asking Gemini
  directly "is there a strong reaction on the facecam here" is likely both more accurate and less
  infrastructure than standing up `fer`/MTCNN/Haar cascade ourselves.

### Code excerpts worth keeping verbatim

The combination formula — the exact shape of "how 4 signals become 1 score," worth keeping as a
reference for what *not* to do about normalization, and a reasonable starting formula shape
otherwise:

```python
# src/detector.py — _score_candidate
combined = (
    det_cfg["weight_loudness"] * loudness_score
    + det_cfg["weight_transcript"] * trans_score
    + det_cfg.get("weight_chat", 0.0) * chat_score
    + det_cfg.get("weight_visual", 0.0) * visual_score
)
```

Chat velocity from raw Twitch chat replay JSON — this is the real, minimal working pattern for
turning a chat log into a time-series signal:

```python
# src/chat_parser.py — compute_chat_velocity
bins = np.arange(t_min, t_max + bin_width, bin_width)
counts, _ = np.histogram(df["time"], bins=bins)   # messages per second-bin
times = (bins[:-1] + bins[1:]) / 2
return times, counts.astype(float)
```

and the normalization step that actually makes it comparable to the other signals (done in
`main.py`, not inside the function above — worth noting as the "right" place to normalize):

```python
# main.py
if chat_vel_global is not None and chat_vel_global.std() > 0:
    chat_vel_global = (chat_vel_global - chat_vel_global.mean()) / chat_vel_global.std()
```

---

## Audit pass — additional files read [2026-07-29]

This section answers "did you actually read every file" honestly for Repos 1 and 2 above. The
original pass on ClipsAI read 4 of 93 files and the original pass on twitch-clip-miner read 8 of
24 — small enough in the second case that it was nearly complete, but ClipsAI's read was narrowly
scoped to clip-finding only and skipped two entire subsystems (`resize/`, `transcribe/`) plus
`diarize/pyannote.py`. Full file trees were pulled via `gh api .../git/trees/main?recursive=true`
and every non-test, non-vendored, non-doc file not already covered was read in full via
`gh api repos/<owner>/<repo>/contents/<path>?ref=main`.

### ClipsAI — the resize/reframe subsystem (previously unread entirely)

Files read in full: `clipsai/resize/resize.py`, `clipsai/resize/resizer.py` (1034 lines — the
largest file in the repo), `clipsai/resize/vid_proc.py`, `clipsai/resize/crops.py`,
`clipsai/resize/segment.py`, `clipsai/resize/rect.py`, `clipsai/resize/img_proc.py`,
`clipsai/diarize/pyannote.py`, `clipsai/transcribe/transcriber.py`,
`clipsai/transcribe/transcription.py` (partial — the sentence-building logic), `setup.py`,
`setup.cfg`. This is the code the original write-up correctly identified as existing but never
actually read ("Pyannote... is used only for the separate `resize()` function... It is never
imported by `clipfinder.py`").

**`resize()` (`clipsai/resize/resize.py`) is a genuinely separate three-stage pipeline** from
clip-finding: speaker diarization → scene detection → face-tracking crop calculation. It requires
a HuggingFace auth token for pyannote (a real external dependency/friction point the clip-finding
path doesn't have).

**How the crop position is actually chosen (`Resizer` class, `resizer.py`) — this is the concrete
"how do you reframe 16:9 to 9:16 without cutting off the speaker" answer the original write-up
didn't have**:
1. Speaker-diarization segments and scene-change timestamps are merged
   (`_merge_scene_change_and_speaker_segments`) so a crop segment never spans a hard cut.
2. For each segment, it searches for the first frame with a detected face, starting an eighth of
   the way into the segment (skipping likely-silent lead-in), using **MTCNN**
   (`facenet_pytorch.MTCNN`) for face detection. The search batch size grows
   super-linearly each iteration (`batch_period = (batch_period + 3) * 2` → 1s, 8s, 22s, 50s...)
   so segments with an early face are cheap to resolve and only segments with a late/rare face pay
   for a wider scan.
3. **Active-speaker selection when multiple faces are on screen is done via mouth movement, not
   just face size/position.** Face bounding boxes across sampled frames are clustered with
   **KMeans** (`sklearn.cluster.KMeans`, k = number of distinct faces seen) to group detections
   into per-person tracks, then **MediaPipe FaceMesh** computes a mouth-aspect-ratio (MAR) per
   frame per track (`avg_mouth_height / mouth_width` using specific landmark index sets for
   upper/lower inner lip), and the ROI is set to whichever tracked face's MAR **changes the most**
   across frames — i.e., whoever is actually talking, not just whoever is biggest/most-centered.
   If no mouth movement is detected for any track (e.g. everyone off-screen or static), it falls
   back to the face that appeared in the most sampled frames. If no face is found in a segment at
   all, the crop defaults to the center 50%×50% box of the frame.
4. `_merge_identical_segments` collapses adjacent segments whose crop x/y centers differ by less
   than 4% of the video's width/height (`max_position_difference_ratio = 0.04`) — prevents
   needless micro-jitter cuts in the vertical pan track when the camera/speaker position barely
   moved between segments.
5. Batch sizing for GPU/CPU face-detection passes is computed dynamically from actual available
   memory (`pytorch.get_free_cpu_memory()`, `torch.cuda`), not a fixed constant — a real
   memory-safety technique for processing arbitrarily long VODs without OOMing.
6. `cleanup()` explicitly deletes the MTCNN model object and calls `torch.cuda.empty_cache()` —
   the library takes GPU memory hygiene seriously enough to make it a public API method.

**Scene detection (`vid_proc.py`) uses PySceneDetect's `AdaptiveDetector`** (a real, maintained
third-party library, not custom code) with `min_scene_len` tied to `min_scene_duration * fps`.
Frame extraction (`extract_frames`) uses PyAV, seeking to the nearest keyframe then decoding
forward to the exact target PTS — real efficient random-access frame pulling, parallelized via
`ThreadPoolExecutor` for the post-decode numpy/downsample/grayscale step.

**Diarization (`diarize/pyannote.py`) uses the pretrained `pyannote/speaker-diarization-3.1`
pipeline** (HuggingFace-gated). The file's own header comments document a real measured
performance number worth keeping: **~2.5% real-time factor on one Nvidia V100 + one Intel Cascade
Lake CPU — i.e., about 1.5 minutes to diarize a 1-hour recording.** `_adjust_segments` resolves
speaker-overlap regions by cutting the *earlier* speaker's segment short at the next speaker's
start time (favors the incoming speaker in an overlap, doesn't produce overlapping segments), and
hard-drops any segment under `min_segment_duration` (default 1.5s) rather than merging it into a
neighbor — speakers who only ever get short segments can end up entirely absent, which is why
`_relabel_speakers` exists (to keep remaining speaker IDs contiguous after that filtering).

**Transcription (`transcribe/transcriber.py`) confirms the granularity the whole TextTiling
pipeline (Repo 1 above) actually runs on: character-level, not word-level.** WhisperX's alignment
step is called with `return_char_alignments=True`, and `Transcription._build_sentence_info()`
(in `transcription.py`) tokenizes the flattened transcript with **NLTK's `sent_tokenize()`**, then
walks the character-level alignment to assign each sentence a start/end time. Because NLTK's
sentence text can drift from the raw whisper character stream (whitespace/quote normalization),
there's an explicit fuzzy-recovery step, `_realign_char_idx_with_sentence`, that searches a small
±3-character window to resync when a straight index-walk falls out of alignment, raising a hard
error only if that narrow search also fails:

```python
# clipsai/transcribe/transcription.py — _realign_char_idx_with_sentence
for offset in range(1, search_window_size * 2):
    offset *= -1
    if char_info[char_idx + offset]["char"] == correct_char:
        return char_idx + offset
# realignment failed -> raise TranscriptionError
```

This is a real, non-obvious dependency: TextTiling's sentence-level boundaries (Repo 1's core
technique) only work because this NLTK-tokenize-then-realign step successfully keeps NLTK's
sentence splits in sync with WhisperX's raw character timings — an unusual transcript (heavy
non-English punctuation, unusual quote glyphs) is a plausible real failure point.
`TranscriberConfigManager` also hard-allow-lists only 10 languages (en, fr, de, es, it, ja, zh, nl,
uk, pt) at the config-validation layer — a real, ClipsAI-specific limitation layered on top of
Whisper, which itself supports far more languages.

**CLI entry points: there are none.** `setup.py` defines no `console_scripts`/`entry_points` at
all — ClipsAI is a pure importable library. The only runnable entry points in the whole repo are
three Jupyter notebooks under `sandbox/` (`clipsai.ipynb`, `resizer.ipynb`, `transcribe.ipynb`).
Directly answers the brief's question about CLI entry points: this repo doesn't have one.

### twitch-clip-miner — remaining files (`clipper.py`, `downloader.py`, two transcriber backends, `utils.py`)

The original pass read 8 of this repo's 24 files, all substantively load-bearing ones except the
actual render/export step and the ingestion/transcription backends. Reading the rest:

- **`src/downloader.py` (29 lines) is a thin, literal `yt-dlp` wrapper** — `format:
  'best[height<=1080]'`, hardcoded, no adaptive-quality selection. Confirms `yt-dlp` handles VOD
  ingestion for this project exactly as assumed elsewhere in this research. Has a standalone
  `__main__` CLI entry (`python src/downloader.py <url>`).
- **`src/clipper.py` is the actual ffmpeg export step**, previously only described conceptually
  via the NMS/dedup logic in `detector.py`. The crop technique here is a **naive centered 9:16
  crop with no face-tracking** — `crop=ih*9/16:ih,scale=1080:1920` — a direct contrast worth
  keeping against ClipsAI's dynamic mouth-movement-tracked crop documented above; this repo just
  centers on the input frame's height and scales, always. Adds fixed 0.5s fade-in/out on both
  video and audio. `get_video_duration()` has a real two-tier fallback worth reusing: try
  `ffprobe -show_entries format_duration` first, and if that raises, regex-parse the
  human-readable `Duration: HH:MM:SS.ff` line out of `ffmpeg -i`'s stderr instead — a robustness
  pattern for any pipeline that can't assume `ffprobe` is present/working. `clip_segments()`
  simply sorts by score descending and takes the top `max_clips` (no dedup here — that already
  happened upstream in `_merge_clips`), and drops any clip under 1.0s after clamping to video
  bounds.
- **`src/transcriber.py` uses faster-whisper (CTranslate2), with real GPU/CPU auto-detection**:
  `ctranslate2.get_cuda_device_count() > 0` picks `small`+`cuda`/`float16` vs. `base`+`cpu`/`int8`
  (the check also covers ROCm on AMD per the code's own comment). **Real inconsistency found**:
  the module docstring explicitly recommends `vad_filter=True` ("great for VODs with long
  silences/quiet gameplay") but the actual shipped call hardcodes `vad_filter=False` — documented
  behavior and actual default disagree. Transcripts are cached to `{audio_stem}_words.json` keyed
  only by filename stem with no content hash, so a same-named-but-different audio file with
  `force=False` would silently return a stale cached transcript.
- **`transcribe_audio_auto()` is a pluggable transcription-backend selector** driven by
  `config.yaml`'s `transcription.backend` (`auto`/`whisper-cpp`/faster-whisper). In `auto` mode it
  checks whether a whisper.cpp binary + ggml model file both exist on disk and prefers that
  (citing Vulkan GPU acceleration) over faster-whisper if so — a real, reusable pattern for a
  transcription module that has to work across heterogeneous end-user hardware without requiring
  a specific backend to be installed.
- **`src/transcriber_whisper_cpp.py` shells out to a `whisper-cli.exe` binary** with
  `--word-thold 0.01 --split-on-word --max-len 0 --best-of 5`. Two real bugs found: (1) its
  default `whisper_cli` path argument is hardcoded to the original author's personal machine path
  (`C:/Programming/Projects/Python/twitch-clipper/tools/whisper-cli.exe`) — harmless in practice
  because `transcribe_audio_auto()` always overrides it with a config-relative path, but calling
  this function directly with defaults silently fails on any other machine; (2) it calls
  `subprocess.run(cmd, shell=True, check=False)` **without** `capture_output=True`, meaning
  `proc.stderr`/`proc.stdout` are always `None`, so its own error-logging path
  (`logger.error(proc.stderr[-1000:])`) would itself raise `TypeError: 'NoneType' object is not
  subscriptable` if `whisper-cli.exe` ever actually failed — the failure-handling code is broken
  and would mask the real error with a crash. Output parsing does defensively handle two different
  whisper.cpp JSON schema shapes (a newer segment-based format with millisecond offsets, and an
  older word-based format) — real evidence whisper.cpp's own output format has changed across
  versions and this code was patched to cope.
- **`src/utils.py` is confirmed to be an empty 4-line stub** ("Shared helpers (time formatting,
  logging)" comment, no code) — not a coverage gap, just unused/aspirational scaffolding.

None of this changes the Repo 1/Repo 2 "concrete reusable pattern" recommendations already in this
file, but it does add two new ones worth folding into the cross-repo synthesis: ClipsAI's
mouth-movement-tracked dynamic crop is a substantially better reframing technique than a naive
centered crop (relevant if/when this project adds vertical-format export), and the
pluggable-transcription-backend pattern (auto-detect whisper.cpp-on-disk vs. faster-whisper) is a
reusable, low-effort way to support both GPU-light and GPU-heavy user setups without hardcoding one
transcription stack.

### ClipsAI completion note — `media/editor.py` (the actual ffmpeg execution layer) and tests

Closing the last real gap in this repo: `clipsai/media/editor.py`'s `MediaEditor` class (1493
lines — the class every other module in this repo ultimately calls to actually invoke ffmpeg;
`trim`, `transcode`, `watermark_and_crop_video`, `watermark_corner_of_video`,
`merge_audio_and_video`, `concatenate`, `crop_video`, `resize_video`), plus `tests/test_clip.py`
and `tests/test_resize.py` (spot-read per the task's "tests worth a glance" guidance — both are
real, meaningful parametrized unit tests, not smoke tests).

**The concrete, previously-missing answer to "how does ClipsAI actually render the dynamic-crop
vertical video from the `Segment` list `Resizer.resize()` produces":** `resize_video()` does **not**
build one filter_complex with per-segment crop/trim/setpts the way metaleey's `merge_segments_direct`
does (documented in `deep_dive_ingestion_and_pipelines.md`). It's the simpler, less efficient
pattern: loop over every segment, call `crop_video()` once per segment (a separate `ffmpeg -ss/-to
-vf crop=...` subprocess writing a real temp `.mp4` file per segment to disk), then call
`concatenate()` once at the end to stitch all the per-segment temp files together, then delete the
temp files. This is a direct, concrete point of comparison worth having for this project's own
export-step design: **metaleey's single-pass multi-input-seek+concat-filter technique (already
recommended in the ingestion/pipelines file) is a strict efficiency improvement over what ClipsAI
itself does** — N+1 ffmpeg subprocess invocations plus N temporary files on disk, versus one ffmpeg
process with no intermediate files. `crop_video()` itself doesn't fast-seek (no `-ss` before `-i`;
it's placed after `-i`, meaning it decodes from the start of the file up to the seek point every
time) and re-encodes with `-preset veryfast -crf 18` — real, if imprecise-on-speed defaults worth
knowing if reusing this pattern.

`watermark_and_crop_video()` (a separate method, used for the single-crop + logo-overlay case, not
the multi-segment resize case) confirms the exact ffmpeg watermark-compositing technique: a
`colorchannelmixer=aa={opacity}` filter to make the logo translucent, `scale2ref` to size the logo
relative to the video (not a fixed pixel size), then `overlay=(x):(y)` — a clean, reusable three-step
ffmpeg watermark recipe if this project ever wants to burn in a logo/CTA overlay.

**From the tests**: `test_clip.py`'s valid-config fixture confirms `ClipFinderConfigManager` accepts
`max_clip_duration` up to **900 seconds (15 minutes)** as a valid config value (`min_clip_duration:
15, max_clip_duration: 900` passes validation) — a real, previously-unstated upper bound on how long
a single "clip" can be in this library's own validation layer, relevant context for the
`k=[37,53,73,97]` "10+ minute clip" bucket documented in this file's Repo 1 section: clips in that
bucket can apparently run up to 15 minutes before the config layer would reject them.
`test_resize.py` confirms `Resizer._calc_resize_width_and_height_pixels`'s aspect-ratio math via
direct parametrized cases (e.g. 1920×1080 → 607×1080 for a 9:16 target, extreme ratios like 1:100
and 100:1 handled without error) and confirms `_merge_scene_change_and_speaker_segments`'s splitting
behavior with concrete before/after segment-list examples — both are genuine regression tests
with real expected values, not placeholder/smoke tests, so they're a trustworthy secondary
confirmation source for the algorithms documented above.

This closes out `ClipsAI/clipsai`: every non-trivial file (all of `clip/`, `resize/`, `diarize/`,
`transcribe/`, plus `media/editor.py` and two representative test files) has now been read directly.
Remaining unread files (`filesys/*.py`, the rest of `media/*.py`, `utils/*.py`, `clip/exceptions.py`
and its siblings, the other 4 test files, `sandbox/*.ipynb`) are generic file-handling wrappers,
exception class definitions, or example notebooks — genuinely low-value for a "how does moment
detection/reframing actually work" research question, and skipping them matches this project's own
stated audit standard.

---

## Repo 3 — bendawg2010/Auto-clipper

- **Stars:** 3 (as of 2026-07-29)
- **Link:** https://github.com/bendawg2010/Auto-clipper
- **Note:** default branch is `claude/twitch-clip-analyzer-MPT08`, not `main` — this repo appears
  to itself be a Claude Code output/branch, not a hand-written project, which is worth flagging
  given the source.
- **Files read in full:** `analysis/arc_clip_detector.py` (the 1700-line core pipeline),
  `analysis/yolo_local_analyzer.py`, `analysis/clip_modes.py`, `models/README.md`

### Real technique

This is a **frame-sampling classifier → score → temporal-cluster → pad** pipeline, and it's
actually two detectors layered together, not just "YOLO":

1. **Model reality check:** the bundled `models/best.pt` is a real YOLOv11n checkpoint, ~5.4 MB
   (consistent with a real nano-model export, not a placeholder), fine-tuned on the Arc Raiders
   v0.11 Roboflow dataset (2,880 training frames). Per `models/README.md` it detects **13 shipped
   entity classes**: `raider, raider-down, rocketeer, bastion, leaper, bombardier, hornet, wasp,
   snitch, pop, fireball, probe, turret`. The code's scoring table (`ENTITY_PROFILES` in
   `arc_clip_detector.py`) additionally knows how to score 3 more classes (`queen`, `sentinel`,
   `tick`) that the shipped model doesn't currently output but a better-trained one could, plus 3
   inert HUD-digit-artifact classes (`"0"`, `"1"`, `"5"`) that show up as YOLO false-positive labels
   in the raw dataset and are explicitly zeroed out. So "13 classes" (the user's brief) is the
   real, currently-active number; "19" is the code's forward-compatible scoring vocabulary.
2. **Two independent per-frame scorers, blended.**
   - `YOLODetector.detect()` runs the model on a sampled frame and returns bounding boxes + class +
     confidence. `ScoringEngine.score_yolo()` turns that into a 0–100 score per frame: each detected
     entity class has a hand-tuned `base` score, a `count_bonus` per additional instance beyond the
     first, a 1.3× multiplier if any instance's bounding box exceeds 20% of frame area (i.e., it's
     close/large on screen), a hard floor of 90 if a boss-class entity (`queen`) is present at all,
     plus flat bonuses from `COMBINATION_RULES` — a list of lambda-based co-occurrence rules like
     `"pvp_kill": raider>=1 and raider-down>=1 → +55` or `"squad_wipe": raider-down>=2 → +65`. It
     also adds a 1.2× multiplier if multiple detected entities are spatially close together
     (mean pairwise normalized distance < 0.3) — a real proxy for "things are clustered/chaotic."
   - **Separately**, `PixelAnalyzer` runs pure OpenCV/HSV color-threshold analysis on hand-measured
     HUD regions (documented in the file header as literally measured pixel-by-pixel from 762
     annotated frames of the dataset) — health-bar white-pixel fraction, blue teammate-status bars,
     red damage vignette on screen edges, orange/yellow fire-color detection, death-screen
     brightness/saturation thresholds, inventory-screen detection, etc. This produces its own
     0–100ish `pixel_score` and works **even with zero YOLO model present** — it's a genuine
     no-ML fallback path (`ArcClipDetectorAdapter` auto-detects whether `best.pt` exists and runs
     "YOLO + pixel" or "pixel-only" accordingly).
   - `ScoringEngine.combine(yolo, pixel, boss)` blends them: `blended = yolo*0.65 + pixel*0.35`,
     but with a **safety floor** — `if pixel >= 60: final = max(blended, pixel*0.8)` — explicitly to
     stop the YOLO channel from burying an obvious pixel-only signal (fire/explosion/damage
     vignette) in cases the object detector missed. Boss presence forces the final score to at
     least 85 regardless.
3. **Sampling cadence:** one frame per second by default (`SAMPLE_INTERVAL = 1.0`, overridable via
   a `sample_fps` override), read via OpenCV with a fast-skip optimization — non-sampled frames
   call `cap.grab()` (advances the decoder without the costly color-convert + numpy copy that
   `cap.read()` does) instead of decoding frames that will just be thrown away.
4. **Frame → clip decision is `Clusterer.cluster()`, and this is the direct answer to "what
   triggers the cut, how much padding, how does it handle continuous vs. single-frame
   detections":**
   - Filter every scored frame down to "hot" frames: `final_score >= threshold` (a
     `scoring_version`-dependent default between 30 and 45 on the 0–100 scale, e.g. 35 for
     `v3_temporal`, the default version).
   - Sort hot frames by timestamp, then greedily group them: a hot frame joins the current cluster
     if it's within `gap` seconds (`merge_gap`, default 5s) of the cluster's last frame; otherwise
     it starts a new cluster. **This is the continuous-vs-single-frame handling** — a run of
     back-to-back hot frames (continuous action) collapses into one cluster regardless of length; an
     isolated hot frame more than `gap` seconds from its neighbors becomes its own (likely tiny)
     cluster.
   - Each cluster becomes a clip: `start = first_hot_frame_time - pad`, `end = last_hot_frame_time +
     pad` (`pad` default 2s in the CLI, 2.0s hardcoded in the web-adapter path). If the resulting
     span exceeds `max_d` (default 60s), it re-centers on the single peak-scoring frame and takes a
     fixed `max_d`-wide window around it instead of the full cluster span. **If the span is under
     `min_d` (default 3s), the cluster is discarded outright** — this is the mechanism that kills
     one-off noisy single-frame false positives: a lone hot frame padded by 2s on each side only
     reaches 4s, which usually survives, but the discard rule exists specifically to drop clusters
     that don't clear the bar even after padding.
   - The final highlight's `duration` is then re-clamped a second time to `[min_clip_duration,
     max_clip_duration]` config overrides (default 20–60s) with a flat `+10s` extension added, for
     export purposes — so the *clustering* window and the *final exported clip* window are computed
     separately, with the export step biased longer for watchability.
5. **`ClipMode` enum (`clip_modes.py`)** is a clean orchestration layer worth noting structurally:
   it gates which detector(s) run (`CV`, `YOLO`, `VOICE` speech-trigger, `HYBRID` = CV+YOLO,
   `ALL` = everything) from a single config value, rather than hardcoding a fixed pipeline — a
   useful pattern if we want a similar "pick your signal mix" switch.

### Concrete reusable pattern for our project

This won't be reused as YOLO/Arc-Raiders code (we don't want to fine-tune a per-game model), but
**the `score-per-sampled-frame → threshold → temporal-cluster-with-gap → pad → clamp-duration →
discard-if-too-short` architecture is directly portable and is the strongest single architectural
finding across all three repos for a general-purpose, model-agnostic clipper:**

- Replace `YOLODetector.detect()` + `ScoringEngine.score_yolo()` with a call to Gemini's native
  video/frame understanding to produce a 0–100 "how exciting/clippable is this moment" score per
  sampled timestamp (Gemini can be prompted to reason about the actual content — reactions, kills,
  jokes, dramatic beats — instead of a fixed 13-class taxonomy), and everything downstream
  (`Clusterer.cluster()`'s threshold/gap/pad/min/max logic) can be reused almost verbatim, since it
  only depends on `(timestamp, score)` pairs, not on how the score was produced.
- Keep the **pixel-only fallback pattern** as a design principle even if we don't reuse the exact
  HSV thresholds: always have a cheap, model-optional signal path (audio RMS from repo 2, or basic
  scene-cut/motion detection) so the pipeline degrades gracefully instead of hard-failing when a
  heavier model call is unavailable/rate-limited/too expensive for a given run.
  the `queen`/boss-floor pattern ("if this specific high-value signal fires, force a score floor
  regardless of everything else") is a good template for our own must-clip conditions (e.g., a
  detected donation/subscription alert, a clear on-screen "NEW RECORD" type overlay, etc.).
- The **combination-rules-as-lambdas** pattern (`COMBINATION_RULES`, a list of
  `{name, cond: lambda counts: ..., bonus, category}`) is a clean, easily-extensible way to encode
  "these signals together mean something special" without a tangle of nested if/elif — worth
  copying the *shape* of this even though our conditions will be entirely different (e.g., "loud
  audio peak + chat velocity spike + Gemini-reported laughter" instead of "raider + raider-down").

### Code excerpts worth keeping verbatim

The clustering/padding/discard logic — this is the reusable core, independent of what produced the
per-frame scores:

```python
# analysis/arc_clip_detector.py — Clusterer.cluster
def cluster(self, frames):
    hot = sorted([f for f in frames if f.final_score >= self.thresh],
                 key=lambda f: f.timestamp_seconds)
    if not hot:
        return []
    clusters, cur = [], [hot[0]]
    for f in hot[1:]:
        if f.timestamp_seconds - cur[-1].timestamp_seconds <= self.gap:
            cur.append(f)
        else:
            clusters.append(cur); cur = [f]
    clusters.append(cur)

    clips = []
    for i, cf in enumerate(clusters):
        pk = max(cf, key=lambda f: f.final_score)
        s = max(0, cf[0].timestamp_seconds - self.pad)
        e = cf[-1].timestamp_seconds + self.pad
        if (e - s) > self.max_d:                      # too long: recenter on the peak
            c = pk.timestamp_seconds
            s = max(0, c - self.max_d / 2); e = c + self.max_d / 2
        if (e - s) < self.min_d:                       # too short even after padding: drop it
            continue
        ...
```

The blend-with-safety-floor combiner — a good template for fusing an ML signal with a cheap
fallback signal without letting the ML signal suppress an obvious fallback hit:

```python
# analysis/arc_clip_detector.py — ScoringEngine.combine
def combine(self, yolo, pixel, boss):
    blended = yolo * 0.65 + pixel * 0.35
    f = max(blended, pixel * 0.8) if pixel >= 60 else blended
    if boss:
        f = max(f, 85)
    return min(100, f)
```

---

## Audit pass — additional files read [2026-07-29]

(Repo 3 — bendawg2010/Auto-clipper. Note: a separate audit pass covering Repos 1–2 also lives in
this file under the same heading text, further up — that one and this one were done independently;
this section is scoped entirely to Repo 3's remaining files and doesn't touch Repos 1/2.)

The prior Repo 3 pass read 4 of bendawg2010/Auto-clipper's 69 files. The user pushed back that
this was surface-level and asked directly whether every line/word had actually been read — it
had not. This pass fetched and read, in full, via `gh api repos/bendawg2010/Auto-clipper/contents/<path>?ref=claude/twitch-clip-analyzer-MPT08`:
`analysis/__init__.py` (empty), `analysis/ai_analyzer.py` (329 lines), `analysis/audio_detector.py`
(217), `analysis/chat_detector.py` (269), `analysis/clip_trigger_detector.py` (361),
`analysis/detector.py` (459), `analysis/game_profiles.py` (4016), `analysis/hybrid_detector.py`
(384), `analysis/motion_detector.py` (215), `analysis/roboflow_analyzer.py` (284),
`analysis/roboflow_model_analyzer.py` (236), `analysis/scene_detector.py` (232),
`analysis/video_utils.py` (53), `app.py` (2339), `clip_manager.py` (1501), `desktop.py` (52) — 16
files, ~10,900 lines. `templates/index.html` was spot-checked (grep, not full read) only to confirm
the UI's detection-method dropdown options against what `app.py` dispatches on. Test files,
CHANGELOG/CONTRIBUTING, install scripts, and `models/README.txt` were skipped per the project's own
audit standard (no structural surprises expected there and none of this changes a moment-detection
finding).

The single biggest correction to the prior write-up: **this repo already does LLM-vision-based
moment detection**, and **neither `arc_clip_detector.py` nor `hybrid_detector.py` is "the" pipeline**
— `app.py` exposes 13 independent, mutually-exclusive detection strategies behind one dropdown, and
the ones already documented are two peers among that set, not the top-level system.

### Headline finding — `analysis/ai_analyzer.py`: real, working LLM-vision detection via xAI Grok

`GrokVisionAnalyzer` sends **individual sampled frames** (not video, not batches) to xAI's Grok
vision API and asks it to directly judge excitement — this is exactly the "ask an LLM if this is a
good moment" approach the project's own Gemini-native plan calls for, already implemented and
working end to end against a different vendor. Concretely:

- **Dynamic model selection.** `_resolve_vision_model()` calls `GET https://api.x.ai/v1/models` at
  init time and picks the first available candidate from a hardcoded priority list — cheapest-first:
  `grok-4-1-fast-non-reasoning`, `grok-4-1-fast-reasoning`, `grok-4.20-beta-0309-non-reasoning`,
  `grok-4.20-beta-0309-reasoning`, `grok-2-vision-latest`, `grok-2-vision-1212` — falling back to
  any model with `"vision"` in its name, then any `"fast"` + `"non-reasoning"` model, then a
  hardcoded `grok-4-1-fast-non-reasoning` string if the endpoint call fails outright. This
  "probe /models, pick from a ranked candidate list, degrade gracefully" pattern is worth copying
  regardless of vendor — it's a real defense against a hardcoded model ID going stale.
- **Sampling and encoding:** one frame every `sample_interval_sec` (8s, per the `app.py` call site;
  the class docstring default is 10s), JPEG-encoded at quality 60 and base64'd
  (`cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])`), sent **one frame per HTTP
  request** — there is no multi-image batching and no video-native upload; this is meaningfully
  more expensive per-analyzed-second than a true video-understanding call would be, and it means the
  model never sees temporal context across frames, only the single still.
- **Prompting is entirely game-profile-driven** — `ai_system_prompt`/`ai_user_prompt` come from
  `game_profiles.py` (see below), so the "what counts as exciting" definition changes per game
  without touching this file at all. The Arc Raiders system prompt is a real, structured rubric
  (kills / combat / Arc encounters / explosions / close calls / loot / deaths, scored 0.0–1.0 with a
  written scale: "0.0 = menu/nothing, 0.3 = minor action, 0.6 = good combat, 0.8 = kill/major
  moment, 1.0 = insane play") — a genuinely good example of a structured scoring rubric to steal the
  *shape* of for a Gemini prompt.
- **Retry/failure handling is real, not aspirational:** `_analyze_single` retries transient errors
  (429/500/503/timeout) twice with `2**(attempt+1)`s backoff, and the whole `analyze_frames` run
  aborts early after 5 *consecutive* failures (`"AI API failing consistently"`) rather than silently
  producing zero highlights after burning the whole budget on a dead key/outage.
- **Highlight assembly mirrors the same cluster-and-pad shape documented for `arc_clip_detector.py`**
  but implemented independently in this file: frames scoring `exciting=True` and `score>=0.4` are
  kept (falling back to the top 5 scored frames with `score>=0.2` if nothing clears the bar), merged
  if within `merge_gap` (profile-driven, default 15s) of each other, and the merged span is clamped
  to `[min_clip_duration, max_clip_duration]` with a flat `clip_extension` added — the same
  clamp-and-extend idiom that shows up in literally every detector in this repo (see the repeated
  `duration = max(min_dur, min(max_dur, duration + extension))` line below).

```python
# analysis/ai_analyzer.py — GrokVisionAnalyzer._call_grok
payload = {
    "model": self.model,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
            {"type": "text", "text": user_prompt},
        ]},
    ],
    "max_tokens": 150,
    "temperature": 0.3,
}
```

This is a straight OpenAI-compatible chat-completions vision call (xAI's API mirrors OpenAI's
shape) — trivially portable to Gemini's `generateContent` with an inline image part, which is the
project's actual target.

### `app.py` is the real top-level orchestrator — and it's a flat menu of 13 peer strategies, not a hierarchy

This directly answers the task's open question: **`hybrid_detector.py` does not call
`arc_clip_detector.py`, `chat_detector.py`, `ai_analyzer.py`, or any other detector module — none of
these files import each other.** Every "detector" is a standalone class with its own
`analyze_video(video_path, progress_callback)` contract, and `app.py`'s `_run_analysis_on_file`
(the function invoked by both `/api/analyze` and the watch-folder loop) is a single large
`if/elif` ladder that picks exactly one of them per run based on a `detection_method` string that
comes straight from a `<select>` in `templates/index.html`. The dropdown (confirmed by grepping
`templates/index.html`, not re-transcribed from memory) has these 13 options, with `arc_cv_pipeline`
marked `selected` as the actual UI default (not `audio_cv`, which is only the *code's* fallback
when the value is missing/unrecognized):

`arc_cv_pipeline` (labelled "Auto-Clipper CV — HUD + VFX analysis (recommended)"), `audio_cv`,
`clip_triggers`, `audio_only`, `cv_only`, `motion`, `scene_change`, `hybrid` ("all signals
combined"), `chat_spikes`, `ai_vision` (xAI Grok), `roboflow_workflow`, `roboflow_model`,
`yolo_local`.

Each maps to one detector class, imported flatly at the top of `app.py`:

```python
# app.py — imports feeding the detection_method dispatch
from analysis.detector import GameDetector                      # "audio_cv" (default) / "cv_only"
from analysis.ai_analyzer import GrokVisionAnalyzer              # "ai_vision"
from analysis.audio_detector import AudioDetector                # "audio_only"
from analysis.motion_detector import MotionDetector              # "motion"
from analysis.scene_detector import SceneChangeDetector          # "scene_change"
from analysis.hybrid_detector import HybridDetector              # "hybrid"
from analysis.roboflow_analyzer import RoboflowWorkflowAnalyzer  # "roboflow_workflow"
from analysis.roboflow_model_analyzer import RoboflowModelAnalyzer  # "roboflow_model"
from analysis.yolo_local_analyzer import YoloLocalAnalyzer       # "yolo_local"
from analysis.arc_clip_detector import ArcClipDetectorAdapter    # "arc_cv_pipeline"
from analysis.clip_trigger_detector import ClipTriggerDetector   # "clip_triggers"
# analysis.chat_detector.ChatSpikeDetector is imported lazily inline for "chat_spikes"
```

So the corrected picture: **`arc_clip_detector.py` (the 1700-line YOLO+pixel pipeline documented
above) is the code behind exactly one dropdown option, `arc_cv_pipeline`** — it happens to be the
one the UI defaults to, which is a reasonable signal the author considers it the best detector, but
it is not architecturally "the pipeline." **`hybrid_detector.py` is a different, unrelated
dropdown option** — a from-scratch fusion of audio-loudness + frame-motion + color-histogram
scene-change computed in a single OpenCV pass, sharing no code with `arc_clip_detector.py` at all.

**A genuinely confusing naming collision worth flagging explicitly:** the word "hybrid" means two
unrelated things in this codebase. `detection_method="hybrid"` → `HybridDetector` in
`hybrid_detector.py` fuses **audio + motion + scene-histogram**. But `arc_clip_detector.py`
separately has its own `ClipMode.HYBRID` (documented in the prior pass via `clip_modes.py`) meaning
**CV pixel-analysis + YOLO** fused together *inside* the `arc_cv_pipeline` option. A user picking
"Hybrid — all signals combined" from the UI dropdown is not getting YOLO or pixel-HUD-analysis at
all; they're getting the audio/motion/scene fusion. Anyone reading this repo's code without tracing
both files independently would reasonably conflate the two.

**Two more concrete, quotable mechanisms found only in `app.py`:**

1. A sensitivity slider (0–100, UI-exposed) maps to a uniform threshold multiplier applied to
   whichever detector is chosen:

   ```python
   # app.py — _run_analysis_on_file
   # 0=very selective (threshold*1.6), 50=default (threshold*1.0), 100=catch everything (threshold*0.3)
   sensitivity_multiplier = 1.6 - (sensitivity / 100) * 1.3
   ```

   applied to both `intensity_threshold` and `audio_threshold_db` (the latter via a separate
   linear `audio_adjust = (sensitivity/100 - 0.5) * 8` dB shift) on whatever detector object was
   just constructed, via a generic `_apply_sensitivity(det)` helper that duck-types on
   `hasattr(det, 'profile')` / `hasattr(det, 'intensity_threshold')` — one continuous knob that
   works across every detector class without each one needing bespoke UI wiring.
2. For `arc_cv_pipeline` specifically, the *same* sensitivity slider is instead mapped to one of 5
   discrete named scoring presets inside `ArcClipDetectorAdapter` (not a continuous multiplier):

   ```python
   # app.py — _run_analysis_on_file, arc_cv_pipeline branch
   # 0-19: v1_strict | 20-39: v5_combat_only | 40-59: v3_temporal (DEFAULT)
   # 60-79: v2_balanced | 80-100: v4_aggressive
   ```

   This wasn't visible from reading `arc_clip_detector.py` in isolation — the prior pass noted
   `v3_temporal` is the default `scoring_version` but didn't know it's one rung of a 5-step UI
   dial with named tiers, distinct from every other detector's continuous sensitivity scaling.
3. A free-form `detection_overrides` dict, passed through from the request body straight into
   whichever detector's `profile` (or top-level attribute) matches a fixed allow-list of keys —
   `intensity_threshold, audio_weight, audio_threshold_db, merge_gap, min/max_clip_duration,
   fallback_threshold_ratio, window_seconds, brightness_threshold, sample_fps, peak_weight,
   menu_suppress, trigger_phrases` — giving power users per-run fine-tuning beyond the single
   sensitivity slider, applied *after* the sensitivity multiplier so overrides always win.
4. `yolo_local` degrades gracefully to `arc_cv_pipeline` (`v3_temporal`) when `models/best.pt` is
   missing, rather than erroring — the same "always have a fallback path" principle the prior write-up
   flagged as a design pattern worth copying, now confirmed to also operate at the orchestration
   layer, not just inside `ArcClipDetectorAdapter` itself.
5. **A real, if minor, bug:** `chat_spikes` reads the VOD's Twitch URL from `job.get("url", "")` to
   extract a VOD ID for the GQL chat fetch. That works when the job came from `/api/analyze` with a
   live URL, but a job re-analyzed from the saved library has `job["url"] = f"library:{filename}"`
   (set in `start_analysis`) — `ChatSpikeDetector._extract_vod_id`'s regex won't match that, so
   chat-spike detection silently returns zero highlights (logged, not crashed) for any library
   re-analysis. Same class of bug for `watch:{filename}` jobs from the watch-folder loop.

### `analysis/chat_detector.py` — a second, independent Twitch-chat detector: direct GQL, no external binary

This is a genuinely different implementation of "chat velocity = highlight signal" than
twitch-clip-miner's (Repo 2), worth comparing directly since the original task called that out:
`ChatSpikeDetector` does **not** shell out to `TwitchDownloaderCLI.exe`. It talks to Twitch's own
internal GraphQL endpoint directly over `urllib`, using the same public web client ID every
browser-based Twitch chat-replay tool uses:

```python
# analysis/chat_detector.py — ChatSpikeDetector._fetch_chat
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

This is a real, dependency-free alternative to standing up a separate CLI tool — no subprocess, no
external binary, pure stdlib `urllib`/`json`, paginating via GQL cursors up to a 200-page safety
cap. The offset comes back as `contentOffsetSeconds` on each comment node (same field
twitch-clip-miner's CLI-tool JSON exposes), bucketed into fixed 5-second windows
(`_build_histogram`), and spike-detected with a **mean + std-dev threshold that the UI sensitivity
setting bends**, not a flat z-score cutoff like Repo 2's:

```python
# analysis/chat_detector.py — ChatSpikeDetector._find_spikes
spike_threshold = avg + std_dev * (2.0 - self.intensity_threshold * 2)
spike_threshold = max(spike_threshold, avg * 1.5)   # at least 1.5x average, regardless
```

Reusability note: this GQL approach is arguably *more* portable for our project than
twitch-clip-miner's `TwitchDownloaderCLI` dependency, since it removes an external-binary
requirement entirely — worth using this file's persisted-query pattern instead if/when we add chat
as a signal, rather than the Repo 2 approach previously recommended. It still inherits the same
weakness flagged in Repo 2's writeup (raw message count, no unique-chatter or emote-spam
normalization) — that critique still applies here unchanged.

### `analysis/audio_detector.py` and the audio path in `detector.py`/`hybrid_detector.py` — ffmpeg-native dB peaks, no numpy/scipy/librosa

Every audio-aware detector in this repo (`AudioDetector`, `GameDetector`, `HybridDetector`) uses the
**identical** ffmpeg invocation to get per-second peak loudness — this is copy-pasted three times
verbatim, not shared via `video_utils.py` the way the fps-guard code was consolidated:

```python
# repeated verbatim in audio_detector.py, detector.py, hybrid_detector.py
cmd = ["ffmpeg", "-i", video_path,
       "-af", "astats=metadata=1:reset=48000,"
              "ametadata=print:key=lavfi.astats.Overall.Peak_level:file=-",
       "-f", "null", "-"]
```

This is a materially different technique from twitch-clip-miner's `librosa.feature.rms()` +
`gaussian_filter1d` + `scipy.signal.find_peaks()` approach (Repo 2): no Python audio library at
all — ffmpeg's own `astats` filter does the peak-level extraction, and the "peak-finding" is just a
per-second max plus a linear dB-to-0..1 scale between a profile-driven `audio_threshold_db` (e.g.
-15dB for Arc Raiders) and `audio_ceiling_db` (-3dB). This is a strictly lighter dependency
footprint (no numpy/scipy/librosa needed just for the audio signal) and worth preferring for a v1
if we don't already have scipy in the pipeline for another reason. `AudioDetector` itself
(`audio_only` mode) is otherwise a smaller version of the same
threshold→cluster(`merge_gap`)→clamp-duration pattern documented for every other detector in this
repo — nothing new architecturally, just confirmation the pattern is used consistently across all
~8 CV/audio detector classes, not only `arc_clip_detector.py`.

### `analysis/clip_trigger_detector.py` — an entirely new detection paradigm: verbal "clip that" spotting

Not present in either of the other two repos, and not covered at all by the original 4-file pass
(it's the `VOICE` mode referenced only in passing via `clip_modes.py`). `ClipTriggerDetector`
transcribes the full VOD with Whisper (`faster-whisper` preferred, `openai-whisper` fallback, with
`vad_filter=True` to skip silence for speed) and regex-searches the transcript for the streamer
literally saying "clip that" / "clip this" / "clip it" / "clip me" / bare "clip":

```python
# analysis/clip_trigger_detector.py
DEFAULT_TRIGGER_PHRASES = ["clip that", "clip this", "clip it", "clip me", "clip"]
CLIP_FALSE_POSITIVES = {"ping", "ped", "per", "board", "s", "ping", "art"}
```

The false-positive set is a negative lookahead on the bare word "clip" so it doesn't fire on
"clipping" / "clipboard" / "clip art" / "clipper" — a real, if slightly ad-hoc (it's matching the
word *following* "clip", so "clip ping" would need to actually be spoken, which doesn't obviously
correspond to any of those words appearing as suffixes; this looks like an attempt at suffix
exclusion implemented as next-word exclusion and may not actually catch "clipping" the way intended,
since "clipping" is one token, not "clip" + "ping"). When a trigger fires, the highlight covers the
**`clip_duration` seconds *before* the trigger**, not after — correctly modeling how "clip that" is
actually used live (reacting after the exciting thing already happened), and using word-level
timestamps from Whisper (not just segment-level) to anchor precisely on when the trigger word itself
was spoken:

```python
# analysis/clip_trigger_detector.py — _triggers_to_highlights
clip_start = max(0, t - self.clip_duration)          # duration BEFORE the trigger
clip_end = min(t + self.pre_pad, duration) if duration else t + self.pre_pad
```

This is directly reusable for our project regardless of what other signals we build — verbal clip
triggers are a free, zero-inference-cost signal once we're transcribing anyway (which we already
plan to do for captions/narration), and it requires no visual or audio-energy heuristics at all,
just a transcript.

### `analysis/detector.py` (`GameDetector`) — the actual default detector, distinct from `arc_clip_detector.py`

This is worth being precise about, since it's easy to conflate with `arc_clip_detector.py`: the UI's
`audio_cv` option (and the code-level fallback default when `detection_method` is missing/unknown)
is `GameDetector` from `detector.py`, **not** `ArcClipDetectorAdapter`. `GameDetector` is a purely
declarative, per-game HSV-color-threshold system driven entirely by `game_profiles.py`'s
`"detectors"` dict (`kill_feed`, `damage`, `hit_marker`, `explosion`, `special`, each with a
`region`, HSV `lower`/`upper` bounds, a `weight`, and a `multiplier`) — there is no YOLO, no
PixelAnalyzer, no bundled model weights involved at all. It predates (or is a simpler
sibling of) `arc_clip_detector.py`'s YOLO+pixel system — the file even carries a backwards-compat
alias, `ArcRaidersDetector = GameDetector`, confirming it used to be Arc-Raiders-specific before
being generalized to the 31-game profile system. Two details worth keeping:

- **Menu/loading-screen suppression is a hard gate, not a score penalty:** `_is_menu_frame` checks
  for near-black frames (`mean_brightness < 0.04`) or a uniform, dim center region
  (`std < 10 and brightness < 0.25`) and forces `score = 0.0` unconditionally — and this override
  happens **even when audio is loud**, explicitly to stop a gunshot playing over a loading screen
  from producing a false highlight (`if label == "Menu/Lobby": score = 0.0` regardless of
  `audio_score`). `hybrid_detector.py` implements essentially the same guard independently (plus an
  extra low-saturation check and optional game-specific `menu_suppress_colors`), again duplicated
  rather than shared.
- **Component scoring blend is a straight weighted sum with no per-component normalization beyond
  each detector's own `multiplier`**, then the dominant label is just whichever component had the
  highest individual score — the same "un-normalized weighted sum" pattern flagged as a weakness in
  twitch-clip-miner's combiner (Repo 2) shows up here too, independently.

### `analysis/hybrid_detector.py`, `motion_detector.py`, `scene_detector.py` — near-identical single/multi-signal detectors

These three are structurally the same file duplicated with different subsets of signals:
`MotionDetector` and `SceneChangeDetector` are each a single-signal version of exactly the motion
and scene-change math that `HybridDetector` also computes internally (frame-diff mean for motion,
`cv2.compareHist` correlation + chi-square for scene change, brightness-delta "flash" detection for
both) — none of the three imports either of the other two; each recomputes its slice of the same
formulas from scratch. `HybridDetector`'s actual fusion rule is a **max-of-signals with an
agreement bonus**, not a weighted sum like every other combiner in this project's research so far:

```python
# analysis/hybrid_detector.py — _analyze_video_pass
max_score = max(audio_score, motion_score, scene_score)
signals_active = sum(1 for s in [audio_score, motion_score, scene_score] if s >= 0.2)
if signals_active >= 3:
    fused = min(max_score * 1.3, 1.0)
elif signals_active >= 2:
    fused = min(max_score * 1.15, 1.0)
else:
    fused = max_score
```

This is a different, and arguably better-motivated, fusion idiom than the flat weighted sums seen
elsewhere: "a moment only needs one strong signal to qualify" (per the class docstring) but multiple
agreeing signals boost confidence multiplicatively rather than needing to already be included in a
weight — worth considering as an alternative combiner shape to the ClipsAI-adjacent normalize-then-sum
approach recommended in the original synthesis, particularly since it naturally handles the "we
don't have all signals available every run" case (audio-less clips, chat-less clips) without needing
to re-tune weights per available-signal-set.

### `analysis/roboflow_analyzer.py` and `roboflow_model_analyzer.py` — two cloud-hosted Roboflow backends, distinct from local YOLO

Both are real, working alternatives to the locally-bundled `best.pt` (`yolo_local_analyzer.py`,
already read in the original pass) — neither reuses any code from `arc_clip_detector.py`.

- `RoboflowWorkflowAnalyzer` (`roboflow_workflow`) streams the video over **WebRTC** to a *hosted*
  Roboflow **workflow** (not just a model) — `workspace="beanies-workspace"`,
  `workflow="detect-and-classify-3"` — a specific, named, third-party-hosted pipeline this repo
  depends on continuing to exist, requesting `"webrtc-gpu-medium"` compute in the `"us"` region via
  `inference_sdk.webrtc.VideoFileSource`/`StreamConfig`. Frame results arrive via an
  `@session.on_data()` callback carrying `detection_predictions`/`classification_predictions`,
  scored by average confidence + a detection-count bonus (capped at 5 detections).
- `RoboflowModelAnalyzer` (`roboflow_model`) is the simpler HTTP alternative: samples one frame/sec
  locally with OpenCV and calls `InferenceHTTPClient.infer()` against
  `https://detect.roboflow.com` per frame, hardcoded to model ID `"arc-raiders-05arl-bgcvo/1"` (a
  *different* trained model than the bundled `best.pt`, meaning there are at least two distinct
  Arc-Raiders-tuned YOLO models referenced across this repo — one shipped as a local file, one
  hosted on Roboflow's platform under a different ID).

Both funnel into the same 3-second-bucket → threshold → merge-gap → clamp-duration highlight builder
as everything else in this repo (again independently reimplemented, not shared). Neither is directly
relevant to a Gemini-native plan, but they confirm "cloud inference API called per-sampled-frame,
scored by confidence/count, bucketed into windows" is a viable, previously-implemented pattern for
exactly the kind of external-vision-API integration this project intends to build with Gemini
instead of Roboflow.

### `analysis/game_profiles.py` — 31 game profiles, not just Arc Raiders, plus a real internal inconsistency

This file is far bigger in scope than the original pass suggested: `GAME_PROFILES` defines **31**
complete per-game detection profiles (Arc Raiders, War Thunder, Fortnite, Apex Legends, Valorant,
Call of Duty, League of Legends, Counter-Strike, Minecraft, GTA V, Overwatch, Rocket League, Dead by
Daylight, Escape from Tarkov, PUBG, Elden Ring, Rainbow Six Siege, Rust, The Finals, Marvel Rivals,
Fall Guys, Lethal Company, Among Us, Path of Exile, Warframe, Halo Infinite, Palworld, Monster
Hunter World, Deadlock, Sea of Thieves, Hunt: Showdown, Genshin Impact, Final Fantasy XIV, Naraka
Bladepoint), each with its own HSV detector regions, audio/motion/brightness thresholds, and a
full bespoke Grok system prompt describing that specific game's HUD/kill-feed/highlight vocabulary.
`get_profile()` also supports **user-defined custom profiles** loaded from a `custom_profiles.json`
file sitting next to the app (merged over the `arc_raiders` defaults so unset keys still work), which
is exactly what `app.py`'s `/api/custom-profiles` route (found in this pass, not documented before)
lets a user build through the UI without touching code. So "13 detectable classes for one game" (the
prior write-up's framing) understates the project's actual scope by a lot — Arc Raiders is the
best-supported game (bundled YOLO weights), but the detection *architecture* is built and tuned for
30 other titles too.

**A real, concrete bug/staleness finding:** immediately above the `"war_thunder"` profile entry
sits an orphaned comment block headed `===== ARC RAIDERS V2 — Research-based detection =====`,
containing real, specific corrections to the *actual* `"arc_raiders"` profile directly above it —
e.g. "NO kill feed — deaths emit a RED FLARE skyward", "NO hit markers — crosshair is dynamic",
"THIRD-PERSON shooter — muzzle flash on character model, not center screen". But the live
`"arc_raiders"` profile (lines 16–113) still defines `kill_feed` and `hit_marker` HSV detectors as
if the corrections never happened — the "V2" research notes were written, sourced (ARC Raiders Wiki,
GameRant, GamingBolt, Steam Community, etc. — cited inline), and then never applied to any actual
profile entry; they just sit as dead documentation wedged between `arc_raiders` and `war_thunder`
with no corresponding `arc_raiders_v2` key anywhere in the 4016-line file. Anyone tuning this
project's Arc Raiders detection from the comments alone would be tuning against a HUD that doesn't
match the shipped detector regions.

### `analysis/video_utils.py` — small file, real evidence of this repo's own review process

Only 53 lines, but its docstring is itself a finding: it documents a bug the author (or a prior
review pass) caught in this exact codebase —

```python
# analysis/video_utils.py
"""
Extracted after the review caught 7+ copies of the NaN-safe fps guard
drifting apart (two files used `math.isnan`, five used `fps != fps`,
one used `or 30.0` which misses NaN entirely).
"""
```

— confirming `probe_video()`/`safe_fps()`/`frame_interval_for()` were consolidated here specifically
because OpenCV's `cap.get(cv2.CAP_PROP_FPS)` returns NaN on some codec/container combinations and
several of this repo's many detector files had drifted into subtly different (and in one case
actually broken — `fps or 30.0` doesn't catch NaN, since `NaN or 30.0` evaluates to `NaN`) guards
against it. This doesn't affect any file read in this pass (they all correctly call
`probe_video()`/`frame_interval_for()` now), but it's worth noting as evidence this repo has gone
through at least one real self-correction pass, consistent with the repo's default branch itself
being a Claude Code output.

### `clip_manager.py` — confirms a real ffmpeg export pipeline, plus features not previously documented

Directly answers whether clips actually get exported with real ffmpeg calls: yes.
`ClipManager.extract_clips()` cuts every highlight with:

```python
# clip_manager.py — extract_clips
# -ss after -i = frame-accurate (decode from nearest keyframe); before -i is fast but off by 1-5s
cmd = ["ffmpeg", "-y", "-i", video_path, "-ss", str(start_time), "-to", str(end_time),
       "-c:v", "libx264", "-preset", "fast", "-crf", "23",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", clip_path]
```

naming clips `{job_id}_{clip_id}.mp4` (8-char UUID prefix), with a thumbnail grabbed at the clip's
temporal midpoint (falling back to the clip's own first frame if the midpoint grab fails) and a
`clip_info` dict (`id`, `filename`, `thumbnail`, `start_time`, `end_time`, `duration`, `label`,
`confidence`, `timestamp_display`) — this is the canonical "highlight → clip" record shape every
detector's output eventually flows into. Beyond the plain cut, this file implements a lot more than
the original pass's scope suggested:

- **`download_vod()`** uses `yt_dlp` with `concurrent_fragment_downloads=16` (comment: "Twitch HLS
  has 4-10s fragments; pulling 16 at a time saturates home broadband and cuts 1h-VOD downloads from
  ~8 min to ~2 min") and a 5-tier progress-percentage cascade (total-bytes → fragment-index →
  `_percent_str` parsing → elapsed-time estimate → file-size-growth estimate) so the UI progress bar
  degrades gracefully across yt-dlp's inconsistent progress-hook payloads, plus exponential-backoff
  retry (up to 3 attempts) specifically on network-class errors.
- **`make_tiktok()` / `make_youtube_short()`** build a single `-filter_complex` that crops
  independent gameplay and webcam regions (passed as 0–1 ratios from the UI, so the user visually
  selects both boxes), scales/pads each to a 1080-wide strip, and `vstack`s them into a 1080×1920
  vertical video — YouTube Shorts additionally reserves an 80px black `safezone` bar at the top for
  the platform's own UI overlay before stacking. This is a real, complete reframing solution, not a
  naive center-crop (contrast against twitch-clip-miner's naive `crop=ih*9/16:ih` center crop,
  documented in the Repo 1/2 audit pass above — this repo does the more sophisticated thing for
  vertical export, even though it still doesn't do ClipsAI's mouth-tracked dynamic version).
- **`get_smart_thumbnail()`** samples N evenly-spaced candidate frames, scores each via
  `ffprobe … signalstats` (`YMAX - YMIN` for contrast, penalized by distance of `YAVG` from
  mid-gray 128), and keeps the highest-contrast, most-mid-toned frame as the thumbnail — a genuinely
  useful, cheap (no ML) "pick a good thumbnail" heuristic.
- **`detect_volume_spikes()`** is effectively a general-purpose version of `AudioDetector`'s ffmpeg
  `astats` extraction, exposed as its own API endpoint (`/api/clips/<job_id>/<clip_id>/volume-spikes`)
  for spike markers *within* an already-cut clip (e.g. for caption/SFX timing), not for
  whole-VOD highlight detection.
- Also present: `split_clip`, `extend_clip`, `merge_clips` (with configurable transitions),
  `add_captions`, `add_zoom_pan`, `add_sound_effect`, `add_watermark`, `batch_tiktok` — all real
  ffmpeg-subprocess implementations, confirming this is a full post-production toolkit sitting
  behind the detection layer, not just a cutter.

### `app.py` / `desktop.py` — a full Flask web app with a UI-driven editing suite, plus a desktop wrapper

The original pass didn't establish that this repo is a Flask web app at all. It is: `app.py`
(2339 lines) defines ~50 REST routes on a standard `Flask(__name__)` app (10 GB max upload for VOD
files), and `desktop.py` (52 lines) is a thin `pywebview` wrapper that runs the same Flask server in
a background thread and opens it in a native OS window instead of a browser tab, falling back to
`webbrowser.open()` if `pywebview` isn't installed — so the "app" ships as both a local web UI and a
double-clickable desktop app from the same Flask backend. Beyond starting an analysis job and
serving clips, the UI (per its route list) lets a user: build/save custom game profiles through a
form (`/api/custom-profiles`) rather than editing `game_profiles.py`; run a background
"watch folder" mode that auto-analyzes any new VOD dropped into the library directory
(`_watch_folder_loop`, polling every 5s) using whichever detection method (including
`clip_triggers`) was configured when watching started; stitch selected clips into one highlight
reel via an ffmpeg concat filter with selectable resolution/quality; detect near-duplicate clips
by >50% time-range overlap; sort/filter the clip list by confidence/duration/time or
tag/review-status; save/apply export presets and track basic usage analytics to local JSON files;
and manually cut an arbitrary-timestamp clip from a library VOD outside of any detector run at all
(`/api/manual-clip`). None of this changes the moment-*detection* picture, but it's a materially
different picture of the project's actual scope than "a detection script" — it's a small SaaS-shaped
product wrapped around the 13 detectors.

### Addendum to the cross-repo synthesis (does this change the bottom-line recommendation?)

The three findings above that most affect the "Bottom line recommendation" at the end of this
document:

1. **`ai_analyzer.py` is real prior art for the project's actual plan**, not a hypothetical: an
   LLM-vision-per-sampled-frame detector, prompted with a structured game-specific scoring rubric,
   feeding the same cluster/pad/clamp assembly logic as every other detector here, already exists
   and works against xAI's Grok. It validates the "replace YOLO with a Gemini vision call" direction
   from the original synthesis rather than changing it — but it also shows the concrete failure mode
   to avoid: per-frame-only calls with no temporal/video context and no batching. If Gemini's native
   video understanding (multi-frame or true video input) is available to us, it should be used
   instead of naively porting this file's one-request-per-frame approach, which is the weakest part
   of an otherwise well-built detector.
2. **The recommendation to treat `arc_clip_detector.py`'s cluster/pad/clamp skeleton as "the"
   architecture still holds**, but should be understood as: this repo converged on that *exact same*
   skeleton independently, at least 8 separate times, across `ai_analyzer.py`, `audio_detector.py`,
   `chat_detector.py`, `detector.py`, `hybrid_detector.py`, `motion_detector.py`,
   `scene_detector.py`, `roboflow_analyzer.py`, and `roboflow_model_analyzer.py` (a
   threshold/merge-gap/clamp-duration highlight builder shows up, hand-duplicated, in every single
   one). That's stronger evidence for the pattern than a single well-built file, not weaker — but it
   also means our own implementation should write this once, shared, rather than reproduce this
   repo's own duplication.
3. **New, reusable idea not in the original synthesis: expose detection strategy and sensitivity as
   user-facing controls, not just an internal implementation detail.** `app.py`'s flat
   detection-method dropdown + universal sensitivity slider + free-form per-field override dict is a
   genuinely good UX pattern independent of which detector "wins" — worth adopting the *shape* of
   this control surface (one strategy selector, one continuous sensitivity knob applied generically
   via duck-typed attribute access, one escape-hatch override dict) even though our project is a
   single-operator Colab pipeline rather than a multi-user Flask app.
4. **The `HybridDetector` max-plus-agreement-bonus fusion rule** (`max(signals) * 1.3` if all
   signals agree, `*1.15` if two agree, otherwise just the max) is worth weighing against the
   normalize-then-sum combiner recommended in the cross-repo synthesis below — it degrades better
   when not every signal is available for every run (e.g., a VOD with no chat log, or a clip with a
   dead facecam), which is a real scenario for us once signals beyond audio are added incrementally.

This does **not** overturn the existing "Bottom line recommendation" (Auto-clipper's cluster/pad
skeleton + Gemini video-understanding score + audio-RMS pre-filter + chat velocity + ClipsAI
boundary-snapping) — it reinforces point 2 above, adds the per-frame-vs-video-native caveat to the
Gemini-vision piece, and adds the sensitivity-slider/override-dict UX pattern and the
agreement-bonus fusion shape as two new, additive ideas worth folding in when the funnel is actually
built.

---

## Cross-repo synthesis: what should our project actually use?

The three repos solve genuinely different sub-problems, and the honest conclusion is **we need
pieces of all three, not a single winner** — they're complementary, not competing:

1. **Use ClipsAI's TextTiling-on-embeddings as the boundary-refinement layer.** Whatever finds
   *when* something exciting happens (see below), the *exact* clip start/end should snap to a
   TextTiling topic boundary from the transcript, so clips don't open or close mid-sentence. This is
   the only one of the three techniques that's about clip *edges* rather than clip *existence* —
   the other two only tell you a moment is hot, never where a clean cut actually is. Reuse the
   algorithm (gap score → smooth → depth score → local-maximum-above-cutoff), not necessarily the
   heavyweight `all-roberta-large-v1` embedding model.

2. **Use Auto-clipper's score→cluster→pad→clamp architecture as the moment-detection skeleton.**
   It's the most general, model-agnostic of the three designs — it works whether the per-timestamp
   score comes from a fine-tuned YOLO model, pure pixel heuristics, or (our actual plan) a Gemini
   video-understanding call. Its threshold/merge-gap/pad/min-duration/discard-short-clusters logic
   is exactly the mechanism needed to turn "Gemini says this 3-second window looks exciting" into a
   real, watchable clip boundary without hand-rolling that logic from scratch. This is the piece
   most directly reusable *as code*, not just as inspiration.

3. **Use twitch-clip-miner's signal-fusion pattern (audio-peak-seeded candidates + chat velocity +
   z-score normalization) as the pragmatic v1 multi-signal combiner**, with two concrete fixes on
   top of what it does: (a) normalize *every* channel before combining (it only normalizes
   loudness and chat, not transcript/visual — this is the one clear mistake worth not repeating),
   and (b) — **corrected 2026-07-30, same too-quick-to-discard mistake as elsewhere in this
   research (see PROJECT.md's YOLO/Parakeet correction notes)**: don't drop `fer`/MTCNN in favor of
   Gemini outright. Gemini genuinely does more (detects *and explains* a reaction) but it costs real
   tokens; `fer`/MTCNN are free, open, and run locally with zero API cost. That makes them a real
   candidate for the free **statistical pre-filter stage** (stage 1 of the funnel, alongside
   audio-RMS peaks) — flag high-facial-expressivity windows for free, *before* any Gemini call,
   which directly serves the funnel's whole point (spend LLM budget only on windows that already
   look promising). Gemini still does the richer detect-and-explain work downstream, at stage 2/3,
   on the windows this free pass already flagged — the two aren't actually competing for the same
   role once cost is accounted for.

**Bottom line recommendation:** build the v1 moment-detector as Auto-clipper's cluster/pad skeleton,
driven by a Gemini-video-understanding score per sampled window (replacing YOLO) with cheap audio-
RMS peak-finding (from twitch-clip-miner) as a free pre-filter to cut down how many windows we pay
Gemini to look at, chat velocity added as a second cheap signal once we have a chat-log source
wired up, and every clip's final start/end snapped to the nearest ClipsAI-style transcript topic
boundary so clips read as complete thoughts instead of arbitrary windows.
