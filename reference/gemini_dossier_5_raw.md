# Gemini dossier #5 — "Advanced Research Dossier: AI Clipping & Video Pipeline Architecture," raw, as pasted by the user, true verbatim

**Status: reference only, not verified as a whole.** Saved in full per
explicit instruction ("ADD ALL OF THESE DONT SUMMARIZE").

**Note, 2026-07-30: this file was originally saved as a condensed
paraphrase instead of the exact original wording. Replaced here with the
true verbatim text, corrected after the user flagged that source material
should never be reworded on my own judgment, only recorded exactly as
given.**

Preceded by the user's framing: *"This document serves as an extension to
our master reference, detailing specialized tools, state orchestration
models, and production tricks discovered across developer forums and
open-source GitHub repositories for automated stream clipping."*

---

Category 1: Advanced VOD Ingestion & Event Triggers
Twitch EventSub Webhooks — The official real-time protocol to trigger serverless scripts the exact moment a creator or moderator creates a custom stream marker.
streamlink CLI — Used for capturing live stream chunks directly to disk for real-time edge processing before a VOD is even finalized.
twitchAPI Python Async Library — Essential for checking streamer broadcast status, uptime, and follower spikes asynchronously without blocking your main script loop.
chat-downloader JSON Output Parsing — Method of dumping live or VOD chat logs into structured arrays to look for emoji floods (e.g., LUL, Kappa, PogChamp) as organic interest signals.
Category 2: Smart Frame Analysis & Visual Detection
OpenCV Haar Cascades / DNN Face Detection — Used to programmatically locate where a streamer's physical face-cam is positioned inside a 16:9 gameplay stream.
Google MediaPipe Face Mesh — Lightweight framework to track user head movement and scale the vertical 9:16 crop window dynamically.
Gemini 2.5 Flash Native Video Understanding — Passing raw stream segments directly into Gemini's multi-modal endpoint to judge narrative coherence, hook strength, and emotional climax without parsing gigabytes of intermediate files.
YOLO Object Detection for Gaming — Custom-trained models to detect specific game events (e.g., victory screens, elimination feeds, boss encounters) to use as automated cut markers.
Category 3: FFmpeg Assembly & Subtitle Rendering Tricks
NVENC Hardware Acceleration (-c:v h264_nvenc) — Offloads video rendering from the CPU to NVIDIA graphics cards, speeding up vertical short export times by up to 10x.
Dynamic Stacked Layout Filtergraph — Standard FFmpeg filter expression to place the gameplay on the bottom half, blurred background in the center, and the face-cam cropped on top.
ffsubsync Cross-Correlation — Automatically aligns auto-generated Whisper SRT subtitle timestamps with actual audio tracks to eliminate subtitle drift.
loudnorm Audio Normalization — FFmpeg audio filter that ensures all generated shorts hit standard platform loudness (-14 LUFS) to prevent audio clipping upon upload.
Category 4: State Management & Session Resilience
LangGraph SqliteSaver — Replaces volatile in-memory storage (MemorySaver) so your clipping pipeline preserves state across restarts or long processing jobs.
Pydantic Schema Validation — Enforces strict JSON data contracts from LLM outputs so clipping timestamps (start_time, end_time) never contain invalid float types or markdown text.
Dead-Letter Queue (DLQ) Architecture — Isolates corrupted VOD downloads or failed render jobs into a separate quarantine folder for manual inspection rather than crashing the batch loop.
Idempotent SQLite Tracking — Logs processed VOD IDs in a local database to ensure the bot never duplicates work on server reboots.

---

**Assessment, same standing rule as every other dossier — reference only,
independently checked before use:**

- Items 1-6 and 9-16 (everything except Gemini native video understanding
  and YOLO gaming detection) all describe real, well-known,
  already-verified libraries/techniques covered elsewhere in
  `verified_tools_catalog.md` (Twitch EventSub, streamlink, twitchAPI,
  chat-downloader, OpenCV, MediaPipe, NVENC, ffsubsync, LangGraph
  SqliteSaver/Pydantic/DLQ pattern — the last three are also already
  `pipeline.py`-proven patterns, see `SALVAGE_INVENTORY.md`). No new
  verification needed for these.
- **Gemini 2.5 Flash Native Video Understanding and YOLO Object Detection
  for Gaming are the two genuinely new, checkable claims** in this
  dossier — see `research/tool_verification.md` for the verification pass
  (both confirmed real: native video input is real per Google's own
  current API docs; a real project — `bendawg2010/Auto-clipper` — ships an
  actual fine-tuned YOLOv11n model for exactly this).
