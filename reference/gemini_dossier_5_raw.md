# Gemini dossier #5 — "Advanced Research Dossier: AI Clipping & Video Pipeline Architecture," raw, as pasted by the user

**Status: reference only, not verified as a whole.** Saved in full per
explicit instruction ("ADD ALL OF THESE DONT SUMMARIZE") — nothing below is
condensed or paraphrased from the original paste.

Preceded by the user's framing: *"This document serves as an extension to
our master reference, detailing specialized tools, state orchestration
models, and production tricks discovered across developer forums and
open-source GitHub repositories for automated stream clipping."*

---

## Category 1: Advanced VOD Ingestion & Event Triggers

1. Twitch EventSub Webhooks — official real-time protocol to trigger serverless scripts the exact moment a creator/moderator creates a custom stream marker.
2. `streamlink` CLI — captures live stream chunks directly to disk for real-time edge processing before a VOD is even finalized.
3. `twitchAPI` Python async library — checks streamer broadcast status, uptime, follower spikes asynchronously without blocking the main script loop.
4. `chat-downloader` JSON output parsing — dumps live/VOD chat logs into structured arrays to look for emoji floods (LUL, Kappa, PogChamp) as organic interest signals.

## Category 2: Smart Frame Analysis & Visual Detection

5. OpenCV Haar Cascades / DNN Face Detection — programmatically locates a streamer's physical face-cam inside a 16:9 gameplay stream.
6. Google MediaPipe Face Mesh — lightweight framework, tracks head movement, dynamically scales the vertical 9:16 crop window.
7. **Gemini 2.5 Flash Native Video Understanding** — passing raw stream segments directly into Gemini's multimodal endpoint to judge narrative coherence, hook strength, and emotional climax without parsing gigabytes of intermediate files.
8. YOLO Object Detection for Gaming — custom-trained models to detect specific game events (victory screens, elimination feeds, boss encounters) as automated cut markers.

## Category 3: FFmpeg Assembly & Subtitle Rendering Tricks

9. NVENC Hardware Acceleration (`-c:v h264_nvenc`) — offloads rendering from CPU to NVIDIA GPU, up to 10x faster vertical-short export.
10. Dynamic Stacked Layout Filtergraph — standard FFmpeg filter expression: gameplay on bottom half, blurred background center, face-cam cropped on top.
11. `ffsubsync` cross-correlation — automatically aligns auto-generated Whisper SRT timestamps with actual audio tracks, eliminates subtitle drift.
12. `loudnorm` audio normalization — FFmpeg audio filter ensuring generated shorts hit standard platform loudness (-14 LUFS), prevents clipping on upload.

## Category 4: State Management & Session Resilience

13. LangGraph `SqliteSaver` — replaces volatile in-memory storage (`MemorySaver`) so the clipping pipeline preserves state across restarts/long jobs.
14. Pydantic schema validation — enforces strict JSON data contracts from LLM outputs, so clipping timestamps (`start_time`, `end_time`) never contain invalid float types or markdown text.
15. Dead-Letter Queue (DLQ) architecture — isolates corrupted VOD downloads or failed render jobs into a quarantine folder for manual inspection instead of crashing the batch loop.
16. Idempotent SQLite tracking — logs processed VOD IDs locally, ensures the bot never duplicates work on server reboots.

---

**Assessment, same standing rule as every other dossier — reference only,
independently checked before use:**

- Items 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16 all describe real,
  well-known, already-verified libraries/techniques covered elsewhere in
  `verified_tools_catalog.md` (Twitch EventSub, streamlink, twitchAPI,
  chat-downloader, OpenCV, MediaPipe, NVENC, ffsubsync, LangGraph
  SqliteSaver/Pydantic/DLQ pattern — the last three are also already
  `pipeline.py`-proven patterns, see `SALVAGE_INVENTORY.md`). No new
  verification needed for these.
- **Item 7 (Gemini 2.5 Flash Native Video Understanding) and item 8 (YOLO
  for gaming event detection) are the two genuinely new, checkable claims**
  in this dossier — see verification pass.
