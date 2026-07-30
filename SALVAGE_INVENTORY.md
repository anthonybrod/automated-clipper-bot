# Salvage inventory — verified-working code from `youtube-auto-videos`

Every item below was confirmed to exist at the stated location by directly
reading `pipeline.py` in the `youtube-auto-videos` repo on 2026-07-29 — not
recalled from memory. Re-verify against current `pipeline.py` before porting,
since that project is still actively changing.

Source repo: `C:\Users\AwBro\Desktop\youtube auto videos\pipeline.py`

## Directly portable (small, self-contained, no project-specific coupling)

| Function | Location | What it does | Why we need it here |
|---|---|---|---|
| `get_secret(key)` | `pipeline.py:74` | Reads `google.colab.userdata` first if running in Colab, falls back to `os.environ`. | Every credential (Google API key, Twitch Client ID/Secret) needs this exact pattern or we repeat the "key not found in Colab" bug already solved once. |
| `safe_json_parse(text, model=None)` | `pipeline.py:319` | Repairs/parses LLM JSON output (handles markdown fences, trailing commas, etc.) instead of a bare `json.loads`. | The Gemini reference script (`reference/gemini_suggestions.md`) crashes on exactly the malformed-JSON case this already fixes. |
| `_track_tokens(resp)` / `get_session_tokens()` | `pipeline.py:383` / `pipeline.py:389` | Accumulates real token usage from `usage_metadata` across a run. | Needed for real cost tracking from day one, not bolted on after an overspend like last time. |
| `_new_temp_path(suffix)` / `cleanup_temp_files()` | `pipeline.py:400` / `pipeline.py:405` | Temp-file hygiene for generated media. | Same need here — clips, cropped video, caption files. |

## Portable with adaptation (real pattern, needs a new schema/domain)

| Function | Location | Pattern to reuse | Adaptation needed |
|---|---|---|---|
| `call_gemini_inspector(...)` | `pipeline.py:736` | Real `response_schema=` passed into `generate_content` config for **server-side JSON schema enforcement** — not just `response_mime_type: application/json` (which the Gemini reference script uses alone, and which is the weaker option). Also shows the correct pattern for attaching image/audio `inline_data` parts alongside a prompt. | Replace `InspectorVerdict` schema with a `ClipTarget`-style Pydantic model (start_time, end_time, title, hook_reason, score) for judging VOD moments. |
| `get_working_model(capability, default)` / `discover_best_working_models(...)` | `pipeline.py:601` / `pipeline.py:674` | Tests real candidate models against the actual account/quota before committing to one, ranked pro > flash > lite, non-preview > preview, caches result to a JSON file. | Directly reusable concept for picking which Gemini model handles VOD-moment analysis — avoids repeating the `gemini-3-pro-image` zero-quota mistake. |
| `validate_api_keys()` | `pipeline.py:3888` | Pre-flight check that actually calls each API once before a real run starts, hard-blocks on failures that have no fallback, soft-warns on failures that do. | This is the direct model for `validate_environment.py` in this project — add a real Twitch Helix token-exchange test alongside the Gemini check. |
| Budget enforcement (`COST_PER_TOKEN`, `DEFAULT_BUDGET_LIMIT`, the check inside `cognitive_ai_supervisor`) | `pipeline.py:577`, `pipeline.py:585` | Compares real accumulated cost against a real limit *between* stages, hard-stops and writes a dead-letter entry rather than silently continuing. Known honest limitation: only checks between stages, not mid-stage. | Same mechanism, new per-unit cost model (VOD-analysis tokens + any paid transcription). Learned the hard way (a real $2.57 overspend) on the other project — build this in from day one here instead. |
| `_write_dead_letter(state)` + supervisor retry/dead-letter pattern | `pipeline.py:1633` | Shared helper for writing failed/exhausted-retry work to a queue file instead of losing it silently. | Reuse directly for VODs that fail moment-detection or fail QA repeatedly. |
| ffmpeg vertical-crop | `pipeline.py:3522` | `crop=ih*(9/16):ih,scale=1080:1920` then `-c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart`. Confirmed mathematically correct center-crop from 16:9 to 9:16. | Port the exact ffmpeg args; this is the same transform the Gemini reference script's `assemble_vertical_clip` was attempting, just already proven working here. |

## Conceptually relevant, not literally reusable

- **Asset-reuse/lock-once pattern** (see project memory `project_asset_reuse_strategy`): lock reference assets once, reuse across runs. Analogous idea here — cache a broadcaster's VOD list / already-scored clip metadata instead of re-querying/re-scoring on every run.
- **Rule-of-3 variant scoring** (`pipeline.py` search: `rule_of_three_variant_count`): generate N candidates, score them, pick the best or synthesize — could apply to clip-title/hook generation, not required for v1.

## Explicitly NOT salvaged (confirmed project-specific, no crossover)

- Anything under `RESEARCH TOOLS/` in the other repo (Master Voice Library, animation style refs) — those are Parents Teach Kids character/voice assets, unrelated to this project.
- `MentorScript` / `Scene` / child-character / mentor-persona logic — entirely specific to the kids'-education format.
