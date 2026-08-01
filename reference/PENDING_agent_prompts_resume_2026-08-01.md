# PENDING — resume here (plan revised, 1 of 12 done)

## READ THIS FIRST — status as of end of session 2026-08-01

**The 3 original broad-scope agents produced ZERO output.** Launched
~19:14-19:15, confirmed via `SendMessage` to have been stopped, and a full
search of the session temp directory found no partial transcript for any
of them. ~48 minutes and ~$15 for nothing. Real, unrecovered lost work.

**The approach was then redesigned so that can't repeat**, and the new
approach is **proven working** — don't re-litigate it, just continue it:

- **Split 3 broad agents → 12 small ones**, one source file each. Smaller
  scope = faster completion = less lost if one dies.
- **Check before saving**: verify the report's specific claims against the
  real source file (grep for distinctive quoted strings/hashes/numbers) to
  confirm it isn't fabricated, before it counts as done.
- **Save + commit + push per item**, immediately. Never batch, never wait
  for a whole wave to finish.

**Result of the first item (proof the loop works):** commit `7e009fb` —
`reference/mining_2026-08-01_deep_dive_moment_detection_VERBATIM.md`.
~7.5 minutes, 9/9 verification spot-checks passed, 39 portable code items
/ 11 fixable-code items / 23 free tools / 20 efficiency paths / 28
corrections. Compare to 48 minutes and nothing.

### Progress: 1 of 12 complete

| # | Source file | Status |
|---|---|---|
| 1 | `deep_dive_moment_detection.md` | ✅ DONE — commit `7e009fb` |
| 2 | `deep_dive_ingestion_and_pipelines.md` | ⬜ pending |
| 3 | `verified_tools_catalog.md` | ⬜ pending |
| 4 | `gemini_suggestions.md` | ⬜ pending |
| 5 | `gemini_dossier_1_raw.md` | ⬜ pending |
| 6 | `gemini_dossier_2_raw.md` | ⬜ pending |
| 7 | `gemini_dossier_4_raw.md` | ⬜ pending |
| 8 | `gemini_dossier_5_raw.md` | ⬜ pending |
| 9 | `gemini_dossier_6_raw.md` | ⬜ pending |
| 10 | `RESEARCH_YOUTUBE_SOURCES.md` + `tool_verification.md` (together) | ⬜ pending |
| 11 | `fresh_pass_videos_1-9.md` | ⬜ pending |
| 12 | `fresh_pass_videos_10-17.md` | ⬜ pending |

**Skip `gemini_dossier_3_raw.md` entirely** — confirmed fabricated by a
prior AI session, excluded from this project's trusted material.

