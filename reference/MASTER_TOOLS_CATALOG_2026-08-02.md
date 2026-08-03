# MASTER TOOLS CATALOG — everything found, with URLs, sources, and roles

**Purpose.** One consolidated, URL-complete index of every tool surfaced
across this project's research, organized by pipeline stage, each with:
real URL, where the finding came from, verification status, how it could
help, and its **Rule 20 role** (primary / fail-safe / cross-check /
assist / feature).

**Additive — nothing removed.** This does not replace
`reference/verified_tools_catalog.md` (the earlier catalog, still valid)
or any `*_VERBATIM.md` report. It consolidates and adds URLs the earlier
docs lacked.

**Verification legend:**
- ✅ **Verified** — checked against a live source this session or in prior
  logged research (stars/downloads/license read directly)
- ⚠️ **Corrected** — a prior claim about this was wrong; the fix is noted
- ❓ **Unverified** — a real lead, never independently checked. Per Rule 12
  this is not fact.

**Rule 20 roles:** 1 Primary · 2 Backup/fail-safe · 3 Cross-check ·
4 Assist (free pre-filter) · 5 Feature/quality add

---

## STAGE 1 — INGESTION (VOD, live stream, chat)

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **yt-dlp** | https://github.com/yt-dlp/yt-dlp | ✅ 181,579★ | 1 | The chosen VOD/stream downloader. Handles Twitch HLS internally. |
| **`concurrent_fragment_downloads=16`** | (yt-dlp option) | ✅ | — | **~4× speedup**, single option. Source comment: Twitch HLS has 4–10s fragments; 16 at a time cuts a 1h VOD from ~8 min to ~2 min. Slowest non-API step in the pipeline. |
| **streamlink** | https://github.com/streamlink/streamlink | ✅ 11,666★ | 2 | Fail-safe if yt-dlp throttles or breaks on a Twitch change. |
| **yt-dvr** | https://github.com/MCJack123/yt-dvr | ✅ 22★, source-read | 5 | Background daemon, continuous multi-channel recording. MPEG-TS containers survive interruption; auto-remux to MP4 on daemon restart. **All three claims source-verified.** Enables always-on live capture. |
| **lay295/TwitchDownloader** | https://github.com/lay295/TwitchDownloader | ✅ 3,828★ | 2, 5 | Chat JSON schema is a de facto standard (`content_offset_seconds`, `commenter`, `bits_spent`). Also does **chat rendering** (burned-in overlay) which the GQL route can't. |
| **Twitch GQL direct** | `https://gql.twitch.tv/gql` | ✅ source-read | 1 | **Highest-value single artifact found.** Full VOD chat replay, pure `urllib`+`json`, **no API key, no OAuth, no binary**. Persisted query `VideoCommentsByOffsetOrCursor`, sha256 `b70a3591ff0f4e0313d126c6a1502d79a1c02baebb288227c582044571e9e5a4`, Client-ID `kimne78kx3ncx6brgo4mv6wki5h1ko`. |
| **xenova/chat-downloader** | https://github.com/xenova/chat-downloader | ⚠️ **crashed for real** | 2 | Chosen chat tool, but produced a real reproducible `KeyError: 'data'` in its Twitch GraphQL path. Needs defensive `.get()` chaining + Tenacity backoff (Rule 5) before Stage 1 depends on it. |
| **PetterKraabol/Twitch-Chat-Downloader** | https://github.com/PetterKraabol/Twitch-Chat-Downloader | ✅ 649★, stale 2022 | 2 | Distinct from xenova's (pip `tcd`). 4 output formats incl. raw JSON. Real fallback for the crash above. |
| **Teekeks/pyTwitchAPI** | https://github.com/Teekeks/pyTwitchAPI | ✅ 292★, active | 1, 5 | Async. `get_videos()` for VOD metadata + dedicated `eventsub` module for **live online/offline detection** — source-verified. Directly serves live monitoring. |
| **Twitch Helix Get Clips** | https://dev.twitch.tv/docs/api/reference/#get-clips | ✅ | 1 | Viewer-curated highlights. App token only (Client ID + Secret), no user OAuth. |
| **Twitch Helix Create Clip** | https://dev.twitch.tv/docs/api/reference/#create-clip | ✅ | 5 | Self-directed clipping at an exact timestamp — but needs **user OAuth + `clips:edit`**, materially bigger scope. Deferred. |
| **wredan/Twitch-Chat-Analyzer** | https://github.com/wredan/Twitch-Chat-Analyzer | ✅ 25★, stale 2023 | 3 | VADER sentiment, 6-way classification, emotional-peak detection. **Real integration cost caveat:** Java/Kafka/Spark/ElasticSearch/Kibana stack, not a script. |
| **David-Fryd/chat-analyzer** | https://github.com/David-Fryd/chat-analyzer | ✅ 18★, **stale since Aug 2022** | 3 | Per-second chat-activity JSON over a VOD timeline. Built on `chat-downloader` — inherits its fragility. |
| **kickpython** | https://pypi.org/project/kickpython | ✅ 14★, source-verified | 5 | Kick's Pusher WebSocket chat. Source literally connects to `wss://ws-{CLUSTER}.pusher.com`. Multi-platform expansion. |
| **Scorpy-37/Kick.com-PythonChatReader** | https://github.com/Scorpy-37/Kick.com-PythonChatReader | ✅ 19★, source-verified | 2 | Kick chat via `undetected_chromedriver`, explicitly waits out Cloudflare. |
| **CanadianZombies/download-twitch** | https://github.com/CanadianZombies/download-twitch | ⚠️ **capability fabricated** | — | Real repo (8★), but claimed "rip time-segments from a stream" is false — source read shows a **Discord clip-reposting bot**. No VOD/timestamp logic. |
| **IcePanorama/TwitchClipsDLer** | https://github.com/IcePanorama/TwitchClipsDLer | ⚠️ overstated | 2 | Real (4★) but requires **manual paste of each clip URL** — no bulk auto-discovery as claimed. |
| **Kick VOD downloader (fileshot.io)** | https://fileshot.io/tools/kick-vod-downloader | ❓ page live, unauditable | 2 | Generic SEO downloader-mill template; no source to audit. Low trust. |

