# Save-system attack findings — VERBATIM AGENT REPORT (2026-08-06)

**Provenance.** An adversarial workflow was launched 2026-08-06 with 5 attack
agents plus per-finding skeptics. **14 of 15 agents died on a session limit.**
One survived: the `live-handoff` lens. Its findings are reproduced below
**verbatim and uncondensed** (Rule 15), recovered from the workflow journal
before that temp directory could be lost.

## ⚠️ NONE OF THIS WAS VERIFIED

Every skeptic agent assigned to refute these findings died on the same session
limit. The surviving agent also carried a note that the safety classifier was
unavailable when reviewing its work. **Treat every item as a LEAD requiring
independent verification, not an established fact** (Rule 12).

They are saved because two are marked critical and one concerns a privacy
issue in a DIFFERENT repository. Withholding them would be worse than the
uncertainty. See also PART 11 of `HANDOFF_REPORT_2026-08-06.md`.

---

## 1. [CRITICAL] The live-handoff already stopped tracking — in the very session it was built in. The day's biggest finding never reached session-state.md.

### Evidence (as reported)

```
$ cd "C:/Users/AwBro/Desktop/automated clipper bot" && stat -c '%y  %n' .claude/session-state.md
2026-08-06 13:42:12.993526900 -0700  .claude/session-state.md

$ git log --format='%h %ad %s' --date=format:'%Y-%m-%d %H:%M:%S' --since='2026-08-06 13:42:12'
3de7f4b 2026-08-06 13:46:22 Rule 22: header last
859a139 2026-08-06 13:46:20 INDEX: add the H1 report row
71ef7db 2026-08-06 13:45:38 Rule 22: header and handoff hash refreshed last
638c8b3 2026-08-06 13:45:36 Save everything 2026-08-06: regenerate handoff in full detail, record H1
101cdd7 2026-08-06 13:44:29 H1 landed: real repost data from X, and it contradicts the architecture

$ grep -n -i 'H1' .claude/session-state.md | tail -5
129:- H1 RE-RUN LAUNCHED 2026-08-06 (user: "this is next", headroom 26%
149:  again. H1 (CORE clippers on X) also still running.

$ bash "C:/Users/AwBro/.claude/hooks/clipper-bot-session-start.sh" | grep -ci 'repost data\|contradicts the architecture'
0
```

### Why it matters (as reported)

A commit whose own subject says it "contradicts the architecture" landed 2 minutes after the last append and never made it into the live buffer. session-state.md still claims H1 is "still running." A cold session reading the SessionStart injection would resume believing an agent is in flight and the architecture is intact — both false. This is precisely the failure the mechanism was ported to prevent, reproducing inside its own build session. The directive fires on every message but nothing verifies it was obeyed, so silent skipping is the default failure mode, same as the old end-of-session save.

### Suggested fix (as reported, NOT applied)

Make obedience checkable rather than trusted. Add a save_check.sh check: if `git log --since=<mtime of session-state.md>` returns any commits, FAIL — durable work landed after the last live append. Also have the UserPromptSubmit hook include the file's current mtime and the count of commits newer than it in the directive text, so the drift is visible in-context on every message instead of only at save time.

---

## 2. [CRITICAL] CRITICAL PRIVACY: the directive's relative path plus a globally-scoped hook writes raw session content into the sibling repo, where .claude/ is NOT gitignored

### Evidence (as reported)

