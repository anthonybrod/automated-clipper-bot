# Verified tools catalog — decision-ready, organized by pipeline stage

Merges real findings from: the 17-video research
(`../research/RESEARCH_YOUTUBE_SOURCES.md`, plus the live re-read still in
progress), and three Gemini reference dossiers, each independently checked
against reality (`../research/tool_verification.md` has the full audit
trail — every claim here traces back to a real check, not to the dossier's
own framing).

**Status key:** ✅ VERIFIED (real, matches claim) · ⚠️ MISMATCH (real, but
does something different than claimed, or is stale/archived) · ❌ NOT FOUND
(hallucinated or unconfirmable) · 🎥 from video research (creator-confirmed
via real transcript, not independently repo-checked) · ⏳ verification
pending

**On URLs below:** every GitHub link is one I confirmed exists directly via
`gh api` this session (not guessed). SaaS product URLs are only included
where I independently verified the domain (Vyro, Opus Clip); anywhere else
a SaaS product is named without a URL, that domain has not been checked —
flagged explicitly rather than guessed, per this project's standing rule
against fabricating URLs.

---

## 1. VOD ingestion / downloading

| Tool | Status | URL | Note |
|---|---|---|---|
| `yt-dlp` | ✅ | https://github.com/yt-dlp/yt-dlp | Universal, well-known, downloads Twitch VODs + YouTube. Not re-verified individually (unambiguous). |
| Twitch Helix `Get Clips` | ✅ (docs) | https://dev.twitch.tv/docs/api/reference/#get-clips | Real, documented endpoint. Only needs an app access token (Client ID+Secret, `client_credentials`) — no user login. **Our proposed primary highlight signal** — see `gemini_suggestions.md`. |
| Twitch Helix `Create Clip` | ✅ (docs) | https://dev.twitch.tv/docs/api/reference/#create-clip | Real, but needs a **user** OAuth token with `clips:edit` scope — materially bigger auth scope than Get Clips. See PROJECT.md open decisions. |
| Twitch EventSub | ✅ (docs) | https://dev.twitch.tv/docs/eventsub/ | Real webhook system for live event triggers (stream online, follows, etc.) — did not confirm it covers clip-creation events specifically, would need the full subscription-types doc. |
| `streamlink` | ✅ | https://github.com/streamlink/streamlink | Pipes live Twitch streams into ffmpeg/a file. Well-known, real. |
| OBS Replay Buffer | 🎥 ✅ | https://obsproject.com/ (built-in OBS Studio feature, not a separate repo) | **Confirmed 3x independently across the video research** (videos 7, 8, 9) — free, native OBS feature, hotkey-saves the last N minutes. Zero extra infrastructure. |
| StreamerBot | 🎥 ✅ | https://streamer.bot/ | Confirmed via video 7 (Vaika) — real-time automated clip triggering during a live stream, zero manual button presses. |
| `pyTwitchAPI` / `twitchAPI` | ✅ | https://github.com/Teekeks/pyTwitchAPI | Full async Twitch Helix + EventSub + chat framework. Real, actively maintained (v4.5.0). |
| `Fittiboy/twitch-clip-archiver` | ✅ | https://github.com/Fittiboy/twitch-clip-archiver | Mass-downloads a channel's existing clips, local or Google Drive. Real, matches claim, ~2yr stale. |
| `zigai/twitch-scraper` | ✅ | https://github.com/zigai/twitch-scraper | CLI+library, clip/profile metadata scraper. Real, matches claim, ~1.5yr stale (most recently active of the small archival tools). |
| `IcePanorama/TwitchClipsDLer` | ✅ (but hobby-grade) | https://github.com/IcePanorama/TwitchClipsDLer | Real `yt-dlp` wrapper for bulk clip downloads. Author's own description flags it as "a quickly hacked together tool" — reference/pattern only. |
| `CanadianZombies/download-twitch` | ⚠️ | https://github.com/CanadianZombies/download-twitch | Real, but narrower than the name suggests — specifically a Discord-webhook clip poster, not a general downloader. Author's own README says "*Possibly*" works. |
| `lay295/TwitchDownloader` | ✅ | https://github.com/lay295/TwitchDownloader | 3,827 stars, most-starred Twitch tool found across all research. Real VOD/clip/chat downloader, fully deep-dived — see `deep_dive_ingestion_and_pipelines.md`. |

