#!/usr/bin/env bash
# SessionStart: stdout is injected as context. Keep it SHORT - this cost is
# paid on every session. Points at START_HERE.md rather than inlining it.
REPO="/c/Users/AwBro/Desktop/automated clipper bot"
[ -d "$REPO/.git" ] || exit 0
HEAD=$(cd "$REPO" && git log --oneline -1 2>/dev/null)
DIRTY=$(cd "$REPO" && git status --porcelain 2>/dev/null | wc -l)
cat << MSG
[automated clipper bot — auto-injected at session start]
If this session touches the Twitch clipping bot, read this FIRST:
  C:\Users\AwBro\Desktop\automated clipper bot\START_HERE.md
Then that repo's CLAUDE.md (rules) and PROJECT.md. Do not reconstruct the
plan from memory or chat history — read the files.
Repo HEAD: $HEAD
Uncommitted files: $DIRTY $([ "$DIRTY" -gt 0 ] && echo "(work awaiting approval — do NOT commit without asking)")
Non-negotiables: user has final say on 'complete'; ask before launching
agents and confirm usage headroom; nothing is factual unless confirmed
this session or user-OK'd.
MSG

# --- load the live session state written by the UserPromptSubmit directive ---
# Ported from Sonovore/claude-code-handoff, whose SessionStart hook loads the
# previous session-state.md. Without this the state file is write-only and the
# continuous save never reaches the next session. Tail-limited so a long file
# cannot blow up the startup cost.
STATE="$REPO/.claude/session-state.md"
if [ -s "$STATE" ]; then
  echo ""
  echo "=== Live session state (last 40 lines of .claude/session-state.md) ==="
  tail -40 "$STATE"
  echo "=== end session state ==="
fi
exit 0
