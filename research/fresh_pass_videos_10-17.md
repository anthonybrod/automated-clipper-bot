# Fresh pass — 8 assigned videos (Twitch/streamer clipping automation research)

**What this is:** a from-scratch, careful re-study of 8 specific YouTube videos
the user flagged as helpful for the "automated clipper bot" project, done a
second time because the first pass's write-up was lost to a context-compaction
event. This pass reads the **actual, real, full spoken transcript** of every
one of the 8 videos (fetched via `youtube_transcript_api` into
`research/transcripts/*.txt` by a parallel process, then read in full here —
not paraphrased from titles/descriptions), plus live-browser-verified full
video descriptions for several of them. This is a materially stronger source
than the prior recovery pass documented in `RESEARCH_YOUTUBE_SOURCES.md`,
which explicitly states its own limitation: *"none of the raw dumps... contain
the actual spoken transcript of any of the 17 videos — only titles,
chapter/timestamp lists, and descriptions."* This pass closes that gap for
these 8.

**Confidence convention:** **[verified]** = actually read the real
transcript/description text myself. **[search]** = relying on metadata/title
without substantive real content read. Every fact below is [verified] via
full transcript unless explicitly marked otherwise.

**A note on research-tooling reliability (transparency, not a content
finding):** live browser navigation to YouTube in this session was unstable —
repeated, fast, unexplained autoplay-driven navigation away from the
requested video toward other (thematically related) videos in the same
recommendation cluster, even after pausing/muting the player. Full,
reliable spoken-transcript text was ultimately obtained for all 8 videos via
the pre-fetched transcript files rather than the live "Show transcript" UI
button (consistent with the prior session's own note that ref-based clicking
of that button is unreliable). Live-browser `ytInitialPlayerResponse` reads
did succeed for full video descriptions on 3 of the 8 videos before drift
made further live reads unreliable; those 3 are marked accordingly below.

---

## 1. "1-day-a-week VIDEO CLIPPING SYSTEM that GENERATES LEADS"

**Channel:** COMMAND · **URL:** https://www.youtube.com/watch?v=JhOhaDvOfFk

**[verified — full transcript read, 615 caption snippets].** This video
already received the deepest treatment of all 17 videos in the prior recovery
pass (`RESEARCH_YOUTUBE_SOURCES.md`, section 2 "Video 1"), because that pass
read the video's linked **public GitHub repo end-to-end**
(`github.com/COMMAND-LABS/step-by-step-video-clipping-demo`) — full script
contents, exact commands, exact config values. That repo-level detail is not
duplicated here; see that document for: the exact faster-whisper config
(`large-v2`, `device="cpu"`, `compute_type="int8"`, `beam_size=5`,
`vad_filter=True`), the exact ffmpeg extraction command (`-crf 20`,
`PADDING_SEC = 20.0`), the full No-Code Architects Toolkit REST endpoint list,
the exact `claude` CLI subprocess invocation used for moment identification,
the Airtable MCP server (`github.com/domdomegg/airtable-mcp-server`), and
Metricool's exact "Advanced" plan price ($53/month). What follows here is new
texture from actually reading the spoken transcript, which the prior pass did
not have.

**The creator's own framing and numbers (spoken on camera):**
- Opens with a real inbound-lead screenshot and the actual Zoom call that
  produced it, then states: *"The system... turned that Zoom call into 10
  vertical video clips posted across five social media platforms."*
- Track record stated directly: **6 months, solo, no team, no editors, no
  paid ads**, while simultaneously servicing **4 clients** and delivering "AI
  upskilling programs" in the Miami area. Output in that window: **67 videos
  produced, 402 posts published**.
- Requirements stated as exactly **"four things": a laptop, some free
  open-source software, two paid softwares (i.e. Claude and Metricool), and
  whatever video editing software you like** for manual touch-ups. All-in
  cost (excluding the laptop): **about $100/month**, with "almost zero
  marginal cost as you produce clips at scale."
- Skill recommendation: experience with or interest in **Python, Claude, and
  Docker** "will help a lot," though he states anyone can follow the video
  regardless of experience level.

**The 7 steps, as walked through live on screen (transcript detail beyond
what the repo alone shows):**
1. **Transcript.** If your recording tool already gives you a transcript,
   skip this step. Otherwise, faster-whisper. He explicitly times it on
   camera: a **9-minute-12-second** input video took **"just under 10
   minutes"** to transcribe on his machine — i.e., roughly **1 minute of
   processing per 1 minute of video**. His stated rationale for going local
   instead of SaaS: (a) you avoid uploading large video files over the
   internet, which for real 1-4+ hour recordings "can take hours, if not
   days, depending on internet conditions," and (b) SaaS transcription tools
   typically charge **per minute of input video**, whereas local processing
   has no marginal cost regardless of volume.
2. **Moment identification via Claude Code**, triggered by a script that
   feeds the transcript plus a prompt file to Claude Code. He reads part of
   the actual prompt on screen: *"You are a viral social media content
   strategist specializing in short-form video. Analyze the transcript
   excerpt and identify its two most viral-worthy moments..."* — output
   includes start/end timestamps, a title, a hook, and a "why it's viral"
   justification. **Live demo of prompt-parameter tuning**: he edits the
   script to ask for **3 clips instead of 2**, re-runs it, and confirms 3
   clips come back — a small but concrete illustration that the clip *count*
   is just a prompt parameter, not hardcoded.
3. **Cutting via ffmpeg**, looping over the `moments.json` file. He
   explicitly justifies **why not just use CapCut, Descript, or Opus
   Clip**: *"the benefits of this system is it runs almost entirely locally
   and it's open source... as you produce clips at scale, the costs...stay
   fixed. Whereas these other SaaS tools will start charging you more money
   as you feed more minutes into their systems... or as you generate more
   clips."*
4. **Manual review/rough-edit pass.** He opens the generated clips in Finder
   and edits one live in **Camtasia** (explicitly says CapCut/Descript/etc.
   work fine too) — trims to exact start/end frames, adds logos on either
   side. Explicitly frames this as optional/to-taste and invites viewer
   feedback on the edit in the comments.