```
The hook is registered at USER level (C:/Users/AwBro/.claude/settings.json), so it fires in every project, and the directive names a bare relative path:
  "append it to .claude/session-state.md NOW"
The hook itself has no cwd/project gate — I fed it a foreign cwd and it still ran:
$ echo '{"cwd":"C:/tmp","prompt":"TEST PROBE 1 harmless"}' | bash "C:/Users/AwBro/.claude/hooks/clipper-bot-log-prompt.sh"
<live-handoff> ... </live-handoff>   (EXIT=0)
$ tail -3 "C:/Users/AwBro/Desktop/automated clipper bot/.claude/session-prompts.log"
=== 2026-08-06 13:42:11 ===
TEST PROBE 1 harmless

The sibling repo does NOT ignore .claude/:
$ cd "C:/Users/AwBro/Desktop/youtube auto videos" && git check-ignore -v .claude/session-state.md; echo "exit=$?"
exit=1                     <-- 1 = NOT IGNORED
$ git remote -v
origin	https://github.com/anthonybrod/youtube-auto-videos.git (fetch/push)

Sandbox proof using that repo's exact .gitignore (no repo files touched):
$ cp "C:/Users/AwBro/Desktop/youtube auto videos/.gitignore" $SB/yt/ && echo "- DECISION: ..." > $SB/yt/.claude/session-state.md
$ cd $SB/yt && git add -A --dry-run
add '.claude/session-state.md'
add '.gitignore'

This is a live near-miss, not hypothetical: the session that spawned me is rooted in "youtube auto videos", and its prompts are already landing in the clipper repo's log (13:38:50 "i bet the save everything still doesnt work...", 13:42:58, 13:45:25).
```

### Why it matters (as reported)

Two leaks in one. (a) Any session rooted outside the clipper repo that obeys the directive literally creates `<that repo>/.claude/session-state.md`. In youtube-auto-videos that file is untracked-but-not-ignored, so `git add -A` or `git add .` stages it and the next push puts durable conversation content on a GitHub remote. The clipper repo's own .gitignore protects nothing here — the write lands somewhere else. (b) In the other direction, prompts from every unrelated project are being appended verbatim into the clipper repo's .claude/session-prompts.log (708 lines, 41 KB, no rotation), concentrating cross-project raw conversation in one folder.

### Suggested fix (as reported, NOT applied)

Two changes. In clipper-bot-log-prompt.sh, gate on cwd: parse `.cwd` from the hook JSON (it is already in the payload and currently discarded) and exit 0 silently unless it is under the clipper bot repo. Then make the directive name the absolute path — `C:\Users\AwBro\Desktop\automated clipper bot\.claude\session-state.md` — so it cannot resolve into a foreign repo. Independently, add a bare `.claude/` line to `C:\Users\AwBro\Desktop\youtube auto videos\.gitignore` (it currently ignores only `.claude/settings.local.json`) so the failure is contained even if the hook is wrong.

---

## 3. [HIGH] SessionStart's `tail -40` silently drops 74% of session-state.md and cuts mid-entry

### Evidence (as reported)

```
$ cd "C:/Users/AwBro/Desktop/automated clipper bot"
$ TOT=$(wc -l < .claude/session-state.md); echo "total lines: $TOT ; loaded by tail -40: 40 ; DROPPED: $((TOT-40))"
total lines: 152 ; loaded by tail -40: 40 ; DROPPED: 112
$ echo "bytes total: $(wc -c < .claude/session-state.md) ; bytes loaded: $(tail -40 .claude/session-state.md | wc -c)"
bytes total: 9744 ; bytes loaded: 2694

The directive says "one line" per fact; the file is not written that way:
$ awk 'NR>20' .claude/session-state.md | grep -c '^- '   ->  20   (top-level bullets)
$ awk 'NR>20' .claude/session-state.md | grep -c '^  '   -> 107   (continuation lines)

So the 40-line window covers ~6 of 20 entries and lands mid-thought. Actual SessionStart run, first line of the injected state block:
=== Live session state (last 40 lines of .claude/session-state.md) ===
  30/59/29s = Twitch's clip-tool UI presets. Twitch durations measure THE
  TOOL, not the moment. G2's 20-70s acceptance band holds at 89% ...
```

### Why it matters (as reported)

The file is append-only and unbounded; the reader is a fixed 40-line window. The better the mechanism works — the more durable facts get appended — the more of the earlier record falls out of the handoff, with no warning anywhere. Everything before line 41 is already invisible today, including the file's own header explaining what it is and why it exists. And because entries average ~6 lines rather than the "one line" the directive asks for, the window opens mid-sentence, so the next session's first impression of project state is a sentence fragment.

### Suggested fix (as reported, NOT applied)

Bound by entries, not lines: split on `^- ` and emit the last N complete entries (`awk 'BEGIN{RS="\n- "}' ...` or `tac | awk` until N bullets seen), so the window never opens mid-item. Separately, cap the file: at save time, fold everything above the last N entries into START_HERE.md/PROJECT.md and truncate the buffer, so "dropped by tail" and "already durable" mean the same thing.

