# SAVE EVERYTHING — the protocol

**Trigger:** the user says *"save everything"* (or save / wrap up / hard
save / checkpoint / we're done).

**The user's own definition (2026-08-03), which governs:**

> *"SAVE EVERYTHING = that prompt format we saved + anything else u need to
> will save our work and update for future you to pick up with all info
> needed and exactly where we left off."*

Restated by the user the same session, and this is the whole test:

> *"save everything means what u need to pick up where we left off."*

**The bar is not "did I write files." It is: could a fresh session with
zero memory resume from this alone?** If a future session would have to
ask "what were we doing?" or "why did we decide that?" — the save was
incomplete, regardless of how many commits landed.

**The deliverable is a regenerated, ready-to-paste handoff prompt** —
`SESSION_HANDOFF_PROMPT.md` §1, current and correct, that the user copies
into the next session. It must contain, at minimum:
- a **progress report** — what actually got built last session
- an **open checklist** — every unfinished item as a `[ ]`, including
  things blocked on the user
- **new ideas, tools, and findings** from the session, not yet acted on
- the **context that never survives a reset** — budget, mechanisms,
  environment facts, the honest headline

Everything else in this protocol exists to make that prompt *true*: the
repo saved, `START_HERE.md` accurate, nothing discussed-but-unwritten, no
stale hash.

**End every save by showing the user that block**, not just a commit hash.

**What it means operationally:** run every step below **in order**, then
report. Not a vibe, not a judgment call — the same sequence every time, so
the user can check whether it actually ran.

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

### 9. Report — honestly, and hand over the prompt
- **Show the regenerated handoff block from step 4**, in a copyable code
  fence. This is the deliverable the user asked for; a commit hash alone
  does not satisfy "save everything."
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

---

## The `START_HERE.md` format — exactly what to write in each section

Step 3 says "update `START_HERE.md`." This is *what that means*, so the
format survives even when the session that wrote it is gone. **Written at
the user's instruction (2026-08-03): "you need to save the format so you
know what to add."**

`START_HERE.md` is **overwritten each session, not appended.** History
lives in git. It is a **router, not a duplicate** — point at the real file,
don't restate its contents, or the two drift apart.

### Header
```
Last updated: **YYYY-MM-DD** · Written at commit `<short hash>` (this file's
own commit lands *after*, so HEAD will read one ahead — see §0) · Working
tree <clean|dirty>, local = GitHub. **Drive pull pending** (user runs it).
```
The hash is `git rev-parse --short HEAD` **at the moment of writing**. It
will be one behind after committing — that is correct and §0 explains it.

### What this project is
Only changes if the project's scope or goal changes. Must always answer, in
this order: what it is → why it exists (the payout model) → why budget is a
constraint → the 6-stage pipeline table → the single most important
technique → campaign rules. A cold session that skips this cannot judge
whether any decision was right.

### §0 Validate this file
Static. Only touch it if a new staleness check is added.

### §1 State right now
- **The honest headline first** — currently "zero pipeline code exists."
  Never let a list of finished infrastructure imply progress that didn't
  happen.
- **Done and durable** — what actually survives, not what was discussed.
- **`✅ COMPLETE — authorized by user YYYY-MM-DD`** for each item the user
  approved *this session*. Rule 10: never self-stamp.
- **`⏳ BLOCKED — pending a yes/no`** for anything waiting on the user.
- **Uncommitted work**, if any, and what it is.
- **The workstream progress table** — real counts (`1 of 6`), not vibes.

### §2 Next action
**One specific action, not a menu.** A cold session must be able to start
without deciding anything first. If the next action is a question for the
user, say that explicitly and give the exact wording to ask.

### §3 Blockers and open leads
Everything waiting on someone else, with enough context to act the moment
it unblocks. Include the cost/time estimates and the agent-or-solo call.

### §3b Questions only the user can answer
Numbered, standing, and **kept even after answering** — record the answer
inline. This is where a fresh session finds out what it cannot derive from
the repo. Rule: search the repo before adding a question here.

### §4 How we work
Only edit if `CLAUDE.md` changed. Must state the current rule count — §0
greps `CLAUDE.md` and compares against this number, so a wrong count here
fires a false alarm every session.

### §5 Where things are
Only edit if files were added, moved, or renamed. Every link must resolve —
`check_links.sh` proves it.

### Before saving, verify
```bash
bash check_links.sh                                    # links resolve
grep -cE '^[0-9]+\. ' CLAUDE.md                        # matches §4's count
grep -o 'Written at commit .[a-f0-9]*.' START_HERE.md  # matches HEAD
grep -o '[a-f0-9]\{7\}' SESSION_HANDOFF_PROMPT.md      # NO stale hash
```
> **Real precedent (2026-08-03):** a final cold-start test caught
> `SESSION_HANDOFF_PROMPT.md` still carrying commit `efcadda` while HEAD
> was `c6f569a`, and `README.md` still claiming 11 operating rules when
> there were 20. Both are exactly what this checklist now catches. The
> stale hash is the worst kind of error here — it sends the next session to
> a commit that predates the work it's supposed to resume from.

### ⚠️ Never use `git checkout <file>` to undo an edit
It reverts the **whole file**, not one line — including uncommitted work
written minutes earlier. This destroyed real content on 2026-08-03. Remove
a test line with `sed`, or commit good work before experimenting.