---

## STAGE 2 — TRANSCRIPTION

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **faster-whisper** | https://github.com/SYSTRAN/faster-whisper | ✅ 24.7k★ | 1 | Current favored engine (no longer a binding rule — Rule 6 removed pending research). CTranslate2, INT8, word timestamps. |
| **`Systran/faster-whisper-large-v3`** | https://huggingface.co/Systran/faster-whisper-large-v3 | ✅ 1,213,984 dl/mo, MIT | 1 | Canonical CT2 baseline — likely today's default. |
| **`distil-whisper/distil-large-v3`** | https://huggingface.co/distil-whisper/distil-large-v3 | ✅ 1,644,401 dl/mo, MIT | 1 | **Strongest upgrade candidate found.** 6.3× faster than large-v3, WER within ~0.2% on ESB. Card documents faster-whisper/CT2 compatibility with code. |
| **`deepdml/faster-whisper-large-v3-turbo-ct2`** | https://huggingface.co/deepdml/faster-whisper-large-v3-turbo-ct2 | ✅ 102,754 dl/mo, MIT | 1 | Drop-in CT2 turbo weights — swap a model string, zero code change. |
| **`openai/whisper-large-v3-turbo`** | https://huggingface.co/openai/whisper-large-v3-turbo | ✅ 8.6M dl/mo, MIT | 2 | Base weights; needs CT2 conversion. Usable directly via `transformers` if conversion fails. |
| **`nvidia/parakeet-tdt-0.6b-v3`** | https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 | ✅ 202,172 dl/mo, **CC-BY-4.0** | 1 (GPU) | 25 languages, RTFx 3,332, avg WER 6.34%. Faster than Whisper on GPU. **Needs NVIDIA NeMo** — heavier dep. License moved off MIT. |
| **WhisperX** | https://github.com/m-bain/whisperX | ✅ 23.4k★ | 5 | Word-level forced alignment + diarization; ~10ms timestamp accuracy via wav2vec2. |
| **whisper.cpp** | https://github.com/ggerganov/whisper.cpp | ✅ | 2 | **Vulkan GPU acceleration** — works on AMD/Intel where CUDA doesn't. Real fallback for non-NVIDIA hardware. Flags for word timestamps: `--word-thold 0.01 --split-on-word --max-len 0 --best-of 5`. |
| **`kyutai/stt-1b-en_fr`** | https://huggingface.co/kyutai/stt-1b-en_fr | ✅ CC-BY-4.0, 135 likes | **5 (live)** | 🔴 **Re-opened by Rule 20 review.** True streaming ASR, **0.5s delay**, semantic VAD built in. Was dismissed for not fitting batch VOD work — but the project's Phase 1 is *live* monitoring, which faster-whisper doesn't serve. |
| **`usefulsensors/moonshine`** | https://huggingface.co/usefulsensors/moonshine | ✅ MIT, 27M/61M params | 2, 4 | Re-opened. CPU-only fail-safe; rough fast pass to locate speech regions. Card admits hallucination — fine for "is there speech," not for captions. |
| **openai-whisper** | https://github.com/openai/whisper | ✅ | 2 | Reference implementation, second fallback. |
| **Silero VAD** | https://github.com/snakers4/silero-vad | ✅ | 1 | **Already bundled inside faster-whisper** (`silero_vad_v6.onnx`) — verified from source. `vad_filter=True` skips silence; big win on dead-air-heavy Twitch VODs. |

---

## STAGE 3 — MOMENT DETECTION (audio, chat, vision, semantic)

