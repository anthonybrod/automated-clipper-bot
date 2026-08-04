# START HERE

**The single entry point for this project. Read this first, every session.**

Last updated: **2026-08-03** · Written at commit `b1d2ec7` (this file's own
commit lands *after*, so HEAD will read one ahead — see §0) · Working tree
clean, local = GitHub. **Drive pull pending** (user runs it).

This file is a **router, not a duplicate** — it points at the real sources
rather than restating them, so nothing can drift out of sync. It is
**overwritten each session**, not appended; history lives in git.

---

## What this project is (read before anything else makes sense)

An **automated Twitch clipping bot**, built on a **$0 open-source stack** —
no paid SaaS anywhere in the pipeline. It watches a streamer's content,
detects the best moments statistically rather than by watching everything,
transcribes and captions locally, cuts to the right format per platform,
and publishes — **with a human approval gate**, not fully unsupervised.

**Why it exists:** to earn **Clipping.net bounty payouts**. The target is
the streamer **Lacy** (@LacyCrashOuts — high-intensity rage, gambling, and
argument clips). Clips are paid **per 1,000 views**, and campaigns enforce
a **minimum view threshold per post** — a clip that lands under it pays
**$0**. That is why hook quality and engagement aren't cosmetic concerns:
they're the difference between getting paid and not.

**Why budget discipline is a first-class constraint, not a preference:**
payouts are roughly $0.50–$3.00 per 1,000 views, so any recurring API cost
eats the margin directly. This is the reasoning behind the free-tool rules,
the statistical pre-filter (keep most of a VOD away from any paid call),
and Rule 20's five-role tool evaluation.

**Scope note:** a second "Tier 2" monetization channel appears in older
planning docs. It is **explicitly out of scope** — its design is
anti-shadowban/hash-randomization tooling built because it expects to get
banned. Only Tier 1, the compliant clipper, is active.

