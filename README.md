# Automated Clipper Bot

Pulls the best clips from Twitch VODs/streams, adds captions, and produces
YouTube Shorts + long-form compilations, cross-posted to multiple
platforms. Built entirely on a $0, local-first, open-source stack —
no paid SaaS subscriptions in the pipeline itself.

> **Working on this project? Start with [`START_HERE.md`](START_HERE.md)** —
> the single session entry point: current state, the next action, blockers,
> open questions, and where everything lives. This README is the public
> front door; `START_HERE.md` is the working one. For a catalogue of every
> document in the repo and when to read it, see [`INDEX.md`](INDEX.md).

**Status: research phase. No pipeline code has been written yet — by
design.** As of 2026-08-04 the project has its **first measured detection
numbers** rather than generic advice: from 50 human-curated clip moments,
median clip length **39.5s** (78% fall in 20–70s), hook openings split
**36% direct question / 22% shouted name / 0% narration**, and a
**transcript-only detector** — verbal repetition in 22 of 50 moments — that
costs nothing per VOD and slots into the free pre-filter. Three findings
contradict the current architecture and are flagged rather than applied; see
[PROJECT.md](PROJECT.md) for all of it, and [INDEX.md](INDEX.md) for where
every document lives.

## Sources and destinations

**IN — clips are sourced from:**

| Platform | URL |
|---|---|
| **Twitch (primary, V1)** | https://www.twitch.tv/lacy/ — [VODs](https://www.twitch.tv/lacy/videos) · [clips 24h](https://www.twitch.tv/lacy/clips?range=24hr) · [clips 7d](https://www.twitch.tv/lacy/clips?range=7d) |
| Kick (secondary, sparse) | https://kick.com/lacy — [VODs](https://kick.com/lacy/videos) · [recent clips](https://kick.com/lacy/clips?sort=date&range=week) · [best clips](https://kick.com/lacy/clips?sort=view&range=week) |

**OUT — finished clips are posted to:**

| Platform | URL |
|---|---|
| X | https://x.com/CoreCrashOuts |
| YouTube | https://www.youtube.com/@CORECrashOUTS |

**Scope:** V1 sources from Lacy only, to prove the pipeline end to end.
V2 expands to the whole CORE group. Which platforms to publish to is still
an open research question — Stage 5 is deliberately built as a list of
targets behind one interface rather than hard-coded outlets.

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