5. **Captions via the NCA Toolkit API** (Stephen G. Pope's open-source,
   Docker-based project). Concrete detail not in the repo-focused writeup:
   after captioning, he **spots a real typo** ("AI engineer" rendered with a
   lowercase "e"), manually edits the generated `.ass` caption file, and
   instead of re-running the full caption-generation script, runs a separate
   **"burn" script** that only re-burns the (now-corrected) existing caption
   file onto the video — i.e., the pipeline has a fast, cheap "fix a typo and
   re-render" path distinct from "regenerate captions from scratch." He also
   notes that for **more complex caption-file edits or custom caption
   templates/styling**, you can hand the task to Claude Code directly rather
   than editing the `.ass` file by hand.
6. **Marketing-copy generation.** Switches specifically to **Claude Desktop**
   (not Claude Code) "for visual purposes." Sets up an **MCP connection
   between Claude and Airtable** (free tier is sufficient — he's on it
   himself). Clip must be reachable via a public URL first — he uses
   **Google Cloud Storage** for that. The Airtable base has 3 tables (his
   repo includes a **one-click install** to provision them): a prompts
   table, a content table, and a distribution-prompts table. He reads the
   actual prompt structure used: references the clip's cloud-storage URL,
   the original recording date, today's date, a CTA driving traffic to
   **parsty.io** (his own AI-engineering bootcamp, tied to the specific Zoom
   call being clipped), contextual info about the clip, the clip's own
   transcript, general requirements, additional context, an explicit output
   JSON schema, and target SEO keywords. **Explicit tip, repeated twice
   verbatim across steps 6 and 7**: *"make sure we have a fresh session to
   avoid context rot"* before firing off each Claude prompt.
7. **Distribution via Metricool**, again via an MCP connection from Claude.
   A third Airtable table holds several pre-written **distribution prompts**
   for reference; for the demo he only needs to change the target
   publish-time field (schedules for 10:00 a.m. while it's "7:30 a.m. ish" at
   recording time). Confirms the result by reloading Metricool's actual
   content calendar and pointing at the newly scheduled post.

**Explicit self-assessment of automation level:** *"I think in reality, what
you want is semi-automated, right? You could automate this further. There's a
clear path to do that, but..."* — he deliberately keeps human review gates
rather than building a fully closed-loop system. Personal cadence: **"I spend
one day a week filling my content calendar, and this system pushes content
out for me in the background... for the other 6 days of the week."** More
input recordings = further ahead on the content calendar, linearly.

**Analytics-feedback / self-adjustment hunt result:** **None found.** No
mention anywhere in the transcript of checking post-publish view counts,
retention, CTR, or engagement and using that data to change future clip
selection, captions, pacing, or posting strategy. The system is
production+distribution automation with human review gates, not a
performance-driven feedback loop. No A/B testing of titles/thumbnails/hooks
mentioned.

---

## 2. "This AI Machine automatically clips & posts 100+ Shorts from 1 Video"

**Channel:** Jay E / RoboNuggets · **URL:** https://www.youtube.com/watch?v=LiWf_BGg87o

**[verified — full transcript read, 1092 caption snippets].** This is the
single most technically detailed video of the 8 — a full node-by-node n8n
workflow build, narrated the entire way through.

**Economic framing given up front (concrete, named numbers):**
- A content-business example, described as paying clippers **"$140,000 for a
  month"** — attributed to a business/creator referred to as **"Neon"** in
  the transcript (auto-caption; treat the exact name as approximate).
- Cites an article (auto-captioned as **"by roster"** — likely a garbled
  transcription of a real outlet name, treat as approximate) framing clipping
  as *"an entry-level editor job that can fetch roughly a rate of $15 per
  1-minute video,"* stated to align with **Upwork** rate data.
- Cites **Google Trends** twice: once for the general rise in "AI automation"
  as a skill, once specifically for **n8n**, described as having "shot up in
  demand quite recently."

**Tool named for orchestration: n8n**, explicitly compared to **Zapier** and
a third tool the auto-captions render as "Mink.com" (near-certainly **Make**,
i.e. Make.com — a plausible ASR mis-transcription). Free trial available via
a link in the description.

**The 4-step framework, and the exact n8n build for each step:**

*Step 1 — Input.* Trigger node = **Schedule** (demoed at "once per day").
Second node = Google Sheets **"Get Row in Sheet"** action, renamed "get long
form." Reads from a shared **Google Sheets template** (copy-able from the
RoboNuggets community) with (at minimum) columns for the long-form video
link and a production-status flag. Filter condition: production status
equals **"for production"**; toggles **"return only first matching row"**
on, so each scheduled run processes exactly one queued video.

