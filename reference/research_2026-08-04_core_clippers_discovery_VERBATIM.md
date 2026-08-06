<!-- CORRECTION BANNER added 2026-08-06. The body below is UNCHANGED. -->
> ## ⚠️ RENAMED — `@LacyCrashOuts` is now `@CoreCrashOuts`
>
> This file predates 2026-08-06 and uses the old name. **It was always the
> OUTPUT channel** — where finished clips get posted — and it has simply
> been renamed. Some passages below describe it as a "target streamer";
> that was never accurate.
>
> | | Now |
> |---|---|
> | Output | **`x.com/CoreCrashOuts`** + **`youtube.com/@CORECrashOUTS`** |
> | Source (V1) | **`twitch.tv/lacy`** — VODs and `/clips?range=7d` |
> | Scope | V1 = Lacy only → V2 = the whole CORE group |
>
> **The body is deliberately left uncorrected** (Rule 16 — a raw record is
> never rewritten to reflect a later finding).

# CORE clipper discovery + scene conventions — VERBATIM agent report

**Date:** 2026-08-04
**Task:** (1) Identify large/successful "CORE" clipper accounts on X beyond the three
the user already named (@yoxics, @scubaryan_, @coresculture — covered by a separate
agent, deliberately not duplicated here). (2) Determine what the CORE clipping scene's
conventions actually are.
**Report type:** Verbatim agent report. Written by a research subagent. Nothing here is
project-approved fact. Every claim carries an evidence label.

**Evidence labels used throughout:**
- **VERIFIED** — I fetched the page myself and read its content. URL given.
- **REPORTED** — a source states it; I did not independently confirm. URL given.
  *Includes all follower counts* (see ACCESS STATUS — I never saw an X profile page).
- **UNVERIFIED** — could not confirm at all. Treat as a lead, not a fact.

---

## ⚠️ ACCESS STATUS — read first

**What I could NOT reach:**

| Target | Result |
|---|---|
| `x.com` / `twitter.com` direct fetch | **HTTP 402 Payment Required** on every attempt. Zero X pages read directly. |
| `publish.twitter.com/oembed` (tweet-text API) | 301 → `publish.x.com/oembed` → **HTTP 402**. Blocked. |
| `xcancel.com` (Nitter mirror) | Anti-bot challenge page. Blocked. |
| `r.jina.ai` proxy over x.com | **HTTP 403**. Blocked. |
| `sotwe.com` X profile mirrors | Appeared in search results, never successfully fetched. |
| `xbeast.io` X analytics | Fetched, but **all metrics behind a login wall**. Only a bare follower number was public. |
| `streamscharts.com` (Twitch clip stats) | **HTTP 403**. Blocked. |
| `sportskeeda.com` article fetch | **HTTP 405**. Blocked (search snippets only). |
| TikTok / Instagram profile pages | Not fetchable. |

**What I COULD reach:**
- WebSearch. **Critically: the search index returns X profile metadata** (bio text,
  follower count, join date) and **verbatim tweet text** inside result titles/snippets.
  Every handle, bio and follower number in this report came through that channel. It is
  second-hand and possibly stale. I have labelled all of it **REPORTED**, never VERIFIED.
- Full article fetches that worked: Tubefilter, Complex (×2), Forbes, KnowYourMeme,
  win.gg, coreboys.org, clipping.net, twitchmetrics.net.

**Consequence for this report:** I have **zero directly-observed X post data**. No view
counts, no like counts, no video durations, no subtitle screenshots, no aspect ratios
measured off an actual post. Section 3 (conventions) is built from *caption text and bio
text that the search index surfaced verbatim* plus published journalism. Section 4 (what
performs) is the weakest section and I say so there rather than padding it.

---

## 1. WHAT CORE IS

**Determination: CORE is a creator group / content house — an org, not a clipping niche
and not a clipping collective.** Confidence: **high**. Four independent sources agree.

- **CORE = "Create Own Run Everything"** — a streaming/creator group founded by six
  ex-FaZe Clan creators, operating out of a shared Los Angeles mansion.
  **VERIFIED** (fetched): https://www.tubefilter.com/2026/05/01/new-faze-clan-creator-group-house-core/
