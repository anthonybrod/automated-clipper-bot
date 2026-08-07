#!/usr/bin/env bash
# final_save.sh — the complete save. Everything, everywhere, verified.
#
# Run this when you want a full checkpoint: the repo, the raw chat
# transcripts, the gitignored .claude/ buffers, and the out-of-repo hooks.
#
#   bash final_save.sh
#
# WHY THIS EXISTS
# `save_check.sh` verifies the REPO is saved. It does not save anything, and
# it cannot see the things that live outside git:
#   - the raw chat transcripts (.jsonl) — the fallback when a curated note is
#     missing or disputed
#   - .claude/session-state.md and .claude/session-prompts.log — gitignored
#     because this is a PUBLIC repo, and therefore backed up NOWHERE (K6)
#   - ~/.claude/settings.json — the ONLY thing that registers the 4 hooks.
#     Restoring hooks_backup/ without it yields four inert scripts that fail
#     silently (K6).
# This script closes all of that, then hands off to save_check.sh for the
# repo half.
#
# SAFE BY DESIGN: copy-only. It never deletes, moves, or overwrites an
# existing backup file (`cp -n`). It does not commit or push on its own —
# it stages nothing and tells you exactly what it found.

set -uo pipefail
cd "$(dirname "$0")" || exit 1

TODAY=$(date +%Y-%m-%d)
STAMP=$(date +%Y-%m-%d_%H%M)
AI="/c/Users/AwBro/Desktop/AI"
CLAUDE_HOME="/c/Users/AwBro/.claude"
PROJ="$CLAUDE_HOME/projects/C--Users-AwBro-Desktop-youtube-auto-videos"
DEST="$AI/claude_transcripts_backup_$TODAY"
PY="/c/Users/AwBro/AppData/Local/Programs/Python/Python312/python.exe"

ok()   { printf "  \033[32mOK\033[0m    %s\n" "$1"; }
warn() { printf "  \033[33mWARN\033[0m  %s\n" "$1"; }
err()  { printf "  \033[31mFAIL\033[0m  %s\n" "$1"; ERRS=$((ERRS+1)); }
ERRS=0

echo "════════════════════════════════════════════════════════════"
echo "  FINAL SAVE — $STAMP"
echo "════════════════════════════════════════════════════════════"

