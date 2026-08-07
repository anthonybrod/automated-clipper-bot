# FILE MAP — every folder, every file, what's in it, where to find things

**What this is.** A physical map of everything saved, folder by folder, with
real sizes. Use it to answer *"where is X?"*

**How this differs from the other two indexes** — all three are needed:

| File | Answers |
|---|---|
| **`FILE_MAP.md`** (this file) | **Where is it?** Physical location, size, folder purpose |
| [`INDEX.md`](INDEX.md) | **When should I read it?** Purpose and reading order |
| [`HANDOFF_REPORT_2026-08-06.md`](HANDOFF_REPORT_2026-08-06.md) | **What does it all mean?** Findings, status, open questions |

*Verified against the filesystem 2026-08-07. Sizes are real bytes.*

---

# 1. ROOT — the documents a session reads

| File | Size | What it is |
|---|---|---|
| [`START_HERE.md`](START_HERE.md) | 37 KB | **Session entry point.** §0 self-validation · sources/destinations · THE METHOD · state now · next action · blockers · §3b questions only the owner can answer · how we work · where things are |
| [`PROJECT.md`](PROJECT.md) | 64 KB | **Stated single source of truth.** Status, architecture outline with sourcing, implemented-vs-aspirational checklist, deferred backlog |
| [`CLAUDE.md`](CLAUDE.md) | 30 KB | **21 numbered rules, 16 active.** Each records the failure that caused it. Removed: 2, 4, 6, 8, 9. **No Rule 17 exists** |
| [`HANDOFF_REPORT_2026-08-06.md`](HANDOFF_REPORT_2026-08-06.md) | 31 KB | **Full transfer document, 13 parts.** Read first if you are new |
| [`SESSION_HANDOFF_PROMPT.md`](SESSION_HANDOFF_PROMPT.md) | 34 KB | §1 ready-to-paste prompt · §2 template · §3 maintenance rules |
| [`INDEX.md`](INDEX.md) | 21 KB | Document catalogue by purpose and reading order |
| [`FILE_MAP.md`](FILE_MAP.md) | this | Physical map — where everything lives |
| [`SAVE_PROTOCOL.md`](SAVE_PROTOCOL.md) | 14 KB | 9-step save sequence + the written `START_HERE.md` format |
| [`SALVAGE_INVENTORY.md`](SALVAGE_INVENTORY.md) | 38 KB | **Reusable code from the sibling project**, each confirmed to exist at the stated location. **Read before writing any function (Rule 1)** |
| [`README.md`](README.md) | 5 KB | Public front door |

### Root — executable

| File | Size | What it does | Status |
|---|---|---|---|
| [`final_save.sh`](final_save.sh) | 5.9 KB | **Complete save**: transcripts + .claude/ buffers + settings.json + integrity checks + save_check | ✅ |
| [`save_check.sh`](save_check.sh) | 6.9 KB | **11 checks that GATE the save.** Non-zero exit = save not done | ✅ working |
| [`check_links.sh`](check_links.sh) | 1.2 KB | Link rot across 121 links | ⚠️ K7 — always exits 0 despite documenting exit 1 |
| [`validate_environment.py`](validate_environment.py) | 12 KB | Pre-flight: ffmpeg, API keys, Twitch credentials. All 8 logged defects fixed | ⚠️ **never run green** — needs one Colab cell |
| [`requirements.txt`](requirements.txt) | 3.5 KB | ✅ **REBUILT 2026-08-07.** Was 4 lines covering NONE of the architecture's tools — a fresh clone could not run either research script. Now pins real verified versions, marks faster-whisper as an undecided candidate (Rule 6), flags ffmpeg + chat-downloader as not installed, and documents every credential |

---

# 2. `reference/` — 32 files, 1.1 MB. Research, sources, agent reports

**The naming convention tells you what a file is:**

| Pattern | Means | Editable? |
|---|---|---|
| `*_VERBATIM.md` | Agent report, word-for-word | ❌ **Never** (Rule 15/16) |
| `*_raw.md`, `handoff_2026-08-01_*` | Raw external source as supplied | ❌ **Never** (Rule 16) |
| `deep_dive_*.md` | Read directly from real repo source via `gh api` | ✅ analysis |
| `mining_*`, `research_*` | Dated agent output | ❌ verbatim |
| Everything else | Synthesis and catalogues | ✅ |

