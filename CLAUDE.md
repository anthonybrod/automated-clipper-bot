# Working on this repo

> ## 🚩 RESUMING? READ THIS FIRST
>
> **[`reference/PENDING_agent_prompts_resume_2026-08-01.md`](reference/PENDING_agent_prompts_resume_2026-08-01.md)**
> is the live pick-up point. It is written to be read cold, with no memory
> of any prior conversation. It contains:
> - the 12-item mining progress table (1 done, 11 pending, 1 to skip),
> - the exact prompt wording that produced the one successful report,
> - the mine → check → save → commit → push procedure,
> - two open leads to verify (does the sibling project's video code still
>   work; is `validate_environment.py` one auth fix from passing),
> - and the user's standing instruction: **ask before launching agents,
>   and confirm usage headroom first.**
>
> Do not reconstruct the plan from memory or from chat history — read that
> file. Then read this file's rules, then `PROJECT.md`.

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

**Provenance audit (run 2026-08-01 after the user pointed out that not all
of these came from this session — Rule 12 applied to the rules
themselves):**

**The pattern this audit found**: Claude repeatedly converted *agreements
about a specific claim* into *binding forward-looking rules*. Confirming
"yes, that's an accurate restatement" or "yes, that's contamination" is
**not** the same as "adopt this as a standing rule." Only rules where the
user was explicitly asked "adopt this as a rule?" and said yes — or which
the user stated themselves, in their own words — count as adopted.

**A second principle the user stated while pruning these**: *"we dont know
the best service and model cuz we are in the research stage."* Tool/model/
threshold choices are **research outputs, not rules**. Don't pre-commit
the answer to a question the research hasn't answered yet. Documented
preferences and reasoning belong in `PROJECT.md`'s Architecture Outline
(where they can be revised freely); this file is for how we *work*, not
which library wins.

- **Genuinely adopted, active rules**: 3, 5, 7, 10, 11, 12, 13, 14, 15,
  16, 17, 18, 19, 20. (13–19 added at the end of the 2026-08-01 session:
  cost discipline, the accuracy cluster — external-AI material is
  reference-only, preserve source verbatim, keep raw record separate from
  evaluation — plus save-to-GitHub-and-Drive-per-agent, and verify agent
  reports against real source before saving them. 14–16 and 18 restate
  standing user rules that were being followed but had never been written
  into this numbered list; 19 documents the check step that was actually
  executed and proven this session. **20 added 2026-08-02** after the user
  reviewed the saved research and found free, working tools had been
  dismissed too readily — it defines five roles every tool gets evaluated
  against, not just "is it the primary pick.")
- **REMOVED 2026-08-01 at the user's direction**: 2, 4, 6. Each entry
  below records what was actually agreed vs. what got written, and where
  the underlying finding still lives.
- **⚠️ PROVISIONAL, never authorized**: 8, 9 (see below).
- **Inherited from a prior session, not re-confirmed today**: 1.
- **⚠️ Rules 8 and 9 — NOT user-confirmed.** Both came from Gemini's
  "Last Mile Technicalities" list and were adopted by Claude's own
  judgment without asking, in direct conflict with this repo's standing
  rule that external-AI material is reference-only until the user says
  otherwise. They are marked below as **PROVISIONAL** and should be either
  confirmed by the user or dropped. They may well be technically correct —
  that is not the point; they weren't authorized.
- **Rule 1 — carried over, not re-confirmed this session.** It is a real,
  pre-existing standing rule already documented in this repo before today
  (see the "Hard rule" paragraph above), so it isn't invented — but the
  earlier note calling it "reconfirmed here" was inaccurate. Treat as
  inherited, not freshly OK'd.

Resolved one at a time with the user against real Gemini-sourced planning
material, following an explicit process: nothing from Gemini becomes a rule
just because Gemini said it, even when it overlaps with something true —
only what the user explicitly confirms. Full resolution process and
reasoning: `reference/handoff_2026-08-01_evaluation.md`. Once adopted,
these are followed automatically; any real reason to deviate gets raised
with the user first, not silently decided.

1. *(inherited from a prior session — not re-confirmed 2026-08-01)*
   **Reuse verified logic over re-deriving** (restates the hard rule
   above, not new).
