# Automated Clipper Bot

Pulls the best clips from Twitch VODs/streams, adds captions, and produces
YouTube Shorts + long-form compilations, cross-posted to multiple
platforms. Built entirely on a $0, local-first, open-source stack —
no paid SaaS subscriptions in the pipeline itself.

> **Working on this project? Start with [`START_HERE.md`](START_HERE.md)** —
> the single session entry point: current state, the next action, blockers,
> open questions, and where everything lives. This README is the public
> front door; `START_HERE.md` is the working one.

**Status: pre-flight / research phase. No pipeline code has been written
yet — by design.** The project's own discipline is to prove out every hard
dependency (APIs, models, credentials, tools) before writing a real
pipeline stage, the same way this repo's `validate_environment.py` checks
things before anything real runs. See [PROJECT.md](PROJECT.md) for the
full, authoritative status, architecture, and backlog — this file is a
short front door, not a duplicate of it.

## What this is

A separate project from this author's other automation work, built
specifically around Twitch clip harvesting: detect the best moments in a
stream (statistically, not just by watching everything), transcribe and
caption them locally, cut them to the right format per platform, and get
them published — with a human approval step in the loop, not a fully
unsupervised bot.

## The $0 stack

| Stage | Tool |
|---|---|
| Stream/VOD ingestion | [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) |
| Transcription | [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) (local, CTranslate2 INT8) |
| Highlight detection | statistical pre-filter (chat velocity Z-score, audio-RMS spikes) → cheap LLM score → expensive LLM detail |
| Timestamp correction | `snap_clip_to_words()` (ported technique — LLM-proposed cut points get snapped onto real word-boundary timestamps) |
| Video assembly | `ffmpeg` |
| Local LLM judging | [Ollama](https://ollama.com) (Llama 3.2) |
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) + `AsyncSqliteSaver` |

Full architecture, with sourcing/verification for every choice above, is
in [PROJECT.md](PROJECT.md#architecture-outline-2026-07-29-cost-philosophy-added-2026-07-30).

## Repo layout

- [`PROJECT.md`](PROJECT.md) — single source of truth: status, architecture,
  backlog. Read this in full before making any claim about the project.
- [`CLAUDE.md`](CLAUDE.md) — working rules for anyone (human or AI)
  contributing to this repo, including 20 adopted operating rules.
- [`SALVAGE_INVENTORY.md`](SALVAGE_INVENTORY.md) — verified-working
  functions/patterns ported from a sibling project's production pipeline,
  each confirmed to actually exist at the stated location before being
  listed here.
- [`validate_environment.py`](validate_environment.py) — pre-flight checks
  (ffmpeg, API keys, Twitch credentials) that must pass before any real
  pipeline code runs.
- `reference/` — source material: research dossiers, verified tool
  catalogs, and (as of 2026-08-01) verbatim handoff documents kept
  separate from their own evaluation, so raw source and analysis never
  blend into each other.
- `research/` — full transcripts and independent re-reads of the video
  research this architecture is grounded in.

## Getting started

This project is designed to run in a Google Colab notebook (mount Drive,
clone this repo, run `validate_environment.py`). You'll need:

- A Google API key (`GOOGLE_API_KEY`) with Gemini access.
- A Twitch Developer Console app (`TWITCH_CLIENT_ID` / `TWITCH_CLIENT_SECRET`) —
  create one at [dev.twitch.tv/console](https://dev.twitch.tv/console).
- `ffmpeg` (auto-installed in Colab; install locally otherwise).

Set the credentials as Colab secrets (or environment variables) under
those exact names, then run:

```bash
python validate_environment.py
```

It will report PASS/FAIL/WARN for each dependency before anything else
runs — nothing in this pipeline is meant to fail expensively mid-run
because a credential was missing.