Files 1-4 live in `AI\automated clipper bot\sample reference\`; files 5-9
also in `sample reference\`; files 10-12 in `sample research\`.

### The per-file prompt template (use this for items 2-12)

Take the appropriate original prompt from the section below and adapt it
to a **single file**, keeping all 5 extraction lenses (A-E) and all the
critical requirements intact. The exact wording that produced the
successful item 1 report:

> You're doing a focused mining pass on ONE already-verified research
> document for a Twitch clip-bot project (`automated clipper bot`,
> targeting streamer @LacyCrashOuts). This doc was produced by a careful
> earlier research phase and is considered trustworthy. Your job is to
> re-read it closely through a specific lens, because a first pass tends
> to compress/miss real value — this exact failure mode is documented in
> this project's own history (`C:\Users\AwBro\Desktop\AI\claude_failure_report.md`
> §10: "a genuine full re-read of the source file... later found 30
> additional reusable patterns... missing from the document entirely" —
> don't repeat that by skimming).
>
> **Read this ONE file in full, end to end, not skimmed:**
> `<FULL PATH TO THE ONE FILE>`
>
> Extract and report under these 5 headings (skip a heading if genuinely
> nothing qualifies — don't pad):
>
> **A. Complete/portable code or config** — anything ready to use close to
> as-is (a real function, a real ffmpeg command, a real config pattern, a
> real algorithm with concrete parameters), with the exact section heading
> or a short exact quote to grep for so it can be found again.
> **B. Fixable code** — something close but broken/incomplete/buggy as
> documented, worth starting from rather than writing fresh, noting exactly
> what's wrong with it.
> **C. Free/unutilized tools** — any tool mentioned as available, real, and
> free that ISN'T already the chosen primary pick for its pipeline stage
> (secondary/backup/alternative options, or things noted as "not currently
> used" or "worth reconsidering"). Include the real URL if the doc has one.
> **D. Efficiency paths** — anything that saves real cost/time/API
> budget/compute (a pre-filter that avoids paid calls, a caching technique,
> a faster library, a batching approach).
> **E. Anything that materially changes or adds to what's already believed
> true** — a correction, a caveat, a gotcha, a real bug found in a
> third-party tool, a number/threshold with real justification behind it.
>
> **Critical requirements:**
> - For EVERY item: cite the exact section heading or a short exact quote
>   to grep for, plus any URL the doc provides, plus a detailed note on HOW
>   it helps this project or could help. The user's stated purpose: "We will
>   often go back before major setbacks and changes and reference the info
>   we have here today. So make detailed notes of that and how to go back
>   and find each item with urls and detailed notes about how it helps us
>   or could help."
> - Be exhaustive and specific, not a highlights reel. This report becomes
>   a permanent reference index saved to the project repo.
> - Do NOT condense, summarize, use placeholders, or infer. Quote real
>   content directly where it matters.
> - If something genuinely has nothing new beyond the obvious, say so
>   plainly rather than manufacturing filler.
>
> Your final message IS the report — it will be saved verbatim to the
> project repo, so write it as a finished document, not as a message to a
> person.

---

## The original 3 broad prompts (kept for reference / scope fidelity)

Preserved unchanged so the *scope* of what was originally asked for stays
verifiable. Use the per-file template above for actual execution — these
3 are the record of the original request, not the execution plan anymore.

---

## Agent 1 — mine the 3 verified reference docs

```
You're doing a second-pass mining exercise on already-verified research documents for a Twitch clip-bot project (`automated clipper bot`, targeting streamer @LacyCrashOuts). This is NOT a first read — these docs were already produced by a careful research phase and are considered trustworthy (unlike raw Gemini output elsewhere in this project, which needs independent verification). Your job is to re-read them closely through a specific lens the user just asked for, because a first pass tends to compress/miss real value — this exact failure mode is documented in this project's own history (`C:\Users\AwBro\Desktop\AI\claude_failure_report.md` §10: "a genuine full re-read of the source file... later found 30 additional reusable patterns... missing from the document entirely" — don't repeat that by skimming).

Read these 4 files in full, end to end, not skimmed:
1. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\deep_dive_moment_detection.md`
2. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\deep_dive_ingestion_and_pipelines.md`
3. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\verified_tools_catalog.md`
4. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\gemini_suggestions.md`

For each, extract and report under these 5 headings (skip a heading for a file if genuinely nothing qualifies — don't pad):

**A. Complete/portable code or config** — anything you find that's ready to use close to as-is (a real function, a real ffmpeg command, a real config pattern), with exact file name + section/line so it can be found again.
**B. Fixable code** — something close but broken/incomplete/buggy as documented, worth starting from rather than writing fresh, noting what's wrong with it.
**C. Free/unutilized tools** — any tool mentioned as available, real, and free that ISN'T already the chosen primary pick for its pipeline stage (secondary/backup/alternative options, or things noted as "not currently used" or "worth reconsidering").
**D. Efficiency paths** — anything that saves real cost/time/API budget/compute (e.g. a pre-filter that avoids paid calls, a caching technique, a faster library, a way to batch things).
**E. Anything that materially changes or adds to what's already believed true** — a correction, a caveat, a gotcha, a real bug in a third-party tool, a number/threshold with real justification.

For every item, cite the exact source file and enough location detail (section heading, or a short exact quote to grep for) that someone could navigate straight back to it. This report needs to function as a real index, not a vague summary — be specific and exhaustive rather than picking a few highlights. If a whole file turns out to have nothing new beyond what's already well-known/obvious, say so plainly rather than manufacturing filler.
```

## Agent 2 — mine the 5 trustworthy Gemini dossiers + research index

```
You're doing a second-pass mining exercise on Gemini-sourced research dossiers for a Twitch clip-bot project (`automated clipper bot`, targeting streamer @LacyCrashOuts). These are raw external-AI output already independently fact-checked once (see `tool_verification.md` in the same folder) — treat named tools/repos as needing verification if you're unsure, but the main task here isn't re-verifying, it's mining for value a first read may have compressed away. This exact failure mode is documented in this project's own history (`C:\Users\AwBro\Desktop\AI\claude_failure_report.md` §10: "a genuine full re-read... later found 30 additional reusable patterns... missing from the document entirely" — don't repeat that by skimming).

Read these files in full, end to end:
1. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\gemini_dossier_1_raw.md`
2. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\gemini_dossier_2_raw.md`
3. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\gemini_dossier_4_raw.md`
4. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\gemini_dossier_5_raw.md`
5. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\gemini_dossier_6_raw.md`
6. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample research\RESEARCH_YOUTUBE_SOURCES.md`
7. `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample research\tool_verification.md`

**Skip `gemini_dossier_3_raw.md` entirely if you see it — it's confirmed fabricated (invented by a prior AI session, not real Gemini output) and excluded from this project's trusted material.**

For each file, extract and report under these 5 headings (skip a heading if nothing qualifies — don't pad):

**A. Complete/portable code or config** — ready-to-use as-is, with exact file + location so it can be found again.
**B. Fixable code** — close but broken/incomplete, worth starting from, noting what's wrong.
**C. Free/unutilized tools** — real, free tools mentioned that aren't already the chosen primary for their pipeline stage — secondary/backup/alternative options worth reconsidering.
**D. Efficiency paths** — anything saving real cost/time/API budget/compute.
**E. Corrections/gotchas** — anything that changes or adds nuance to what's already believed true.

Cite the exact source file and enough location detail (section heading or a short exact quote to grep for) that someone could navigate straight back to it. This needs to function as a real index — be specific and exhaustive, not a highlights reel. If a file has nothing new beyond what's already obvious/known, say so plainly.
```

## Agent 3 — mine the 17-video fresh-pass research (likely the richest of the three)

```
You're doing a second-pass mining exercise on this project's most exhaustive research documents. Some context: `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample research\fresh_pass_videos_1-9.md` and `fresh_pass_videos_10-17.md` were themselves ALREADY a deliberate re-read of 17 YouTube video transcripts, specifically commissioned because a first pass had compressed away real content. Your job is a THIRD pass on the same material, through a specific new lens the user just asked for — because even a careful second pass can still miss things a differently-framed third pass catches. This project has documented, real precedent for this exact pattern: `C:\Users\AwBro\Desktop\AI\claude_failure_report.md` §10 records a case where "a genuine full re-read... later found 30 additional reusable patterns... missing from the document entirely." Don't repeat that by skimming — read both files completely, end to end.

For each of the two files, extract and report under these 5 headings (skip a heading if nothing qualifies — don't pad):

**A. Complete/portable code or config** — any real code snippet, command, or config pattern mentioned as something a video's creator actually used, ready to reuse close to as-is. Cite which video/section.
**B. Fixable code** — something close but broken/incomplete as described, worth starting from rather than writing fresh.
**C. Free/unutilized tools** — this is likely the richest category here. Any real, free tool a video mentions that ISN'T already the chosen primary pick for its pipeline stage in this project's PROJECT.md architecture (faster-whisper, ClipsAI, yt-dlp, ffmpeg, ollama, LangGraph, twitch-clip-miner, Auto-clipper, openshorts are already chosen — anything else free and real is a candidate for this list, especially if a video's creator specifically said it was useful/underrated).
**D. Efficiency paths** — anything a creator did to cut cost, time, or API/compute usage, including non-obvious workflow tricks.
**E. Anything that corrects or adds nuance to what's already believed true** — a real gotcha, a real number/threshold with justification, a warning about a platform behavior (shadowbanning, rate limits, content policy), a business/monetization detail.

Cite the exact video (filename-derived ID is fine, or the section heading used in the doc) and enough location detail that someone could navigate straight back to it. This needs to function as a real index — be specific and exhaustive, not a highlights reel. If genuinely nothing new turns up in a section, say so plainly rather than manufacturing filler.
```

---

## When resuming — explicit user instruction on exact order

**Literally the first two things to do, in this order, before anything
else:**

1. **Ask the user directly whether to relaunch mining agents now** — do
   not relaunch unilaterally, this must be asked first. **The session
   ended at 84% usage with the user explicitly saying "hold on more agents
   till we get more limit"** — so confirm there's actual headroom before
   spending anything.
2. **Confirm everything from the 2026-08-01 session is actually saved** —
   run `git log --oneline -6` and `git status` in
   `C:\Users\AwBro\Desktop\automated clipper bot`, verify it's clean and
   matches `origin/master`, and report that back before doing anything
   else. Don't assume the save held; check it.

Only after both: launch the next item(s) from the 12-item table above,
one file per agent, using the per-file prompt template. Then for each
report that comes back:
1. **Check it** — grep the real source file for several distinctive
   claims from the report (exact quoted strings, hashes, unusual numbers,
   structural claims). Confirm it isn't fabricated.
2. **Save it verbatim** to
   `reference/mining_2026-08-01_<source_file_name>_VERBATIM.md`.
3. **Commit and push immediately** — never batch.
4. **Tick it off in the 12-item table above** and push that too.

Do NOT try to `SendMessage`-resume the old agent IDs
(`a25c900efa6ccb6aa`, `ac2ed4b6c496e4820`, `a7acbccd99510c8c8`) — already
confirmed dead/stopped, resuming will fail. (Item 1's successful agent,
`ac7d3228d798a7c2b`, is complete and needs nothing further.)

Once all 12 are done: update `PROJECT.md`'s backlog entry, and delete or
rewrite this file so it stops describing a "pending" state that's no
longer true.

## Still queued after the 12-item mine (from PROJECT.md's backlog)

- **Phase 2**: extend the Hugging Face deep dive. The 3 original HF agents
  completed and their full reports are saved verbatim
  (`reference/research_2026-08-01_huggingface_*_VERBATIM.md`, commit
  `11c6dba`) — that data loss is already fixed. Remaining scope is
  *extension*: datasets, more Spaces, TTS/voice-clone models for the
  deferred multi-language idea, or actually prototyping the concrete
  candidates already found (`distil-whisper/distil-large-v3`,
  `MIT/ast-finetuned-audioset-10-10-0.4593`,
  `dima806/facial_emotions_image_detection`, `meta-llama/Llama-Guard-3-1B`).
- **Phase 3**: Opal / Vercel / "Claude connectors like higgsfield"
  (https://www.youtube.com/watch?v=mFOoNPFylLI&t=2s) / the user's Gemini
  Plus suite + Google free tools. Note `Needs Research01.txt` was checked
  and is **identical** to the Cowork plugin docs already saved in
  `PROJECT.md`'s backlog — no new information there, don't re-research it.
- **Phase 4**: one agent doing deeper web research for ways to advance the
  project's tech/scope/quality, aligned to project goals and the same
  5-lens prompt.