*Step 2 — Analyze via AI tool named **Klap*** (rendered "Clap"/"ClapF" in the
auto-captions throughout — this is unambiguously the real product **Klap**,
a long-form-to-shorts AI clipping SaaS with a public API). Node = **HTTP
Request**, method POST, renamed "analyze long form." Auth setup: generic
credential type, **Header Auth**, header name typed exactly
**`Authorization`** (capitalization and no trailing whitespace called out as
mandatory), value = a Klap API key generated from Klap's dashboard (requires
a credit card on file, but billing is **usage-based, not a forced monthly
subscription**). Body (JSON) fields dragged in from Klap's own docs, with the
**source video URL** mapped dynamically from the Sheet row (shown in n8n's
UI in green to indicate a dynamic/expression value). Other body params
enabled: **captions = true**, **reframe = true** (crops/frames the video
around wherever the speaker's face is), emoji settings, silence/pause
removal, and **intro title = true**.
- **Pricing given on-screen from Klap's docs:** roughly **$1 USD per clip**
  generally, working out to about **$0.85 per clip** specifically when
  generating 10 clips from one long-form video.
- Workflow-building tip demonstrated live: set the **Wait** node to **1
  second** while testing (scale to **5 minutes** for production), and
  **"pin"** test-run data on nodes (right-click → Pin, or keyboard shortcut
  **`P`**) so repeated test-step clicks don't re-trigger paid API calls.
- **Polling/retry pattern, shown explicitly**: a "get status" HTTP GET node
  checks Klap's job status; an **IF node** checks `status == "ready"`; the
  **false branch loops back to the Wait node** to poll again, and the **true
  branch proceeds** to a "get shorts details" node that pulls per-clip
  title, platform-specific auto-generated captions, and short IDs.

*Step 3 — Produce/export.* A duplicated HTTP POST node ("export shorts") to
a different Klap endpoint, requiring a **`presetId`** field that Klap's docs
mark required but which — at the time of recording — **"they're still
building this out... you can literally type whatever here and it will still
work"** (he types `123` as a placeholder), noting Klap's future plan is to
let this ID select caption-font templates. A "get shorts" GET node (no body
needed) retrieves final rendered clip URLs once status is "ready" — previewed
directly by pasting the URL into a browser tab. A Google Sheets **"Update
Row"** node flips the original long-form row's status from "for production"
to **"done,"** matched using a **`first()`** expression to resolve
ambiguous multi-item references (since one long-form video now maps to
multiple generated-clip items), and logs a "date produced" column via a
dynamic today's-date expression. A second, separate Google Sheets node
("log shorts") **appends** new rows — one per generated short — into a
*second* sheet, capturing the clip URL, per-platform captions, a
publishing-status column ("for publishing" → "done"), and an ID column
computed with the literal **Excel-style formula `=ROW()-1`**.

*Step 4 — Auto-publish, via **Blotato*** (rendered "Blot"/"Plotato" in
auto-captions — this is the real cross-posting tool **Blotato**), described
on-camera as *"an AI content engine"* that both manages content and
auto-publishes to social channels. Explicit reasoning given for why a
third-party poster is necessary rather than posting directly: *"the way
these social channels work is... they only want an accredited third party to
be auto posting to them"* — and Blotato is called out as **"one of the
cheapest options."** Separate POST nodes per platform (TikTok, Instagram,
YouTube, LinkedIn shown), each passing Blotato's API key, a `text` field
mapped from Klap's auto-generated caption, and a `mediaUrl` field mapped
from the clip URL. A **"batching" option** is enabled — batch size 1, delay
**60,000 ms (60 seconds)** — so multiple queued videos post one-by-one at a
1-minute cadence rather than all firing simultaneously. A final Google
Sheets node marks each published short's status "for publishing" → "done,"
matched on the short-form-link column.

**Production-scaling tip given explicitly at the end:** split this into
**two separate n8n workflows** — one on a daily schedule that only produces
shorts, and a second, independently scheduled workflow (example given:
**every 3 hours**) that only handles publishing already-produced clips —
decoupling production cadence from posting cadence.

**Monetization — 3 methods given explicitly, plus a partial 4th:**
1. Build/sell the automation to a content-creator client directly (this is
   literally why RoboNuggets built it — a paying client requested it); tip
   given: most YouTube channels list a contact email on their channel "About"
   page.
2. If you already run a clipping business charging **~$15/clip**, use this
   system on the back end to auto-generate the clips and widen your margin.
3. **Whop** (rendered "WP"/"WO" in the transcript — this is the real
   marketplace **Whop**) — creators post clipping bounty jobs; you get paid
   based on the views your submitted clips generate; also names it as a
   platform where AI tools/software (examples given: **Bolt, Fireflies,
   Lovable**) recruit users, not just where creators find clippers.
4. Affiliate programs — general point, illustrated with Skool-community
   affiliate commissions; RoboNuggets' own community affiliate rate is stated
   as **50% for life**.

**Recurring-cost breakdown given on-screen:** Klap ≈ $0.85/clip at 10
clips/video (variable, usage-based); **N8N** $24/month starter plan after
free trial; **Blotato** $29/month after free trial (community discount
code available).

**Analytics-feedback / self-adjustment hunt result:** **None found.** The
entire pipeline is production → publish; nothing reads back real
post-publish performance data to adjust anything. No A/B testing mentioned.

---

## 3. "Automate Streamer Clipping with Claude Code + Submagic"

**Channel:** Damian Malliaros · **URL:** https://www.youtube.com/watch?v=lge0jth5sl0

**[verified — full transcript read, 537 caption snippets].**

**Economic framing (concrete numbers stated on camera):** streamers pay
clippers "thousands of dollars per month"; some streamers are described as
**"publicly saying that they constantly pay over $1 million to clippers
every single month."** Typical clipper payout: **$1 to $3 per 1,000 views**
generated. Worked example given directly: a clip that reaches **500,000
views** on a platform like TikTok — called "not an unreasonable amount" —
could net the clipper **$500 to $1,500** from that single clip. Stated
problem this video is solving: manual clipping "can take you up to 1 hour and
sometimes even more" per output video, which caps how many clips (and
therefore how many viral-lottery-tickets) you can produce.

**Core tool: Submagic (submagic.co).**
- Manual workflow demoed first: paste a YouTube URL (upload-from-computer and
  Google Drive import are also supported) into Submagic's **"Magic Clips"**
  function → set **clip duration** (Auto, or fixed presets **<30s / 30-60s /
  60-90s**) → choose a **caption theme**, explicitly built from **real named
  creator caption styles** — the transcript names **"Hormozi" (i.e., Alex
  Hormozi), "Daniel," and "Kendrick"** among the preset options, with the
  creator explaining the value proposition directly: *"people are already
  familiar with those captions and when they see our video, they are going
  to be more likely to stick and watch it."* He picks **"Hormozi 2."** →
  **Tracking** toggle left on, so the crop/camera follows moving faces. →
  Generate.
- Output includes a per-clip **"virality score"** — demo clip scores **98**
  — computed, per the transcript, from **"these four metrics"** (the video
  does not name all four individually on screen, only that there are four).
- **Submagic MCP server** (described as newly launched at time of
  recording) is the automation bridge: exposes Submagic's functions to any
  AI agent. Setup steps shown: download the **Claude Desktop app**
  (claude.com/download) → open its code/connector settings → prompt Claude
  in plain language to connect via the Submagic MCP, citing
  **docs.submagic.co (MCP server docs)** as the reference link pasted in for
  Claude's context → generate a **Submagic API key** (Account → API section
  in the Submagic dashboard) → paste the key into Claude → restart the app →
  Claude confirms: **"connected and authenticated, 15 Submagic tools
  available."**
