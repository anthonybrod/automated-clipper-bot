# CORE clippers on X — named-account deep dive (VERBATIM agent report)

**Date:** 2026-08-06
**Accounts researched (user-supplied, exact handles):**
1. yoxic — `@yoxics`
2. ryan 🤿 — `@scubaryan_`
3. Core Culture — `@coresculture`

**What this file is:** the verbatim output of a research agent, task H1. It supersedes
nothing; it is the measured companion to
`research_2026-08-04_core_clippers_discovery_VERBATIM.md` (task H2), which was
scene-level and largely REPORTED. This one is largely **VERIFIED** because a public
mirror worked.

**Evidence grading used throughout:**
- **VERIFIED** — the agent fetched it and saw it. URL given.
- **REPORTED** — a source says so. URL given.
- **UNVERIFIED** — inference or unconfirmed.

---

## 0. ACCESS STATUS — READ FIRST

### What FAILED
- **Direct `x.com` / `twitter.com` page loads** — gated, as expected. Not usable.
- **`xcancel.com` (Nitter instance)** — returned a "Checking your browser" bot-check
  interstitial. No timeline. **VERIFIED failure**, fetched 2026-08-06.
- **`api.vxtwitter.com`** — redirected to the project's GitHub page instead of serving
  JSON. **VERIFIED failure.**
- **Full user timelines** — no endpoint reachable returns a list of an account's posts.
  Every status ID below had to be found one at a time through web search. **This is the
  single biggest limitation of this report** and it biases the sample (see §5).
- **Watching the videos.** I could not play any clip. Everything about motion — zoom
  rhythm, cut count, where the hook lands in the first 1–3 seconds, audio — is therefore
  **NOT** established by this report.

### What WORKED — the breakthrough
**`api.fxtwitter.com/<handle>/status/<id>` serves public JSON with no authentication.**
It returns verbatim post text, likes, retweets, replies, **view counts**, timestamps,
author profile stats, and — critically — **exact video duration in seconds plus pixel
width and height.**

**`api.fxtwitter.com/<handle>` serves the profile object** (followers, lifetime tweet
count, lifetime media count, join date).

**Video poster-frame thumbnails on `pbs.twimg.com` download unauthenticated**, so I
downloaded and visually inspected 5 of them. That is the only direct visual evidence in
this report.

> ⚠️ **Caveat on the thumbnails.** X's `amplify_video_thumb` is the poster frame. It is
> *usually* at or near the first frame, but I cannot prove it is frame 0 for any given
> clip. Treat thumbnail observations as **"a frame from early in the clip,"** not as a
> guaranteed reading of second 0. Hook analysis below is weaker than the duration
> analysis for exactly this reason.

### Sample size actually obtained
| Account | Posts with full metrics | Of which video (duration known) |
|---|---|---|
| `@yoxics` | 7 | 7 |
| `@scubaryan_` | 11 | 6 |
| `@coresculture` | 7 | 5 |
| **Total** | **25** | **18** |

A handful of older `@scubaryan_` IDs surfaced by search returned HTTP 404 through the
mirror (listed in §5). Cause not established — deletion, or a stale search index.

---

## 1. THE HEADLINE FINDING — LENGTH vs TWITCH'S PRESETS

This is the comparison the task asked for, and it came out clean.

**All 18 observed durations, sorted (seconds) — all VERIFIED:**

```
16.350  17.463  22.350  29.117  37.966  38.483  42.920  45.616  47.550
55.296  56.710  57.170  57.416  59.328  60.000  60.000  60.033  126.400
```

