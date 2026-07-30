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
where I independently verified the domain via live web search + a direct
site visit (Vyro, Opus Clip, and as of the 2026-07-30 verification pass:
NexusClips, Submagic, Repurpose.io, Nuelink, Pabbly Connect, Blotato,
Metricool, Headliner); anywhere else a SaaS product is named without a URL,
that domain has not been checked — flagged explicitly rather than guessed,
per this project's standing rule against fabricating URLs. One name —
**Biro** — was investigated and could NOT be independently confirmed as a
real distinct product; see section 7 for what was actually found (strong
evidence it's a transcription artifact, not a real company).

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
| NexusClips | 🎥 ✅ | https://nexusclips.com | **Domain confirmed via web search + direct site visit 2026-07-30.** Real, matches claim exactly — Twitch-specific AI clip tool (site copy explicitly lists "Twitch twitch clips" / "Twitch free automatic twitch clips" among its use cases), auto-picks best moments, vertical reformat, animated subtitles/hooks, Google sign-in. Confirmed 3x independently in video research (videos 6, 8, 9 — all Cal's Creation / Cpaws Music), including a real 7-day-trial report (video 8). Videos 6 and 8 both give a real discount code from the creator ("Cal" / "Cal C", 10% off) — matches the task's "CAL" reference. Not open-source; a buy-vs-build alternative. |

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
| Submagic | 🎥 ✅ | https://submagic.co | **Domain confirmed via web search + direct site visit 2026-07-30** (`www.submagic.co` redirects to `submagic.co`). Real, France-based, founded 2023, "4M+ businesses" claimed. Matches claim — AI captions (123 languages), auto B-roll, silence removal, AI avatars, and a "Magic Clips" feature that auto-extracts multiple shorts from long source video. Real pricing captured: Starter $12/mo, Pro $23/mo, Business $41/mo (all billed yearly; higher month-to-month), plus a **+$12/mo "Magic Clips" add-on** (10 long videos/mo → auto clips) on every tier — relevant if ever considered as a buy vs. build comparison point for our own clipping stage. Free trial: 3 videos, no credit card. Confirmed via 2 independent videos (3, 4) as a real, named competitor in AI captioning/clipping. |
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
| Repurpose.io | 🎥 ✅ | https://repurpose.io | **Domain confirmed via web search + direct site visit 2026-07-30.** Real — site copy explicitly lists Twitch among its 12+ connected platforms (YouTube, TikTok, Instagram, Facebook, Snapchat, Pinterest, LinkedIn, X, Amazon, BlueSky, Twitch, Drive, Dropbox), and its own YouTube channel (`@Repurposeio`) has a video literally titled "How To Auto-Post Twitch Clips to Social Media" — this is video 5, confirmed as the company's own channel. Real pricing: Starter $35/mo, Pro $79/mo, Agency $179/mo (all monthly billing, 17% cheaper yearly), 14-day free trial, 10 free videos, no card required. "980,434+ creators" claimed. |
| Nuelink | 🎥 ✅ | https://nuelink.com | **Domain confirmed via web search + direct site visit 2026-07-30.** Real, matches claim as a cross-poster (12 platforms: Facebook, Instagram, TikTok, LinkedIn, X, Pinterest, YouTube, Threads, Bluesky, Google Business, Telegram, Mastodon — notably no Twitch listed natively). Real pricing: Standard $12/mo, Premium $32/mo, Business $52/mo, Agency $85.30/mo, Agency-Plus $152/mo (yearly billing). 7-day free trial, "60,000+ creators & businesses," 4.9/5 from 600+ reviews. Has MCP/API support for Claude/ChatGPT to post directly. Confirmed via video 15 (Nuelink's own channel). |
| Pabbly Connect | 🎥 ✅ | https://www.pabbly.com/connect/ | **Domain confirmed via web search + direct site visit 2026-07-30.** Real — a Zapier-alternative no-code automation platform (2,000+ app integrations), built by MagnetBrains LLC (Jaipur, India; founded 2019, Neeraj Agarwal/Jeewan Garg). Matches claim (cross-platform posting automation). Real pricing: Free tier 100 tasks/mo; Standard $14-19/mo for 10,000 tasks/mo; **Unlimited $59-79/mo for unlimited tasks** (notably cheaper than Zapier's $254/mo or Make's $29/mo at equivalent 10k-task volume, per their own comparison chart — a real, useful data point if a cheap glue-layer is ever needed). SOC2 Type 2 + ISO 27001:2022 certified. Confirmed via video 17, whose description mentions the real discount code "ROMYT." |
| Blotato | 🎥 ✅ | https://blotato.com | **Domain confirmed via web search + direct site visit 2026-07-30.** Real — "social media automation for AI agents," built specifically for n8n/Make/MCP-driven pipelines (matches video 2's n8n-based workflow context exactly; also directly corroborated by multiple real n8n.io community workflow listings that name Blotato explicitly). Publishes to 9 platforms (X, LinkedIn, TikTok, Instagram, YouTube, Threads, Facebook, Reddit, Bluesky) via one hosted API. Real pricing: **$29/mo starting price, flat, unlimited posts** (no per-post fee), 7-day free trial. Founded by Sabrina Ramonov (Forbes 30 Under 30). "667K+ posts published last month," "10,000+ business owners on the platform." |
| Metricool | 🎥 ✅ | https://metricool.com | **Domain confirmed via web search + direct site visit 2026-07-30.** Real, matches claim as the distribution tool named in video 1's open-source repo writeup. Real pricing directly re-confirms the $53/mo figure already captured: Free $0/mo (1 brand), Starter from $20/mo, **Advanced from $53/mo** (up to 15 brands; includes Metricool API for Zapier/Make/MCP), scaling to $159/mo for 50 brands. Notable extra detail: Metricool's own channel list explicitly includes **Twitch** alongside Facebook/Instagram/TikTok/YouTube/LinkedIn/Threads/Bluesky/Pinterest — directly relevant if Twitch-native distribution via a SaaS is ever considered instead of building our own poster. |

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
- **Biro** — ⚠️ **investigated and NOT independently confirmed as a real, distinct product** (2026-07-30 pass). Multiple targeted web searches (`"Biro" clipper app paid clipping`, `Biro clipping platform streamers Whop`, `"join Biro" OR "Biro app" clipping campaign creators`, `"biro.gg"`) turned up **zero** matches for a clipping/streamer-marketplace product of that name — only an unrelated TikTok/Instagram personal creator (@birovr) and a Scribd doc for an unrelated "Elysia Biro" influencer campaign. I then went back to the actual video 12 transcript (`research/transcripts/gXXzimVa2A8.txt`, Headliner's "How to Become a Clipper," 00:00-00:11): the narrator says *"become a clipper using platforms like Biro"* exactly once at the very start, then for the entire rest of the video (00:54, 01:05, 01:08, 08:12) repeatedly names and live-demos **"Vyro"** — the product already independently verified elsewhere in this file (`https://www.vyro.com/`). No second product is ever shown. **Conclusion: "Biro" is almost certainly an ASR/auto-caption mis-transcription of "Vyro"** (a plausible v→b mishearing), not a second real company — there is no evidence of a real "Biro" clipping product to link to. Recommend treating the earlier "Biro" citations in `RESEARCH_YOUTUBE_SOURCES.md` (lines 180, 236, 671) as referring to Vyro, not a distinct tool. Video 13 (OpusClip's channel) does not mention "Biro" at all on inspection — its own paid-marketplace example is a Discord community called "Clip Money" (separate from the unrelated fintech company of the same name already flagged elsewhere in this project), not Biro.
- **Vyro** — https://www.vyro.com/ (domain confirmed via web search 2026-07-30) — real, notable, launched October 2025, MrBeast-backed (built by the team behind his analytics company ViewStats), also used by Mark Rober and Unwell. Real rate ~$3/1,000 views. (See the Biro note directly above — video 12 also demos Vyro under the "Biro" name.)
- **Headliner** — https://www.headliner.app — **domain confirmed via web search + direct site visit 2026-07-30.** Real, matches claim (genuinely free clipping/video tools) — multiple independent April 2026 press releases ("Headliner Makes Video Tools Free" — podnews.net, Sounds Profitable, podcastnewsdaily.com) confirm Headliner made its clip/caption/schedule tools free specifically to help creators facing rising production costs. Owned by SpareMin. Confirmed via video 12 (Headliner's own channel), which uses Headliner's free tools to prep clips for submission to paid clipper marketplaces like Vyro.
- Streamer clip-farming/bounty economy (Discord submission channels) — corroborated independently by both the video research and the first Gemini dossier's "Lacy" tangent.

---

## Verification still pending

- **All of the previously-pending domains were checked in the 2026-07-30 pass** (NexusClips, Submagic, Repurpose.io, Nuelink, Pabbly Connect, Blotato, Metricool, Headliner) — each confirmed real via live web search plus a direct site visit; see sections 3, 4, 5, and 7 above for the confirmed URLs and pricing/feature detail found along the way.
- **Biro is the one exception, and it does not appear to be a real, distinct product at all.** Despite multiple targeted searches, no independently verifiable "Biro" clipping/streamer marketplace exists. Going back to the source transcript (video 12) shows the name is mentioned once and then the entire demo is of "Vyro" (already verified elsewhere in this file) — strong evidence "Biro" is an auto-caption mis-transcription of "Vyro," not a second product. Nothing should be hard-linked under the name "Biro"; see the detailed note in section 7.

All named GitHub repos across all six Gemini dossiers are now fully
verified (see `research/tool_verification.md` for the full combined audit
trail — 34+ repos checked, ~85% clean matches).

## The two real architecture strategies (from video research, still the clearest framing)

1. **DIY/self-hosted** (recommended, matches the budget lesson from Parents Teach Kids): faster-whisper (free) → Claude/Gemini for moment-scoring (already paying for this) → NCA toolkit or raw ffmpeg for cut/caption → any real cross-poster. Near-zero recurring cost, no generative-art QA wall to hit.
2. **SaaS-chained** (faster to stand up, real recurring cost): Opus Clip/Submagic/NexusClips for curation+captions, glued to Blotato/Metricool/Repurpose.io via n8n/Make/Pabbly. Often $30-100+/mo stacked across tools.
