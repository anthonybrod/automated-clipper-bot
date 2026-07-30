# Gemini dossier #4 — "50 battle-tested tools" master resource list, raw, as pasted by the user, true verbatim

**Status: reference only, not verified as a whole.** Saved in full per
explicit instruction ("ADD ALL OF THESE DONT SUMMARIZE").

**Note, 2026-07-30: this file was originally saved as a condensed
paraphrase instead of the exact original wording. Replaced here with the
true verbatim text, corrected after the user flagged that source material
should never be reworded on my own judgment, only recorded exactly as
given.**

Preceded by the user's framing: *"Here is a comprehensive master resource
list of 50 battle-tested tools, scripts, libraries, and architectural
designs gathered from open-source repositories, developer forums, and 'I
Built an AI Clipping Bot' creator guides across YouTube and GitHub.
These options are categorized to help you build, optimize, or scale a
stream-clipping machine (whether you're targeting bounty programs like
Lacy's or launching your own network)."*

---

Part 1: VOD & Chat Ingestion Utilities (Getting the Source Material)

twitchAPI (Python Wrapper) — Asynchronous library for interacting with Twitch Helix API and EventSub to fetch VOD metadata and stream start times.
yt-dlp — The gold-standard fork for downloading high-resolution VODs and highlights from Twitch and YouTube without getting rate-limited.
twitch-clip-archiver — Python utility that automatically sweeps a channel for new clips or VOD archives and queues them locally.
TwitchDownloader (CLI/GUI) — Open-source tool designed specifically for fast multithreaded downloading of Twitch VOD files and chat dumps.
streamlink — Extracts live streams and VODs straight to a local player or file stream for real-time segment capture.
chat-downloader — Python library to scrape live or VOD chat logs, letting your pipeline inspect viewer comments alongside video.
TwitchChatDownloader — Specifically outputs VOD chat logs into heavily structured JSON with precise timestamps for spike correlation.
Twitch-VOD-Downloader — Lightweight node/python script optimized for headless server execution during overnight processing.
Twitch-Helix-Scraper — Pulls top-performing streamer metrics to identify which broadcast blocks had the highest viewer retention.
Twitch-EventSub-Listener — Real-time webhook listener to trigger immediate clipping scripts the moment a stream ends or a big event occurs.
Part 2: Highlight & Spike Detection Engines (Finding the Viral Moments)

ClipsAI (Open-Source Library) — Python library that uses word-level transcripts and speaker diarization to find natural story breaks.  
whisperx — Fast automatic speech recognition with word-level timestamps, essential for precise subtitle alignment.  
ai-clipping-comfyui — ComfyUI node set bringing server-side Whisper and virality ranking into local visual workflows.  
OpenShorts Engine — Self-hosted open-source alternative to commercial AI clippers with zero setup Docker configurations.  
stream-clipper (Rust/Svelte) — Desktop utility combining audio track analysis and chat density spikes to auto-detect stream highlights.  
cut-the-crap — Uses FFmpeg audio silence/volume analysis to carve out dead air and uninteresting lobby waiting screens.
AI-auto-segment-edit-video-pipeline — Full pipeline using ASR, semantic LLM analysis, and smart video merging.  
Clip-Maker-Streamers — Open-source desktop app template built to slice horizontal stream VODs into viral short chunks.
AI-Clipping-Software — Repository implementing automated LLM clip selection and face tracking via .env configurations.
twitch-clip-miner — Automated script that watches specific streamer VODs and mines high-probability engagement windows.
Part 3: Video Assembly & Vertical Cropping (FFmpeg & OpenCV Power Tools)

Smart Face-Tracking Cropper (OpenCV) — Automatically detects the streamer's face-cam layout in a 16:9 frame and centers the 9:16 crop window on them.
FFmpeg Dynamic Scale & Pad — Core script command to pad horizontal gameplay with top/bottom blurred background layers instead of hard cropping.
ffsubsync — Automatically synchronizes subtitle SRT files with audio tracks using cross-correlation.
whisper-subtitles-generator — Generates styled, animated word-by-word karaoke captions directly onto vertical video outputs.
GPU-Accelerated NVENC Filter — Custom FFmpeg flags (-c:v h264_nvenc) to leverage NVIDIA GPUs for 10x faster short rendering.
Multi-Clip Stitcher — Combines multiple micro-highlights into a cohesive 60-second compilation video.
Overlay Frame Compositor — Applies custom border frames, channel watermarks, or community bounty branding during assembly.
Audio Normalization Filter (loudnorm) — FFmpeg filter ensuring all generated clips hit standard platform audio loudness levels (-14 LUFS).
Aspect Ratio Matrix Transformer — Dynamically outputs 9:16 (TikTok/Reels), 1:1 (Instagram Feed), and 16:9 (YouTube) from a single run.
Keyframe-Locked Trimming Utility — Prevents black frames or video stutter at cut boundaries by aligning -ss with video keyframes.
Part 4: Agent Orchestration & State Management

LangGraph State Machine (StateGraph) — Orchestrates multi-step clipping tasks (Ingest $\rightarrow$ Transcribe $\rightarrow$ Analyze $\rightarrow$ Render) with strict schema validation.
SqliteSaver Persistence Layer — Backs up agent workflow states to local disk or Google Drive, preventing data loss during long processing runs.
Pydantic Strict Response Schemas — Enforces JSON output guardrails so Gemini or local LLMs never return malformed clipping timestamps.
Dead-Letter Queue Handler — Automatically quarantines corrupted VOD files or failed renders into an error folder for debugging.
Non-Fatal API Retry Decorator — Implements exponential backoff to handle transient network hiccups or rate limits gracefully.
Streamlit Local Command Center — Provides a lightweight browser-based UI to trigger batch clipping runs and review outputs manually.
Dockerized Environment Containers — Dockerfile and docker-compose.yml packages containing pre-configured FFmpeg, Python dependencies, and system binaries.
Multi-Agent Supervisor Pattern — Central router node that delegates tasks between transcription, AI analysis, and rendering agents.
In-Memory Cache Manager — Caches VOD transcripts locally to avoid re-downloading or re-transcribing the same source video multiple times.
Automated Integration Test Suite — Runs self-diagnostic checks on generated output paths before marking a batch job as complete.
Part 5: Distribution, Bounties & Automation Hubs

Discord Webhook Notifier — Automatically posts generated clip previews and metadata logs directly into a private Discord channel or bounty submission room.
TikTok Content Posting API Integration — Python script utilizing official developer endpoints to auto-schedule vertical short uploads.
YouTube Data API v3 Shorts Publisher — Automatically uploads rendered 9:16 files with optimized titles, descriptions, and hashtags.
Instagram Graph API Reel Uploader — Publishes completed vertical videos directly to creator business accounts.
Google Drive Batch Exporter — Automatically syncs finished short clips to a shared cloud folder for easy team review or mobile downloading.
CSV Batch Manifest Reader — Reads a simple spreadsheet of VOD links and processes an entire creator backlog overnight.
Local Storage Database (sqlite3) — Tracks which VODs have already been processed to prevent duplicate clipping runs.
Telegram Bot Notification Alert — Sends instant push notifications and status updates to your phone when a batch finishes rendering.
Engagement Analytics Scraper — Tracks view velocity and retention metrics post-upload to feed back into prompt improvement loops.
Auto-Clean Temp File Manager — Purges raw multi-gigabyte VOD downloads automatically after clip extraction to save local hard drive space.

---

**Note on item "Engagement Analytics Scraper" (Part 5):** this is the
closest any dossier has come to directly naming the analytics-feedback-loop
concept the user originally flagged as missing — "feeds back into
prompt-improvement loops" is exactly the self-adjustment mechanism being
hunted for. No specific tool/repo is named though, just the concept — worth
treating as a design target to build, not an existing tool to adopt.