- **Natural-language workflow spec given to Claude Code** (paraphrased from
  the actual prompt read on camera): accept either a **YouTube URL or a
  Google Drive URL** as input (explicitly because "not all streamers stream
  on YouTube... some stream on Twitch, some stream on Kick" but "these
  streamers almost always actually give you the full stream in a Google
  Drive link"); leave clip length on **Auto**; use the **Hormozi 2** caption
  style; enable Submagic's **"Magic b-rolls"** feature (auto-inserted
  relevant b-roll + auto "magic zooms"). Claude Code turns this into a
  standing, reusable automation, auto-triggered by natural-language phrases
  like **"clip the stream"** or **"make shorts from this URL."**
- **Live re-test performed on camera:** pastes a *different*, real ~4-hour
  stream URL, tells Claude "turn this into clips" — confirms in both Claude
  Code's own output and directly inside the Submagic web dashboard that the
  job was correctly submitted and is "processing."
- **Idea floated but not built in the video:** an automatic scraper watching
  either the streamer's YouTube channel or a shared Google Drive folder for
  new content, which would trigger the clipping workflow with **zero**
  manual step.

**Scheduling/distribution layer: Submagic's own native Calendar tool.**
Connects TikTok/Instagram/YouTube via an OAuth-style "allow access" flow;
creator explicitly reassures viewers: *"Submagic will only post things when
you actually specifically tell it to."* Automated on top via a further
Claude Code prompt: after each clip-generation run, **find the 20 best
clips by Submagic's own score and auto-schedule them for that day.**

**Explicit, concrete posting-ramp schedule given (a real behavioral-adjustment
rule, driven by platform response, though pre-programmed rather than
live-adaptive) — worth flagging as the closest thing to
"self-adjustment" content found across all 8 videos:**
- **Week 1:** 2-3 posts/day per platform.
- **Week 2:** 10 posts/day.
- **Weeks 3-4 onward:** ~20 posts/day (steady-state).
- Explicit stated reason: *"if you immediately start posting 20 per day, you
  will see that your account is going to get flagged, and you're going to
  get zero views on those posts."* This full ramp schedule (including the
  exact per-week numbers above) is itself given to Claude Code as a plain-
  language instruction, and Claude Code implements it as a rule inside the
  automation. **This is NOT a true analytics-feedback loop** — it does not
  read the creator's own actual post performance and adapt; it's a
  fixed, pre-set ramp applied uniformly to any new account. But it is the
  one clear instance across all 8 videos of "adjust future publishing
  behavior based on a real platform-response risk (getting flagged)."
- **Live re-test performed on camera:** told Claude Code "publish the one
  with the highest score" — confirmed the correct clip posted to both TikTok
  and Instagram, with captions/titles pulled directly from Submagic's own
  auto-generated metadata (not separately re-written).

**Finding streamers who pay for clips — two channels named:**
1. **Whop** (captioned "Whoop") — described as where "multiple popular
   streamers and YouTubers go set up clipping campaigns," paying per 1,000
   views; some campaigns are **open** (joinable without an application),
   which is given as his personal recommendation for where to start.
2. Organic discovery directly on **Twitch or Kick**: stream moderators
   "constantly spamming and advertising their clipping communities" in chat,
   typically within "the first 5 minutes of watching the stream," with a
   join/apply link.

**Analytics-feedback / self-adjustment hunt result:** the posting-ramp
schedule above is the closest match found in any of the 8 videos, but it is
not a real feedback loop against measured per-post analytics — see caveat
above. No mention of checking actual view/retention/CTR data per clip and
adjusting clip *selection or style* (as opposed to posting *cadence*). No
A/B testing of titles/thumbnails/hooks mentioned.

---

## 4. "The BEST AI Clipping Tool in 2026: Riverside vs Opus Clip vs Submagic"

**Channel:** Julian Eisenkirchner · **URL:** https://www.youtube.com/watch?v=pa5LVtcbgD0

**[verified — full transcript read, 392 caption snippets].** Riverside is a
paid sponsor of this video (disclosed on camera), but the creator states he
was a paying Riverside customer before that relationship began, and gives
Opus Clip a genuinely negative review despite the sponsorship — worth noting
as a real, non-uniformly-positive comparison rather than an undifferentiated
ad.

**Riverside — positioned as an all-in-one record+edit+publish tool, not
just a clipper:**
- **Recording:** supports iPhone, generic smartphone, or a professional
  camera (demoed connected via a cam-link device). Selling point stated
  directly: *"you always get the best quality... it's always uploading full
  quality video"* regardless of local connection strength (i.e., local
  progressive recording/upload rather than a live, connection-quality-capped
  stream). Auto-transcribes in the background while recording.
- **"Co-creator"** — an in-editor AI chat panel driven by plain-language
  commands, demoed live: *"create a thumbnail for me"* → Riverside grabs and
  ranks candidate screen-grab frames from the footage and produces
  downloadable thumbnail options; *"add subtitles to this video"* → prompts
  a style choice (**basic / professional / playful** — he picks
  professional) and applies automatically; further chat commands shown:
  *"improve the sound quality"* / *"add background music."*
- **Auto-generated content package** per uploaded video, all directly
  copy-pasteable: **keywords, a summary, key takeaways, suggested titles,
  "sound bites," and chapters.**
