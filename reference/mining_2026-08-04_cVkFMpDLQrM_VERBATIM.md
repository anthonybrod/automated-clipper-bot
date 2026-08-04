# VERBATIM AGENT MINING REPORT — cVkFMpDLQrM

- **Source file:** `C:\Users\AwBro\Desktop\automated clipper bot\research\transcripts\cVkFMpDLQrM.txt`
- **Video ID:** `cVkFMpDLQrM`
- **Title (line 1 of file):** `# Lacy's Best Streamer University Moments`
- **URL (line 2 of file):** `https://www.youtube.com/watch?v=cVkFMpDLQrM`
- **Date of report:** 2026-08-04
- **Type:** Verbatim agent report. Quotes are word-for-word from the transcript file. Project Rule 15 applies — nothing below is paraphrased or condensed. Raw quotes are kept separate from interpretation; interpretation is always in a block explicitly labelled **INTERPRETATION**.
- **Read status:** Full file read end to end, all 1,070 lines.

---

## METHOD NOTE (read before using any number in this report)

Measured facts about the file, produced by counting, not by estimating:

- **1,068 timestamped caption lines**, first `[00:00]`, last `[35:39]` (2,139 seconds of compilation).
- **Gap distribution between consecutive caption timestamps** (seconds → count):
  `0→61, 1→418, 2→348, 3→120, 4→51, 5→31, 6→17, 7→6, 8→2, 9→5, 10→3, 11→1, 12→1, 14→1, 16→1, 18→1`
- **Non-speech tags present and their counts:** `[screaming] ×17`, `[laughter] ×13`, `[snorts] ×4`, `[applause] ×3`, `[cheering] ×2`, `[clears throat] ×2`, `[cough] ×1`.
- **Censored-profanity tokens:** `93` occurrences across `86` lines. (In the raw file the token is bracket + NBSP + two underscores + NBSP + bracket; rendered throughout this report as `[ __ ]`.)
- **Fully-capitalised caption lines:** `89`, forming `46` contiguous ALL-CAPS runs.

**How segment boundaries were derived.** The `[MM:SS]` marks in this file are **caption cues on the compilation's own single continuous 0:00–35:39 timeline** — they are *not* clip boundaries, and the gaps between them are not clip durations (median gap is 1–2s). Segment boundaries below were therefore derived by me from **content shifts** (new location, new cast, new premise, new bit) while reading, then timestamped to the caption cue where the new content starts. Boundaries are my judgement; the timestamps and quotes at those boundaries are literal from the file. Where a boundary was ambiguous I say so inline.

---

## A. COMPLETE / PORTABLE CODE

**NOTHING FOUND.**

Searched the full text for `ffmpeg`, `python`, `api`, `script`, `github`, `install`, `pip`, `npm`, `http`, `.com`, `obs`, `render`, `encode`, `download`, `upload`, `whisper`, `yt-dlp`. The only URL in the file is the source URL on line 2. The only hits on `obs` and `edit` were inside ordinary words:

```
[02:44] JOBS.
[12:31] >> bro? You owe me. It's a $3,000 edition.
```

This is a raw entertainment compilation with no technical content. No code, commands, or tool configs are present.

---

## B. FIXABLE CODE

**NOTHING FOUND.** See section A — the file contains no code of any kind, broken or otherwise.

---

## C. FREE / UNUTILIZED TOOLS

**NOTHING FOUND in the spoken content.** No tool, product, service, or software is named anywhere in the transcript. Every hit on `free` was ordinary speech:

```
[05:49] free just cuz you [ __ ] up your [ __ ]
[07:51] feel free. Um we got a few minutes left.
[24:22] >> HEY YO, EVERYBODY SPAM FREE LACY.
```

---

## D. EFFICIENCY PATHS

**NOTHING FOUND in the spoken content.**

**One artifact-level observation, clearly labelled as mine and not as a claim from the video:**

**INTERPRETATION.** The transcript artifact itself carries two free signals that need no audio DSP and no model call, because they are already in the text YouTube hands you:

1. **The `[screaming]` / `[laughter]` / `[applause]` / `[cheering]` tags.** YouTube's auto-caption pipeline emitted 40 non-speech tags total in this file. They are free text markers for exactly the acoustic events Stage 3 wants.
2. **ALL-CAPS caption runs.** 89 of 1,068 lines (8.3%) are fully capitalised. Their positions cluster tightly around the `[screaming]` tags — e.g. the caps run `01:43–01:59` sits on `[screaming]` at `01:05` / `02:16`; the run `06:09–06:32` sits on `[screaming]` at `06:05` and `06:11`; the run `24:13–24:22` sits on `[screaming]` at `24:13`. Whether caps is a deliberate loudness marker or an ASR artifact is **not verified** and must be checked against a second transcript before being trusted.

**Not a fact. A lead to verify.**

---

## E. CORRECTIONS / GOTCHAS

**E1 — The task brief's premise about deriving clip length from timestamp gaps is wrong for this file.**
The brief said to "derive from the `[MM:SS]` gaps between moments." Measured, the gaps between consecutive caption cues are: 1s (418 times), 2s (348 times), 3s (120 times). These are ASR caption cadence, not moment boundaries. The compilation is one continuous timeline. **Anything that reads clip length off raw caption gaps will output ~1.5 seconds and be useless.** Moment length in a compilation must come from content-shift detection, not from timestamp arithmetic.

**E2 — Large timestamp gaps mark *non-verbal* action, not scene cuts.**
The 18 gaps of ≥8s are the file's silent stretches. Every one of them lands inside a physical-action bit, not at a topic change. The largest:

```
18s  21:31 -> 21:49
16s  23:51 -> 24:07
14s  20:09 -> 20:23
12s  08:40 -> 08:52
```

At `[20:09]` → `[20:23]` the surrounding lines are `>> There's a cart.` then `>> There you are.` — that is fourteen seconds of people wheeling a cart, no dialogue. **Gotcha: silence in a compilation is a positive signal (visual gag in progress), not a negative one.** A detector that prunes low-speech-density windows would delete the cart heist, the barricade build, and the arrest.

**E3 — Speaker attribution is unusable.**
The file marks turn changes with `>>` but never names a speaker. Many lines have no `>>` at all (e.g. `[09:04] I'm terrorizing homecoming.`, `[31:57] Are you a bully?`). **Do not build any Stage 3 rule that depends on knowing who is talking.**

**E4 — ASR mangles the subject's own name, constantly.**
Across the file "Lacy" is rendered as `Lacy`, `Lazy`, `Ly`, and `Acy`:

```
[00:04] Why you bouncing on Lacy? Okay, Lacy.
[22:24] lazy.
[23:44] Lazy. Let's go.
[24:45] Lazy wheelchair.
[25:37] >> Hold on. Wait. Wait. Acy,
[15:47] wait. Wait. Hold on. No. Ly. Ly. No. Ly.
```

**Any keyword search for the streamer's name must match `Lacy|Lazy|Ly|Acy` or it will miss roughly half the mentions.** `[06:41] >> LI.` is very likely a fifth spelling.

**E5 — Profanity is pre-censored in the transcript, so profanity density is still measurable but the words are gone.**
93 `[ __ ]` tokens. You can count intensity, you cannot read the word. Useful as a density signal; useless for semantic matching.

**E6 — ASR garbles the single biggest number in the file.**
`[11:18] >> I GOT TWO I GOT $1,000 ON HIS HEAD and I` / `[11:20] GOT,000 ON MY HEAD.` The second figure lost its leading digits entirely. **Numbers extracted from auto-transcripts are unreliable; do not let a money-amount regex drive a clip-worthiness score on its own.**

**E7 — The compilation opens on a scream, not on context.**
Line 4 of the file, the literal first frame of a professionally curated best-of, is:

```
[00:00] LET'S [screaming] GO.
```

There is no intro, no title narration, no setup. **The editor's first choice contradicts the common assumption that a clip needs establishing context.**

---

## F. DETECTION SIGNALS — FULL MOMENT CATALOGUE

50 moments. Every one is a positive example by construction (curated best-of). Format: ID, time range, derived duration, **verbatim** anchor quotes, then the observable signal.

### M01 — [00:00]–[00:01] — 2s — COLD-OPEN STING
```
[00:00] LET'S [screaming] GO.
```
Signal: `[screaming]` tag at t=0. Volume spike from silence.