### Audio-event & emotion

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **`MIT/ast-finetuned-audioset-...`** | https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593 | ✅ 796,368 dl/mo, BSD-3 | 3, 4 | **Concrete answer to "detect screaming."** AudioSet 527 classes; *Screaming, Shout, Yell, Laughter* verified as real classes via the actual ontology. RMS says "loud"; this says "it was a scream, not a bass drop." |
| **`nicofarr/panns_Cnn14`** | https://huggingface.co/nicofarr/panns_Cnn14 | ✅ Apache-2.0 | 4 | Same 527 classes, lighter CNN. Lower latency if compute is tight. |
| **`FunAudioLLM/SenseVoiceSmall`** | https://huggingface.co/FunAudioLLM/SenseVoiceSmall | ⚠️ 29,557 dl, custom license | 4 | Re-opened. **No screaming class** (original catch was right), but *does* detect **laughter/applause** + emotion + ASR in one pass, claimed 5× faster than Whisper-Small. **License ambiguity is a real blocker** for monetized use. |
| **`ehcalabres/wav2vec2-lg-xlsr-...`** | https://huggingface.co/ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition | ✅ 13,816 dl, Apache-2.0 | 3 | 8-class emotion, 82.23% val. RAVDESS = *acted* speech; transfer to real reactions unverified. |
| **`firdhokk/speech-emotion-...`** | https://huggingface.co/firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3 | ✅ 8,735 dl, Apache-2.0 | 3 | 91.99% acc, Whisper backbone (easy to bolt on). Also acted corpora. |
| **`superb/wav2vec2-base-superb-er`** | https://huggingface.co/superb/wav2vec2-base-superb-er | ✅ 77,316 dl, Apache-2.0 | 3 | Re-opened. IEMOCAP — **different training data** from the two above. As an ensemble member that's the value, not standalone accuracy. |
| **`audeering/wav2vec2-large-robust-...`** | https://huggingface.co/audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim | ⚠️ **research-only** | — | Continuous arousal/valence/dominance — conceptually ideal for "excitement intensity," trained on naturalistic MSP-Podcast. **Commercial use requires a paid license.** Excluded from shipping. |
| **ffmpeg `astats`** | https://ffmpeg.org | ✅ source-read | 1, 4 | Per-second peak loudness with **zero Python audio deps** — no librosa/scipy/numpy. `astats=metadata=1:reset=48000` + `ametadata=print`. Removes 3 heavy deps from the critical path. |
| **librosa + scipy** | https://librosa.org | ✅ | 1 | Full RMS *curve* for prominence-based peak-finding. Real params: z-score → `gaussian_filter1d(sigma=1.0)` → `find_peaks(prominence=0.6σ, distance=1.0s)` → pad ±15s. |
| **pydub** | https://github.com/jiaaro/pydub | ✅ | 4 | Decibel-jump detection (>15dB in 1s) per the plan's audio trigger. |

### Chat signal

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **Vedal-Chat-Pipeline** | https://github.com/felixkeng/vedal-chat-pipeline | ⚠️ **0★, unofficial** | 4 | Source of the "Hype Score" formula (recent msgs / avg msgs ≥ 2.0). Formula matches exactly — but it's an unaffiliated fan project, **not** a Vedal/Neuro-sama official repo. Use the math, not the pedigree. |
| **jamesbaughnd/twitch-clip-miner** | https://github.com/jamesbaughnd/twitch-clip-miner | ✅ source-read | 1 | Chat-velocity histogram + z-score. ⚠️ **Contains a real bug**: `t_max = df["time"].min() if time_range` — should be `.max()`. Fix before porting. |