- **Founding six members:** Marlon, Adapt, Lacy, StableRonaldo, Silky, JasonTheWeen.
  **VERIFIED** (fetched, Tubefilter, same URL). Corroborated **REPORTED** by Complex:
  https://www.complex.com/pop-culture/a/jaelaniturnerwilliams/faze-marlon-adapt-new-streaming-group-core
- **Formed after FaZe Clan's collapse** — Tubefilter: established "five months after FaZe
  Clan's collapse," which it places around Christmas 2025; all six had left FaZe in the
  late-Dec-2025 exodus. **VERIFIED** (fetched, Tubefilter).
- **Reveal date reported as 30 April 2026**, during a livestream hosted by FaZe's former
  CEO Banks. **REPORTED** (search snippet, streamer.guide / win.gg):
  https://streamer.guide/blog/core-streaming-group-adapt-marlon-lacy-2026
- **Official X account: @thecoreboys**, tagline "Create. Own. Run Everything."
  **REPORTED** (search snippet): https://x.com/thecoreboys
- **CORE YouTube ~1 million subscribers.** **VERIFIED** (fetched win.gg):
  https://win.gg/lacy-announces-he-is-leaving-core/
- Fan shorthand for the group is **"the CORE Boys."** **VERIFIED** (fetched):
  https://coreboys.org/

**So "CORE clippers" means: accounts that clip the CORE members' streams** — not members
of a clipping org called CORE. This matters. The three handles the user named split into
two different kinds of account (see §2), and only one of them is CORE-dedicated.

**Where CORE clips circulate:** X, TikTok, YouTube Shorts, Instagram Reels. Dedicated
CORE clip properties I found named (all **REPORTED**, search snippets):
- X: @coresculture, @coreboysculture, @coreboyscentral, @CoreBoysWorld
- YouTube: @Core_boys_clipss, @Coreboysclip, @createownruneverything0
- Instagram: @officialcoreboys
- Web: https://coreboys.org/ (**VERIFIED** fetched) — runs a "Clip Draft" where "fans vote
  on the best moment of the week" for homepage placement.

---

## 2. OTHER LARGE CORE CLIPPER ACCOUNTS

### The honest headline finding

**The CORE-*dedicated* clip accounts are small. The giant accounts are general
streamer-clip pages that cover CORE as part of a wider beat.** Of the three the user
named, @yoxics and @scubaryan_ are the second kind; @coresculture is the first kind.

Concretely: @coreboysculture — the CORE-dedicated page I could get a number for — is
reported at **2,079 followers**, while @scubaryan_ is reported at **~683K–691K**. Two
orders of magnitude. So "giant CORE clippers" almost certainly means *large general
streamer-clip pages that clip CORE members*, and that is what I hunted.

### Tier A — Giant general streamer-clip pages that demonstrably post CORE content

All follower counts **REPORTED** via search-index profile metadata. Dates of those
snapshots are unknown; treat as approximate.

| Handle | Followers (REPORTED) | Bio (verbatim, REPORTED) | Proof it covers CORE |
|---|---|---|---|
| **@FearedBuck** | **1.1M** | "#1 Trusted Source for Kai Cenat 🗽💫 \| Twitch • YouTube • Media • News • Verified by @KaiCenat \| Est. 2022" | Posted the Streamer University follower-gain leaderboard listing Lacy #2, Marlon #5, JasonTheWeen #6, StableRonaldo #10, Silky #13 — https://x.com/FearedBuck/status/2081587648112529734 ; and a Lacy clip post — https://x.com/FearedBuck/status/1947291864362565881 |
| **@clippedszn** | **240.3K** (joined Sept 2015) | "5.1B+ \| any means possible" | Streamer-clip page in the same reply/quote network; CORE-specific post not individually confirmed — see caveat below |
| **@Kick_Champ** ("KickChamp👑") | **195K** (joined Aug 2023) | "Most Reliable News Source 🥇 │ Not Impersonating Anyone │ Sponsored by @Rainbetcom" | Posted the CORE launch itself: https://x.com/Kick_Champ/status/2049949850737787362 |
| **@Dexerto** | **1.3M** (joined Sept 2009) | "The leading source for influencer, streamer, gaming, and viral content" | Adjacent — a **media company**, not a bounty-style clipper. Include as a benchmark, not a model. |