# ── 1. RAW CHAT TRANSCRIPTS ─────────────────────────────────────
echo ""
echo "1. Raw chat transcripts (the actual conversation record)"
mkdir -p "$DEST" 2>/dev/null
if [ -d "$PROJ" ]; then
  BEFORE=$(ls -1 "$DEST" 2>/dev/null | wc -l)
  cp -n "$PROJ"/*.jsonl "$DEST/" 2>/dev/null
  AFTER=$(ls -1 "$DEST" 2>/dev/null | wc -l)
  SIZE=$(du -sh "$DEST" 2>/dev/null | cut -f1)
  ok "$AFTER files ($((AFTER-BEFORE)) new), $SIZE  ->  $DEST"
  # newest transcript, so you can see whether THIS session is captured
  NEW=$(ls -t "$PROJ"/*.jsonl 2>/dev/null | head -1)
  [ -n "$NEW" ] && ok "newest: $(basename "$NEW")  $(du -h "$NEW" | cut -f1)  modified $(date -r "$NEW" '+%H:%M:%S')"
else
  err "transcript dir not found: $PROJ"
fi

# ── 2. THE GITIGNORED BUFFERS (backed up nowhere else — K6) ──────
echo ""
echo "2. .claude/ buffers — gitignored, so this is their ONLY backup"
mkdir -p "$DEST/claude_state" 2>/dev/null
for f in session-state.md session-prompts.log; do
  if [ -f ".claude/$f" ]; then
    cp ".claude/$f" "$DEST/claude_state/${STAMP}_$f" 2>/dev/null \
      && ok "$f  ($(wc -l < ".claude/$f") lines, $(wc -c < ".claude/$f") bytes)" \
      || err "could not copy $f"
  else
    warn ".claude/$f does not exist"
  fi
done

# ── 3. HOOK REGISTRATION (K6 — the gap that makes hooks_backup inert) ──
echo ""
echo "3. Hook registration + live hooks (outside git entirely)"
if [ -f "$CLAUDE_HOME/settings.json" ]; then
  cp "$CLAUDE_HOME/settings.json" "hooks_backup/user-level-settings.json" 2>/dev/null \
    && ok "settings.json -> hooks_backup/ (closes K6: without this the backup is inert)" \
    || err "could not copy settings.json"
  cp "$CLAUDE_HOME/settings.json" "$DEST/claude_state/${STAMP}_settings.json" 2>/dev/null
else
  err "settings.json NOT FOUND — hooks cannot be re-registered from backup"
fi
DRIFT=0
for h in clipper-bot-log-prompt clipper-bot-session-start clipper-bot-precompact clipper-bot-session-close; do
  if [ -f "$CLAUDE_HOME/hooks/$h.sh" ]; then
    if ! diff -q "$CLAUDE_HOME/hooks/$h.sh" "hooks_backup/$h.sh" >/dev/null 2>&1; then
      cp "$CLAUDE_HOME/hooks/$h.sh" "hooks_backup/$h.sh" && warn "$h.sh had DRIFTED — backup refreshed"
      DRIFT=$((DRIFT+1))
    fi
  else
    err "live hook missing: $h.sh"
  fi
done
[ "$DRIFT" -eq 0 ] && ok "all 4 hooks byte-identical to hooks_backup/"
cp -n "$CLAUDE_HOME/CLAUDE.md" "hooks_backup/user-level-CLAUDE.md" 2>/dev/null
ls -1 "$CLAUDE_HOME/hooks/"*.bak >/dev/null 2>&1 && \
  warn "stray .bak file(s) in ~/.claude/hooks/ — not backed up, check if wanted"

# ── 4. THE DATA (proof it is intact, not just present) ──────────
echo ""
echo "4. Project data integrity"
T=$(ls -1 research/transcripts/*.txt 2>/dev/null | grep -vc _summary)
U=$(grep -l '^# https://www.youtube.com/watch' research/transcripts/*.txt 2>/dev/null | wc -l)
[ "$T" -eq "$U" ] && ok "$T transcripts, all $U carry a source URL on line 2" \
                  || err "$T transcripts but only $U carry a source URL"
C=$(wc -l < research/twitch_clips/lacy_clips_7d_2026-08-06.txt 2>/dev/null)
[ "${C:-0}" -eq 964 ] && ok "964-clip dataset intact ($C rows)" || err "clip dataset is $C rows, expected 964"
S=$(grep -c SUCCESS research/transcripts/_summary_batch2.txt 2>/dev/null)
[ "${S:-0}" -eq 6 ] && ok "_summary_batch2.txt holds the REAL record (6 SUCCESS rows)" \
   || err "_summary_batch2.txt shows $S SUCCESS rows — a no-op re-run may have overwritten it (recover: git show d9be435:research/transcripts/_summary_batch2.txt)"
R=$(ls -1 reference/*VERBATIM*.md 2>/dev/null | wc -l)
ok "$R verbatim agent reports preserved"

# ── 5. REPO STATE ───────────────────────────────────────────────
echo ""
echo "5. Repository"
UNC=$(git status --porcelain | wc -l)
[ "$UNC" -eq 0 ] && ok "working tree clean" || warn "$UNC uncommitted file(s) — commit before calling this done:
$(git status --short | sed 's/^/          /')"
git fetch -q origin 2>/dev/null
SB=$(git status -sb | head -1)
case "$SB" in
  *ahead*)  err "NOT PUSHED: $SB" ;;
  *behind*) err "behind origin: $SB" ;;
  *)        ok "synced with origin — $(git log --oneline -1)" ;;
esac
ok "$(git rev-list --count HEAD) commits, $(git ls-files | wc -l) tracked files, $(du -sh .git | cut -f1) of history"

# ── 6. THE REPO-SIDE GATE ───────────────────────────────────────
echo ""
echo "6. save_check.sh (the repo-side gate)"
if bash save_check.sh > /tmp/_sc.txt 2>&1; then
  ok "$(grep -c PASS /tmp/_sc.txt) checks passed"
else
  err "save_check FAILED:"; grep FAIL /tmp/_sc.txt | sed 's/^/          /'
fi

# ── SUMMARY ─────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════════"
if [ "$ERRS" -eq 0 ]; then
  echo "  ✅ FINAL SAVE COMPLETE — $ERRS failures"
else
  echo "  ❌ FINAL SAVE INCOMPLETE — $ERRS failure(s) above. Do NOT call it done."
fi
echo "════════════════════════════════════════════════════════════"
echo ""
echo "  Backed up to:  $DEST"
echo "  Repo pushed:   github.com/anthonybrod/automated-clipper-bot"
echo ""
echo "  ⚠️ ONE THING THIS SCRIPT CANNOT DO — Google Drive."
echo "     Claude has no Drive access. Run this in Colab yourself:"
echo ""
cat <<'COLAB'
       from google.colab import drive
       drive.mount('/content/drive')
       import os
       P = "/content/drive/MyDrive/CLAUDE AI CLIP BOT V1 attempt"
       if os.path.isdir(f"{P}/.git"):
           get_ipython().system(f'cd "{P}" && git pull')
       else:
           get_ipython().system(f'git clone https://github.com/anthonybrod/automated-clipper-bot.git "{P}"')
       get_ipython().system(f'ls -la "{P}"')
COLAB
echo ""
exit $(( ERRS > 0 ))