- **"Magic Clips"** — auto-ranks candidate short clips with an explicit
  on-screen **"viral score"** (his own term, matches what's shown in the UI);
  demoed scores in the 90s trending down for lesser candidates. Per-clip
  actions: like/dislike, share directly, or open for further editing. Auto
  vertical-reframes to 9:16 and correctly tracks/frames the speaker
  (including alongside inset screen-share content in his demo).
- **"Magic Segments"** — sibling feature to Magic Clips, but extracts
  still-16:9 "worth sharing on its own" segments (e.g., for long-podcast
  guest answers) rather than vertical shorts.
- **"Hooks"** — generates multiple alternate hook-cut candidates from the
  same source video (example shown: a 41-second hook variant), independently
  playable/editable.
- **"Posts"** — auto-drafts structured social copy directly from the video's
  transcript: a multi-part post (main-content sections 1/2/3 plus a
  conclusion) with several auto-selected still-frame image options to pair
  with it, explicitly usable for Instagram/LinkedIn.
- Coupon/discount for Riverside offered (1 month free), link in description
  (exact code not spoken aloud in the transcript).

**Submagic (his second tool — paid with his own money, used narrowly):**
- Praises the **caption template presets** specifically as genuinely good.
- **Text-based editing**: select a word/phrase in the transcript panel, click
  "remove from selection," and the corresponding video segment is cut
  automatically — no manual timeline scrubbing needed.
- His actual, primary real-world use case, stated directly: paste a
  long-form YouTube video URL and Submagic auto-generates **25 clips**. Then
  the blunt, concrete quality assessment — easy to skim past but a real,
  specific data point: *"in practice, in reality, from these 25 clips that
  I'm getting, I can only really use like maybe two, maybe three."* That's
  roughly an **8-12% usable-clip yield** from Submagic's raw AI output, in
  his own stated practical experience. He separately assesses: *"the AI is
  like not very good of like picking [what] is like a really good short form
  video."*

**Opus Clip (third tool — his least favorite, does not use for his own
content):**
- Direct verdict: *"I just think that it's not that good, to be honest."*
- Specifically tested Opus Clip's **AI auto-B-roll insertion** feature and
  calls multiple generated results **"basically unusable,"** singling out a
  badly rendered hand/gesture shot as looking **"very weird"** and stating
  he "would not use that."
- Notes broad feature overlap with Submagic (paste a long video → get
  auto-clips + auto-ratings).
- One concession: **interface cleanliness/ease-of-use** — calls it "very
  clean and very minimal," usable by someone with zero video-editing
  background.

**Final stated verdict:** quick captioned clips with no quality/control
requirements → Submagic or Opus Clip are fine. Serious, full-control,
still-AI-assisted workflow → **Riverside**, his explicit personal pick.

**Analytics-feedback / self-adjustment hunt result:** **None found.** Every
"score" discussed in this video (Riverside's viral score, Submagic's
virality score referenced implicitly via comparison) is a **pre-publish AI
prediction** based on transcript/content analysis, not a closed loop against
actual measured post-publish view/retention/CTR data. No A/B testing of
titles/thumbnails/hooks against real click data mentioned anywhere.

---

## 5. "3 FREE AI Tools Just KILLED Video Production Agencies"

**Channel:** iampauljames · **URL:** https://www.youtube.com/watch?v=R8LKMhmyeY4

**[verified — full transcript read, 264 caption snippets, AND full video
description read live via browser (`ytInitialPlayerResponse`)].** Not
Twitch-specific, but directly relevant as a free/no-recurring-cost AI video
production stack that's transferable to clip post-production (captioning,
vertical reframe, B-roll generation) — flagged as tangential-but-useful per
the task's own instruction to note minor/in-passing tools.

**Full description text (exact, as published):**
> "I put the AI tools I use for helping local businesses in one place 👉
> pauljames.com/AIToolsTraining ... Triple Stack Video System: Turn 3 Free AI
> Tools Into Professional Video Services... This tutorial walks through the
> exact workflow for stacking **CapCut's AI Creator**, **Veed's** camera
> control, and **Meta AI's** unlimited generation into finished client
> videos... TOOLS COVERED: CapCut AI Creator (10-minute video generation, no
> limits), Veed (image-to-video with custom camera prompts), Meta AI
> (unlimited image generation + animation + extension)."

(Note: the video's auto-generated captions render "Veed" as just **"V"**
throughout the spoken transcript — the real product name, confirmed via the
actual description text, is **Veed**.)