**Caveat on @clippedszn:** I confirmed the account, size and bio, and that it is a
streamer-clip page ("Back when streaming wasn't all about competition 💔" —
https://x.com/clippedszn/status/2056441122730193081). I did **not** find a CORE-specific
post from it. Do not assume CORE coverage without checking.

**Reference point for the two the user already named** (a separate agent owns these; given
only so the tiering above is calibrated, all **REPORTED**):
- @scubaryan_ — "daily streamer clips and other news," "sponsored by @rainbetcom";
  one snapshot said **683.4K**, another **~690,900**.
- @yoxics — "FBI ASSOCIATE | powered by @roobet · dm 4 promo 🪐," joined June 2016;
  search snapshot **533.4K**, xbeast.io landing page **603K** (**VERIFIED** I fetched
  xbeast and saw "603K followers"; the rest of its analytics was paywalled).
  Beware near-identical impostor handles: **@yoxicz** (2,657) and **@y0xics** (1,883).

### Tier B — Mid-size clip pages in the same network (useful as format templates, not as "giant")

All **REPORTED** via search snippets:

| Handle | Followers | Bio (verbatim) |
|---|---|---|
| @StreamDepot | 25.6K | "Not Impersonating anymore / Daily Streamer Clips" |
| @DornerClipz | 19.5K (joined Nov 2023) | "500m +\| daily streamer clips and entertainment news" + @Roobet |
| @CutnPaid | 17.1K | "Daily Streamer Clips," "Impersonating No One," "Sponsored by @rainbetcom" |
| @TheClipBot ("Nick🏂") | 15.2K (joined Mar 2023) | "#1 Source For Clips/Memes/Reactions Of AMP & Friends" — AMP, not CORE |
| @streamupdates_ | 10.2K (joined Sept 2022) | "Daily streamer clips - Dm for promo - powered by @Roobet" |
| @Clipnewz | 5,374 (joined Nov 2025) | "Not Impersonating Anyone \| Daily Streamer Clips📸 · DM for promo📩" |
| @gottaclipit | 3,348 (joined June 2024) | daily streamer clips, "not impersonating anyone," powered by @rainbetcom |
| @coreboysculture | 2,079 (joined Oct 2025) | "Content & Updates for @TheCoreBoys" |
| @ClipDramaTV | 1,912 (joined Jan 2023) | "Streamer Drama and Esports Updates," daily uploads, Florida USA |
| @StreamerClipss | 222 (joined Sept 2022) | "Not impersonating anyone. Follow for fast and reliable updates, news and clips" |
| @mbbclipped | 62 (joined June 2024) | "streamers \| celebs \| daily clips" |

### Accounts I found but could NOT size
@coresculture (bio **REPORTED**: "All CORE News, Updates & Content for @TheCoreBoys"),
@coreboyscentral ("the number 1 source for daily clips & news relating to @thecoreboys,"
joined March 2026), @CoreBoysWorld, @ReckedClips ("Daily Clips 🔥 🎬 Clipping All
Streamers"), @ClipGD ("Clips, Funny videos, Throwbacks and more"), @clippedbytee
("influencer clips and fights"), @StreamerUdaily ("Streamer University clips… everything
SU by the hour"; one snapshot said 405 followers).

### Direct answer to "aim for 5+"
**Genuinely giant (>150K) AND new (not among the user's three): three —
@FearedBuck (1.1M), @clippedszn (240K), @Kick_Champ (195K)**, plus @Dexerto (1.3M) as an
adjacent media benchmark. **I did not find five more giant accounts.** The rest of the
niche that I could reach is a long tail of 200–25K-follower pages. I am not going to
invent a fourth and fifth to hit the number.

---

## 3. SCENE CONVENTIONS

### 3a. Caption style — the strongest finding in this report

Every one of the following is **verbatim tweet text surfaced by the search index**
(**REPORTED**; I did not load the posts). The pattern across them is unambiguous.

- @yoxics: *"IShowSpeed crashed out on Marlon, Lacy and Jasontheween for breaking his fake
  bed in his streaming room made out of toilet paper 😭"* —
  https://x.com/yoxics/status/2027419134309601459
- @yoxics: *"Lacy showing off infront of his TikTok crush 😳"* —
  https://x.com/yoxics/status/1877024110363967558
- @scubaryan_: *"Lacy tried fitting in with Silky and Max but ended up ruining the whole
  vibe 💀"* — https://x.com/scubaryan_/status/1795897967016083691
- @FearedBuck: *"Lacy tried clip farming BenDaDonnn with his "I love my boyfriend" t-shirt
  then Gotti showed up out of no where 😭 "Sh*t funny till a real one press you.""* —
  https://x.com/FearedBuck/status/1947291864362565881
- @coresculture: *"Lacy was left in tears and ended his stream after saying…"* —
  https://x.com/coresculture/status/2072926796366922190
- @coresculture: *"Another shot of the CORE car collection🔥 [via X @drewwall_]"* —
  https://x.com/coresculture/status/2060498409451147625
- @coreboysculture: *"Who's the worst & best gamer out of these CORE Members🤔 - Marlon -
  JasonTheWeen - Silky - Adapt"* — https://x.com/coreboysculture/status/2054203655650202105
- @coreboysculture: *"The CORE Boys have generated almost 20 Million views between 2 Tiktok
  videos all within 3 days🤯🔥"* — https://x.com/coreboysculture/status/2051385797824172304
- @CoreBoysWorld: *"It's official all members of The CORE Group have been accepted into Kai
  Cenat's Streamer University '26 😭🔥 Students: Lacy, StableRonaldo, Jasontheween, Marlon
  and silky Professor: Adapt"* — https://x.com/CoreBoysWorld/status/2074361584957493751
- @Kick_Champ: *"Lacy, Marlon, Silky, Stable Ronaldo, Adapt, and JasonTheWeen launch their
  own org CORE (Create Own Run Everything) right after FaZe Banks went live announcing his
  next move 👀"* — https://x.com/Kick_Champ/status/2049949850737787362
- @clippedszn: *"Back when streaming wasn't all about competition 💔"* —
  https://x.com/clippedszn/status/2056441122730193081
- @Kick_Champ: *"Life before egos and money took over 💔"* —
  https://x.com/Kick_Champ/status/1961311111979917628
- @LacyUpdatesLIVE: *"Twitter/X will officially delete Lacy's twitter community in the new
  update ❌ Lacy's twitter community was the 2nd biggest streamer community with over
  60,000+ members at one point🔥"* — https://x.com/LacyUpdatesLIVE/status/2047058085601042538

**Extracted rules (my inference from the 13 samples above — inference, not a source claim):**

1. **Third person, past tense, names the streamer(s) in plain text.** "Lacy tried…",
   "IShowSpeed crashed out on…". Not first person, not "watch this."
2. **The caption gives away the payoff.** It is a summary, not a tease. No "wait for it,"
   no "you won't believe." The caption *is* the story; the clip is the proof.
3. **Exactly one trailing emoji as a tone tag.** Observed set: 😭 💀 👀 😳 💔 🔥 ❌ 🤯 🤔.
   😭/💀 = funny-painful. 👀 = drama/tease. 💔 = nostalgia. 🔥 = hype. Emoji goes at the
   end, after the sentence. Multi-emoji only on hype/announcement posts (🤯🔥, 😭🔥).
4. **Length ~8–30 words**, one sentence, occasionally two.
5. **No hashtags observed in any sample. No "link in bio." No CTA.**
6. **Streamers referenced by bare name, not @-handle**, in the clip captions. @-handles
   appear only for sponsors and for source credit.
7. **Source credit convention exists**: `[via X @drewwall_]` when reposting someone else's
   footage.
8. Recurring sentence frames: **"X crashed out on Y for Z"**, **"X tried A but B"**,
   **"X was left [state] after [event]"**, **"Back when / Life before…"** (nostalgia bait).

Note: **"crash out" is the scene's native term** for the rage-blowup moment — the exact
content category this project targets. It appears in captions, in TikTok titles, and in
Twitch clip titles for Lacy. Using it in captions is speaking the dialect.

### 3b. Bio conventions (near-universal across the network)

Assembled from the bios quoted in §2 (**REPORTED**). Four recurring components:

1. **Authority claim**: "#1 Trusted Source for…", "Most Reliable News Source 🥇",
   "the number 1 source for daily clips & news relating to…"
2. **Impersonation disclaimer** — appears on at least six separate accounts, in near-
   identical wording: "Not Impersonating Anyone" / "Impersonating No One" / "Not
   impersonating anyone" / "Not Impersonating anymore." This is a scene-wide norm,
   presumably to survive X impersonation reports.
3. **Gambling sponsor tag**: "Sponsored by @Rainbetcom" (@scubaryan_, @Kick_Champ,
   @CutnPaid, @gottaclipit) or "powered by @Roobet" (@yoxics, @streamupdates_,
   @DornerClipz). This is the scene's dominant monetisation, separate from clip bounties.
4. **Cumulative-views flex**: "5.1B+" (@clippedszn), "500m +" (@DornerClipz).
   Plus "DM for promo" as an inbound-sales line.

### 3c. Clip length / aspect ratio / cadence

**I could not measure these off real posts.** What I have is (a) platform guidance and
(b) journalism about the wider clip-farm economy. Use as hypotheses, not as observed
CORE-scene practice.

From **clipping.net's own X/Twitter clipper guide** (**VERIFIED** — I fetched it):
https://clipping.net/blog/x-twitter-clipper-guide
- Ideal clip length **30–60 seconds**; hard max 2m20s.
- Aspect ratio: **both 16:9 and 9:16 accepted**; the guide says landscape reportedly
  performs better for certain content types on X.
- Caption formula recommended: **hook statement → context → call-to-action**. Their example:
  *"This is the craziest take I've heard all week 👀."* (Note: the real CORE-scene captions
  in §3a use no CTA — the platform's advice and the actual practice diverge.)
- Cadence: minimum 1–2 videos/day, **recommended 3–5/day**, aggressive 10+/day.
- Rates: "Campaign rates range from $10 to $300+ per 100K views."

From **Forbes, "Inside The 'Clipping Farms' Driving Fintech's Marketing Boom"**, 11 Feb 2026
(**VERIFIED** — I fetched it):
https://www.forbes.com/sites/boazsobrado/2026/02/11/inside-the-clipping-farms-driving-fintechs-marketing-boom/
- **"Fifteen-second segments typical"** across TikTok / Reels / Shorts / X.
- Standard pay **$1–$5 per 1,000 views**; low-end campaigns **$0.20 per 1,000**;
  Whop listings **$40–$400 per million views**; Stake network **~$100 per post** flat.
- Stake network scale: **50M impressions daily**; accounts needed **50M+ monthly views**
  to participate. One campaign: **37M impressions for $250**.
- Named: **@FearedBuck** grew **64,000 → 645,000+ followers** after pivoting to
  Stake-watermarked streamer content in **August 2024**. (Search snapshot now says 1.1M.)
- Also named: @BadTwtProfiles (exposed the operation, Dec 2024), Discord admin "harkits."

**Conflict to be aware of:** 15s (Forbes, cross-platform norm) vs 30–60s
(clipping.net, X-specific). Unresolved. The project should measure real CORE-scene posts.

### 3d. Subtitles / burned-in captions

**UNVERIFIED — I found nothing.** No source described subtitle styling, font, position, or
whether these accounts burn in captions at all. I am not going to guess. This is a gap the
user must fill by looking at actual posts.

### 3e. Watermarking

From KnowYourMeme, "Stake Ads on Twitter / X" (**VERIFIED** — I fetched it):
https://knowyourmeme.com/memes/stake-ads-on-twitter-x
- The watermark convention on sponsored clip pages **"evolved from simple logos to banners
  reading 'GAMBLE RESPONSIBLY | #AD.'"**
- Named accounts in that ecosystem: **@FearedBuck** (one post: **11.7 million views,
  61,000 likes** — the single hardest engagement number in this entire report),
  **@scubaryan_**, **@CFC_Janty** (21,000+ likes, 24 Aug 2024), **@picsthatgohard_**,
  **@lmfaooooos**, **@fuckstake_**.

**Direct relevance:** START_HERE.md line 63 specifies "zero watermarks or logos" for this
project's clips. That is *opposite* to the dominant convention among the giant accounts —
but their watermarks are paid gambling ads, not branding. The project's no-watermark rule
is consistent with a bounty clipper (who is not selling ad space) and I see no evidence it
hurts. Flagging the tension, not recommending a change.

---

## 4. WHAT PERFORMS

**This is the weak section and I will not pad it.** X-side engagement data was almost
entirely unreachable. Here is everything real I have.

**The one hard X engagement figure I found:**
- @FearedBuck, one Stake-watermarked clip post: **11.7 million views, 61,000 likes**
  (**VERIFIED** via KnowYourMeme, fetched). ≈0.52% like-to-view. No date given for the post.
- @CFC_Janty: **21,000+ likes**, 24 Aug 2024 (**VERIFIED**, same source). Football, not
  streamer content.

**Lacy's own top Twitch clips** (native Twitch clip views — *not* X views; useful as a
signal of which *moments* the audience clips, not of X performance).
**VERIFIED** — I fetched https://www.twitchmetrics.net/c/494543675-lacy/clips :

| # | Title (verbatim) | Views | Category |
|---|---|---|---|
| 1 | "wild" | 320,648 | Fortnite |
| 2 | "CLEAN THIS" | 166,212 | Streamer University |
| 3 | "WOAH JSHOCK???" | 145,138 | Just Chatting |
| 4 | "Lacy texting and driving without seatbelt..." | 143,989 | Just Chatting |
| 5 | "cpr" | 126,003 | Just Chatting |
| 6 | "LMFAO" | 111,849 | Fortnite |
| 7 | "o7 L BMW" | 105,563 | Just Chatting |
| 8 | "😭😭" | 94,635 | Fortnite |
| 9 | "sus" | 91,775 | Just Chatting |
| 10 | "LMAO" | 89,381 | Just Chatting |

*(The page also carried trailing date/time strings — e.g. "Fri, Mar 29 at 19:07" — which I
read as timestamps, not durations. Do not treat them as clip lengths.)*

**Observations from that table (mine, low-to-medium confidence):**
- **7 of 10 are Just Chatting or IRL-adjacent**, not gameplay. Reaction/drama beats
  gameplay in Lacy's clip economy.
- **Twitch-native clip titles are 1–3 words**, often all-caps or bare lowercase, sometimes
  emoji-only. This is the *opposite* of the X caption style in §3a (full explanatory
  sentence). Two different surfaces, two different conventions — don't reuse one for
  the other.
- Category "Streamer University" appearing at #2 shows **event/collab content spikes**.

**Softer signals (REPORTED / inference):**
- Lacy ranked **#2 of the ~50 Streamer University attendees by followers gained
  (+445,100)**; Marlon +310,700 (#5), JasonTheWeen +309,900 (#6), StableRonaldo +287,400
  (#10), Silky +171,400 (#13). Source: @FearedBuck post text surfaced in search —
  https://x.com/FearedBuck/status/2081587648112529734 . **Reads as: CORE members are
  top-tier clip subjects, and Lacy is the strongest of them.**
- **Cross-CORE collision moments perform**: the two most-shared caption examples I found
  both involve multiple named creators colliding (IShowSpeed vs Marlon/Lacy/JasonTheWeen;
  Lacy vs BenDaDonnn/Gotti). Multi-name captions appear over-represented.
- **Nostalgia framing** is a distinct recurring format with its own emoji (💔):
  "Back when streaming wasn't all about competition 💔" / "Life before egos and money took
  over 💔". Cheap to produce from archive footage.
- CORE TikTok reference point: **"almost 20 Million views between 2 Tiktok videos all
  within 3 days"** (@coreboysculture, **REPORTED**).

**Two scene practices that are reported as effective but are dishonest** — flagging so the
project makes a deliberate choice, not recommending them:
- **Recycling old clips as new during a drama cycle.** xQc, publicly, at @yoxics: *"Lacy in
  hot water = post multiple unrelated, out of chronology lacy clips"* —
  https://x.com/xQc/status/1958571062922285105 (**REPORTED**).
- **False/narrative-stirring captions.** JasonTheWeen, quoted by Complex (**VERIFIED**,
  fetched): *"Clip pages nowadays, especially on Twitter [and] TikTok, they're paid by
  Stake or Dollar Tree. They put false captions and stir this narrative…"* —
  https://www.complex.com/life/a/tracewilliamcowen/jasontheween-x-platform-clip-pages-problem
  The same article notes he threatened legal action over a false-caption post.
  **A bot that auto-writes punchy captions can land here by accident. Worth a guardrail.**

**What I do NOT have and will not fake:** per-post view counts for @yoxics / @scubaryan_ /
@coresculture; any distribution of views across a clipper's posts; any measured
clip-length-vs-performance relationship; any A/B evidence on caption style; the minimum
view threshold Clipping.net applies to the Lacy campaign.

---

## 5. DOES LACY OVERLAP WITH CORE?

**Yes — Lacy is a founding member of CORE. Maximum possible overlap.** This is the single
most important finding for the project: CORE clippers are not an adjacent reference class,
they are *literally the people clipping this project's target streamer.*

- **Founding member of CORE**, one of the original six. **VERIFIED** (Tubefilter, fetched).
- Real name **Nick Fosco**, born 18 Feb 2003. **REPORTED** (search snippet, streamerage.com).
- Twitch: **twitch.tv/lacy**. **~2.3M Twitch followers**; **all-time peak 120,782 concurrent
  viewers on 17 July 2026**; **241h 5m streamed in the last 30 days**; **ranked #15 on
  Twitch in 2026**. **REPORTED** (search snippets citing streamscharts.com — the site
  itself returned 403 to me).
- Known for Fortnite, IRL/Just Chatting, and **"viral feuds."** **REPORTED**.

**Complication — Lacy's current CORE membership is genuinely ambiguous as of this date:**
- win.gg (published 29/07/2026, **VERIFIED** — I fetched it): Lacy posted on X that he was
  leaving CORE, gave no reason; and *"had previously announced departing CORE in June 2026
  but remained on the roster, leading fans to believe this latest announcement may also be
  a troll."* — https://win.gg/lacy-announces-he-is-leaving-core/
- A search-engine summary asserted flatly that he left in June 2026 and is no longer part
  of CORE as of August 2026 (**REPORTED**, no primary source shown — I distrust this).
- **coreboys.org/members still lists Lacy on the official roster** (**VERIFIED** — I
  fetched https://coreboys.org/ ; the roster lists Stable Ronaldo, JasonTheWeen, Lacy,
  Silky, Marlon, Adapt).

**Practical read:** whether or not he is formally in CORE this week, he is inside the CORE
content universe — he lives the same content, collides with the same people, and is clipped
by the same accounts. The CORE clipper findings transfer to him **directly**. The only
thing the membership question affects is whether "CORE" is a useful caption keyword for
his clips right now — and that is worth the user checking before hardcoding it.

**Also relevant: Lacy has personally paid for clips before.** A Sportskeeda headline
(**REPORTED**, article fetch returned 405 so I have the headline only): *"FaZe Lacy
announces $20,000 prize for livestream clip creators, most watched clip to win $5000
extra."* —
https://www.sportskeeda.com/us/streamers/news-faze-lacy-announces-20-000-prize-livestream-clip-creators-watched-clip-win-5000-extra
Date and current status unknown. **Worth the user chasing down** — a most-watched-clip
prize on top of per-view pay changes clip-selection strategy materially.

---

## 6. 🚩 CRITICAL FLAG — @LacyCrashOuts could not be found

`START_HERE.md` line 25 identifies the target streamer as **"Lacy (@LacyCrashOuts …)"**.

**I searched for that handle twice, with two different query formulations, and found zero
evidence it exists.** No X profile, no mention, no reference on any platform. What the
searches returned instead was TikTok/YouTube "Lacy crash out" *content* (the phrase is
scene slang for his rage moments) and his real accounts.

**Handles I did find associated with Lacy** (all **REPORTED**, search snippets):
- **@LacyHimself** — his main X account (listed as "FaZe Lacy," https://x.com/LacyHimself ;
  seen posting: *"man i was in a nerd outfit saying random shit nerds would say…"* —
  https://x.com/LacyHimself/status/2062000426682388945 )
- **@LacyUpdatesLIVE** — "Lacy Updates," an updates/fan account for @LacyHimself
- **@USECODELACY** — "LACY UPDATES"
- **twitch.tv/lacy** — the stream itself

**This is exactly the failure mode the project has been burned by before.** Either
@LacyCrashOuts is a real but unindexed/small account the user knows of, or it is an
assumption that got written into START_HERE.md and has been propagating since.
**The user must confirm it before anything is built against it.** If the bot is meant to
post to a handle, or to monitor one, the wrong handle breaks everything downstream
silently.

---

## 7. WHAT THE USER NEEDS TO SUPPLY (things no amount of searching will get)

1. **Confirm or correct @LacyCrashOuts.** See §6. Highest priority.
2. **Logged-in X access, or manual screenshots/exports.** Everything in §3c–3d and §4 that
   is missing — real clip durations, aspect ratios, subtitle styling, per-post view counts,
   posting cadence — requires seeing actual posts. 10–20 saved posts from @yoxics,
   @scubaryan_, @coresculture and @FearedBuck would convert most of this report's
   inferences into measurements.
3. **The actual Clipping.net Lacy campaign terms** — the minimum view threshold, the rate,
   allowed platforms, whether a most-watched bounty exists. Published rate *ranges* are in
   §3c but the campaign's own numbers were not findable publicly.
4. **Whether Lacy is currently in CORE** (§5) — affects caption keywords.
5. **A decision on the caption-honesty guardrail** (§4) — the scene's two highest-leverage
   tactics are recycling old clips and writing narrative-stirring captions, both of which
   drew public callouts from xQc and JasonTheWeen and a legal threat.

---

## 8. FULL SOURCE LIST

**Fetched and read in full (VERIFIED access):**
- https://www.tubefilter.com/2026/05/01/new-faze-clan-creator-group-house-core/
- https://www.complex.com/life/a/tracewilliamcowen/jasontheween-x-platform-clip-pages-problem
- https://www.forbes.com/sites/boazsobrado/2026/02/11/inside-the-clipping-farms-driving-fintechs-marketing-boom/
- https://knowyourmeme.com/memes/stake-ads-on-twitter-x
- https://win.gg/lacy-announces-he-is-leaving-core/
- https://coreboys.org/
- https://clipping.net/blog/x-twitter-clipper-guide
- https://www.twitchmetrics.net/c/494543675-lacy/clips
- https://www.complex.com/pop-culture/a/khal/streamer-university-2026-best-moments
- https://xbeast.io/twitter-influencers/yoxics (paywalled beyond follower count)

**Search-index snippets only (REPORTED) — X profiles and posts:**
- https://x.com/thecoreboys · https://x.com/coresculture · https://x.com/coreboysculture ·
  https://x.com/coreboyscentral · https://x.com/CoreBoysWorld
- https://x.com/FearedBuck · https://x.com/clippedszn · https://x.com/Kick_Champ ·
  https://x.com/Dexerto · https://x.com/scubaryan_ · https://x.com/yoxics
- https://x.com/StreamDepot · https://x.com/DornerClipz · https://x.com/CutnPaid ·
  https://x.com/TheClipBot · https://x.com/streamupdates_ · https://x.com/Clipnewz ·
  https://x.com/gottaclipit · https://x.com/ClipDramaTV · https://x.com/StreamerClipss ·
  https://x.com/mbbclipped · https://x.com/reckedclips · https://x.com/ClipGD ·
  https://x.com/clippedbytee · https://x.com/StreamerUdaily
- https://x.com/LacyHimself · https://x.com/LacyUpdatesLIVE · https://x.com/usecodelacy
- Individual posts quoted verbatim in §3a and §4, each with its status URL inline.

**Secondary articles (REPORTED, snippet or partial):**
- https://www.complex.com/pop-culture/a/jaelaniturnerwilliams/faze-marlon-adapt-new-streaming-group-core
- https://streamer.guide/blog/core-streaming-group-adapt-marlon-lacy-2026
- https://www.sportskeeda.com/us/streamers/news-faze-lacy-announces-20-000-prize-livestream-clip-creators-watched-clip-win-5000-extra (405 on fetch — headline only)
- https://www.clipaffiliates.com/blog/clipping-net-review
- https://awfulannouncing.com/twitter/x-users-fighting-stake-sponsored-posts.html
- https://www.404media.co/what-is-stake-gambling-casino-watermark/
- https://streamscharts.com/channels/lacy (403 on fetch — snippet only)
- https://streamerage.com/lacy/

**Blocked, no data obtained:** x.com/twitter.com direct, publish.x.com/oembed,
xcancel.com, r.jina.ai, sotwe.com, streamscharts.com, youtube.com channel pages,
tiktok.com, instagram.com.

---

*End of verbatim agent report. Nothing above is project-approved. All follower counts are
second-hand from search-index metadata of unknown date. No handle in this report was
invented; every one appeared in a search result with a resolvable URL.*