### M02 — [00:02]–[00:30] — 29s — WHEELCHAIR WELCOME ROAST
```
[00:02] >> ALL RIGHT. SO, why are you bouncing on?
[00:04] Why you bouncing on Lacy? Okay, Lacy.
[00:09] >> I had to hop up the steps.
[00:12] Streamer You. We love, you know, handy
[00:14] the disabled people, bro. We do. And I
[00:19] want to hold monitor represent. It's
[00:24] you might I might gift you a new
[00:25] wheelchair with real like turbo boosters
[00:26] on it.
[00:27] >> Oh god.
```
Signal: rapid two-person overlapping banter, escalating absurd offer, reaction beat `>> Oh god.`

### M03 — [00:31]–[00:43] — 13s — LOCKER THREAT
```
[00:31] >> Hey, you ever been inside of a locker?
[00:33] >> You ever been pushed off that
[00:34] wheelchair?
[00:37] >> Lucky ass little kid, bro. Lucky lucky
[00:40] ass little. That lucky ass little, bro.
[00:42] I'll shove HIS ASS IN A LOCKER.
```
Signal: threat volley; caps spike on the punchline `I'll shove HIS ASS IN A LOCKER.`

### M04 — [00:44]–[01:07] — 24s — CHAIR-TIP THREAT / FORCED SUBMISSION
```
[00:44] >> ALL RIGHT, LACY, WATCH.
[00:45] >> NO, NOT YOU. NOT YOU. NO, NOT YOU.
[00:55] >> What happens if I push your chair over?
[00:56] >> No. No, no, no, no, no, no, Please,
[00:57] please, please, please, please.
[00:59] >> So, now you do what I say.
[01:04] >> yeah, that's what I thought.
[01:05] >> Whoa. [screaming]
```
Signal: **panic-repetition** ("No. No, no, no, no, no, no" + "please" ×5), then `[screaming]`. This repetition-under-threat pattern recurs 6 more times in the file.

### M05 — [01:08]–[01:34] — 27s — GUN ROBBERY IN DORM
```
[01:08] >> No, I'm not on nothing you want, G.
[01:14] >> MAN. PUT THAT GUN IN MY MOUTH.
[01:16] >> I'M A PEEP. I love you.
[01:19] >> Are you okay?
[01:20] >> Wait, WHAT ROOM YOU IN?
[01:24] >> 218.
[01:30] >> I love you, bro.
```
Signal: caps spike, hard tonal whiplash from threat to `I love you, bro.`

### M06 — [01:35]–[02:30] — 56s — POLICE / ACCUSATION SHOUTING MATCH
```
[01:35] >> Police. Police. Police.
[01:43] >> HEY, GET HIM. GET HIM. GET HIM.
[01:48] >> OFFICER, HE THREATENED ME. HE FRIED ME.
[01:50] >> GOT SOMETHING IN HIS LEFT POCKET.
[01:58] >> HE THREATENED ME. OFFICER. OFFICER. HE
[01:59] THREATENED ME.
[02:11] >> No. No. No. We got reports. We got
[02:13] reports of robbery. We need of robbery.
[02:16] >> DO YOURSELF [screaming]
[02:17] AROUND. HE ROBBED ME. HE ROBBED ME. WHAT
[02:21] DO I DO?
[02:23] WHERE'S THE GUN? WHERE'S THE GUN?
```
Signal: **longest sustained ALL-CAPS run in the file (`01:43`–`01:59`, 16s)** plus a second run `02:15`–`02:23` (8s), plus `[screaming]`, plus triple-repetition (`Police. Police. Police.` / `GET HIM. GET HIM. GET HIM.` / `WHERE'S THE GUN? WHERE'S THE GUN?`).

### M07 — [02:36]–[03:04] — 29s — BROKEN GUN / COPS SUCK
```
[02:36] >> No, they broke the gun.
[02:42] >> YOU GUYS YOU GUYS [ __ ] SUCK AT YOUR
[02:44] JOBS.
[02:45] >> WE ABOUT TO LOCK YOU UP.
[02:59] >> It's off forever. Leave him alone.
```
Signal: caps run `02:42`–`02:45`, censored profanity, insult punchline.

### M08 — [03:07]–[03:38] — 32s — HOUR OF WORK DESTROYED
```
[03:08] >> Bro, come on. Please. I just spent like
[03:09] an hour doing that. I just spent like an
[03:11] hour.
[03:15] >> Don't drop it. Don't drop it.
[03:20] >> Oh my god. Now I see how it feels.
[03:26] >> Turn my [ __ ] up, fat ass.
[03:35] THAT'S WHAT I THOUGHT. LIKE, YEAH,
```
Signal: begging-repetition, `Oh my god`, caps payoff `THAT'S WHAT I THOUGHT.`

### M09 — [03:39]–[04:10] — 32s — RUBY / SPIDER-MAN BACKPACK OF SNACKS
```
[03:39] >> RUBY.
[03:39] >> YO, [screaming]
[03:40] SAVE YOU, MAN.
[03:42] >> WE'RE LAGGING LIKE CRAZY, BRO. I need
[03:48] >> It's pouring rain. I heard you have
[03:50] snacks. I heard you have snacks. I got
[03:54] >> Oh my god, he has a Spider-Man backpack.
[03:55] Oh my god, I love Spider-Man. Locked in,
[04:01] >> Oh my god, you have so many sacks.
[04:02] >> Take whatever you want.
```
Signal: **`Oh my god` ×3 inside 8 seconds** — excitement/reveal marker. Plus `[screaming]` at the open.

### M10 — [04:11]–[04:49] — 39s — ALMOST RAN HER OVER / WATER-GUN CHASE
```
[04:11] >> YOU ALMOST ran her over.
[04:12] >> No, you almost ran over, weirdo.
[04:17] >> I'm talking that gun like I don't got
[04:18] water right here. Let's see how far you
[04:19] get.
[04:33] >> No. Okay. Please. OKAY.
[04:37] [screaming]
[04:43] >> THAT'S A LAUGH, MAN. DAD DOESN'T LAUGH.
[04:46] [screaming]
```
Signal: **two `[screaming]` tags 9 seconds apart**, plus a 22-second near-silent stretch of pure chase action (`[04:21] Yeah.` → `[04:26] See what happen` → `[04:31] everybody.`).

### M11 — [04:50]–[05:20] — 31s — SLUMBER PARTY ENTRY / "YOU HAVE TO KISS ME"
```
[04:50] >> Body tea, attitude tea, hair on fleek,
[04:53] everything.
[04:54] >> Can you do something to like prove that
[04:55] you're a body?
[04:56] >> You have to kiss me.
[05:02] >> You have to kiss me.
[05:07] >> Wow. You're in.
[05:09] >> Am I in too? My name is Yousef. Nice to
[05:19] >> OH MY GOD.
```
Signal: dare, repeated demand, `>> Wow.` reaction, then caps `OH MY GOD.` closer.

### M12 — [05:21]–[06:04] — 44s — TORN ACL / PE CLASS / MUKBANG
```
[05:21] >> Hey gang, what happened to you?
[05:23] >> Tore my ACL.
[05:33] >> Wait, so what do I do in PE class now?
[05:35] >> You watch.
[05:37] >> Can I do a mukbang instead?
[05:39] >> Uh, sure. Just make sure you bring me
[05:52] >> Uh I'mma tell on you.
[05:59] >> YOU GOT TO FIND OUT how
```
Signal: question-and-answer interview cadence; absurd request `Can I do a mukbang instead?` as the punchline.

### M13 — [06:05]–[06:40] — 36s — COACH "NO EXCUSES" / FOCUS CHANT
```
[06:05] >> NO EXCUSES. [screaming]
[06:09] >> COACH. I THINK I GOT AN EXCUSE.
[06:11] >> HEY. [screaming] HEY. HEY. WE DON'T MAKE
[06:13] EXCUSES.
[06:14] >> WE DON'T MAKE EXCUSES. COME [laughter]
[06:14] ON. GET BACK. GET BACK. GET BACK. GET
[06:15] BACK. GET BACK IN THE WHEELCHAIR.
[06:19] We're not MAKING NO EXCUSES.
[06:26] FOCUS. FOCUS.
[06:29] FOCUS. FOCUS. FOCUS. FOCUS. FOCUS.
[06:32] FOCUS. FOCUS. FOCUS.
```
Signal: **densest signal region in the entire file** — two `[screaming]`, one `[laughter]`, two caps runs (`06:09`–`06:15` = 6s, `06:22`–`06:32` = 10s), and `FOCUS.` repeated **10 times** in 6 seconds. If Stage 3 has one canary test case, this is it.