**The "Triple Stack" — three free tools, one per production layer:**
1. **CapCut AI Creator Mode** — "instant video" option: pick a style, pick
   horizontal (YouTube) or vertical (Reels/Shorts) format, either type one
   sentence and let AI build the whole video or paste a full script for
   CapCut to voice, visualize, cut, and caption automatically. Concrete tip
   given: **narrator voices with a green badge "tend to perform better"** —
   test a few. Can generate up to **10 minutes** of video in one pass. Before
   export, drops into a full edit bay (swap clips, rewrite text, reorder
   pacing, upload your own footage or pull from CapCut's stock library) and
   a further full timeline editor ("edit more") with transitions/text
   overlays/effects.
2. **Veed** — described as a broader content suite (background removal,
   image gen, video creation), but the specific feature highlighted is
   **image-to-video with separate camera-motion prompting**: one prompt for
   "what happens in the scene," a second, independent prompt for **how the
   camera moves** (zoom, pan, orbit) — explicitly framed as the difference
   between "amateur motion and professional-look cinematography." If unsure
   what to write, a **suggestion icon** has Veed analyze the uploaded image
   and recommend a camera move itself. **Exact free-tier export settings
   given to stay unlimited: 5-second clips at 768 resolution, "quality mode"
   turned on** — this configuration is stated to give unlimited generations.
3. **Meta AI** — image generation (not video) as the starting point: control
   aspect ratio, and specific style-slider guidance given: **"keep variety
   moderate, weirdness low, and stylization high for clean results."**
   Generates 4 image options per prompt; can "restyle" an image (change
   aesthetic, keep content) or edit details before animating. **The "hack"
   called out explicitly**: each animated clip is only 5 seconds, but
   hitting **"extend"** continues the video from its final frame — repeating
   extend → download → extend again lets you build a 30-second or 1-minute+
   clip with no hard limit.

**Two worked business-monetization examples given, with exact price
figures:**
- Wedding photographer example: animate 5 of their existing photos in Meta
  AI, extend each to 15 seconds, compile in CapCut with voiceover/music.
  Stated total production time: **~2 hours**. Stated charge: **$500 for a
  package of five videos**, with recurring monthly repeat orders implied.
- Agency/local-business example: combine all three tools for branded video
  ads. Stated pricing model: **$1,200-$1,500/month retainer for 8-12
  videos**, or straight per-video billing.
- General framing throughout: **$4 to $600** as the stated range of what
  "finished content" from this stack can be sold for (very wide range as
  literally spoken — likely meant as "$400 to $600" but transcribed/spoken
  as "$4 to $600"; flagging the ambiguity rather than silently resolving it).

**Analytics-feedback / self-adjustment hunt result:** **None found.** Pure
production-technique and monetization-pitch content; no analytics or
iteration loop of any kind mentioned.

---

## 6. "How to Auto Share Posts to Multiple Social Media Accounts with Facebook Cross-Posting Automation!"

**Channel:** Nuelink · **URL:** https://www.youtube.com/watch?v=oFneHfcXNGQ

**[verified — full transcript read, 75 caption snippets (this is a short,
~3-minute tutorial), AND full video description read live via browser].**
Not Twitch-specific, but directly relevant as a concrete cross-posting
automation tool with a clearly documented setup flow — the kind of
minor/in-passing tool the task explicitly asked not to filter out.

**Tool: Nuelink** (newlink.com per the spoken audio, but the real product/
domain, confirmed via the description and on-screen branding, is
**Nuelink**). Full description text (exact):
> "Learn how to supercharge your social media presence with our tutorial on
> setting up Facebook Cross-Posting using Nuelink! In this step-by-step
> guide, we'll show you how to use Nuelink's cross-posting automation to
> effortlessly share Facebook reels, text, or image posts across all your
> social media accounts... What You'll Learn: Automations → Add New
> Automation → Facebook Crossposting Setup → Select Your Facebook Page →
> Choose Target Channels → Post Scheduling & Collection Options →
> Follow-Up Comments → Specific Post Selection → **Videos as Reels**
> (automatically convert your videos into vertical formats suitable for
> Facebook) → Hashtag Crossposting → Finalize Your Setup. Once set up,
> Nuelink will scan your Facebook account **every hour**, automatically
> sharing your new posts across all connected platforms."

**Exact setup flow as narrated:**
1. Log into Nuelink; pre-link all target social accounts (including Facebook
   Pages).
2. Automations → Add Automation → Cross-posting → "Add Automation" under
   Facebook Cross-Posting.
3. Pick the source Facebook Page, then select which social channels receive
   the cross-post. Explicit note: **don't forget to select a Pinterest
   board** if targeting Pinterest.
4. Optional: assign posts to a specific **collection** with its own
   schedule, or leave that off for immediate/automatic cross-posting as soon
   as detected.
5. Optional **"send a follow-up comment"** feature: auto-adds a comment to
   each cross-posted item, with an explicit **AI-assisted comment-writing
   option** ("spice it up with AI") plus hashtags/emojis/images, and a
   **configurable delay** before the comment posts — demoed set to **2
   minutes** after the original post.
6. Filter which post *types* get cross-posted: text-only, single image,
   multimedia, video, all of the above, or **restricted to posts containing
   a specific hashtag**.
7. Save. From then on, **Nuelink polls/scans the linked Facebook account on
   an hourly cadence** and auto-shares any new matching content to every
   connected platform, with no further manual action.

**Analytics-feedback / self-adjustment hunt result:** **None found.** This
is a short, purely mechanical distribution-automation tutorial with zero
performance-analytics content.

---

## 7. "I Built an AI To Run My Social Media on Autopilot"

**Channel:** Creator Magic · **URL:** https://www.youtube.com/watch?v=u8V45xsnkGA

**[verified — full transcript read, 189 caption snippets, AND full video
description read live via browser].** High relevance: **Opus Clip + Zapier**
end-to-end build, and this is the video with the clearest **human-in-the-loop
curation gate** of any of the 8.

**Full description (exact):**
> "👉 Build Your Own AI Content Machine with OpusClip: mrc.fm/opusclip ✨ Get
> 1 FREE Week + 50% OFF your first 3 months with code MAGIC! ✨ In this
> video, I build a fully automated AI Employee that takes my long form
> YouTube videos, turns them into dozens of viral clips, and publishes them
> to Instagram Reels without me lifting a finger... powered by OpusClip's
> insane new automation features... You'll see exactly how to set up your
> brand kit, create templates, and use Zapier..."
> Timestamps: 0:00 My AI Employee · 0:22 Step 1: Setting Up Your Brand Kit
> in OpusClip · 1:02 Step 2: Creating a Custom Brand Template · 1:28 Step 3:
> Building the "Creator" Automation in Zapier · 2:02 Action: Automatically
> Clip New Videos · 3:04 Step 4: Building the "Publisher" Automation · 3:43
> **The Human in the Loop (Virality Score)** · 4:40 How to Quickly Edit Your
> AI Clips · 5:27 Step 5: Looping Through Approved Clips · 6:11 Step 6:
> Automatically Post to Instagram · 7:06 Success! The Automation Works ·
> 7:17 How You Can Build This.

**Opus Clip brand-kit setup (asset-reuse pattern, directly analogous to this
project's own "asset reuse strategy" memory note):**
- Adds **brand vocabulary** to a running list so captions never misspell
  brand-specific terms.
- Uploads a **custom font** (his actual channel font).
- Uploads a branded **outro** media asset.
- Builds a reusable **brand template**: platform-specific aspect ratio
  (chooses **4:5 for Instagram**), a **"simple"** caption style using the
  custom font, an **effects** layer (e.g., "light bounce"), and AI cleanup
  toggles — specifically **removing filler words and pauses** "to keep
  things nice and tight and snappy." Template is named and saved for reuse
  ("Creator Magic" template).

**Zapier automation #1 — "Opus Creator" (production):**
- Trigger: **YouTube → New Video in Channel**, configured via the channel ID
  (found in the channel's "About" page).
- Action: **Opus Clip → Clip Your Video.** Explicit tool note: *"Opus does
  have an API, but it's application only, and with Zapier you can automate
  straight out the box"* — i.e., Zapier is used specifically because it
  provides pre-built Opus Clip actions without needing to apply for raw API
  access.
- Maps the new video's URL in automatically. Configures: **clip length
  30-60 seconds** ("the sweet spot for posting... on Instagram"), selects
  the saved **"Creator Magic"** brand template, and sets **"Don't Clip" =
  false** (i.e., clipping is enabled). Test run reports an **ETA of 6
  minutes** to process one video.

**Zapier automation #2 — "Opus Publisher" (curation + distribution):**
- Trigger: **Opus Clip → New Project Completed** — fires as soon as
  automation #1 finishes a clipping job.
- Action: **Opus Clip → Get Clips.** Result of this specific run: **5 clips**
  returned, each carrying a **"high virality score."**
- **Notable extra Opus Clip feature named: an AI-generated "why this will
  trend" explanation, explicitly stated to be "powered by Google Gemini."**
  Demo example given: the source content covered something announced at a
  real **"Dev Day 2025"** event, and Opus's Gemini-backed explanation
  correctly identified that "people are searching for this right now" — a
  form of **real-world topical/trend-relevance detection**, distinct from
  (and not to be confused with) genuine post-publish-performance feedback.
- **"Liked clips only" toggle — the explicit human-in-the-loop control.**
  Creator states directly: *"if you want a human in the loop... I love that
  clip, so again, it's another heart going on this clip... it's as simple as
  that to make sure I have complete control of what I'm putting out on
  Instagram, and not just throwing slop out there without monitoring it."*
  Only clips he personally hearts inside the Opus Clip web UI get pulled
  into the publishing automation.
- Opus Clip's **in-app clip re-editing** is used live: a generated clip has
  its subject slightly mis-centered ("95% of the way there, but sometimes it
  just doesn't quite get it in the screen") — he manually re-centers the
  crop and trims the tail, then saves; a quick re-edit/re-render follows.
- **Looping mechanism**: Zapier's **"Create Loop from Line Items"** action
  iterates over the liked clips, mapping each clip's **title** and **video
  URL** into loop variables (tested with the 5 liked clips from this run).
- **Publishing step, with a named limitation and workaround**: target is
  **Instagram (business account required)**. Explicit note: *"The actual
  Instagram video publish action is broken on Zapier right now, but I've got
  a workaround that I've posted up down below for you"* — implemented as two
  chained **API Request** actions against the Instagram Graph API directly
  (first request notifies/stages the video for publish; second request,
  referencing the first response's returned ID, actually publishes it).
  Posts are explicitly scheduled at **"randomized times"** within the loop
  rather than all at once.
- Confirmed working live: refreshes Instagram and shows the clip live and
  playable on the account.

**Analytics-feedback / self-adjustment hunt result:** **None found**, beyond
the pre-publish "why this will trend" (Gemini-powered, topical-relevance,
not post-publish-performance) signal and the manual heart/like
human-curation gate described above. No mention of checking actual
Instagram/TikTok/YouTube view or retention data after publishing and feeding
it back into clip selection, style, or posting decisions. No A/B testing of
titles/thumbnails/hooks.

---

## 8. "How to Automate Cross-Platform Social Media Posting"

**Channel:** Pabbly · **URL:** https://www.youtube.com/watch?v=av06ZI2bKW4

**[verified — full transcript read, 404 caption snippets]. Description not
independently re-verified live in this pass** (a live-browser re-fetch
attempt was interrupted mid-session by an account spend-limit event before
it completed) — **[search]** for anything beyond the transcript itself, but
the transcript alone is exhaustive for this video's actual content, which is
a full live screen-recorded build.

**Tool: Pabbly Connect** (`pabbly.com/connect`). Free tier explicitly stated:
**100 tasks/month** for new signups. Two workflow-builder modes offered:
**"Beta"** (described in-product as "modern, fast and more flexible") and
**"Classic"** ("stable and the familiar approach") — creator uses Beta for
this build. Workflows are organized into user-created **folders** (e.g., his
own "automations" folder). A **Pabbly Community** forum is referenced for
extra how-tos (e.g., "how to create a new folder inside Connect").

**The exact automation built, step by step (source → Instagram + LinkedIn
cross-post, triggered by a native Facebook Page post):**
1. **Trigger: Facebook Pages → New Post.** Connection built by clicking
   "Connect with Facebook Pages," authorizing the account (auto-succeeds if
   already logged into Facebook in the same browser), then selecting the
   specific Page (his demo page: **"Digital Dynamics"**). A **"Simple
   Response"** toggle is turned on to get a cleaner/organized webhook payload
   (vs. an "advanced"/raw error-format response if left off).
2. To actually receive trigger data, Pabbly requires a **live test
   submission** — he manually creates a real new post (caption + image) on
   the Facebook Page to fire the webhook once, then confirms Pabbly received
   it (shows the returned post ID, name, image link, and caption in the
   Pabbly UI).
3. **Action step: File Uploader by Pabbly → "Upload File and Get URL."**
   Explicit stated purpose: Facebook's returned image URL is very long, so
   this step **re-hosts/shortens it** into a clean URL before it's reused
   across other platforms' post-creation calls. Inputs are **mapped**
   (Pabbly's term for inserting a dynamic reference to a previous step's
   output) rather than typed manually: file URL ← Facebook trigger's image
   URL; file name ← a literal string built from the post's **photo ID**
   plus a **`.jpg`** extension.
4. **Action step: Instagram for Business → "Publish Photo."** New connection
   via "Connect with Instagram for Business" (again auto-succeeds if
   Instagram is already linked to the same Facebook login). Selects the
   target Instagram account from a dropdown. Maps in the **shortened file
   URL** from step 3 and the **caption** directly from the Facebook trigger
   step. Confirmed live by refreshing the real Instagram account and showing
   the new post with matching image + caption.
5. **Action step: LinkedIn → "Share Text with Image."** New connection via
   "Connect with LinkedIn" (email/password sign-in, autofill shown). An
   **"author"** field auto-populates after a manual "refresh fields" click.
   Maps in the same shortened file URL plus the same caption text; sets
   **visibility = Public**. Confirmed live on the actual LinkedIn profile.
6. Full recap given on-camera: Facebook-Pages-new-post trigger → File
   Uploader (shorten URL) → Instagram publish-photo action → LinkedIn
   share-text-with-image action, fully automatic and "without wasting your
   minutes."

**Support/contact info given on screen at the end (concrete, worth
preserving verbatim):** support email **support@pabbly.com**, community/
forum at **forum.pabbly.com**, and a separate URL referenced for
pricing-related questions. A workflow **"clone link"** for this exact
automation is stated to be in the video description (not independently
re-confirmed this pass — see confidence note above).

**Analytics-feedback / self-adjustment hunt result:** **None found.** This
is a pure mechanical cross-posting demo with no analytics, scoring, or
feedback-loop content of any kind — it is the most purely "plumbing" of all
8 videos, no AI content-judgment step anywhere in it (contrast with Klap/
Opus Clip/Submagic/Riverside's scoring layers in the other 7 videos).

---

## Cross-video patterns

**The single most important finding, stated directly:** across all 8 videos'
**full, real, spoken transcripts** (not just titles/descriptions this time),
**there is no genuine analytics-feedback / self-adjusting content loop
anywhere.** No creator describes checking real post-publish performance data
— views, retention/watch-time curves, CTR, comments/engagement — and using
it to programmatically or even manually adjust future clip style, pacing,
topic selection, captions, thumbnails, or titles. **No A/B testing of
titles, thumbnails, or hooks is mentioned in any of the 8 videos.** This
extends and strengthens the prior recovery pass's same conclusion
(`RESEARCH_YOUTUBE_SOURCES.md` §5a) — that pass could only check
titles/descriptions and explicitly flagged this as an open question; this
pass checked the actual full spoken content of all 8 and the answer is
still no. The two closest adjacent things found, both worth remembering but
neither is the real thing:
- **lge0jth5sl0's explicit posting-cadence ramp** (2-3/day → 10/day → 20/day
  over weeks 1-4) — a real behavior change driven by a real platform-response
  risk (new accounts getting "flagged" and drawing "zero views" if they post
  at full volume immediately), but it's a fixed, pre-set schedule applied
  uniformly, not a loop that reads a specific account's actual measured
  results and adapts.
- **Pre-publish AI "virality"/"viral" scores**, present in *four* of the
  eight tools discussed (Klap in video 2, Submagic in video 3, Opus Clip in
  video 7, Riverside in video 4) plus Opus Clip's Gemini-powered "why this
  will trend" topical-relevance explanation (video 7) — all of these predict
  likely performance from the content itself before publishing; none of them
  close the loop against real measured outcomes afterward.

**Real, cross-referenced tool names (new confirmations/corrections from this
pass, building on the already-compiled list in `RESEARCH_YOUTUBE_SOURCES.md`
§5d):**
- **Klap** — video 2's auto-captions consistently mangle this to
  "Clap"/"ClapF," which could easily be misread as a different/unknown tool
  if only skimming the transcript; the real product is Klap, and it has a
  genuine, documented public API used directly via n8n HTTP Request nodes
  (Header-Auth style, `Authorization` header) — not just a UI product.
- **Veed** — video 5's auto-captions render this as just "V" throughout the
  spoken transcript; only the video's actual *description* text (read
  separately, live) confirms the real name is Veed.
- **Blotato** — video 2's captions render this "Blot"/"Plotato"; confirmed
  real via cross-reference with the already-known "Blotato" name from the
  prior recovery pass.
- **Nuelink** — video 6's audio says "newlink.com," but the actual on-screen
  branding/description confirm the product is Nuelink (a Nuelink-branded
  channel, consistent with the already-known "Nuelink" cross-poster entry
  from the prior pass).
- **Submagic's MCP server** is a real, concrete, currently-usable
  integration point (confirmed: "15 Submagic tools available" once
  connected via Claude Desktop) — this is a genuinely actionable finding for
  this project if Submagic is ever adopted: it's controllable by an AI
  coding agent directly, not just via its own web UI.
- **Opus Clip's brand-kit / brand-template system** (video 7) is the
  clearest concrete precedent across all 8 videos for this project's own
  "asset reuse strategy" pattern (lock reference assets once, reuse across
  runs) — brand vocabulary list, custom font, custom outro, and a named
  reusable per-platform template (aspect ratio + caption style + effects +
  filler-word removal) are all set up once and then referenced by ID in
  every subsequent automated clipping run.
- **Riverside, Submagic, and Opus Clip get a rare head-to-head, opinionated
  comparison** in video 4, from someone who actually pays for and uses all
  three: Riverside wins on all-in-one control and quality; Submagic wins
  narrowly on caption templates and text-based editing but has poor raw
  clip-selection quality (his own stated ~2-3-usable-out-of-25 yield); Opus
  Clip is rated worst overall, with its auto-B-roll feature singled out as
  "basically unusable," though its UI is praised as the easiest for total
  beginners.
- **Whop** appears independently in two of these 8 videos (video 2 and
  video 3) as a real marketplace where streamers/creators post paid
  clipping bounty campaigns — third-plus independent confirmation when
  combined with the prior recovery pass's video 13 finding.
- **The clipper-economy pay-rate numbers now have three independent,
  mutually consistent data points** across videos 2 and 3: ~$15/minute of
  clipped footage (video 2, citing an Upwork-corroborated rate) and $1-3 per
  1,000 views generated, i.e. up to $500-$1,500 for one 500k-view clip
  (video 3) — these are two different pay models (flat per-minute-edited
  vs. performance/CPM-per-view) both genuinely in use in this economy, not
  a contradiction.

**A serendipitous, out-of-scope find worth a one-line pointer (not one of
the assigned 8, encountered via YouTube's own recommendation carousel while
researching video 4/8, and already independently corroborated in
`RESEARCH_YOUTUBE_SOURCES.md` as its own video 9):** *"The Clip Farm Setup
That Gets Your Stream Clips On TikTok In 10 Minutes"* (Cpaws Music,
`dOQS2q_ONG0`) — names **OBS's native Replay Buffer** feature (free,
built-in, hotkey-saves the last N minutes of a live stream with zero
manual clipping during the stream itself) and **Nexus Clips** as the
auto-reframe/caption tool, plus a concrete 3-way clip-type taxonomy ("Value
Tip Clip," "Best Reaction Clip," "Personality Clip") for what actually gets
views. Flagged here only as a pointer for a future dedicated pass, not
analyzed further under this task's 8-video scope.