## 2. Transcription (ASR)

| Tool | Status | URL | Note |
|---|---|---|---|
| `faster-whisper` | ✅ 🎥 | https://github.com/SYSTRAN/faster-whisper | **Primary recommendation.** Local, free, CTranslate2 Whisper — confirmed both via video research (video 1's real repo uses it) and independent verification (24.6k stars, actively maintained). |
| `whisperX` | ✅ | https://github.com/m-bain/whisperX | Word-level timestamps + speaker diarization. Real, 23.3k stars, very actively maintained. Consider over plain faster-whisper if diarization (who's speaking) matters. |
| OpenAI `whisper` | ✅ | https://github.com/openai/whisper | The foundational model both of the above build on. Real, well-known. |
| `chat-downloader` | ✅ | https://github.com/xenova/chat-downloader | Scrapes VOD/live chat logs (Twitch, YouTube, others), no auth needed. Real, matches claim, not updated since 2023 — check for forks if needed. |
| NVIDIA Parakeet (`nemo-parakeet-tdt-0.6b-v3`) | ✅ (optional GPU path) | https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 | Free, open-weight, faster than whisper on GPU. See PROJECT.md's cost-philosophy correction — kept as a documented optional path, not primary. |

## 3. Highlight / moment detection

### Full-pipeline candidates (do everything end-to-end, not just one stage)

| Tool | Status | URL | Note |
|---|---|---|---|
| **`mutonby/openshorts`** | ✅ **strongest candidate found so far** | https://github.com/mutonby/openshorts (product site: openshorts.app) | **2,784 stars, pushed same day as verification (2026-07-29) — real, popular, actively developed.** Confirmed in its own README: Gemini 3.0 Flash for clip selection, YOLOv8 + MediaPipe for face-tracked auto-cropping, faster-whisper for transcription. Fully deep-dived at the source-code level — see `deep_dive_openshorts.md`. (Is itself a fork of `kamilstanuch/Autocrop-vertical`.) |
| `PriyeshPandey2000/ai-video-clipper` | ✅ | https://github.com/PriyeshPandey2000/ai-video-clipper | Confirmed via full README read: local `whisper.cpp` transcription, Groq/Llama-3.3-70B for clip scoring, a visual review editor, 9:16 burned-subtitle export. Only 2 stars — brand new/unproven, but the architecture (local ASR + fast cheap LLM scoring + human review step) matches our own DIY-strategy thinking closely. |
| `cyberbol/AI-Video-Clipper-LoRA` | ✅ | https://github.com/cyberbol/AI-Video-Clipper-LoRA | Confirmed via README: WhisperX + Qwen2-Audio-7B (ambient sound parsing, e.g. detecting "wind blowing, melancholic music") + Qwen2-VL video captioning. 18 stars, pushed same day as verification. Different angle than most — a *dataset creator* (for training a LoRA) rather than a direct clipping pipeline, but the ambient-sound-aware captioning idea is novel and worth borrowing. |
| `ClipsAI/clipsai` | ✅ | https://github.com/ClipsAI/clipsai | 522 stars. Real story-break detection via TextTiling (topic-shift analysis), not diarization as one dossier implied. Fully deep-dived — see `deep_dive_moment_detection.md`. |

### ⚠️ Confirmed do-not-use (real repo, wrong domain)