### M14 — [06:41]–[07:07] — 27s — MAX IN THE STUDIO / KISS ATTEMPT
```
[06:41] >> LI.
[06:45] What you got going on, bro?
[06:46] >> I just checked into my dorm, dude.
[06:49] >> Listen, let's hop in the studio. Max,
[06:52] are YOU DOING?
[06:54] >> MAX, NO. MAX. [screaming] MAX, PLEASE.
[07:00] >> This we going to be hell.
[07:02] >> If you you trying I'm out. This [ __ ]
[07:05] trying TO KISS ME.
[07:06] >> YO, WHAT?
```
Signal: name shouted 3× (`MAX, NO. MAX. [screaming] MAX, PLEASE.`), then a reveal, then a caps reaction `>> YO, WHAT?`

### M15 — [07:08]–[07:47] — 40s — FEET-CONTENT MONEY INTERVIEW
```
[07:08] >> UM, I'm not going to say no to the bag
[07:10] if it's right there. So, I did it. But I
[07:12] mean, I think it's a it's a crazy ass
[07:14] stigma, but I I don't really feel like
[07:29] done anything. What I post is what I
[07:31] post.
[07:31] >> Wait, so you was making a bag off just
[07:33] your feet?
[07:34] >> Yes.
[07:35] >> How much you make a month off your feet?
[07:37] I need to know. I'm not going
[07:46] >> My biggest month.
```
Signal: no shouting at all — **quiet confession/reveal**. Marked by `>> Wait, so...` + a one-word `>> Yes.` beat. Proof that not every curated moment is loud.

### M16 — [07:48]–[09:03] — 76s — CLASS DISRUPTION / THROWN OUT
```
[07:48] >> Uh pretty much if you guys have any
[07:55] >> Oh really? Lacy
[08:01] >> You rolled your fat ass in here
[08:04] 45 minutes late.
[08:05] >> You showed up literally 30 minutes late.
[08:10] >> Wait, the class is over already? Why is
[08:12] it so short?
[08:16] >> Short ass class. It was like 2 minutes.
[08:20] >> [ __ ] fat ass is rolling around campus
[08:31] >> Would you wheel your fat ass out of
[08:33] here?
[08:33] >> No.
[08:33] >> Please. I'm staying. I want to learn.
[08:40] >> you're here to learn. [applause]
[08:52] >> Consume food.
[08:53] >> I want to learn. I want to learn.
[08:55] [applause]
[08:56] >> Oh, he's clapping that. Over that. Over
[08:59] that. Really? Okay. [applause]
```
Signal: **the only `[applause]` in the file — all 3 tags, at `08:40`, `08:55`, `08:59`**. Also a 12s silent gap `08:40`→`08:52` (the applause playing out). Group-reaction audio is the marker here, not shouting.

### M17 — [09:04]–[09:51] — 48s — HOMECOMING ASK + REJECTION
```
[09:04] I'm terrorizing homecoming.
[09:11] >> Wait, dude. Yo, I asked everybody. I
[09:14] asked Chris. I asked Cuy.
[09:16] >> I asked Kai. Um, I asked a lot more
[09:19] people. I got no one at home coming. You
[09:24] >> I actually got like four albums right
[09:27] >> God damn, you're him. Wait. No.
[09:32] And I ain't going to lie, you just
[09:33] wouldn't be at the top of the list,
[09:34] buddy. You know,
[09:36] >> but respect respectfully though, hope
[09:44] [laughter]
[09:44] >> Would you would you go to homecoming
```
Signal: setup → rejection → `[laughter]` at `09:44`. Rejection-as-punchline.

### M18 — [09:52]–[10:30] — 39s — "EVIL UNIVERSITY" / "STAND UP THEN I'LL BE SCARED"
```
[09:52] >> really unfortunate for you, Ronald?
[09:58] >> It's evil ass world, bro. Evil
[10:01] University. This is evil. Take action.
[10:07] >> Because what people I strike fear into
[10:09] people. They're scared of me at this
[10:11] campus.
[10:19] >> Stand up then I'll be scared, [ __ ]
[10:21] >> If you can stand up, I'll be scared. You
[10:23] can't stand up.
[10:27] you to me. [screaming]
```
Signal: boast → brutal callback insult → `[screaming]`. Classic setup/punchline shape.

### M19 — [10:31]–[11:15] — 45s — DEAN CONFRONTATION → TRUCE
```
[10:31] >> I'M NOT bad at you though.
[10:39] >> Come on, Dean. Come on, Dean.
[10:50] man? You're the worst dean in the world.
[10:53] >> I thought you was bully. Come here.
[10:57] >> It's a truce. [laughter] I [ __ ] with
[10:58] y'all boys.
[11:00] >> Hey. Hey. This better keep it loose.
[11:04] >> THE [ __ ]
[11:05] >> [ __ ] MY [ __ ] [ __ ]
[11:09] WHAT THE ASS TO HIS ASS TO THE
[11:12] NEVERLAND.
```
Signal: conflict → `[laughter]` de-escalation at `10:57` → immediate re-escalation into a caps + 4-profanity burst at `11:04`–`11:12`.

### M20 — [11:16]–[11:32] — 17s — $1,000 BOUNTY
```
[11:16] Get the back everybody. I GOT
[11:18] >> I GOT TWO I GOT $1,000 ON HIS HEAD and I
[11:20] GOT,000 ON MY HEAD. HEY, I'MMA DOUBLE IT
[11:23] ON YOUR [ __ ]
[11:27] >> I GOT CASH ON ME RIGHT NOW.
[11:29] >> WHOEVER DO IT, I GOT $1,000. This
```
Signal: **money stated out loud + caps run + shortest non-sting moment in the file (17s)**. Money-on-the-line is a self-contained hook needing no setup.

### M21 — [11:33]–[12:24] — 52s — "Y'ALL GOOD?" / DEPRESSED / CAN'T CHASE YOU
```
[11:33] >> y'all good?
[11:36] >> Are y'all good?
[11:38] >> Hey, y'all good?
[11:43] >> No, I'm I'm just I'm just depressed,
[11:52] >> Hey, this is
[11:54] I can't chase you.
[11:56] I can't chase you.
[12:05] >> Dude, this is just bullying. I can't
[12:07] even get it.
[12:16] >> Serious? Are you serious?
```
Signal: `y'all good?` asked 3 times in 5 seconds; `I can't chase you.` twice; then a 9s silence `11:56`→`12:05`. Verbal repetition + long silence.

### M22 — [12:25]–[13:38] — 74s — $3,000 PHONE CRACKED / WORST DAY EVER
```
[12:28] >> YOU just cracked my phone.
[12:30] >> Do you have zel,
[12:31] >> bro? You owe me. It's a $3,000 edition.
[12:34] >> It's a $3,000.
[12:37] >> I'm so sorry. I'm I'm a
[12:44] >> Yes. I promise it was busted. Is my
[12:47] >> Won't turn on. Wait, won't turn on.
[12:50] >> Oh my god.
[12:51] I have to pay you now.
[12:58] >> Has I DON'T HAVE A PHONE.
[13:01] >> I'LL PAY YOU BACK. I'M BEING SO SERIOUS.
[13:02] LIKE [screaming]
[13:08] >> This has BEEN THE WORST DAY [screaming]
[13:10] EVER.
[13:11] >> OH, I'm getting getting been getting
[13:13] bullied. They stole my phone, put it on
[13:15] top of a lamp post, and it cracked. So,
[13:17] all I have is my chat phone. Look, you
[13:18] can see I'm not lying. I have no apps.
[13:25] seem like [ __ ] OH MY GOD.
[13:26] [screaming]
[13:32] [laughter]
```
Signal: **three `[screaming]` tags in 24 seconds (`13:02`, `13:08`, `13:26`) plus `[laughter]` at `13:32`** — highest tag density outside M13. Property damage + a dollar figure + escalating distress.

### M23 — [13:39]–[14:23] — 45s — EGO ACCUSATION / "WORST RNG EVER"
```
[13:39] >> Chad, it's not a e, bro. I don't have an
[13:41] ego. I don't You guys watch my phone
[13:44] break. Okay. What is it?
[13:45] >> Lacy. Ego. Small streamer. That's
[13:47] disabled and a cat girl.
[14:02] >> This timing like this is just the worst
[14:04] RNG ever. Come on. Just let me have a
[14:06] little snack. Come on. Just let me just
[14:08] let me have a little Dean. Come on. Just
[14:10] let me have a
[14:14] >> Have a nice day. Ly.
```
Signal: `Come on. Just let me` repeated 4× in 8 seconds — pleading-repetition. Ends on a dismissive kiss-off `>> Have a nice day. Ly.`

### M24 — [14:24]–[14:42] — 19s — "YOU STINK"
```
[14:24] YOU'RE NOT ON THAT. YOU'RE NOT ON THAT.
[14:27] >> YOU'RE NOT ON THAT.
[14:28] >> OH GOD.
[14:30] >> YOU STINK. YOU SMELL like [ __ ] now.
[14:39] [screaming]
```
Signal: entirely ALL-CAPS moment (caps run `14:24`–`14:28`), same phrase 3×, closes on `[screaming]` after a 9s action gap.