### Vision / facecam

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **MediaPipe Face Detection (BlazeFace)** | https://github.com/google-ai-edge/mediapipe | ✅ 36.4k★ | 1 | ⚠️ **Correct component — NOT Face Mesh** (wrong 3× independently). 135K params, 2.94ms CPU. Face Mesh adds 2 more model stages for 478 landmarks — built for filters/avatars, overkill here. |
| **`dima806/facial_emotions_image_detection`** | https://huggingface.co/dima806/facial_emotions_image_detection | ✅ 54,471 dl/mo, 126 likes, Apache-2.0 | 4 | Most-used pure emotion classifier on HF. ViT, 7-class, card claims 90.92%. Real upgrade over `fer` as a free local high-reaction signal. |
| **`py-feat/resmasknet`** | https://huggingface.co/py-feat/resmasknet | ✅ 7,867 dl/mo, MIT | 4 | Direct actively-maintained replacement for `fer`/MTCNN (py-feat org updated June 2026). Published ICPR 2020 method. |
| **`trpakov/vit-face-expression`** | https://huggingface.co/trpakov/vit-face-expression | ✅ 15,923 dl/mo, Apache-2.0 | 3 | Lower accuracy (71%) than dima806 — but different training data, so usable as ensemble cross-check. |
| **`fer` (PyPI) + MTCNN** | https://pypi.org/project/fer/ | ✅ | 4 | Free local facecam-reaction signal. Config from source: `max_samples: 8`, `sample_rate: 2.5s`, disk-cached per `(video, start, end)`. **Reversed from an earlier dismissal** — free, so it belongs in the pre-filter, not competing with Gemini. |
| **`AdamCodd/YOLOv11n-face-detection`** | https://huggingface.co/AdamCodd/YOLOv11n-face-detection | ✅ Apache-2.0, 43 likes | 2 | WIDERFACE AP: Easy .942 / Med .921 / **Hard .810**. Heavier than BlazeFace, but better on occluded/hard faces — a fail-safe for frames BlazeFace misses. |
| **`py-feat/face_multitask_v2`** | https://huggingface.co/py-feat/face_multitask_v2 | ⚠️ **non-commercial** | — | 478-pt mesh + AU + valence/arousal. Excluded on license **and** weight class. |
| **facenet_pytorch MTCNN** | https://github.com/timesler/facenet-pytorch | ✅ | 4 | Face detection for crop targeting; GPU-capable. |
| **PySceneDetect** | https://github.com/Breakthrough/PySceneDetect | ✅ | 4, 5 | `AdaptiveDetector` for scene cuts — game↔BRB↔just-chatting transitions as clip boundaries *and* menu-screen detection. |
| **PyAV** | https://github.com/PyAV-Org/PyAV | ✅ | — | Keyframe-seek frame extraction; much faster than OpenCV for scattered timestamps (exactly the "score these 40 windows" pattern). |
| **OpenCV** | https://opencv.org | ✅ 90.2k★ | 1 | ⚠️ **Gotcha**: `cap.get(CAP_PROP_FPS)` returns NaN on some containers, and `fps or 30.0` does **not** catch NaN. Use `fps != fps` or `math.isnan`. Also: `cap.grab()` not `cap.read()` for skipped frames — free speedup. |
| **`Epidot/TwitchLeagueBert-...-highlight-detection`** | https://huggingface.co/Epidot/TwitchLeagueBert-1000k-finetuned-highlight-detection | ❓ 6 dl/mo, weak metrics | 3 | Text-classification (not vision) trained for **Twitch highlight detection** — literally our task. F1 0.398 is poor and docs are minimal, but it's the only model found trained on this exact problem. |

### Semantic / boundary correction

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **`snap_clip_to_words()`** (openshorts) | https://github.com/mutonby/openshorts | ✅ source-read | 1 | ⚠️ **Real behavior corrected**: snaps to **word-boundary timestamps** + up to **0.35s lead / 0.45s tail** padding. NOT "nearest 0.1s silence gap" (that was fabricated). Single most valuable technique found. |
| **ClipsAI TextTiling** | https://github.com/ClipsAI/clipsai | ✅ 524★, MIT, stale Jan 2024 | 1 | Topic-boundary detection so clips are complete thoughts. Real `k` schedules: `[5,7]` <3min, `[11,17]` 3min+, `[37,53,73,97]` 10min+. Dedup: start+end deltas < 15s. ⚠️ **No CLI — import only.** |
| **sentence-transformers** | https://github.com/UKPLab/sentence-transformers | ✅ | 1 | `all-roberta-large-v1` — **free local embeddings** mean the TextTiling layer costs zero API budget. |
| **NLTK** | https://www.nltk.org | ✅ | 1 | `sent_tokenize()` for TextTiling. ⚠️ Fragile char-resync with WhisperX; raises hard `TranscriptionError`. Twitch transcripts (emotes, gamertags, no punctuation) are exactly the pathological case. |
| **pyannote/segmentation-3.0** | https://huggingface.co/pyannote/segmentation-3.0 | ✅ 6.5M dl/mo, MIT (gated) | **5, 3** | 🟠 **Re-opened.** Does VAD + **overlapped-speech detection** — two people talking over each other *is* an argument/hype signal, standalone, no diarization needed. Directly on-target for @LacyCrashOuts. |
| **pyannote/speaker-diarization-community-1** | https://huggingface.co/pyannote/speaker-diarization-community-1 | ✅ 4.97M dl/mo, CC-BY-4.0 (gated) | 5 | Beats 3.1 on DER (DIHARD3: 20.2% vs 21.4%). ~1.5 min to diarize 1 hour on a V100. |
| **pyannote/speaker-diarization-3.1** | https://huggingface.co/pyannote/speaker-diarization-3.1 | ✅ 8.8M dl/mo, MIT (gated) | 5 | Standard choice; pure PyTorch. Gated — needs HF token. |

### Reference architectures (moment detection)

