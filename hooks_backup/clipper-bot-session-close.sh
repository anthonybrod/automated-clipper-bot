#!/usr/bin/env bash
# Stop hook: (1) reminds to update START_HERE.md before a final push,
# (2) surfaces broken doc links. ALWAYS exits 0 - must never block a session.
REPO="/c/Users/AwBro/Desktop/automated clipper bot"
[ -d "$REPO/.git" ] || exit 0

DIRTY=$(cd "$REPO" && git status --porcelain 2>/dev/null | wc -l)

# link rot: only when there ARE changes (a rename could have broken a link)
if [ "$DIRTY" -ge 1 ] && [ -f "$REPO/check_links.sh" ]; then
  BROKEN=$(cd "$REPO" && bash check_links.sh 2>/dev/null | grep -c '^BROKEN:')
  [ "$BROKEN" -gt 0 ] && echo "WARNING (clipper bot): $BROKEN broken doc link(s). Run 'bash check_links.sh' - a link pointing at a renamed/deleted file silently breaks the cold-start path."
fi

[ "$DIRTY" -lt 2 ] && exit 0
TOUCHED=$(cd "$REPO" && git status --porcelain 2>/dev/null | grep -c "START_HERE.md")
if [ "$TOUCHED" -eq 0 ]; then
  echo "REMINDER (clipper bot): $DIRTY uncommitted changes, and START_HERE.md is not among them. Before the final push, update it - state now, next action, blockers, and the real commit hash. A stale START_HERE.md is what breaks the next cold start."
fi
exit 0
