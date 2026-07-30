# Fresh-Pass Deep Research: Twitch VOD Clipping Automation (9 videos)

Re-study of 9 previously-flagged YouTube videos for the "automated clipper bot" project
(Twitch VOD highlight detection → auto-clip generation → captioning → vertical reframe →
YouTube Shorts / TikTok / Reels distribution → cross-posting/monetization). This pass reads
full real transcripts and full real YouTube descriptions for every video (fetched via
in-page `ytInitialPlayerResponse` extraction and YouTube's auto-generated caption transcripts,
saved locally and read in full) — **all 9 videos below are [verified]**: every fact tagged as
such was read from the actual transcript text and/or the actual expanded video description,
not inferred from title/thumbnail. Nothing in this document is marked [search].

Source transcript files (full, timestamped): `C:\Users\AwBro\Desktop\automated clipper bot\research\transcripts\<video_id>.txt`

---

## 1. "How To Auto-Post Twitch Clips to Social Media (TikTok, YouTube, Instagram, Twitter, and more)"
**Channel:** Repurpose io | **URL:** https://www.youtube.com/watch?v=zNtNYkgCnSA
**Length:** 2:40 (160s) | **Views:** ~1,066 | **Confidence: [verified]** (full transcript + full description read)

This is a short promotional/demo video for **Repurpose.io** (https://repurpose.io), a
cross-posting/distribution automation SaaS. It is entirely about **distribution automation**,
not clip detection or editing — there is no clip-selection, editing, or captioning
functionality shown or discussed.

### Concrete workflow shown (three distinct "workflow" types inside Repurpose.io)
1. **Backup workflow ("back up all my content")**: Create new workflow → select **Twitch**
   as the source → select your Twitch account → choose "back up all my content" → destination
   **Google Drive or Dropbox** → choose which content type to back up: **highlights, uploads,
   or clips** → "create workflow." Framed explicitly as solving Twitch's VOD-expiry problem
   ("Twitch doesn't save your videos forever... if you're not backing them up, they're
   eventually gone").
2. **Repurpose existing content workflow**: Workflows tab → "repurpose existing content" →
   source = Twitch → destination = any supported platform (demoed with **YouTube Shorts**) →
   content type (e.g., highlights) → "create workflow" → then you can **select specific days
   and times** for the old content to be scheduled out to the destination platform(s).
3. **Automate all future content workflow**: source = Twitch → destination platform (demoed
   with **Pinterest**) → "create workflow" → from then on, **every new Twitch stream
   highlight or clip is automatically repurposed to that destination with zero manual
   action** ("set it and forget it").

### Supported destination platforms named in the video
YouTube Shorts, Instagram Reels, TikTok, Twitter, Google Drive, Dropbox, Pinterest.

### Notable phrasing/positioning
"Less effort, more content, less burnout, more reach." No mention of AI-based clip selection,
virality scoring, or any performance-feedback loop — this tool is purely the "get it
everywhere automatically" layer that would sit *downstream* of a clip-generation tool like
NexusClips/Opus/Submagic seen in the other videos.

### Analytics-feedback / self-adjustment content
**None found.** No mention of checking post-publish metrics, A/B testing, or adjusting
future output based on performance.

---

## 2. "How To Make Twitch Clips That Go VIRAL Every Time!"
**Channel:** Cal's Creation | **URL:** https://www.youtube.com/watch?v=Yj0CAaUhuQM
**Length:** 5:18 (318s) | **Views:** ~2,149 | **Includes paid promotion (sponsored)**
**Confidence: [verified]** (full transcript + full description read)

Sponsored deep-dive tutorial on **NexusClips** (https://nexusclips.com — discount code
`CAL` for 10% off any plan, monthly or yearly). This is the single richest video for concrete
per-clip editing/scoring mechanics.

### Full description timestamps
`00:00` The issue with posting stream clips/shorts | `00:11` The secret to making viral
clips/shorts easily | `00:35` The AI that creates viral clips | `02:10` How to curate viral
clips for your personal style | `02:51` (aside) | `02:59` How this tool edits your clips for
you | `04:04` How to automatically caption your stream clips | `04:25` The importance of
adding your Twitch name to clips | `05:12` A "secret" to use with your stream clips (the hook
feature) | `06:41` How to post & schedule your clips for growth | `07:47` Free Twitch artwork.

### NexusClips workflow (exact steps from transcript)
1. **Ingest**: "Video to Clips" option, log in with Twitch account (grants access to full
   stream VODs) — **or** log in with a YouTube account instead/also, so old YouTube gameplay
   videos can be mined for clips too. Select the specific stream/VOD to process.
2. **AI clip generation**: AI scans the full VOD and compiles a list of candidate clips down
   the left side. Example given: a 4-hour horror stream yielded **~70 different clips**
   ("literally one clip every day for 2 months").
3. **Virality Index**: every candidate clip gets a **numeric score out of 100** ("virality
   index"), and the AI **ranks clips highest-to-lowest** by this score. Per the creator: "the
   higher the number the more likely that clip is to go viral **based on the content of the
   clip**... it bases this purely on **what has gone viral before on the short-form platforms
   like TikTok and Shorts**." This is explicitly a **pre-trained/heuristic virality model**,
   not a per-account feedback loop — the model is informed by aggregate what's-gone-viral-
   before data, not by *this specific creator's own* post-publish performance.
   - Explicitly stated: lower-ranked clips are "still... worth making," not junk — score is
     relative likelihood, not a hard filter.
4. **"Generate new moments" (prompted clip search)**: a separate button lets you type a
   free-text prompt against the *same* processed stream to pull a different cut of clips —
   e.g. prompting "give me jump scares" against a horror stream returns AI-selected jump-scare
   moments, still virality-ranked. You can prompt by emotion, moment-type, or niche and the
   tool "tunes itself" while still returning the viral ranking.
5. **Editing bay** (per selected clip): click "create clip" → yellow slider to trim
   start/end → "edit clip" → full editor:
   - **Framing**: auto face+gameplay detection; creator's personal preference = webcam
     face zoomed in above gameplay, "very typical twitch clip look"; chat overlay is also an
     available framing option.
   - **Subtitles**: auto-generated as soon as speech is detected; style customizable — creator
     uses a **purple highlighted-word-as-spoken font** ("because it has that kind of Twitchy
     feel... twitch colors being purple").
   - **Sticker**: adds your channel name/handle (YouTube, TikTok, or Twitch icon variants).
     Creator's practice: use the **Twitch-icon sticker**, purple color, placed for only a
     few seconds at the very start, positioned between webcam and gameplay so it doesn't
     obstruct content — explicitly framed as a conversion mechanism ("if they don't know
     your channel name... they can't check you out on Twitch").
   - **Hook feature** (creator's "favorite feature"): AI auto-generates a short **teaser
     text block overlaid at the very start of the clip** that previews what's coming, e.g.
     AI picked "unexpected twist ahead" for a horror-game jump-scare clip. Explicit purpose:
     differentiate from generic stream clips and **stop viewers' infinite-scroll** — "it will
     drive up your attention time, which is the difference between a clip that will boom and
     a clip that will completely flop." Hook text/font/color are editable.
6. **Auto-caption + auto-hashtag/tags for posting**: when you click share → TikTok (or
   YouTube Shorts), the tool auto-generates a **full caption and hashtag set** "based on its
   own research on what's going to do the best for you" — specifically: **"it will find clips
   similar to yours and see which ones have done well, and then it will use those tags on
   yours."** This is an explicit (if coarse) analytics-informed feature — hashtag/caption
   choice is driven by aggregate performance data of *similar* clips across the platform, not
   the individual creator's own account history. Different tag sets are generated per
   destination platform (TikTok tags differ from Shorts tags).
7. **Publish/schedule**: one-click publish direct to linked TikTok/Shorts accounts, or click
   "program" instead of publish to **schedule** the clip for a future date. A **content
   calendar** on the home screen shows everything queued and its scheduled date.

### Analytics-feedback / self-adjustment content
Partial/indirect: virality scoring and hashtag/caption generation are both explicitly stated
to be derived from aggregate "what's gone viral before" / "clips similar to yours that have
done well" data — i.e., the *product* has a feedback loop baked in from cross-user data, but
nothing in this video describes the *creator* reviewing his own post-publish view/retention
numbers and manually adjusting strategy. No A/B testing of titles/thumbnails/hooks is
mentioned.

---

## 3. "How I made a Fully-Automated Clipping System || TUTORIAL #streaming #streamerbot #tutorial"
**Channel:** Vaika (VTuber/Twitch streamer) | **URL:** https://www.youtube.com/watch?v=1CNVAfY2FKc
**Length:** 28:19 (1700s) | **Views:** ~12,208 | **Confidence: [verified]** (full transcript +
full description read)

**This is the single most technically important video of the 9** for the "detect the best
moment live, during the stream, using free/local tools" half of the project. It is a from-
scratch build tutorial for a **zero-click, chat-reactive, live auto-clipping pipeline** using
only free software. Creator states she spent **over a year** refining/testing this on her own
streams.

### Required stack (all free)
- **OBS Studio** (streaming software) — creator notes an important gotcha: the **Advanced
  Scene Switcher plugin** (used for advanced/experimental triggers, see below) is **no longer
  supported on current OBS** and requires rolling back to **OBS version 30.2.3** specifically
  (link given in description: `github.com/obsproject/obs-studio/releases/tag/30.2.3`).
- **Aitum Vertical** — free OBS plugin for vertical-format scene composition/recording
  (`obsproject.com/forum/resources/aitum-vertical.1715/`).
- **Streamer.bot** (`streamer.bot`) — free automation/scripting bot that integrates with
  Twitch chat, OBS (via websocket), and third-party services; described as "the entire
  brains" of the system.
- **Speakerbot** — Streamer.bot's "sister program," used to handle TTS (text-to-speech) and
  integrate it with the auto-clipper triggers.
- (Optional/experimental extras) **Advanced Scene Switcher** OBS plugin
  (`obsproject.com/forum/resources/advanced-scene-switcher.395/`) for mic-volume-peak and
  screen-region pattern-matching triggers (requires the older OBS build above).

### Setup steps (condensed, but every concrete number/setting preserved)
1. **Aitum Vertical dock setup**: Docks menu → Vertical → open settings (cog icon) → set
   canvas resolution to **1080×1920** (standard vertical format for YouTube/TikTok). Aside:
   references another VTuber (**RickyVTuber**)'s trick of setting the canvas as wide as two
   monitors so gameplay and VTuber model (green-screened) can be recorded as two separate
   zones and edited apart later (link given: `x.com/rickyvt_/status/1807024787555794965`).
2. **Backtracking (the core mechanism)**: Aitum Vertical's "Backtrack" continuously records
   in a rolling buffer the entire time you stream but **only writes a clip to disk when
   triggered**. Settings used: "Backtrack runs while streaming/recording" = checked; **clip
   length = 120 seconds (2 minutes)** — "I found they capture just about everything needed at
   that length." Save-location must have enough free space since many clips accumulate per
   stream (creator manually reviews/deletes obsolete ones post-stream). **Hotkey**: Save
   Backtrack (not the Record/Start-Stop hotkey) set to **Shift+F4** — explicit warning to use
   an uncommon modifier (right-Shift/right-Alt) to avoid conflicts.
3. **Vertical Scenes/Sources**: separate "vertical scenes" (distinct from normal OBS scenes,
   freely named) are built by adding **entire existing OBS scenes** as sources (not
   individual elements) — this captures alerts/overlays/audio in one pass. Explicit warning:
   **do not rename OBS sources** when doing this, or it breaks your live scenes. Manual
   crop/scale/position (drag corners, Alt+drag to crop) to fit gameplay + webcam/VTuber into
   the vertical frame; recommends keeping a **vertical-format "safe zone" template overlay**
   visible while aligning (TikTok UI icons cover large screen areas). Multiple vertical
   scenes are built (e.g., "gaming" scene, "just chatting" scene with chat visible in frame
   — explicitly because "funny clippable moments can stem from chat saying something
   stupid"). Final step: **right-click each vertical scene → "Linked Scenes"** to bind each
   vertical scene to its corresponding real OBS scene, so recording follows whichever scene
   is live.
4. **Hardware/load caveats**: explicitly tested — an **RTX 4080 struggled** when backtracking
   + streaming simultaneously at a resolution larger than the vertical target; recommends
   testing your own hardware headroom, or using a secondary PC. OBS's own built-in backtrack
   recording has less system load than Aitum's but lacks vertical-format support.
5. **OBS recording settings (parallel full-VOD recording, optional but recommended)**:
   Output mode = Advanced → Recording tab → format must be **Hybrid MP4** (only format that
   supports embedded markers) → audio bitrate bumped to **6,000** (higher than streaming
   bitrate) for crisp VOD quality → "Automatically record when streaming" checked (or,
   as the creator actually does it, record start/stop is controlled by Streamer.bot itself).
6. **Streamer.bot action build ("auto clip" action)**:
   - Sub-action 1: **OBS → "Create Record Chapter"** — embeds a **named marker** into the
     OBS Hybrid-MP4 recording (creator names it "clip") so markers are visible/labeled when
     scrubbing the VOD in an editor later.
   - Sub-action 2 (optional): **Twitch Channel → "Create Clip Marker"** — creates a marker on
     the Twitch VOD too; explicitly **not** recommended to auto-create actual Twitch clips
     via this route because it floods you with clips you then have to individually review —
     better to just use the marker to *locate* moments and rely on the local backtrack
     recording for the actual clip file.
   - Sub-action 3: **Core → System → Keyboard Press**, set to the same Shift+F4 hotkey — this
     is what actually fires the Aitum Backtrack save.
7. **THE KEY TECHNIQUE — chat-reactive auto-triggering (chat-spike/sentiment detection)**:
   Streamer.bot → Commands tab → new custom command (creator's naming convention: prefix
   commands meant for manual/chat use with "!", e.g. `!autoclipcontroller`, though this
   particular command is meant to be **triggered passively by chat, not typed on purpose**).
   In the command's trigger list, literally list **chat keywords** on separate lines: `lmao`,
   `kek`, `lol`, `funny`, `silly`, `laughing`, `hilarious`, plus **channel-specific emote
   names** (e.g. her own emote "VikerVWow") and reaction words like `GG`. Settings: match
   **location = "anywhere in message"**; **ignore bot accounts** = checked; **ignore per-user
   counter** = checked; **case-sensitive = off**; **source = Twitch message**.
   - **Cooldowns (critical to prevent over-triggering)**: **global cooldown = 120 seconds**
     and **per-user cooldown = 120 seconds** — matched exactly to the backtrack clip length,
     so an active chat doesn't spam-trigger saves faster than clips can be produced.
   - **Permissions**: left open to everyone (viewer/mod/all) by default; can be restricted to
     specific users if desired.
   - This command is then wired as the **trigger** on the "auto clip" action (Core Commands →
     Command Triggered → select the command).
8. **Other native Streamer.bot triggers the creator also wires to the same auto-clip action**:
   **raids** (explicit reasoning: "you never know when a big streamer might raid you and you
   want to capture that moment"), **follows**, **gift subs**, **channel-point redeems**,
   **donation-goal-reached** (via the **Tiltify plugin** integration), **shout-outs**, and
   **TTS-triggered events** (via Speakerbot integration). Recommends creating a **separate
   named action per trigger type** (e.g., name the OBS marker "raid" specifically) so VOD
   markers are self-explanatory later when editing.
9. **Advanced/experimental extras (require the older OBS 30.2.3 + Advanced Scene Switcher
   plugin, "no longer supported" on current OBS, explicitly marked experimental)**:
   - **Mic-volume-peak trigger**: Advanced Scene Switcher macro — "if audio output volume of
     [mic source] is above [threshold%]" → triggers the same clip hotkey. Intended for
     scream/loud-reaction detection; creator notes it won't help if you don't scream much or
     have a noise gate.
   - **Screen-pattern-matching / OCR-style trigger**: reads a defined screen region (via a
     screenshot source) and pattern-matches against a reference image to detect specific
     game-UI states — concrete example given: detecting the **"You Died" screen in Dark
     Souls** to trigger a death counter/clip. Uses "perform check only in [specific] area" to
     narrow the match zone and reduce false positives; described as **resource-heavy and can
     crash OBS**. Bonus idea from the same plugin: auto-play lobby music when the lobby
     screen is detected, auto-stop when it's no longer detected.
   - **(Unfinished/idea-stage) Chat-rate-spike trigger**: creator says she was "in talks with
     someone in the Streamlabs Discord" about building a trigger based on **spike in chat
     message rate** (not specific keywords) — reasoning: "chat rate means something
     interesting and clippable is happening," useful especially for smaller streamers.
     Explicitly unfinished ("I didn't get very far in working out the sub actions, but anyone
     who wants a crack at it, feel free"). Related unbuilt idea: use chat-rate monitoring to
     also auto-trigger **Shield Mode** (Twitch's anti-raid/bot-raid protection) when a bot
     raid is detected via rate spike.

### Cross-referenced tutorials named in the description (for anyone building this stack)
- Aitum Widescreen Recording — **RickyVTuber**: `x.com/rickyvt_/status/1807024787555794965`
- StreamerBot Setup — **Nutty** (`@nuttylmao`): `youtu.be/CIlcWCoKBcs`
- StreamerBot v1.0 Setup — **Nutty**: `youtu.be/gfGy1gRH5ik`
- StreamerBot Tutorials — **Gael_Level**: `youtu.be/9PF4wmEWsic`
- Free Safe-Zone Overlays — **TheOrsonLord**: `youtu.be/9dEMB1bvDo0`

### Analytics-feedback / self-adjustment content
**None.** This video is 100% about live *detection/triggering* mechanics (chat sentiment,
raids, mic peaks, screen state), not about post-publish performance review or adjusting
future clipping behavior based on view/retention data.

---

## 4. "I Let an AI Run My Twitch Clips for 7 Days… Here's What Happened"
**Channel:** Cal's Creation | **URL:** https://www.youtube.com/watch?v=oLg-TMlKUKA
**Length:** 7:28 (448s) | **Views:** ~1,603 | **Confidence: [verified]** (full transcript +
full description read)

Follow-up/case-study video from the same channel as Video 2, using the same tool
(**NexusClips**, code `CAL` for 10% off). This is the closest thing among the 9 videos to a
genuine **experiment log with real before/after numbers**, though it's an experiment in
*hands-off automation*, not in analytics-driven iteration.

### The experiment
Creator streamed for a week doing **zero manual clipping/editing/posting** and let NexusClips
run unattended: it auto-picked moments, auto-edited, auto-captioned, and (per his normal
workflow) he just reviewed and clicked "post" with no tweaks. Explicit test question: "can
the AI actually do better than me, who is not too bad at editing myself?"

### Concrete observations
- NexusClips' top-ranked ("highest ranked, most viral option" per its virality list) pick for
  clip #1 was a moment the creator "would have never really thought to clip" — explicit
  praise for the tool's ability to catch moments a human would dismiss as not clip-worthy.
- Some AI-picked clips were "weird"/unexpected picks that nonetheless **outperformed
  carefully-edited clips** — creator's read: "it means that this is working."
- **His normal (non-experiment) workflow, described explicitly**: use NexusClips to generate
  the base clip, then manually tweak captions/fonts/colors, add his Twitch name, and **"add a
  hook to the start of the video to make it maybe a little bit more retention-based."** This
  is a direct, explicit statement that a hook is used specifically as a **retention lever**
  (i.e., an intentional, if informal, optimization based on general understanding of what
  drives retention — not a measured feedback loop, but a named causal belief).
- Auto-caption/auto-hashtag quality assessment: "this AI does consider the context of your
  clip and the niche it's in, and it will do the hashtag research essentially for you" — same
  claim as Video 2 (aggregate-performance-informed tag generation).
- **Scale/schedule**: planned 1 clip/day × 7 days × 3 platforms (YouTube, TikTok, Reels) = 21
  posts; actually **stretched to 14 days / 42 total clips** because the tool kept generating
  usable clips he didn't want to waste.
- Used NexusClips' **built-in scheduling + content calendar** to queue posts in advance across
  platforms without manual export/upload.
- **Result stated as a real number**: "after day 1 to day 14 of posting one clip a day across
  all those platforms, they **totaled around 100,000 views**" — explicitly stated to be *more*
  than his usual manual short-form performance on those same channels, attributed to
  **volume/consistency** (posting more, across more platforms, than he would have bothered to
  do manually) rather than to superior per-clip editing quality.
- Explicit acknowledgment that **not every clip performed** — "some flops," "didn't hit the
  stratosphere of views that the others did" — but total volume/consistency still won out.
- Stated broader belief: consistent daily posting (enabled by automation) itself functions as
  a growth lever independent of any one clip's quality — "a really good way of keeping your
  channel consistent and professional looking... keeps you in people's minds."
- Explicit position on AI-in-content ethics: fine with AI that automates *his own* real
  streamed content (clipping/captioning/voice cleanup), opposed to AI that generates
  synthetic images/video/humans in place of real content ("you kind of haven't made the
  video... you've kind of just got robots to fathom up this thing").

### Analytics-feedback / self-adjustment content
The clearest example across all 9 videos of a *creator* explicitly naming a specific
editorial choice (hooks) as a **retention-driving lever** and reporting **real aggregate
view numbers** from a controlled before/after-style test. Still **not** a system that reads
back per-clip analytics and *automatically* adjusts future clip selection/style — the
adjustment (adding hooks/tweaking captions) is manual and happens only when he opts out of
"hands-off" mode.

---

## 5. "The Clip Farm Setup That Gets Your Stream Clips On TikTok In 10 Minutes"
**Channel:** Cpaws Music | **URL:** https://www.youtube.com/watch?v=dOQS2q_ONG0
**Length:** 7:01 (422s) | **Views:** ~5,936 | **Includes paid promotion**
**Confidence: [verified]** (full transcript + full description read)

Sponsored tutorial combining **OBS Replay Buffer** (free, built into OBS — distinct from the
Aitum backtrack approach in Video 3) with **Nexus Clips** (link: `nexusclips.com/?via=cpaws`,
code `CPAWS` for 10% off) for editing/distribution. Also includes an explicit **content-type
framework** and a **weekly cadence schedule**.

### Part 1 — OBS Replay Buffer setup (exact steps)
Settings (bottom right) → Output → Replay Buffer → **enable replay buffer** = on → **maximum
replay time = 60 seconds**. Hotkeys → find **"Replay Buffer: Save Replay"** (not "Start Replay
Buffer," which merely keeps it running silently in the background) → creator binds it to
**Numpad 9**. Pressing that hotkey saves the **last 60 seconds** as a clip file. Output →
Recording tab shows the folder path clips are saved to. Output is a **raw, unedited,
horizontal** file at this stage.

### Part 2 — Nexus Clips editing workflow (condensed vs. Video 2's fuller walkthrough)
"Import clip" → clip loads into editor in ~5 seconds → trim on the timeline with **C to cut
in, C again to cut out**, delete unwanted segments → **Reframe**: one click auto-detects
face + gameplay and centers them (manual nudge available) → **Subtitles**: auto-generated in
~5 seconds, pick a template → **Sticker**: promote Twitch/YouTube handle, recommended
placement = **very end of the clip, brief moment only** → **Hook**: pick a preset, edit text →
finished edit in "less than a minute or two" → **Share** panel posts **directly to TikTok or
YouTube** with no download step required (download-then-manual-upload only needed for
Instagram or other platforms without direct integration).

### Explicit tips stated as improving performance (creator's own stated best practices)
- **Hook length: keep it to about 3–9 words** — "something simple, but really you just want
  to spark their curiosity to make them actually want to watch the video."
- **Subtitle vertical placement**: not too high or too low (risk of being cut off by platform
  UI) — "right in the middle or right underneath your chin is usually a good spot."
- **Pacing**: "don't be afraid to cut out too much" dead air — "pacing is everything these
  days, attention spans are so low."

### The "3 types of clips that actually perform" framework (explicit, named)
1. **Value Tip Clip** — share a non-obvious tip about the game ("not a basic tip, but
   something that makes someone say 'wait, seriously?'"). Concrete example: in Fortnite,
   visible footsteps is off by default — turning it on is "an instant competitive edge."
   Stated advantage for newer streamers: doesn't require charisma, just game knowledge.
2. **Best Reaction Clip** — explicit warning that most streamers fail here because they clip
   *every* reaction instead of only their best; the tell for a genuinely good one: **"your
   chat was going crazy before you even processed what happened — they clipped it before you
   did."**
3. **Personality Clip** — an unscripted moment where personality shows through (funny chat
   exchange, hot take, natural one-liner); explicit rule: **"never try to fake it, only use it
   when it happens naturally"** — self-test: "you cannot stop watching it back yourself and
   chat goes crazy."

### Recommended weekly cadence (explicit schedule)
- **Day 1**: stream with replay buffer running, hit the save-hotkey on notable moments.
- **Day 2**: one **20–30 minute batch session** in Nexus Clips — import everything, reframe,
  caption, export, all clips in one sitting.
- **Days 3–7**: post **one clip per day**, pre-scheduled.
- Framed explicitly as an algorithm-consistency play: "the other half... is being consistent
  enough to where **the algorithm actually starts pushing you**."

### Numbers mentioned (from the creator's paid community/students, not the tool itself)
Referenced (not independently verified, stated as anecdote): students in his private Discord
reportedly hitting "**over 150,000 views in the first 2 days**," reaching Twitch Affiliate, or
getting 30+ concurrent viewers on first streams.

### Analytics-feedback / self-adjustment content
No mention of checking real post-publish metrics to adjust future clips. The "3 types" and
hook-length/subtitle-placement rules are presented as the creator's general accumulated
best-practice knowledge, not as output of a measured analytics loop. The "algorithm pushing
you" claim is about **posting-consistency** driving algorithmic distribution, not about
content-style adaptation from data.

---

## 6. "AI-Powered Viral Clips – 100% Automated, No Editing!"
**Channel:** Stephen G. Pope | **URL:** https://www.youtube.com/watch?v=Yb01G77xscQ
**Length:** 70:08 (4,208s) | **Views:** ~18,065 | **Confidence: [verified]** (full transcript
of all ~2,000 caption lines + full description read)

**By far the most technically deep and directly reusable video of the 9** — a complete,
from-scratch, no-code (Airtable + Make.com) build of a self-hosted AI clipping pipeline using
a free/open-source video-processing API. This is a full architecture blueprint, not just tool
recommendations.

### High-level pitch
Build "at a fraction of the cost" of paid services like **Opus Clip** (named directly as the
cost comparison target), turning long-form podcast/YouTube video into "hundreds of viral
videos completely automated," with face-detection-driven auto-crop and auto-captioning.
Creator calls his demo system "**Content Clip Magic**." Free companion resources: Airtable
template + link list at
`https://www.skool.com/content-academy/ai-powered-viral-podcast-clips100-automated-no-editing`,
and his paid community at **`no-code-architects.dev`** ("No Code Architects Community") which
provides pre-filled Make.com blueprint imports, an Airtable/Make beginner course, a business
course, and near-daily live support calls.

### Full tool/service stack named
- **Airtable** — the system's database (tables: `Videos`, `Clips`; views used as pipeline
  gates, e.g. "Generate Transcript," "Generate Clip Scripts," "Crop Clip," "Caption Clip").
- **Make.com** (formerly Integromat) — the workflow/automation orchestrator; scenarios built
  per pipeline stage.
- **NCA Toolkit** ("No-Code Architects Toolkit") — a **free, open-source** API (Docker image
  distributed via **Docker Hub**) that provides transcription, FFmpeg-based cut/crop/scale,
  and burned-in captioning, self-hosted so you pay only for server compute rather than a
  monthly SaaS fee.
- **DigitalOcean App Platform** — used to host the NCA Toolkit container. Explicitly preferred
  over **Google Cloud** (which the creator normally uses / runs two instances of) because
  Google Cloud **times out on very long videos**, whereas DigitalOcean does not have that
  limitation. Cost stated: **~$50/month** for the server tier he used in the demo (explicitly
  says you can go cheaper/smaller, and can spin the server up for a day or two of testing and
  delete it before being billed the full month).
- **DigitalOcean Spaces** — S3-compatible object storage bucket, used to store
  transcripts/clips generated by the pipeline for download.
- **Postman** — used to manually test the NCA Toolkit API endpoints (an `/authenticate` check
  and a transcription smoke test) before wiring it into Make.com; a pre-built Postman
  collection link is provided in the description for viewers to duplicate.
- **Claude (Anthropic)**, model **"Sonnet"** — used for the clip-selection/extraction step
  (see below). Max tokens set to **3,000**.
- **ChatGPT (OpenAI)**, models **"4o-mini"** and **"4o"** — used for (a) converting Claude's
  free-text clip output into strict JSON, and (b) parsing the Vision-analysis text response
  into strict JSON.
- **ChatGPT-4 Turbo Vision** ("analyze images" module) — used for face-position detection on
  clip thumbnails for smart vertical cropping. Creator notes this was **the only model that
  worked reliably** for him for this specific sub-task; other models he didn't fully test, and
  even GPT-4 Turbo occasionally refused ("I can't actually find the coordinates of a face") —
  handled by simply ignoring/skipping failed individual clips since the pipeline is built to
  generate large volumes anyway.

### End-to-end pipeline (five chained Make.com automations)
1. **Add a video row** in Airtable (`Videos` table): description, source video link
   (link/URL), source video width×height, and the desired output clip width×height.
2. **Automation 1 — Transcribe**: Airtable search trigger (polling; creator notes a
   proper Airtable-native "instant trigger" would be better but is more complex to set up)
   → HTTP module calls NCA Toolkit's transcription endpoint (`/media/transcribe`, via
   `Make an API key auth'd request`) with the media URL + row ID + a **webhook callback URL**.
   The webhook pattern is used specifically because **Make.com scenarios time out after 5
   minutes**, so a long transcription job runs async on the DigitalOcean server and calls
   back into an **Airtable-native automation** (a webhook-triggered Airtable automation, not a
   Make scenario) when done, writing the resulting **transcript text URL** and **SRT file
   URL** back into the row. A `total bundles > 0` filter guards the trigger so it doesn't fire
   on empty search results.
3. **Automation 2 — Identify/generate clips**: downloads the transcript and SRT files (HTTP
   Get a File), converts the binary to string (`toString()`), and sends the full transcript to
   **Claude (Sonnet)** with a system prompt: *"You are a video editor tasked with looking at a
   video and pulling out shorter clips from a longer video but that those clips still make
   sense and are enjoyable to watch."* The user prompt asks for **5 unique clips, each roughly
   1–2 minutes / ~100–300 words**, each independently meaningful and delivering complete
   value, plus a sample output format. Claude's free-text result is then passed to **ChatGPT
   4o-mini** to be converted into strict JSON: `{clips: [{clip: "...", description: "4-5 word
   auto description"}]}` (response format explicitly set to JSON object + auto-parsed).
   - **Deterministic vs. AI design decision (explicitly stated as a lesson learned)**: the
     creator originally tried to have an LLM also locate each clip's exact start/end position
     within the SRT file, but found this **unreliable** — "sometimes it would work, sometimes
     it would just give me the wrong answer" — and switched to **plain regex/string matching**
     (Make's built-in `substring()`/`length()` functions plus three chained "Match Pattern
     (Advanced)" text-parser modules) to find the SRT segment numbers containing the clip's
     start and end text, then extract the exact SRT chunk between them. Direct quote:
     **"there's good times to use AI and there's also good times when to use something more
     deterministic."**
   - New rows created in the `Clips` table with clip description, clip text, and the matched
     SRT chunk; a separate **native Airtable automation** ("detect start/end time") then
     calculates exact start/end/duration timestamps from that SRT chunk automatically.
   - **Implicit quality-control side effect noted**: because each automation module only
     fires if the previous one succeeded, asking for 5 clips sometimes yields only 3 clips in
     Airtable — the creator explicitly frames this as *desirable* self-filtering ("this is to
     ensure the quality of the final clip... if you want more clips you can run this as many
     times as you want").
4. **Automation 3 — Cut the clips**: Airtable search (view "cut clips") → single HTTP POST to
   NCA Toolkit's **`/v1/ffmpeg/compose`** endpoint with the row ID, the master video file URL,
   the clip's start time + duration, and a webhook callback → NCA toolkit cuts the exact
   sub-clip from the master file and posts the resulting clip URL back via webhook.
5. **Automation 4 — Smart vertical crop**: NCA Toolkit auto-generates a **thumbnail** for each
   cut clip; that thumbnail URL is sent to **OpenAI's Analyze-Image (Vision)** module with a
   prompt asking for (a) the image's height/width and (b) the **X/Y coordinates of the center
   of the subject's face**. A second ChatGPT (4o) call reformats that analysis into strict
   JSON `{width, height, x, y}`. Airtable is updated with these "assessed" values, which feed
   **pre-built Airtable formulas** computing final `crop_x_width`, `crop_y_height`,
   `clip_left_x_width`, `clip_top_y_height` — explicitly built to handle the edge case where
   the subject is near the frame edge and there isn't enough room for a full vertical crop.
   A second NCA Toolkit **`/v1/ffmpeg/compose`** POST then performs the actual crop+scale from
   the source resolution (demoed at 1920×1080) up/out to the vertical target (1080×1920),
   using the calculated coordinates.
6. **Automation 5 — Auto-caption**: Airtable search (view "caption clip") → single HTTP POST
   to NCA Toolkit's **`/v1/video/caption`** endpoint with the cropped clip's URL, caption
   style settings (font size, bold, etc.), row ID, and a webhook → captions are burned in and
   the finished clip URL is written back to Airtable — pipeline complete.

### Concrete technical/config gotchas explicitly called out (useful if replicating)
- NCA Toolkit environment variables required: `API_KEY` (underscore not dash, **no leading/
  trailing spaces**) plus three more to connect to DigitalOcean Spaces: `S3_ENDPOINT_URL`,
  `S3_ACCESS_KEY`, `S3_SECRET_KEY`.
- Repeated, emphatic warning: a stray space/character in the raw-JSON request-body fields is
  the single most common cause of **HTTP 400 "bad request"** errors — recommends stripping
  all spaces/newlines into one long unbroken JSON line to eliminate hidden characters.
- Recommends testing every stage first against a **9-second test video** before running the
  full pipeline against a real long-form file (creator notes full transcription of a longer
  video took **20–30 minutes** in his own test run).
- Notes you can monitor DigitalOcean App Platform's **Insights/runtime logs** to confirm the
  server is actually processing a request while waiting.
- General cost/scaling note: server response time is a function of paid tier size — a 2GB RAM
  DigitalOcean instance was "a lot slower" and degraded further under concurrent requests;
  there exist even-cheaper hosting configurations than what's demoed, not covered in this
  video.

### Analytics-feedback / self-adjustment content
**None.** This video is exclusively about the *generation* pipeline (transcribe → select →
cut → crop → caption). It does not touch distribution, scheduling, or any post-publish
metrics loop at all.

---

## 7. "Best AI Video Editing Tools in 2026 (Don't Choose Wrong)"
**Channel:** Youri van Hofwegen | **URL:** https://www.youtube.com/watch?v=OHODMrUZlpo
**Length:** 24:42 (1,482s) | **Views:** ~313,140 | **Confidence: [verified]** (full transcript
+ full description read)

**This video contains the single most important analytics-feedback finding across all 9
videos.** A head-to-head comparison of four AI editing/clipping tools — **Captions.ai**,
**VEED** (transcribed inconsistently as "Vit"/"Veed" but confirmed via description as VEED —
"Opus Clip vs VEED vs Submagic vs Captions.ai"), **Submagic**, and **Opus Clip** — scored
across four categories: ease of use, editing, repurposing, and price. Sponsor/affiliate link:
`youricreates.com/opus`.

### Captions.ai
- Feature set: Mirage Studio + "AI Creator" (avatar generation, not covered in depth), an
  **AI editing tool**, and an **AI Shorts** feature (upload a video or paste a link →
  automatically generates short clips). **AI Shorts only supports YouTube links** (no other
  platform ingestion). The **AI edit tool only accepts vertical-format source video** — a
  real limitation, meaning it templatizes/tailors already-vertical footage rather than doing
  general horizontal-to-vertical editing.
  - Generated **5 clips of ~30 seconds each** in the repurposing test; reviewer's critique: no
    visible sorting/ranking mechanism between generated clips, and "besides the first clip, I
    don't really see a lot of strong hooks that the AI filtered out."
- Scores: Ease of use 5/5, Editing 2/5, Repurposing 3/5, Price 2/5.
- Pricing: **$10/month** entry tier (very limited — "pretty much the only thing you get is
  access to viral caption styles"); realistically need the **"Max" plan at $25/month**.

### VEED
- Magic Tools: clean/remove background noise, **remove filler words**, **remove silences**,
  **Magic B-roll** (auto-inserts contextually relevant stock images/video matched to spoken
  topic), face-appearance touch-up, eye-contact correction, background removal/green-screen,
  **"Magic Cut"** (automatically removes "ums," "uhs," and bad takes).
  - **AI Clips feature explicitly rates each generated clip on 4 named axes: "flow, hook,
    interest, and engagement"** and lists/sorts clips by that combined rating. Reviewer's
    explicit critique: **"I wouldn't say I agree with how they rated them... I wouldn't give
    some of these clips as high a score as they did"** — flagged as a scoring system that
    exists but that the reviewer judges as not very accurate/trustworthy.
  - Also supports both vertical and horizontal source ingestion (unlike Captions.ai).
- Scores: Ease of use 4/5, Editing 4/5, Repurposing 3/5, Price 2/5.
- Pricing: **Light $20/month** (no watermark removal beyond basics, limited upload size — "a
  little" flexible); realistically most users need **Pro at ~$50/month** for better export
  resolution, more caption languages, and the AI Clips feature itself.

### Submagic
- Feature set: auto-generated transcription on ingest, remove silences/bad takes, Brand tab
  (custom image/text overlays), caption style presets (reviewer used a **"Hormozi"-style**
  preset — i.e., the large bold word-highlight caption style popularized by Alex Hormozi
  content), **"Magic B-roll"** (secondary supporting images/video) + **"Magic Zooms"**
  (automated dynamic zoom-in effects timed to speech/emphasis), an AI button bundling
  eye-contact correction + audio cleanup, and **"Magic Clips"** — the auto-repurposing feature
  (long-form → multiple shorts).
  - Reviewer's explicit take on Submagic's scoring: **"I actually find Submagic's rating
    system to be more accurate than VEED's. It feels more real in terms of how it judges the
    clips"** — but also notes a real weakness: **"a lot of clips are basically the same thing,
    just slightly trimmed differently... that kind of kills the whole point of generating a
    lot of different options."**
- Scores: Ease of use 5/5, Editing 3.5/5, Repurposing 4/5, Price 3.5/5.
- Pricing: **Starter $19/month**, but the **Magic Clips add-on is another $19/month on top**
  — real all-in cost **≈$38/month** for full repurposing capability.

### Opus Clip — the standout for analytics-feedback specifically
- **Supports many more source-link types than the other three**: YouTube, Rumble,
  **Twitch**, and even Zoom recordings — directly relevant to Twitch-clipping use.
- **"You've got analytics, so you can actually connect your accounts and see how your clips
  are performing. That means you're not just making content blindly. You can check what's
  working and adjust."** — an explicit, named **connected-account post-publish analytics
  dashboard** used for manual creator feedback/adjustment.
- **Calendar/auto-posting**: upload a finished clip, pick a date, Opus **automatically posts
  it for you** — described as "a big time saver, especially if you're posting across multiple
  platforms."
- **"Viral score" is explicitly stated NOT to be a generic/random heuristic**: **"This isn't
  just a random metric. It's based on actual performance data from other videos through
  their analytics tool. So it's way more trustworthy than what we saw on VEED."** This is a
  direct, named claim that Opus Clip's scoring model is calibrated against **real aggregate
  cross-user/cross-video performance data** collected via its own analytics product — the
  clearest "the tool's own recommendation engine is trained on real outcome data" statement
  found in any of the 9 videos.
- Also: doesn't naively over-generate — **"it actually checks how many good clips it can
  realistically pull from your video without filling it with duplicates."**
- AI enhancement features: remove filler words, remove pauses, profanity censoring, **speech
  enhancement** (vocal clarity/richness), **"Tracker"** (keeps the active speaker centered in
  frame automatically even if they physically move out of frame in the source horizontal
  video — an auto-reframing/tracking-crop feature distinct from a one-time static crop),
  **autogenerate stock B-roll** vs. **autogenerate AI B-roll** (two distinct modes — stock
  library footage vs. AI-generated footage), **autogenerate AI hooks** (adds a natural AI
  voice-over hook in a chosen language at the start of a clip if it doesn't already have a
  strong hook), auto emojis, auto transitions (crossfade/cross-zoom/zoom-in, previewable),
  **speaker-color coding** (highlights whichever of multiple speakers is currently talking),
  many caption style/font/position options, and **XML export** for continuing the edit in a
  professional NLE, or direct HD export.
- **"Trending topics"** feature mentioned as an extra differentiator (not elaborated in
  depth) contributing to Opus's top repurposing score.
- Scores: Ease of use 4/5, Editing 4.5/5, **Repurposing 5/5 (category winner, explicitly "not
  by a little")**, Price 4.5/5.
- Pricing: **Starter $15/month** (called "already solid... more than enough" for most people),
  **Pro $29/month** for ~300 minutes of processed video per month, with the ability to buy
  additional credit blocks rather than being forced onto a bigger fixed tier.

### Overall verdict
Opus Clip wins overall across every category tested, explicitly credited to (a) the
connected-analytics/adjust-based-on-data workflow, (b) the performance-data-calibrated viral
score, and (c) auto-posting/scheduling, combined with the most generous and flexible pricing
of the four.

### Analytics-feedback / self-adjustment content
**This is the strongest, most explicit finding in the entire 9-video set.** Opus Clip is
described as having (1) a connected post-publish analytics dashboard that lets a creator
"check what's working and adjust," and (2) a virality-scoring model explicitly stated to be
trained/calibrated on **real aggregate performance data**, not a static heuristic. VEED has a
comparable but reviewer-distrusted per-clip scoring system (flow/hook/interest/engagement)
with no claimed connection to real performance data. No tool in this video does *automatic*
style/topic adjustment based on analytics — the loop described for Opus is still creator-in-
the-loop ("you can check... and adjust"), not autonomous.

---

## 8. "How to Become a Clipper: Learn How to use Free Video Tools"
**Channel:** Headliner | **URL:** https://www.youtube.com/watch?v=gXXzimVa2A8
**Length:** 12:32 (752s) | **Views:** ~1,419 | **Confidence: [verified]** (full transcript +
full description read)

Official tutorial from **Headliner** (`make.headliner.app`, free account) demonstrating the
**"clipper for hire" side-hustle economy** using the **Vyro** clipping-campaign marketplace
platform in tandem with Headliner's free editing tool. This is the clearest walkthrough of the
*campaign/marketplace* side of clip-farming (complementary to Video 9's Discord-community
version of the same economy).

### Vyro marketplace mechanics (as demoed)
- Sign up, browse **active campaigns** (demoed: a "Huge Conversations" podcast campaign
  featuring **Cleo Abrams**), join a campaign, and the campaign provides the **raw source
  content to clip** (in the demo: a full ~1-hour podcast video file) plus a **required
  end-card/outro** asset that must be appended to every submitted clip.
- Each campaign has its **own explicit rules** that must be followed to qualify for payout —
  concrete examples shown: mandatory caption text ("Watch [X] interview"), mandatory channel
  tag, **required hashtags**, mandatory **disclosure of affiliation**, and a **minimum video
  length** requirement.

### Headliner editing workflow
- **"Video podcasting"** entry point, two modes: **Multi-Clips flow** (fully automatic —
  generates **up to 10 clips per upload** in one batch, recommended by presenter for anyone
  treating this as a side-hustle since it's the fastest way to batch content) or **Single
  Clipping flow** (fully manual, for creators who already know their exact desired
  timestamps).
- Platform-aware output optimization: choosing "YouTube" as target offers **15-second,
  60-second, and 3-minute** clip-length presets, explicitly said to be **"leveraging the data
  that we have on YouTube Shorts engagement to ensure the clips are best optimized"** — i.e.
  Headliner claims its own length presets are informed by aggregate Shorts engagement data
  (a platform-level, not per-account, analytics claim).
- Template picker (or start from a blank canvas) → caption style auto-applied → **auto-framing
  enabled by default** ("ensures the active speaker will always be in frame") → optional
  intro/outro card upload (append the campaign-provided end-card to every clip) → cosmetic
  presets (e.g. "karaoke" caption animation style) → **"Get your clips"** → fully async
  background processing, **completion notified by email** (no need to wait on-screen).
- Post-processing: clips appear under a Projects tab; can be individually fine-edited
  (captions, in/out points) — explicit warning that **some campaigns prohibit editing their
  provided source** entirely since it's already pre-edited/approved, so read each campaign's
  rules before touching anything.
- Direct example of a manual caption fix: correcting a mis-transcribed proper noun ("Monte
  Carlo Tree Search") in the auto-generated transcript, which triggers **automatic
  reprocessing** of the video with the corrected caption.
- Export options: **bulk "Export All"**, or **native scheduling** inside Headliner (three-dot
  menu → Share → schedule) — requires a one-time account-linking/verification step per
  destination platform. Scheduling flow auto-suggests an **AI-generated, SEO-optimized
  title**, can auto-generate a caption/description (though the presenter notes campaigns often
  already dictate exact required captions), supports adding videos to a **playlist** (useful
  for organizing by campaign) and re-adding any campaign-required **tags**.
- **Explicit anti-flagging advice**: don't mass-post a large volume of content quickly on an
  account with little posting history — "you can pretty easily get your account flagged" —
  recommends scheduling output out over time instead. Also notes some campaigns impose their
  own **daily content-volume caps**.

### Analytics-feedback / self-adjustment content
One platform-level claim (Headliner's YouTube Shorts length presets are informed by
"data... on YouTube Shorts engagement") but no creator-facing analytics dashboard or
post-publish feedback loop is shown or discussed in this video.

---

## 9. "How To Make Money with AI Clipping"
**Channel:** OpusClip (official) | **URL:** https://www.youtube.com/watch?v=IunLg0FY5hY
**Length:** 10:45 (645s) | **Views:** ~117,649 | **Confidence: [verified]** (full transcript +
full description read)

Official Opus Clip channel video framing clipping explicitly as a **paid side-hustle/
monetization economy** ("Whop Clipping" is named as one branded variant of this economy — the
description explicitly says "If you've heard of Whop Clipping then you've already heard of
one type of AI clipping, but that isn't the only way to start clipping"). This is the richest
video of the 9 for **concrete payout economics** of the clip-farming ecosystem.

### Payout economics (concrete numbers stated)
- Typical range: **$0.50–$2 per 1,000 views**, depending on the specific community/campaign.
- Named example campaign paying **$3 per 1,000 views** but with a **hard $3,000 campaign
  budget cap** — of which $400 had already been claimed by other clippers at time of filming,
  leaving only $2,600 available regardless of how viral any individual clip goes (an important
  mechanic: campaigns are budget-capped pools, not unlimited per-view payout).
- Named example: **Emma Chamberlain podcast campaign paying $60 per 1,000 views** (accessed
  via a Discord clipping community) — explicitly called out by the presenter as unusually low
  reward-per-view despite the high-profile source ("It's not that much, but let's use this as
  an example" — appears to be a transcription/speech quirk since $60/1,000 views would be
  extraordinarily high relative to the other examples given; taking the raw transcript at face
  value as instructed).
- Anecdotal high-end figures cited (attributed to an outside video, not independently
  verified by the presenter): **top clippers reportedly earning $20,000–$30,000/month**;
  reference to a video where streamer **Adin Ross** stated his **top clippers earn over
  $200,000/month**; the platform **Kick** is stated to have paid out **over $2 million** in
  clipping-program funds total.
- Concrete Discord-community campaign examples shown: a streaming campaign requiring
  **minimum 100,000 views for payout eligibility** (called "quite high" by the presenter); on
  the "**Clip Money**" Discord, three different active campaigns shown paying **75 cents per
  1,000 views** with budget caps of **$2,800**, **$7,000**, and **$3,500** respectively.
- Named clipper communities/marketplaces to join: a general **"Clipping"** Discord server
  (campaigns organized by category: streaming, podcast, music, brands, misc.) and
  **"Clip Money"** Discord (requires linking your accounts, then browse active campaigns with
  visible payout rate + budget cap + platform requirements). Explicit progression path
  stated: build a track record in these open/public communities first, since **the highest-
  paying private communities are invite-only for clippers who already have a proven track
  record**.

### Opus Clip workflow specific to campaign clipping (as demoed)
- **"Clip Anything"** — free-text prompt-driven clip extraction (same conceptual feature as
  NexusClips' "generate new moments" in Video 2): demoed against an Emma Chamberlain podcast
  by prompting for **"all her personal controversial opinions"** specifically, because that
  content type is believed likely to go viral.
- **Brand template builder**: aspect ratio selection (demoed 9:16), caption style/font
  picker, and a **logo/watermark overlay** placement tool — used specifically to satisfy a
  campaign's required-watermark rule (dragged into the top-right corner in the demo) and a
  visible **"safe zone" box** showing where overlay elements will/won't render across
  platforms.
- Any source link type accepted: **YouTube, Google Drive, Twitch, Kick, Rumble**, or direct
  upload.
- Processing time stated: **roughly 10 minutes** for a full podcast episode ("get clips in
  one click").
- Yield example: a full Emma Chamberlain podcast episode produced **39 different clips** in
  one pass.
- Per-clip fine-editing shown: full transcript-level clip editor (add new clip sections by
  typing timestamps, click "add"), per-word caption color/highlight toggling, timeline
  **split** tool for manual cuts, **AI enhancer** to increase audio quality / remove filler
  words / remove pauses, and manual **B-roll** insertion.

### Analytics-feedback / self-adjustment content
No creator-facing analytics dashboard is demonstrated in this specific video (unlike Video 7's
description of Opus's connected-analytics feature) — this video is focused on the economics
and campaign-sourcing side, not the editing/analytics side of the same product.

---

## Cross-video patterns

1. **NexusClips appears independently across 3 of the 9 videos** (Videos 2, 4, 5 — all
   different channels/creators, two of them explicitly paid sponsorships), each time
   described with materially the same feature set: virality-index scoring (0–100), a
   free-text "find me X kind of moment" prompt feature, an AI-generated retention "hook"
   overlay, auto-captioning, a Twitch-name "sticker" branding overlay, auto-hashtag/caption
   generation claimed to be informed by "clips similar to yours that have done well," and
   built-in cross-platform scheduling with a content calendar. This is the single most
   independently-corroborated tool across the whole set.
2. **Opus Clip is the only tool in the set explicitly and repeatedly described as having a
   real connected-account, post-publish analytics dashboard** (Video 7) and a virality-
   scoring model **explicitly stated to be calibrated on real aggregate performance data**
   rather than a generic/static heuristic (Video 7) — this is the strongest single
   analytics-feedback finding in the whole batch. Opus Clip is also the only compared tool
   that natively ingests Twitch links directly (Video 7) and is separately shown/recommended
   for the Twitch-VOD clip-farming use case in Video 9 (official Opus Clip channel).
3. **"Hook" as a retention lever is named independently by four different sources**
   (NexusClips/Video 2, NexusClips-user/Video 4, Nexus-Clips-via-Cpaws/Video 5's "3–9 word"
   rule, and Opus Clip's "autogenerate AI hooks" voice-over feature in Video 7) — clearly a
   convergent, cross-tool-vendor best practice, though only Video 4 explicitly frames it in
   causal "retention-based" language from the creator's own mouth.
4. **Auto-hashtag/caption generation "based on what similar clips have done well" is claimed
   by two independent tools** (NexusClips in Videos 2 & 4; Headliner's Shorts-length presets
   in Video 8, and implicitly Opus Clip's viral score in Video 7) — i.e., multiple vendors
   market a "the tool learned from aggregate cross-user outcome data" positioning, though none
   of the 9 videos show or describe a *per-individual-creator* feedback loop (i.e., "your
   channel's own view/retention history changes what the tool does for you next").
5. **Vertical-format smart-cropping via face-detection is a convergent technique** implemented
   three separate ways: NexusClips' one-click auto-reframe (Videos 2 & 5), Opus Clip's
   "Tracker" continuous face-following crop (Video 7), and — most technically detailed — the
   custom GPT-4-Vision-driven X/Y-coordinate detection + Airtable-formula-driven crop
   calculation in the from-scratch NCA Toolkit build (Video 6).
6. **Chat-based signal is used as a highlight-detection proxy in two independent contexts**:
   Video 3's explicit chat-keyword/emote-triggered auto-clip system (the closest thing in this
   set to true real-time "chat-spike detection"), and Video 5's "best reaction clip" heuristic
   ("your chat was going crazy before you even processed what happened — they clipped it
   before you did").
7. **OBS-based capture is the common denominator for the live-recording layer** across the two
   most build-oriented videos: Video 3 uses OBS + the free **Aitum Vertical** plugin +
   **Streamer.bot** for a fully automated, zero-click, chat/event-triggered live pipeline;
   Video 5 uses plain **OBS Replay Buffer** (a simpler, manual-hotkey, single-button
   alternative requiring no plugins or bot software) feeding into NexusClips for editing.
   These represent two different sophistication tiers of the same "capture layer" problem —
   worth studying as a fully-automated-vs-simple-manual-trigger tradeoff.
8. **The self-hosted/open-source alternative to all the paid SaaS tools is the NCA Toolkit**
   (Video 6) — a free, Docker-deployable FFmpeg+transcription+captioning API that, combined
   with Airtable + Make.com + an LLM (Claude or ChatGPT) for clip selection, replicates most
   of what NexusClips/Opus Clip/Submagic do as paid products, at server-hosting cost only
   (~$50/month DigitalOcean instance in the demo, admitted to be reducible further). This is
   the most directly buildable blueprint in the entire set for a from-scratch "automated
   clipper bot."
9. **Distribution/cross-posting automation is a separate, distinct product category** from
   clip generation/editing — Repurpose.io (Video 1) does *only* distribution (Twitch → any
   platform, on a schedule or fully automatically) and explicitly has zero clip-selection or
   editing intelligence; it would sit downstream of any of the generation tools above in a
   full pipeline.
10. **The clip-farming "gig economy" (get paid per-1,000-views to clip someone else's
    content) is a distinct monetization model** covered in real depth by two videos (8 and 9)
    independently, both naming Discord-based campaign marketplaces (Vyro in Video 8; a
    general "Clipping" server and "Clip Money" in Video 9) with materially the same mechanics:
    join a campaign, follow campaign-specific branding/hashtag/caption rules, submit clips
    from provided source material, get paid per view up to a hard campaign budget cap, and
    graduate into higher-paying invite-only private communities once you have a track record.
    This is directly relevant if the "automated clipper bot" project intends to monetize by
    clipping *other people's* Twitch streams rather than (or in addition to) a single
    creator's own content.