| Repo | URL | Status | How it helps |
|---|---|---|---|
| **mutonby/openshorts** | https://github.com/mutonby/openshorts | ✅ **2,828★**, actively developed | Strongest reference found. `snap_clip_to_words`, `SmoothedCameraman`/`SpeakerTracker`, 3-tier JSON repair, `GeminiBlockedError` fail-fast, real per-model pricing table, "2-second test" hook rule, diversity guard. |
| **bendawg2010/Auto-clipper** | https://github.com/bendawg2010/Auto-clipper | ✅ 3★, MIT | ⚠️ **Ships 13 peer detection strategies + 31 game profiles**, not one pipeline. The **cluster→pad→clamp skeleton** was independently reinvented **8–9 times in this one repo** — strongest architectural signal in the research. Also: bundled YOLOv11n (~5.4MB, 2,880 training frames, MIT). |
| **nirvagold/stream-clipper** | https://github.com/nirvagold/stream-clipper | ⚠️ **freemium** | RMS + chat spike detection, the 1.5× "combo bonus." Free tier watermarks + caps 720p — **skip the app, keep the technique**. |
| **metaleey/AI-auto-segment-edit-video-pipeline** | https://github.com/metaleey/AI-auto-segment-edit-video-pipeline | ✅ 3★ | Single-pass multi-input-seek + concat filter — **strictly better than ClipsAI's N+1 subprocess approach**. Speech-pause snapping (independent convergence). |
| **HA6Bots/TCCG** | https://github.com/HA6Bots/Twitch-Clips-Compilation-Generator-TCCG- | ✅ 140★, **stale 2021** | Clip→compilation stitching. Note trailing hyphen in URL is real. |
| **Vijax0/ai-clip-creator** | https://github.com/Vijax0/ai-clip-creator | ✅ 98★ | PyTorch, explicitly handles "multi-hour Twitch VODs," has a web UI. |
| **PriyeshPandey2000/ai-video-clipper** | https://github.com/PriyeshPandey2000/ai-video-clipper | ✅ 2★ | Electron + local whisper.cpp + Groq scoring + SQLite/Drizzle. Local-first architecture reference. |
| **Kuonirad/AutoCutAI** | https://github.com/Kuonirad/AutoCutAI-Autonomous-AI-Video-Editor-that-Understands-Semiotics-Rhythm | ✅ 3★ | ⚠️ **Nearly dismissed on README tone** — actual source has a genuine working beat-sync algorithm (`SimpleBeatSyncPolicy`). Rule 20 case study. |
| **htekdev/vidpipe** | https://github.com/htekdev/vidpipe | ✅ 205★ | ⚠️ Also nearly dismissed. Real: ~12,000 lines TS, 51 test files, 8 AI agents. |
| **indiser/ViralContent-Factory** | https://github.com/indiser/ViralContent-Factory | ✅ 13★ | Reddit-story→Shorts. **Zero Twitch relevance** — pipeline shape only. |
| **modelscope/FunClip** | https://github.com/modelscope/FunClip | ✅ 6.1k★ | Local Gradio UI, speaker diarization, LLM-assisted clipping. ⚠️ "Blazing-fast on consumer hardware" is **not** in its README; Whisper mode needs heavy GPU. |
| **tryvinci/vinci-clips** | https://github.com/tryvinci/vinci-clips | ✅ | Full-stack (Next.js/Node/Express/FFmpeg). Needs MongoDB — skipped for overhead, not capability. |

---

## STAGE 4 — RENDERING / ASSEMBLY

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **FFmpeg** | https://ffmpeg.org | ✅ | 1 | Backbone. Real production clip command: `-ss` **after** `-i` = frame-accurate (before = off by 1–5s); `-c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -movflags +faststart`. |
| **Chat boxblur** | (ffmpeg filter) | ✅ | 5 | `[0:v]crop=350:450:20:20,boxblur=20:10[blurred];[0:v][blurred]overlay=20:20` — blurs stream chat to prevent TOS flags from viewer messages. Campaign-safety requirement. |
| **9:16 split-screen** | (ffmpeg `vstack`) | ✅ source-read | 1 | Facecam top / gameplay bottom → 1080×1920. **YouTube Shorts variant reserves an 80px top safezone** for platform UI. Ratio-based regions work at any input resolution. |
| **`loudnorm` -14 LUFS** | (ffmpeg filter) | ✅ | 5 | Platform-standard audio normalization. |
| **ffmpeg-python** | https://github.com/kkroening/ffmpeg-python | ✅ 11.0k★, **stale ~2yr** | 2 | Filtergraph wrapper. Maintenance risk noted. |
| **MoviePy** | https://github.com/Zulko/moviepy | ✅ 14.8k★ | 2 | Composite concat + text overlays. |
| **jappeace/cut-the-crap** | https://github.com/jappeace/cut-the-crap | ⚠️ **corrected owner**, 115★, stale 2022 | 4 | Dead-air/AFK removal via ffmpeg silence detection. **Was attributed to `vantezzen` — that URL 404s.** Real owner is `jappeace`. |
| **WyattBlue/auto-editor** | https://github.com/WyattBlue/auto-editor | ✅ 4.6k★, active | 4 | Cuts silent/motionless sections. ⚠️ "zero motion *or* audio" overstates it — threshold-based, audio is default, motion is opt-in `--edit motion`. |
| **danielgatis/rembg** | https://github.com/danielgatis/rembg | ✅ 24.1k★ | 5 | Background removal without green screen. ⚠️ Built for **still images**, not live/webcam — use-case was mischaracterized. |
| **Pillow** | https://python-pillow.org | ✅ 13.7k★ | 5 | Thumbnail text overlays, gradients, color grading. |
| **`get_smart_thumbnail()`** | (technique, from Auto-clipper) | ✅ source-read | 5 | **Zero-ML thumbnail selection**: sample N frames, score via `ffprobe signalstats` — `YMAX-YMIN` contrast penalized by `YAVG` distance from 128. Free, no API. |
| **`.ass` + `\an5` karaoke captions** | (ASS format) | ⚠️ **provisional** (Rule 9) | 5 | Word-level karaoke timing. Gemini-sourced, never user-authorized — needs a yes/no. |
| **arcusmaximus/YTSubConverter** | https://github.com/arcusmaximus/YTSubConverter | ✅ 1,075★, active | 5 | `.ass` → YouTube `.ytt`/SRV3 styled captions. |
| **smacke/ffsubsync** | https://github.com/smacke/ffsubsync | ⚠️ **corrected owner**, 7,808★ | 2 | Subtitle/audio sync via cross-correlation. **Was attributed to `agnostic-apollo` — that 404s.** |
| **No-Code Architects Toolkit** | https://github.com/stephengpope/no-code-architects-toolkit | ✅ 2.3k★ | 5 | Self-hosted free captioning. |