### M25 — [14:43]–[15:12] — 30s — DARK-ROOM INTERROGATION
```
[14:43] >> Did you lock him in a a dark room? Yes
[14:46] or no?
[14:46] >> No, you didn't put me in a corner of a
[14:48] room. Wait, was you said I locked you in
[14:49] the dark room?
[14:50] >> Yes.
[14:50] >> The light was on. That's how you know
[14:51] he's lying.
[15:02] >> I'M SORRY, GUYS.
[15:04] >> NO, NO, PLEASE.
```
Signal: **yes/no interrogation format**, one-word `>> Yes.` beat, then a technicality punchline `The light was on. That's how you know he's lying.` No shouting until the caps tail.

### M26 — [15:13]–[15:45] — 33s — STAGED KICK
```
[15:13] >> OKAY. HEY, LISTEN. LISTEN. Act like you
[15:15] kicked me and run the [ __ ] off.
[15:17] >> OH, [ __ ]
[15:19] >> OH, [ __ ]
[15:21] >> OH, [ __ ]
[15:26] >> Did you just let him?
[15:30] >> You're a little He kicked my bro,
[15:32] >> bro. He literally kicked my [ __ ]
[15:35] >> Crazy. I'm just trying to walk by.
[15:41] >> He's so lucky. I can't pick his little
[15:42] ass up.
```
Signal: **`OH, [ __ ]` three times in 5 seconds (`15:17`, `15:19`, `15:21`)** — a pure profanity-burst reaction cluster with almost no other words. Very machine-detectable.

### M27 — [15:46]–[16:23] — 38s — TRASH CAN
```
[15:46] [screaming]
[15:47] wait. Wait. Hold on. No. Ly. Ly. No. Ly.
[15:49] Oh. Oh [ __ ]
[15:55] >> And I'm going to PUT YOU IN A [ __ ]
[15:56] TRASH CAN. YOU UNDERSTAND, KID?
[15:58] >> WAIT. WATCH OUT. WATCH OUT. WATCH OUT.
[16:00] >> [ __ ] TRASH CAN. YOU UNDERSTAND, KID?
[16:02] >> You ever met us OUT OF A TRASH CAN?
[16:04] >> THIS [ __ ] KIND OF FUN.
[16:06] >> WAIT. WATCH OUT FOR MY KNEE, MAN.
[16:07] >> [ __ ] your knee.
[16:13] >> PUTTING YOUR LITTLE ASS INSIDE OF A
[16:16] TRASH CAN, KID.
[16:19] >> WAIT, is this the third This is the
[16:20] third time I seen.
```
Signal: **opens on a bare `[screaming]` tag with no words at all**, then three caps runs, `WATCH OUT` ×3, and the same threat line delivered twice verbatim.

### M28 — [16:24]–[17:13] — 50s — DOOR / CORNER CONFRONTATION
```
[16:24] >> GUYS,
[16:24] >> GET THE AWAY.
[16:26] >> GET THE HELP.
[16:32] >> GOOD WITH THE FIRST GUY.
[16:33] >> SHUT UP.
[16:34] >> SHUT UP. Shut up. Shut the [ __ ] up.
[16:40] >> BELIEVE HIM. OPEN THE DOOR. Open the
[16:42] door. Open the [ __ ] door. [screaming]
[16:55] >> All right, BRO. WAIT. WAIT. WAIT. WAIT.
[16:56] WAIT. WAIT. WAIT. WAIT. EASY.
[16:57] EASY. EASY. EASY. Sit down. Sit down.
[17:00] nowhere. Hey. Hey. Sit the [ __ ] DOWN.
[17:03] >> YES. NO. I LIKE THAT. Stay in that
[17:04] corner. STAY IN THAT [ __ ] CORNER. YOU
[17:06] LITTLE YOU WANT TO PUT ME IN THE CORNER
[17:08] IN A WHEELCHAIR? YOU.
```
Signal: **`WAIT.` ×8 and `EASY.` ×4 inside 3 seconds** — the densest single-word repetition burst in the file. Plus `SHUT UP` ×3, `Open the door` ×3, `[screaming]`.

### M29 — [17:14]–[18:02] — 49s — "ARE WE PLAYING HOME ALONE?"
```
[17:14] >> YO, I promise you,
[17:16] >> please. I want you to lock the door.
[17:17] >> Oh my god.
[17:19] >> Oh my god.
[17:25] Say sorry.
[17:26] >> I'm not say sorry.
[17:27] >> Oh, you're not saying sorry.
[17:32] >> Come try. Come try,
[17:36] >> Oh my god.
[17:38] Oh [ __ ]
[17:44] >> We all [ __ ] abuse a joke. Are we
[17:48] playing home alone? This little is a
[17:52] 14year-old beating the out of us more.
[17:56] >> What are you doing? You keep doing the
[18:00] >> Like he actually beat the nut. It's a
```
Signal: `Oh my god` ×3 in 22 seconds; four consecutive 4s silence gaps `17:44`→`17:56` (physical action); a stated-out-loud framing line `Are we playing home alone?`

### M30 — [18:03]–[18:31] — 29s — "HOW YOU AIM AND WALK?"
```
[18:03] >> Let me know if y'all need one.
[18:09] >> Out on the court.
[18:11] >> On the court. How you aim and walk?
[18:13] >> Ask me to walk.
[18:18] >> Oh, he on some scary movie [ __ ]
[18:28] >> Hey. Hey. I ain't going to lie. We might
[18:30] need that [ __ ]
```
Signal: quiet moment; punchline is the wheelchair callback `How you aim and walk?` A 10s silence `18:18`→`18:28`.

### M31 — [18:32]–[19:56] — 85s — CHICKEN TENDER COUNT / "UNLIMITED FOOD"
```
[18:32] >> How many chicken nuggets did we get? How
[18:34] many pops of chicken tenders? Okay.
[18:36] Okay. One,
[18:38] two,
[18:41] three,
[18:44] four,
[18:46] five,
[18:47] 6 7
[18:51] 8
[18:53] 9.
[18:56] Now empty the backpack.
[19:01] How many's in the backpack? How many's
[19:02] in the back?
[19:06] [cough]
[19:08] [snorts]
[19:18] >> Oh my god,
[19:22] there's so many more.
[19:27] Holy [ __ ] We have unlimited food. We
[19:30] have unlimited food.
[19:35] Wait, we need to keep one box.
[19:41] >> Okay. Okay. Okay. How many is that? 4 8
[19:46] 12 16 8. We have 20. We have 20. Okay.
[19:50] Now, the next thing we got to get Red
[19:52] Bull.
```
Signal: **counting-out-loud structure** — a natural built-in tension ramp with a reveal payoff (`We have unlimited food.` repeated). Also the only `[cough]` and one of four `[snorts]`. 85s long, one of the longest.

### M32 — [19:57]–[21:48] — 112s — CART HEIST / BARRICADE BUILD / POOL PARTY
```
[20:02] >> Wait. Oh my god. I have an idea.
[20:06] >> There there's a thing. Do you want to
[20:07] just grab the cart?
[20:09] >> There's a cart.
[20:23] >> There you are.
[20:37] Come on. Come on. Come on.
[20:49] >> Come on. Come on. Come on. Come on. Come
[20:51] on. Come on.
[20:53] >> Make a wall. Make a wall.
[20:56] >> Where's the pool party at?
[21:01] Hurry up.
[21:12] [clears throat]
[21:19] >> You guys need some electrical power?
[21:27] Oh my god.
[21:31] Oh my god.
```
Signal: **LONGEST MOMENT IN THE FILE — 112 seconds.** Almost no dialogue; carried by the 18s gap `21:31`→`21:49` and the 14s gap `20:09`→`20:23`. `Come on.` said 12+ times. Hook is the idea-announcement `Wait. Oh my god. I have an idea.`

### M33 — [21:49]–[22:37] — 49s — "DO I FIT?" / STEALING OBJECTS
```
[21:49] All right, let's go. Let's go.
[21:54] Do I fit?
[21:59] Hey, baby.
[22:01] >> Wait, how you did the [ __ ] is this fat
[22:04] ass just stealing objects, bro?
[22:08] >> I'm not going to lie. That wheelchair
[22:11] >> What the are you doing, bro?
[22:20] >> I got a microwave,
[22:25] >> What the [ __ ]
[22:31] >> THEY BROUGHT IT OUT.
[22:33] >> WHAT THE [ __ ] is that?
```
Signal: **`What the` disbelief reaction ×4** in 30 seconds. Absurd-object reveal (`I got a microwave,`).