---

## 4. [HIGH] `tail -40` is not a byte bound — the hook's own comment claiming it prevents context blowup is false

### Evidence (as reported)

```
The hook comment claims: "Tail-limited so a long file cannot blow up the startup cost."
Sandbox test (copy of the hook repointed at a temp repo; no real files touched). 40 lines, 20 KB each — exactly the shape the "append one line" directive encourages:
$ python.exe -c "open(r'$SB/repo/.claude/session-state.md','w').write(('- FACT '+'x'*20000+'\n')*40)"
$ wc -c $SB/repo/.claude/session-state.md
800360
$ OUT=$(bash $SB/ss.sh); echo "SessionStart stdout bytes injected: $(printf '%s' "$OUT" | wc -c)"
SessionStart stdout bytes injected: 801031
```

### Why it matters (as reported)

SessionStart stdout is injected into context verbatim. A 40-line file produced 801 KB of injection — roughly 200K tokens, enough to consume or exceed the context window before the session starts, on a machine where the user hits metered limits weekly and has already lost sessions to them. The line count is capped; nothing caps the bytes. The directive telling Claude to write "one line" per fact actively pushes toward long lines, so this is the encouraged shape, not a pathological one.

### Suggested fix (as reported, NOT applied)

Add a hard byte cap after the line cap: `tail -40 "$STATE" | head -c 8000` and print a truncation marker when the cut fires, so the next session knows the window was clipped rather than silently reading a partial record.

---

## 5. [HIGH] Nothing on the save path ever reads session-state.md — the live buffer is write-only and orphaned

### Evidence (as reported)

```
$ cd "C:/Users/AwBro/Desktop/automated clipper bot"
$ for f in save_check.sh START_HERE.md PROJECT.md CLAUDE.md SESSION_HANDOFF_PROMPT.md; do printf '%-28s ' "$f"; grep -c -i 'session-state\|live-handoff' $f; done
save_check.sh                0
START_HERE.md                0
PROJECT.md                   0
CLAUDE.md                    0
SESSION_HANDOFF_PROMPT.md    0

Only two references exist in the whole repo — SAVE_PROTOCOL.md's preamble (lines 6-8) and one INDEX.md row (line 146). Neither is a step.
$ grep -nE '^#+ *(Step|[0-9])' SAVE_PROTOCOL.md    # the 9 steps
68:### 1. Audit the conversation for unsaved decisions   <- names .claude/session-prompts.log, NOT session-state.md
83:### 2. Save anything found in step 1
88:### 3. Update `START_HERE.md`
... (steps 4-9: no mention)
```

### Why it matters (as reported)

START_HERE.md is the documented session entry point and it never mentions the mechanism at all — a cold session learns about live-handoff only from hook stdout, so if the hooks are ever unregistered the mechanism becomes completely invisible with no error. Worse, save_check.sh is the gate that decides whether a save may be reported done, and it has zero checks on session-state.md. A "save everything" can pass all 12 checks while the entire live buffer — the thing built specifically to stop facts being lost — is never folded into any durable doc. Step 1 tells you to audit session-prompts.log and skips the state file entirely.

### Suggested fix (as reported, NOT applied)

Add session-state.md to SAVE_PROTOCOL step 1 alongside session-prompts.log ("every entry must be reflected in a durable doc or explicitly dropped"), add a save_check.sh check that fails when session-state.md is newer than START_HERE.md, and add a §5 row in START_HERE.md naming the file with its absolute path so a hookless cold read still finds it.

---

## 6. [MEDIUM] The mechanism is unrecoverable if ~/.claude is lost: settings.json (the hook registration) is in no backup, and neither is session-state.md

### Evidence (as reported)

