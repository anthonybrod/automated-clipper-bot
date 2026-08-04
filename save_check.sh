#!/usr/bin/env bash
# save_check.sh — mechanically verify that "save everything" actually happened.
#
# WHY THIS EXISTS (2026-08-04): SAVE_PROTOCOL.md defined 9 steps, and on
# 2026-08-04 three of them were silently skipped anyway — step 1 (audit the
# conversation), step 5 (cross-file consistency), step 8 (transcript backup).
# The user found them by asking twice, which is exactly what the protocol was
# supposed to make unnecessary. Their words: "i was supposed to just say
# 'save everything' and u would reference the save protocol and complete it."
#
# A protocol that depends on remembering is the same failure class as a file
# nothing points at. This script checks OUTCOMES, not intentions. Run it as
# step 5 of SAVE_PROTOCOL, BEFORE committing and BEFORE reporting anything.
#
# Exit 0 = every check passed. Exit 1 = at least one FAIL; do not report done.

cd "$(dirname "$0")" || exit 1
TODAY=$(date +%Y-%m-%d)
FAIL=0
pass() { printf "  PASS  %s\n" "$1"; }
fail() { printf "  FAIL  %s\n" "$1"; FAIL=$((FAIL+1)); }
warn() { printf "  WARN  %s\n" "$1"; }

echo "=== SAVE CHECK — $TODAY ==="

# --- 1. START_HERE.md actually updated this session ---------------------
if grep -q "Last updated: \*\*$TODAY\*\*" START_HERE.md; then
  pass "START_HERE.md dated today (Rule 22)"
else
  fail "START_HERE.md NOT dated today — Rule 22 says it is the last action of every session"
fi

# --- 2. header hash within 1 commit of HEAD -----------------------------
HDR=$(grep -oE 'Written at commit `[a-f0-9]+`' START_HERE.md | grep -oE '[a-f0-9]{7,}' | head -1)
if [ -n "$HDR" ] && git cat-file -e "$HDR" 2>/dev/null; then
  AHEAD=$(git rev-list --count "${HDR}..HEAD" 2>/dev/null)
  if [ "${AHEAD:-99}" -le 1 ]; then
    pass "header hash $HDR is HEAD-$AHEAD (0 or 1 is correct)"
  else
    fail "header hash $HDR is $AHEAD commits behind HEAD — work landed after START_HERE was written"
  fi
else
  fail "header hash missing or not a real commit: '$HDR'"
fi

# --- 3. PROJECT.md not stale (it has gone stale 3x in 3 days) -----------
if grep -q "$TODAY" PROJECT.md; then
  pass "PROJECT.md mentions today"
else
  fail "PROJECT.md has no mention of $TODAY — it is the stated single source of truth and it is stale"
fi

# --- 4. handoff prompt regenerated, no stale hash -----------------------
H_HASH=$(grep -oE 'Last known good is [a-f0-9]{7,}' SESSION_HANDOFF_PROMPT.md | grep -oE '[a-f0-9]{7,}' | head -1)
if [ -n "$H_HASH" ] && git cat-file -e "$H_HASH" 2>/dev/null; then
  H_AHEAD=$(git rev-list --count "${H_HASH}..HEAD" 2>/dev/null)
  if [ "${H_AHEAD:-99}" -le 3 ]; then
    pass "handoff prompt points at $H_HASH (HEAD-$H_AHEAD)"
  else
    fail "handoff prompt hash $H_HASH is $H_AHEAD behind — it would send the next session to a commit predating the work"
  fi
else
  fail "handoff prompt has no valid commit hash"
fi

# --- 5. handoff keeps the proven format ---------------------------------
MISSING=""
for s in "just to catch you up" "TASK #1" "OPEN CHECKLIST" "LAST SESSION" \
         "NEW THIS SESSION" "ALSO READ" "BEFORE STARTING" "CONTEXT I'll forget"; do
  grep -qF "$s" SESSION_HANDOFF_PROMPT.md || MISSING="$MISSING '$s'"
done
[ -z "$MISSING" ] && pass "handoff keeps the proven format (8 sections)" \
                  || fail "handoff missing format sections:$MISSING"

# --- 6. structural integrity of the handoff file ------------------------
SECS=$(grep -c '^## ' SESSION_HANDOFF_PROMPT.md)
MERGED=$(grep -c '^---##' SESSION_HANDOFF_PROMPT.md)
if [ "$SECS" -eq 3 ] && [ "$MERGED" -eq 0 ]; then
  pass "handoff structure intact (3 sections, no merged headings)"
else
  fail "handoff structure broken — $SECS sections (want 3), $MERGED merged heading lines (want 0)"
fi

# --- 7. links resolve ---------------------------------------------------
LINKOUT=$(bash check_links.sh 2>&1)
if echo "$LINKOUT" | grep -q BROKEN; then
  fail "broken links: $(echo "$LINKOUT" | grep BROKEN | tr '\n' ' ')"
else
  pass "$(echo "$LINKOUT" | tr -d '\-' | xargs)"
fi

# --- 8. rule count agrees between CLAUDE.md and START_HERE.md -----------
RC=$(grep -cE '^[0-9]+\. ' CLAUDE.md)
if grep -q "$RC numbered rules" START_HERE.md; then
  pass "rule count agrees ($RC)"
else
  fail "CLAUDE.md has $RC numbered rules; START_HERE.md §4 claims something else"
fi

# --- 9. every source doc is reachable from INDEX/PROJECT/START_HERE -----
INVIS=0
for f in $(git ls-files 'reference/*.md' 'research/*.md' 2>/dev/null); do
  b=$(basename "$f")
  n=$(cat INDEX.md PROJECT.md START_HERE.md 2>/dev/null | grep -cF "$b")
  [ "$n" -eq 0 ] && { echo "        invisible: $f"; INVIS=$((INVIS+1)); }
done
[ "$INVIS" -eq 0 ] && pass "every source document is reachable from a doc a session reads" \
                   || fail "$INVIS document(s) invisible to a cold read — add INDEX.md rows"

# --- 10. transcript backup ran (step 8, skipped on 2026-08-04) ----------
BK="/c/Users/AwBro/Desktop/AI/claude_transcripts_backup_$TODAY"
if [ -d "$BK" ] && [ "$(ls -1 "$BK" 2>/dev/null | wc -l)" -gt 0 ]; then
  pass "transcripts backed up ($(ls -1 "$BK" | wc -l) files)"
else
  fail "no transcript backup for $TODAY — SAVE_PROTOCOL step 8"
fi

# --- 11. nothing uncommitted, nothing unpushed --------------------------
if [ -z "$(git status --porcelain)" ]; then
  pass "working tree clean"
else
  warn "uncommitted changes — expected mid-save, must be empty AFTER the commit:"
  git status --short | sed 's/^/        /'
fi
git fetch -q origin 2>/dev/null
SB=$(git status -sb | head -1)
case "$SB" in
  *ahead*)  fail "commits not pushed: $SB" ;;
  *behind*) fail "local is behind origin: $SB" ;;
  *)        pass "synced with origin" ;;
esac

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "=== SAVE CHECK PASSED — safe to report done ==="
  echo "Remaining manual step: remind the user to pull Drive in Colab."
  exit 0
else
  echo "=== SAVE CHECK FAILED: $FAIL problem(s) — DO NOT report the save as done ==="
  exit 1
fi
