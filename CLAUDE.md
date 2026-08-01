# Working on this repo

**Read [PROJECT.md](PROJECT.md) in full before making any claim about this
project's status, architecture, or backlog.** It is the single authoritative
reference. Chat history is not authoritative; PROJECT.md is. If something in
a conversation conflicts with PROJECT.md, PROJECT.md wins unless the code has
since changed (check the code, then update PROJECT.md — don't let it go stale).

Project in one line: **Automated Clipper Bot** — pulls the best clips from
Twitch VOD/streams, adds captions, produces YouTube Shorts + long-form
compilations, cross-posts. Separate project from `youtube-auto-videos`
(Parents Teach Kids), kept in its own folder/repo per explicit instruction,
but actively salvaging verified-working code/patterns from that project
where they fit — see PROJECT.md's Salvage Inventory.

Current state: pre-flight phase. No pipeline code has been written yet.
Before writing any real pipeline stage, prove out every hard dependency
(APIs, models, credentials, tools) the same way `validate_api_keys()` and
`discover_best_working_models()` did for the other project — catch failures
before they cost money or time, not after.

Any code, architecture, or "reference implementation" that arrives from an
external AI (labeled in PROJECT.md as "from Gemini" or similar) is treated as
inspiration only, never trusted or copied verbatim without independent
verification first — established project rule, since prior examples from
that source looked complete but had real bugs and unimplemented claims.

**Hard rule, before writing any new function/pattern: check internal
resources first, including the sister project.** In order: (1)
`SALVAGE_INVENTORY.md` and `reference/verified_tools_catalog.md` in this
repo, (2) `C:\Users\AwBro\Desktop\youtube auto videos\pipeline.py` (grep it
directly — 4,000+ lines of real, proven, bug-fixed code covering budget
enforcement, retry/dead-letter handling, model discovery, secret retrieval,
JSON repair, checkpointing), (3) the deep-dive docs under `reference/` for
techniques already extracted from real external repos. Only write new code
from scratch once all three have been checked and come up empty for the
specific problem at hand. Don't re-derive a similar-but-different version
of something that already works — port it directly. This was an explicit,
repeated user correction (2026-07-30), not a nice-to-have.

## Adopted rules (2026-08-01) — strict defaults, ask before straying

Resolved one at a time with the user against real Gemini-sourced planning
material, following an explicit process: nothing from Gemini becomes a rule
just because Gemini said it, even when it overlaps with something true —
only what the user explicitly confirms. Full resolution process and
reasoning: `reference/handoff_2026-08-01_evaluation.md`. Once adopted,
these are followed automatically; any real reason to deviate gets raised
with the user first, not silently decided.

1. **Reuse verified logic over re-deriving** (reconfirms the hard rule
   above, not new).
2. **Chat-spike detection defaults to Z≥2.5 chat-velocity statistics**
   combined with keyword/emote-density weighting — not raw keyword-
   occurrence counting alone as the primary trigger.
3. **AI judge/verification calls fail closed, scoped.** Hook-quality
   scoring, TOS/content checks, Ollama context-check: any exception or
   unparseable response = reject, never silently pass. Does **not** extend
   to pre-flight hard/soft checks or human-review-gate timeouts — those
   keep their own existing, separate logic.
4. **No synthesized-narration audio mixing.** This pipeline has no
   narration track (raw streamer audio is the source) — don't port the
   sibling project's Narration/Music/SFX mixing pattern here.
5. **Flaky third-party API wrapper calls (`chat-downloader` and similar) get
   Tenacity exponential backoff + jitter by default.**
6. **faster-whisper is the default/primary transcription engine.** WhisperX
   and Parakeet remain optional upgrade paths, never silently promoted to
   default.
7. **VOD-list caching**: content-hash keyed (skip re-querying Twitch if the
   source manifest is unchanged) plus persisted URL, title, and content
   notes per VOD — extend the real `pipeline_tasks`/`payout_logs` schema
   found in a `Lacy_Clip_Bot` Drive export (see the evaluation file), don't
   design a new one from scratch.
8. **MP4 exports always get `-movflags +faststart`.**
9. **Karaoke/animated captions always use `.ass` format with `\an5`
   centering** — never plain `.srt` for that use case.
10. **The user has final say before any phase transition, and before
    anything is marked complete or finished.** Report what was done and
    how it was tested — the "complete/finished" designation itself belongs
    to the user, never something declared unilaterally.
11. **Default to multiple parallel background agents for research/
    verification/mining work spanning multiple independent sources** — act
    as director/orchestrator (scope each agent tightly, synthesize what
    comes back), not as the one doing every read serially.