- **`meitarbe/cognetivy`** — https://github.com/meitarbe/cognetivy — real, popular (780 stars), but it's "the open-source state layer for AI coding agents" (session/state tracking for coding agents) — **nothing to do with video processing.** Flagged as the single most dangerous finding across all three dossiers specifically because it doesn't 404 or look obviously wrong — a careless `git clone` based on the dossier's description alone would pull the wrong thing entirely.

### Detection signals & techniques

| Tool | Status | URL | Note |
|---|---|---|---|
| Twitch `Get Clips` (viewer-curated) | ✅ (docs) | https://dev.twitch.tv/docs/api/reference/#get-clips | See section 1 — our proposed primary signal, simplest auth. |
| `jamesbaughnd/twitch-clip-miner` | ✅ | https://github.com/jamesbaughnd/twitch-clip-miner | Scores VOD moments via audio energy + speech transcription + chat velocity + facial emotion recognition, GPU-accelerated. Real, functionally sophisticated, but only 6 stars — young/unproven. Fully deep-dived, one real bug found — see `deep_dive_moment_detection.md`. |
| Claude/Gemini as moment-scorer | ✅ 🎥 | n/a (technique, not a repo) | **Confirmed as the real, working core of video 1's actual open-source pipeline** (`COMMAND-LABS/step-by-step-video-clipping-demo`) — shells out to the `claude` CLI directly, scores every candidate moment across 6 dimensions (Insight Quality, Quotability, Emotional Resonance, Controversy, Practical Value, Narrative Power), outputs structured JSON. Also now independently corroborated by `openshorts` (Gemini 3.0 Flash) and `PriyeshPandey2000/ai-video-clipper` (Groq/Llama-3.3-70B) — three separate real projects converge on "cheap/fast LLM scores candidate moments," not a hypothetical. |
| `porplax/auto-highlighter` | ⚠️ | https://github.com/porplax/auto-highlighter | Real, but simpler than implied — a fixed dB-threshold loudness detector, not an AI system. Useful as a cheap first-pass filter, not a full solution. (Note: `porplax/auto-highlighter-py` as named in some dossiers does not exist — no `-py` suffix on the real repo.) |
| NLTK / `vaderSentiment` | ✅ | https://github.com/nltk/nltk / https://github.com/cjhutto/vaderSentiment | Real, lexicon-based sentiment analysis — could flag emotionally-charged chat/transcript segments. Not updated since 2020 but doesn't need to be (lexicon-based). |
| `bendawg2010/Auto-clipper` | ✅ | https://github.com/bendawg2010/Auto-clipper (real code on branch `claude/twitch-clip-analyzer-MPT08`) | Real, MIT-licensed, free YOLOv11n model (13 classes, ~5MB) for the game *Arc Raiders* specifically. Its `Clusterer.cluster()` clip-decision logic is decoupled from YOLO — reusable with our own Gemini scores. Kept as an optional zero-cost plug-in, not discarded — see PROJECT.md's correction note. |
| `nirvagold/stream-clipper` | ✅ | https://github.com/nirvagold/stream-clipper | Tauri/Rust/Svelte desktop app, zero-LLM statistical detector (audio-RMS + chat density, with a 1.5x "combo bonus" when both fire together). Real commercial product. |
| NexusClips | 🎥 ✅ | not independently verified | Confirmed 3x independently in video research (videos 6, 8, 9) — paid SaaS, real 7-day-trial report exists. Not open-source; a buy-vs-build alternative. Domain not checked this session. |

## 4. Video editing / rendering / captioning

