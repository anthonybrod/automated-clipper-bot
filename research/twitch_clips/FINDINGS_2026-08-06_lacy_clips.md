# Findings — 964 real Lacy Twitch clips, 7 days (2026-08-06)

**What this is.** First-party data pulled directly from
`twitch.tv/lacy/clips?range=7d` with `yt-dlp`, no auth and no API key. Raw
rows in [`lacy_clips_7d_2026-08-06.txt`](lacy_clips_7d_2026-08-06.txt),
format `duration|view_count|title`.

**Why it matters more than anything else in `reference/`.** Every other
source in this repo is somebody talking *about* clipping. This is **964
moments that real humans actually chose to clip, with the view count each
one earned.** It is free, it refreshes daily, and it is the closest thing
the project has to ground truth.

**Source confirmed by the user 2026-08-06:**

| | URL |
|---|---|
| Channel | `twitch.tv/lacy` |
| VODs | `twitch.tv/lacy/videos` |
| Clips, 24h | `twitch.tv/lacy/clips?range=24hr` |
| Clips, 7d | `twitch.tv/lacy/clips?range=7d` |

**Stage 1 is no longer theoretical.** `yt-dlp` reached both the VOD list
(real titles/durations/IDs, e.g. a 10,003s stream) and the clip list, with
no credentials. The Twitch assumption in the Architecture Outline was
correct after all — it just traced through a wrong target handle.

---

## Duration

| Metric | Value |
|---|---|
| Median | **30s** |
| Mean | 35.5s |
| p25 / p75 | 29s / 49s |
| Min / max | 4s / 60s |

**71% of all clips sit at exactly 30s, 59s or 29s.** That is not a property
of the moments — those are **Twitch's clip-tool UI presets**. Clippers hit
the default and move on.

> ### ⚠️ The correction this forces
> **Twitch clip durations measure the tool, not the moment.** They cannot be
> used to derive how long a good moment *is*. G2's median of 39.5s came from
> a YouTube best-of where an editor chose each boundary freely; that number
> describes editorial judgement, this one describes a slider.
>
> **What does corroborate:** G2's *acceptance band*. It proposed 20–70s, and
> **89% (862/964) of real clips fall inside it.** Two independent sources,
> different methods, same range. That band is safe to build on.
>
> **What does not:** any single "target length" taken from Twitch data.

## Views — the finding that changes the business case

| Metric | Value |
|---|---|
| Median | **5 views** |
| Mean | 35 |
| Max | 7,073 |
| All 964 clips combined | 33,624 |

| Threshold | Clips | Share |
|---|---|---|
| ≥ 5,000 | **1** | 0.1% |
| ≥ 1,000 | **6** | 0.6% |
| ≥ 500 | 9 | 0.9% |
| ≥ 100 | 34 | 3.5% |
| ≥ 50 | 72 | 7.5% |

**Top clip ÷ median = ~1,400×.** The distribution is brutally power-law:
99.4% of community-clipped moments never reach 1,000 views on Twitch.

> **⚠️ Read this carefully — it is not a payout prediction.** Twitch clip
> views and reposted Shorts/X views are different audiences with different
> discovery mechanics. A clip that dies on Twitch can travel elsewhere.
>
> **What it does establish:** *selection is where all the value is.* If the
> bot posts an average moment it earns roughly nothing; the entire return
> lives in the top ~1%. That is a direct, evidence-based justification for
> the three-stage funnel and for every hour spent on detection quality —
> and it raises the stakes on the minimum-view-threshold rule, since most
> moments would land under it.

## Titles as a free signal

Clipper-written titles are blunt and label the moment type directly —
`lacy sad`, `lacy on dem percs`, `prank call`, `Ron hates lacy`,
`lacy has to pee in bottle on stream`, `LacyStreams while still high after
knee surgery` (7,073 views, the top clip).

Cross-reference against G2's moment taxonomy (physical escalation 28%,
verbal roast 20%, authority 12%, reveal 12%, romance 12%, heist 10%,
one-liner 6%) — **not yet done**, on the to-do list.

---

## What this makes possible (queued, not built)

**An evaluation harness the project currently has no equivalent of.** Right
now there is no way to measure whether a detector is any good. But every
clip here carries a view count and points back into a VOD — so a detector
can be run over that VOD and scored on whether the moments it picks match
the clips that actually earned views. **Ground truth, for free, refreshing
daily.** Nothing else in the repo can measure detector quality at all.

## Caveats, stated rather than buried

- **7-day window only.** No seasonality, no comparison period.
- **Views were read at one moment in time** and keep accruing; recent clips
  are undercounted relative to older ones.
- **Community selection is itself biased** — it reflects who was watching
  live and felt like clipping, not an objective "best moment."
- **964 rows, some titles contained non-UTF-8 bytes** and were read with
  replacement characters. Durations and view counts are unaffected.
- **Kick was NOT pulled** at the user's instruction — nearly empty today.
