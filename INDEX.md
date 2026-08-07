# INDEX — every document in this repo, what's in it, and when to read it

**Why this file exists.** On 2026-08-04 the user observed that finished work
kept reading as missing: *"it seems like these were done well just lost and
unorganized even those i asked. i wonder if we lost more things."* They were
right, and it was measurable. A findability audit checked every source
document against the three files a session actually reads
(`PROJECT.md`, `START_HERE.md`, `PENDING_...md`) and found **12 of 30 were
mentioned in none of them** — including all three Hugging Face research
reports, which had nearly been lost once already and were re-saved verbatim
at the user's explicit insistence.

Nothing was actually lost. But a file nothing points at is *functionally*
lost, because no future session will ever open it. **That is the gap this
index closes.**

**How to use it:** find the row for what you need, read the "read it when"
column. Sizes are real. Every path is a working link — `check_links.sh`
verifies them.

---

> **⚠️ Reading anything dated before 2026-08-06?** It will describe
> `@CoreCrashOuts` as the target streamer. That framing is **superseded** —
> the target is the whole **CORE group**, and `@CoreCrashOuts` is the user's
> own channel where clips get posted. See the SCOPE CORRECTION at the top of
> [`START_HERE.md`](START_HERE.md). Raw records are deliberately left
> uncorrected (Rule 16).

> **Looking for WHERE a file physically lives?** [`FILE_MAP.md`](FILE_MAP.md)
> maps every folder and file with real sizes, what each naming convention
> means, which files must never be edited, what lives outside the repo, and a
> "where do I find...?" lookup table. Three indexes, three questions:
> FILE_MAP = where · INDEX = when to read · HANDOFF_REPORT = what it means.

## 1. Start here / how we work

| File | What it is | Read it when |
|---|---|---|
| [`START_HERE.md`](START_HERE.md) | **The session entry point.** State now, next action, blockers, questions only the user can answer, where things live. Overwritten each session. | **First, every session.** Run its §0 self-validation before trusting it. |
| [`CLAUDE.md`](CLAUDE.md) | 21 numbered operating rules, 16 active. Each written because a specific failure happened, with the failure recorded. | Before doing any work. These are strict defaults. |
| [`SAVE_PROTOCOL.md`](SAVE_PROTOCOL.md) | The 9-step sequence run when the user says *"save everything"*, plus the written format for every section of `START_HERE.md`. | When saving, or when unsure what a save must include. |
| [`SESSION_HANDOFF_PROMPT.md`](SESSION_HANDOFF_PROMPT.md) | §1 is the ready-to-paste catch-up block for a new session; §2 is its template; §3 its maintenance rules. | At the end of a session, to regenerate the paste block. |
| [`PROJECT.md`](PROJECT.md) | Status, architecture outline with sourcing, the honest implemented-vs-aspirational checklist, deferred backlog. | Before making any claim about status or architecture. |
| [`README.md`](README.md) | Public front door. Short by design. | Only when the public presentation matters. |

## 2. Live agenda

| File | What it is | Read it when |
|---|---|---|
| [`reference/PENDING_agent_prompts_resume_2026-08-01.md`](reference/PENDING_agent_prompts_resume_2026-08-01.md) | **The running status board** — workstreams A–K with per-item detail and the exact agent prompts to reuse. 1,037 lines. Filename is dated; contents are current. | Before starting any workstream item. Don't re-derive a prompt that's already written here. |

## 3. Decision-ready synthesis — read these to actually choose something

| File | What it is | Read it when |
|---|---|---|
| [`reference/MASTER_TOOLS_CATALOG_2026-08-02.md`](reference/MASTER_TOOLS_CATALOG_2026-08-02.md) | ~110 tools, one consolidated URL-complete index by pipeline stage. Each carries a real URL, where it came from, verification status, and its **Rule 20 role** (primary / fail-safe / cross-check / assist / feature). | **Before picking any tool.** This is the answer to "what are our options here." |
| [`reference/verified_tools_catalog.md`](reference/verified_tools_catalog.md) | Decision-ready merge of the 17-video research and three Gemini dossiers, every claim traced to a real check. | When you want the short list rather than everything. |
| [`SALVAGE_INVENTORY.md`](SALVAGE_INVENTORY.md) | Reusable functions/patterns from the sibling project's production `pipeline.py`, each confirmed to exist at the stated location. | **Before writing any new function.** Rule 1 — port, don't re-derive. |
| [`reference/retroactive_rule20_review_2026-08-02.md`](reference/retroactive_rule20_review_2026-08-02.md) | Workstream A: re-examining already-"complete" work for free tools dismissed too readily. 1 of 6 items done. | When working A, or when a tool was rejected and you want to know why. |
| [`reference/research_targets_platforms_2026-08-02.md`](reference/research_targets_platforms_2026-08-02.md) | Workstream D scope: platforms, free inference routes, galleries, hosting. Suggested 5-agent split. | When starting D. |

