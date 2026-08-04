# PENDING — resume here

## 📋 LIVE AGENDA & PROGRESS — update this every session, read it first

**Last updated: 2026-08-02.** This is the running status board. Nothing
here is finished; nothing here is lost.

---

## ⭐ FIRST THING NEXT SESSION — build `START_HERE.md`

**User's explicit direction (2026-08-02):** *"then i said this to make it
automated but we ran out of tokens we will make note and add it to the 1st
thing on the agenda."* Original ask: *"lets plan the auto reference file to
ensure we are on the same page every session."*

This is **task #1**, before workstream A/B/C/D. It was designed and
approved on 2026-08-01, deferred purely for budget. Estimated ~10 minutes
on a fresh limit. **The full design is recorded in "Also queued" below —
don't re-derive it, just build it.**

**Two parts, and part 2 is the one that makes it "automated":**

1. **Build the file** — `START_HERE.md` at the repo root, undated, a
   router not a duplicate, five fixed sections (state now / single next
   action / blockers & open leads / how we work / where things are),
   overwritten each session rather than appended.

2. **Make the update ritual a RULE — this is the actual ask.** The user's
   word was *"automated."* A file that depends on remembering to update it
   is not automated; it decays exactly like the dated file it replaces.
   Proposed **Rule 22**: *updating `START_HERE.md` is the last action of
   every session, immediately before the final commit and push — not
   optional, not skippable, and it happens even when the session is being
   cut short by a usage limit.* Ask the user to confirm before adopting
   (Rule 14 process — no rule gets adopted unasked). **(Numbered 22, not
   21 — Rule 21 was taken later on 2026-08-02 by "run every check before
   reporting.")**

**Why it matters, in the user's own framing:** *"to ensure we are on the
same page every session."* The current setup works for session two —
proven this session — but breaks by session three or four, when there are
competing dated resume files and no obvious winner. That is precisely the
mess this project already spent a full session untangling.

---

Four research workstreams are open below.

### A. Retroactive Rule 20 review — re-check completed work for dismissed tools
*Why: Rule 20 (added 2026-08-02) was created after the user found working
free tools had been dismissed too readily in already-"completed" research.
Everything marked done before that rule existed needs re-reading through
the five-role lens. Output goes in
`reference/retroactive_rule20_review_2026-08-02.md` — a NEW file; per Rule
16 the raw `*_VERBATIM.md` reports are never edited.*

| # | Target | Status |
|---|---|---|
| A1 | HF audio/transcription report | ✅ **done** — 5 tools re-opened, incl. Kyutai STT (judged against batch when the project's Phase 1 is live) |
| A2 | HF vision/detection report | ⬜ pending |
| A3 | HF local-LLM/judging report | ⬜ pending |
| A4 | Mining report (`deep_dive_moment_detection`) | ⬜ pending |
| A5 | The 78-source tool-directory audit (`handoff_2026-08-01_evaluation.md` §1) | ⬜ pending |
| A6 | **The 17 already-mined YouTube videos** (`research/fresh_pass_videos_1-9.md` + `_10-17.md`) — added 2026-08-02 at user direction: *"add the recheck for useful dismissed data in those youtube videos that were marked complete"* | ⬜ pending |

### B. The 12-item source-mining pass
*Why: the original 3 broad agents died producing nothing. Split to 12
small ones, one source file each, verified and saved per item.*

**1 of 12 done** — see the full table further down this file. Item 1
(`deep_dive_moment_detection.md`) is complete and pushed (`7e009fb`).
**Note:** items 2–12 now also carry the Rule 20 five-role instruction in
their prompt template, so they evaluate tools correctly on the first pass
rather than needing an A-workstream re-review afterward.

### C. YouTube videos not yet transcribed
*Why: 6 videos referenced across the planning docs have no transcript.
`research/fetch_transcripts.py` already exists and succeeded 17/17 before
— reuse it (Rule 1), don't browser-scrape.*

| Video | ID | Status |
|---|---|---|
| Higgsfield / Claude connectors | `mFOoNPFylLI` | ✅ 521 snippets (2026-08-04) |
| Claude + Whop Clipping Workflow | `PafYu69s5NA` | ✅ 351 snippets (2026-08-04) |
| Gemini Gems Tutorial | `QqwNue_KL-4` | ✅ 145 snippets (2026-08-04) |
| Lacy's Best Streamer University Moments | `cVkFMpDLQrM` | ✅ 1068 snippets (2026-08-04) |
| How Lacy Got Used On Stream | `mVqnCvE337E` | ✅ 2337 snippets (2026-08-04) |
| Lacy's Content Strategy Breakdown | `lYafPAHVOno` | ✅ 397 snippets (2026-08-04) |

Confirmed missing from `research/transcripts/` (which holds 18 files for
the original 17 videos + a summary). The 3 Lacy-specific ones are the only
source anywhere for **what a clip-worthy Lacy moment actually looks like** —
that directly informs detection thresholds and hook patterns.

### D. Platform / free-inference / hosting research
*Why: the user supplied a target list as a method instruction — widen from
"models within HF" to hubs, hosted inference, galleries, and hosting.
Full detail + suggested 5-agent split:
`reference/research_targets_platforms_2026-08-02.md`.*

⬜ Not started. Highest-leverage lead: **Ollama on a free Oracle ARM VM**
(always-on judging without the user's PC running).

### Also queued

**`START_HERE.md` — designed, approved, not yet built.** User chose
"Monday, on a fresh limit" (2026-08-01) over building it immediately.
The full design, so it isn't re-derived:

> **Problem it solves:** this file is named for an event and dated. Next
> session it's ambiguous — still pending? Make a `_2026-08-04` version?
> Within a few sessions there are competing resume files and no obvious
> winner. That's the exact mess this project already spent a session
> untangling.
>
> **Design:**
> - **Undated name**, at the **repo root** (not `reference/`) — visible
>   immediately on GitHub and in any listing, never ambiguous which is
>   current.
> - **A router, not a duplicate.** Points to `PROJECT.md`, `CLAUDE.md`,
>   the agenda tables, the reference docs. Restates nothing — one source
>   per fact, so nothing can drift out of sync.
> - **Overwritten each session, not appended.** It describes *now*.
>   History already lives in git and the dated reference files.
> - **Five fixed sections:** (1) state right now, (2) the single specific
>   next action — not a menu, (3) blockers & open leads, (4) how we work
>   (pointer to rules + the non-negotiables), (5) where things are.
> - **The ritual that keeps it true:** updating it becomes the *last*
>   action of every session, right before the final push. Worth making a
>   rule so it can't be skipped.
> - This dated file stays unedited afterward as a historical record;
>   `START_HERE.md` links to it.

- **Rules 8 & 9** still ⚠️ PROVISIONAL — Gemini-sourced, never authorized.
  Need a yes/no from the user. (Rule state as of 2026-08-02: **15 active**
  — 3, 5, 7, 10–21. Removed at user direction: 2, 4, 6. Provisional: 8, 9.
  Inherited from a prior session: 1.)
- **Two unverified leads** (do these before related build work): does the
  sibling project's video code still run, and is `validate_environment.py`
  one auth fix from passing. Both detailed below.
- **💬 A real discussion is queued, not decided** —
  [`reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md`](DISCUSS_next_phase_autonomy_prompt_2026-08-02.md).
  The user drafted an "autonomy prompt" for the build phase (*"Lead
  Principal Engineer… take 100% ownership… don't stop until your code
  passes its own integration tests"*) and asked for an opinion. **Nothing
  adopted.** The file holds the draft verbatim, three problems to resolve
  (it collides with Rule 10; the integration-test clause has nothing to
  bite on until code exists; "intern → titan" needs measurable rungs), and
  **the key finding: every mechanism it reaches for already exists in
  proven form in the sibling `pipeline.py`** — retry/dead-letter with
  degraded-mode tracking, post-render corruption QA, output smoke tests,
  and the quality-ratchet pattern we invented this session. Five open
  questions at the end need the user's answers before this goes anywhere.
- **⚠️ Filename vs. content date:** this file is named `_2026-08-01` (when
  it was created) but its agenda reflects **2026-08-02** work. The
  agenda's "Last updated" line is authoritative, not the filename. This
  discrepancy is exactly why `START_HERE.md` above should get built.

### E. The failure report — what's fixed, what isn't
*`C:\Users\AwBro\Desktop\AI\claude_failure_report.md` (1,400 lines, filed
2026-07-30) is this project's quality bar. Tracking real progress against
its findings, honestly — including where nothing has changed.*

| Finding | Status |
|---|---|
| §3 `validate_environment.py`'s 8 defects | ✅ **Fixed** — a newer local copy had all 8 addressed; diff-confirmed and pushed 2026-08-01 |
| §17 "parallel agents used only after I raised it, then abandoned" | ✅ **Fixed and made a rule** — Rule 11. **12 agents launched** across 2026-08-01/02: 1 tool-claim check, 4 tool-directory audit, 3 source-mining (died, zero output), 3 Hugging Face (hit a session limit, resumed via `SendMessage`, all 3 completed), 1 mining item-1 (succeeded). **8 of 12 produced usable output.** |
| §17 "work not committed incrementally" | ✅ **Fixed** — Rule 18 + save-per-item; proven when the limit hit mid-session and nothing was lost |
| §12/§17 "free tools dismissed against a stated budget constraint" | ✅ **Rule written** (Rule 20), ⬜ **retroactive fix in progress** — workstream A, 1 of 6 done |
| §2/§19 "verification reported without being performed" | ✅ **Fixed and made a rule** — Rule 19 (grep the real source); proven at 9/9 spot-checks on mining item 1 |
| §1 "condensing source labeled as verbatim" | ✅ **Fixed and made a rule** — Rule 15; the 3 HF reports were re-saved word-for-word after being caught summarized |
| §10 "research reported complete while incomplete" | ⚠️ **Partially** — the 12-item re-mine (workstream B) exists precisely to fix this. 1 of 12 done. |
| §14 "no pipeline code at all in project 2" | ❌ **Still true.** Zero pipeline code written. Everything to date is restoration, research, and rules. This is the honest headline. |
| §13.0 "model discovery never wired into the pipeline" | ❌ **Unaddressed here** — that's a defect in the *sibling* project, untouched |
| §14 "the pipeline has never once run to completion" | ⚠️ **Contested, unresolved** — two `.mp4` files dated 2026-07-27 exist on disk, which is 3 days *before* the report. Whether that constitutes a completed run is **untested**. See the leads section below. |
| §21b "4,059-line single-file monolith" | ❌ **Unaddressed** — sibling-project structural issue |
| §18 "paying repeatedly for the same work" | ⚠️ **Improved, not solved** — Rule 13 + small-scope agents + save-per-item directly target it, and the 48-min/$15 zero-output failure did *not* recur. But one broad-agent failure still happened this session before the fix. |

**Net:** the *process* failures the report documented are now mostly
addressed with real rules and proven practice. The *deliverable* failure —
no working pipeline code — is unchanged. Worth stating plainly rather than
letting a long list of green checkmarks imply otherwise.

### Reference docs produced so far (all pushed)
| File | What it holds |
|---|---|
| `MASTER_TOOLS_CATALOG_2026-08-02.md` | **~110 tools, all with URLs**, by pipeline stage, with Rule 20 roles. Start here when picking a tool. |
| `retroactive_rule20_review_2026-08-02.md` | Workstream A output |
| `research_targets_platforms_2026-08-02.md` | Workstream D scope |
| `mining_2026-08-01_deep_dive_moment_detection_VERBATIM.md` | Workstream B item 1 |
| `research_2026-08-01_huggingface_*_VERBATIM.md` (×3) | The HF passes, raw |
| `handoff_2026-08-01_chat_pasted_originals.md` | All pasted source, verbatim |
| `handoff_2026-08-01_evaluation.md` | Evaluation of the above (kept separate per Rule 16) |

---

## 2026-08-02 SESSION ADDENDUM — operational facts that only existed in that conversation

### ✅ The cold-start mechanism is PROVEN, not theoretical

The 2026-08-01 session ended by writing these notes *hoping* a cold
session could resume from them. **2026-08-02 tested that for real and it
worked.** The user pointed at this file, it was read cold, and work
resumed correctly with no re-derivation and no reconstruction from chat
history. **Trust this file — it has been validated once in production.**

### ✅ The checkpoint survived a real hard-limit hit

The 2026-08-01 session ended at 95% usage and was cut off. On resume,
`git status` was clean and local matched `origin/master` at `9e732d8` —
**nothing was lost.** The save-per-item discipline (Rules 13/18) is
proven under actual failure conditions, not just in principle. This is
the strongest argument for never batching commits.

### ⚠️ Unresolved contradiction about the 3 dead mining agents

On 2026-08-02 a system task-notification claimed: *"their transcripts are
saved on disk, so their progress is not lost. Resume any of them by
sending a message to its id with SendMessage, or check its worktree/output
for partial work."*

**This contradicts what was actually observed on 2026-08-01**, where (a) a
full search of the session temp directory found **three 0-byte output
files and no transcript anywhere**, and (b) `SendMessage` to all three IDs
returned *"was stopped by the user and won't be resumed."*

**Not retried on 2026-08-02** (budget). Treat as genuinely unresolved. If
it ever matters, one `SendMessage` attempt to `a25c900efa6ccb6aa` /
`ac2ed4b6c496e4820` / `a7acbccd99510c8c8` settles it cheaply — but the
12-item re-mine (workstream B) makes those agents redundant anyway, so
this is curiosity, not a blocker.

### 📉 Real burn-rate data point

2026-08-02 went from a fresh session to **99% used in a single sitting**,
doing: 1 mining agent, ~8 file writes/edits, ~10 commits, and several
large file reads. **No agent-heavy research at all** — that budget went
almost entirely to reading, writing, and committing documentation. Plan
accordingly: documentation work is *not* cheap, and a session doing both
research agents *and* thorough note-keeping will not fit in one window.

### 🔍 A practice worth repeating: self-audit against the conversation before wrapping

At the end of 2026-08-02 the user asked: *"go back and re read the convo"*
and check the notes actually captured everything. **That audit found three
real problems**, one of which was genuine content loss:
1. The entire `START_HERE.md` design — discussed in detail, user-approved,
   and **never saved** beyond a one-line mention. It would have been lost.
2. An inaccurate agent count (said 10, actual 12 launched / 8 useful).
3. A cold-read trap — this file's *name* says 2026-08-01 while its agenda
   says 2026-08-02.

**Do this every session before the final push.** Writing notes as you go
is not sufficient; the gaps only become visible when the notes are read
back against what was actually discussed. Cheap, and it caught real loss.

---

## SESSION CONTEXT THAT ONLY EXISTS HERE — read before doing anything

Written deliberately at the end of the 2026-08-01 session because it lives
nowhere else and would otherwise be lost. Everything below is operational
reality, not theory.

### Where everything is

| Thing | Location |
|---|---|
| Working repo (local) | `C:\Users\AwBro\Desktop\automated clipper bot` |
| GitHub (source of truth) | `github.com/anthonybrod/automated-clipper-bot`, branch `master` |
| User's Drive copy | `/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt` |
| User's Colab notebook | `Claude's AI clip bot v1.ipynb` |
| Sibling project (salvage source) | `C:\Users\AwBro\Desktop\youtube auto videos` — has `pipeline.py` (~4,059 lines) |
| Raw research inputs | `C:\Users\AwBro\Desktop\AI\automated clipper bot\sample reference\` and `sample research\` |
| The quality bar / history | `C:\Users\AwBro\Desktop\AI\claude_failure_report.md` |

**Real Python on this machine** (`python`/`py` do NOT resolve — Windows
Store stub): `C:\Users\AwBro\AppData\Local\Programs\Python\Python312\python.exe`

### The Drive sync mechanism (proven working twice)

Claude has **no** Drive access — no Drive Desktop app installed, no API,
and the in-app browser + Chrome extension both hit sign-in walls (tried 3
separate links, all failed; don't retry, it's not a permissions problem).
So: **Claude pushes to GitHub, the user pulls into Drive.** One line:

```python
!git -C "/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt" pull
```

Prefer that over `%cd` — the `%cd` magic broke once on the spaces in the
folder name ("No closing quotation"). The full bootstrap cell (mount +
clone-or-pull, idempotent) is saved further down this file.

### How the user works — read this before interacting

- **Ask before launching agents. Confirm usage headroom first.** Not
  optional. The session ended at 95% used with the user saying explicitly:
  *"hold on more agents till we get more limit."*
- **The user is the director.** They decide phase transitions and when
  something is "complete." Claude reports what was done and how it was
  tested; the verdict is theirs. They said it plainly: *"i am always the
  final say before we move on and before we mark anything as complete or
  finished."*
- **Budget is a live constraint, not background.** Metered plan, hard
  daily + weekly limits, hit repeatedly, and they've paid out of pocket to
  continue. A failed agent run this session burned ~48 minutes and ~$15
  for zero output and they were rightly angry about it. Weekly reset:
  **Monday, 1:00 PM.**
- **They catch real mistakes.** Over this session they caught: an
  overstated "CONFIRMED" claim, two rules adopted without authorization,
  three rules that pre-committed research outcomes, and rules I'd listed
  as from-this-session that weren't. Take pushback seriously and check
  before defending anything.
- **Never delete or overwrite their content** without being asked
  directly — append and preserve. Removed rules stay in `CLAUDE.md` struck
  through with the reason, not erased.

### What actually happened this session (so it isn't re-derived)

The project folder **did not exist on disk** at session start — it was
restored via `git clone` from GitHub. Before that, work was scattered
across `AI\automated clipper bot\` (with confusing `sample `-prefixed
duplicates), several Drive-export zips, and two Colab notebooks.

Real findings, each already written up in the reference docs:
- `validate_environment.py` on GitHub was **older** than a fixed local
  copy; the fixed one (retry/backoff, token tracking, single token
  exchange, `get_secret()` throughout) was swapped in and pushed.
- A real, reproducible `KeyError: 'data'` crash in `chat_downloader`'s
  Twitch GraphQL path, found in an actually-executed notebook — not
  hypothetical. Needs defensive `.get()` chaining before Stage 1 depends
  on it.
- A real (empty) `pipeline_tasks` / `payout_logs` SQLite schema recovered
  from a code-less Drive export — adopted as the basis for Stage 6 VOD
  tracking rather than designing one.
- **4 hallucinated repo-owner attributions** in Gemini's tool directory
  (`cut-the-crap`→ real is `jappeace/`, Camoufox → real is `daijro/`,
  `ffsubsync` → real is `smacke/`, plus a fabricated capability on
  `CanadianZombies/download-twitch`).
- **MediaPipe "Face Mesh" is wrong** — caught three times independently.
  Correct component is lightweight **Face Detection / BlazeFace**.
- Tier 2 (gambling-affiliate burner channel) is **out of scope** — its own
  design is anti-shadowban/hash-randomization tooling built because it
  expects bans. Deferred, not built. Only Tier 1 (compliant clipper) is
  active scope.

### The three research reports already saved (don't re-run these)

`reference/research_2026-08-01_huggingface_{audio_transcription,
vision_detection,local_llm_judging}_VERBATIM.md` — full Hugging Face
passes, saved word-for-word. Concrete candidates found, none yet adopted:
`distil-whisper/distil-large-v3` (~6.3x faster than large-v3),
`MIT/ast-finetuned-audioset-10-10-0.4593` (real scream/shout/laughter
classes), `dima806/facial_emotions_image_detection`,
`meta-llama/Llama-Guard-3-1B` (Ollama-pullable content safety).

---

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
> **Do NOT dismiss a tool for losing the "primary pick" slot.** For each
> one, say which of these five roles it could fill: (1) primary,
> (2) backup/fail-safe when the primary breaks or is rate-limited/too
> expensive, (3) cross-check to verify the primary's output, (4) assist —
> a free local pre-filter that narrows work before an expensive stage,
> (5) feature/quality add the pipeline otherwise wouldn't have. A free,
> local, offline tool costs nothing to keep in reserve, and "Gemini can
> also do that" is not a reason to discard one — Gemini costs real tokens
> per call. Never judge on star count, README tone, or last-commit date
> alone; unmaintained is not the same as non-functional. If you do set
> something aside, record *why* and *what would bring it back*, never a
> bare "not needed."
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

## HIGH-VALUE LEAD — verify before rebuilding anything (user-reported 2026-08-01)

**Two claims from the user that, if true, save real work. Both need
verification — do NOT treat either as fact until checked, and do NOT
dismiss them either. The user was clear these are recollections
("im sure there is notes"), not certainties.**

### Lead 1: two output files exist — everything beyond that is UNVERIFIED

> **CORRECTION, same session (2026-08-01).** An earlier version of this
> section was headed "CONFIRMED — the sibling project DID produce real
> video. The docs saying otherwise are WRONG," and told a future agent to
> re-grade salvage entries from "unproven" to "proven." **That was an
> overreach and the user caught it.** What was actually verified is that
> two files exist on disk. That does not establish that the current code
> works, which code produced them, or that any run completed successfully
> by the pipeline's own definition — a run can emit MP4s and still fail
> later stages. The claim has been scoped back to the real evidence below.
> The user's ruling, now Rule 12 in `CLAUDE.md`: *"if we didn't confirm it
> in this session and i didn't personally give the ok then its not
> factual."*

The user's words: *"the project that built youtbe video from generated
text worked. It wasn't free but that code produced a short and longer
video with voiceover and the worst stick animation ever but it ran and
worked im sure there is notes."*

**FACTUAL — directly verified 2026-08-01 by a real directory listing:**

```
-rw-r--r-- 480,883 bytes  Jul 27 12:21  short_1785179923.mp4
-rw-r--r-- 423,461 bytes  Jul 27 12:21  video_1785179923.mp4
```
Both at `C:\Users\AwBro\Desktop\youtube auto videos\`. Also factual:
`enterprise_workspace/` exists with a populated tree (`deliverables`,
`shorts`, `thumbnails`, `metadata`, `review`, `audit_logs`, `references`,
`criteria`, `dead_letter`, `analytics_feedback`, `algorithm_evolution`).

**FACTUAL — user-confirmed directly this session:** the user has seen
these videos and describes them as having voiceover and stick animation,
*"they are not great but clearly it fetched something and made something
from it."* That is the user's own first-hand account and counts as
confirmed under Rule 12.

**INFERENCE, not fact:** the `1785179923` suffix *appears* to match the
pipeline's run-ID convention (`f"live_{int(time.time())}"` /
`f"run_{int(time.time())}"` in its `__main__`), and that integer decodes
to 2026-07-27 12:18:43, ~2.5 min before the files' mtime. Suggestive of a
timed run, **not proof of one** — the pattern match was not traced back to
actual executing code.

**EXPLICITLY NOT VERIFIED — do not assume any of these:**
- ❌ That the code currently in `pipeline.py` still works.
- ❌ That the code currently in `pipeline.py` is what produced these files
  (the repo changed heavily after Jul 27 — 99 commits across the project's
  life, many after that date).
- ❌ That any run completed *successfully by the pipeline's own
  definition* — a run can emit MP4s and still fail later QA/distribution
  stages. Output files ≠ a passing run.
- ❌ That the two contradicting documentation claims are false. The files'
  existence is **in tension with** `CLAUDE.md`'s *"no full successful
  end-to-end Colab run has happened yet"* and `claude_failure_report.md`
  §14's *"never once run to completion"* — and that tension is worth
  investigating — but tension is not disproof, and neither doc should be
  edited until someone actually establishes what happened.

**User's own framing, which is the correct one to carry forward:** *"we
had many ai hallucinations on the way here and ai going off notes from
past projects it was very messed up idk if that code still works we will
test it its just in notes for now."*

**Why it's still worth investigating:** IF the assembly path turns out to
work, the clipper bot's Stage 4 (rendering) needs exactly that — ffmpeg
muxing, TTS/voiceover integration, an assembly/encode path emitting both
a short and a long cut. That would be port-instead-of-rebuild work.
But that upgrade is **conditional on testing it**, not on these files
existing. Leave `SALVAGE_INVENTORY.md`'s current grading alone until a
real test says otherwise.

**What the responsible agent should do (the user explicitly asked for
this to be checked and watched for):**
1. **Watch the two MP4s** and critique them honestly — the user said they
   want a critic's read, and described the animation as "the worst stick
   animation ever." Assess: does the voiceover sync, is the pacing right,
   are captions readable, is the vertical (short) framing correct, what
   would actually need to improve for publishable output.
2. **Trace which code paths actually produced them** — `assembly_agent`,
   the ffmpeg command builder, the TTS chain, the image/animation
   generator. Those specific functions are the proven ones.
3. **Find the run's artifacts** in `enterprise_workspace/` (deliverables,
   shorts, thumbnails, metadata, audit_logs) — the audit log and the
   printed "Cost Summary" from that run reveal real per-stage behavior
   and real cost, far better evidence than reading the code cold.
4. **Only after establishing what actually happened**, decide whether the
   sibling project's docs need correcting and whether any
   `SALVAGE_INVENTORY.md` entries should be re-graded. Do not do either
   pre-emptively — see the correction notice at the top of this section.
5. **Note the cost caveat**: the user said *"It wasn't free"* — this run
   used paid API calls. Relevant to the clipper bot's explicit
   cost-philosophy constraint; find the actual figure in that run's Cost
   Summary rather than guessing.

### Lead 2: `validate_environment.py` may be one small auth fix from passing

The user's words: *"one of the validate_environment.py was a minor
authentication (maybe my twitch api or something small) from a working
test."*

**Current documented status** (`PROJECT.md`): "Not yet run end-to-end
with real Twitch credentials — blocked on the user creating a Twitch
Developer Console app." If the user actually ran it and got as far as an
auth error, that means **ffmpeg and `GOOGLE_API_KEY` checks likely already
passed**, and the only remaining failure is the Twitch credential step —
a materially smaller gap than "never run."

**How to verify (very cheap):** just run it. The credentials are now in
Colab as secrets (`GOOGLE_API_KEY`, `TWITCH_CLIENT_ID`,
`TWITCH_CLIENT_SECRET`), and the project is cloned into Drive, so a
single Colab cell does it:
```python
%cd "/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt"
!python validate_environment.py
```
It prints PASS/FAIL/WARN per check with the real error text. That output
immediately tells us which specific check fails and why — no guessing.
**Do this before spending any agent budget on Stage 1 work**, since it
directly resolves the project's single stated blocker.

**Note the version caveat:** the copy now in Drive/GitHub is the *fixed*
version (retry/backoff, token tracking, single token exchange, real
`get_secret()` throughout) swapped in this session — newer than whatever
the user last ran. So a previously-seen error may already be fixed.

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