```
INDEX.md line 146 claims hooks_backup/ is the protection: "Copies of the 4 lifecycle hooks + the user-level CLAUDE.md, which live in ~/.claude/ and are therefore OUTSIDE version control. If that folder is lost the whole resume system goes with it."

$ cd "C:/Users/AwBro/Desktop/automated clipper bot" && find . -name 'settings*.json' -not -path './.git/*'
(no output — settings.json is nowhere in the repo)
$ ls hooks_backup/
clipper-bot-log-prompt.sh  clipper-bot-precompact.sh  clipper-bot-session-close.sh  clipper-bot-session-start.sh  user-level-CLAUDE.md

session-state.md exists in exactly one place on disk:
$ find "C:/Users/AwBro/Desktop/AI" "C:/Users/AwBro/Desktop/automated clipper bot" -name 'session-state*'
C:/Users/AwBro/Desktop/automated clipper bot/.claude/session-state.md
$ ls "C:/Users/AwBro/Desktop/AI/claude_transcripts_backup_2026-08-06"
01963dc5-....jsonl  143a3b23-....jsonl  31cd27c6-....jsonl  82fe0786-....jsonl   (transcripts only)
```

### Why it matters (as reported)

Restoring hooks_backup/ after a ~/.claude loss gives you four inert shell scripts. settings.json is the only thing that registers them, so the hooks would sit on disk and never fire — and they would fail silently, which is the worst shape: the user believes the resume system is restored while every message goes unlogged and every session starts with no state injection. Separately, session-state.md is gitignored and copied nowhere, so losing .claude/ loses the entire live buffer; the .jsonl transcripts hold the raw conversation but not the curated durable facts.

### Suggested fix (as reported, NOT applied)

Copy settings.json into hooks_backup/ as `user-level-settings.json` and add a save_check.sh check that diffs it against the live ~/.claude/settings.json (the same drift check that already proves the 4 hook scripts are byte-identical). For the buffer itself, have SAVE_PROTOCOL step 8 copy session-state.md into the dated transcript backup dir alongside the .jsonl files.

---

## 7. [MEDIUM] save_check.sh check 7 passes when a doc is entirely missing, because check_links.sh reports that as "MISSING DOC:" not "BROKEN:"

### Evidence (as reported)

```
save_check.sh check 7 greps only for BROKEN:
  LINKOUT=$(bash check_links.sh 2>&1)
  if echo "$LINKOUT" | grep -q BROKEN; then fail ... else pass ...
check_links.sh uses a different prefix for a missing doc:
  [ -f "$doc" ] || { echo "MISSING DOC: $doc"; ... }

Sandbox proof — deleted the PENDING resume file from a throwaway copy:
$ cd $SB/links && rm -f reference/PENDING_agent_prompts_resume_2026-08-01.md
$ OUT=$(bash check_links.sh 2>&1); echo "$OUT"
MISSING DOC: reference/PENDING_agent_prompts_resume_2026-08-01.md
--- checked 0 relative links across 5 docs ---
$ if echo "$OUT" | grep -q BROKEN; then echo "check 7 -> FAIL"; else echo "check 7 -> PASS"; fi
check 7 -> PASS   <-- doc is GONE and check 7 still passes

Related, same file: check_links.sh's own header says "(exit 1 if any link is broken)" but it always exits 0 —
$ bash check_links.sh   # with 2 known-broken links
BROKEN: START_HERE.md -> DOES_NOT_EXIST.md
BROKEN: START_HERE.md -> also/missing.md
--- checked 2 relative links across 5 docs ---
EXIT CODE = 0
(cause: BROKEN is incremented inside a `| while read` subshell and there is no `exit $BROKEN` at all)
```

### Why it matters (as reported)

reference/PENDING_agent_prompts_resume_2026-08-01.md is described in the user's own memory index as the cold-read pick-up point. If it is renamed or deleted, the gate that exists to catch exactly this reports PASS. The header-doc count is also wrong ("across 5 docs" while the loop iterates 6), so the output actively understates coverage. The always-zero exit is latent today because save_check.sh greps stdout instead of trusting $?, but the script's documented contract says otherwise, so the next caller that does the obvious thing gets a silent always-pass.

### Suggested fix (as reported, NOT applied)

In save_check.sh check 7, grep for `-qE 'BROKEN|MISSING DOC'`. In check_links.sh, collect results without a subshell (`while read ... done < <(...)`) and end with `exit $((BROKEN>0))`, and fix the hardcoded "5 docs" to the real loop count.

---