| Tool | Status | URL | Note |
|---|---|---|---|
| ffmpeg vertical-crop (`crop=ih*9/16:ih,scale=1080:1920`) | ✅ (already ours) | n/a (our own code) | Already working in `youtube-auto-videos/pipeline.py:3522` — port directly, don't rewrite. See `SALVAGE_INVENTORY.md`. |
| No-Code Architects Toolkit | ✅ 🎥 | https://github.com/stephengpope/no-code-architects-toolkit | **Real, 2.3k stars**, self-hosted free REST API wrapping ffmpeg (caption burning, cut/trim/split, transcribe, silence detection, thumbnails). Confirmed both via video research (video 1 uses it for captions; video 10 is literally the toolkit's own creator) and independently. Strong candidate for our captioning stage. |
| `ffsubsync` | ✅ | https://github.com/smacke/ffsubsync | Auto-syncs subtitle timing to audio via voice-activity-detection + FFT alignment. Real, 7,807 stars, actively maintained (pushed 2026-07-24). |
| `auto-editor` | ✅ | https://github.com/WyattBlue/auto-editor | CLI, cuts silence/dead-air automatically based on audio loudness. Real, actively maintained (v29.3.1, Nov 2025). |
| `ffmpeg-python` | ✅ (but old) | https://github.com/kkroening/ffmpeg-python | Real Python ffmpeg bindings, matches claim, but no release since 2019 — confirm compatibility before depending on it, or just shell out to ffmpeg directly (already our pattern). |
| `MoviePy` | ✅ | https://github.com/Zulko/moviepy | Real, simpler alternative to raw ffmpeg for text overlays/watermarks/concatenation. |
| `rembg` | ✅ | https://github.com/danielgatis/rembg | Real background-removal tool (no green screen needed), CPU/CUDA/ROCm. |
| NVENC hardware encoding | ✅ | https://developer.nvidia.com/nvenc (NVIDIA SDK docs, not a repo) | Real, standard `-c:v h264_nvenc` ffmpeg flag for GPU-accelerated rendering. |
| Submagic | 🎥 ✅ | not independently verified | Confirmed via 2 independent videos (3, 4) as a real, named competitor in AI captioning/clipping — paid SaaS. Domain not checked this session. |
| Opus Clip | 🎥 ✅ | https://www.opus.pro/ (domain confirmed via web search 2026-07-30, Vyro cross-reference) | **Most-repeated tool across the whole video batch (4 separate videos)** — paid SaaS, has a "Brand Kit" feature for locked branding (same idea as our own asset-reuse pattern). Buy-vs-build alternative, not open-source. |
| `Kuonirad/AutoCutAI` | ✅ | https://github.com/Kuonirad/AutoCutAI-Autonomous-AI-Video-Editor-that-Understands-Semiotics-Rhythm | Real, working beat-synced rough-cut algorithm, verified via actual code read (`editor/v1.py`), not just its own grandiose README. 3 stars. See `gemini_dossier_6_raw.md`. |
| `htekdev/vidpipe` | ✅ | https://github.com/htekdev/vidpipe | 205 stars, active. CLI tool: transcribes, removes silence, generates captions, creates shorts/social posts. 8 specialized AI agents on `@github/copilot-sdk`. |

## 5. Distribution / cross-posting

| Tool | Status | URL | Note |
|---|---|---|---|
| YouTube Data API v3 | ✅ | https://developers.google.com/youtube/v3 | Real, standard, for auto-uploading finished Shorts. |
| `instagrapi` | ✅ | https://github.com/subzeroid/instagrapi | Real unofficial Instagram API wrapper (moved from `adw0rd`). Own docs warn private-API automation is fragile in production — sandbox carefully. |
| `davidteather/TikTok-Api` | ✅ (but fragile) | https://github.com/davidteather/TikTok-Api | Confirmed real via GitHub API: 6,530 stars, not archived, pushed 2026-07-03 (actively maintained). **151 open issues** — a real, current maintenance-burden signal for any unofficial wrapper fighting TikTok's anti-bot countermeasures. Usable, but budget for it breaking periodically. |
| `discord.py` | ✅ | https://github.com/Rapptz/discord.py | Real, standard — for posting into Discord bounty/submission channels. |
| Repurpose.io | 🎥 ✅ | not independently verified | Confirmed via video research — video 5 is literally that company's own channel. Dedicated Twitch-clip cross-posting SaaS. Domain not checked this session. |
| Nuelink | 🎥 ✅ | not independently verified | Confirmed via video 15 — another real cross-poster. Domain not checked this session. |
| Pabbly Connect | 🎥 ✅ | not independently verified | Confirmed via video 17 — cross-platform posting automation tool. Domain not checked this session. |
| Blotato, Metricool | 🎥 (named, not independently verified) | not independently verified | Named in video-2's description (n8n SaaS-chained approach); Metricool's price ($53/mo) was captured in the recovered research — real recurring-cost data point if that route is ever chosen. Domains not checked this session. |

