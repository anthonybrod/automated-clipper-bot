# Gemini dossier #2 — "Master Research Dossier," raw, as pasted by the user, true verbatim

**Status: reference only, not verified as a whole.** See
[`../research/tool_verification.md`](../research/tool_verification.md) for
the real, independently-checked status of every specific claim below, and
[`verified_tools_catalog.md`](verified_tools_catalog.md) for the
decision-ready summary.

**Note, 2026-07-30: this file was originally saved as a condensed
paraphrase instead of the exact original wording. Replaced here with the
true verbatim text, corrected after the user flagged that source material
should never be reworded on my own judgment, only recorded exactly as
given.**

**Verification findings, confirmed real 2026-07-30 (unchanged from before
this correction):** the Reddit threads (Category 2) came back 0/5
confirmable and the YouTube "devlog" videos (Category 3) came back only
1/10 confirmed real. Treat both categories as unverified-by-default.

---

Master Research Dossier: 50 Sources for AI Clipping Bots
Here are 50 concrete sources, repositories, video essays, and developer threads documenting how to build automated Twitch clipping bots and AI video pipelines.
Category 1: Open-Source GitHub Repositories (Full Bots & Pipelines)
HA6Bots/Twitch-Clips-Compilation-Generator-TCCG- - A 3-part system that collects clips automatically and puts them together into compilations. (https://github.com/HA6Bots/Twitch-Clips-Compilation-Generator-TCCG-)
Vijax0/AI-clip-creator - Application that automatically creates clips from videos, trained on 2,500+ videos. (https://github.com/Vijax0/AI-clip-creator)
Anil-matcha/ai-clipping-comfyui - Open-source ComfyUI nodes for clipping long-form videos into viral shorts using Whisper and face-tracking. (https://github.com/Anil-matcha/ai-clipping-comfyui)
SamurAIGPT/ai-clipping-generator - Next.js SaaS boilerplate that auto-extracts viral shorts, Reels, and TikToks. (https://github.com/SamurAIGPT/ai-clipping-generator)
jamesbaughnd/twitch-clip-miner - Python AI script that watches Twitch VODs and mines high-retention windows using FFmpeg. (https://github.com/jamesbaughnd/twitch-clip-miner)
pelledrijver/twitch-highlights - OS-independent module for creating highlight videos from trending Twitch clips. (https://github.com/pelledrijver/twitch-highlights)
BayoDev/Twitch-Best-Of - Automatically creates best-of videos of a channel/category without requiring API tokens. (https://github.com/BayoDev/Twitch-Best-Of)
CasperKristiansson/Twitch-Youtube-Auto-Uploader - Uploads the top Twitch clips to YouTube automatically using the v3 Data API. (https://github.com/CasperKristiansson/Twitch-Youtube-Auto-Uploader)
R3turn-Dev/TwitchClipDumper - Python tool to download all clips from a specific channel using authorization tokens. (https://github.com/R3turn-Dev/TwitchClipDumper)
camalot/chatbot-medaloverlay - Streamlabs chatbot script for auto-clipping and overlays. (https://github.com/camalot/chatbot-medaloverlay)
CanadianZombies/download-twitch - Downloads Twitch clips and embeds them into Discord webhooks automatically. (https://github.com/CanadianZombies/download-twitch)
zigai/twitch-scraper - Scrapes Twitch clip and profile metadata to track viral engagement numbers. (https://github.com/zigai/twitch-scraper)
patrickwjh/Streamheart - Intelligent modular streaming platform for IRL streams on Twitch. (https://github.com/patrickwjh/Streamheart)
IcePanorama/TwitchClipsDLer - Mass-downloading tool using yt-dlp to pull multiple clips at once. (https://github.com/IcePanorama/TwitchClipsDLer)
Fittiboy/twitch-clip-archiver - Python script to automatically archive a channel's clips to local storage. (https://github.com/Fittiboy/twitch-clip-archiver)
Category 2: Reddit & Developer Forum Discussions
r/Twitch: "We built a Twitch bot that clips your highlights while you're live" - Creator of Clipt.ai explaining their chat-reading logic. (https://www.reddit.com/r/Twitch/comments/1pjgwop/we_built_a_twitch_bot_that_clips_your_highlights/)
r/Python: "Created an application that can automatically create clips" - Developer breakdown of using local models to parse Twitch APIs. (https://www.reddit.com/r/Python/comments/1jicj6c/created_an_application_that_can_automatically/)
r/opensource: "Built an open-source AI video clipper to replace Opus/Munch" - Workflow discussion on replacing paid clipping SaaS with local Python APIs. (https://www.reddit.com/r/opensource/comments/1pw51w7/built_an_opensource_ai_video_clipper_to_replace/)
r/Twitch: "Automating clips from stream downloads" - Discussion on vertical layout scripting and generating captions. (https://www.reddit.com/r/Twitch/comments/1jw7cs0/automating_clips_from_stream_downloads/)
r/Twitch: "Auto clipping?" - Discussion on using Streamer.BOT with folder watch triggers to detect and crop clips locally. (https://www.reddit.com/r/Twitch/comments/1mvy0x8/auto_clipping/)
r/Twitch: "Using Twitch Chat to find highlights" - Thread debating how to parse chat velocity (LUL/Omg spam) to find timestamp markers.
r/Twitch: "Make clips with your voice - Just yell 'Clip That!'" - Scripting voice-activated timestamps into local VOD markers.
r/artificial: "AI Tools to making short clips automatically" - Deep dive into LLM context windows vs Video parsing.
r/youtubers: "I built an AI pipeline in n8n that makes full Reddit story videos" - Great cross-reference for automated assembly pipelines.
Twitch Developer Forums: "Best practices for Create Clip API" - Official dev forums on rate limits and webhook handling for CreateClip.
Category 3: YouTube Videos (Tutorials & "I Built X")
(Note: Search these exact titles on YouTube to find the specific devlog videos)
26. "I Built an AI Video Editor that Prints Money" by AI Jason - Breaks down using LLMs to scan transcripts for hooks.
27. "Build a Node API + Twitch bot using the Copilot CLI" by Cassidoo - Rapidly scaffolding a chat listener that triggers events.
28. "I Made a Python Bot That Auto-Uploads TikToks/Shorts" by CodeAesthetic / FireShip (similar topics) - Covers bypassing manual upload limits.
29. "How to Make a Twitch Chat Bot in Python 2023" - Standard boilerplate tutorial for connecting to Twitch IRC.
30. "Automating my Twitch stream with Python (Streamer.bot)" - Connecting local OBS replay buffers to Python scripts.
31. "I Built a Bot to Farm Twitch Clips" - Explores the API architecture of pulling from the top 100 streamers hourly.
32. "Turn Long Videos into Shorts AUTOMATICALLY with Python & OpenAI" - Tutorial on using Whisper and FFmpeg crop filters.
33. "Creating Viral Shorts with FFmpeg (Vertical Cropping Trick)" - Explains the crop=ih*9/16:ih command used in clip bots.
34. "How Streamers Farm Clips (The Meta Explained)" - Explains the business model behind Lacy and FaZe bounty Discords.
35. "Auto-Syncing Subtitles with Python & Whisper" - Tutorial on burning dynamic words onto vertical videos.
Category 4: The Core Stack (Libraries & Tools)
yt-dlp - The undisputed tool for downloading Twitch VODs programmatically. (https://github.com/yt-dlp/yt-dlp)
TwitchAPI (Python) - Asynchronous wrapper for Helix API (fetching VOD metadata). (https://github.com/Teekeks/pyTwitchAPI)
Twitch EventSub Webhooks - Twitch's official docs on real-time stream triggers. (https://dev.twitch.tv/docs/eventsub/)
Twitch Create Clip API - Official endpoint documentation for server-side clipping. (https://dev.twitch.tv/docs/api/reference/#create-clip)
Chat-Downloader - Python package to scrape Twitch VOD chat logs for spike analysis. (https://github.com/xenova/chat-downloader)
OpenAI Whisper - The foundation for transcribing VODs into text. (https://github.com/openai/whisper)
WhisperX - Advanced Whisper branch that provides exact word-level timestamps for captions. (https://github.com/m-bain/whisperX)
FFmpeg-Python - The wrapper used to write complex video cropping logic in Python. (https://github.com/kkroening/ffmpeg-python)
MoviePy - Simpler alternative to FFmpeg for adding text, watermarks, and concatenating clips. (https://github.com/Zulko/moviepy)
tmi.js - The standard Node.js library for connecting to Twitch chat for real-time spike detection. (https://github.com/tmijs/tmi.js)
Category 5: Automation & Distribution Integrations
Google API Python Client (YouTube v3) - Used to auto-upload the final clips as YouTube Shorts. (https://developers.google.com/youtube/v3)
tiktok-api (Unofficial Wrappers) - Because official TikTok APIs are restrictive, developers use these to upload. (https://github.com/davidteather/TikTok-Api)
Instagrapi - Unofficial Instagram API wrapper for publishing Reels automatically. (https://github.com/adw0rd/instagrapi)
Discord.py - Used to send the finished clips and status updates into your Clip Bounty Discord. (https://github.com/Rapptz/discord.py)
Celery / Redis - Task queuing libraries necessary if you scale the bot to process multiple streamers at once. (https://github.com/celery/celery)

---

**Real, project-relevant detail confirmed independently (not from this
dossier) while checking the Create Clip API item:** `POST /helix/clips`
(Create Clip) needs a **user** OAuth access token with the `clips:edit`
scope — not the simple Client ID + Secret `client_credentials` flow. See
PROJECT.md's "Open decisions" section.
