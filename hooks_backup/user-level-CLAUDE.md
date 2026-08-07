# Global instructions (all projects, all directories)

## 🚩 Working on the Automated Clipper Bot?

If this session touches the **Twitch clipping bot** (@LacyCrashOuts clips,
`automated-clipper-bot`, Clipping.net bounties, or anything in
`C:\Users\AwBro\Desktop\automated clipper bot`):

**Read `C:\Users\AwBro\Desktop\automated clipper bot\START_HERE.md` first.**
It is that project's single session entry point — state right now, the
single next action, blockers and open leads, how we work, and where
everything is. Then that repo's own `CLAUDE.md` (21 numbered rules, 16
active) and `PROJECT.md`.

**Do not reconstruct that project's plan from memory, from chat history, or
from a summary — read the files.** They are written to be read cold and
have been validated doing so.

**Why this lives here (user-level) and not only in the project:** a
project's `CLAUDE.md` only auto-loads when the session is *rooted in that
directory*. Sessions have repeatedly been rooted elsewhere — most often in
the sibling project `C:\Users\AwBro\Desktop\youtube auto videos` — where
the clipper bot's instructions never load at all. A cold-start test on
2026-08-03 confirmed this silent failure. **This file is the only
instruction path that fires regardless of working directory.**

Three non-negotiables that apply the moment that project comes up, before
reading anything else:

1. **The user has final say** on phase transitions and on anything being
   called complete. Nothing is written as complete until they say so
   in-session; when they do it is stamped
   `✅ COMPLETE — authorized by user YYYY-MM-DD`. Until then the only
   honest statuses are *in progress*, *awaiting user approval*, or
   *blocked*.
2. **Ask before launching agents, and confirm usage headroom first.**
   Budget is a live constraint — metered. ⚠️ THE RESET MECHANIC IS
   UNCONFIRMED: this line long claimed "hard weekly reset Monday 1pm" but the
   user never said that. What they actually report is a ~5-HOUR ROLLING
   SESSION WINDOW plus a MONTHLY credit reset. Pace against the 5-hour window;
   ask them to confirm.
   hit repeatedly. One session went fresh to 100% on a single agent plus
   note-keeping.
3. **Nothing is factual** unless confirmed in-session or the user OK'd it
   — including notes from past sessions, other AI output, and Claude's own
   earlier conclusions. Those are leads to verify, not facts to build on.

---

## Environment facts (this machine)

- **Real Python interpreter** — `python` and `py` do NOT resolve (Windows
  Store stub). Use:
  `C:\Users\AwBro\AppData\Local\Programs\Python\Python312\python.exe`
- **Google Drive** — no Desktop app installed, no API access, and browser
  sign-in walls block it. Claude cannot read or write Drive. The working
  pattern is: Claude pushes to GitHub, the user pulls in Colab. A fresh
  Colab runtime needs `drive.mount()` before any `git -C ... pull` will
  work, or the path won't exist.
