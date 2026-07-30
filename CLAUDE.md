# Working on this repo

**Read [PROJECT.md](PROJECT.md) in full before making any claim about this
project's status, architecture, or backlog.** It is the single authoritative
reference. Chat history is not authoritative; PROJECT.md is. If something in
a conversation conflicts with PROJECT.md, PROJECT.md wins unless the code has
since changed (check the code, then update PROJECT.md — don't let it go stale).

Project in one line: **Automated Clipper Bot** — pulls the best clips from
Twitch VOD/streams, adds captions, produces YouTube Shorts + long-form
compilations, cross-posts. Separate project from `youtube-auto-videos`
(Parents Teach Kids), kept in its own folder/repo per explicit instruction,
but actively salvaging verified-working code/patterns from that project
where they fit — see PROJECT.md's Salvage Inventory.

Current state: pre-flight phase. No pipeline code has been written yet.
Before writing any real pipeline stage, prove out every hard dependency
(APIs, models, credentials, tools) the same way `validate_api_keys()` and
`discover_best_working_models()` did for the other project — catch failures
before they cost money or time, not after.

Any code, architecture, or "reference implementation" that arrives from an
external AI (labeled in PROJECT.md as "from Gemini" or similar) is treated as
inspiration only, never trusted or copied verbatim without independent
verification first — established project rule, since prior examples from
that source looked complete but had real bugs and unimplemented claims.
