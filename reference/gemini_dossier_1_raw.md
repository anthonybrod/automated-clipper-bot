# Gemini dossier #1 — raw, as pasted by the user

**Status: reference only, not verified as a whole.** See
[`../research/tool_verification.md`](../research/tool_verification.md) for
the real, independently-checked status of every specific claim below, and
[`verified_tools_catalog.md`](verified_tools_catalog.md) for the
decision-ready summary. Saved here verbatim so the original claims are never
lost, per this project's "log/persist everything, don't let it live only in
chat" discipline.

Preceded by the user's framing: *"Based on a deep web scan of open-source
repositories, developer forums (like Reddit's r/Twitch and r/commandline),
and coding tutorials, here is a massive, heavily researched list of 50
concrete tools, GitHub repos, libraries, and frameworks you can use to build
an AI clipping bot."*

---

## Part 1: Complete "AI Clipping Bot" Open-Source Repositories

1. `Vijax0/ai-clip-creator` — full-stack app handling multi-hour Twitch VODs, NVIDIA GPU, AI highlight extraction.
2. `samyaksgupta/Clips` — local AI clipping tool, separates webcam from gameplay, face tracking, vertical 9:16 formatting, no watermarks.
3. `ContentAutomation/TwitchCompilationCreator` — scrapes Twitch clips, composites with logo overlays, normalizes audio, auto-uploads to YouTube.
4. `jamesbaughnd/twitch-clip-miner` — FFmpeg + AI, watches Twitch VODs, mines high-retention windows.
5. `porplax/auto-highlighter-py` — CLI tool shared on Reddit, auto-highlights/clips Twitch VODs based on chat density.
6. `TheDanniCraft/clipify` — Next.js/Drizzle ORM, auto-plays a streamer's best clips when AFK, heavy Twitch API integration.
7. `HA6Bots/Twitch-Clips-Compilation-Generator-TCCG-` — 3-part bot: collects clips, stitches together, preps for social media via VPS.
8. `offish/twitchtube` — highly starred Python bot, compiles most-viewed Twitch clips, uploads to YouTube via Selenium.
9. `pelledrijver/twitch-highlights` — OS-independent Python module, fetches trending clips via Twitch API, stitches by streamer name.
10. `Fittiboy/twitch-clip-archiver` — mass-downloading utility, scrapes a streamer's existing clips, backs up locally or to Google Drive.

## Part 2: VOD Ingestion, Chat Scrapers, and Downloaders

11. `yt-dlp` — downloads high-res Twitch VODs and YouTube videos, bypasses rate limits.
12. `twitchAPI` (`pyTwitchAPI`) — standard async Python wrapper for Twitch Helix API, VOD markers and chat streams.
13. `chat-downloader` — Python package, scrapes chat logs from Twitch VODs (for finding "LUL"/"POG" spam spikes).
14. `streamlink` — CLI utility, pipes Twitch live video streams into FFmpeg or a local file.
15. `TwitchChatDownloader` — outputs VOD chat logs into structured JSON with precise timestamps.
16. `CanadianZombies/download-twitch` — lightweight Python module, rips specific segments of a stream.
17. `IcePanorama/TwitchClipsDLer` — wrapper around `yt-dlp`, bulk-downloads hundreds of bounty clips fast.
18. `zigai/twitch-scraper` — scrapes metadata (viewer count spikes) to feed an AI decision engine.
19. Twitch EventSub Webhooks — official Twitch API architecture, triggers a serverless function the moment a streamer creates a manual marker.
20. `Thomrl/InstaGet` — rips media assets/thumbnails/clips across platforms for compilation pipelines.

## Part 3: Spike Detection & AI Analysis Tools

21. `openai/whisper` — foundational open-source ASR, generates transcripts from downloaded VOD audio.
22. `m-bain/whisperX` — optimized Whisper, word-level timestamps + speaker diarization.
23. `SYSTRAN/faster-whisper` — CTranslate2 Whisper implementation, up to 4x faster on local GPUs.
24. NLTK / VADER Sentiment Analysis — analyze chat logs to detect when chat turns highly emotional.
25. `cut-the-crap` (GitHub) — analyzes audio volume, chops out silent "dead air."
26. LangChain / LangGraph — orchestration framework, forces LLMs to validate narrative structure of a clip.
27. Pydantic — Python data validation, forces AI to return exact `start_time`/`end_time` floats.
28. Google Gemini Flash (1.5 / 2.5) — 1M+ token context window, passes a full 4-hour stream transcript in one prompt.
29. OpenCV (Haar Cascades/DNN) — detects where the streamer's face-cam is located in a 16:9 frame.
30. Google MediaPipe — advanced facial tracking, pans/crops the 9:16 vertical window to follow the streamer.

## Part 4: Video Processing & Rendering

31. FFmpeg — backbone of all open-source video bots: cropping, burning subtitles, hardware-accelerated rendering.
32. `ffmpeg-python` — Python wrapper, human-readable complex FFmpeg filtergraphs.
33. `auto-editor` — CLI app, automatically cuts out portions with no motion or audio.
34. `MoviePy` — programmatic video editing: text overlays, watermarks, simple transitions.
35. `ffsubsync` — automatically synchronizes out-of-sync subtitle text with the video's audio track.
36. `whisper-subtitles-generator` — takes Whisper output, renders stylized "Alex Hormozi style" animated captions.
37. FFmpeg `boxblur` + `scale` filters — take horizontal video, duplicate, blur background, unblurred video centered.
38. ImageMagick — required by MoviePy for text cards, bounty overlay graphics, split-screen borders.
39. NVENC (NVIDIA Hardware Encoding) — `-c:v h264_nvenc`, renders clips 10x faster via GPU.
40. `rembg` — automatically removes background behind a streamer's webcam without a green screen.

## Part 5: Bot Orchestration, Bounties, and Distribution

41. `discord.py` — auto-posts finished vertical videos into Discord bounty submission channels.
42. `python-telegram-bot` — push notifications when an 8-hour VOD finishes processing.
43. Google API Python Client (`youtube-data-api-v3`) — auto-uploads finished 9:16 files as unlisted YouTube Shorts.
44. `tiktok-api` / Playwright — headless browser automation to mimic a user uploading (official TikTok APIs restrictive).
45. `instagrapi` — unofficial Instagram API wrapper, auto-publish Reels.
46. Streamlit — quick local web UI, human previews AI's clip choices before rendering.
47. SQLite (`sqlite3`) — logs which VOD URLs already processed, avoids duplicate work on server restart.
48. Docker & `docker-compose` — packages Python scripts, FFmpeg binaries, API keys into one container for a VPS.
49. Celery / Redis — task queues, scale to processing 50 streamers at once, distribute rendering workload.
50. Google Drive API — auto-uploads finished `.mp4` clips to a shared cloud folder for editors/social managers.

---

Also pasted separately, same message thread: a link to
[Build a Node API + Twitch bot using the Copilot CLI](https://www.youtube.com/watch?v=XCVdnvBam6c)
— "walks through the developer workflow of constructing a functioning Twitch
bot and API endpoints from scratch using AI coding assistants." Confirmed
real by the tool-verification pass (matches the one YouTube devlog citation
across both dossiers that turned out to actually exist).
