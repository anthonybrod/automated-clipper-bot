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

📂 THE DEFINITIVE MASTER TOOL & RESOURCE DIRECTORY: @LacyCrashOuts
Status: Unified Compilation of All 78 Sources [cite: 1–78].
This master list follows the "Director, Not Laborer" philosophy, providing the official URLs and exact operational roles for every tool identified during the research and pre-flight phases [cite: 44, 659].
1. VOD & LIVE STREAM INGESTION (Source Material)
yt-dvr (github.com/MCJack123/yt-dvr): Primary. A background service used to automatically ping and record Lacy's live streams in real-time using resilient MPEG-TS (.ts) containers [cite: 1, 28, 331, 517].
yt-dlp (github.com/yt-dlp/yt-dlp): Used. The gold-standard fork used to download high-resolution VODs and extract server-side m3u8 master manifests [cite: 5, 45, 110, 631].
streamlink (github.com/streamlink/streamlink): Backup. CLI utility used to pipe live streams directly into a local player or capture file if yt-dlp throttles [cite: 45, 50, 75, 631].
TwitchDownloader (github.com/Lay295/TwitchDownloader): Alternative. Designed for fast multithreaded downloading of Twitch VOD files and structured chat dumps [cite: 45, 50, 110, 631].
CanadianZombies/download-twitch (github.com/CanadianZombies/download-twitch): Alternative. Used for ripping specific time-segments from a stream without downloading multi-gigabyte 8-hour VODs [cite: 75, 77, 94].
IcePanorama/TwitchClipsDLer (github.com/IcePanorama/TwitchClipsDLer): Alternative. Used to bulk-download hundreds of existing viewer-made clips for mass archival [cite: 75, 77, 94].
Kick Vod Online Downloader (fileshot.io/tools/kick-vod-downloader): Alternative. A web-based extractor for Kick VODs when local CLI tools hit Cloudflare walls [cite: 26, 362].
2. CHAT MINING & VIRALITY SIGNAL DETECTION
chat-downloader (github.com/xenova/chat-downloader): Primary. Scrapes Twitch, YouTube, and Kick chat logs with millisecond timestamps to detect KEKW/💀 spikes [cite: 5, 45, 110, 445, 631].
TwitchChatDownloader (github.com/PetterKraabol/Twitch-Chat-Downloader): Backup. Specialized tool used to output chat logs into structured JSON arrays for precise reaction correlation [cite: 45, 50, 75, 631].
TwitchAPI (Python) (github.com/Teekeks/pyTwitchAPI): Used. Asynchronous library used to fetch VOD metadata and monitor Lacy's "Live" status without blocking the main script [cite: 45, 50, 75, 631].
Vedal-Chat-Pipeline (github.com/felixkeng/vedal-chat-pipeline): Used (Math). Source for the "Hype Score" methodology (current messages / average messages ≥ 2.0) [cite: 1, 60, 518, 574].
David-Fryd/chat-analyzer (github.com/David-Fryd/chat-analyzer): Alternative. Processes past stream data to provide a summarized activity map over the stream's lifetime [cite: 7, 262].
wredan/Twitch-Chat-Analyzer (github.com/wredan/Twitch-Chat-Analyzer): Alternative. Implements Sentiment Analysis to detect emotional peaks (anger, laughter, hype) in viewers [cite: 78, 695, 698].
kickpython (pypi.org/project/kickpython): Alternative. Python wrapper used to connect to Kick’s Pusher-based WebSocket chatrooms [cite: 233, 596].
Scorpy-37/Kick.com-PythonChatReader (github.com/Scorpy-37/Kick.com-PythonChatReader): Alternative. Script to read live Kick messages via undetected_chromedriver to bypass Cloudflare protection [cite: 35, 233, 490].
3. LOCAL TRANSCRIPTION & SEMANTIC SEGMENTATION
faster-whisper (github.com/SYSTRAN/faster-whisper): Primary. Fast CTranslate2 implementation used for high-speed local transcription with a lean INT8 VRAM footprint [cite: 5, 24, 45, 110, 531].
WhisperX (github.com/m-bain/whisperX): Upgrade. Adds word-level forced alignment and speaker diarization to eliminate subtitle drift [cite: 46, 51, 96, 110, 358].
ClipsAI (github.com/ClipsAI/clipsai): Primary. Algorithm (TextTiling) used for semantic gap scoring to ensure clips start and end on complete thoughts [cite: 1, 5, 46, 97, 110].
FunClip / SenseVoice (github.com/modelscope/FunClip): Backup. Blazing-fast multilingual transcription and emotion detection running entirely on consumer hardware [cite: 36, 455, 460].
Ollama (ollama.com): Primary. Local LLM runner used to execute Llama 3.2 for scoring hooks and verifying clip quality at zero token cost [cite: 5, 6, 61, 110, 445].
Google Gemini API (ai.google.dev): Primary (Cloud). Default processing engine for grading hook strength and multimodal video understanding (Flash 1.5/2.5) [cite: 64, 69, 75, 538].
4. VIDEO ASSEMBLY, CROPPING & EFFECTS
FFmpeg (ffmpeg.org): Primary. The project backbone for video trimming, cropping, watermarking, and hardware-accelerated NVENC rendering [cite: 5, 56, 110, 394, 631].
ffmpeg-python (github.com/kkroening/ffmpeg-python): Used. Wrapper used to write complex filtergraphs (like stacking gameplay under face-cam) in Python [cite: 52, 75, 78, 94].
OpenCV (opencv.org): Primary. Computer vision used to programmatically locate Lacy's face-cam position in a 16:9 frame [cite: 75, 79, 94, 226].
Google MediaPipe Face Mesh (github.com/google-ai-edge/mediapipe): Primary. Lightweight framework used to track Lacy's head movement and dynamically scale the 9:16 crop window [cite: 24, 36, 75, 79, 94, 458].
cut-the-crap (github.com/vantezzen/cut-the-crap): Primary. Uses FFmpeg volume analysis to strip dead air and AFK screens locally before processing [cite: 70, 75, 81, 86, 97].
auto-editor (github.com/WyattBlue/auto-editor): Backup. Automatically cuts out video portions where there is zero motion or audio [cite: 76, 87, 95, 99].
rembg (github.com/danielgatis/rembg): Alternative. Open-source tool used to remove webcam backgrounds without a green screen [cite: 76, 87, 95].
Pillow (PIL) (python-pillow.org): Primary. Image library used to apply dynamic text overlays and gradients to high-CTR viral thumbnails [cite: 469, 622, 641].
moviepy (github.com/Zulko/moviepy): Backup. Programmatic video editing used for composite concatenations and simple text overlays [cite: 52, 75, 78, 94, 631].
5. DISTRIBUTION, PUBLISHING & STEALTH
Playwright (playwright.dev): Primary. Headless browser used to emulate human sessions and bypass platform posting restrictions [cite: 3, 30, 47, 517, 632].
instagrapi (github.com/subzeroid/instagrapi): Primary. Unofficial Python wrapper for automated Reel publishing and account session persistence [cite: 15, 28, 47, 110, 632, 683].
YouTube Data API v3 (developers.google.com/youtube/v3): Primary. Official API for managing Shorts uploads and tracking view quotas [cite: 3, 17, 47, 48, 110, 536, 632].
TikTok Content Posting API (developers.tiktok.com): Alternative. Official endpoint for automated scheduled uploads (requires account auditing) [cite: 71, 82, 93, 120, 549].
TikTokAutoUploader (github.com/makiisthenes/TiktokAutoUploader): Alternative. Uses raw Requests to upload to TikTok in <3 seconds without Selenium [cite: 1, 65, 599].
GeckCore/TikTok_Bot (github.com/GeckCore/TikTok_Bot): Alternative. Autonomous TikTok engine utilizing persistent Chrome profiles to bypass bot detection [cite: 33, 481, 518].
X API v2 (developer.x.com): Primary. Native posting to the @LacyCrashOuts brand account (16:9 format) [cite: 3, 35, 510, 543].
Undetected-Playwright / Camoufox (github.com/berstend/camoufox): Used. Stealth browser arguments used to mask bot fingerprints during video uploads [cite: 3, 205, 220, 517].
EditThisCookie (editthiscookie.com): Primary. Chrome extension used to export session JSON pools for browser rotation [cite: 3, 517, 527].
youtube-upload (tokland) (github.com/tokland/youtube-upload): Alternative. Command-line tool used for direct script-to-YouTube uploads [cite: 17, 294].
6. ORCHESTRATION, STATE & AUTOMATION
LangGraph (github.com/langchain-ai/langgraph): Primary. Orchestration framework used to manage the pipeline's state-machine execution graph [cite: 65, 71, 112, 527].
AsyncSqliteSaver / SQLite (sqlite.org): Primary. Replaces volatile MemorySaver to persist task queues and payouts in pipeline_master.db [cite: 29, 71, 110, 527, 633].
n8n (n8n.io): Backup. Self-hosted, free Docker orchestrator used to link Telegram webhooks with social posting pipelines [cite: 5, 17, 110, 394, 453].
Streamlit (streamlit.io): Used. Rapid web framework used to spin up local "Command Centers" for human-in-the-loop review [cite: 52, 71, 76, 93, 110].
tenacity (github.com/jd/tenacity): Used. Retry library used to handle transient network hiccups and API rate limits [cite: 2, 154, 201].
7. ANCHORED RESEARCH REPOSITORIES (The "Salvage Yard")
OpenShorts (github.com/mutonby/openshorts): Logic Donor. Source for snap_clip_to_words() and two-stage moment scoring [cite: 1, 16, 24, 46, 518, 628].
Indiser/ViralContent-Factory (github.com/indiser/ViralContent-Factory): Logic Donor. Python automated pipeline for batch-processing content [cite: 49, 57, 59].
Auto-clipper (github.com/bendawg2010/Auto-clipper): Logic Donor. Scans VODs for engagement via HSV color analysis and voice-triggered markers [cite: 5, 46, 110, 442, 518].
PriyeshPandey2000/ai-video-clipper (github.com/PriyeshPandey2000/ai-video-clipper): Alternative. Local-first Electron app featuring local Whisper and Groq AI scoring [cite: 46, 49, 57, 59].
Metaleey/AI-auto-segment-edit-video-pipeline (github.com/metaleey/AI-auto-segment-edit-video-pipeline): Alternative. Python pipeline handling ASR and semantic analysis for smart clipping [cite: 49, 70, 81, 92].
HA6Bots/TCCG (github.com/HA6Bots/Twitch-Clips-Compilation-Generator-TCCG-): Alternative. Management interface for automatically stitching clips into compilations [cite: 48, 76, 94].
Vijax0/ai-clip-creator (github.com/Vijax0/AI-clip-creator): Alternative. Full-stack PyTorch application for multi-hour Twitch VOD highlight extraction [cite: 48, 72, 76, 94].
8. EXTERNAL AI & UTILITY SERVICES
Clipping.net (clipping.net): Primary Bounty Hub. Payout platform hosting the $25,000 Lacy bounty pools [cite: 435, 455].
Pollinations.ai (pollinations.ai): Alternative. Fetches auth-free AI images for scene background generation [cite: 578, 586, 589].
OpenRouter (openrouter.ai): Used. Universal API gateway used to generate structured short-form scripts across 30+ LLMs [cite: 578, 586, 589].
Postproxy / Blotato (postproxy.dev, blotato.com): Reference. Unified social media infrastructure used for 2026 platform spec research [cite: 41, 42, 495, 504].
Claude Code (anthropic.com): Used. Agentic terminal tool used for scaffolding project directories and wiring automation logic [cite: 102, 103, 106, 514].
ffsubsync (github.com/agnostic-apollo/ffsubsync): Alternative. Uses cross-correlation to align out-of-sync subtitle text with video audio [cite: 51, 71, 75, 79, 99].
YTSubConverter (github.com/arcusmaximus/YTSubConverter): Alternative. Creates styled YouTube (SRV3/YTT) subtitles for formatted captions [cite: 56, 556].