### M34 — [22:38]–[24:06] — 89s — BARRICADE IN THE ROOM / CHICKEN
```
[22:43] [laughter]
[22:44] >> guys. Make those face. Make some space.
[22:47] >> What are we doing? What the hell are we
[22:49] doing? kick in [laughter] the back.
[22:51] >> What is going on?
[22:58] >> Watch out, boys.
[23:01] >> Watch yourself. Watch yourself. Watch
[23:02] yourself. Okay, we're going for you and
[23:17] >> Hold on. Let's see. Let's see. Let's eat
[23:19] the chicken smelling. [laughter]
[23:30] >> Sit down. Have a nice little
[23:30] >> Wait, wait. We got to move it. Okay. The
[23:31] door can't shut.
[23:44] Lazy. Let's go.
```
Signal: **three `[laughter]` tags** (`22:43`, `22:49`, `23:19`), `Watch yourself.` ×3, `What is going on?` bewilderment marker, 16s silence `23:51`→`24:07`.

### M35 — [24:07]–[25:13] — 67s — ARREST OF THE GUY IN THE WHEELCHAIR
```
[24:09] >> Why am I doing this?
[24:13] >> WHY AM I [screaming] UNDER ARREST?
[24:15] >> WATCH OUT. OH NO.
[24:17] >> You arrested THE DUDE IN THE WHEELCHAIR.
[24:18] >> DON'T GIVE A [ __ ]
[24:19] >> SO YEAH, I'M THE DUDE THAT PUT THREE
[24:20] PICNIC TABLES WHEN I CAN'T EVENING WALK.
[24:22] >> HEY YO, EVERYBODY SPAM FREE LACY.
[24:30] [ __ ] did I do?
[24:34] >> Hop a little harder. Hop a little
[24:36] >> Hop a little. Can I at least get my
[24:37] wheelchair?
[24:40] >> Hey, somebody get the wheelchair. Get
[24:48] >> Somebody get the wheelchair.
[24:54] >> They taking your ass to jail.
[24:57] >> Yo, THEY GOT HIM STANDING, BRO.
[24:59] >> HE CAN'T EVEN WALK, DUDE. That's [ __ ]
[25:02] >> I didn't even do [ __ ] Hey, they're
[25:05] >> WHAT? What are you doing?
[25:09] >> HEY. HEY.
[25:11] >> WHAT THE [ __ ]
```
Signal: `[screaming]`, three caps runs, `get the wheelchair` ×4, plus an **explicit chat CTA spoken on camera: `EVERYBODY SPAM FREE LACY.`** Injustice framing (`arresting A DUDE WHO CAN'T WALK.`).

### M36 — [25:14]–[25:56] — 43s — CHAIN / "CAN I PULL YOU AROUND?"
```
[25:14] >> what the [ __ ] is you want me to help
[25:22] >> No, I tore my hotel.
[25:26] >> NO. WHERE'S MY CHAIN? MY
[25:28] >> WAIT. Can Can I pull you around?
[25:30] >> Weird. I mean, you could try, but let's
[25:34] >> Okay. Okay. Ready? I guess we're going.
[25:34] [ __ ] [laughter] it.
[25:40] >> Yo, James, SHUT THE [ __ ] UP. MAYBE SOME
[25:43] FRIED RICE, [ __ ]
[25:44] >> MAKE ME SOME FRIED CHICKEN. SOME FRIED
[25:46] chicken fried chicken. GENERAL TO LIKE
[25:50] SHUT THE [ __ ] UP, [ __ ]
```
Signal: `[laughter]` at `25:34`, then a caps + profanity explosion `25:40`–`25:50` (5 censored tokens in 10s).

### M37 — [25:57]–[26:59] — 63s — DIET COACHING / PIZZA / SIX-PACK
```
[25:57] >> See, hold on. Let's take this pizza.
[25:59] See, look. This is your problem. Okay.
[26:04] >> Um, honestly, I want
[26:11] to get I want to get I want to get a
[26:12] six-ack.
[26:15] >> this got to go.
[26:17] >> Cheese, bread, crust. Not happening.
[26:25] >> Mac and cheese.
[26:26] >> Terrible.
[26:27] >> Protein, protein, vegetables. Good.
[26:33] >> but talking to Lacy, it's literally no
[26:34] point, gang.
[26:36] >> You know what? You know how sexy you
[26:37] will be if you locked in? Don't y'all
[26:39] got no fitness channel together?
[26:55] >> God damn. PUFF IT OUT, DEAN.
```
Signal: quiet, structured **verdict cadence** — item, then one-word ruling (`Terrible.` / `Good.` / `Not happening.`). Zero shouting until the caps closer.

### M38 — [27:00]–[27:38] — 39s — SECURITY BADGE
```
[27:00] >> Here go my security badge. Here go my
[27:02] security badge.
[27:03] >> What are you doing?
[27:05] >> Yo, back up, my [ __ ]
[27:11] sour [laughter]
```
Signal: `[laughter]` at `27:11`; three consecutive 5–7s silence gaps `27:05`→`27:23` (physical bit). Line repeated verbatim to open.

### M39 — [27:39]–[28:21] — 43s — TP ACCUSATION + FORCED RUN
```
[27:41] >> Okay. Can I confess something? You have
[27:30] >> wait a second. You TP my own campus.
[27:32] >> I did not TP the campus. I did not do
[27:34] that. That was not me.
[27:43] >> and I want to see you run down this hall
[27:44] and then run back.
[27:45] >> What? You want me to? Really? You want
[27:48] me to Okay. You want me to run down the
[27:52] >> to the water jug and run back?
[27:55] >> I should I hop?
[27:56] >> Run.
[27:57] >> I can't run.
[28:01] >> Yeah. There we go.
[28:04] >> No. This is torture.
[28:08] I came to snitch. I didn't come to to
[28:11] get in trouble.
```
Signal: denial-repetition (`I did not TP the campus. I did not do that. That was not me.`), then an impossible-order beat with a one-word refusal `>> I can't run.` and a labelled emotional payoff `This is torture.`

### M40 — [28:22]–[29:26] — 65s — LOCKED OUT / WHEELCHAIR DIED
```
[28:22] >> Where the [ __ ] did you come from?
[28:25] >> My mom's vagina.
[28:26] >> Okay, I understand that. But like
[28:36] >> You're clubbed everything. You getting
[28:38] locked out your goddamn room.
[28:40] >> Hey, Dean S. My wheelchair just died.
[28:42] >> Wait, you're locked out your room now?
[28:45] >> Are you stressing out?
[28:48] >> Please help me.
[28:51] >> My wheelchair died. [laughter]
[29:01] >> Dean. My wheelchair died. Okay, come on.
[29:04] >> Keep pushing me deep.
[29:10] >> How was your first day? It
[29:17] >> Uh 3:30 almost.
[29:19] >> I still got like two more hours.
[29:20] >> Two more hours. [laughter]
```
Signal: **crude-answer punchline in the first 4 seconds** (`Where the [ __ ] did you come from?` / `My mom's vagina.`), then two `[laughter]` tags (`28:51`, `29:20`), then a soft landing.

### M41 — [29:27]–[29:51] — 25s — "GOOD NIGHT, DEAN" / "ABSOLUTELY NOTHING"
```
[29:27] >> This is Yogi.
[29:33] >> good night, Dean. Let me know if you
[29:34] want to come in and sleep with me.
[29:35] >> Oh my god. What the [ __ ]
[29:38] >> I'm proud of you, man.
[29:39] >> Why?
[29:40] >> You're getting bullied and what are you
[29:41] doing? What are you doing?
[29:43] >> I just ate food.
[29:44] >> Nothing. Absolutely [ __ ] nothing.
[29:47] >> Listen.
[29:50] >> What? Lectures. [snorts]
```
Signal: setup question `Why?` → punchline `I just ate food.` → topper `Nothing. Absolutely [ __ ] nothing.` → `[snorts]` laugh-reaction at `29:50`. **Textbook joke architecture in 25 seconds.**

### M42 — [29:52]–[30:35] — 44s — SOAKED / HAZING SURVIVOR
```
[29:52] >> Brother, look at how wet I am.
[29:53] >> Yeah, what happened?
[29:54] >> I just got a water bottle dumped on my
[29:55] head and a lemon shoved in my mouth.
[29:57] >> Who did that?
[29:58] >> Silky.
[29:59] >> Can I tell you something, bro? I'm proud
[30:01] >> you've been you've been getting haze
[30:02] sketch gave you a really hard time last
[30:04] night and you made it through. That's
[30:05] what a real brother does.
[30:09] >> [ __ ] it. I like that. You know what?
[30:26] >> our sisters. ONE OF OUR SISTERS.
[30:26] [laughter] YES. That's one of our
```
Signal: **"look at how wet I am" is a spoken visual-state announcement** — the clip self-describes its own visual gag. Q&A recap format: `what happened?` → `Who did that?` → one-word answer `Silky.`

