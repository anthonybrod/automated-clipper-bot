# Gemini reference dump — evaluated, not trusted

**Rule for this file and this category of material generally: content from an
external AI is reference/inspiration only. Never copy verbatim into the real
pipeline without independent verification.** Confirmed explicitly by the user
("GEMNI CODE IS ALWAYS BAD. WE JUST USE IT FOR REFERENCE") after this exact
dump was reviewed and found to have real bugs.

## What was useful (kept as inspiration)

- **4-component lean workflow shape**: Ingest & Metadata -> Spike Detection &
  Filtering -> Multimodal Quality Gate (LLM judges narrative
  completeness/hook strength, not just "is there motion") -> Assembly &
  Export. Reasonable shape, worth keeping as a starting skeleton.
- **Using engagement signals to narrow down WHERE to look** in a multi-hour
  VOD instead of transcribing/scanning the whole thing. Directionally right;
  the specific mechanism proposed (compute chat-velocity spikes ourselves)
  is the weakest part of this idea — see refinement below.
- Real, accurate context on the streamer clip-farming/bounty economy (Lacy,
  Discord submission channels, Whop Clipping, Biro) — corroborates and
  extends what turned up independently in our own YouTube research, no
  reason to doubt this part.
- The ffmpeg vertical-crop filter (`crop=ih*9/16:ih,scale=1080:1920`) is
  mathematically correct AND we already have this exact technique working in
  production — see `pipeline.py:3522` in the youtube-auto-videos repo. Don't
  write this from scratch; port it directly.

## Refinement over what Gemini proposed

Gemini's spike-detection plan requires us to separately collect Twitch chat
replay logs and compute message-velocity spikes ourselves — real extra
infrastructure Twitch's API doesn't hand you.

**Twitch's `Get Clips` Helix endpoint is simpler and likely better as a
primary signal**: it returns clips *viewers already created* from a
broadcaster's VODs, sorted by view count, for any date range — a free,
already-human-curated highlight detector, zero extra infrastructure, real
documented API. Worth using as the primary/first signal instead of building
chat-spike detection from scratch. (Needs a pre-flight check like everything
else — confirm this endpoint actually returns clips for a target
broadcaster/date-range before relying on it.)

## Real bugs found in the provided `twitch_clipper_agent.py`

1. **No Colab-secrets support.** `get_gemini_client()` only reads
   `os.environ.get("GOOGLE_API_KEY")`. Colab Secrets aren't exposed as OS
   env vars automatically — they need `google.colab.userdata.get()`. This
   would recreate the exact "key not found" problem already solved in
   `pipeline.py` via `get_secret()` (checks `google.colab.userdata` first,
   falls back to `os.environ`). Port `get_secret()` directly instead of
   rewriting this.
2. **`ClipTarget` Pydantic model is defined but never used.**
   `analyze_vod_for_clips` does raw `json.loads(response.text)` and returns
   plain dicts — no `response_schema=ClipTarget` passed to
   `generate_content`, no actual validation happening despite the model
   existing. `pipeline.py`'s `call_gemini_inspector` pattern
   (`pipeline.py:736`) already solves this correctly — passes a real Pydantic
   `response_schema` for server-side enforcement. Use that pattern, not this.
3. **No JSON-repair/defensive parsing.** A malformed/fenced response would
   crash `json.loads` outright. `pipeline.py`'s `safe_json_parse`
   (`pipeline.py:319`) already handles this (markdown fences, trailing
   commas, etc.) — reuse it.
4. **Claims to "burn in captions" but there is no caption-burning code
   anywhere in what was provided.** The docstring/comment oversells the
   function; `assemble_vertical_clip` only crops and scales.
5. **No actual VOD/transcript ingestion function exists.**
   `analyze_vod_for_clips(transcript_text)` takes transcript text as a
   parameter, but nothing in the script produces that transcript from a real
   Twitch VOD. The `__main__` block is a comment-stub, not a real entry
   point. This is a two-function skeleton, not the "complete pipeline" it
   was described as.

Net assessment: keep the architecture shape and the streamer-economy context;
do not port any of the actual code. Rebuild each piece using patterns already
proven out in `pipeline.py` (see `../SALVAGE_INVENTORY.md`).