---

## STAGE 5 — DISTRIBUTION

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **YouTube Data API v3** | https://developers.google.com/youtube/v3 | ✅ | 1 | Official Shorts + long-form upload. |
| **X API v2** | https://developer.x.com | ✅ | 1 | Native 16:9 posting. |
| **Meta Graph API** | https://developers.facebook.com/docs/graph-api | ✅ | 1 | Instagram Reels via `/media` + `/media_publish`. |
| **TikTok Content Posting API** | https://developers.tiktok.com/products/content-posting-api | ✅ | 1 | Official; requires account auditing. |
| **subzeroid/instagrapi** | https://github.com/subzeroid/instagrapi | ✅ ~6.3k★ | 2 | Unofficial Reels publishing. Own docs warn private-API automation is fragile. |
| **makiisthenes/TiktokAutoUploader** | https://github.com/makiisthenes/TiktokAutoUploader | ✅ **1,127★**, MIT | 2 | Both claims source-verified: <3s uploads, layout-change resistant. Mechanism: browser only for login/cookie capture, uploads via raw HTTP + Node-generated signature. |
| **tokland/youtube-upload** | https://github.com/tokland/youtube-upload | ✅ 2,190★, stale 2024 | 2 | CLI script→YouTube upload. |
| **Playwright** | https://playwright.dev | ✅ | 2 | Browser automation where APIs are paywalled/restricted. |
| **daijro/camoufox** | https://github.com/daijro/camoufox | ⚠️ **corrected owner, 10,674★** | 2 | 🟠 **Badly under-weighted originally.** Firefox fork, C++-level fingerprint patching (not JS injection), Playwright-compatible, actively maintained. **Was attributed to `berstend` — 404.** |
| **ETCExtensions/Edit-This-Cookie** | https://github.com/ETCExtensions/Edit-This-Cookie | ✅ ~2k★ | — | ⚠️ Real cookie exporter, but "session JSON pools for browser rotation" is **invented terminology** — not a product feature. |
| **GeckCore/TikTok_Bot** | https://github.com/GeckCore/TikTok_Bot | ⚠️ **0★, dormant** | — | Real repo, matches description, but zero-traction single-author project. Not the "autonomous engine" implied. |
| **`-movflags +faststart`** | (ffmpeg flag) | ⚠️ **provisional** (Rule 8) | 5 | Instant-play/progressive download. Gemini-sourced, never authorized. |

---

## STAGE 6 — ORCHESTRATION, JUDGING, STATE