### M43 — [30:36]–[30:59] — 24s — CAMERAMAN KIDNAPPED / NO HELP
```
[30:36] >> He's one of my brothers.
[30:16] >> Why did you not help me when my
[30:17] cameraman was getting kidnapped?
[30:20] >> I'm in a I'm in a wheelchair.
[30:31] >> What are you going to do about it, Lacy?
[30:32] >> Oh, yeah. Lacy, what you going to do
[30:33] about it? Roll over me.
[30:38] >> That's too far, man. That actually
[30:44] >> That's actually [ __ ]
```
Signal: accusation → deadpan excuse `I'm in a wheelchair.` → crowd taunt. (Note: boundary here is soft; `[30:16]` content belongs to this bit though it precedes my chosen start cue.)

### M44 — [31:00]–[31:45] — 46s — SPARTAN KICK / CARRYING THE WHEELCHAIR DOWN
```
[30:47] >> I think we just Spartan kick this fat
[30:54] >> just a wheelchair doesn't mean I can't
[30:55] hear you guys, bro. Three.
[31:00] >> One, two, three.
[31:02] >> One, two, three.
[31:06] >> Okay. Wait, wait, wait. Pull it back.
[31:09] >> One, two, three.
[31:15] >> We got We got All good. All good.
[31:23] >> You got to go on your feet. You got to
[31:25] go on your feet. Oh, look.
[31:30] >> We'll carry it down. We'll carry it
[31:33] >> Hey, we tried, you know. Yeah, we did.
[31:34] We gave it our best.
```
Signal: **`One, two, three.` countdown three separate times** — a built-in, machine-detectable tension-and-release structure, same family as M31's counting. Overheard-insult beat: `just a wheelchair doesn't mean I can't hear you guys, bro.`

### M45 — [31:46]–[31:56] — 11s — TRANSITION / "I RESPECT"
```
[31:36] >> Dean, guess what, Dean? I didn't go.
[31:38] >> GET YOUR FORTNITE playing ass the [ __ ]
[31:40] off my face.
[31:41] >> I DIDN'T GO TO THE PARTY, DEAN.
[31:46] >> I respect
```
Signal: 11s micro-moment, one caps insult + one caps reply. **One of only two sub-15s non-sting moments in the file.**

### M46 — [31:57]–[33:01] — 65s — PIT BULLY INTERVIEW
```
[31:57] Are you a bully?
[31:59] >> Am I a bully?
[32:00] >> Are you a bully?
[32:01] >> Do I look like a bully? My name is Pit
[32:03] Bully.
[32:04] >> Pit bully.
[32:07] >> So you're not you're not going to bully
[32:09] >> No, I'm bully.
[32:14] >> You know who my husband is?
[32:15] >> No.
[32:16] >> Drew.
[32:17] >> I'm the winner of Could have been love
[32:18] season 2. You don't see the Could have
[32:20] been love thing. I did a sleepover with
[32:21] Truski.
[32:35] >> Thank you, sir. I appreciate you.
[32:39] >> Okay. Well, can I ask you a question
[32:42] >> How big's his dick?
[32:43] >> Not bigger than mine.
[32:50] Okay. Do you want to touch it?
[32:52] >> Your your dick?
[32:53] >> I'm okay. No, no, I'm okay. I keep hands
```
Signal: **`bully` said 7 times in 12 seconds** — a keyword-density spike, plus a shock-question payoff `How big's his dick?` / `Not bigger than mine.`

### M47 — [33:02]–[33:56] — 55s — HOMECOMING PROPOSAL TO MARLEY
```
[33:10] >> The one thing about this bear that it
[33:11] brought me
[33:12] >> um was it it introduced me to someone
[33:15] that means a lot to me. And
[33:18] >> um you know coming is today
[33:23] >> this person just is so amazing and um
[33:28] they just light a spark under me. So
[33:35] >> Marley, [cheering]
[33:36] >> will you roll at a homecoming with me?
[33:46] >> the bears are powerful. Will you be the
[33:48] wheel to mature? Roll to homecom.
[33:53] [cheering]
[33:54] >> I will.
```
Signal: **both `[cheering]` tags in the file** (`33:35`, `33:53`). A slow, quiet, 25-second sincere build → the ask → crowd reaction → two-word payoff `>> I will.` **Wholesome, and the editor kept it.** This is the counter-example to "clip-worthy = loud."

### M48 — [33:57]–[34:07] — 11s — ROBOT SWEARING / "BUMPED YOUR HEAD"
```
[33:57] >> Yo, why is this Why IS A ROBOT SWEARING
[33:59] UP ON ME, BRO?
[34:00] >> DUMB ASS BUMPED YOUR HEAD. HAHA.
[34:02] [laughter] HAHA. BUMPED YOUR HEAD,
[34:03] DUMBASS.
[34:08] >> OH. Oh my god. Oh my god.
```
Signal: **11 seconds, all caps, `[laughter]` at `34:02`.** The other sub-15s moment. Proof the editor will keep an 11-second clip if the payoff is instant.

### M49 — [34:08]–[35:05] — 58s — GIRLFRIEND ROSTER BIT
```
[34:11] >> You want to see my girlfriend?
[34:13] >> This is Tena.
[34:15] Oh, that's the money I'm talking about.
[34:18] >> You said you said you were dating Sophie
[34:19] Ray, too. We're on and on.
[34:22] >> How many How many have you had like
[34:26] >> Oh, five five
[34:30] >> Sophie Monday, Reky Tuesday, Sabrina
[34:34] Carpenter Wednesday, [snorts]
[34:36] 9:00 p.m. Pacific. That's when we
[34:37] popping the Blu-rays.
[34:41] >> Sour Patch Kid and the popcorn. Then
[34:43] around 1:00 am on Wednesday, Ice Spice
[34:46] pulls up.
[34:49] >> record a little music, you know.
[34:52] >> Dabble with the 4K DVDs.
[34:56] >> Mario, you're killing me, bro.
[34:59] >> actually killing.
[35:02] >> You're actually killing me,
[35:04] [clears throat]
```
Signal: **escalating list-bit** with a named-celebrity ladder; `[snorts]` at `34:34`; the partner's corpsing reaction is stated three times (`you're killing me, bro.` / `actually killing.` / `You're actually killing me,`) and `[clears throat]` at `35:04` is the stifled laugh.

### M50 — [35:06]–[35:39] — 34s — BATTLEFIELD BETRAYAL / BREAKUP (CLOSER)
```
[35:10] >> Lacy? Let's roll into the battlefield
[35:13] and you take off running and let me
[35:15] leave me back there to get shot.
[35:17] >> I did not.
[35:18] >> YEAH, I JUST GOT LIT UP.
[35:23] >> I'm sorry. I'm sorry. Not
[35:24] >> You're on your own.
[35:25] >> Not again. No. No. Please. No. Don't do
[35:27] this.
[35:27] >> No. Don't do this. Don't do this.
[35:28] >> Don't talk to me.
[35:29] >> Don't do this. Come on.
[35:30] >> Don't call me. Don't come to my house.
[35:34] >> We're done.
[35:37] >> Drew, don't do this.
[35:39] >> Drew, don't do this, bro.
```
Signal: **`Don't do this` ×5 in 12 seconds**, apology repetition, and a hard two-word button `>> We're done.` The compilation ends on a cliffhanger with no resolution.

---

### F-PATTERN ANALYSIS

**INTERPRETATION.** All 50 moments sort cleanly into **seven types**. Counts are mine, from the catalogue above.

| # | Type | Count | % | Detectable signature | Example IDs |
|---|---|---|---|---|---|
| 1 | **Physical escalation / assault-bit** (someone is grabbed, kicked, tipped, boxed, chased, carried) | 14 | 28% | `[screaming]`, ALL-CAPS run, 4–18s silence gaps, profanity burst | M03, M04, M10, M13, M24, M26, M27, M28, M29, M33, M34, M36, M44 |
| 2 | **Verbal conflict / roast / threat volley** (no contact, pure escalation) | 10 | 20% | rapid `>>` turn alternation, caps, insult keywords (`fat ass`, `bully`) | M02, M07, M08, M16, M18, M19, M23, M38, M45, M46 |
| 3 | **Authority / law-enforcement scene** (cops, arrest, Dean, interrogation) | 6 | 12% | keywords `police / officer / arrest / Dean`, question-answer cadence | M06, M25, M35, M39, M40, M41 |
| 4 | **Interview / reveal / confession** (quiet; someone admits or discloses) | 6 | 12% | LOW volume, `>> Wait, so...`, one-word `>> Yes.` beats | M12, M15, M22, M37, M42, M49 |
| 5 | **Acquisition / heist / accumulation** (food, cart, microwave, "unlimited") | 5 | 10% | counting out loud, `Come on.` chants, long silence, `Oh my god` | M09, M31, M32, M34 (shared), M43 |
| 6 | **Romance / social-stakes** (kiss, homecoming ask, rejection, breakup) | 6 | 12% | `[cheering]`, `[laughter]`, a direct question, a one-or-two-word answer | M11, M14, M17, M47, M50 |
| 7 | **Punchline / one-liner micro-clip** (self-contained joke, ≤25s) | 3 | 6% | `[laughter]` or `[snorts]` within 3s of the line | M41, M48, M01 |

