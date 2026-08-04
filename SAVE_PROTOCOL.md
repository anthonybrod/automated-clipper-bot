# SAVE EVERYTHING — the protocol

**Trigger:** the user says *"save everything"* (or save / wrap up / hard
save / checkpoint / we're done).

**What it means:** run every step below **in order**, then report. Not a
vibe, not a judgment call — the same sequence every time, so the user can
check whether it actually ran.

**Why it's written down:** before this existed, "save everything" produced
a slightly different sequence each time. That degrades silently. A
protocol is auditable; improvisation isn't.

---

## The steps

### 1. Audit the conversation for unsaved decisions
Re-read what was actually discussed **this session** and confirm each
decision, finding, correction, and design is written down somewhere
durable. **Writing notes as you go does not catch this** — gaps only
become visible reading back.

> Real precedent: the entire `START_HERE.md` design was discussed at
> length, approved, and never written down. It survived only because the
> user said "go back and re-read the convo." That is the failure this step
> exists to prevent. (Rule 21)

Also check `.claude/session-prompts.log` — the `UserPromptSubmit` hook
logs the user's prompts verbatim. If something there isn't reflected in
the notes, it was missed.

### 2. Save anything found in step 1
Verbatim source material → its own file, never blended with analysis
(Rule 16). Decisions → the relevant doc. Rules → `CLAUDE.md`, but **only
if the user explicitly approved them** (Rule 14).

### 3. Update `START_HERE.md`
All five sections, from **real state** — not memory:
- **§1 State now** — what's done, what's in flight, uncommitted work
- **§2 Next action** — the single specific next step, not a menu
- **§3 Blockers & open leads** — what's waiting on the user
- **§4 How we work** — only if the rules changed
- **§5 Where things are** — only if files were added/moved
- **Header** — date, commit hash, tree state

### 4. Regenerate `SESSION_HANDOFF_PROMPT.md` §1
The ready-to-paste block. **Never carry a stale commit hash** — it is the
most load-bearing line in it.

### 5. Run the checks (Rule 21 — before reporting, not after being asked)
```bash
cd "C:\Users\AwBro\Desktop\automated clipper bot"
bash check_links.sh                # every doc link resolves
grep -cE '^[0-9]+\. ' CLAUDE.md    # matches the count in START_HERE §4
git status --short                 # know exactly what's about to commit
```
Cross-check that `START_HERE.md` and `PROJECT.md` don't contradict each
other, and that no pointer describes stale contents.

### 6. Commit
Real message: what changed, **why**, and what was verified. Never
`git add -A` without reading `git status` first — confirm no `.jsonl`, no
`.claude/`, nothing unintended.

### 7. Push and verify — do not skip
```bash
git push origin master
git log --oneline -1     # confirm the commit landed
git status --short       # must be empty
git status -sb | head -1 # must show no divergence from origin
```
**A push is not done until it's verified.** Assuming it worked is the same
class of error as claiming verification that never ran.

### 8. Back up transcripts if the session was substantial
```bash
cp -n "/c/Users/AwBro/.claude/projects/C--Users-AwBro-Desktop-youtube-auto-videos"/*.jsonl \
      "/c/Users/AwBro/Desktop/AI/claude_transcripts_backup_<TODAY>/"
```
These are the raw record and the fallback when a curated note is missing
or disputed. They live in local app data and are **not** guaranteed to
survive app updates or cache clearing.

### 9. Report — honestly
- The commit hash, and that the tree is clean and synced
- **What is still pending, blocked, or awaiting approval** — never let a
  list of completed items imply more than was done
- **Remind the user to pull Drive** — Claude cannot do this:
  ```python
  !git -C "/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt" pull
  ```
  (a fresh Colab runtime needs `drive.mount()` first, or the path won't exist)

---

## Rules that bind during a save

- **Rule 10** — nothing is written as complete unless the user said so
  in-session. If they did, stamp it `✅ COMPLETE — authorized by user
  YYYY-MM-DD`. Otherwise the honest statuses are *in progress*, *awaiting
  user approval*, *blocked*.
- **Rule 15** — preserve source material and agent reports word-for-word.
  Never condense.
- **Rule 16** — raw record and evaluation live in separate files.
- **Rule 21** — every check runs *before* reporting, not after being asked.
- **Never `git add -A` blind.** Read `git status` first.

## What Claude cannot do

- **Push to Google Drive.** No Desktop app, no API, browser sign-in walls.
  The user pulls in Colab. Always say so rather than implying both landed.
- **Guarantee the notes captured everything.** Step 1 plus the verbatim
  prompt log are mitigations, not proof. The transcripts are the fallback.