| Tool | URL | Status | Role | How it helps |
|---|---|---|---|---|
| **LangGraph** | https://github.com/langchain-ai/langgraph | ✅ | 1 | StateGraph orchestration. |
| **AsyncSqliteSaver** | (`langgraph.checkpoint.sqlite.aio`) | ✅ **verified gotcha** | 1 | ⚠️ Sync `SqliteSaver` exposes `aget_tuple`/`aput` so `hasattr()` returns True — but **calling them raises `NotImplementedError`** at runtime. Must use the `.aio` variant with `ainvoke()`. |
| **SQLite** | https://www.sqlite.org | ✅ | 1 | Idempotent VOD tracking. **Real recovered schema**: `pipeline_tasks(id, vod_url, start_time, end_time, status, tier1_path, tier2_path)` + `payout_logs(task_id, platform, post_url, view_count, payout_status)`. |
| **Ollama** | https://ollama.com | ✅ | 1 | Local LLM judge, zero token cost. |
| **`meta-llama/Llama-Guard-3-1B`** | https://huggingface.co/meta-llama/Llama-Guard-3-1B | ✅ 59,858 dl/mo | 1, 3 | **Clean fit for the TOS-safety check.** 13 harm categories, purpose-built as a safety gate, **first-party Ollama**: `ollama pull llama-guard3:1b`. Same weight class as the current judge. |
| **`meta-llama/Llama-Prompt-Guard-2-86M`** | https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M | ✅ 98,656 dl/mo | 5 | 🟠 **More relevant than originally judged.** 86M jailbreak/injection detector. The pipeline feeds **untrusted Twitch chat into LLM prompts** — that's a real injection surface, not tangential. |
| **`Qwen/Qwen2.5-7B-Instruct`** | https://huggingface.co/Qwen/Qwen2.5-7B-Instruct | ✅ 12.2M dl/mo, **Apache-2.0** | 1 | Most credibly-reported upgrade over Llama 3.2 for structured JSON. |
| **`Qwen/Qwen2.5-1.5B-Instruct`** | https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct | ✅ 14.1M dl/mo, Apache-2.0 | 2 | Smaller, commercially clean (unlike the 3B). |
| **`Qwen/Qwen2.5-3B-Instruct`** | https://huggingface.co/Qwen/Qwen2.5-3B-Instruct | ⚠️ **non-commercial** | — | "qwen-research" license blocks monetized use. |
| **`NousResearch/Hermes-3-Llama-3.2-3B`** | https://huggingface.co/NousResearch/Hermes-3-Llama-3.2-3B | ✅ llama3 license | 1 | **Same base weights/size as the current model**, fine-tuned for function-calling + strict JSON schema. Sibling Hermes-2-Pro self-reports 90% function-calling / 84% JSON-mode. Needs manual GGUF import (`bartowski/Hermes-3-Llama-3.2-3B-GGUF`). |
| **`microsoft/Phi-3.5-mini-instruct`** | https://huggingface.co/microsoft/Phi-3.5-mini-instruct | ✅ 1.2M dl/mo, **MIT** | 2 | 3.8B, permissive license. |
| **`Salesforce/xLAM-2-3b-fc-r`** | https://huggingface.co/Salesforce/xLAM-2-3b-fc-r | ⚠️ **CC-BY-NC** | — | Claims SOTA BFCL v3 but research-only. Blocked for monetized use. |
| **Ollama `format: json`** | https://ollama.com | ❓ | — | **Possibly bigger lever than any model swap** — grammar-constrained decoding forces valid JSON at token level regardless of model. Check whether existing calls already use it before adding complexity. |
| **unitary/toxic-bert** | https://huggingface.co/unitary/toxic-bert | ✅ 196,138 dl/mo, Apache-2.0 | 3 | Multi-label toxicity. ⚠️ Card warns it flags swearing regardless of tone — real over-flagging risk on Twitch banter. |
| **KoalaAI/Text-Moderation** | https://huggingface.co/KoalaAI/Text-Moderation | ✅ 40,738 dl/mo, OpenRAIL-M | 3 | 9 categories. ⚠️ Self-disclosed **74.9% accuracy, Macro F1 0.326 on rare classes** — weakest exactly where TOS risk is highest. Use only inside a fail-closed wrapper. |
| **eliasalbouzidi/distilbert-nsfw-text-classifier** | https://huggingface.co/eliasalbouzidi/distilbert-nsfw-text-classifier | ✅ 7,178 dl/mo, Apache-2.0 | 3 | Binary safe/nsfw, self-reported 98% acc / 0.974 F1. |
| **cardiffnlp/twitter-roberta-base-hate-latest** | https://huggingface.co/cardiffnlp/twitter-roberta-base-hate-latest | ✅ 4,309 dl/mo, cc-by-4.0 | 3 | Hate speech, **trained on tweets** — register matches chat better than Wikipedia-trained models. |
| **cardiffnlp/twitter-roberta-base-sentiment-latest** | https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest | ✅ 2.6M dl/mo | 4 | 124M tweets; register-matched to captions/chat. |
| **j-hartmann/emotion-english-distilroberta-base** | https://huggingface.co/j-hartmann/emotion-english-distilroberta-base | ✅ 553,603 dl/mo | 4 | 7-way emotion incl. **surprise** — better hook proxy than plain polarity for rage/shock content. |
| **tenacity** | https://github.com/jd/tenacity | ✅ | 1 | Retry/backoff (Rule 5). |
| **Streamlit** | https://streamlit.io | ✅ | 5 | Local human-review "Command Center" UI. |
| **n8n** | https://n8n.io | ✅ ~198.5k★ | 2 | Self-hosted Docker workflow orchestrator (free Zapier alternative). |
| **pywebview** | https://pywebview.flowrey.dev | ✅ | 5 | 52 lines turns a local Flask tool into a double-clickable desktop app. |