**Recurring elements that appear across many types — these are the strongest generalisable features:**

1. **VERBAL REPETITION IS THE SINGLE MOST RELIABLE MARKER.** It appears in **at least 22 of 50 moments** and is trivially detectable from text alone with no audio processing. Verbatim instances: `FOCUS.` ×10 (`06:26`–`06:32`), `WAIT.` ×8 (`16:55`–`16:56`), `Don't do this` ×5 (`35:25`–`35:39`), `Come on.` ×12 (`20:37`–`21:04`), `please` ×5 (`00:56`–`00:57`), `bully` ×7 (`31:57`–`32:09`), `Oh my god` ×3 (`03:54`–`04:01`), `OH, [ __ ]` ×3 (`15:17`–`15:21`), `Police. Police. Police.` (`01:35`), `GET HIM. GET HIM. GET HIM.` (`01:43`), `WHERE'S THE GUN? WHERE'S THE GUN?` (`02:23`), `We have unlimited food.` ×2 (`19:27`–`19:30`), `EASY.` ×4 (`16:57`), `SHUT UP` ×3 (`16:33`–`16:34`), `Watch yourself.` ×3 (`23:01`–`23:02`), `WATCH OUT.` ×3 (`15:58`), `I can't chase you.` ×2 (`11:54`–`11:56`), `y'all good?` ×3 (`11:33`–`11:38`), `get the wheelchair` ×4 (`24:40`–`24:51`), `YOU'RE NOT ON THAT.` ×3 (`14:24`–`14:27`), `Open the door` ×3 (`16:40`–`16:42`), `Just let me` ×4 (`14:04`–`14:10`).
   **Proposed rule: ≥3 repetitions of the same short phrase inside a 10-second window is a clip-worthiness trigger on its own.**

