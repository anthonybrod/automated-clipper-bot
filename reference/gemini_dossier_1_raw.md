# Gemini dossier #1 — raw, as pasted by the user, true verbatim

**Status: reference only, not verified as a whole.** See
[`../research/tool_verification.md`](../research/tool_verification.md) for
the real, independently-checked status of every specific claim below, and
[`verified_tools_catalog.md`](verified_tools_catalog.md) for the
decision-ready summary.

**Note, 2026-07-30: this file was originally saved as a condensed
paraphrase (shortened bullet phrasing) instead of the exact original
wording. Replaced here with the true verbatim text of what the user
pasted, corrected after the user flagged that source material should never
be reworded on my own judgment, only recorded exactly as given.**

The user's preceding message: *"Based on a deep web scan of open-source
repositories, developer forums (like Reddit's r/Twitch and r/commandline),
and coding tutorials, here is a massive, heavily researched list of 50
concrete tools, GitHub repos, libraries, and frameworks you can use to build
an AI clipping bot.*

*These represent the actual tech stack used by creators who post "I built
an AI clipping bot" videos, broken down by how they fit into the pipeline
we designed in `twitch_clipper_agent.py`."*

---

Part 1: Complete "AI Clipping Bot" Open-Source Repositories
These are fully built, open-source clipping engines you can fork or study to see exactly how others are solving this problem on GitHub:

1. `Vijax0/ai-clip-creator`: A popular full-stack app on GitHub that handles multi-hour Twitch VODs, runs locally on NVIDIA GPUs, and uses AI to extract highlights.
2. `samyaksgupta/Clips`: An open-source local AI clipping tool built specifically to separate webcam feeds from gameplay, track faces, and format vertical 9:16 shorts without watermarks.
3. `ContentAutomation/TwitchCompilationCreator`: A fully automated Python system that scrapes Twitch clips, composites them with logo overlays, normalizes audio, and auto-uploads to YouTube.
4. `jamesbaughnd/twitch-clip-miner`: A Python script leveraging FFmpeg and AI to watch Twitch VODs and specifically mine for high-retention windows.
5. `porplax/auto-highlighter-py`: A CLI tool actively shared on Reddit built for live streamers to automatically highlight and clip Twitch VODs based on chat density.
6. `TheDanniCraft/clipify`: A Next.js/Drizzle ORM tool that auto-plays a streamer's best clips when they go AFK, with heavy Twitch API integration.
7. `HA6Bots/Twitch-Clips-Compilation-Generator-TCCG-`: A 3-part bot system that collects clips automatically, stitches them together, and prepares them for social media via VPS.
8. `offish/twitchtube`: A highly starred Python bot that automatically makes compilations of the most-viewed Twitch clips and uploads them to YouTube using Selenium.
9. `pelledrijver/twitch-highlights`: An OS-independent Python module designed to fetch trending clips via the Twitch API and stitch them based on streamer names.
10. `Fittiboy/twitch-clip-archiver`: A mass-downloading utility to scrape a streamer's existing clips and back them up locally or to Google Drive.

Part 2: VOD Ingestion, Chat Scrapers, and Downloaders

11. `yt-dlp`: The undisputed open-source king for downloading high-res Twitch VODs and YouTube videos bypassing rate limits.
12. `twitchAPI` (`pyTwitchAPI`): The standard async Python wrapper for the Twitch Helix API to get VOD markers and chat streams.
13. `chat-downloader`: A Python package to scrape chat logs from Twitch VODs. You parse this data to find "LUL" or "POG" spam spikes.
14. `streamlink`: A CLI utility that pipes Twitch live video streams directly into FFmpeg or a local file for real-time capture.
15. `TwitchChatDownloader`: Specifically outputs VOD chat logs into heavily structured JSON with precise timestamps.
16. `CanadianZombies/download-twitch`: A lightweight Python module for ripping specific segments of a stream rather than the full 8-hour VOD.
17. `IcePanorama/TwitchClipsDLer`: A wrapper around `yt-dlp` that makes bulk-downloading hundreds of bounty clips at once incredibly fast.
18. `zigai/twitch-scraper`: A targeted tool to scrape metadata (viewer count spikes) to feed into your AI decision engine.
19. Twitch EventSub Webhooks: The official Twitch API architecture used to trigger a serverless function the exact moment a streamer creates a manual marker.
20. `Thomrl/InstaGet`: Open-source script to rip media assets, thumbnails, and clips across platforms for compilation pipelines.

Part 3: Spike Detection & AI Analysis Tools

21. `openai/whisper`: The foundational open-source ASR (Automatic Speech Recognition) model used to generate transcripts from the downloaded VOD audio.
22. `m-bain/whisperX`: A heavily optimized version of Whisper that provides word-level timestamps and speaker diarization (knowing who is speaking), crucial for dynamic captions.
23. `SYSTRAN/faster-whisper`: The CTranslate2 implementation of Whisper that runs up to 4x faster on local GPUs, saving massive compute time on long VODs.
24. NLTK / VADER Sentiment Analysis: Python libraries used to analyze the downloaded chat logs to automatically detect when the chat turns highly emotional (hype, anger, laughs).
25. `cut-the-crap` (GitHub): An open-source tool that analyzes audio volume in video files and automatically chops out all the silent "dead air."
26. LangChain / LangGraph: The orchestration framework (which we used in your pipeline) for forcing LLMs (like Gemini or Claude) to validate the narrative structure of a clip.
27. Pydantic: The Python data validation library used to force the AI to return exact `start_time` and `end_time` floats instead of conversational text.
28. Google Gemini Flash (1.5 / 2.5): With its massive 1M+ token context window, it is currently the industry favorite for passing a full 4-hour stream transcript in a single prompt.
29. OpenCV (Haar Cascades/DNN): Computer vision library used in Python to detect where the streamer's face-cam is located in a 16:9 frame.
30. Google MediaPipe: Used for advanced facial tracking to actively pan and crop the 9:16 vertical window to follow the streamer if they move around their room.

Part 4: Video Processing & Rendering

31. FFmpeg: The undisputed backbone of all open-source video bots. Used for cropping, burning subtitles, and hardware-accelerated rendering.
32. `ffmpeg-python`: The Python wrapper that makes writing complex FFmpeg filtergraphs (like stacking gameplay under a face-cam) human-readable in your script.
33. `auto-editor`: A command-line app that analyzes a video and automatically cuts out portions where there is no motion or audio.
34. `MoviePy`: A Python module for programmatic video editing, great for adding text overlays, watermarks, or simple transitions without complex FFmpeg math.
35. `ffsubsync`: Automatically synchronizes out-of-sync subtitle text with the video's audio track using cross-correlation logic.
36. `whisper-subtitles-generator`: An open-source tool that takes Whisper output and renders stylized, animated "Alex Hormozi style" captions.
37. FFmpeg `boxblur` + `scale` filters: The open-source command string to take a horizontal video, duplicate it, blur the background, and lay the unblurred video in the center.
38. ImageMagick: Required by MoviePy to dynamically generate text cards, bounty overlay graphics, and split-screen borders programmatically.
39. NVENC (NVIDIA Hardware Encoding): Appending `-c:v h264_nvenc` to your pipeline's FFmpeg commands to render clips 10x faster using your GPU.
40. `rembg`: An open-source Python tool to automatically remove the background behind a streamer's webcam without a green screen.

Part 5: Bot Orchestration, Bounties, and Distribution

41. `discord.py`: The standard library used to make your clipping bot auto-post the finished vertical videos into your specific Discord bounty submission channels.
42. `python-telegram-bot`: Used to push notifications to your phone when a massive 8-hour VOD finishes processing and the clips are ready.
43. Google API Python Client (`youtube-data-api-v3`): Used to auto-upload the finished 9:16 files directly as unlisted YouTube Shorts.
44. `tiktok-api` / Playwright: Because official TikTok APIs are restrictive, developers use headless browser automation (Playwright/Selenium) to mimic a user uploading a video.
45. `instagrapi`: An unofficial open-source Instagram API wrapper used to automatically publish Reels.
46. Streamlit: Used (as in your previous architecture) to spin up a quick local web UI so a human can preview the AI's clip choices before rendering them.
47. SQLite (`sqlite3`): The built-in Python database used to log which VOD URLs have already been processed so your bot doesn't duplicate work on a server restart.
48. Docker & `docker-compose`: How top bot creators package their Python scripts, FFmpeg binaries, and API keys into a single container so it runs flawlessly on any VPS.
49. Celery / Redis: Open-source task queues used if you scale your bot to process 50 different streamers at once, distributing the rendering workload.
50. Google Drive API: Python scripts to automatically upload the finished `.mp4` clips to a shared cloud folder where video editors or social media managers can grab them.

[Build a Node API + Twitch bot using the Copilot CLI](https://www.youtube.com/watch?v=XCVdnvBam6c)
This tutorial walks through the developer workflow of constructing a functioning Twitch bot and API endpoints from scratch using AI coding assistants.
