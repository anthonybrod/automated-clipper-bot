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

---

## 1. VOD ingestion / downloading

| Tool | Status | Note |
|---|---|---|
| `yt-dlp` | ✅ | Universal, well-known, downloads Twitch VODs + YouTube. Not re-verified individually (unambiguous). |
| Twitch Helix `Get Clips` | ✅ (docs) | Real, documented endpoint. Only needs an app access token (Client ID+Secret, `client_credentials`) — no user login. **Our proposed primary highlight signal** — see `gemini_suggestions.md`. |
| Twitch Helix `Create Clip` | ✅ (docs) | Real, but needs a **user** OAuth token with `clips:edit` scope — materially bigger auth scope than Get Clips. See PROJECT.md open decisions. |
| Twitch EventSub | ✅ (docs) | Real webhook system for live event triggers (stream online, follows, etc.) — did not confirm it covers clip-creation events specifically, would need the full subscription-types doc. |
| `streamlink` | 🎥/✅ | Pipes live Twitch streams into ffmpeg/a file. Well-known, real. |
| OBS Replay Buffer | 🎥 ✅ | **Confirmed 3x independently across the video research** (videos 7, 8, 9) — free, native OBS feature, hotkey-saves the last N minutes. Zero extra infrastructure. |
| StreamerBot | 🎥 ✅ | Confirmed via video 7 (Vaika) — real-time automated clip triggering during a live stream, zero manual button presses. |
| `pyTwitchAPI` / `twitchAPI` (`Teekeks/pyTwitchAPI`) | ✅ | Full async Twitch Helix + EventSub + chat framework. Real, actively maintained (v4.5.0). |
| `Fittiboy/twitch-clip-archiver` | ✅ | Mass-downloads a channel's existing clips, local or Google Drive. Real, matches claim, ~2yr stale. |
| `zigai/twitch-scraper` | ✅ | CLI+library, clip/profile metadata scraper. Real, matches claim, ~1.5yr stale (most recently active of the small archival tools). |
| `IcePanorama/TwitchClipsDLer` | ✅ (but hobby-grade) | Real `yt-dlp` wrapper for bulk clip downloads. Author's own description flags it as "a quickly hacked together tool" — reference/pattern only. |
| `CanadianZombies/download-twitch` | ⚠️ | Real, but narrower than the name suggests — specifically a Discord-webhook clip poster, not a general downloader. Author's own README says "*Possibly*" works. |

## 2. Transcription (ASR)