## 4. Deep dives — real source code, read directly, not from READMEs

These are the most technically load-bearing documents in the repo. All four
were produced by reading actual repository source via `gh api`.

| File | What it is | Read it when |
|---|---|---|
| [`reference/deep_dive_openshorts.md`](reference/deep_dive_openshorts.md) | `mutonby/openshorts`, 2,784★ — "the strongest, most production-hardened reference found across all research." Source of `snap_clip_to_words()`, the single most important technique found. 1,266 lines. | **Stage 3 or 4 work.** Start here before designing either. |
| [`reference/deep_dive_moment_detection.md`](reference/deep_dive_moment_detection.md) | How three real repos actually decide "this is the moment" — real function names, verbatim excerpts. 1,230 lines. | Stage 3. This is the core open question of the project. |
| [`reference/deep_dive_ingestion_and_pipelines.md`](reference/deep_dive_ingestion_and_pipelines.md) | `TwitchDownloader` (C#), `stream-clipper` (Rust/Tauri), `AI-auto-segment-edit-video-pipeline` (Python). 1,362 lines. | Stage 1, or when considering an alternative overall architecture. |
| [`research/tool_verification.md`](research/tool_verification.md) | Independent live GitHub/PyPI verification of an external AI's "50 concrete tools" list. The audit trail behind every verified claim. | When you need to know whether a specific tool claim was ever actually checked. |

## 5. Verbatim agent reports — never condensed, per Rule 15

⚠️ **These four were invisible before 2026-08-04** — referenced by no
document a session reads. Three of them had already been nearly lost once
and were re-saved word-for-word at the user's explicit insistence.

| File | What it is | Read it when |
|---|---|---|
| [`reference/research_2026-08-01_huggingface_audio_transcription_VERBATIM.md`](reference/research_2026-08-01_huggingface_audio_transcription_VERBATIM.md) | ASR alternatives to faster-whisper, diarization, **audio emotion/event classification for detecting screaming** — verified against live HF model cards. | Stage 2, or any work on detecting excitement from audio. |
| [`reference/research_2026-08-01_huggingface_vision_detection_VERBATIM.md`](reference/research_2026-08-01_huggingface_vision_detection_VERBATIM.md) | Face detection/tracking vs MediaPipe BlazeFace, expression recognition, game-context detection. Verified from live pages. | Stage 4 face tracking / dynamic crop. |
| [`reference/research_2026-08-01_huggingface_local_llm_judging_VERBATIM.md`](reference/research_2026-08-01_huggingface_local_llm_judging_VERBATIM.md) | Structured-JSON / function-calling models vs Llama 3.2, local TOS-safety classifiers, hook-quality scoring, real benchmarks. | Stage 3's LLM scoring, or picking the local judging model. |
| [`reference/mining_2026-08-01_deep_dive_moment_detection_VERBATIM.md`](reference/mining_2026-08-01_deep_dive_moment_detection_VERBATIM.md) | Workstream B item 1 of 12 — full 5-lens extraction (portable code / fixable code / free tools / efficiency / corrections). 675 lines. | The model for what a B item should produce. |

| [research_2026-08-06_core_clippers_named_VERBATIM.md](reference/research_2026-08-06_core_clippers_named_VERBATIM.md) | **H1 — the first REAL repost data.** 25 X posts via api.fxtwitter.com (public JSON, unauthenticated), 18 durations, 5 frames viewed. **Reposts median 51.4s, 44% at 55–61s, 0 of 18 on Twitch presets → hand-trimmed.** Contradicts the Architecture Outline: no 9:16, no subtitles, chat burned in. Zero hashtags in 25 captions. Sample is search-sourced so it favours winners. | **Before designing Stage 4 (cut/format) or Stage 5.** |

### Workstream G — transcript mining (2026-08-04, in progress)

| File | What it is | Read it when |
|---|---|---|
| [`reference/mining_2026-08-04_mVqnCvE337E_VERBATIM.md`](reference/mining_2026-08-04_mVqnCvE337E_VERBATIM.md) | **G1 — How Lacy Got Used On Stream.** 108KB, 1,741 timestamp citations. ⚠️ **Hostile secondary source** — adversarial narrator who admits prior errors. Every claim about people/events is a lead, not a fact. States plainly what it cannot answer: no VOD timecodes, no view counts, no Clipping.net mechanics. | Detection signals and hook patterns — after reading its framing warning. |
| [`reference/research_2026-08-04_core_clippers_discovery_VERBATIM.md`](reference/research_2026-08-04_core_clippers_discovery_VERBATIM.md) | **H2 — CORE clipper discovery + scene conventions.** 31KB, 22 VERIFIED / 2 UNVERIFIED, full source list. No handle invented; every one resolves to a real URL. **Flagged that @CoreCrashOuts could not be found — RESOLVED 2026-08-06: the output channel was simply renamed to @CoreCrashOuts.** | CORE scene conventions, and before trusting the target handle. |
| [`reference/mining_2026-08-04_cVkFMpDLQrM_VERBATIM.md`](reference/mining_2026-08-04_cVkFMpDLQrM_VERBATIM.md) | **G2 — the curated best-of. The most directly usable document in the repo for Stage 3.** 50 moments segmented from a labelled dataset, with real clip-length statistics (median 39.5s), 7 moment types, a text-only detection signal, hook-opening distribution, and 3 corrections that would each have broken the planned detector. 811 timestamp citations. | **Before designing Stage 3 detection or Stage 4 cut lengths.** |
| [`reference/mining_2026-08-04_lYafPAHVOno_VERBATIM.md`](reference/mining_2026-08-04_lYafPAHVOno_VERBATIM.md) | **G3 — Lacy Content Strategy Breakdown.** 101 timestamp citations, 10 honest NOTHING-FOUND entries. Key: the source is **third-party commentary, not Lacy**, and it states **zero hook principles and zero thresholds**. Explicitly says: do not seed Stage 3 defaults from this file. | Stage 3 strategy context — but read its SOURCE NATURE header first. |

## 6. Verbatim raw source — external material, reference only

**Rule 16: raw record and evaluation never blend.** Nothing in this section
is verified. Treat every claim as a lead, not a fact (Rule 12).

| File | What it is | Read it when |
|---|---|---|
| [`reference/handoff_2026-08-01_master_planning_session_raw.md`](reference/handoff_2026-08-01_master_planning_session_raw.md) | ⚠️ *Was invisible.* **919 lines** — the full Gemini planning-session export: master blueprint, campaign constraints, the Tier 1/Tier 2 rationale, payout structure. The richest single source document in the project. | When you need the original campaign requirements or the full planning rationale. |
| [`reference/handoff_2026-08-01_78source_tool_directory.md`](reference/handoff_2026-08-01_78source_tool_directory.md) | ⚠️ *Was invisible.* The 78-source "Definitive Master Tool & Resource Directory" as given. Superseded for decisions by the MASTER_TOOLS_CATALOG, but this is the original. | To check what the directory originally claimed about a tool. |
| [`reference/handoff_2026-08-01_chat_pasted_originals.md`](reference/handoff_2026-08-01_chat_pasted_originals.md) | Everything pasted into chat that session, reproduced exactly. | To recover an original instruction's exact wording. |
| [`reference/handoff_2026-08-01_evaluation.md`](reference/handoff_2026-08-01_evaluation.md) | The **analysis** of the above — deliberately a separate file. | After reading the raw material, for what was made of it. |
| [`reference/handoff_2026-08-01_step8_gateway_v1.md`](reference/handoff_2026-08-01_step8_gateway_v1.md) · [`_v3.md`](reference/handoff_2026-08-01_step8_gateway_v3.md) | ⚠️ *Were invisible, zero inbound links.* Two versions of the "Step 8 Gateway" handoff, showing real drift between drafts (v1 playwright-based; v3 chat-downloader-based). Both contain a known defect: they swallow exceptions while claiming to be fail-closed. | Comparing how the plan changed — and as a worked example of code that violates its own stated rule. |
| [`reference/gemini_dossier_1_raw.md`](reference/gemini_dossier_1_raw.md) · [`2`](reference/gemini_dossier_2_raw.md) ⚠️ · [`3`](reference/gemini_dossier_3_raw.md) ⚠️ · [`4`](reference/gemini_dossier_4_raw.md) ⚠️ · [`5`](reference/gemini_dossier_5_raw.md) ⚠️ · [`6`](reference/gemini_dossier_6_raw.md) | Six Gemini dossiers, verbatim. **Dossier 3 is known fabricated.** Dossiers 4, 5 and 6 were each *originally saved as condensed paraphrases* and had to be replaced with the true originals — the exact failure Rule 15 exists to prevent. ⚠️ marks the four that were invisible. | Only alongside `tool_verification.md`, which says which claims survived checking. |
| [`reference/gemini_suggestions.md`](reference/gemini_suggestions.md) | Gemini code dump, reviewed and found to contain real bugs. User: *"GEMNI CODE IS ALWAYS BAD. WE JUST USE IT FOR REFERENCE."* | As a cautionary reference only. |
| [`reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md`](reference/DISCUSS_next_phase_autonomy_prompt_2026-08-02.md) | **NOT ADOPTED — discussion notes.** The autonomy-prompt idea plus the research-vs-code sequencing question. Ends with 5 open questions for the user. | Before the research→build phase transition. |

## 7. Video research — 23 transcripts, all with source URLs

| File | What it is | Read it when |
|---|---|---|
| `research/transcripts/*.txt` | **23 full transcripts.** Every file carries its YouTube URL on line 2 and every line is timestamped `[MM:SS]`, so any quote can be verified at the exact second. Batch 1 = 17 videos (`_summary.txt`); batch 2 = 6 videos fetched 2026-08-04 (`_summary_batch2.txt`). | Whenever a claim traces back to a video — go to the raw words. |
| [`research/RESEARCH_YOUTUBE_SOURCES.md`](research/RESEARCH_YOUTUBE_SOURCES.md) | Recovery of 17-video research that existed only in chat and was dropped by a context-compaction event. | Overview of what the 17 videos collectively established. |
| [`reference/PENDING_agent_prompts_resume_2026-08-01.md`](reference/PENDING_agent_prompts_resume_2026-08-01.md) §F/G/H | **Workstreams added 2026-08-04**: F = sweep the `AI\` folder for never-imported material; G = mine the 6 new transcripts for detection thresholds and hook patterns; H = CORE clipper research on X. Each carries its full agent prompt. | Before starting F, G or H. |
| [`research/fresh_pass_videos_1-9.md`](research/fresh_pass_videos_1-9.md) · [`10-17`](research/fresh_pass_videos_10-17.md) | Careful from-scratch re-study of all 17, reading full real transcripts and descriptions. Redone because the first pass was lost to compaction. | Per-video detail. **Workstream A6 targets these two files.** |

**The 3 Lacy videos (fetched 2026-08-04) are the highest-value item here** —
they are the only source anywhere for *what a clip-worthy Lacy moment
actually looks like*, which is what Stage 3's detection thresholds and hook
patterns have to be built against:

| Video | ID | Snippets |
|---|---|---|
| How Lacy Got Used On Stream | `mVqnCvE337E` | 2,337 |
| Lacy's Best Streamer University Moments | `cVkFMpDLQrM` | 1,068 |
| Lacy's Content Strategy Breakdown | `lYafPAHVOno` | 397 |

Also newly available: **`PafYu69s5NA` — "Claude + Whop Clipping Workflow"**,
which opens by describing a clip *"found, analyzed, cut, and captioned
automatically and completely for free with Claude."* That is this project's
exact problem statement, from someone who already built it.

## 7b. First-party data — the only ground truth in the repo

| File | What it is | Read it when |
|---|---|---|
| [`research/twitch_clips/FINDINGS_2026-08-06_lacy_clips.md`](research/twitch_clips/FINDINGS_2026-08-06_lacy_clips.md) | **964 real Lacy clips, 7 days, with durations and view counts.** Median 30s but 71% are Twitch UI presets; G2's 20-70s band corroborated at 89%. Views are power-law: median 5, only 0.6% reach 1,000. | **Before setting any Stage 3 threshold**, and before assuming the payout maths work. |
| [`research/twitch_clips/lacy_clips_7d_2026-08-06.txt`](research/twitch_clips/lacy_clips_7d_2026-08-06.txt) | The raw 964 rows: `duration|view_count|title`. | Re-running the analysis, or building the J1 eval harness. |

## 7c. Handoff and audit

| File | What it is | Read it when |
|---|---|---|
| [`HANDOFF_REPORT_2026-08-06.md`](HANDOFF_REPORT_2026-08-06.md) | **Full professional handoff.** 13 parts: architecture, all measured data, open questions, where evidence contradicts the plan, repository map, workstream status, the save system, the unverified attack findings, and an honest accounting of cost and waste. Written to be read cold by anyone. | **First, if you are new to this project** — or handing it to someone else. |
| [`reference/research_2026-08-06_save_system_attack_VERBATIM.md`](reference/research_2026-08-06_save_system_attack_VERBATIM.md) | **8 findings against the save system, verbatim.** ⚠️ **NONE VERIFIED** — every skeptic assigned to refute them died on a session limit. Two critical, one a privacy issue affecting the **sibling** repo. Leads, not facts. | Before trusting the save system, and before working workstream K. |

## 8. Code

| File | What it is | Read it when |
|---|---|---|
| [`validate_environment.py`](validate_environment.py) | Pre-flight checks (ffmpeg, API keys, Twitch credentials) with a deliberate hard-block vs soft-warn distinction. All 8 previously-logged defects fixed. | Before any real run. **Not yet run green** — needs one Colab cell. |
| [`research/fetch_transcripts.py`](research/fetch_transcripts.py) | Batch 1 fetcher. Succeeded 17/17. | As the proven pattern to copy. |
| [`research/fetch_transcripts_batch2.py`](research/fetch_transcripts_batch2.py) | Batch 2 fetcher, 6/6. Refuses to overwrite an existing transcript. | To add more videos — edit the `VIDEOS` list. |
| [`hooks_backup/`](hooks_backup/) | **Copies of the 4 lifecycle hooks + the user-level CLAUDE.md**, which live in `~/.claude/` and are therefore OUTSIDE version control. If that folder is lost the whole resume system goes with it. Includes the ported live-handoff mechanism. | Restoring the hooks, or reading how the continuous save works. |
| [`save_check.sh`](save_check.sh) | **The gate for "save everything."** 11 checks on outcomes, not intentions. Exit non-zero means the save is NOT done. Written 2026-08-04 after three protocol steps were silently skipped in a paid session. | Step 5 of SAVE_PROTOCOL, and from START_HERE §0. |
| [`check_links.sh`](check_links.sh) | Verifies every relative markdown link across the key docs. Wired into the `Stop` hook. | Automatically, and from `START_HERE.md` §0. |

---

## Outside this repo

| What | Where |
|---|---|
| Sibling project — the salvage source | `C:\Users\AwBro\Desktop\youtube auto videos\pipeline.py` (~4,059 lines) |
| The quality bar / failure history | `C:\Users\AwBro\Desktop\AI\claude_failure_report.md` (1,400 lines, evidence-cited) |
| Raw research inputs, un-imported | `C:\Users\AwBro\Desktop\AI\automated clipper bot old\` |
| Session transcript backups | `C:\Users\AwBro\Desktop\AI\claude_transcripts_backup_2026-08-03\` (~66MB) |
| User's Drive copy | `/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt` |
| Real Python (`python`/`py` do **not** resolve) | `C:\Users\AwBro\AppData\Local\Programs\Python\Python312\python.exe` |

---

## Maintaining this file

**Add a row whenever a file is added.** A document with no row here is
invisible in practice, which is the whole problem this file was created to
fix — 12 files sat unreferenced for days despite being finished work the
user had specifically asked for.

Re-run the findability audit any time:

```bash
cd "C:\Users\AwBro\Desktop\automated clipper bot"
for f in $(git ls-files 'reference/*.md' 'research/*.md'); do
  b=$(basename "$f")
  n=$(grep -c -F "$b" INDEX.md PROJECT.md START_HERE.md 2>/dev/null | awk -F: '{s+=$2} END{print s}')
  [ "$n" -eq 0 ] && echo "INVISIBLE: $f"
done
```
