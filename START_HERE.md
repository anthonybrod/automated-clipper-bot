# START HERE

**The single entry point for this project. Read this first, every session.**

Last updated: **2026-08-03** · Repo state at last update: `d966155`, clean,
local = GitHub = Drive.

This file is a **router, not a duplicate** — it points at the real sources
rather than restating them, so nothing can drift out of sync. It is
**overwritten each session**, not appended; history lives in git.

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
- 15 active operating rules, each written because a specific failure
  happened

**In flight (nothing is finished, nothing is lost):**
| Workstream | Progress |
|---|---|
| A — Rule 20 retroactive review | 1 of 6 |
| B — 12-item source mining | 1 of 12 |
| C — 6 untranscribed YouTube videos | 0 of 6 |
| D — Platform / hosting research | not started |

Full agenda with per-item detail:
[`reference/PENDING_agent_prompts_resume_2026-08-01.md`](reference/PENDING_agent_prompts_resume_2026-08-01.md)
(its filename is dated; its contents are current — this file supersedes it
as the entry point).

---

## 2. Next action

**Propose Rule 22 and get an explicit yes or no from the user.**

`START_HERE.md` now exists (this file). The remaining half of that task is
the part that makes it *automated* rather than aspirational:

> **Proposed Rule 22:** Updating `START_HERE.md` is the last action of
> every session, immediately before the final commit and push. Not
> optional, not skippable — and it happens even when a usage limit is
> cutting the session short.

Not adopted. Per Rule 14, no rule is adopted without the user's explicit
confirmation. **Ask, don't assume.**

After that resolves, the user picks the order of workstreams A–D.

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

## 4. How we work

**Read [`CLAUDE.md`](CLAUDE.md) and apply it** — 21 rules, 15 active.
They are strict defaults; deviating from one requires asking first.

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

---

## 5. Where things are

| What | Where |
|---|---|
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
| Transcript fetcher (hit 17/17 previously) | `research/fetch_transcripts.py` |

**Outside this repo:**
| What | Where |
|---|---|
| Sibling project (salvage source) | `C:\Users\AwBro\Desktop\youtube auto videos\pipeline.py` (~4,059 lines) |
| The quality bar / failure history | `C:\Users\AwBro\Desktop\AI\claude_failure_report.md` |
| Raw research inputs | `C:\Users\AwBro\Desktop\AI\automated clipper bot\` |
| User's Drive copy | `/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt` |
| Real Python (`python`/`py` do NOT resolve) | `C:\Users\AwBro\AppData\Local\Programs\Python\Python312\python.exe` |
