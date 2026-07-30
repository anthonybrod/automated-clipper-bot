# Gemini dossier #2 — "Master Research Dossier," raw, as pasted by the user

**Status: reference only, not verified as a whole.** See
[`../research/tool_verification.md`](../research/tool_verification.md) for
the real, independently-checked status of every specific claim below, and
[`verified_tools_catalog.md`](verified_tools_catalog.md) for the
decision-ready summary. Saved here verbatim so the original claims are never
lost.

**Important, confirmed finding from verification:** the Reddit threads
(Category 2) came back 0/5 confirmable and the YouTube "devlog" videos
(Category 3) came back only 1/10 confirmed real. Treat both categories as
unverified-by-default — they read as pattern-matched/invented, not
independently discovered sources, despite the "Master Research Dossier"
framing implying a real web scan.

---

## Category 1: Open-Source GitHub Repositories (Full Bots & Pipelines)

1. `HA6Bots/Twitch-Clips-Compilation-Generator-TCCG-` — https://github.com/HA6Bots/Twitch-Clips-Compilation-Generator-TCCG-
2. `Vijax0/AI-clip-creator` — https://github.com/Vijax0/AI-clip-creator (trained on 2,500+ videos, per claim)
3. `Anil-matcha/ai-clipping-comfyui` — https://github.com/Anil-matcha/ai-clipping-comfyui (ComfyUI nodes, Whisper + face-tracking)
4. `SamurAIGPT/ai-clipping-generator` — https://github.com/SamurAIGPT/ai-clipping-generator (Next.js SaaS boilerplate)
5. `jamesbaughnd/twitch-clip-miner` — https://github.com/jamesbaughnd/twitch-clip-miner
6. `pelledrijver/twitch-highlights` — https://github.com/pelledrijver/twitch-highlights
7. `BayoDev/Twitch-Best-Of` — https://github.com/BayoDev/Twitch-Best-Of (no API tokens required, per claim)
8. `CasperKristiansson/Twitch-Youtube-Auto-Uploader` — https://github.com/CasperKristiansson/Twitch-Youtube-Auto-Uploader (v3 Data API)
9. `R3turn-Dev/TwitchClipDumper` — https://github.com/R3turn-Dev/TwitchClipDumper
10. `camalot/chatbot-medaloverlay` — https://github.com/camalot/chatbot-medaloverlay (Streamlabs chatbot script)
11. `CanadianZombies/download-twitch` — https://github.com/CanadianZombies/download-twitch
12. `zigai/twitch-scraper` — https://github.com/zigai/twitch-scraper
13. `patrickwjh/Streamheart` — https://github.com/patrickwjh/Streamheart
14. `IcePanorama/TwitchClipsDLer` — https://github.com/IcePanorama/TwitchClipsDLer
15. `Fittiboy/twitch-clip-archiver` — https://github.com/Fittiboy/twitch-clip-archiver

## Category 2: Reddit & Developer Forum Discussions — VERIFICATION: 0/5 confirmed

16. r/Twitch: "We built a Twitch bot that clips your highlights while you're live" — https://www.reddit.com/r/Twitch/comments/1pjgwop/we_built_a_twitch_bot_that_clips_your_highlights/
17. r/Python: "Created an application that can automatically create clips" — https://www.reddit.com/r/Python/comments/1jicj6c/created_an_application_that_can_automatically/
18. r/opensource: "Built an open-source AI video clipper to replace Opus/Munch" — https://www.reddit.com/r/opensource/comments/1pw51w7/built_an_opensource_ai_video_clipper_to_replace/
19. r/Twitch: "Automating clips from stream downloads" — https://www.reddit.com/r/Twitch/comments/1jw7cs0/automating_clips_from_stream_downloads/
20. r/Twitch: "Auto clipping?" — https://www.reddit.com/r/Twitch/comments/1mvy0x8/auto_clipping/
21. r/Twitch: "Using Twitch Chat to find highlights" — no URL given.
22. r/Twitch: "Make clips with your voice - Just yell 'Clip That!'" — no URL given.
23. r/artificial: "AI Tools to making short clips automatically" — no URL given.
24. r/youtubers: "I built an AI pipeline in n8n that makes full Reddit story videos" — no URL given.
25. Twitch Developer Forums: "Best practices for Create Clip API" — no URL given.

## Category 3: YouTube Videos (Tutorials & "I Built X") — VERIFICATION: 1/10 confirmed

*Dossier's own note: "Search these exact titles on YouTube to find the specific devlog videos" — i.e. no direct URLs were given for any of these.*

26. "I Built an AI Video Editor that Prints Money" by AI Jason — **not confirmed**
27. "Build a Node API + Twitch bot using the Copilot CLI" by Cassidoo — **CONFIRMED**, matches https://www.youtube.com/watch?v=XCVdnvBam6c (a URL the user had already separately shared)
28. "I Made a Python Bot That Auto-Uploads TikToks/Shorts" by CodeAesthetic / FireShip (dossier's own hedge: "similar topics") — **not confirmed**
29. "How to Make a Twitch Chat Bot in Python 2023" — **not confirmed**
30. "Automating my Twitch stream with Python (Streamer.bot)" — **not confirmed**
31. "I Built a Bot to Farm Twitch Clips" — **not confirmed**
32. "Turn Long Videos into Shorts AUTOMATICALLY with Python & OpenAI" — **not confirmed**
33. "Creating Viral Shorts with FFmpeg (Vertical Cropping Trick)" — **not confirmed**
34. "How Streamers Farm Clips (The Meta Explained)" — **not confirmed**
35. "Auto-Syncing Subtitles with Python & Whisper" — **not confirmed**

## Category 4: The Core Stack (Libraries & Tools)

36. `yt-dlp` — https://github.com/yt-dlp/yt-dlp
37. `TwitchAPI` (Python) — https://github.com/Teekeks/pyTwitchAPI
38. Twitch EventSub Webhooks — https://dev.twitch.tv/docs/eventsub/ (confirmed real, loads fine)
39. Twitch Create Clip API — https://dev.twitch.tv/docs/api/reference/#create-clip (confirmed real, loads fine — see note below)
40. `Chat-Downloader` — https://github.com/xenova/chat-downloader
41. OpenAI Whisper — https://github.com/openai/whisper
42. WhisperX — https://github.com/m-bain/whisperX
43. FFmpeg-Python — https://github.com/kkroening/ffmpeg-python
44. MoviePy — https://github.com/Zulko/moviepy
45. `tmi.js` — https://github.com/tmijs/tmi.js

## Category 5: Automation & Distribution Integrations

46. Google API Python Client (YouTube v3) — https://developers.google.com/youtube/v3
47. `tiktok-api` (unofficial) — https://github.com/davidteather/TikTok-Api
48. Instagrapi — https://github.com/adw0rd/instagrapi (note: repo has since moved to `subzeroid/instagrapi`)
49. Discord.py — https://github.com/Rapptz/discord.py
50. Celery / Redis — https://github.com/celery/celery

---

**Real, project-relevant detail confirmed independently (not from this
dossier) while checking item 39:** `POST /helix/clips` (Create Clip) needs a
**user** OAuth access token with the `clips:edit` scope — not the simple
Client ID + Secret `client_credentials` flow. See PROJECT.md's "Open
decisions" section.