## 8. [MEDIUM] Both context-injecting hooks are unscoped: every project on this machine pays 379 bytes per message and 3,388 bytes per session start for clipper-bot content, mislabeled as its own

### Evidence (as reported)

```
$ cat C:/Users/AwBro/.claude/settings.json     # user-level: no matcher, no project scope on any of the 4 hooks
$ echo '{"prompt":"x"}' | bash "C:/Users/AwBro/.claude/hooks/clipper-bot-log-prompt.sh" | wc -c
379
$ bash "C:/Users/AwBro/.claude/hooks/clipper-bot-session-start.sh" | wc -c
3388

Neither script contains any cwd or project check (grep for cwd in both: no matches). The SessionStart block is also mislabeled outside the repo:
=== Live session state (last 40 lines of .claude/session-state.md) ===
$ cd "C:/Users/AwBro/Desktop/youtube auto videos" && ls .claude/session-state.md
ls: cannot access '.claude/session-state.md': No such file or directory
```

### Why it matters (as reported)

379 bytes on every single message across every project is a standing tax on a user whose stated hard constraint is metered weekly usage they have hit repeatedly. The correctness cost is worse than the token cost: a session in youtube-auto-videos is handed 40 lines of Twitch-clipping findings under a header naming a relative path that, in that working directory, points at a file which does not exist. That is an invitation to write project state into the wrong repo — the exact mechanism of the privacy finding above.

### Suggested fix (as reported, NOT applied)

Scope both hooks on the `cwd` field already present in the hook JSON: exit 0 with no stdout unless cwd is under the clipper bot repo. Where the state block is printed, label it with the absolute path ("last 40 entries of C:\Users\AwBro\Desktop\automated clipper bot\.claude\session-state.md") so it can never be mistaken for the current project's file.

---

## 9. [LOW] Ported-but-unfinished residue in the hooks: a dead STATE variable, an unrotated raw-prompt log, and a stale .bak in the hooks directory

### Evidence (as reported)

```
$ grep -n 'STATE' "C:/Users/AwBro/.claude/hooks/clipper-bot-log-prompt.sh"
24:STATE="/c/Users/AwBro/Desktop/automated clipper bot/.claude/session-state.md"
(assigned once, referenced nowhere else in the file — the hook never touches the state file it names)

$ wc -c -l "C:/Users/AwBro/Desktop/automated clipper bot/.claude/session-prompts.log"
  708 41576
$ grep -rn 'session-prompts' "C:/Users/AwBro/.claude/hooks/"
clipper-bot-log-prompt.sh:23:LOG="...session-prompts.log"     (append only — no rotation, no cap, anywhere)

$ ls "C:/Users/AwBro/.claude/hooks/"
clipper-bot-log-prompt.sh  clipper-bot-precompact.sh  clipper-bot-session-close.sh  clipper-bot-session-close.sh.bak  clipper-bot-session-start.sh
(.bak is unregistered in settings.json and is not mirrored in hooks_backup/)

Also: on unparseable stdin the hook falls back to logging the raw payload verbatim —
$ echo 'not json at all {{{' | bash .../clipper-bot-log-prompt.sh >/dev/null; tail -2 .../session-prompts.log
=== 2026-08-06 13:43:19 ===
not json at all {{{
```

### Why it matters (as reported)

The dead STATE variable is a tell that the port was left half-finished — it reads as if the hook maintains the state file when it only prints a directive asking Claude to, which is exactly the gap that let the top finding happen. The prompt log grows without bound in a folder holding raw conversation, so the privacy blast radius increases forever. And `[ -z "$P" ] && P="$IN"` means any future hook-payload schema change silently starts logging the entire JSON envelope (transcript paths, session ids) instead of the prompt, with no error.

### Suggested fix (as reported, NOT applied)

Delete the unused STATE assignment or make it load-bearing. Rotate the log (`tail -c 2000000` into place when it exceeds ~2 MB). Move clipper-bot-session-close.sh.bak out of the hooks directory into hooks_backup/ so the live hooks dir contains only registered scripts. Make the JSON-parse fallback log a fixed `[unparseable hook payload]` marker rather than the raw envelope.

---

## Attacks tried that found nothing (as reported)

Things I attacked that genuinely held up — reporting these so the real findings aren't diluted.