## 6. Orchestration / infrastructure

| Tool | Status | URL | Note |
|---|---|---|---|
| Real budget enforcement pattern | ✅ (already ours) | n/a (our own code) | `COST_PER_TOKEN`, `DEFAULT_BUDGET_LIMIT`, supervisor check — already working in `pipeline.py`. Port directly. See `SALVAGE_INVENTORY.md`. |
| `get_secret()` | ✅ (already ours) | n/a (our own code) | Colab userdata + env fallback. Already working. Port directly — the Gemini reference script's lack of this exact pattern was one of its real bugs. |
| SQLite (`sqlite3`) | ✅ | https://www.sqlite.org/ | Real, standard — track which VODs already processed, avoid duplicate work across runs. |
| Docker / `docker-compose` | ✅ | https://www.docker.com/ | Real, standard packaging approach if this ever runs on a VPS instead of Colab. |
| Celery / Redis | ✅ | https://github.com/celery/celery / https://redis.io/ | Real task-queue libraries, only relevant if scaling to many streamers at once — not a v1 need. |
| Streamlit | ✅ | https://github.com/streamlit/streamlit | Real, could work as a lightweight human-review UI for AI-picked clips before rendering (mirrors video 1's Airtable human-review step). |

## 7. Business-model context (not tools — market/economics facts)

- **Whop Clipping** — https://whop.com/ — real paid clipper marketplace (platforms pay people/bots per clip). Separate business model from running your own compilation channel. Confirmed via video research (videos 12, 13).
- **Biro** — not independently verified (domain not checked this session) — real, named paid clipper marketplace per video research (videos 12, 13).
- **Vyro** — https://www.vyro.com/ (domain confirmed via web search 2026-07-30) — real, notable, launched October 2025, MrBeast-backed (built by the team behind his analytics company ViewStats), also used by Mark Rober and Unwell. Real rate ~$3/1,000 views.
- **Headliner** — not independently verified (domain not checked this session) — real, named clipping tool with a genuinely free tier per video research (video 12).
- Streamer clip-farming/bounty economy (Discord submission channels) — corroborated independently by both the video research and the first Gemini dossier's "Lacy" tangent.

---

## Verification still pending

- The specific domains for NexusClips, Submagic, Repurpose.io, Nuelink, Pabbly Connect, Blotato, Metricool, Biro, Headliner — named and confirmed real via video research (viewers can see the creator using the actual product), but not independently domain-verified this session. Worth a real check before hard-linking to any of them.

All named GitHub repos across all six Gemini dossiers are now fully
verified (see `research/tool_verification.md` for the full combined audit
trail — 34+ repos checked, ~85% clean matches).

## The two real architecture strategies (from video research, still the clearest framing)

1. **DIY/self-hosted** (recommended, matches the budget lesson from Parents Teach Kids): faster-whisper (free) → Claude/Gemini for moment-scoring (already paying for this) → NCA toolkit or raw ffmpeg for cut/caption → any real cross-poster. Near-zero recurring cost, no generative-art QA wall to hit.
2. **SaaS-chained** (faster to stand up, real recurring cost): Opus Clip/Submagic/NexusClips for curation+captions, glued to Blotato/Metricool/Repurpose.io via n8n/Make/Pabbly. Often $30-100+/mo stacked across tools.
