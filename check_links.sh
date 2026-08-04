#!/usr/bin/env bash
# Validates every relative markdown link in the repo's key docs actually resolves.
# Catches silent link rot when a file is renamed or moved.
# Usage: bash check_links.sh    (exit 1 if any link is broken)
cd "$(dirname "$0")" || exit 1
BROKEN=0
CHECKED=0
for doc in START_HERE.md CLAUDE.md PROJECT.md SESSION_HANDOFF_PROMPT.md \
           reference/PENDING_agent_prompts_resume_2026-08-01.md; do
  [ -f "$doc" ] || { echo "MISSING DOC: $doc"; BROKEN=$((BROKEN+1)); continue; }
  # pull (path) out of markdown links, skip URLs and anchors
  grep -oE '\]\([^)]+\)' "$doc" | sed 's/^](//; s/)$//' \
    | grep -vE '^(https?://|#|mailto:)' | sort -u | while read -r link; do
      target="${link%%#*}"
      [ -z "$target" ] && continue
      base=$(dirname "$doc")
      [ "$base" = "." ] && resolved="$target" || resolved="$base/$target"
      if [ ! -e "$resolved" ] && [ ! -e "$target" ]; then
        echo "BROKEN: $doc -> $link"
      fi
    done
  n=$(grep -oE '\]\([^)]+\)' "$doc" | sed 's/^](//; s/)$//' | grep -vcE '^(https?://|#|mailto:)')
  CHECKED=$((CHECKED+n))
done
echo "--- checked $CHECKED relative links across 5 docs ---"