HOOK REGISTRATION AND EXECUTION (all clean). All 4 hooks in settings.json point at files that exist, and all 4 execute and exit 0. `bash clipper-bot-session-start.sh` -> EXIT=0 with correct HEAD/dirty count. `bash clipper-bot-precompact.sh` -> EXIT=0 and verifiably appended a real snapshot to .claude/precompact-snapshots.log ("=== PRE-COMPACT SNAPSHOT 2026-08-06 13:45:24 === / HEAD: 101cdd7 ..."). `bash clipper-bot-session-close.sh` on a clean tree -> EXIT=0, silent (correct: it must not spend stdout when there is nothing to say). UserPromptSubmit emits exactly the directive and nothing else.

PRIVACY *INSIDE THE CLIPPER REPO* (clean — the leak is entirely in the sibling repo). `git ls-files .claude/` -> empty. `git log --all --oneline -- .claude` -> empty, so it has never been committed even historically. `git check-ignore -v .claude/session-state.md` -> `.gitignore:18:.claude/`, exit 0. That repo's protection is correct; my finding is that the write can land somewhere else.

MALFORMED / HOSTILE HOOK INPUT (clean). Empty stdin -> EXIT=0, directive still printed, nothing garbage logged. Malformed JSON `not json at all {{{` -> EXIT=0, no Python traceback on stdout or stderr. No format-string injection: the payload goes through `printf '%s'` as an argument, and the directive heredoc is quoted (`<<'DIRECTIVE'`) so prompt content cannot expand into it.

MISSING-FILE FAILURE MODES (clean). Sandbox copy of SessionStart repointed at a temp repo: session-state.md absent -> block cleanly omitted, EXIT=0, no stderr. session-state.md present but 0 bytes -> `[ -s ]` correctly suppresses it, EXIT=0. Missing .claude directory -> log hook's `mkdir -p` recreates it. Missing .git -> both repo hooks exit 0 early.

BACKUP FIDELITY OF THE HOOK SCRIPTS THEMSELVES (clean). diff'd all 4 hooks_backup/ scripts against the live ~/.claude/hooks/ copies: IDENTICAL. hooks_backup/user-level-CLAUDE.md vs the live C:/Users/AwBro/.claude/CLAUDE.md: IDENTICAL. No drift. (The gap is settings.json, which is reported as a finding — the scripts are fine.)

SETTINGS OVERRIDE (clean). No project-level settings.json in the clipper repo's .claude/ that could shadow the user-level hooks, and `grep -i hook` in youtube-auto-videos/.claude/settings.local.json -> no matches. Nothing competes with the registration.

THE STATE FILE IS GENUINELY BEING MAINTAINED — this part works. It is not write-once-and-abandoned: it grew from 9,088 bytes to 9,744 bytes during my run, and its content maps onto today's real work (the 964-clip dataset, the Twitch-duration correction, the power-law view finding, the Kick secondary source). The defect is that it stopped at 13:42 and missed the last five commits, not that it was never used.

save_check.sh IS A REAL GATE, NOT THEATRE. Ran it live: it FAILED with exit 1 on a genuine defect nobody had spotted — `invisible: reference/research_2026-08-06_core_clippers_named_VERBATIM.md` (a source doc reachable from no document a cold session reads). It was then fixed in commit 859a139 "INDEX: add the H1 report row". Checks 1-8 and 10-11 all passed against real state, and the 2026-08-06 SAVEDATE fix (validating the last save's date rather than today's) is working — no false alarms this run.

WINDOWS/MSYS QUOTING (clean). Suspected `wc -l` leading-whitespace would break `[ "$DIRTY" -gt 0 ]` under Git Bash; it does not — bash arithmetic comparison strips it, and the live output ("Uncommitted files: 0") is correct. Paths with spaces ("automated clipper bot") are quoted correctly in all four scripts.

NOT PURSUED, and why: concurrent-session write collisions on session-state.md (two sessions doing read-modify-write) are a plausible design risk, but I could not produce evidence of an actual lost append, so I left it out rather than pad the count. Same for save_check.sh check 11 giving a false "synced with origin" when `git fetch -q origin` fails offline — real in principle, but I could not trigger it without cutting the network.
