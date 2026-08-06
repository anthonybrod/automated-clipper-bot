#!/usr/bin/env bash
# PreCompact: fires before the transcript is compacted - the sudden-death
# case a Stop-based reminder cannot cover. Snapshots repo state to disk.
REPO="/c/Users/AwBro/Desktop/automated clipper bot"
[ -d "$REPO/.git" ] || exit 0
LOG="$REPO/.claude/precompact-snapshots.log"
mkdir -p "$(dirname "$LOG")" 2>/dev/null
{
  printf '\n=== PRE-COMPACT SNAPSHOT %s ===\n' "$(date '+%Y-%m-%d %H:%M:%S')"
  printf 'HEAD: %s\n' "$(cd "$REPO" && git log --oneline -1 2>/dev/null)"
  printf 'Uncommitted:\n%s\n' "$(cd "$REPO" && git status --short 2>/dev/null)"
  printf 'START_HERE.md last modified: %s\n' "$(stat -c %y "$REPO/START_HERE.md" 2>/dev/null)"
} >> "$LOG" 2>/dev/null
exit 0
