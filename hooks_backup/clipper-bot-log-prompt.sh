#!/usr/bin/env bash
# UserPromptSubmit hook. Two jobs:
#   1. Append the user's prompt verbatim to a local log (decisions that live
#      only in conversation get lost when notes miss them).
#   2. Print a LIVE-HANDOFF directive. stdout from this hook is injected into
#      Claude's context on EVERY message.
#
# WHY THE DIRECTIVE (added 2026-08-06): this project spent three days on an
# end-of-session save that kept failing - steps silently skipped, START_HERE
# stale four times, PROJECT.md stale three times. The user had pointed at a
# shipped implementation (Sonovore/claude-code-handoff) whose actual mechanism
# is CONTINUOUS, not end-of-session: "Every time you send a message, Claude
# sees a <live-handoff> directive telling it to check if anything important
# happened and update session-state.md."
#
# That is the fix. A save that happens as work happens has no end-of-session
# step left to skip. Ported rather than re-derived (Rule 1) - the third day of
# debugging a home-grown version was the cost of not doing that first.
#
# Kept deliberately short: it fires on every message, and budget is a live
# constraint for this user.

LOG="/c/Users/AwBro/Desktop/automated clipper bot/.claude/session-prompts.log"
STATE="/c/Users/AwBro/Desktop/automated clipper bot/.claude/session-state.md"
mkdir -p "$(dirname "$LOG")" 2>/dev/null

IN=$(cat 2>/dev/null)
P=$(printf '%s' "$IN" | "/c/Users/AwBro/AppData/Local/Programs/Python/Python312/python.exe" -c \
  "import sys,json
try:
    d=json.load(sys.stdin); print(d.get('prompt') or d.get('user_prompt') or '')
except Exception:
    pass" 2>/dev/null)
[ -z "$P" ] && P="$IN"
[ -n "$P" ] && { printf '\n=== %s ===\n%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$P"; } >> "$LOG" 2>/dev/null

# --- the live-handoff directive (this is what reaches Claude) ---
cat <<'DIRECTIVE'
<live-handoff>
If anything durable happened since the last message — a decision, a
correction, a finding, work completed, something deferred — append it to
.claude/session-state.md NOW, one line, before doing anything else. Do not
wait for "save everything"; that is what kept failing. If nothing durable
happened, ignore this silently and do not mention it.
</live-handoff>
DIRECTIVE
exit 0