### 2a. Deep dives — real source code, not READMEs *(the most technically load-bearing files)*

| File | Size | Contains |
|---|---|---|
| `deep_dive_ingestion_and_pipelines.md` | 89 KB | TwitchDownloader (C#), stream-clipper (Rust), AI-auto-segment-edit-video-pipeline (Python) |
| `deep_dive_moment_detection.md` | 88 KB | How 3 real repos decide "this is the moment", with real function names |
| `deep_dive_openshorts.md` | 77 KB | `mutonby/openshorts`, 2,784★. **Source of `snap_clip_to_words()`** — the single most important technique found |

### 2b. Agent reports — verbatim, never condensed

| File | Size | Contains |
|---|---|---|
| `mining_2026-08-04_mVqnCvE337E_VERBATIM.md` | 109 KB | G1 — Lacy drama. 1,741 citations. ⚠️ hostile secondary source |
| `mining_2026-08-01_deep_dive_moment_detection_VERBATIM.md` | 84 KB | B1 — 5-lens extraction, the model for B2–B12 |
| `mining_2026-08-04_cVkFMpDLQrM_VERBATIM.md` | 56 KB | **G2 — the curated best-of. Best detection source in the repo.** 50 moments, hook distribution, the text-only repetition detector |
| `research_2026-08-04_core_clippers_discovery_VERBATIM.md` | 32 KB | H2 — CORE scene, 22 VERIFIED claims |
| `research_2026-08-06_core_clippers_named_VERBATIM.md` | 30 KB | H1 — 25 real X reposts. ⚠️ sample is mostly **non-Lacy** |
| `mining_2026-08-04_lYafPAHVOno_VERBATIM.md` | 28 KB | G3 — content strategy. ⚠️ third-party commentary, contradicts itself |
| `research_2026-08-06_save_system_attack_VERBATIM.md` | 24 KB | **8 findings against the save system. ⚠️ NONE VERIFIED** → workstream K |
| `research_2026-08-01_huggingface_audio_transcription_VERBATIM.md` | 14 KB | ASR alternatives, **audio event detection for screaming** |
| `research_2026-08-01_huggingface_local_llm_judging_VERBATIM.md` | 13 KB | Structured-JSON models, TOS classifiers, hook scoring |
| `research_2026-08-01_huggingface_vision_detection_VERBATIM.md` | 13 KB | Face detection vs BlazeFace, expression recognition |

### 2c. 🔧 TOOLS — start here when choosing anything

| File | Size | Contains |
|---|---|---|
| **`MASTER_TOOLS_CATALOG_2026-08-02.md`** | **34 KB** | **~110 tools by pipeline stage.** Real URL, origin, verification status, and Rule 20 role (primary / fail-safe / cross-check / assist / feature). **Read before picking any tool** |
| `verified_tools_catalog.md` | 26 KB | Decision-ready short list, every claim traced to a real check |
| `handoff_2026-08-01_78source_tool_directory.md` | 11 KB | The original 78-source directory as supplied (raw) |
| `../research/tool_verification.md` | 52 KB | **The audit trail** — live GitHub/PyPI checks. Where 4 hallucinated repos were caught |

### 2d. Live agenda and planning

| File | Size | Contains |
|---|---|---|
| `PENDING_agent_prompts_resume_2026-08-01.md` | 65 KB | **The running status board.** Workstreams A–K with per-item detail and **full reusable agent prompts** |
| `retroactive_rule20_review_2026-08-02.md` | 12 KB | Workstream A — free tools dismissed too readily. 1 of 6 |
| `DISCUSS_next_phase_autonomy_prompt_2026-08-02.md` | 12 KB | **NOT ADOPTED.** Ends with 5 open questions for the owner |
| `research_targets_platforms_2026-08-02.md` | 8.7 KB | Workstream D scope |

### 2e. Raw external source — reference only, never edited

| File | Size | Contains |
|---|---|---|
| `handoff_2026-08-01_master_planning_session_raw.md` | 64 KB | **919 lines** — the richest single source. Campaign constraints, Tier 1/2 rationale, payout structure |
| `handoff_2026-08-01_chat_pasted_originals.md` | 19 KB | Everything pasted into chat, exactly |
| `gemini_dossier_6_raw.md` | 18 KB | Master architecture + ecosystem index |
| `handoff_2026-08-01_evaluation.md` | 12 KB | The **analysis** of the above — deliberately separate |
| `gemini_dossier_1_raw.md` · `2` · `3` · `4` · `5` | 5–10 KB each | ⚠️ **Dossier 3 is fabricated.** 4, 5, 6 were once wrongly saved condensed and had to be replaced |
| `handoff_2026-08-01_step8_gateway_v1.md` · `v3.md` | 4–5 KB | Two drafts showing real drift. Both swallow exceptions while claiming fail-closed |
| `gemini_suggestions.md` | 4.5 KB | Gemini code found to contain real bugs. Cautionary only |

---

# 3. `research/` — 6 files + 23 transcripts, 929 KB. Video research and data

| File | Size | Contains |
|---|---|---|
| `fresh_pass_videos_1-9.md` | 63 KB | Careful re-study of 9 videos. **Workstream A6 target** |
| `fresh_pass_videos_10-17.md` | 55 KB | The other 8. **A6 target — split, don't one-shot** |
| `tool_verification.md` | 52 KB | Live GitHub/PyPI verification audit trail |
| `RESEARCH_YOUTUBE_SOURCES.md` | 42 KB | Recovery of 17-video research lost to a compaction event |
| `fetch_transcripts.py` | 3.6 KB | Batch 1 fetcher — succeeded 17/17 |
| `fetch_transcripts_batch2.py` | 2.9 KB | Batch 2 — 6/6. Refuses to overwrite existing files |

### `research/transcripts/` — 23 transcripts + 2 summaries, 623 KB

**Format:** line 1 = title · **line 2 = source YouTube URL** · then `[MM:SS] text`
per line. Every quote is checkable at the exact second.
`_summary.txt` (batch 1, 17 videos) · `_summary_batch2.txt` (batch 2, 6 videos)

**The 3 Lacy transcripts — the only source for what a clip-worthy Lacy moment
looks like:**

| ID | Video | Snippets |
|---|---|---|
| `mVqnCvE337E` | How Lacy Got Used On Stream | 2,337 |
| `cVkFMpDLQrM` | Best Streamer University Moments *(curated best-of)* | 1,068 |
| `lYafPAHVOno` | Lacy's Content Strategy Breakdown | 397 |

**Not yet mined (G4/G5/G6):** `PafYu69s5NA` (351) · `mFOoNPFylLI` (521) ·
`QqwNue_KL-4` (145). **`PafYu69s5NA` is the highest-value unread file in the
repo** — it opens describing this project's exact problem, already solved.

### `research/twitch_clips/` — the only first-party ground truth

| File | Size | Contains |
|---|---|---|
| `lacy_clips_7d_2026-08-06.txt` | 25 KB | **964 real clips**, format `duration\|view_count\|title` |
| `FINDINGS_2026-08-06_lacy_clips.md` | 4.8 KB | The analysis with caveats stated inline |

**Reproduce it:**
```bash
"C:/Users/AwBro/AppData/Local/Programs/Python/Python312/python.exe" -m yt_dlp \
  --flat-playlist --print "%(duration)s|%(view_count)s|%(title)s" \
  "https://www.twitch.tv/lacy/clips?range=7d"
```

---

# 4. `hooks_backup/` — 5 files, 24 KB

Copies of what lives in `~/.claude/` (outside version control).

| File | Backs up |
|---|---|
| `clipper-bot-session-start.sh` | SessionStart — injects repo state + session-state buffer |
| `clipper-bot-log-prompt.sh` | UserPromptSubmit — logs prompts + injects the live-handoff directive |
| `clipper-bot-precompact.sh` | PreCompact — snapshots before context dies |
| `clipper-bot-session-close.sh` | Stop — reminds to update `START_HERE.md` |
| `user-level-CLAUDE.md` | The user-level instructions that load in **every** session |

> ⚠️ **`settings.json` IS NOT BACKED UP** — and it is the only thing that
> *registers* the hooks. Restoring this folder alone yields four inert scripts
> that fail silently. **That is finding K6.**
> Also: `~/.claude/hooks/` contains `clipper-bot-session-close.sh.bak`, which
> has no counterpart here.

---

# 5. Runtime scaffold — empty by design

`audit_logs/` · `checkpoints/` · `clips_out/` · `dead_letter/` · `review/` ·
`transcripts/` — each holds a `.canary` file. Recovered from a Drive export;
proof a bootstrap step ran successfully once. **Do not delete.**

`__pycache__/` — build artifact, ignorable.

---

# 6. `.claude/` — 🔒 GITIGNORED, NEVER COMMIT

| File | Contains |
|---|---|
| `session-prompts.log` | **Every owner prompt, verbatim**, timestamped. 1085 lines |
| `session-state.md` | Durable facts appended live during sessions |

**This is a PUBLIC repo.** These hold raw conversation. They are the fallback
when a curated note is missing or disputed — and **backed up nowhere** (K6).
See K1: an unverified finding says the sibling repo does *not* ignore
`.claude/` and has a public remote.

---

# 7. Outside the repo

| What | Where | Notes |
|---|---|---|
| Live hooks | `C:\Users\AwBro\.claude\hooks\` | 4 active + 1 `.bak` |
| Hook registration | `C:\Users\AwBro\.claude\settings.json` | ⚠️ **not backed up** |
| User-level instructions | `C:\Users\AwBro\.claude\CLAUDE.md` | Loads in **every** session, any directory |
| **Sibling project** | `C:\Users\AwBro\Desktop\youtube auto videos\pipeline.py` | ~4,059 lines. **The salvage source (Rule 1)** |
| Quality bar | `C:\Users\AwBro\Desktop\AI\claude_failure_report.md` | 1,400 lines, evidence-cited |
| Transcript backups | `AI\claude_transcripts_backup_{08-03,04,06,07}\` | ~68 MB each. Also `claude_evidence_backup_2026-07-30` |
| Un-imported research | `AI\CLIP BOT STUFF\`, `AI\auto clipper bot #2\`, `AI\automated clipper bot old\`, `AI\tmp_openshorts\`, `AI\Random dumps unorganized\` | **Workstream F — the owner triages these. DO NOT sweep unprompted** |
| Owner's Drive copy | `/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt` | Owner pulls in Colab; Claude cannot write |
| **Real Python** | `C:\Users\AwBro\AppData\Local\Programs\Python\Python312\python.exe` | `python` and `py` do **not** resolve |

---

# 8. Quick answers — "where do I find…?"

| I need… | Go to |
|---|---|
| **A tool for a pipeline stage** | `reference/MASTER_TOOLS_CATALOG_2026-08-02.md` |
| **Whether a tool claim was ever checked** | `research/tool_verification.md` |
| **Code I can reuse instead of writing** | `SALVAGE_INVENTORY.md` → sibling `pipeline.py` |
| **How to cut a clip accurately** | `reference/deep_dive_openshorts.md` (`snap_clip_to_words()`) |
| **How to detect a moment** | `reference/mining_2026-08-04_cVkFMpDLQrM_VERBATIM.md`, then `deep_dive_moment_detection.md` |
| **Real numbers** (length, views, hooks) | `research/twitch_clips/FINDINGS_2026-08-06_lacy_clips.md` |
| **What a good clip looks like posted** | `reference/research_2026-08-06_core_clippers_named_VERBATIM.md` |
| **The exact words of a video** | `research/transcripts/<video_id>.txt` |
| **What to work on next** | `reference/PENDING_agent_prompts_resume_2026-08-01.md` |
| **A prompt to re-run a dead agent** | Same file — they are written out in full |
| **Why a rule exists** | `CLAUDE.md` — each records its own failure |
| **What the owner said, exactly** | `.claude/session-prompts.log` |
| **Campaign / payout terms** | `reference/handoff_2026-08-01_master_planning_session_raw.md` |
| **What is broken in the save system** | `reference/research_2026-08-06_save_system_attack_VERBATIM.md` + PENDING §K |

---

## Maintaining this file

Add a row when you add a file. Re-verify sizes with:

```bash
cd "C:\Users\AwBro\Desktop\automated clipper bot"
ls -1S reference/ | while read f; do printf "%8s  %s\n" "$(wc -c <"reference/$f")" "$f"; done
```
