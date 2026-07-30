# Gemini dossier #4 — "50 battle-tested tools" master resource list, raw, as pasted by the user

**Status: reference only, not verified as a whole.** Saved in full per
explicit instruction ("ADD ALL OF THESE DONT SUMMARIZE") — nothing below is
condensed or paraphrased from the original paste.

Preceded by the user's framing: *"Here is a comprehensive master resource
list of 50 battle-tested tools, scripts, libraries, and architectural
designs gathered from open-source repositories, developer forums, and 'I
Built an AI Clipping Bot' creator guides across YouTube and GitHub. These
options are categorized to help you build, optimize, or scale a
stream-clipping machine (whether you're targeting bounty programs like
Lacy's or launching your own network)."*

Note: many items in this dossier are generic technique/category names
("Smart Face-Tracking Cropper (OpenCV)") rather than specific `owner/repo`
claims, unlike dossiers 1-3. Only the specific-sounding named projects are
independently checkable; the rest are technique descriptions already
covered by real, confirmed libraries elsewhere in `verified_tools_catalog.md`.

---

## Part 1: VOD & Chat Ingestion Utilities (Getting the Source Material)

1. `twitchAPI` (Python Wrapper) — async library for Twitch Helix API + EventSub, fetches VOD metadata and stream start times.
2. `yt-dlp` — gold-standard fork for downloading high-res VODs/highlights from Twitch and YouTube without rate-limiting.
3. `twitch-clip-archiver` — Python utility, sweeps a channel for new clips/VOD archives, queues locally.
4. `TwitchDownloader` (CLI/GUI) — open-source tool for fast multithreaded downloading of Twitch VOD files and chat dumps.
5. `streamlink` — extracts live streams/VODs to a local player or file stream for real-time segment capture.
6. `chat-downloader` — Python library, scrapes live/VOD chat logs.
7. `TwitchChatDownloader` — outputs JSON chat history with precise timestamps for spike correlation.
8. `Twitch-VOD-Downloader` — lightweight node/python script optimized for headless server execution overnight.
9. `Twitch-Helix-Scraper` — pulls top-performing streamer metrics to identify highest-viewer-retention broadcast blocks.
10. `Twitch-EventSub-Listener` — real-time webhook listener, triggers immediate clipping scripts the moment a stream ends or a big event occurs.

## Part 2: Highlight & Spike Detection Engines (Finding the Viral Moments)

11. `ClipsAI` (open-source library) — Python library, word-level transcripts + speaker diarization, finds natural story breaks.
12. `whisperx` — fast ASR with word-level timestamps, precise subtitle alignment.
13. `ai-clipping-comfyui` — ComfyUI node set, server-side Whisper + virality ranking into local visual workflows.
14. `OpenShorts Engine` — self-hosted open-source alternative to commercial AI clippers, zero-setup Docker configs.
15. `stream-clipper` (Rust/Svelte) — desktop utility, audio track analysis + chat density spikes, auto-detects stream highlights.
16. `cut-the-crap` — FFmpeg audio silence/volume analysis, carves out dead air and lobby waiting screens.
17. `AI-auto-segment-edit-video-pipeline` — full pipeline: ASR, semantic LLM analysis, smart video merging.
18. `Clip-Maker-Streamers` — open-source desktop app template, slices horizontal stream VODs into viral short chunks.
19. `AI-Clipping-Software` — repo implementing automated LLM clip selection + face tracking via `.env` configs.
20. `twitch-clip-miner` — watches specific streamer VODs, mines high-probability engagement windows.

## Part 3: Video Assembly & Vertical Cropping (FFmpeg & OpenCV Power Tools)

21. Smart Face-Tracking Cropper (OpenCV) — detects streamer's face-cam layout in a 16:9 frame, centers the 9:16 crop window.
22. FFmpeg Dynamic Scale & Pad — pads horizontal gameplay with top/bottom blurred background layers instead of hard cropping.
23. `ffsubsync` — auto-synchronizes SRT subtitles with audio tracks via cross-correlation.
24. `whisper-subtitles-generator` — styled, animated word-by-word karaoke captions on vertical video.
25. GPU-Accelerated NVENC Filter — `-c:v h264_nvenc` for 10x faster short rendering via NVIDIA GPUs.
26. Multi-Clip Stitcher — combines multiple micro-highlights into a cohesive 60-second compilation.
27. Overlay Frame Compositor — applies custom border frames, watermarks, or bounty branding during assembly.
28. Audio Normalization Filter (`loudnorm`) — ensures generated clips hit standard platform loudness (-14 LUFS).
29. Aspect Ratio Matrix Transformer — dynamically outputs 9:16 (TikTok/Reels), 1:1 (Instagram Feed), 16:9 (YouTube) from one run.
30. Keyframe-Locked Trimming Utility — prevents black frames/stutter at cut boundaries by aligning `-ss` with keyframes.

## Part 4: Agent Orchestration & State Management

31. LangGraph State Machine (`StateGraph`) — orchestrates multi-step tasks (Ingest → Transcribe → Analyze → Render) with schema validation.
32. `SqliteSaver` persistence layer — backs up agent workflow state to disk/Google Drive, prevents data loss on long runs.
33. Pydantic strict response schemas — enforces JSON output guardrails so LLMs never return malformed clipping timestamps.
34. Dead-Letter Queue Handler — quarantines corrupted VODs or failed renders into an error folder.
35. Non-Fatal API Retry Decorator — exponential backoff for transient network hiccups/rate limits.
36. Streamlit Local Command Center — lightweight browser UI to trigger batch runs and review outputs manually.
37. Dockerized Environment Containers — Dockerfile + docker-compose.yml with pre-configured ffmpeg/Python/system binaries.
38. Multi-Agent Supervisor Pattern — central router node delegates tasks between transcription/analysis/rendering agents.
39. In-Memory Cache Manager — caches VOD transcripts locally, avoids re-downloading/re-transcribing the same source.
40. Automated Integration Test Suite — self-diagnostic checks on generated output paths before marking a batch job complete.

## Part 5: Distribution, Bounties & Automation Hubs

41. Discord Webhook Notifier — auto-posts clip previews/metadata into a private Discord channel or bounty submission room.
42. TikTok Content Posting API Integration — official developer endpoints, auto-schedules vertical short uploads.
43. YouTube Data API v3 Shorts Publisher — auto-uploads rendered 9:16 files with optimized titles/descriptions/hashtags.
44. Instagram Graph API Reel Uploader — publishes completed vertical videos to creator business accounts.
45. Google Drive Batch Exporter — auto-syncs finished shorts to a shared cloud folder for team review/mobile download.
46. CSV Batch Manifest Reader — reads a spreadsheet of VOD links, processes an entire creator backlog overnight.
47. Local Storage Database (`sqlite3`) — tracks which VODs already processed, prevents duplicate runs.
48. Telegram Bot Notification Alert — instant push notifications/status updates when a batch finishes rendering.
49. Engagement Analytics Scraper — tracks view velocity + retention metrics post-upload, feeds back into prompt-improvement loops.
50. Auto-Clean Temp File Manager — purges raw multi-gigabyte VOD downloads automatically after clip extraction.

**Note on item 49 (Engagement Analytics Scraper):** this is the closest any
dossier has come to directly naming the analytics-feedback-loop concept the
user originally flagged as missing — "feeds back into prompt-improvement
loops" is exactly the self-adjustment mechanism being hunted for. No
specific tool/repo is named though, just the concept — worth treating as a
design target to build, not an existing tool to adopt.