**The 6-stage pipeline**, each with a verified tool choice (full reasoning
and sourcing in [`PROJECT.md`](PROJECT.md)'s Architecture Outline):

| Stage | What it does | Chosen approach |
|---|---|---|
| 1 Ingestion | Pull the VOD/stream + chat | `yt-dlp`; chat via Twitch GQL (keyless) or `chat-downloader` |
| 2 Transcription | Word-level timestamps, local + free | `faster-whisper` (candidates open — see catalog) |
| 3 Moment detection | Find the clip-worthy moments | **Three-stage funnel** — free statistical pre-filter → cheap LLM score → expensive LLM detail on top-N only |
| 4 Assembly | Cut, crop, caption, blur chat | `ffmpeg` — 9:16 split-screen (facecam over gameplay), karaoke captions, chat boxblur for TOS safety |
| 5 Distribution | Publish per platform | YouTube Data API, X API, Meta Graph, TikTok — with a human approval gate |
| 6 Orchestration | State, retries, budget | LangGraph + `AsyncSqliteSaver`; port the proven retry/dead-letter/budget machinery from the sibling project |

**The single most important technique found in all research:**
`snap_clip_to_words()` — LLMs are unreliable at millisecond arithmetic, so
proposed cut points get snapped onto **real word-boundary timestamps** from
the transcript (with ~0.35s lead / 0.45s tail padding into silence) before
anything is cut. Every other source assumed raw LLM timestamps were safe.
They aren't.

**Campaign rules that constrain the build** (from the plan/checklist —
these are requirements, not preferences): mandatory `#lacy` hashtag and
Lacy's name in the caption; **zero watermarks or logos**; Tier-1
English-speaking audience targeting; stream chat must be blurred to avoid
TOS flags from viewer messages; no botting or fake engagement.

**Full source material:** the master plan and checklists are preserved
verbatim in `reference/handoff_2026-08-01_*.md` — including a 920-line
planning transcript and a 78-source tool directory. The decision-ready
tool list is
[`reference/MASTER_TOOLS_CATALOG_2026-08-02.md`](reference/MASTER_TOOLS_CATALOG_2026-08-02.md)
(~110 tools, real URLs, Rule 20 roles).

---

## 0. Validate this file before trusting it

**This file goes stale by design** — it is written during a session and can
miss whatever happened after. A cold-start test on 2026-08-03 found it
carrying a commit hash one commit behind and a wrong rule count. **Run
these three checks first; if any disagrees, believe the repo, not this
file, and fix the file.**

```bash
cd "C:\Users\AwBro\Desktop\automated clipper bot"
git log --oneline -3          # header hash should be HEAD or 1 behind
git status --short            # uncommitted work? this file may not describe it
grep -cE '^[0-9]+\. ' CLAUDE.md   # must match the rule count in §4
bash check_links.sh           # every doc link still resolves? (catches link rot)
```

**On the hash:** a file can never record the hash of the commit that
contains it — writing this file changes it, then committing produces a new
hash. So **HEAD one ahead of the header is normal and correct.** Two or
more ahead means real work landed after this file was updated: read those
commits, then fix this file. This offset was found by actually running the
check on 2026-08-03; the original wording ("must match") would have
false-alarmed on every single session.

**If the working tree is dirty:** uncommitted work is *not* lost — read
`git diff` to see what it is. It is likely a session that ended before
saving. Do **not** commit it without asking; approval status cannot be
determined from a diff (Rule 10).

---

## 1. State right now

**Phase: research and organization. Zero pipeline code exists.** That is
the honest headline — everything so far is project restoration, source
verification, tool cataloguing, and operating rules. It is a deliberate
sequencing choice, not a stall (reasoning: §4 of
[`reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md`](reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md)).

**Done and durable:**
- Project restored from GitHub after the local folder went missing; now
  synced across local / GitHub / the user's Drive folder
- `validate_environment.py` — the newer, already-fixed version deployed
  (all 8 previously-logged defects addressed)
- ~110 tools catalogued with real URLs, roles, and verification status
- 4 research reports saved verbatim (3 Hugging Face + 1 source-mining)
- 16 active operating rules, each written because a specific failure
  happened

**✅ COMPLETE — authorized by user 2026-08-03: the Rule 10 marking
convention.** Nothing is written as complete until the user says so
in-session; when they do, it is stamped `✅ COMPLETE — authorized by user
YYYY-MM-DD`. Until then the only honest statuses are *in progress*,
*awaiting user approval*, or *blocked*. See Rule 10 in `CLAUDE.md`.

**✅ COMPLETE — authorized by user 2026-08-03: the four delivery-hole
fixes.** A cold-start test found the resume system was one mechanism deep,
not three. Fixed: (1) a pointer in the sibling project's `CLAUDE.md`,
since this repo's banner only auto-loads when a session is rooted here and
sessions have repeatedly been rooted in the sibling; (2) the cross-session
memory entry rewritten to point at this file and to document that
auto-load failure; (3) §0 of this file, self-validation against its own
staleness; (4) a global `Stop` hook (`~/.claude/hooks/`) reminding to
update this file before a final push — global, not project-level, so
working directory doesn't matter.

**✅ COMPLETE — authorized by user 2026-08-03: the save system itself.**
`SAVE_PROTOCOL.md` defines what *"save everything"* means (the user's own
words govern it), and it now carries **the written `START_HERE.md` format** —
what belongs in every section, in what order, with the rule governing each.
This file is overwritten every session, so without a written format it
degrades a little each time.

Four cold-start test passes were run against the whole system. **Every pass
found real bugs**; all are fixed:

| Pass | What it found |
|---|---|
| 1 orientation | `PROJECT.md` stale again; `README.md` never pointed here |
| 2 execution | Rule 11 vs Rule 13 undefined for one-file tasks; no cost estimates; no partial-work handling |
| 3 failure modes | `check_links.sh` ran only when someone remembered — now fires from the Stop hook |
| 4 final | `SESSION_HANDOFF_PROMPT.md` carrying a **stale commit hash**; `README.md` claiming 11 rules when there are 20 |

Pass 4's were the dangerous kind — a stale hash sends the next session to a
commit that predates the work it is meant to resume from. The greps that
caught them are now a written pre-save checklist in `SAVE_PROTOCOL.md`,
not something someone has to remember to run.

**✅ COMPLETE — authorized by user 2026-08-03: Rule 22 adopted.**
Updating this file is now the non-skippable last action of every session,
before the final push, *even when a usage limit is cutting things short* —
which is exactly when it gets skipped and exactly when it matters most.

**✅ RESOLVED by user 2026-08-03: Rules 8 & 9 dropped.** Asked directly,
answered *"Neither — drop both."* They were Gemini-sourced and adopted
without authorization; that is why they are gone, not a technical
judgment. Both are struck through in `CLAUDE.md` with the reasoning kept,
so the record survives. Decide them at build time, against real output.

**No blockers remain.** The next action is §2.

**Outside git:** a 66MB transcript backup at
`AI\claude_transcripts_backup_2026-08-03\` — the raw record, and the
fallback when a curated note is missing or disputed.

**In flight (nothing is finished, nothing is lost):**
| Workstream | Progress |
|---|---|
| A — Rule 20 retroactive review | 1 of 6 |
| B — 12-item source mining | 1 of 12 |
| C — 6 untranscribed YouTube videos | 0 of 6 |
| D — Platform / hosting research | not started |

**Rough cost per workstream** (from real measured sessions — budget is a
live constraint, so plan before starting):

| Work | Realistic cost | Notes |
|---|---|---|
| One mining/review item (A2–A6, B2–B12) | ~7–10 min, one agent | A1 and B1 both landed in this range |
| A6 — the 17 videos | Larger — 2 big files | Highest payoff, but split it; don't one-shot |
| C — fetch 6 transcripts | Minutes, no agent | `fetch_transcripts.py`, pure API |
| D — platform research | 5 agents as scoped | The most expensive item queued |
| Doc/note work | **Not cheap** | One session went fresh→100% on *one* agent plus note-keeping |

**Agent or solo?** Rule 11 (default to agents) and Rule 13 (scope small)
both apply. The resolution: **one agent per source file** — that is what
worked. A1 and B1 were single-file and succeeded; the original 3
broad-scope agents covering many files each died producing nothing. Don't
read many files in one agent, and don't spawn an agent for something a
grep answers.

**If a session dies mid-workstream:** partial work is not lost — it is
either on disk (uncommitted, readable via `git diff`) or in the agent
transcript. Finish the *current item*, save it, then stop. **Never leave an
item half-analysed with no note** — a half-finished review that looks
complete is worse than an obviously unstarted one. Mark it in the checklist
as partial and say what remains.

**⚠️ Never use `git checkout <file>` to undo a test edit.** It reverts the
*whole* file, including unrelated uncommitted work. This destroyed real
content on 2026-08-03 (this very section). Remove the specific line with
`sed`, or commit good work before running any experiment.

Full agenda with per-item detail:
[`reference/PENDING_agent_prompts_resume_2026-08-01.md`](reference/PENDING_agent_prompts_resume_2026-08-01.md)
(its filename is dated; its contents are current — this file supersedes it
as the entry point).

---

## 2. Next action

**The user's own instruction (2026-08-03), verbatim:**

> *"1st test the save project we made today worked then present the
> checklist progress report and to do list and suggest starting point"*

Do these in order. **Do not pick a workstream first** — the user
deliberately declined to choose one until after this report.

**Step 1 — test that the save system actually worked.** Run §0's checks
above, and confirm each mechanism does what it claims:

```bash
cd "C:\Users\AwBro\Desktop\automated clipper bot"
git log --oneline -3                            # matches this file's header?
git status --short                              # clean?
grep -cE '^[0-9]+\. ' CLAUDE.md                 # matches §4's count?
bash check_links.sh                             # all links resolve?
grep -o '[a-f0-9]\{7\}' SESSION_HANDOFF_PROMPT.md   # NO stale hash
```

Then confirm the parts a cold session depends on: the `SessionStart` hook
injected the repo state at the top of this session (it prints HEAD and the
uncommitted count — check it against the real values), `~/.claude/CLAUDE.md`
loaded even though the working directory may not be this repo, and
`.claude/session-prompts.log` has the prior session's prompts.

**Report honestly.** Four cold-start passes were run on 2026-08-03 and
*every one found real bugs*. Assume this one will too — a pass that finds
nothing should be treated as a weak test, not a clean bill of health.

**Step 2 — present the progress report, checklist, and to-do list.** From
§1 and §3 of this file plus `SESSION_HANDOFF_PROMPT.md` §1's open checklist.
Lead with the honest headline (**zero pipeline code exists**) so a list of
finished infrastructure cannot imply progress that did not happen.

**Step 3 — suggest a starting point, then stop and let the user decide.**
Workstreams A–D are in §3 with cost estimates. Recommend one and say why,
but the choice is the user's under Rule 10.

---

## 3. Blockers & open leads

**Waiting on the user:**
- **Rules 8 and 9** — ⚠️ provisional, Gemini-sourced, adopted without
  authorization. Need a yes/no or they get dropped.
- **Rule 22** — see §2.
- **Usage headroom** — confirm before launching any agents. Budget is a
  live constraint: metered, hard weekly reset **Monday 1pm**, hit
  repeatedly. Last session went fresh to 100% on *one* agent plus
  note-keeping. Documentation work is not cheap.

**Unverified leads — check these before related build work, not after:**
1. **Does the sibling project's video code still run?** Two `.mp4` files
   dated 2026-07-27 exist on disk at
   `C:\Users\AwBro\Desktop\youtube auto videos\`. Their existence is
   verified; whether the current code produced them, and whether it still
   works, is **not**. Do not treat as proven.
2. **Is `validate_environment.py` one auth fix from passing?** One Colab
   cell settles it and resolves the project's stated credentials blocker.

**Known real defect, unfixed:** `chat_downloader`'s Twitch GraphQL path
throws a reproducible `KeyError: 'data'`. Needs defensive `.get()` chaining
plus Tenacity backoff before Stage 1 depends on it.

**A discussion is queued, not decided:** the "autonomy prompt" for the
eventual build phase —
[`reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md`](reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md).
Five open questions at the end need the user's answers.

---

## 3b. Questions only the user can answer

**First: check the repo before asking anything.** The user's standing
point (2026-08-03): *"in the github and drive are the whole of our work u
can refer back to those for any questions too."* The entire history is
here — every verbatim source document, every research report, every
decision and its reasoning, plus full `git log`. **If a question is
answerable from the files, answer it yourself.** Search before asking:

```bash
grep -ril "<term>" . --include=*.md      # search every doc
git log --oneline --all | head -40       # what happened, in order
git log -p --follow <file>               # how one file evolved and why
```

The commit messages are deliberately detailed — they record *why*, not
just *what*. They are a primary source, not metadata.

The questions below are the residue: things genuinely **not** in any file
because they can't be — decisions, preferences, and facts about the
outside world. **Ask them when they become relevant, not all at once.**
Marked ⚡ where an answer unblocks real work.

**Decisions currently owed (ask early):**
1. ⚡ **Rule 22** — adopt "updating `START_HERE.md` is the last action of
   every session, non-skippable"? Yes/no.
2. ⚡ **Rules 8 & 9** — keep or drop? Both Gemini-sourced, adopted without
   authorization: ffmpeg `-movflags +faststart`, and `.ass`/`\an5` karaoke
   captions.
3. ⚡ **Usage headroom** — how much budget is left this session? Required
   before launching any agents.
4. **Workstream order** — A, B, C, or D first? The user picks.

**Scope and direction:**
5. **Which streamer(s) beyond Lacy**, if any? The architecture supports a
   multi-creator `config.json`, but only Lacy is scoped.
6. **Is the Clipping.net campaign still live**, and are the dollar figures
   in the planning docs current? Research could not confirm the specific
   "$5,000 X pool / $20,000 multi-platform" figures as presently active —
   they may describe a 2024 campaign.
7. **VOD-only, or live monitoring too?** This is load-bearing: it decides
   whether a streaming ASR (Kyutai) matters at all, and whether the bot
   needs always-on hosting. Planning docs say live; the Get Clips path is
   VOD-based.
8. **The 5 open questions** in
   [`reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md`](reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md)
   about the eventual build-phase autonomy prompt.

**Things only the user can run or check:**
9. ⚡ **Run `validate_environment.py` in Colab** — one cell, settles the
   credentials blocker. Claude cannot run Colab.
10. **Did the sibling project's video actually get produced by the current
    code, and does it still run?** The user watched those `.mp4` files;
    that first-hand account is faster than any archaeology.
11. **Pull Drive** after every push — Claude has no Drive access.
12. **Twitch Developer credentials** — only the user can create the app.

**When something is genuinely ambiguous:** ask rather than guess, but do
everything that *doesn't* depend on the answer first (Rule 10 — the user
directs, but that isn't a licence to stall).

---

## 4. How we work

**Read [`CLAUDE.md`](CLAUDE.md) and apply it** — 21 numbered rules, 16
active (3, 5, 7, 10–21 minus the removed/provisional ones). Rule 22 is
*proposed only* and is not in the file. They are strict defaults;
deviating from one requires asking first.

The ones that actually get broken, so check against these specifically:

- **The user has final say** on phase transitions and on anything being
  called "complete." Report what was done and how it was tested — the
  verdict is theirs. *(Rule 10)*
- **Nothing is factual** unless confirmed this session or the user OK'd
  it. Past notes, old docs, other AI output, and Claude's own earlier
  conclusions are leads to verify, not facts to build on. *(Rule 12)*
- **External-AI material is reference only** — including its "rules" and
  confident technical claims. Ask about items individually; never
  batch-adopt. *(Rule 14)*
- **Run every check BEFORE reporting done**, not after the user asks.
  Audit against the conversation, check cross-file consistency, check
  stale values, confirm the save landed. *(Rule 21)*
- **Preserve source material word-for-word** — never condense,
  summarize, or placeholder it. Applies to agent reports too. *(Rule 15)*
- **Keep raw records separate from evaluation.** Never edit a raw record
  to reflect a later finding. *(Rule 16)*
- **Don't dismiss free tools** — evaluate against all five roles
  (primary / fail-safe / cross-check / assist / feature). *(Rule 20)*
- **Don't waste tokens.** Scope agents small, save incrementally, do the
  free thing first, read narrowly. *(Rule 13)*

**Saving:** Claude pushes to GitHub; the user pulls into Drive. Claude has
**no** Drive access. A fresh Colab runtime needs `drive.mount()` before the
pull works:
```python
!git -C "/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt" pull
```

**Raw session transcripts** are backed up outside the repo (they are
~66MB and `.gitignore`d, so they must never be committed). Latest:
`C:\Users\AwBro\Desktop\AI\claude_transcripts_backup_2026-08-03\`
(precedent: `claude_evidence_backup_2026-07-30`). Source of truth lives at
`C:\Users\AwBro\.claude\projects\C--Users-AwBro-Desktop-youtube-auto-videos\*.jsonl`
— local app data, **not guaranteed to survive app updates or cache
clearing** (the failure report §24 documents source material already lost
this way). Re-run the backup when a session produces significant work:
```bash
cp -n "/c/Users/AwBro/.claude/projects/C--Users-AwBro-Desktop-youtube-auto-videos"/*.jsonl \
      "/c/Users/AwBro/Desktop/AI/claude_transcripts_backup_<DATE>/"
```
These are the raw record. The curated notes in this repo are a *selection*
— and that selection has failed at least once (the `START_HERE.md` design
was discussed, approved, and nearly lost). The transcripts are the fallback
when a note is missing or disputed.

---

## 5. Where things are

| What | Where |
|---|---|
| **SAVE EVERYTHING protocol** — the 9-step sequence run when the user says save | [`SAVE_PROTOCOL.md`](SAVE_PROTOCOL.md) |
| **Session handoff prompt** — ready-to-paste catch-up block + its template | [`SESSION_HANDOFF_PROMPT.md`](SESSION_HANDOFF_PROMPT.md) |
| **Live agenda, per-item detail** | [`reference/PENDING_agent_prompts_resume_2026-08-01.md`](reference/PENDING_agent_prompts_resume_2026-08-01.md) |
| **Rules** | [`CLAUDE.md`](CLAUDE.md) |
| **Project status, architecture, backlog** | [`PROJECT.md`](PROJECT.md) — current as of 2026-08-02 |
| **~110 tools with URLs + roles** — read before picking any tool | [`reference/MASTER_TOOLS_CATALOG_2026-08-02.md`](reference/MASTER_TOOLS_CATALOG_2026-08-02.md) |
| Reusable code from the sibling project | [`SALVAGE_INVENTORY.md`](SALVAGE_INVENTORY.md) |
| Rule 20 retroactive review (workstream A) | [`reference/retroactive_rule20_review_2026-08-02.md`](reference/retroactive_rule20_review_2026-08-02.md) |
| Platform/hosting research scope (workstream D) | [`reference/research_targets_platforms_2026-08-02.md`](reference/research_targets_platforms_2026-08-02.md) |
| Queued discussion — autonomy prompt | [`reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md`](reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md) |
| Raw source material, verbatim | `reference/handoff_2026-08-01_*.md` |
| Research reports, verbatim | `reference/*_VERBATIM.md` |
| Pre-flight checks | [`validate_environment.py`](validate_environment.py) |
| Link-rot checker (run from §0) | [`check_links.sh`](check_links.sh) |
| Transcript fetcher (hit 17/17 previously) | `research/fetch_transcripts.py` |

**Outside this repo:**
| What | Where |
|---|---|
| Sibling project (salvage source) | `C:\Users\AwBro\Desktop\youtube auto videos\pipeline.py` (~4,059 lines) |
| The quality bar / failure history | `C:\Users\AwBro\Desktop\AI\claude_failure_report.md` |
| Raw research inputs | `C:\Users\AwBro\Desktop\AI\automated clipper bot\` |
| User's Drive copy | `/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt` |
| Real Python (`python`/`py` do NOT resolve) | `C:\Users\AwBro\AppData\Local\Programs\Python\Python312\python.exe` |