| Tool | Status | Note |
|---|---|---|
| `faster-whisper` (`SYSTRAN/faster-whisper`) | ✅ 🎥 | **Primary recommendation.** Local, free, CTranslate2 Whisper — confirmed both via video research (video 1's real repo uses it) and independent verification (24.6k stars, actively maintained). |
| `whisperX` (`m-bain/whisperX`) | ✅ | Word-level timestamps + speaker diarization. Real, 23.3k stars, very actively maintained. Consider over plain faster-whisper if diarization (who's speaking) matters. |
| OpenAI `whisper` | ✅ | The foundational model both of the above build on. Real, well-known. |
| `chat-downloader` (`xenova/chat-downloader`) | ✅ | Scrapes VOD/live chat logs (Twitch, YouTube, others), no auth needed. Real, matches claim, not updated since 2023 — check for forks if needed. |

## 3. Highlight / moment detection

### Full-pipeline candidates (do everything end-to-end, not just one stage)

| Tool | Status | Note |
|---|---|---|
| **`mutonby/openshorts`** (openshorts.app) | ✅ **strongest candidate found so far** | **2,784 stars, pushed same day as verification (2026-07-29) — real, popular, actively developed.** Confirmed in its own README: Gemini 3.0 Flash for clip selection, YOLOv8 + MediaPipe for face-tracked auto-cropping, faster-whisper for transcription. This is a more complete, more validated open-source reference than anything else found across all research — worth reading in full the same way video 1's COMMAND-LABS repo was, before designing our own pipeline from scratch. (Is itself a fork of `kamilstanuch/Autocrop-vertical` — that lineage may be worth a look too.) |
| `PriyeshPandey2000/ai-video-clipper` | ✅ | Confirmed via full README read: local `whisper.cpp` transcription, Groq/Llama-3.3-70B for clip scoring, a visual review editor, 9:16 burned-subtitle export. Only 2 stars — brand new/unproven, but the architecture (local ASR + fast cheap LLM scoring + human review step) matches our own DIY-strategy thinking closely. |
| `cyberbol/AI-Video-Clipper-LoRA` | ✅ | Confirmed via README: WhisperX + Qwen2-Audio-7B (ambient sound parsing, e.g. detecting "wind blowing, melancholic music") + Qwen2-VL video captioning. 18 stars, pushed same day as verification. Different angle than most — a *dataset creator* (for training a LoRA) rather than a direct clipping pipeline, but the ambient-sound-aware captioning idea is novel and worth borrowing. |

### ⚠️ Confirmed do-not-use (real repo, wrong domain)

- **`meitarbe/cognetivy`** — real, popular (780 stars), but it's "the open-source state layer for AI coding agents" (session/state tracking for coding agents) — **nothing to do with video processing.** Flagged as the single most dangerous finding across all three dossiers specifically because it doesn't 404 or look obviously wrong — a careless `git clone` based on the dossier's description alone would pull the wrong thing entirely.

### Detection signals & techniques

| Tool | Status | Note |
|---|---|---|
| Twitch `Get Clips` (viewer-curated) | ✅ (docs) | See section 1 — our proposed primary signal, simplest auth. |
| `jamesbaughnd/twitch-clip-miner` | ✅ | Scores VOD moments via audio energy + speech transcription + chat velocity + facial emotion recognition, GPU-accelerated. Real, functionally sophisticated, but only 6 stars — young/unproven, worth reading the code before relying on it. |
| Claude/Gemini as moment-scorer (LLM judges transcript for hooks/narrative structure) | ✅ 🎥 | **Confirmed as the real, working core of video 1's actual open-source pipeline** — shells out to the `claude` CLI directly, scores every candidate moment across 6 dimensions (Insight Quality, Quotability, Emotional Resonance, Controversy, Practical Value, Narrative Power), outputs structured JSON. Also now independently corroborated by `openshorts` (Gemini 3.0 Flash) and `PriyeshPandey2000/ai-video-clipper` (Groq/Llama-3.3-70B) — three separate real projects converge on "cheap/fast LLM scores candidate moments," not a hypothetical. |
| `porplax/auto-highlighter` (not `-py`) | ⚠️ | Real, but simpler than implied — a fixed dB-threshold loudness detector, not an AI system. Useful as a cheap first-pass filter, not a full solution. |
| NLTK / `vaderSentiment` | ✅ | Real, lexicon-based sentiment analysis — could flag emotionally-charged chat/transcript segments. Not updated since 2020 but doesn't need to be (lexicon-based). |
| NexusClips | 🎥 ✅ | Confirmed 3x independently in video research (videos 6, 8, 9) — paid SaaS, real 7-day-trial report exists. Not open-source; a buy-vs-build alternative. |

## 4. Video editing / rendering / captioning

| Tool | Status | Note |
|---|---|---|
| ffmpeg vertical-crop (`crop=ih*9/16:ih,scale=1080:1920`) | ✅ (already ours) | Already working in `youtube-auto-videos/pipeline.py:3522` — port directly, don't rewrite. See `SALVAGE_INVENTORY.md`. |
| No-Code Architects Toolkit (`stephengpope/no-code-architects-toolkit`) | ✅ 🎥 | **Real, 2.3k stars**, self-hosted free REST API wrapping ffmpeg (caption burning, cut/trim/split, transcribe, silence detection, thumbnails). Confirmed both via video research (video 1 uses it for captions; video 10 is literally the toolkit's own creator) and independently. Strong candidate for our captioning stage. |
| `ffsubsync` | ✅ | Auto-syncs subtitle timing to audio via voice-activity-detection + FFT alignment. Real, matches claim. |
| `auto-editor` | ✅ | CLI, cuts silence/dead-air automatically based on audio loudness. Real, actively maintained (v29.3.1, Nov 2025). |
| `ffmpeg-python` (`kkroening/ffmpeg-python`) | ✅ (but old) | Real Python ffmpeg bindings, matches claim, but no release since 2019 — confirm compatibility before depending on it, or just shell out to ffmpeg directly (already our pattern). |
| `MoviePy` | ✅ | Real, simpler alternative to raw ffmpeg for text overlays/watermarks/concatenation. |
| `rembg` | ✅ | Real background-removal tool (no green screen needed), CPU/CUDA/ROCm. |
| NVENC hardware encoding | ✅ | Real, standard `-c:v h264_nvenc` ffmpeg flag for GPU-accelerated rendering. |
| Submagic | 🎥 ✅ | Confirmed via 2 independent videos (3, 4) as a real, named competitor in AI captioning/clipping — paid SaaS. |
| Opus Clip | 🎥 ✅ | **Most-repeated tool across the whole video batch (4 separate videos)** — paid SaaS, has a "Brand Kit" feature for locked branding (same idea as our own asset-reuse pattern). Buy-vs-build alternative, not open-source. |

## 5. Distribution / cross-posting

| Tool | Status | Note |
|---|---|---|
| YouTube Data API v3 (`google-api-python-client`) | ✅ | Real, standard, for auto-uploading finished Shorts. |
| `instagrapi` (now `subzeroid/instagrapi`, moved from `adw0rd`) | ✅ | Real unofficial Instagram API wrapper. Own docs warn private-API automation is fragile in production — sandbox carefully. |
| `davidteather/TikTok-Api` | ✅ (but fragile) | Confirmed real via GitHub API: 6,530 stars, not archived, pushed 2026-07-03 (actively maintained). **151 open issues** — a real, current maintenance-burden signal for any unofficial wrapper fighting TikTok's anti-bot countermeasures. Usable, but budget for it breaking periodically; don't treat it as a stable foundation the way `yt-dlp` or `pyTwitchAPI` are. |
| `discord.py` (`Rapptz/discord.py`) | ✅ | Real, standard — for posting into Discord bounty/submission channels. |
| Repurpose.io | 🎥 ✅ | Confirmed via video research — video 5 is literally that company's own channel. Dedicated Twitch-clip cross-posting SaaS. |
| Nuelink | 🎥 ✅ | Confirmed via video 15 — another real cross-poster. |
| Pabbly Connect | 🎥 ✅ | Confirmed via video 17 — cross-platform posting automation tool. |
| Blotato, Metricool | 🎥 (named, not independently verified) | Named in video-2's description (n8n SaaS-chained approach); Metricool's price ($53/mo) was captured in the recovered research — real recurring-cost data point if that route is ever chosen. |

## 6. Orchestration / infrastructure

| Tool | Status | Note |
|---|---|---|
| Real budget enforcement pattern (`COST_PER_TOKEN`, `DEFAULT_BUDGET_LIMIT`, supervisor check) | ✅ (already ours) | Already working in `pipeline.py` — port directly. See `SALVAGE_INVENTORY.md`. |
| `get_secret()` (Colab userdata + env fallback) | ✅ (already ours) | Already working. Port directly — the Gemini reference script's lack of this exact pattern was one of its real bugs. |
| SQLite (`sqlite3`) | ✅ | Real, standard — track which VODs already processed, avoid duplicate work across runs. |
| Docker / `docker-compose` | ✅ | Real, standard packaging approach if this ever runs on a VPS instead of Colab. |
| Celery / Redis | ✅ | Real task-queue libraries, only relevant if scaling to many streamers at once — not a v1 need. |
| Streamlit | ✅ | Real, could work as a lightweight human-review UI for AI-picked clips before rendering (mirrors video 1's Airtable human-review step). |

## 7. Business-model context (not tools — market/economics facts)

- **Whop Clipping, Biro** — real paid clipper marketplaces (platforms pay people/bots per clip). Separate business model from running your own compilation channel. Confirmed via video research (videos 12, 13).
- **Headliner** (free tier) — real, named clipping tool with a genuinely free tier. Confirmed via video 12.
- Streamer clip-farming/bounty economy (Discord submission channels) — corroborated independently by both the video research and the first Gemini dossier's "Lacy" tangent.

---

## Verification still pending

- The live 9/8-video re-read (analytics-feedback/self-adjustment hunt, deeper tool/trick extraction) — running, will merge in once back.
- `davidteather/TikTok-Api` — not yet independently checked despite being a fragile unofficial-API dependency, worth doing before relying on it.

All three Gemini dossiers are now fully verified (25 named GitHub repos
checked total: 19 clean matches, 5 real-but-mismatched, 1 hallucinated
owner, 1 near-miss naming). See `research/tool_verification.md` for the full
combined audit trail.

## The two real architecture strategies (from video research, still the clearest framing)

1. **DIY/self-hosted** (recommended, matches the budget lesson from Parents Teach Kids): faster-whisper (free) → Claude/Gemini for moment-scoring (already paying for this) → NCA toolkit or raw ffmpeg for cut/caption → any real cross-poster. Near-zero recurring cost, no generative-art QA wall to hit.
2. **SaaS-chained** (faster to stand up, real recurring cost): Opus Clip/Submagic/NexusClips for curation+captions, glued to Blotato/Metricool/Repurpose.io via n8n/Make/Pabbly. Often $30-100+/mo stacked across tools.