2. **THE WHEELCHAIR / DISABILITY CALLBACK IS THE SHOW'S SPINE.** 19 lines contain `wheelchair`, 6 contain `walk`, 4 contain `stand up`, 4 contain `fat ass`. Nearly every moment is built on it. The strongest punchlines are all callbacks to it: `Stand up then I'll be scared` (`10:19`), `How you aim and walk?` (`18:11`), `You arrested THE DUDE IN THE WHEELCHAIR.` (`24:17`), `I'm in a I'm in a wheelchair.` (`30:20`), `just a wheelchair doesn't mean I can't hear you guys` (`30:54`), `will you roll at a homecoming with me?` (`33:36`).
   **For this specific streamer, `wheelchair|walk|stand up|roll|hop` is a high-precision keyword set.**

3. **RECURRING CAST NAMES ARE A FREE SCENE-INDEX.** `Dean` appears in 13 lines; `Drew`, `Max`, `Ruby`, `Marley`, `Silky`, `Yousef`, `Ronald`, `James`, `Mario`, `Chris`, `Kai`, `Cuy`, `Truski`, `Tena`, `Yogi` each anchor a moment. A shouted proper name is frequently the first word of a clip (see G).

4. **SILENCE IS POSITIVE, NOT NEGATIVE.** Every gap ≥8s sits inside a physical bit (see E2). The 112-second cart heist (M32) is almost wordless and the editor kept all of it.

5. **NOT ALL POSITIVE EXAMPLES ARE LOUD.** M15 (feet money), M25 (dark room), M37 (diet coaching), M42 (hazing recap), M47 (proposal) contain **zero** `[screaming]` and almost no caps. **A volume-only detector would discard roughly 20% of what a human editor kept.** M47 in particular is quiet and wholesome and closes the compilation's emotional arc.

---

## G. HOOK PATTERNS — HOW EACH MOMENT OPENS

Verbatim first substantive line of each moment, grouped by opening form.

### G1 — DIRECT QUESTION AS THE FIRST WORDS (18 of 50 = 36%) — the dominant hook
```
[00:02] >> ALL RIGHT. SO, why are you bouncing on?
[00:31] >> Hey, you ever been inside of a locker?
[04:11] >> YOU ALMOST ran her over.        (accusation-as-question)
[05:21] >> Hey gang, what happened to you?
[06:45] What you got going on, bro?
[11:33] >> y'all good?
[14:43] >> Did you lock him in a a dark room? Yes or no?
[18:32] >> How many chicken nuggets did we get? How many pops of chicken tenders?
[24:09] >> Why am I doing this?
[25:14] >> what the [ __ ] is you want me to help you?
[28:22] >> Where the [ __ ] did you come from?
[29:39] >> Why?
[29:53] >> Yeah, what happened?
[30:16] >> Why did you not help me when my cameraman was getting kidnapped?
[31:57] Are you a bully?
[33:57] >> Yo, why is this Why IS A ROBOT SWEARING UP ON ME, BRO?
[34:11] >> You want to see my girlfriend?
[07:31] >> Wait, so you was making a bag off just your feet?
```

### G2 — SHOUTED NAME OR SHOUTED IMPERATIVE (11 of 50 = 22%)
```
[00:44] >> ALL RIGHT, LACY, WATCH.
[01:35] >> Police. Police. Police.
[03:39] >> RUBY.
[06:05] >> NO EXCUSES. [screaming]
[06:41] >> LI.
[15:13] >> OKAY. HEY, LISTEN. LISTEN. Act like you kicked me and run the [ __ ] off.
[16:24] >> GUYS,
[16:24] >> GET THE AWAY.
[22:31] >> THEY BROUGHT IT OUT.
[24:22] >> HEY YO, EVERYBODY SPAM FREE LACY.
[31:00] >> One, two, three.
```

### G3 — NON-VERBAL SOUND, NO WORDS AT ALL (3 of 50 = 6%)
```
[00:00] LET'S [screaming] GO.
[15:46] [screaming]
[19:06] [cough]  /  [19:08] [snorts]    (inside M31)
```

### G4 — DECLARATIVE STATEMENT OF A PROBLEM OR STAKE (12 of 50 = 24%)
```
[02:36] >> No, they broke the gun.
[03:08] >> Bro, come on. Please. I just spent like an hour doing that.
[07:08] >> UM, I'm not going to say no to the bag if it's right there.
[09:04] I'm terrorizing homecoming.
[11:18] >> I GOT TWO I GOT $1,000 ON HIS HEAD
[12:28] >> YOU just cracked my phone.
[13:39] >> Chad, it's not a e, bro. I don't have an ego.
[14:24] YOU'RE NOT ON THAT. YOU'RE NOT ON THAT.
[15:55] >> And I'm going to PUT YOU IN A [ __ ] TRASH CAN.
[25:57] >> See, hold on. Let's take this pizza. See, look. This is your problem.
[27:00] >> Here go my security badge. Here go my security badge.
[29:52] >> Brother, look at how wet I am.
[35:10] >> Lacy? Let's roll into the battlefield and you take off running and let me leave me back there to get shot.
```

### G5 — IDEA / PLAN ANNOUNCEMENT (2 of 50 = 4%)
```
[20:02] >> Wait. Oh my god. I have an idea.
[06:49] >> Listen, let's hop in the studio.
```

### G6 — MID-SCENE, ZERO SETUP (the rest)
```
[21:49] All right, let's go. Let's go.
[27:41] >> Okay. Can I confess something?
[33:10] >> The one thing about this bear that it brought me
```

### G-PATTERN ANALYSIS

**INTERPRETATION.**

- **Not one of the 50 moments opens with narration, context, or an establishing statement.** There is no "so here's what happened." The editor enters every clip already inside the action.
- **`Hey` / `Yo` / `Wait` / `Okay` / `All right` open 21 of the 50 moments.** These four filler-openers are the compilation's punctuation. **A cut-point heuristic that starts a clip 0.5s before a `Hey|Yo|Wait|Okay|All right|Bro` token would reproduce a large fraction of this editor's in-points for free.**
- **Question-openers (36%) plus shouted-name/imperative openers (22%) = 58% of all clips.** Both are single-line, textually detectable, and require no audio analysis.
- The **first shot is almost always the *provocation*, never the *reaction*.** The reaction is the payoff, and it lands 5–30 seconds later. Stage 3 should therefore anchor a clip's start on the *stimulus* line and its end on the reaction, not the reverse.
- **Repeated openers.** Two moments open by saying the same sentence twice in a row: `[27:00] >> Here go my security badge. Here go my security badge.` and `[14:24] YOU'RE NOT ON THAT. YOU'RE NOT ON THAT.` This doubles as an emphasis marker.

---

## H. THRESHOLDS AND NUMBERS

### H1 — FILE-LEVEL COUNTS (measured, not estimated)

| Quantity | Value |
|---|---|
| Total lines in file | 1,070 (2 header lines + 1,068 caption lines) |
| Timestamped caption lines | 1,068 |
| First timestamp | `[00:00]` |
| Last timestamp | `[35:39]` |
| Total compilation duration | 2,139 s = 35 min 39 s |
| Distinct moments identified (my segmentation) | **50** |
| `[screaming]` tags | 17 |
| `[laughter]` tags | 13 |
| `[snorts]` tags | 4 |
| `[applause]` tags | 3 |
| `[cheering]` tags | 2 |
| `[clears throat]` tags | 2 |
| `[cough]` tags | 1 |
| **Total non-speech tags** | **42** |
| Censored profanity tokens `[ __ ]` | 93, across 86 lines |
| Fully-capitalised caption lines | 89 of 1,068 (8.3%) |
| Contiguous ALL-CAPS runs | 46 |
| Longest ALL-CAPS run | `[01:43]`–`[01:59]` = 16 s |
| Caption cues per minute (avg) | 30.0 |

### H2 — DERIVED CLIP LENGTH — **THE NUMBER FOR STAGE 3**

From the 50 moments in section F:

| Statistic | Value |
|---|---|
| **Mean moment length** | **42.7 s** |
| **Median moment length** | **39.5 s** |
| Standard deviation | 21.3 s |
| Minimum | 2 s (the `[00:00]` cold-open sting) |
| Minimum excluding the sting | 11 s (M45, M48) |
| 10th percentile | 17 s |
| 25th percentile | 29 s |
| 75th percentile | 52 s |
| 90th percentile | 67 s |
| Maximum | 112 s (M32, the cart heist) |
| Mean excluding the 2 s sting | 43.5 s |
| Median excluding the 2 s sting | 40 s |

**Distribution:**

| Bucket | Count | Share |
|---|---|---|
| 0–14 s | 4 | 8% |
| 15–24 s | 4 | 8% |
| 25–34 s | 12 | 24% |
| 35–44 s | 10 | 20% |
| 45–59 s | 11 | 22% |
| 60–89 s | 8 | 16% |
| 90–120 s | 1 | 2% |

**66% of moments fall in 25–60 s. 78% fall in 20–70 s.**

> **RECOMMENDED STAGE 3 DEFAULTS (derived from this file):**
> - **Default target clip length: 40 s** (the median).
> - **Accept band: 20 s – 70 s** (covers 78% of what a human editor kept).
> - **Hard floor: 11 s.** Two curated moments are exactly 11 s. Do not reject below ~11 s without a reason; do reject below ~8 s.
> - **Hard ceiling: 112 s**, but anything over 90 s should require an explicit justification — only 1 of 50 (2%) exceeded 90 s, and it was a near-wordless visual set-piece.
> - **Caveat:** these come from **one** compilation, one video ID `cVkFMpDLQrM`, and from **my** content-shift segmentation, not from the editor's actual cut list. Treat as a strong first default to be re-derived against a second best-of before being called validated.

### H3 — TIMESTAMP-GAP NUMBERS

| Gap (s) | Count |
|---|---|
| 0 | 61 |
| 1 | 418 |
| 2 | 348 |
| 3 | 120 |
| 4 | 51 |
| 5 | 31 |
| 6 | 17 |
| 7 | 6 |
| 8 | 2 |
| 9 | 5 |
| 10 | 3 |
| 11 | 1 |
| 12 | 1 |
| 14 | 1 |
| 16 | 1 |
| 18 | 1 |

Gaps ≥ 10 s (the file's 8 longest silences — all inside physical-action bits):
```
18s  21:31 -> 21:49
16s  23:51 -> 24:07
14s  20:09 -> 20:23
12s  08:40 -> 08:52
11s  31:46 -> 31:57
10s  14:14 -> 14:24
10s  18:18 -> 18:28
10s  19:08 -> 19:18
```

### H4 — MONEY, DATES, TIMES AND COUNTS SPOKEN ON CAMERA (verbatim)

```
[11:18] >> I GOT TWO I GOT $1,000 ON HIS HEAD and I
[11:20] GOT,000 ON MY HEAD. HEY, I'MMA DOUBLE IT
[11:29] >> WHOEVER DO IT, I GOT $1,000. This
[12:31] >> bro? You owe me. It's a $3,000 edition.
[12:34] >> It's a $3,000.
[13:04] >> I have another iPhone. Actually, I have
[13:06] an iPhone 14.
[01:24] >> 218.                                   (dorm room number)
[05:29] >> I have your class at 7:00 a.m. tomorrow.
[05:56] >> I'm in your class tomorrow morning at
[05:58] 7:00 a.m.
[08:01] >> You rolled your fat ass in here
[08:04] 45 minutes late.
[08:05] >> You showed up literally 30 minutes late.
[08:16] >> Short ass class. It was like 2 minutes.
[09:24] >> I actually got like four albums right
[13:52] >> 15?
[17:52] 14year-old beating the out of us more.
[18:36] Okay. One,
[18:38] two,
[18:41] three,
[18:44] four,
[18:46] five,
[18:47] 6 7
[18:51] 8
[18:53] 9.
[19:41] >> Okay. Okay. Okay. How many is that? 4 8
[19:46] 12 16 8. We have 20. We have 20. Okay.
[24:19] >> SO YEAH, I'M THE DUDE THAT PUT THREE
[24:20] PICNIC TABLES WHEN I CAN'T EVENING WALK.
[29:17] >> Uh 3:30 almost.
[29:19] >> I still got like two more hours.
[29:22] >> You're not going to sleep till 5?
[32:17] >> I'm the winner of Could have been love
[32:18] season 2.
[32:28] >> So, I'm the winner of season two.
[34:26] >> Oh, five five
[34:27] >> like five days in a week.
[34:36] 9:00 p.m. Pacific. That's when we
[34:37] popping the Blu-rays.
[34:43] around 1:00 am on Wednesday, Ice Spice
[34:52] >> Dabble with the 4K DVDs.
```

**No date of any kind is spoken anywhere in the transcript.** No view counts, no payout figures, no platform metrics, no bounty amounts (the `$1,000` is an in-fiction bounty on a person's head, not a Clipping.net payout). **NOTHING FOUND** on view thresholds or real monetisation numbers — this file contains zero information about the payout side of the project.

---

## APPENDIX — TAG TIMESTAMP INDEX (for building test fixtures)

```
[screaming] : 00:00, 01:05, 02:16, 03:39, 04:37, 04:46, 06:05, 06:11, 06:54,
              10:27, 13:02, 13:08, 13:26, 14:39, 15:46, 16:42, 24:13
[laughter]  : 06:14, 09:44, 10:57, 13:32, 22:43, 22:49, 23:19, 25:34, 27:11,
              28:51, 29:20, 30:26, 34:02
[snorts]    : 02:29, 19:08, 29:50, 34:34
[applause]  : 08:40, 08:55, 08:59
[cheering]  : 33:35, 33:53
[clears throat] : 21:12, 35:04
[cough]     : 19:06
```

ALL-CAPS runs of ≥2 s (candidate shouting windows):
```
01:43-01:59 (16s)   02:15-02:23 (8s)    02:42-02:45 (3s)    03:35-03:39 (4s)
06:09-06:15 (6s)    06:22-06:32 (10s)   06:54-06:56 (2s)    11:09-11:12 (3s)
11:20-11:23 (3s)    14:24-14:28 (4s)    15:02-15:04 (2s)    15:56-16:00 (4s)
16:04-16:07 (3s)    16:13-16:17 (4s)    16:24-16:26 (2s)    17:06-17:08 (2s)
24:13-24:15 (2s)    24:18-24:22 (4s)    25:09-25:14 (5s)    33:59-34:03 (4s)
```

---

*End of verbatim report. Video ID `cVkFMpDLQrM` throughout. Nothing above is asserted as project fact; per project Rule 3, all of it is a lead to be confirmed in-session.*