2. ~~**Chat-spike detection defaults to Z≥2.5 chat-velocity statistics.**~~
   **REMOVED 2026-08-01 at the user's direction**: *"we dont need this
   rule we will find out whats best when that time comes."* The user had
   confirmed that Claude's *restatement* of the technique was accurate,
   which Claude then wrongly treated as authorization to lock the
   threshold in as a binding default. The underlying technique (z-score
   over chat velocity, from `twitch-clip-miner`'s real implementation) is
   still documented in `PROJECT.md`'s Architecture Outline and in the
   mining report — **the specific threshold is to be determined
   empirically when that stage is actually built**, not pre-committed here.
3. **AI judge/verification calls fail closed, scoped.** Hook-quality
   scoring, TOS/content checks, Ollama context-check: any exception or
   unparseable response = reject, never silently pass. Does **not** extend
   to pre-flight hard/soft checks or human-review-gate timeouts — those
   keep their own existing, separate logic.
4. ~~**No synthesized-narration audio mixing.**~~ **REMOVED 2026-08-01 at
   the user's direction — was never actually agreed as a rule.** What the
   user approved was *dropping Gemini's contaminated audio-mix claim*
   ("Narration 100% / Music 15% / SFX 10% to maintain mentorship tone",
   which was bled in from the sibling Parents Teach Kids project). Their
   words: "Yes, drop it — contamination." Claude then converted that into
   a standing prohibition on narration mixing generally, which is a
   different and broader thing than what was agreed. The original
   contamination finding still stands and is recorded in
   `reference/handoff_2026-08-01_evaluation.md`; it just isn't a rule.
5. **Flaky third-party API wrapper calls (`chat-downloader` and similar) get
   Tenacity exponential backoff + jitter by default.**
6. ~~**faster-whisper is the default/primary transcription engine.**~~
   **REMOVED 2026-08-01 at the user's direction**: *"delete 6 we will find
   the best free service after research"* / *"we dont know the best
   service and model cuz we are in the research stage."* Locking in a
   transcription engine now would pre-commit the outcome of research that
   hasn't happened yet — and this session's own Hugging Face pass already
   surfaced real candidates worth evaluating against it (notably
   `distil-whisper/distil-large-v3`, documented as ~6.3x faster than
   large-v3 at ~0.2% WER difference). faster-whisper remains the
   *currently-favored* option in `PROJECT.md`'s Architecture Outline, with
   the reasoning intact — it is simply not a binding rule, and the
   comparison is explicitly still open.
7. **VOD-list caching**: content-hash keyed (skip re-querying Twitch if the
   source manifest is unchanged) plus persisted URL, title, and content
   notes per VOD — extend the real `pipeline_tasks`/`payout_logs` schema
   found in a `Lacy_Clip_Bot` Drive export (see the evaluation file), don't
   design a new one from scratch.
8. ⚠️ **PROVISIONAL — Gemini-sourced, never authorized by the user.**
   MP4 exports always get `-movflags +faststart`.
9. ⚠️ **PROVISIONAL — Gemini-sourced, never authorized by the user.**
   Karaoke/animated captions always use `.ass` format with `\an5`
   centering — never plain `.srt` for that use case.
10. **The user has final say before any phase transition, and before
    anything is marked complete or finished.** Report what was done and
    how it was tested — the "complete/finished" designation itself belongs
    to the user, never something declared unilaterally.
11. **Default to multiple parallel background agents for research/
    verification/mining work spanning multiple independent sources** — act
    as director/orchestrator (scope each agent tightly, synthesize what
    comes back), not as the one doing every read serially.
12. **Nothing is factual unless it was confirmed in this session, or the
    user personally gave the OK.** The user's exact words (2026-08-01):
    *"if we didn't confirm it in this session and i didn't personally give
    the ok then its not factual."* Everything else — notes from past
    sessions, claims in older docs, another AI's output, prior projects'
    documentation, and **my own earlier conclusions** — is a lead to
    verify, not a fact to build on. Context: *"we had many ai
    hallucinations on the way here and ai going off notes from past
    projects it was very messed up."*

    **How to apply, concretely:**
    - State the *scope* of what was actually checked, never more. "Two
      files exist at this path with these sizes" is not "the pipeline
      works." Evidence supports a specific claim, not the interesting
      claim next to it.
    - Label every claim: **factual** (verified this session / user-
      confirmed), **inference** (reasoning from evidence, could be wrong),
      or **unverified** (a lead). Never let the second two get written
      down in the voice of the first.
    - Evidence that is merely *in tension with* an existing claim does not
      disprove it. Don't rewrite or "correct" existing documentation on
      the strength of a suggestive finding.
    - This applies hardest to my own prior output in the same session —
      an earlier conclusion of mine is not a fact just because I wrote it
      confidently. **Caught in practice 2026-08-01**: I labeled a finding
      "CONFIRMED," called two existing documents "factually false," and
      instructed a future agent to re-grade salvage entries as "proven,"
      when all I had actually verified was that two `.mp4` files existed
      on disk. The user caught it. See the correction notice in
      `reference/PENDING_agent_prompts_resume_2026-08-01.md` for the
      corrected version.
13. **Don't waste tokens. The user's time and money are real constraints,
    not background noise.** This user is on a metered plan with hard daily
    and weekly limits, has hit them repeatedly, and has paid out of pocket
    to keep working. Wasted spend directly costs them.

    **How to apply, concretely:**
    - **Scope agents small.** A broad multi-file agent that dies takes
      everything with it. One source per agent, verified and saved
      immediately. Proven this session: 3 broad agents = 48 minutes and
      zero output; 1 narrow agent = ~7.5 minutes and a complete verified
      report.
    - **Save incrementally, never batch.** Commit and push each item as it
      passes its check. Work that isn't pushed can vanish on a limit hit.
    - **Do the free thing first.** Before spending on research, check
      whether the answer already exists in the repo, in a transcript, or
      in a file on disk. Three completed research reports were re-saved
      verbatim this session at zero cost because the data already existed
      — it had just never been written down properly.
    - **Don't re-run what already succeeded.** Check for existing output
      before launching anything.
    - **Read narrowly.** Grep or read specific line ranges instead of
      pulling whole large files into context when a targeted check answers
      the question.
    - **Say what something will cost before spending it**, and take the
      user's stop signals literally and immediately — "hold on more
      agents till we get more limit" means stop, not finish-this-first.
    - **Rework is the most expensive failure mode.** Getting it wrong and
      redoing it costs more than the extra minute of care up front. This
      is the practical argument for Rules 10 and 12, not just a principle.
14. **External-AI material (Gemini and anything like it) is reference
    only. The user has the final word on every piece of it.** The user's
    exact words (2026-08-01): *"i dont want gemnios rules ever unless i
    say so"* and *"we use it for reference and i say the final word."*

    Nothing from an external AI becomes a rule, a fact, or a design
    decision because it sounded authoritative — **including its
    "rules," directives, and confident technical claims.** Ask about
    items individually and get a real yes/no; do not batch-adopt, and do
    not substitute independent verification for actually asking (caught
    this session: Claude verified two Gemini claims against real source
    code instead of asking the user first, which was a different action
    than the one requested). Track record justifying this: across two
    verification passes this session, external-AI material produced 4
    hallucinated repo-owner attributions, a fabricated tool capability, a
    fabricated algorithm parameter, a wrong component recommendation
    caught three separate times, and cross-project contamination — mixed
    in with genuinely useful material, which is exactly what makes it
    dangerous to trust wholesale.
15. **Preserve source material word-for-word. Never condense, summarize,
    paraphrase, or placeholder it.** The user's exact words: *"rule: word
    for word non condensed we need the originals."* Applies to pasted
    source material, external-AI output being recorded, and **completed
    agent reports** — a report that gets summarized into a synthesis
    instead of saved whole is a report the user cannot actually review or
    learn from. Caught this session: three completed Hugging Face research
    reports had been folded into a summary rather than saved, which the
    user correctly called out as making the work effectively null. They
    were then saved verbatim at zero additional cost.
16. **Keep the raw record and the evaluation of it in physically separate
    places.** Verbatim source goes in its own file; analysis, corrections,
    and commentary go in a clearly separate one. Never edit a raw record
    to reflect a later finding — even when the finding is correct. (In
    practice: `reference/handoff_*_chat_pasted_originals.md` holds
    untouched source including claims later proven false;
    `reference/handoff_*_evaluation.md` is where those are corrected.)
18. **Save to GitHub AND Google Drive after each agent completes — never
    batch, never wait for a whole wave.** The user's exact words
    (2026-08-01): *"When we save after an agent... we SAVE in github and
    google drive in our project folder so we avoid timeouts, usage limits,
    wasted tokens, time and u just making things up."*

    **Claude can only do half of this, and must say so rather than imply
    otherwise.** There is no Google Drive Desktop app on this machine
    (verified 2026-08-01: no process, no install directory, no synced
    drive letter) and no Drive API access. Claude commits and pushes to
    GitHub; **Drive updates only when the user runs the Colab pull cell**,
    which does a `git pull` into
    `/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt`. That cell is
    saved in the plan file and confirmed working (2026-08-01, real run,
    17 files pulled).

    So: after each push, **state plainly that GitHub is done and Drive is
    pending the user's pull** — do not report "saved to GitHub and Drive"
    as if both happened. The rule's purpose is durability against
    timeouts and limit hits; GitHub alone achieves that, and Drive is the
    user's convenience copy.
19. **Verify agent/subagent reports against the real source before
    accepting or saving them.** Grep the actual source file for several
    distinctive claims from the report — exact quoted strings, hashes,
    unusual numbers, structural claims. Only save and commit once it
    passes, and record what was checked. Proven this session: a mining
    report passed 9/9 spot-checks (including a persisted-query SHA-256
    hash, an exact quoted bug, and a structural claim about duplicate
    headings), which is what made it trustworthy enough to commit — and
    the one discrepancy found (a line count off by one) was recorded
    rather than hidden.
20. **Don't dismiss working free tools. Evaluate every one against five
    roles, not just "is it the primary pick."** The user's direction
    (2026-08-02): *"not to dismiss so easily and explore tools as back ups
    and fail safes, or to check our work or assist, and add features and
    quality to raise our intern level project to the top level."*

    **The five roles — a tool that loses one can still win another:**
    1. **Primary** — the main implementation for a pipeline stage.
    2. **Backup / fail-safe** — takes over when the primary breaks, is
       rate-limited, is out of quota, or is too expensive for a given run.
       This project already has a real crash (`chat_downloader`'s
       `KeyError`) proving primaries do fail in production.
    3. **Cross-check / verification** — a second, independent signal to
       confirm the primary's output. Especially valuable where a silent
       wrong answer is the failure mode.
    4. **Assist** — narrows the work before an expensive stage runs (a
       free local pre-filter ahead of a paid LLM call is the archetype).
    5. **Feature / quality add** — enables something the pipeline
       otherwise wouldn't do at all.

    **Rules of evaluation:**
    - **Free changes the math.** A free, local, offline tool costs nothing
      to keep in reserve. "Gemini can also do that" is not a reason to
      discard a free tool — Gemini costs real tokens per call and this
      project's cost philosophy is explicit that budget is a first-class
      constraint.
    - **Never judge on star count, README tone, or age alone.** Read what
      it actually does. Two repos (`Kuonirad/AutoCutAI`, `htekdev/vidpipe`)
      were nearly written off on exactly those signals and turned out to
      contain real working implementations. Unmaintained ≠ non-functional.
    - **When a tool is set aside, record WHY and under what condition it
      would come back** — never a bare "not needed." Write it into the
      relevant reference doc so it's recoverable rather than lost.
    - **State the role you're assigning**, not just a verdict. "Not
      primary — keep as free fail-safe for Stage 2" is a real answer;
      "not needed" is not.

    **Why this rule exists — the actual track record it corrects:**
    `fer`/MTCNN (dismissed for Gemini, reversed after user pushback, now a
    valuable free pre-filter), NVIDIA Parakeet (written off as
    "unnecessary," is free/open-weight and faster on GPU), the bundled
    Arc-Raiders YOLO model (called "not directly reusable," is MIT, ~5MB,
    zero setup), `AutoCutAI` and `vidpipe` (nearly discarded on star count
    and README tone, both real), Camoufox (under-weighted as a directory
    entry, actually 10,674★ and actively maintained),
    `jappeace/cut-the-crap` and `py-feat/resmasknet` (both real, free, and
    treated as footnotes). This is a repeated, documented pattern — see
    `claude_failure_report.md` §12's "Free tools dismissed against a
    stated budget constraint," and the cross-session memory
    `feedback_dont_dismiss_free_resources`.