| Measure | Reposted clips on X (this report, n=18) | Lacy raw Twitch clips (user's own 964-clip pull) |
|---|---|---|
| Median duration | **51.4 s** | **30 s** |
| Share in the 55–61 s band | **8 / 18 = 44%** | — |
| Share at/near 30 s (28–31 s) | **1 / 18 = 6%** | — |
| Share landing on 30/59/29 s exactly | **0 / 18 = 0%** | **71%** |

### Two conclusions, both load-bearing

**1. Reposts are much longer than Twitch's 30 s default. They cluster at ~60 s, not 30 s.**
The mass sits at 55–60 s. Only one clip in eighteen is anywhere near 30 s. If the bot
defaults to Twitch's 30 s preset it is producing clips at roughly half the length these
successful accounts actually ship. **The Twitch preset that matches this behaviour is
the 59 s one, not the 30 s one.**

**2. Not one clip lands on a Twitch preset value — they are hand-trimmed.**
Every duration is an irregular decimal: 38.483, 42.920, 45.616, 47.550, 55.296, 57.416,
59.328. Twitch's clip tool emits 30/59/29. **Zero of eighteen** match. The only round
values are 60.000 (×2) and 60.033, which read as a deliberate 60-second cap, not a tool
preset.

> **Implication:** these accounts are **not pressing Twitch's clip button.** They capture
> the stream and trim by hand (or by script) to a target. This directly explains the
> artifact the user already found in the 964-clip Twitch pull: the 30/59/29 spike
> measures Twitch's UI, and the people actually earning from reposts have left that UI
> behind entirely.

**One long outlier:** `@coresculture` posted a **126.4 s** clip and it was the
worst-performing video in that account's sample (4,958 views, 69 likes) —
https://x.com/coresculture/status/2080835599892660396 (**VERIFIED**). Single data point;
suggestive, not conclusive.

---

## 2. FORMAT — WHAT I ACTUALLY SAW

I downloaded and viewed 5 poster frames. This section is the most concrete visual
evidence in the report, and it **contradicts the common assumption that repost clipping
means vertical 9:16 short-form editing.**

### Aspect ratios observed (VERIFIED, from media width×height)

| Post | Pixels | Shape |
|---|---|---|
| yoxics IShowSpeed crashout | 1920×1080 | 16:9 landscape |
| yoxics "🤧💔" | 1920×1080 | 16:9 landscape |
| yoxics Cybertruck | 1920×1080 | 16:9 landscape |
| scubaryan_ Peterbot | 1920×1080 | 16:9 landscape |
| scubaryan_ Jynxzi peak | 1920×1080 | 16:9 landscape |
| scubaryan_ Kai/Adin beef | 1920×1080 | 16:9 landscape |
| coresculture Jynxzi revenue | 1920×1080 | 16:9 landscape |
| coresculture JShock | 1920×1080 | 16:9 landscape |
| scubaryan_ Kai/Jynxzi collab | 1280×720 | 16:9 landscape |
| scubaryan_ Adin beef | 1280×720 | 16:9 landscape |
| coresculture wheelchair | 1280×720 | 16:9 landscape |
| coresculture ragebait | 1280×720 | 16:9 landscape |
| yoxics retiring | 1128×1080 | near-square composite |
| yoxics left CORE | 1398×1080 | near-square composite |
| yoxics cameraman 30% | 1366×1080 | near-square composite |
| coresculture ACL tears | 1440×1080 | 4:3 |
| yoxics TikTok crush | 726×720 | ~1:1 square |

**Not one clip in the sample is 9:16 vertical.** No 1080×1920, no 608×1080. **VERIFIED.**

### What the frames actually show

**(a) Raw 16:9 stream capture, chat burned in, no clipper branding.**
`@yoxics` IShowSpeed crashout (2.04M views) — poster frame shows IShowSpeed's streaming
room, and **live Twitch chat is visible in the top-right of the frame**, legible
messages including `cephalonnnx: backflip onto them`. A red number `9949` sits in the
bottom-left. There are **no burned-in subtitles, no facecam inset, and no @yoxics
watermark or logo anywhere in the frame.**
https://x.com/yoxics/status/2027419134309601459 (**VERIFIED**, frame inspected)

`@scubaryan_` Peterbot clip — same story: raw IRL 16:9, **Twitch chat burned into the
top-right** (`Loiterzz: LARPERS`, `ftfreddy_z: shave bro`), a red `7767` bottom-right, no
subtitles, no watermark.
https://x.com/scubaryan_/status/2077139224642404786 (**VERIFIED**, frame inspected)

`@coresculture` Jynxzi revenue leak — raw 16:9 webcam shot with the **source stream's own
overlay retained**: Twitch glyph + `72,375` top-left, a subathon timer reading
`34 HOURS 12 MINUTES 15 SECONDS` top-right, `101,399` bottom-right. No subtitles, no
watermark.
https://x.com/coresculture/status/2060953804778910030 (**VERIFIED**, frame inspected)

> The red/white corner numbers appear on clips from *different* streams and different
> clipper accounts. I did **not** establish what they are. Most likely part of the source
> streamer's own overlay (live viewer or donation counter). **UNVERIFIED.**

**(b) The odd aspect ratios are side-by-side composites, not crops.**
This corrects an inference I nearly made. `@yoxics` "stepping away from streaming"
(1128×1080) is a **two-panel split screen**: left panel is Lacy talking to camera, right
panel is separate phone footage of several people looking down into a camera. So
1128×1080, 1398×1080 and 1366×1080 are **two vertical/phone sources placed side by
side**, producing a near-square canvas — genuine editing, not a crop of a 16:9 frame.
https://x.com/yoxics/status/2051720582346256462 (**VERIFIED**, frame inspected)

**(c) Subtitles appear only when inherited from the source.**
`@yoxics` "TikTok crush" (726×720, 17.5 s) shows a Top Golf scene with a **burned-in
caption reading `aura.`** in white text with a black outline, centre-lower — the styling
of TikTok/CapCut auto-captions. This clip is square and short, consistent with a
phone/TikTok-sourced repost that already had captions.
https://x.com/yoxics/status/1877024110363967558 (**VERIFIED**, frame inspected)

### Format summary
| Attribute | Finding | Grade |
|---|---|---|
| Aspect ratio | 16:9 landscape dominant (12/17); near-square composites for multi-source; never 9:16 | VERIFIED |
| Subtitles added by clipper | **None observed.** Captions appear only when carried over from a phone/TikTok source | VERIFIED on 5 frames |
| Clipper watermark / branding | **None observed in any frame** | VERIFIED on 5 frames |
| Stream chat visible | **Yes, frequently** — burned in, inherited from source capture | VERIFIED on 2 frames |
| Source-stream overlays (timers, viewer counts) | Left in, not cropped out | VERIFIED on 1 frame |
| Facecam layout | Source-native; no clipper-added inset | VERIFIED on 5 frames |
| Zoom / cut rhythm | **NOT ESTABLISHED** — could not play video | UNVERIFIED |

> **Blunt read for the bot:** the format bar these accounts clear is *low*. There is no
> subtitle burn-in, no reframing, no branding, no vertical conversion. The work is
> **moment selection and caption writing**, not editing. A pipeline that screen-captures
> 16:9, trims to ~55–60 s, and writes a good caption is format-competitive with accounts
> at 600K+ followers.

---

## 3. PER-ACCOUNT

### 3a. `@yoxics` — "yoxic"

**Profile (VERIFIED, fetched 2026-08-06 via api.fxtwitter.com/yoxics):**
- Followers **610,749** · Following 955 · Likes given 229,343
- **Lifetime tweets 97,215 · lifetime media posts 28,212**
- Joined **Wed Jun 22 2016**
- Bio verbatim: `FBI ASSOCIATE | powered by @roobet` · Location field: `dm 4 promo 🪐`
- Verified: yes (individual)

> Corrects H2's REPORTED figures of 533.4K / 603K. The live number is **610,749**.
> H2's warning about impostor handles `@yoxicz` and `@y0xics` still stands and was not
> re-tested.

**Derived cadence (UNVERIFIED arithmetic on VERIFIED inputs):** 97,215 posts over ~3,697
days = **~26 posts/day lifetime average**; 28,212 media posts = **~7.6 media posts/day
lifetime average**. Lifetime averages, not current rate — treat as an order of magnitude.

**Observed posts (all VERIFIED):**

| Date (UTC) | Duration | Pixels | Views | Likes | RTs | Replies | Caption (verbatim) |
|---|---|---|---|---|---|---|---|
| 2026-07-30 16:31 | 57.416 s | 1366×1080 | 1,021,709 | 6,199 | 46 | 154 | "Lacy revealed that he is now taking 30% of his cameraman's Twitch stream revenue after learning that he earns thousands of dollars per month from his viewers on top of his salary 😳" |
| 2026-06-28 21:37 | 42.920 s | 1398×1080 | 1,453,062 | 6,459 | 59 | 151 | "Lacy reveals he has officially parted ways with the new streaming group CORE after things didnt align with eachother 💔 / \"I know this is very similar to KSI leaving Sidemen.. but I wish the best for all the guys\"" |
| 2026-06-04 22:43 | 60.000 s | 1920×1080 | 103,143 | 1,045 | 9 | 43 | "Lacy reveals his 1 of 40 widebody Cybertruck with Forgiato wheels 🔥" |
| 2026-05-05 17:48 | 47.550 s | 1128×1080 | 961,060 | 3,941 | 45 | 331 | "Lacy reveals he's officially stepping away from Streaming to pursue a different career 💔 / \"I'm thinking about retiring I've gotten opportunities that I've dreamed of since a kid.. I love you guys maybe you'll see me soon, or maybe you wont\"" |
| 2026-02-27 16:22 | 38.483 s | 1920×1080 | **2,042,638** | **21,709** | 328 | 92 | "IShowSpeed crashed out on Marlon, Lacy and Jasontheween for breaking his fake bed in his streaming room made out of toilet paper 😭" |
| 2025-08-24 03:09 | 59.328 s | 1920×1080 | 1,116,225 | 19,140 | 274 | 146 | "🤧💔" |
| 2025-01-08 16:06 | 17.463 s | 726×720 | 376,078 | 1,718 | 11 | 23 | "Lacy showing off infront of his TikTok crush 😳" |

- **Median views across these 7: 1,021,709.**
- **Streamer subject:** Lacy in 6 of 7 (the 7th, "🤧💔", subject not established).
  This account is heavily Lacy-centric despite being a general streamer page.
- **Moment types:** reveal/announcement dominates (5 of 7 — career news, breakup with
  CORE, car reveal, revenue split). One rage/crashout. One flex/social.
- **Notable:** the single best performer (2.04M views) is the **rage/crashout**, and it is
  also the **shortest of the long-form clips at 38.5 s.** The pure announcement posts got
  ~1M. **UNVERIFIED as a rule** — n is small.

---

### 3b. `@scubaryan_` — "ryan 🤿"

**Profile (VERIFIED, fetched 2026-08-06 via api.fxtwitter.com/scubaryan_):**
- Followers **691,076** · Following 1,694
- **Lifetime tweets 88,483 · lifetime media posts 18,403**
- Joined **Sun Jul 03 2022**
- Bio verbatim: `not impersonating anyone ~ daily streamer clips and other news | sponsored by @rainbetcom 🤿`
- Verified: yes

**Derived cadence (UNVERIFIED arithmetic on VERIFIED inputs):** 88,483 posts over ~1,495
days = **~59 posts/day lifetime average**; 18,403 media = **~12.3 media posts/day
lifetime average**. Highest cadence of the three by a wide margin.

**Observed posts (all VERIFIED):**

| Date (UTC) | Duration | Pixels | Views | Likes | RTs | Replies | Caption (verbatim) |
|---|---|---|---|---|---|---|---|
| 2026-08-06 17:56 | 2 photos | 1320×1315, 648×648 | 169,167 | 1,569 | 43 | 144 | "the eSports Awards have officially released the nominees for Streamer of the Year 👀🔥" + list of 12 nominees |
| 2026-07-19 00:40 | 60.033 s | 1920×1080 | 154,329 | 6,567 | 169 | 47 | "the Class of 2026 has won the Streamer University basketball match with ClarenceNYC being crowned the MVP by Kai Cenat 😭🔥" |
| 2026-07-14 21:12 | 45.616 s | 1920×1080 | 595,245 | 12,201 | 106 | 47 | "Lacy randomly runs into Peterbot after the Spain vs France World Cup match 😭" |
| 2026-06-10 00:26 | 2 photos | 526×385, 1280×1261 | 799,921 | 7,960 | 215 | 177 | "Kai Cenat's 2026 Streamer University has created a buzz after being announced with athletes and even rappers applying to join 👀🔥 / - Tony Jefferson (NFL) / - Finesse2tymes / - Chrisean Rock / - Ayo & Teo / + many more…" |
| 2026-05-11 20:07 | 22.350 s | 1920×1080 | 222,852 | 1,924 | 18 | 32 | "Jynxzi officially reached his PEAK viewership (253k+) while hosting his League of Legends tournament and couldn't believe it 😭❤️‍🩹 / \"I've been streaming for 7 years… this is the most viewers I've ever hit…\"" |
| 2025-08-26 19:51 | 2 photos | 807×1076, 999×1159 | 1,156,119 | 22,862 | 570 | 170 | "Kai Cenat's 'Streamer University' has been confirmed to return in 2026 👀🔥" |
| 2025-07-26 17:18 | 56.710 s | 1280×720 | 1,082,675 | 16,842 | 209 | 178 | "Kai Cenat says he wants to do another collab with Jynxzi after feeling bad for cancelling their Clash Royale stream due to AMP wanting to do an IRL event the same night ❤️‍🩹" |
| 2025-07-18 01:23 | 16.350 s | 1920×1080 | 544,368 | 6,495 | 102 | 65 | "Kai Cenat responds to people saying he doesn't like Adin Ross and has \"beef\" with him 👀 / \"I got nothing but respect for Adin, I ain't never had a problem with Adin… Adin is my brother.\"" |
| 2025-04-07 01:42 | 37.966 s | 1280×720 | 159,169 | 2,069 | 33 | 38 | "Adin Ross speaks on people creating a \"beef\" between him and Kai Cenat when there isn't any between them personally 👀" |
| 2024-12-12 01:52 | not returned | — | 895,425 | 9,725 | 114 | 81 | "PlaqueBoyMax confronts Lacy for deleting his album that was dropping this month and smacked him 😬" |
| 2024-05-29 19:20 | not returned | — | **1,942,014** | **23,708** | 457 | 111 | "Lacy tried fitting in with Silky and Max but ended up ruining the whole vibe 💀" (bookmarks: 2,189) |

- **Median views across these 11: 595,245.**
- **Streamer subject:** this is a **broad streamer beat, not a CORE page.** Kai Cenat is
  the most frequent subject (5 of 11). Lacy appears in only 3 of 11. Adin Ross, Jynxzi,
  Speed, PlaqueBoyMax also feature. **Do not model this account as a Lacy/CORE
  competitor** — it competes for the same audience but sources far more widely.
- **Moment types:** roughly half are **news/announcement with a still image, not a clip**
  (3 of 11 are photo posts, and they perform *well* — 1.16M, 800K, 169K). Conflict/beef
  framing is a recurring device.
- **Highest performer** is a Lacy social-fail clip from 2024 (1.94M views).

---

### 3c. `@coresculture` — "Core Culture"

**This is the most relevant account of the three for the user's own channel**, because it
is small, new, and CORE-dedicated — i.e. it is the closest structural analogue to
x.com/CoreCrashOuts.

**Profile (VERIFIED, fetched 2026-08-06 via api.fxtwitter.com/coresculture):**
- Followers **6,540** · Following 31
- **Lifetime tweets 938 · lifetime media posts 682**
- Joined **Wed Oct 15 2025**
- Bio verbatim: `All CORE News, Updates & Content for @TheCoreBoys🔥` / `Powered by @Roobet.`
- Verified: yes

**Derived cadence (UNVERIFIED arithmetic on VERIFIED inputs):** 938 posts over ~295 days
= **~3.2 posts/day**; 682 media = **~2.3 media posts/day**. Roughly **73% of everything
this account posts carries media.**

**Observed posts (all VERIFIED):**

| Date (UTC) | Duration | Pixels | Views | Likes | RTs | Replies | Caption (verbatim) |
|---|---|---|---|---|---|---|---|
| 2026-07-25 02:00 | **126.400 s** | 1280×720 | 4,958 | 69 | 1 | 0 | "Lacy ragebaited Jynxzi over his soccer knowledge so hard that Jynxzi left the call and went on a full rant about it on his own stream 😭💀 / \"If Messi's so good, why did he go to a worse league? Because he can't compete with the best\"" |
| 2026-07-22 02:37 | 55.296 s | 1920×1080 | 7,017 | 127 | 0 | 2 | "JShock will be making his way to the CORE house to hang out if Lacy & the rest of the guys👀" |
| 2026-07-19 10:45 | 57.170 s | 1280×720 | 3,477 | 40 | 1 | 0 | "Full interaction of when YourRAGE & PayBae pulled Lacy out of his wheelchair and then made him cry by pulling on his leg with a torn ACL😢" |
| 2026-07-03 06:13 | 29.117 s | 1440×1080 | 7,638 | 160 | 0 | 1 | "Lacy was left in tears and ended his stream after saying he's terrified he could be in a wheelchair for up to a year following his ACL injury... 💔" |
| 2026-05-31 05:17 | 60.000 s | 1920×1080 | **344,114** | **4,403** | 22 | 8 | "StableRonaldo & Jynxzi's Head Moderator HiVise started panicking after they accidentally leaked Jynxzi's YouTube Revenue for the like 30 days which showed $2.8 Million🤯" |
| 2026-05-29 23:07 | photo | 1226×2048 | 3,349 | 108 | 0 | 0 | "Another shot of the CORE car collection🔥 / [via X @drewwall_]" |
| 2026-05-03 11:39 | 2 photos | 400×400, 401×521 | 186,685 | 4,958 | 45 | 22 | "Who else misses Bepsy & hopes to see him back with the CORE boys soon😔" |

**The economics finding — the single most useful number in this report for the user:**

- **Median views across these 7 posts: 7,017.** From a **6,540-follower** account.
- Compare to the user's own measurement of raw Lacy Twitch clips: **median 5 views**,
  with only 6 of 964 clips reaching 1,000.
- **The floor matters more than the ceiling.** Every one of the 7 observed
  `@coresculture` posts cleared **3,349 views minimum**. If a bounty threshold sits at
  1,000 views, **7 of 7 observed posts cleared it.** On Twitch, 958 of 964 clips did not.
- The distribution is still power-law: five posts sat at 3,349–7,638 while two hit
  186,685 and 344,114 — roughly **50× the median.**

> **UNVERIFIED but important caveat:** this is n=7, and the sample was assembled from
> search-indexed posts, which biases toward posts that got engagement (see §5). The true
> median for this account is probably **lower** than 7,017. The direction of the finding
> — that a small X repost account massively outperforms raw Twitch clip views — is
> robust; the exact figure is not.

- **Streamer subject:** CORE-focused as advertised. Lacy in 4 of 7, plus StableRonaldo,
  Jynxzi, JShock, Bepsy, and the CORE group collectively.
- **Moment types:** injury/sympathy arc is heavily worked (3 posts on Lacy's ACL alone),
  plus conflict/ragebait, a money reveal, and nostalgia.
- **Cross-posting/attribution:** this account **credits its sources in-caption** —
  `[via X @drewwall_]`. Neither larger account did so in any observed post.

---

## 4. CROSS-ACCOUNT PATTERNS

### 4a. Captions — the strongest and cleanest finding

Across **all 25 observed captions**:

1. **Zero hashtags. Not one, in any caption, on any of the three accounts. VERIFIED.**
   This is unambiguous and worth hard-coding: do not add hashtags.
2. **Near-universal terminal emoji.** Observed set: 😳 😭 💀 💔 🔥 👀 😬 🤯 😔 😢 ❤️‍🩹
   and combinations (👀🔥, 😭🔥, 😭💀, 🤧💔). Emoji is placed at the **end** of the claim,
   and is the tonal tell for the moment type — 💀/😭 for fails and comedy, 💔/😢 for
   sympathy, 🔥/👀 for reveals and hype, 🤯 for money/number reveals.
3. **Third person, past or present tense, streamer named first.** "Lacy reveals…",
   "Lacy tried…", "Kai Cenat responds…", "IShowSpeed crashed out on…", "PlaqueBoyMax
   confronts Lacy…". The subject's name is essentially always the first token.
4. **The caption gives away the payoff. It does not tease it.** These are not
   "wait for it" captions — they state exactly what happens, in full, including the
   outcome. "…and smacked him", "…left the call and went on a full rant",
   "…ended up ruining the whole vibe". **VERIFIED across the sample.** This is the
   opposite of curiosity-gap copywriting.
5. **The embedded pull-quote is a distinct, repeated device.** A blank line after the
   summary, then a verbatim quote from the clip in double quotes. Seen on at least 5
   posts across **all three** accounts. Examples: `@yoxics` 2071347208671354888 and
   2051720582346256462; `@scubaryan_` 2053929893319106836 and 1946017947752747509;
   `@coresculture` 2080835599892660396. **VERIFIED.**
6. **Bulleted list format for multi-fact news posts**, with a leading dash per line —
   `@scubaryan_` 2064504437440225286, `@yoxics` 2082866617453817941. **VERIFIED.**
7. **Length** is typically ~10–30 words for the summary line, extending further when a
   pull-quote or list is appended.

### 4b. Posting time-of-day (weak, small sample)

Observed post times, UTC:
- `@yoxics`: 03:09, 16:06, 16:22, 16:31, 17:48, 21:37, 22:43
- `@scubaryan_`: 00:26, 00:40, 01:23, 01:42, 17:18, 17:56, 19:20, 19:51, 20:07, 21:12
- `@coresculture`: 02:00, 02:37, 05:17, 06:13, 10:45, 11:39, 23:07

The two large accounts concentrate in roughly **16:00–02:00 UTC** (≈ midday to ~10pm US
Eastern), which maps onto US streaming hours. `@coresculture` skews later/scattered.
**UNVERIFIED as a strategy** — this is a byproduct of which posts search surfaced, not a
timeline scrape.

### 4c. Sponsorship
All three carry a gambling sponsor in bio: `@roobet` for `@yoxics` and `@coresculture`,
`@rainbetcom` for `@scubaryan_`. **VERIFIED from profile bios.** Consistent with H2's
finding that this is the scene's monetisation norm alongside bounties.

### 4d. Scale ladder (VERIFIED profile data, 2026-08-06)
| Handle | Followers | Lifetime posts | Lifetime media | Joined | Media/day (derived) |
|---|---|---|---|---|---|
| `@scubaryan_` | 691,076 | 88,483 | 18,403 | 2022-07-03 | ~12.3 |
| `@yoxics` | 610,749 | 97,215 | 28,212 | 2016-06-22 | ~7.6 |
| `@coresculture` | 6,540 | 938 | 682 | 2025-10-15 | ~2.3 |

---

## 5. HONEST LIMITATIONS — READ BEFORE ACTING ON ANY OF THIS

1. **Selection bias is the big one.** Every post here was found through a **search
   engine**, which indexes posts that got traction. **This sample is skewed toward
   winners.** It is decent evidence for *what successful reposts look like*, and poor
   evidence for *typical output* or *hit rate*. Any median view figure here is an
   overestimate. I could not obtain a single account's full timeline.
2. **Hook (first 1–3 seconds) is NOT established.** I could not play video. Poster-frame
   thumbnails are near-but-not-provably frame 0. **Requirement #1 of the task is only
   partially met and I am not going to pretend otherwise.**
3. **Zoom/cut rhythm: no evidence at all.**
4. **Cadence figures are lifetime averages** derived by arithmetic, and include replies.
   They are not measured current posting rates.
5. **Two `@scubaryan_` posts returned engagement but no media duration** through the
   mirror (1795897967016083691, 1867024599617245465). Not counted in the duration stats.
6. **These `@scubaryan_` IDs surfaced in search but returned HTTP 404 via the mirror**,
   cause unknown — deletion or stale index. Listed so nobody re-chases them blindly:
   `1949642487565291806`, `1920220850348814611`, `1869170850777411677`,
   `1919914855428952242`, `1821407341696188466`, `1831778880325349571`,
   `1920514701659611574`.
7. **n=18 for durations.** The 30 s-vs-55 s conclusion is strong (0/18 preset matches is
   hard to explain away) but it is still eighteen clips.
8. **Nothing here is a Clipping.net bounty figure.** No payout rate, no minimum view
   threshold, no bounty-program detail was verified. The economics in §3c is inference
   from view counts only.

---

## 6. WHAT THE USER MUST SUPPLY

The user is logged in; these gaps close fast with screenshots or pasted links.

**Highest value first:**

1. **Screen-record or describe the first 3 seconds of 5–10 of these clips.** This is the
   one requirement I could not meet. The specific posts most worth checking, because they
   are the verified top performers:
   - https://x.com/scubaryan_/status/1795897967016083691 (1.94M views)
   - https://x.com/yoxics/status/2027419134309601459 (2.04M views)
   - https://x.com/coresculture/status/2060953804778910030 (344K views, small account)
   Specifically: does the clip open **mid-action** or with lead-in? Is there a cut in the
   first second? Any added zoom-punch?

2. **A timeline scrape of `@coresculture`** — scroll its profile and save 30–50
   consecutive posts with view counts. This is the account that matters most (small,
   CORE-dedicated, structurally like CoreCrashOuts) and a *consecutive* run kills the
   selection bias that limits §3c. **The key unknown: what does a `@coresculture` post
   that flopped look like, and how often does that happen?**

3. **Confirm the Clipping.net bounty terms in writing** — exact $ per 1,000 views and
   the exact minimum view threshold. Everything in §3c about "clearing the threshold" is
   currently inference.

4. **Confirm whether the ~60 s cap is a platform constraint or an editorial choice.**
   Three clips landed at 60.000/60.033 s and one at 126.4 s, so 60 s is clearly not a hard
   platform limit for these accounts. Is it a bounty rule, a Roobet/Rainbet sponsor rule,
   or just taste? This determines whether the bot should target 55–60 s or go longer.

5. **Identify what the red/white corner numbers are** (`9949`, `7767`, `101,399`) — if
   they are a source-stream overlay, the bot should expect and preserve them; if they are
   something the clipper adds, that is a format element to replicate.

6. **Confirm whether `@scubaryan_` should be a model at all.** Verified here: it is a
   general streamer page where **Kai Cenat outnumbers Lacy 5-to-3** in the sample. It may
   be the wrong benchmark for a Lacy/CORE-only V1 bot.

---

## 7. SOURCE URLS (all fetched or search-surfaced 2026-08-06)

**Working public mirror (the enabling tool for this report):**
- `https://api.fxtwitter.com/<handle>` — profile JSON
- `https://api.fxtwitter.com/<handle>/status/<id>` — post JSON incl. views + video duration
- `https://pbs.twimg.com/amplify_video_thumb/...` — poster frames, unauthenticated

**Failed:** `https://xcancel.com/yoxics` · `https://api.vxtwitter.com/...` · direct x.com

**Posts cited (VERIFIED via mirror):**
- yoxics: /2082866617453817941 · /2071347208671354888 · /2062666597182103762 ·
  /2051720582346256462 · /2027419134309601459 · /1959452867636662307 · /1877024110363967558
- scubaryan_: /2085424815167479900 · /2078640994090660213 · /2077139224642404786 ·
  /2064504437440225286 · /2053929893319106836 · /1960429873442513150 · /1949157321382178959 ·
  /1946017947752747509 · /1909059083082019171 · /1867024599617245465 · /1795897967016083691
- coresculture: /2080835599892660396 · /2079757659964604875 · /2078793435692028295 ·
  /2072926796366922190 · /2060953804778910030 · /2060498409451147625 · /2050903123116318819

**Frames downloaded and visually inspected (5):** yoxics /2027419134309601459 and
/2051720582346256462 and /1877024110363967558 · scubaryan_ /2077139224642404786 ·
coresculture /2060953804778910030

---

*End of verbatim agent report — 2026-08-06.*