**Real gap, honestly recorded:** no purpose-built "hook quality"/engagement
scorer exists on HF — searched and confirmed. Clickbait detectors exist but
solve the *inverse* problem and are effectively unused (539 and 11
downloads). Sentiment/emotion models are proxies, none validated against
real engagement data. This likely needs the LLM or a custom fine-tune.

**Also confirmed absent:** no general "which game is being played" model.
Twitch's own category API metadata is the correct free source.

---

## PLATFORM / HOSTING / INFERENCE LEADS (all ❓ unverified — see `research_targets_platforms_2026-08-02.md`)

| Target | URL | Why it could matter |
|---|---|---|
| **Ollama on free Oracle ARM VM** | https://ollama.com | Moves local-LLM judging to **always-on free cloud** — a live-stream bot can't depend on the user's PC. Highest-leverage lead. |
| **ModelScope** | https://modelscope.cn | Where FunClip/SenseVoice came from — a real second catalog, not an HF mirror. |
| **Replicate** | https://replicate.com | Hosted GPU inference; attacks the no-GPU constraint. |
| **Modal** | https://modal.com | Same. |
| **Together AI** | https://together.ai | Same. |
| **Streamlit gallery** | https://streamlit.io/gallery?category=llms | Working prior art for the review UI. |
| **Civitai** | https://civitai.com | SD models for thumbnails. ⚠️ Licenses vary wildly; many non-commercial. |
| **LM Arena** | https://beta.lmarena.ai | Free model comparison — pick the judge model before committing. |
| **Qwen Chat** | https://chat.qwen.ai | Free tier; Qwen2.5-7B already flagged as a JSON upgrade candidate. |
| **DeepSeek** | https://chat.deepseek.com | Free open-weight access; may lack image understanding. |
| **Perchance / DrawAny / Imagefree** | https://perchance.org/ai-text-to-image-generator | Claimed no-login free image gen for thumbnails. |
| **ComfyUI** | https://github.com/comfyanonymous/ComfyUI | Truly free unlimited image/video gen — **needs local GPU**. |
| **gentube.app** | https://www.gentube.app | ❓ Unknown — supplied by user, never visited. |
| **OpenRouter** | https://openrouter.ai | ⚠️ One API for **400+** models (a directory claimed "30+" — understated by an order of magnitude). |
| **Pollinations.ai** | https://pollinations.ai | Auth-free, no-key image generation. |
| **Postproxy** | https://postproxy.dev | Unified social posting API, 11 platforms. |
| **Blotato** | https://blotato.com | Separate competing product, 9 platforms, $29/mo+. |
| **Clipping.net** | https://clipping.net | The bounty platform. ⚠️ Real ($60M+ paid) but the specific "$5,000 X / $20,000 multi-platform" pools are **not confirmed currently active**. |
| **Whop** | https://whop.com | Real "Clipping lacy" campaign exists; figures signup-gated. |

---

## PENDING — YouTube videos not yet transcribed or mined

Per the user's direction to check these next. **Not started.**

| Video | URL | Already have transcript? |
|---|---|---|
| Higgsfield / Claude connectors | https://www.youtube.com/watch?v=mFOoNPFylLI&t=2s | ❌ No |
| Claude + Whop Clipping Workflow | https://www.youtube.com/watch?v=PafYu69s5NA | ❌ No |
| Gemini Gems Tutorial | https://www.youtube.com/watch?v=QqwNue_KL-4 | ❌ No |
| Lacy's Best Streamer University Moments | https://www.youtube.com/watch?v=cVkFMpDLQrM | ❌ No |
| How Lacy Got Used On Stream | https://www.youtube.com/watch?v=mVqnCvE337E | ❌ No |
| Lacy's Content Strategy Breakdown | https://www.youtube.com/watch?v=lYafPAHVOno | ❌ No |
| AI Social Media Autopilot | https://www.youtube.com/watch?v=u8V45xsnkGA | ✅ Yes — `research/transcripts/u8V45xsnkGA.txt` |
| AI Clipping Monetization Breakdown | https://www.youtube.com/watch?v=IunLg0FY5hY | ✅ Yes — `research/transcripts/IunLg0FY5hY.txt` |

**Method available:** `research/fetch_transcripts.py` already exists and
succeeded on 17/17 videos previously via `youtube_transcript_api` — reuse
it rather than browser-scraping (Rule 1).

**The 6 un-transcribed videos split into two very different groups:**
- **Technical/tooling** (higgsfield, Whop workflow, Gemini Gems) — likely
  yields real tools and techniques for the catalog above.
- **Lacy-specific content** (Streamer University, "got used on stream",
  content strategy) — yields **target-content understanding**: what a
  clip-worthy Lacy moment actually looks like, which directly informs
  detection thresholds and hook patterns. No other source covers this.
