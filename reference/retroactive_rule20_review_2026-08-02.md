# Retroactive Rule 20 review — tools dismissed too readily in already-completed work

**Why this file exists.** Rule 20 was added 2026-08-02 after the user
reviewed saved research and found working free tools had been dismissed
too easily. The user then directed: *"lets go back and retroactively apply
that on work that had been marked as completed."* This file is that pass.

**What this is NOT.** It does not edit any raw report. Per Rule 16, the
`*_VERBATIM.md` files stay exactly as the agents wrote them, including
verdicts now judged wrong. This is the separate evaluation layer.

**The test being applied (Rule 20's five roles).** A tool that loses the
"primary pick" slot can still win another:
1. **Primary** — main implementation for a stage
2. **Backup / fail-safe** — takes over when primary breaks, is
   rate-limited, out of quota, or too expensive for a run
3. **Cross-check** — independent second signal to verify the primary
4. **Assist** — free local pre-filter narrowing work before an expensive
   stage
5. **Feature / quality add** — enables something otherwise not possible

**Also applied:** free changes the math (a free local tool costs nothing
in reserve); never judge on stars/README-tone/age alone; a set-aside must
record *why* and *what would bring it back*.

**Status: 1 of 4 completed reports reviewed.** Checkpointed and pushed
per report — see the progress table at the bottom.

---

## Report 1 — `research_2026-08-01_huggingface_audio_transcription_VERBATIM.md`

Original report's structure: an 18-row table, then "What's genuinely worth
considering" (4 items) and "What sounds relevant but isn't" (5 items).
The second section is where the Rule 20 problem concentrates — several
items were sorted into "isn't" purely because they lose the primary slot.

### 🔴 MAJOR MISS — Kyutai STT (row 7), dismissed as "Not a clear fit"

**Original verdict:** *"architecturally aimed at live conversational
latency, not the buffered/batched clip-review workflow this project uses;
low current adoption (135 likes) makes it a riskier bet."*

**Why that's wrong — it contradicts this project's own stated Phase 1.**
The evaluation measured it against *VOD/batch* processing. But the
project's core objective, stated in every version of the handoff, is
**monitoring LIVE streams** for crashout moments in real time:

> *"Monitor Lacy's live streams for statistical engagement outliers"*
> — PROJECT.md core objectives
> *"Stream Listener: chat-downloader monitors Twitch IRC chat stream while
> pydub tracks audio decibels in the background"* — the pipeline design

Live monitoring is precisely the workload Kyutai is built for, and it is
a workload **faster-whisper does not serve well** — faster-whisper is a
batch transcriber. The report compared a streaming tool against a batch
requirement, found it didn't fit, and stopped.

**Role assignment (Rule 20):** **Role 5 — feature enabler**, for the live
path specifically. Also partially **Role 4 (assist)**: its built-in
*semantic* VAD (endpointing on meaning, not just silence) is a smarter
trigger than a raw dB threshold for "the streamer just finished a
sentence worth clipping."

**Concrete facts (from the original report, unchanged):** decoder-only
streaming ASR (Moshi architecture), **0.5s delay** for the 1B en+fr model,
2.5s for 2.6B en-only, semantic VAD built in, card claims noise
robustness, CC-BY-4.0, `pip install moshi` or transformers ≥4.53.

**What would keep it excluded:** if the project settles on VOD-only
ingestion (`yt-dlp` pulling completed VODs) and drops live monitoring
entirely. That is a real possibility — the Get Clips path is VOD-based —
but it is a *scope decision that hasn't been made*, not a property of the
tool. **Unverified**: 135 likes is low; nobody has tested its real
accuracy on gaming audio.

### 🟠 `pyannote/segmentation-3.0` (row 10) — undersold

**Original verdict:** *"useful only if you also adopt diarization, since
VAD alone gives you nothing segmentation-3.0 doesn't already fold into the
diarization pipeline."*

**The missed capability: overlapped-speech detection.** The report names
it, then treats it as a diarization sub-feature. But **two people talking
over each other is itself a highlight signal** — arguments, hype moments,
someone getting cut off mid-sentence. For a channel literally named
@CoreCrashOuts, targeting *"stream arguments, rage moments"* per the
campaign brief, overlap is close to a direct proxy for the target content.

**Role assignment:** **Role 5 (feature)** — an argument/overlap detector
usable standalone, no diarization required. Secondarily **Role 3
(cross-check)** against chat-spike and audio-RMS signals; a moment where
overlap, chat velocity, and loudness all coincide is far stronger than any
one alone (this is the same logic as the already-adopted 1.5× "combo
bonus").

**Real friction, unchanged:** MIT but **gated** — needs an HF token and
accepting conditions. Not zero-setup.

### 🟠 `FunAudioLLM/SenseVoiceSmall` (row 13) — half-right dismissal

**Original verdict was correct on the specific claim** — it genuinely
lacks screaming/shouting classes despite sounding perfect for that, and
flagging it as a "sounds right, isn't" case was good work.

**But the dismissal overshot.** Its actual event classes include
**laughter** and **applause**. Laughter is a real, high-value highlight
signal for a reaction streamer — arguably second only to screaming. And
it does ASR + emotion + events **in a single pass at a claimed 5× faster
than Whisper-Small**, which is a genuinely different cost profile from
running separate models.

**Role assignment:** **Role 4 (assist)** — a fast combined pre-pass that
flags laughter-dense windows before expensive scoring runs.

**What keeps it provisional (this part of the original stands):** the
custom FunASR license with an ambiguous "prohibited behavior" clause is a
real blocker for a monetized channel and must be resolved before any
production use. Also primarily benchmarked on Mandarin/Cantonese, English
secondary — **unverified** on English gaming audio.

### 🟡 `usefulsensors/moonshine` (row 6) — "Wrong fit. Skip."

**Original reasoning was sound for the primary slot** — it optimizes for
cheap edge hardware, and its own card admits hallucination/repetition.

**But it's MIT-licensed and tiny (27M/61M params).** Two roles survive:
- **Role 2 (fail-safe):** a Colab session with no GPU, or a local CPU-only
  run, still executes a 27M model. Degraded transcription beats none.
- **Role 4 (assist):** hallucination matters far less for *"is there
  speech in this window at all"* than for final captions. A rough fast
  pass to locate speech regions is a legitimate use of a weak-but-fast ASR.

**What would drop it:** if Parakeet or distil-whisper prove fast enough on
CPU to make a third tier pointless. **Unverified** — nobody has measured
CPU-only throughput for any of these on this project's hardware.

### 🟡 Emotion-model cluster (rows 14, 15, 16) — sorted individually, never as an ensemble

Original verdicts: `ehcalabres` *"use with caution"*, `firdhokk` *"training
data is still small acted corpora"*, `superb/wav2vec2-base-superb-er`
*"Weakest of the emotion options found — skip"*.

**Each critique is individually valid** — RAVDESS/SAVEE/TESS are actors
reading scripted lines, which genuinely may not transfer to spontaneous
Twitch reactions. That caution was correct and should stand.

**What was missed: they were never considered together.** These are three
Apache-2.0 models with **different training data** (RAVDESS vs.
RAVDESS+SAVEE+TESS+URDU vs. IEMOCAP). Independently-trained models
agreeing is a meaningfully stronger signal than any one alone — and
disagreement is itself useful information (flag for human review).

**Role assignment:** **Role 3 (cross-check)** as a small ensemble.
`superb`'s dismissal as "weakest" is exactly the star-count-style
reasoning Rule 20 warns against — for an ensemble member, *different
training data* is the value, not standalone accuracy. It has 77,316
downloads/mo and is Apache-2.0.

**Honest caveat:** three models trained mostly on acted speech may share
the *same* blind spot on spontaneous audio, in which case agreement proves
little. **Unverified** — needs a real test on actual Lacy clips before
being trusted.

### 🟢 Dismissals that were correct — no change

- **`audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim` (row 17)** —
  explicitly research-only; commercial use needs a paid license. Correctly
  excluded for a monetized channel. *(Narrow exception worth noting: using
  it offline to benchmark/calibrate thresholds is not commercial
  deployment — but shipping it is out, and that line should be checked
  with the user before relying on it.)*
- **Silero VAD HF mirrors (row 18)** — correctly identified as already
  bundled inside faster-whisper. Genuinely a non-finding. Good catch.
- **`nvidia/parakeet-tdt-0.6b-v3` (row 5)** — already correctly held as an
  optional GPU path, with the real NeMo-dependency and CC-BY-4.0
  license-change caveats noted. No change needed.
- **`openai/whisper-large-v3-turbo` (row 1)** — correctly identified as
  base weights needing CT2 conversion. *(Minor addition: it remains
  directly usable via `transformers` if a CT2 conversion ever fails —
  a Role 2 fallback path, no new download required.)*

### Summary — Report 1

| Tool | Original verdict | Rule 20 role | Priority |
|---|---|---|---|
| Kyutai STT | "Not a clear fit" | **5 — feature (live path)** | 🔴 High |
| `pyannote/segmentation-3.0` | "only if you adopt diarization" | **5 + 3 — overlap = argument detector** | 🟠 Med-high |
| SenseVoiceSmall | "Right idea, incomplete fit" | **4 — laughter pre-filter** | 🟠 Medium (license blocker) |
| `moonshine` | "Wrong fit. Skip." | **2 + 4 — CPU fail-safe** | 🟡 Low-med |
| `superb`, `ehcalabres`, `firdhokk` | "skip" / "use with caution" | **3 — ensemble cross-check** | 🟡 Low-med |
| `audeering`, Silero mirrors, Parakeet, whisper-turbo | correct as-is | — | ✅ No change |

**The pattern across all five misses:** each tool was measured against a
single assumed workload (batch VOD transcription, or standalone accuracy)
and discarded when it didn't win *that* comparison — without asking
whether it served a different role, or whether the assumed workload was
even the only one this project has. Kyutai is the clearest case: it was
judged against batch processing when the project's stated Phase 1 is live
monitoring.

**Nothing here is adopted.** These are re-opened candidates with roles
assigned, per Rule 12 — no tool listed above has been tested on real Lacy
audio, and none should be treated as a decision.

---

## Progress

| # | Completed report | Rule 20 review |
|---|---|---|
| 1 | `research_2026-08-01_huggingface_audio_transcription_VERBATIM.md` | ✅ done |
| 2 | `research_2026-08-01_huggingface_vision_detection_VERBATIM.md` | ⬜ pending |
| 3 | `research_2026-08-01_huggingface_local_llm_judging_VERBATIM.md` | ⬜ pending |
| 4 | `mining_2026-08-01_deep_dive_moment_detection_VERBATIM.md` | ⬜ pending |
| 5 | The 78-source tool-directory audit (in `handoff_2026-08-01_evaluation.md` §1) | ⬜ pending |
| 6 | **The 17 already-mined YouTube videos** — `research/fresh_pass_videos_1-9.md` + `research/fresh_pass_videos_10-17.md` | ⬜ pending |

**On item 6 (added 2026-08-02 at user direction):** those two files were
themselves already a *second* pass, commissioned because a first pass had
compressed real content away. They are the largest single body of
"completed" research in the project and the most likely place for
dismissed free tools to be buried — video creators name tools in passing
constantly, and a first-pass reader optimizing for "which tool wins"
would drop most of them. Expect this to be the highest-yield item in
workstream A.
