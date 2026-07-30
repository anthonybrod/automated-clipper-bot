# Deep dive: ingestion + alternative full-pipeline architectures — read directly from source, 2026-07-29

Three repos, read via `gh api` (raw source, not paraphrased from READMEs):
`lay295/TwitchDownloader` (C#/.NET, VOD+chat ingestion), `nirvagold/stream-clipper`
(Tauri/Rust/Svelte desktop app, audio+chat multi-signal detection),
`metaleey/AI-auto-segment-edit-video-pipeline` (Python, ASR→LLM→merge pipeline).
Cross-referenced against `verified_tools_catalog.md` (the two known strategies:
DIY/self-hosted vs SaaS-chained) and `deep_dive_openshorts.md` (the coordinating
session's parallel read of the strongest full-pipeline candidate).

---

## Repo 1 — `lay295/TwitchDownloader`

**3,827 stars · https://github.com/lay295/TwitchDownloader · C#/.NET, CLI + WPF GUI**

The most-starred Twitch tool found across all research, by a wide margin. Read
`TwitchDownloaderCore/VideoDownloader.cs`, `ChatDownloader.cs`, `TwitchHelper.cs`,
`Chat/ChatJson.cs`, `Chat/ChatText.cs`, `Tools/DownloadTools.cs`,
`Tools/VideoDownloadThread.cs`, and `TwitchObjects/ChatRoot.cs` in full.

### Real technique

**VOD download — no official API, impersonates the Twitch web player:**

1. Calls Twitch's internal GraphQL endpoint (`https://gql.twitch.tv/gql`) using
   Twitch's own **public web-player Client-ID** (`kimne78kx3ncx6brgo4mv6wki5h1ko`,
   hardcoded, no registration needed) with a persisted-query operation named
   `PlaybackAccessToken_Template` to get a signed `(token, signature)` pair for
   the VOD. No developer app registration, no OAuth required for public VODs;
   an optional user OAuth token is passed through only for subscriber-restricted
   VODs (`Authorization: OAuth {token}` header).
2. Uses that signed token to request the actual **HLS/m3u8 manifest** directly
   from Twitch's CDN: `https://usher.ttvnw.net/vod/v2/{videoId}.m3u8?sig=...&token=...`
   — i.e., it fetches Twitch's own real HLS manifest, not a re-encoded or
   proxied stream. If that call throws an `AuthenticationException` (some
   networks/regions block `usher.ttvnw.net` directly), it falls back to a
   **community-run Cloudflare Worker proxy** at
   `twitch-downloader-proxy.twitcharchives.workers.dev` that mirrors the same
   endpoint — a concrete, real workaround for geo/network blocking worth
   knowing about if VOD fetches ever get blocked in a hosted/CI environment.
3. Downloads the individual `.ts` (or `.mp4` for AV1) segments listed in the
   m3u8 with a **pool of parallel worker threads** (`VideoDownloadThread`,
   configurable thread count), each thread pulling from a shared
   `ConcurrentQueue` of remaining segment names. Each segment download is
   retried up to 5 times with jittered delays (`Random.Shared.Next` +
   `Task.Delay`), verified against an `ExpectedFileSize` derived from the
   first successful download of that segment, and — if a segment is
   unrecoverable after retries — **stubbed with a valid-but-blank MPEG-TS
   packet** (a literal byte array of a minimal valid TS packet embedded in
   the source) so the final `ffmpeg concat` doesn't break on a missing file.
4. Segments are concatenated via `ffmpeg -f concat` (stream copy, not
   re-encode) using a generated `concat.txt` list plus a separately
   `ffmpeg`-serialized `metadata.txt` (chapters, VOD ID) merged in via
   `-map_metadata`. On failure it retries once with `-c:v copy` only
   (audio re-encoded) because some VODs have corrupt audio streams that
   choke pure `-c copy` (a known, documented Twitch VOD quirk, referenced
   in-code as `lay295#1121`).

**Chat download — cursor-paginated GraphQL, not a public REST endpoint:**

1. Uses a *different* hardcoded Client-ID (`kd1unb4b3q4t58fwlpcbzcbnm76a8fp`)
   against the same `gql.twitch.tv/gql` endpoint, persisted-query operation
   `VideoCommentsByOffsetOrCursor`.
2. The full VOD time range is split into N parallel "connections"
   (`downloadOptions.DownloadThreads`, default chunk-per-thread), each doing
   its own **cursor-based pagination** loop: first request seeds with
   `contentOffsetSeconds`, every subsequent request uses the `cursor` from
   the last page's final comment edge, until `pageInfo.hasNextPage` is false.
3. **Resilience pattern worth copying directly**: on `HttpRequestException`,
   it doesn't hard-fail — it increments an `errorCount`, backs off
   `1000ms * errorCount`, and retries, capping at 10 consecutive errors
   before giving up. Separately, Twitch's API sometimes returns a **null**
   `comments` list for no reason (`// video.comments can be null for some
   dumb reason` — verbatim code comment) — this is handled identically with
   its own `nullCount` back-off counter. Both counters **decay** on success
   (`Math.Max(0, errorCount - 0.1)`) rather than resetting to zero, so a
   single blip doesn't fully reset the backoff clock but persistent single
   failures gradually forgive themselves. This is a genuinely well-designed
   retry/backoff pattern, not naive.
4. After collecting all comments, it **deduplicates by comment ID** (parallel
   chunks can overlap at boundaries) and **auto-corrects timestamp drift**:
   some old VODs have chat timestamps offset by up to an hour from the video;
   `AdjustCommentOffsets` estimates the drift from the first comment's
   `created_at` vs. the video's `created_at` and shifts every comment's
   `content_offset_seconds` accordingly if the estimated offset exceeds 5s.

### What a real, complete Twitch chat JSON dump actually looks like

This matters directly for any future chat-velocity-based highlight detection —
this is the exact, real shape (`TwitchObjects/ChatRoot.cs`), not a guess:

```jsonc
{
  "FileInfo": { "Version": {...}, "CreatedAt": "..." },
  "streamer": { "name": "...", "login": "...", "id": 123 },
  "video": {
    "title": "...", "description": "...", "id": "...",
    "created_at": "2026-01-01T00:00:00Z",
    "start": 0.0, "end": 3600.0, "length": 3600.0,
    "viewCount": 12345, "game": "...",
    "chapters": [ { "id": "...", "startMilliseconds": 0, "lengthMilliseconds": 60000,
                    "description": "...", "gameDisplayName": "..." } ]
  },
  "comments": [
    {
      "_id": "...",
      "created_at": "2026-01-01T00:05:12Z",
      "channel_id": "...",
      "content_type": "video",
      "content_id": "...",
      "content_offset_seconds": 312.4,   // <-- the field every downstream
                                          //     chat-velocity tool keys on
      "commenter": { "display_name": "...", "_id": "...", "name": "..." },
      "message": {
        "body": "POGGERS that was insane",
        "bits_spent": 0,
        "fragments": [ { "text": "POGGERS", "emoticon": { "emoticon_id": "..." } }, ... ],
        "user_badges": [ { "_id": "subscriber", "version": "12" } ],
        "user_color": "#FF0000",
        "emoticons": [ { "_id": "...", "begin": 0, "end": 7 } ]
      }
    }
  ],
  "embeddedData": { "thirdParty": [...], "firstParty": [...], "twitchBadges": [...], "twitchBits": [...] }
}
```

Key fields for detection work: `content_offset_seconds` (float, seconds from
VOD start — the timeline anchor), `commenter.display_name`/`_id` (for unique-
user-count windows), `message.body` (raw text for keyword/caps-ratio scoring),
`message.fragments[].emoticon` (whether a message contains an emote — directly
usable as "emote density" the way `stream-clipper` does, see Repo 2), and
`message.bits_spent` (cheer/bits amount — a real monetary-hype signal none of
our other research sources mentioned). **This exact schema is not
theoretical** — `stream-clipper`'s chat parser (Repo 2, below) consumes this
literal JSON shape and even comments `// Parse Twitch JSON format (from
TwitchDownloader)` in its own source, i.e. TwitchDownloader's chat JSON has
already become a de facto standard interchange format other independent tools
build on.

Also useful: `ChatText.cs` shows the plain-text export format
(`[HH:MM:SS] username: message` per line, or a "UTC full" variant with
milliseconds) — a simpler fallback shape if a lighter-weight parser is ever
preferred over full JSON.

### Auth / rate-limiting

There is **no official Twitch Developer API key or OAuth app registration**
anywhere in the ingestion path for public VODs/chat — it entirely impersonates
Twitch's own web player using Twitch's own public client IDs. This is
materially different from (and much lower-friction than) the Twitch Helix API
route documented in `verified_tools_catalog.md` (`Get Clips`/`Create Clip`,
which need a registered app + `client_credentials` or user OAuth). There's no
explicit rate-limiter/token-bucket in the code — resilience is entirely
reactive: retry-with-backoff on HTTP errors (chat) and a bounded thread-restart
budget of `max(threadCount, 95% of total parts)` before giving up entirely
(video segments), not a proactive request-throttle. Worth noting as a **risk**,
not just a technique: this approach depends on Twitch's internal/private API
surface remaining stable and unauthenticated-friendly; it is not a supported,
documented, stable contract the way Helix is.

### Concrete reusable pattern for our project

- **Port directly**: the chat JSON schema above as our canonical intermediate
  chat-log format. It's already proven as an interchange format by a second
  independent tool (`stream-clipper`), so building our own chat-velocity
  detector to consume/produce this exact shape means free interop with both
  of these tools' ecosystems (e.g., could literally feed a TwitchDownloader
  chat export into `stream-clipper`-style analysis code, or vice versa).
- **Adapt**: the dual-counter decaying backoff pattern (`errorCount`/
  `nullCount`, decay by 0.1 per success, cap at 10) for any of our own
  Twitch-facing polling loops — it's a better-than-naive pattern worth
  reusing verbatim in Python (`asyncio.sleep(1.0 * min(error_count, 10))`
  with a similar decay).
- **Borrow the idea, don't port the code**: the GQL-impersonation ingestion
  approach itself is higher-risk/higher-maintenance than `yt-dlp` (already
  our documented primary pick) for VOD download specifically — `yt-dlp`
  wraps equivalent logic and is actively maintained by a much larger team.
  But the **chat-download approach is genuinely additive**: `yt-dlp` does not
  download Twitch VOD chat replay at all. If our pipeline needs full chat
  history (not just live-captured chat via IRC/EventSub), this cursor-paginated
  GQL approach — or literally shelling out to the `TwitchDownloaderCLI`
  binary (`ChatDownload` mode, cross-platform, self-contained executable,
  no .NET SDK needed to *run* it) — is the concrete way to get it.

### Code excerpt worth keeping verbatim

The decaying dual-backoff loop — the exact resilience shape worth porting to
any Python chat-polling code we write:

```csharp
// ChatDownloader.cs — DownloadSection loop
catch (HttpRequestException ex)
{
    if (++errorCount > 10) throw;
    await Task.Delay((int)(1_000 * errorCount), cancellationToken);
    continue;
}
// ...
if (commentResponse.data.video.comments?.edges is null)
{
    if (++nullCount > 10) throw new Exception("Received too many null comment lists.");
    await Task.Delay((int)(100 * nullCount), cancellationToken);
    continue;
}
const double BACK_OFF_FACTOR = 0.1;
nullCount = Math.Max(0, nullCount - BACK_OFF_FACTOR);
errorCount = Math.Max(0, errorCount - BACK_OFF_FACTOR);
```

---

## Audit pass — TwitchDownloader (Repo 1) additional files [2026-07-29]

(A separate, complementary audit pass covering Repos 2 and 3 —
`nirvagold/stream-clipper` and `metaleey/AI-auto-segment-edit-video-pipeline`
— appears further down, after the Repo 3 section and before the Cross-repo
synthesis, under the same "Audit pass" heading. That pass and this one were
done independently and cover disjoint files; the heading is duplicated
because both passes started from the same instruction template.)

The prior pass on `lay295/TwitchDownloader` read 8 of 311 files. This pass reads
the remaining highest-value gaps in `TwitchDownloaderCore` (the reusable
logic library) plus a medium-priority skim of `TwitchDownloaderCLI`, per an
explicit audit request flagging this repo as under-read given its size.
Fetched via the same `gh api repos/lay295/TwitchDownloader/contents/{path}?ref=master
--jq .content | base64 -d` method as the original pass, full file content, no
READMEs. Files read in full this pass: `ClipDownloader.cs`, `ChatUpdater.cs`,
`TsMerger.cs`, `ChatRenderer.cs` (2,253 lines — every subsystem read: init,
ffmpeg piping, SIMD alpha-mask generation, frame-diff caching, animated-emote
compositing, comment-section/highlight-icon layout, text/emoji/RTL/block-art
rendering, asset prefetch+scaling, video-tick range calc — the handful of
remaining lines are repetitive `DrawText`/`DrawTimestamp`/`DrawAvatar`
drawing-primitive plumbing with no new technique in them), `Models/M3U8.cs`,
`Models/M3U8Parse.cs`, `Models/M3U8VideoQualities.cs`, `Models/M3U8VideoQuality.cs`,
`Models/VideoQualities.cs`, `Models/ClipVideoQualities.cs`, `Tools/TwitchRegex.cs`,
`Tools/IdParse.cs` (not originally in scope — see correction below),
`Tools/VideoSizeEstimator.cs`, `Tools/HighlightIcons.cs`, `Tools/FfmpegMetadata.cs`,
`Tools/FfmpegConcatList.cs`, `Tools/ClipQualityComparer.cs`,
`Tools/ClipVideoQualityComparer.cs`, `Chat/EmojiVendor.cs`, `Chat/ChatHtml.cs`,
`Services/FilenameService.cs`, `Services/CacheDirectoryService.cs`,
`TwitchObjects/Gql/GqlClipResponse.cs`, `GqlClipTokenResponse.cs`,
`GqlClipSearchResponse.cs`, `GqlShareClipRenderStatusResponse.cs`, plus
targeted method-level reads inside `TwitchHelper.cs` (the clip-fetch GQL calls)
and `VideoDownloader.cs` (confirming its merge path against `TsMerger.cs`).
At medium priority: `TwitchDownloaderCLI/Modes/DownloadClip.cs`,
`DownloadVideo.cs`, `DownloadChat.cs`, `RenderChat.cs`, `MergeTs.cs`, and their
`Modes/Arguments/*.cs` counterparts (`ClipDownloadArgs.cs`,
`VideoDownloadArgs.cs`, `ChatDownloadArgs.cs`, `ChatRenderArgs.cs`,
`TsMergeArgs.cs`).

### Clip download is a genuinely separate, undocumented path — and it exposes native portrait-crop data

`ClipDownloader.cs` confirms clip download is architecturally distinct from
the VOD path (no HLS/m3u8 involved at all — a clip has a small number of
pre-rendered MP4 "asset" renditions, not segments to stitch): it calls
`TwitchHelper.GetShareClipRenderStatus(clipId)`, a **persisted GQL query named
`ShareClipRenderStatus`** (hash `66038e29eb00d8fd115b0ce1a1382dd9d41168739b08bc87dc042af6a730541f`,
same web-player Client-ID `kimne78kx3ncx6brgo4mv6wki5h1ko` as the VOD path),
appends `?sig=...&token=...` from the response's embedded
`playbackAccessToken` directly onto the chosen asset's `sourceURL`, and
downloads that URL straight with a throttleable `HttpClient` stream copy — no
manifest, no parallel segment threads, no `ffmpeg concat`. If
`--encode-metadata` is set it downloads to a temp file first, then runs a
single `ffmpeg -i temp -i metadata.txt -map_metadata 1 -y -c copy dest` pass
(same `FfmpegMetadata` serializer as the VOD path, see below) rather than
muxing during download.

**Non-obvious, previously undocumented finding**: `GetClipInfo` (ad-hoc
inline GQL query, no persisted hash) and `GetClipLinks` (persisted query
`VideoAccessToken_Clip`, hash `36b89d2507fce29e5ca551df756d27c1cfe079e2609642b4390aa4c35796eb11`,
deserializing to `GqlClipTokenResponse`/`GqlClipResponse`) still exist in
`TwitchHelper.cs` but **are not what the actual download path uses** — they
appear to be legacy/GUI-only (clip search/preview) methods, superseded for
downloading by `GetShareClipRenderStatus`. A naive read of the file tree
(picking `GqlClipResponse.cs`/`GqlClipTokenResponse.cs` because their names
look like "the" clip GQL schema) would document the wrong operation. The
schema actually used, `GqlShareClipRenderStatusResponse.cs`, is a much richer
response than either — critically, each `asset` in `clip.assets[]` carries a
`portraitMetadata` object with `fullTemplateMetadata`/`stackedTemplateMetadata`,
each containing `topLeft`/`bottomRight` **crop-coordinate percentages**
(`PortraitCropCoordinates { xPercentage, yPercentage }`), plus a
`portraitClipLayout` string. This means **Twitch's own clip-render pipeline
already computes and exposes a vertical/portrait crop for clips that have
one** — a real, free, Twitch-native "smart crop to 9:16" signal that
`VideoQualities.FromClip` in `Models/VideoQualities.cs` uses to separate
`IsPortrait`/`IsLandscape` assets and build a `-Portrait` suffixed quality
list callers can request directly (`--quality 1080p60-Portrait`, or the
`"best"` + `"portrait"` keyword combination). **This did not exist anywhere
in the original 8-file read** and is a materially different, better clip-fetch
detail than what was previously documented (which only covered VOD
GQL/HLS). See the cross-repo synthesis addendum below for why this matters
for our own short-form pipeline.

```csharp
// TwitchHelper.cs — the actual GQL operation ClipDownloader.cs uses
public static async Task<GqlShareClipRenderStatusResponse> GetShareClipRenderStatus(string clipId)
{
    var request = new HttpRequestMessage()
    {
        RequestUri = new Uri("https://gql.twitch.tv/gql"),
        Method = HttpMethod.Post,
        Content = new StringContent("{\"operationName\":\"ShareClipRenderStatus\",\"variables\":{\"slug\":\"" + clipId + "\"},"
            + "\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"66038e29eb00d8fd115b0ce1a1382dd9d41168739b08bc87dc042af6a730541f\"}}}",
            Encoding.UTF8, "application/json")
    };
    request.Headers.Add("Client-ID", "kimne78kx3ncx6brgo4mv6wki5h1ko");
    // ... returns clip.assets[].videoQualities[] AND clip.assets[].portraitMetadata (crop coords)
}
```

### Correction: `HighlightIcons.cs` is not a Twitch-native highlight-marker API

The audit brief flagged this file by name as a candidate for Twitch-native
"highlight" moment markers. Having now read it in full: **it is not that.**
It is purely a chat-video-rendering feature — it draws small SVG badge icons
(subscription tier, Prime, gift subs, bit-badge tier, watch streak, charity
donation, raid "Combo") next to *system message* comments when
`ChatRenderer.cs` burns the chat into video, using SkiaSharp to rasterize
inline SVG path strings into cached bitmaps. `HighlightType.ChannelPointHighlight`
is the closest thing to a real "highlight," but it's a **per-message viewer
action** — a user redeemed channel points to make their own single chat
message stand out (`comment.message.user_notice_params.msg_id ==
"highlighted-message"`), not a stream-level moment marker.

What *is* genuinely useful here, and was not documented anywhere in the
original pass: `HighlightIcons.GetHighlightType(Comment)` is a **complete,
free, regex/string-prefix classifier for high-signal synthetic system events
that already exist as ordinary `Comment` entries in the chat JSON** — no
separate API call needed. It classifies, by matching the exact literal
prefixes/suffixes Twitch's IRC system messages use:
`SubscribedTier`/`SubscribedPrime` (`"{name} subscribed at Tier N"` /
`"... with Prime"`), `GiftedMany`/`GiftedSingle`/`GiftedAnonymous`/
`ContinuingGift`/`PayingForward` (gift-sub chains), `Raid` (regex
`^\d+ raiders from {name} have joined! `), `CharityDonation` (`": Donated $X
to support ..."`), `WatchStreak` (`"watched N consecutive streams ... sparked
a watch streak!"`), `BitBadgeTierNotification`, and `Combo` (hype trains).
These are exactly the kind of "audience found this moment significant"
events a moment-detector wants — raids, sub bombs, and donations are strong,
free, zero-LLM signals — and this confirms they're detectable today with
simple string matching against known Twitch system-message templates,
directly in the chat JSON already being ingested. This is a better, more
concrete finding than the "native highlight marker" hypothesis it replaces;
see the synthesis addendum below.

Also confirmed while reading this: the `chapters[]` array in the chat JSON
(`GetOrGenerateVideoChapters`, documented in the original pass) is generated
from `VideoMomentEdge` nodes of `_type == "GAME_CHANGE"` only — i.e. Twitch's
public chapter/moments API tracks **category changes**, not curated
highlights. There is no broader "official highlight moments" feed exposed
anywhere in this codebase; the event-classifier above is the closest real
substitute.

```csharp
// HighlightIcons.cs — GetHighlightType (abridged; full method checks ~10 patterns)
public static HighlightType GetHighlightType(Comment comment)
{
    var bodySpan = comment.message.body.AsSpan();
    var displayName = comment.commenter.display_name.AsSpan();
    if (bodySpan.StartsWith(displayName))
    {
        var bodyWithoutName = bodySpan[displayName.Length..];
        if (bodyWithoutName.StartsWith(" subscribed at Tier")) return HighlightType.SubscribedTier;
        if (bodyWithoutName.StartsWith(" is gifting")) return HighlightType.GiftedMany;
        if (bodyWithoutName.Contains(" consecutive streams ", StringComparison.Ordinal)
            && bodyWithoutName.Contains(" and sparked a watch streak! ", StringComparison.Ordinal))
            return HighlightType.WatchStreak;
        if (bodyWithoutName.StartsWith(": Donated ") && bodyWithoutName[10..].Contains(" to support ", StringComparison.Ordinal))
            return HighlightType.CharityDonation;
        // ... gifted/raid/combo/bits patterns follow the same shape
    }
    if (char.IsDigit(bodySpan[0]) && bodySpan.EndsWith(" have joined! ")
        && Regex.IsMatch(bodySpan, $@"^\d+ raiders from {comment.commenter.display_name} have joined! "))
        return HighlightType.Raid;
    return HighlightType.None;
}
```

### Correction: `TsMerger.cs` is a separate, simpler, non-ffmpeg merge path — not what `VideoDownloader.cs` uses

Confirmed by re-checking `VideoDownloader.cs` directly: the actual VOD
download-and-merge pipeline still works exactly as the original write-up
described — `FfmpegConcatList.SerializeAsync` writes `concat.txt`, then
`RunFfmpegVideoCopy` shells out to `ffmpeg -f concat -i concat.txt ...`. That
part was correct and needed no correction.

`TsMerger.cs`, however, is a **completely different, standalone code path**
exposed as its own CLI verb (`tsmerge`, logged at startup as *"experimental
and is subject to change without notice in future releases"*), for merging
an arbitrary user-supplied list of `.ts`/`.tsv`/`.tsa`/`.m2t`/`.m2ts` files
(or an M3U/M3U8 playlist naming them) — not necessarily anything downloaded
by this tool. Its merge is **raw byte-level concatenation**, no ffmpeg
process at all: it reads each file path from the input list/manifest, first
validates every part is a well-formed MPEG-TS file by checking the file
length is a nonzero multiple of the 188-byte TS packet size (`VerifyVideoPart`),
then does a plain sequential `FileStream.CopyToAsync` of every part directly
into the output stream. This works because MPEG-TS packets are
self-delimited and byte-concatenation-safe — no container remuxing is
needed the way it would be for, say, raw MP4 fragments. Worth knowing as a
**cheap, dependency-free alternative to `ffmpeg -f concat`** for our own
pipeline specifically when segments are confirmed to be raw `.ts` (not
`.mp4`/AV1, which Twitch also serves and which this technique would not be
valid for).

```csharp
// TsMerger.cs — VerifyVideoPart + the actual merge loop
private static async Task<bool> VerifyVideoPart(string filePath)
{
    const int TS_PACKET_LENGTH = 188; // MPEG TS packets: [ 4B header ][ 184B body ]
    await using var fs = File.Open(filePath, FileMode.Open, FileAccess.Read, FileShare.Read);
    var fileLength = fs.Length;
    return fileLength != 0 && fileLength % TS_PACKET_LENGTH == 0;
}
// CombineVideoParts then just does: await fs.CopyToAsync(outputStream, cancellationToken);
// for every part in order — no ffmpeg process, no re-encode, no concat demuxer.
```

### M3U8 manifest parsing and quality selection — confirmed in full

`Models/M3U8.cs` (the record model) and `Models/M3U8Parse.cs` (the
zero-allocation `ReadOnlySpan<char>`-based parser) together implement a
complete, from-scratch HLS master-playlist parser — it does not use any
external m3u8 library. It parses standard tags
(`#EXT-X-VERSION`, `#EXT-X-STREAM-INF`, `#EXT-X-MEDIA`, `#EXT-X-BYTERANGE`,
`#EXT-X-PROGRAM-DATE-TIME`, `#EXT-X-MAP`, `#EXT-X-SESSION-DATA`) plus
**Twitch-proprietary tags** not in the public HLS spec:
`#EXT-X-TWITCH-LIVE-SEQUENCE`, `#EXT-X-TWITCH-ELAPSED-SECS`,
`#EXT-X-TWITCH-TOTAL-SECS`, `#EXT-X-TWITCH-INFO` (explicitly ignored —
"response related info that we don't need"), and Twitch's own
`STABLE-VARIANT-ID=`/`IVS-NAME=`/`IVS-GROUPS=`/`IVS-VARIANT-SOURCE=`
attributes on `#EXT-X-STREAM-INF` lines (IVS = Twitch's underlying "Interactive
Video Service" infra leaking into the manifest).

**Quality-selection heuristic** (`Models/VideoQualities.cs`,
`Models/M3U8VideoQualities.cs`): "best" quality is not just "highest
resolution" — it's `Qualities.Where(landscape-only).MaxBy(x =>
x.Resolution.Pixels * x.Framerate)`, falling back to pixels-only then
bitrate-only if framerate data is missing/inconsistent across variants (so a
1080p60 stream correctly outranks a 1080p30 stream, which plain
resolution-sorting would treat as equal). A **genuinely non-obvious repair
heuristic**: Twitch's m3u8 response sometimes omits `FRAME-RATE=` entirely,
so the parser falls back to regex-extracting the framerate baked into
Twitch's own `STABLE-VARIANT-ID` string (pattern `p\d+(?:-\w+)?$`, e.g.
`"chunked720p60-alt1"` → `60`) rather than leaving it as an unknown 0 that
would corrupt the pixels\*framerate ranking. Portrait/vertical variants are
tracked via a distinct `VideoOrientation` and excluded from the default
"best"/"worst" picks unless the caller's quality string explicitly contains
`"portrait"` — mirroring the clip-side portrait handling above, i.e. **the
whole codebase treats "does this stream have a portrait variant" as a
first-class, queryable property**, not an edge case.

### Correction: the real Twitch-URL/ID-parsing regexes live in `Tools/IdParse.cs`, not `TwitchRegex.cs`

`Tools/TwitchRegex.cs` (12 lines total, read in full) contains exactly two
regexes and neither is for URL/ID parsing: `UrlTimeCode` (extracts a `?t=`
query-string timecode like `1h2m3s`) and `BitsRegex` (detects cheer-emote
tokens like `Kappa100`/`cheerwal500` embedded in message text, matched
against a fixed alternation of ~30 known Twitch cheermote prefixes). The
file the audit brief was actually looking for is `Tools/IdParse.cs`, fetched
and read separately once this became apparent — it has the three regexes
that parse a raw ID or a pasted URL into a usable Twitch video/clip ID, used
by every CLI download mode:

```csharp
// IdParse.cs — the actual URL/ID regexes (lookbehind on the site pattern, bare ID also matches via ^)
[GeneratedRegex("""(?<=^|twitch\.tv\/videos\/)\d+(?=\/?(?:$|\?))""")]
private static partial Regex VideoId { get; }          // twitch.tv/videos/123456789 or bare "123456789"

[GeneratedRegex("""(?<=^|twitch\.tv\/\w+\/v(?:ideo)?\/)\d+(?=\/?(?:$|\?))""")]
private static partial Regex HighlightId { get; }       // twitch.tv/{channel}/v/123456789 (saved "Highlights")

[GeneratedRegex("""(?<=^|(?:clips\.)?twitch\.tv\/(?:\w+\/clip\/)?)[\w-]+?(?=\/?(?:$|\?))""")]
private static partial Regex ClipId { get; }            // clips.twitch.tv/Slug-abc123 or twitch.tv/ch/clip/Slug-abc123
```

`MatchClipId` additionally rejects an all-digit match (`!clipIdMatch.Value.All(char.IsDigit)`)
so a bare numeric string is never misidentified as a clip slug — clip slugs
are always mixed alphanumeric. `MatchVideoOrClipId` (used by
`chatdownload`, which accepts either) simply tries video-then-clip in order.
Directly reusable as the reference regex shapes for our own Twitch
URL-ingestion input parsing (accepting either a raw ID or any of Twitch's
several URL shapes for VODs/highlights/clips).

### `ChatRenderer.cs` — the burned-in overlay technique, and a companion-alpha-mask trick worth stealing

The rendering technique is: generate chat frames as raw pixel buffers in
memory with SkiaSharp, then **pipe them directly into ffmpeg's stdin as a
raw video stream** — no intermediate PNG sequence, no temp files. The
literal default CLI args (`Modes/Arguments/ChatRenderArgs.cs`) show the
exact ffmpeg invocation shape:

```
input-args  (default): -framerate {fps} -f rawvideo -analyzeduration {max_int} -probesize {max_int} -pix_fmt {pix_fmt} -video_size {width}x{height} -i -
output-args (default): -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p "{save_path}"
```

`{pix_fmt}` is chosen at runtime as `bgra` or `rgba` depending on
`SKImageInfo.PlatformColorType` (Skia's in-memory byte order differs by
platform) — a real, easy-to-miss correctness detail for anyone piping raw
Skia/other-canvas-lib frames into ffmpeg themselves. Default render
canvas is a narrow 350×600 "chat sidebar" column at 30fps; `--update-rate`
(default 0.2s) throttles how often the chat content is actually re-rendered
(`UpdateFrame = max(1, updateRate * framerate)` ticks) — most video frames
just re-emit the last composited chat image, which is why the renderer
maintains a persistent `_animComposedFrame` buffer and only recomposites
when the visible-comment index or an animated emote's frame index actually
changes (`GenerateUpdateFrame`/`AnimCacheIsValid`), rather than redrawing
every element every video frame.

**Reusable technique for our own "burn captions/chat over gameplay footage"
work**: `--generate-mask` produces a **second, parallel grayscale video**
containing just the alpha channel of every rendered frame
(`pix_fmt=gray` for that output), built with hand-written AVX2/SSSE3/NEON
SIMD shuffles that extract every 4th byte (the alpha channel) out of the
RGBA/BGRA frame buffer directly (`SetFrameMask`, with a scalar fallback for
CPUs without those instruction sets). This is a genuinely different — and
better — technique than chroma-key (green screen) for compositing a
transparent overlay onto other footage in a two-pass ffmpeg pipeline
(`overlay` filter driven by a luma/alpha mask video instead of `colorkey`):
it gives per-pixel alpha instead of a hard color-threshold cutout, which
matters for anti-aliased text/emote edges. Directly applicable if we ever
render burned-in AI-generated captions, subtitles, or a chat overlay onto
clips and want soft edges instead of green-screen fringing.

```csharp
// ChatRenderer.cs — GetFfmpegProcess: the raw-frame-to-ffmpeg-stdin pattern
var pixFmt = isMask ? "gray" : SKImageInfo.PlatformColorType == SKColorType.Bgra8888 ? "bgra" : "rgba";
// ... args templated with {fps}/{width}/{height}/{pix_fmt}/{save_path}, then:
var process = new FfmpegProcess { StartInfo = { RedirectStandardInput = true, /* ... */ } };
process.Start();
// later, per frame:
ffmpegStream.Write(frame.GetPixelSpan());   // raw bytes straight into ffmpeg's stdin pipe
```

### `FfmpegMetadata.cs` / `FfmpegConcatList.cs` — confirmed exactly as previously described, plus the literal chapter format

Both files were only described conceptually in the original pass; now
confirmed byte-for-byte. `FfmpegConcatList.SerializeAsync` writes an
`ffconcat version 1.0` header then, per segment, `file '<path-no-query-string>'`
+ optional `stream`/`exact_stream_id 0x100`/`0x101`/`0x102` lines (forcing
explicit PMT stream IDs for `.ts` — `StreamIds.TransportStream` — vs `0x1`/`0x2`
for `.mp4`/AV1 segments, `StreamIds.Mp4`) + `duration <seconds>`. Two
independent `FfmpegMetadata.SerializeAsync` overloads exist — one for VODs
(pulls `owner.displayName`/`login`, description, chapters from
`VideoMomentEdge[]` filtered to `_type == "GAME_CHANGE"`) and one for clips
(pulls `broadcaster`/`curator` as `artist`/clipper, single synthetic chapter
from `GenerateClipChapter`) — both funnel into the same `;FFMETADATA1` +
`[CHAPTER]`/`TIMEBASE=1/1000`/`START=`/`END=`/`title=` block format, escaped
per ffmpeg's metadata escaping rules (`\`, `'`, and literal newlines
backslash-escaped; `=`/`;`/`#` explicitly *not* escaped, with an in-code
comment citing an ffmpeg doc bug: `trac.ffmpeg.org/ticket/11096`).

### `FilenameService.cs` — a fully reusable filename-templating pattern

Token-based template engine directly reusable for our own clip-naming
scheme. Supported placeholders: `{title}`, `{id}`, `{channel}`,
`{channel_id}`, `{clipper}`, `{clipper_id}`, `{date}` (fixed `M-d-yy`),
`{random_string}`, `{trim_start}`/`{trim_end}`/`{trim_length}`/`{length}`
(fixed `HH-mm-ss`), `{views}`, `{game}` — plus **custom-format variants**
(`{date_custom="yyyy-MM-dd"}`, `{trim_start_custom="..."}`, etc.) that accept
an arbitrary .NET format string embedded right in the template and applied
via `IFormattable.ToString(format, provider)`. Templates support subfolders:
any `/` or `\` in the resolved template splits into nested directories
(`GetTemplateSubfolders`), each path segment separately sanitized. Invalid
filename characters are **not just stripped or underscored** — the common
Windows-invalid set (`* " : < > ? | / \`) is remapped to their Unicode
**fullwidth** equivalents (`+0xFEE0`, e.g. `?` → `？`) so a title keeps
looking like itself instead of losing information, with a plain
`Path.GetInvalidFileNameChars()` pass as a final safety net for anything
left over (control codes, etc.). A separate regex (`(?<=\d):(?=\d\d)`)
specifically catches colon-separated-looking-like-a-timestamp substrings
(e.g. a title containing `"3:45"`) and underscores those specifically before
the general fullwidth pass. `GetNonCollidingName` appends `" (1)"`, `" (2)"`,
etc. — the same pattern most OS file managers use.

### CLI layer — confirmed real flags/defaults (medium priority, as scoped)

All four relevant verbs read in full (`Modes/*.cs` + matching
`Modes/Arguments/*.cs`), confirming the flag surface if we ever shell out to
`TwitchDownloaderCLI.exe` directly instead of porting logic:

- **`clipdownload -u <id-or-url> -o <file> [-q quality] [--bandwidth kib] [--encode-metadata]`**
  — `-u` accepts either a bare clip slug or any Twitch clip URL shape
  (parsed via `IdParse.MatchClipId`); `--bandwidth` default `-1` (unthrottled).
- **`videodownload -u <id-or-url> -o <file> [-q quality] [-b begin] [-e end] [-t threads=4] [--trim-mode Exact|Safe] [--oauth token]`**
  — output file *extension* selects behavior: `.m4a` forces `Quality =
  "Audio"` and rejects any other extension outright
  (`"Only MP4 and M4A audio files are supported."`); `--trim-mode Safe` vs
  `Exact` is a real documented tradeoff (Exact can stutter the first/last
  few seconds; Safe pads instead) not mentioned in the original pass;
  default 4 parallel download threads, matching the thread-pool detail
  already documented.
- **`chatdownload -u <id-or-url> -o <file> [--compression None|Gzip] [-E/--embed-images] [--timestamp-format ...] [-t threads=4]`**
  — output extension selects `Json`/`Html`/`Text` format automatically;
  `-E` embeds first-party emotes/badges/cheermotes for fully offline
  re-rendering later (feeds `ChatUpdater`'s embed-replace path, see below).
- **`chatrender -i <json> -o <video> [-w 350] [-h 600] [--framerate 30] [--update-rate 0.2] [--generate-mask] [--sharpening]`**
  — confirmed default 350×600 canvas, 30fps, 0.2s update rate;
  `--sharpening` literally appends `-filter_complex
  "smartblur=lr=1:ls=-1.0"` onto the input args string.
- **`tsmerge -i <file-list-or-m3u8> -o <file>`** — the standalone raw-concat
  tool described above, explicitly logged as experimental at every run.

### `ChatUpdater.cs` — re-syncing/trimming an existing chat download (not previously documented)

Confirms this is a genuinely separate operation from both download and
render: it loads a previously-downloaded chat JSON, optionally re-fetches
fresh video/clip metadata and chapters from Twitch (same GQL calls as
download), optionally widens or narrows the trim window — **fetching only
the newly-uncovered time range** via a fresh `ChatDownloader` sub-call
(`GetTrimDownloadOptions`) rather than re-downloading the whole VOD's chat,
then merges the new comments into the existing set via a
`HashSet<Comment>` keyed on comment ID (`CommentIdEqualityComparer`) to
dedupe overlap, re-sorted by offset — and optionally re-embeds or replaces
emote/badge/bit image data. This "expand a previously-cached chat log by
only fetching the delta" pattern is directly reusable if our own pipeline
ever needs to re-process a VOD with a different/wider clip time range
without re-downloading the entire chat history from scratch.

### Files intentionally not deep-read this pass

Per the audit's own priority scoping: `TwitchDownloaderWPF/*` (GUI
code-behind, low priority, skipped — nothing here would change ingestion or
detection strategy), all `*.Tests` projects, XAML files, `Themes/`/
`Translations/`/`Images/` assets, publish profiles, `.github/` workflow
config, and README translations. Within `TwitchDownloaderCore`, the
low-level `Extensions/*.cs` helpers (span/string/dictionary utility
extensions) and `Models/Render/*.cs` (small POCO structs backing
`ChatRenderer`) were referenced/skimmed as needed to understand the files
above but not independently summarized — they're plumbing, not technique.

---

## Repo 2 — `nirvagold/stream-clipper`

**Tauri + Rust + Svelte desktop app · https://github.com/nirvagold/stream-clipper**

A native desktop app (not a cloud/server pipeline) combining audio-track
analysis and chat-density spikes to auto-detect highlights, sold as a
freemium product (free tier: audio-only detection, 5-clip cap, random
subsampling if more are found, 720p+watermark export; Pro tier, license-gated:
chat detection unlocked, unlimited clips, up to 4K, vertical crop, fades,
WebM). Read `src-tauri/src/chat/{analyzer,parser}.rs`,
`src-tauri/src/audio/{analyzer,vad}.rs`, `src-tauri/src/highlight/{scorer,merger}.rs`,
`src-tauri/src/commands/analyze.rs`, `src-tauri/src/video/clipper.rs`, and
`src-tauri/src/pro/_c.rs` (obfuscated but readable — see below) in full.

### Real technique

**No LLM anywhere in detection.** This is the single most important structural
fact about this repo: it is a fully statistical/heuristic multi-signal
detector — everything runs locally, offline, with zero AI API cost, and it's
a real shipped commercial product, not a toy. Two independent signal
generators feed a combiner:

**Audio signal (`audio/analyzer.rs` + `audio/vad.rs`):**
1. Extracts audio to WAV, chunks into fixed-duration windows (`chunk_duration`,
   e.g. 1-2s), computes RMS energy and peak amplitude per chunk (parallelized
   with `rayon`).
2. Runs **WebRTC VAD** (`webrtc-vad` crate, Google's actual production voice-
   activity-detection algorithm, in `VadMode::Aggressive`) over the raw
   samples in 30ms frames, resampling to 16kHz first if the source isn't one
   of WebRTC VAD's four supported native rates (8/16/32/48kHz) via simple
   linear interpolation. This produces a `voice_ratio` (0.0-1.0) per chunk —
   **the explicit design goal is separating "someone is talking/reacting"
   from "a loud game sound effect happened,"** which is a real, documented
   false-positive class for naive volume-threshold clippers (the repo's own
   comments call this out directly: `// IMPROVED with VAD ... Reduces false
   positives by detecting human voice vs game sounds`).
3. Spike detection is **multi-criteria, not single-threshold**: a chunk is a
   candidate only if it's above a percentile-based dynamic threshold (75th-95th
   percentile of RMS depending on a user "sensitivity" 0-4 setting) AND at
   least one of: sudden delta from previous chunk (>1.5x average delta),
   high crest factor (peak/RMS > 2.0, indicating a transient/impact sound
   rather than sustained noise), sustained energy in the next chunk, or
   significantly above baseline+1.5*stddev. **Voice detection (VAD) is
   weighted as the single biggest quality-score contributor (+30 of ~100
   possible points)** — explicit design choice that a streamer's vocal
   reaction is the strongest highlight signal, stronger than raw loudness.
4. Adjacent candidate chunks within a configurable `merge_gap` are merged into
   one spike; a spike must clear both a minimum duration and a minimum
   quality score (40/100) to survive.

**Chat signal (`chat/analyzer.rs`):**
1. Parses chat into fixed time windows (`window_size`, default 5s), computing
   per-window: message count, unique user count, keyword match count (against
   a configurable hype-word list, default `POG`/`POGGERS`/`OMG`/`WTF`/`CLIP
   IT`/`GG`), emote density (fraction of messages containing an emote — note
   this is the exact field lifted from TwitchDownloader's chat JSON, see
   Repo 1), and all-caps character ratio.
2. Baseline is the **median** message-rate across all windows (robust to
   outlier spikes skewing a mean-based baseline); threshold =
   `baseline * rate_multiplier` (default 3x).
3. A window is a spike if it clears the rate threshold **OR** hits a keyword
   count threshold **OR** hits an emote-density threshold (three independent
   OR'd triggers, not just one metric) — adjacent spike windows merge.
4. Score = `rate_score (0-70, scaled off how far above baseline) + keyword_score
   (0-30, 10 pts/keyword match, capped)`.

**Combiner (`highlight/scorer.rs` + `highlight/merger.rs`):**
1. Every audio spike is checked for time-overlap against every chat spike
   (naive O(n*m) pairwise overlap check — fine at this scale). Overlapping
   pairs become a **"Combo" highlight**: `score = (audio.score * audio_weight
   + chat.score * chat_weight) * combo_bonus` (default weights 0.6/0.4,
   `combo_bonus` = 1.5x) — i.e. **a 50% score bonus specifically for moments
   where both independent signals agree**, which is a real, concrete way to
   boost confidence without an LLM call. Audio-only and chat-only spikes that
   don't overlap survive as lower-confidence singleton highlights.
2. A separate merge pass (`merger.rs`) collapses highlights whose time ranges
   overlap by more than a configurable threshold (default 50% of the shorter
   clip's duration), keeping the higher score and unioning the "reasons" list.
3. **Free-tier dark pattern worth knowing about (not worth copying)**: when
   there are more highlights than the free tier's cap, instead of truncating
   to the top-N by score, it truncates to a **random** N using a
   `SystemTime`-seeded RNG — explicitly so free users get *different* clips
   each time they re-run analysis on the same video, an upsell mechanic to
   make Pro's "see everything" feel valuable. Confirmed directly in code
   comments: `// This gives free users different clips each time they
   analyze`.

### Chat format support (worth knowing for our own ingestion)

`chat/parser.rs` auto-detects and parses **three** chat log formats:
Twitch JSON (TwitchDownloader's schema, detected by presence of a top-level
`comments` array), YouTube live-chat JSON (yt-dlp's `replayChatItemAction`
array format), and a generic `[HH:MM:SS] username: message` text format via
regex. This is useful confirmation that a small, format-tolerant parser
covering these three shapes is sufficient to cover the realistic universe of
chat-log inputs a clipping tool will actually receive.

### Pro-tier gating architecture

`src-tauri/src/pro/mod.rs` and `_c.rs`/`_v.rs` are a deliberately
variable-name-obfuscated (but not logically different) copy of the free
chat-analysis code, gated behind `runtime_license_check()`. Not relevant to
detection technique, but a real example of "same algorithm, licensed
differently" — worth knowing if we ever consider a similar tiering model for
distribution, though not our immediate concern.

### Concrete reusable pattern for our project

- **Port directly**: the multi-criteria spike-detection logic (threshold AND
  at-least-one-of{delta, crest-factor, sustained, baseline+stddev}) is
  straightforward to reimplement in Python against `librosa`/`numpy` RMS
  arrays — meaningfully better than the "fixed dB threshold" approach already
  flagged as too-simple in `verified_tools_catalog.md`
  ([`porplax/auto-highlighter`](https://github.com/porplax/auto-highlighter)).
- **Port directly**: WebRTC VAD is available as a Python binding
  (`webrtcvad` on PyPI, same underlying Google C library) — adding voice-vs-
  game-sound filtering to any audio-spike detector we build is a low-effort,
  high-value addition directly validated by this repo's own stated
  false-positive-reduction rationale.
- **Adapt**: the combo-bonus overlap-scoring pattern (audio spike + chat
  spike overlapping in time = confidence multiplier) is a **zero-LLM-cost**
  way to pre-rank candidate moments before ever calling an LLM — see the
  cross-repo synthesis below for how this plugs into a hybrid pipeline.
- **Do not copy**: the random-truncation free-tier dark pattern. Noted only
  because it's a real, observed monetization trick, not because it's a
  technique worth reusing.

### Code excerpt worth keeping verbatim

The combo-bonus scoring rule — the concrete formula for "two independent
signals agreeing is worth more than either alone," reusable directly in a
Python reimplementation:

```rust
// highlight/scorer.rs
if overlaps(audio.start_secs, audio.end_secs, chat.start_secs, chat.end_secs) {
    let combined_score = (audio.score * settings.audio_weight
        + chat.score * settings.chat_weight)
        * settings.combo_bonus;   // default 1.5 — the "signals agree" bonus
    // highlight_type = Combo
}
```

---

## Repo 3 — `metaleey/AI-auto-segment-edit-video-pipeline`

**Python (Vue.js GUI + FastAPI backend + CLI) · https://github.com/metaleey/AI-auto-segment-edit-video-pipeline**

A full self-hosted pipeline: ASR → LLM semantic segmentation → tagging →
optional external "value" scoring → sampling → ffmpeg merge. Built for
Chinese livestream e-commerce content (ASR is FunASR's `paraformer-zh`; the
default LLM is Alibaba DashScope/Qwen; default tag taxonomy is retail/livestream-
selling categories like "产品演示" [product demo] / "购买引导" [purchase
guidance]) — the domain doesn't transfer to Twitch gaming content directly,
but the **architecture is fully domain-agnostic and directly relevant**. Read
`videoclip/core/{chunk_processor,llm_analyzer,tag_normalizer,clip_boundary,
value_analyzer,sampler}.py`, `backend/services/merge_service.py`,
`config-template.yaml`, `docs/value-scoring.md`, and `srt_gen/srt_predict_v2.py`
in full.

### Real technique

**Pipeline shape**: ASR (FunASR paraformer-zh, GPU/MPS/CPU auto-detected) →
SRT with custom text-timestamp aligner → chunked LLM semantic segmentation →
tag normalization → optional value-scoring against external engagement data →
sampling (random, tag-filtered, or value-ranked) → ffmpeg clip+concat. CLI
commands (`main.py process|analyze|sample-from|srt-to-json|value-score`) let
you re-enter the pipeline at any stage using cached intermediate artifacts
(`segments.json`), avoiding redundant ASR/LLM calls on iteration — a good
cost-control habit already partially reflected in our own project's asset-
reuse memory note.

**1. Chunking strategy — two modes, and the better one avoids a common failure
mode:**

- Old/simple mode: fixed sliding time-windows (e.g. 10min windows, 2min
  overlap) — straightforward but risks the LLM proposing segments that then
  get deduplicated across overlapping windows.
- **Better mode** (`create_duration_based_chunks`, the current default):
  accumulates SRT entries into chunks targeting a **40-90 second duration
  band** (configurable min/target/max), greedily deciding at each subtitle
  boundary whether adding the next entry gets the chunk *closer* to the
  target duration than stopping now does — i.e. a true target-seeking greedy
  packer, not a fixed-size window. Combined with an optional
  **`single_segment_per_chunk` mode**: instead of letting the LLM propose
  multiple sub-segments per chunk (which risks fragmenting into many
  sub-6-second clips), it forces exactly one segment per chunk and **snaps
  that segment's time boundaries to the chunk's own boundaries**, keeping
  the LLM's semantic output (title/tags/summary) but overriding its
  timestamps. This directly avoids a fragmentation failure mode that a naive
  "ask the LLM for segments" prompt is prone to.

**2. LLM segmentation prompt — a genuinely different sophistication axis than
"score a transcript window 0-100":**

Unlike the simpler score-a-window approach already documented elsewhere in
our research (video 1's 6-dimension moment scorer, [`mutonby/openshorts`](https://github.com/mutonby/openshorts)'s 2-second-test
scorer — both *score* pre-chunked windows), this repo's core LLM call does
**structural interpretation, not scoring**: given a raw SRT block, it asks
for JSON `segments[]` each with `title`, `tags[]`, `start_ms`, `end_ms`,
`summary` — i.e. the LLM is choosing *where the semantic boundaries are*
within a block of text, not just judging a pre-cut window's quality. The
prompt explicitly instructs "don't cut in the middle of a topic" and derives
the target segment count from `duration / target_seconds` inline in the
prompt text itself (a neat trick: telling the LLM the arithmetic instead of
hoping it infers a reasonable count). It also enforces a **hard-constrained
tag vocabulary appended to every prompt** (see next section) rather than
relying on the LLM's freeform tag choices, and clamps any returned
`start_ms`/`end_ms` that falls outside the input's actual time range
server-side after the fact (defense against LLM boundary-hallucination).

**3. Tag normalization — controlled vocabulary + synonym table + keyword
fallback, applied post-hoc regardless of what the LLM returns:**

`tag_normalizer.py` maintains: (a) a fixed allowed-tag list (15 default
categories) injected into every prompt as a hard constraint ("tags 只能从以下
一级标签中选择" — "tags may ONLY be chosen from this list"); (b) a ~150-entry
hardcoded synonym dictionary mapping likely LLM paraphrases to canonical tags
(e.g. "产品亮点"/"产品卖点"/"产品说明" all collapse to "产品介绍"); (c) a
keyword-substring fallback inference table for anything that matches neither
the allowed list nor the synonym table verbatim; (d) a final fallback tag
("其他"/"Other") if nothing matches. This three-layer normalization
(constrain the prompt → synonym-collapse the response → keyword-infer
whatever's left → fallback) is a materially more robust approach to keeping
LLM-generated categorical tags consistent across thousands of segments than
just trusting the LLM's own consistency, which is a real, common failure
mode with freeform LLM tagging at scale.

**4. Clip boundary alignment — snapping cuts to natural speech pauses, a
post-processing step none of our other sources described:**

`clip_boundary.py` takes the LLM's raw `start_ms`/`end_ms` and searches
nearby SRT entries (within configurable max shift windows, default up to
8s earlier for start / 12s later for end) for a **"natural" cut point** —
defined as either a real silence gap between subtitle entries (≥220ms by
default) or a subtitle line ending in terminal punctuation (。！？!?…) with at
least a smaller "soft gap." It explicitly avoids starting a clip on a line
beginning with a connector word (然后/但是/不过/所以/因为... — "then/but/
however/so/because...") even if the timing would otherwise allow it, since
that reads as an incomplete thought. It also adds small fixed head/tail pads
(180ms/520ms) to avoid clipping the first/last syllable. This is a concrete,
reusable answer to "how do you avoid clips that start or end mid-sentence"
— a real problem with naive "cut exactly where the LLM said" pipelines, and
one none of our previously-reviewed repos addressed explicitly.

**5. Value scoring — the most structurally novel idea in this repo: decouple
"where are the topic boundaries" from "which of these moments actually
matter," using real external engagement data instead of asking the LLM to
judge both at once.**

`value_analyzer.py` ingests a **separate CSV/Excel time-series** of live
engagement metrics (for this repo's e-commerce domain: transaction count,
comment count, average watch duration, viewer count — sampled at some
external cadence, e.g. per-minute), keyed to real-world timestamps via a
`csv_start_time` anchor (the live-stream time that corresponds to video 0:00).
For each LLM-identified segment, it converts the segment's video-relative
`start_ms`/`end_ms` into that same real-world timeline, finds all CSV records
falling in that window (with a **tolerance-expanding variant**,
`analyze_segment_with_tolerance`, that rounds the window out to full CSV
sampling-interval boundaries plus a configurable buffer — necessary because
minute-level external data rarely aligns exactly with second-level video
segment boundaries), and computes a **weighted, per-metric-normalized score**
(each metric normalized 0-100 against its own max value across the whole
stream, then combined via configurable weights, e.g. default
`0.4*transactions + 0.3*comments + 0.2*watch_duration + 0.1*viewers`). This
score is written back onto the segment as `value_score` and can drive
downstream sampling (`sampler.py`'s `sample_by_value`, with a `topk-random`
mode that randomly samples from the top-K highest-scoring segments rather
than deterministically taking the literal top-N — explicitly for output
variety across repeated runs, plus an optional `diversify_tags` pass that
prefers not to pick multiple segments sharing the same tag).

**The direct Twitch-relevant analogy**: swap this repo's e-commerce CSV
(transactions/comments/watch-time/viewers) for a Twitch-native equivalent
time series — chat messages-per-minute, concurrent viewer count if available,
sub/bit/cheer events, raid events — sampled independently of any transcript
analysis, and the exact same `video_ms_to_csv_time` + tolerance-window +
weighted-normalize-and-combine logic applies unchanged. This is a genuinely
reusable **pattern**, not domain-specific code.

### Concrete reusable pattern for our project

- **Port directly**: the duration-window chunking + `single_segment_per_chunk`
  boundary-snapping logic (`chunk_processor.py`) as a defense against
  over-fragmented short clips from LLM-based segmentation — directly
  applicable regardless of which LLM we use for scoring.
- **Port directly**: the clip-boundary natural-pause alignment algorithm
  (`clip_boundary.py`) as a post-processing pass on any clip boundaries our
  pipeline produces (LLM-given or otherwise) before handing them to ffmpeg —
  this is a real gap in every other source reviewed so far.
- **Port directly**: the three-layer tag-normalization pattern
  (prompt-constrain → synonym-collapse → keyword-infer → fallback) for
  whatever categorical taxonomy we end up tagging clips with (moment type,
  content category, etc.) — meaningfully more robust than trusting the LLM's
  raw tag output.
- **Adapt**: the value-scoring module's architecture (external time-series →
  timestamp-join → tolerance-window → weighted-normalize) is the concrete
  template for building our own "cross-reference chat velocity / viewer
  count against LLM-found semantic segments" scoring stage — see synthesis
  below for exactly how this composes with the other two repos' findings.

### Code excerpt worth keeping verbatim

The tolerance-expanding time-join — the core trick for reconciling a
coarse-grained external metrics feed (per-minute Twitch chat/viewer stats,
if that's ever the sampling rate we get) against fine-grained video segment
timestamps:

```python
# value_analyzer.py — analyze_segment_with_tolerance
# Expand segment time boundaries to minute boundaries so a segment
# doesn't miss adjacent low-resolution external records entirely.
expanded_start_s = (int(start_s) // 60) * 60 - tolerance_seconds
expanded_end_s = ((int(end_s) + 59) // 60) * 60 + tolerance_seconds
```

And the prompt-level tag constraint injection — the concrete string appended
to every LLM call to force a controlled vocabulary rather than trusting the
model's own consistency:

```python
# llm_analyzer.py — _append_tag_constraints
f"{prompt}\n\n"
"【标签约束（必须遵守）】\n"                      # "[Tag constraint — MUST follow]"
f"- tags 只能从以下一级标签中选择：{allowed}\n"    # "tags may ONLY be chosen from: {list}"
f"- 每个片段 tags 数量限制为 1-{max_tags} 个\n"
"- 严禁创造新标签、同义改写或近义词变体\n"          # "strictly forbidden to invent new tags"
f"- 无法判断时请使用：{fallback_tag}\n"
```

---

## Audit pass — additional files read [2026-07-29]

Honest coverage check on Repos 2 and 3 above (Repo 1, `lay295/TwitchDownloader`, is being audited
separately given its size — see the note at the end of this section). The original pass on
`nirvagold/stream-clipper` read 11 of 109 files (all the real detection-signal files, but none of
the ffmpeg-wrapper/license/wiring files); the original pass on `metaleey/...` read 10 of 85 files
(all the semantic-segmentation core, but not the video-cutting engine, the orchestration service,
or the CJK/English text-timestamp aligner it explicitly names but never actually reads). Files
fetched via `gh api repos/<owner>/<repo>/contents/<path>?ref=main` and read in full.

### stream-clipper — ffmpeg wrapper, export commands, and the license/anti-crack layer

Files read in full: `src-tauri/src/audio/extractor.rs`, `src-tauri/src/utils/ffmpeg.rs`,
`src-tauri/src/utils/time.rs`, `src-tauri/src/commands/export.rs`,
`src-tauri/src/license/validator.rs`, `src-tauri/src/pro/_v.rs`, `src-tauri/src/lib.rs`,
`src-tauri/src/video/info.rs`.

**`utils/ffmpeg.rs` is the actual FFmpeg command-building layer underneath everything else in this
repo** (previously only referenced conceptually). Real details: the app **ships a bundled,
platform-specific FFmpeg sidecar binary** (`ffmpeg-x86_64-pc-windows-msvc.exe` etc., resolved
relative to the running executable's own directory via `std::env::current_exe()`), falling back to
a system-PATH `ffmpeg` only in debug builds or if no sidecar is found — i.e. this is a
self-contained, no-install-required desktop app, not one that assumes the user has FFmpeg set up.
`extract_audio` converts to 22.05kHz mono PCM16 WAV (a lower sample rate than most ASR
recommendations — WebRTC VAD and the RMS analysis this repo does don't need speech-recognition-
grade audio quality, so this is a real, deliberate resource-saving choice, not an oversight).
`cut_clip` supports both a `-c copy` fast path and a full `libx264`/`aac` re-encode path
(`preset fast`, `crf 23`) gated by a `reencode: bool` flag — the caller decides per-clip whether
speed or seek-accuracy matters more, the same trade-off documented in TwitchDownloader's segment
handling. Video duration is obtained by parsing FFmpeg's own stderr `Duration:` line with a
hand-written parser, not `ffprobe` — one less external binary dependency for a bundled desktop app
to worry about.

**`lib.rs` confirms this is a real, complete Tauri app wired end-to-end**, not a partial prototype:
the full `tauri::Builder` invoke-handler list registers video-info, chat-info, analyze, cancel,
export, preview, config, license commands, plus an `on_window_event` cleanup hook that wipes the
app's entire temp directory (`std::env::temp_dir().join("stream-clipper")`) when the window closes
— a real, complete resource-cleanup lifecycle most of the research repos in this project don't
bother with.

**`commands/export.rs` reveals real UX-facing behavior not documented before**: exporting emits
live progress events over Tauri's event bus (`window.emit("export-progress", ...)`) so the
frontend can show a real progress bar per clip, not just a blocking spinner; there's a global
`AtomicBool` cancellation flag checked between each clip so a mid-export cancel actually stops
further clips rather than just hiding the UI; and `preview_clip` reuses the exact same
`export_clip` function as real export, just pointed at a temp directory with fixed 3s/2s
before/after padding — i.e. "preview" isn't a separate lightweight code path, it's the real export
pipeline run once on one clip.

**`license/validator.rs` and `pro/_v.rs` are a real, deliberate anti-crack design worth documenting
concretely** — the original pass noted `pro/_c.rs` (the Pro chat-analysis code) was "obfuscated but
readable" but didn't read the license-validation machinery itself or the separate Pro
*video-effects* gating module (`_v.rs`, distinct from `_c.rs` — vertical-crop/fade/high-res/
no-watermark gating, not chat analysis). Concrete techniques found:
- License keys are XOR-obfuscated even as *source constants* (`_x`/`_y` functions XOR magic values
  against hardcoded constants at compile time) and sensitive strings are stored as byte arrays
  built via a macro (`_s!(115, 116, 114, ...)` → `"stream-clipper"`) rather than string literals —
  both explicitly aimed at making the compiled binary harder to string-search or pattern-match for
  a cracker, not at making the logic more secure against a determined attacker.
- The on-disk license file is encrypted with a key derived from the **machine ID** (hashed via
  `DefaultHasher`, rotated into a 32-byte keystream) XORed against the license JSON, with an
  index-dependent extra XOR term (`(i as u8).wrapping_mul(7)`) and a trailing checksum — i.e. a
  license file copied to a different machine fails to decrypt/validate (`l.machine_id != cm`
  check in `_v()`), a real (if not cryptographically strong) node-locking mechanism.
- License keys themselves are a real, checksummed format: `XXXXX-XXXXX-XXXXX-XXXXX` (23 chars incl.
  dashes), first 4 chars of the de-dashed string must be one of 4 valid prefixes (`SCPR`/`STRM`/
  `CLIP`/`PRO1`), and the last 4 hex chars are a weighted rolling checksum
  (`s += char_value * ((position+1)*7)`, mod `0xFFFF`) over the preceding 16 — a real, simple but
  functioning offline license-key validation scheme with no server round-trip needed.
- Every function is `#[inline(never)]` and several call `std::hint::black_box(...)` on intermediate
  booleans — both are real anti-optimization techniques specifically to stop the Rust compiler from
  inlining/collapsing the license check into something a binary patcher could trivially find and
  bypass (`black_box` prevents LLVM from proving a value is unused and eliminating the check
  entirely).
- `requires_pro()` is a flat allow-list of feature-flag strings (`"chat_detection"`,
  `"vertical_crop"`, `"custom_keywords"`, `"unlimited_clips"`, `"high_resolution"`, `"no_watermark"`,
  `"batch_export"`, `"fade_effects"`, `"webm_format"`) — confirms and completes the free/Pro feature
  boundary the original pass only partially described from the chat-analysis side; the video side
  gates resolution above 720p and any format other than mp4 behind the same `runtime_license_check()`.

Not a moment-detection technique, so not something to port, but worth flagging for this project's
own future distribution decisions if a paid tier is ever considered: this is a real, concrete
example of what "reasonably serious client-side license gating" looks like in a shipped Tauri app,
including its explicit tradeoffs (still fundamentally crackable since validation runs in the user's
own process — the obfuscation only raises the bar against casual/automated cracking, not a
determined reverse-engineer).

**Completion note on stream-clipper's remaining files** (closing out the last real gap in this
repo): the only files left unread after the two passes above were the `types.rs`/`mod.rs` structs
in each module (`audio/types.rs`, `chat/types.rs`, `highlight/types.rs`, `video/types.rs`,
`commands/config.rs`, `commands/license.rs`, `license/mod.rs`, plus seven trivial `mod.rs`
re-export files and a 6-line `main.rs`). All were read directly. None contain detection logic —
they're pure data/settings definitions — but they pin down several real default constants that
were previously only inferable from the scoring code, worth having exact:

- `ChatAnalyzeSettings::default()`: `rate_multiplier: 3.0`, `window_size: 5.0`s,
  `keyword_threshold: 3`, `emote_threshold: 0.3`, and **the full 20-word hype-keyword list**
  (previously only sampled): `POG, POGGERS, POGU, LETS GO, LET'S GO, OMG, WTF, CLIP IT, CLIP THAT,
  GG, GGWP, HOLY, INSANE, CRAZY, NO WAY, NOWAY, KEKW, LULW, OMEGALUL, HYPE`.
- `AudioAnalyzeSettings::default()`: `sensitivity: 2.0`, `min_duration: 2.0`s, `merge_gap: 3.0`s,
  `chunk_duration: 0.5`s, `sample_rate: 22050`Hz — confirms the 22.05kHz audio-extraction rate
  documented earlier isn't a random choice, it's the same number wired through as the analysis
  chunk's own default sample rate end-to-end.
- `HighlightSettings::default()`: `audio_weight: 0.6`, `chat_weight: 0.4`, `combo_bonus: 1.5`,
  `max_clips: None` — the exact default weights behind the combo-bonus formula already documented
  above, now confirmed as the shipped defaults rather than just example values.
- `ExportSettings::default()`: `format: Mp4`, `resolution: R1080p`, `padding_before: 3.0`s,
  `padding_after: 2.0`s, `vertical_crop/fade_effect/add_watermark: false` — matches the
  `preview_clip` padding values already documented, confirming preview and default export share one
  settings shape (`ClipExport` / `ExportSettings` in `video/types.rs`).
- **`license/mod.rs`'s `get_machine_id()` is the actual node-locking input** the encryption/validation
  logic (documented above) depends on, and it wasn't previously shown: it hashes
  `"{username}:{hostname}:{platform}:{arch}"` via `DefaultHasher` and hex-encodes the result — i.e.
  the "machine ID" is a hash of OS username + hostname + OS + CPU arch, not a hardware serial/MAC
  address. This is a meaningfully weaker node-lock than it might sound (reinstalling the OS with the
  same username/hostname on the same machine reproduces the same ID; a VM or container with matched
  username/hostname would too) — worth knowing precisely if this pattern is ever reused, since a
  hardware-derived ID (disk serial, TPM-backed key) would be a stronger anchor.
- `commands/config.rs` confirms settings persist to `{config_dir}/stream-clipper/config.json` (not
  the OS-registry/keychain) via plain `serde_json`, and doubles as the file/folder picker command
  layer (`pick_folder`/`pick_file`, using `tauri_plugin_dialog`'s async callback-to-channel bridge
  pattern — a real, reusable idiom for turning a callback-based native dialog API into an `async fn`
  Tauri command: spawn an `mpsc::channel`, hand the sender into the dialog's callback, `.recv()` on
  the receiver after invoking the picker).
- `commands/license.rs` is a 23-line pass-through wrapping `license::{load_license, activate_license,
  deactivate_license}` as `#[tauri::command]`s — no logic of its own.

This closes out `nirvagold/stream-clipper`: every non-frontend, non-icon/asset file in
`src-tauri/src/` has now been read in full across the original pass and the two audit passes above.
Only the Svelte/TypeScript frontend component files remain unread, which is an intentional,
reasonable scope cut (this project's research interest is the detection/ingestion logic, which
lives entirely in the Rust backend; the Svelte components are presentation layer over the same
Tauri-command surface already fully documented).

### metaleey/AI-auto-segment-edit-video-pipeline — the video-cutting engine and text/timestamp aligner

Files read in full: `videoclip/core/video.py` (711 lines — the actual FFmpeg cutting/merging
engine, previously unread), `videoclip/core/audio.py`, `videoclip/core/srt_generator.py`,
`backend/services/processing_service.py`, `srt_gen/text_timestamp_aligner.py`; skimmed
`main.py`'s CLI option definitions and `videoclip/models/schemas.py`'s dataclasses for structure.

**`videoclip/core/video.py`'s `VideoProcessor` is a materially more sophisticated FFmpeg
encoding layer than anything else surveyed in this research — this is a real gap the original
pass missed by only reading the LLM-segmentation and tag-normalization modules.** Concrete,
previously-undocumented techniques:
- **Automatic hardware-encoder selection with software fallback.** On startup it probes
  `ffmpeg -encoders` output and picks, in order of preference, NVENC → Intel QSV → AMD AMF (or
  `h264_videotoolbox` unconditionally on macOS), each mapped to its own hardware-accel input flag
  (`cuda`, `qsv`, `d3d11va` on Windows for AMF, `videotoolbox`). If the hardware encode command
  actually fails at runtime, `_run_encode_with_fallback` retries first with `-hwaccel` stripped
  (software decode, hardware encode), and if that still fails, retries a second time forcing
  `libx264` entirely — a real three-tier degradation path (`hw decode+encode` → `sw decode + hw
  encode` → `full software`) none of the other repos in this research implement.
- **A "seek preroll" technique for multi-input concat that avoids visible seam stutter**:
  `_build_seek_window` seeks `seek_preroll_seconds` (default 6.0s) *before* each segment's actual
  start time, then trims precisely to the real start with `setpts=PTS-STARTPTS` inside a filter
  graph — giving the decoder enough leading reference frames to stabilize before the real content
  starts, rather than seeking to the exact frame and risking a corrupt/blocky first frame from
  seeking mid-GOP.
- **`merge_segments_direct` builds one single-pass FFmpeg command with N independent seeked inputs
  feeding a `concat` filter** (not N separate cut files + a second concat pass): each segment gets
  its own `-ss`/`-t`/`-i` triple (so each seeks independently and cheaply rather than one input
  being sequentially decoded start-to-finish), then a `filter_complex` chain trims/resets
  timestamps per segment and concatenates video+audio streams together, with a final
  `aresample=async=1:first_pts=0` to fix audio drift at the seams. This is a genuinely different
  and more efficient architecture than "cut each clip to its own file, then ffmpeg-concat the
  files" (the pattern used by every other repo in this research, including TwitchDownloader and
  twitch-clip-miner) — it does the whole multi-clip extraction-and-stitch in one ffmpeg process
  without ever writing intermediate per-clip files to disk, which matters at scale (many short
  clips from a multi-hour VOD).
- Two independent export paths are supported and can run together: `clip_segments` (cut each
  segment to its own file, optionally re-encoded for frame-accuracy) and `merge_segments_direct`/
  `compose_segments` (direct one-pass stitch) — a project can get both a single "highlights reel"
  output and individual per-clip files from one `compose_segments(..., save_clips_dir=...)` call.
- `merge_videos`/`merge_and_cleanup` (the simpler, already-cut-files case) use the standard
  `ffmpeg -f concat -safe 0` file-list approach (same technique TwitchDownloader uses for its own
  segment merging), with real filename sanitization for human-readable clip names
  (`"".join(c if c.isalnum() or c in (' ','-','_') else '_' for c in title)`).

**`srt_gen/text_timestamp_aligner.py` is the "custom text-timestamp aligner" the original
write-up named but never actually read — it solves a real, non-obvious problem specific to
mixed-language ASR output.** FunASR's paraformer model emits one timestamp per *token*, but what
counts as a token differs by script: an English word is one token/one timestamp, while each
individual Chinese character gets its own token/timestamp, and punctuation gets none. Naively
zipping `text` characters against a flat `timestamps` array breaks the moment any English word
appears in otherwise-Chinese text, because the lengths silently stop matching. This module's
`tokenize_for_alignment()` re-derives the same token boundaries paraformer would have used purely
from the text (walking character-by-character: collect a full run of ASCII letters as one English
word-token, but split any CJK/other character out as its own token, skipping punctuation/spaces
entirely) so it can be zipped 1:1 against the ASR's own timestamp array. `get_text_with_timestamps`
then builds a full per-character timestamp map (an English word's timestamp is broadcast to every
character inside it), and `extract_segment_with_timestamps` uses that map to look up the correct
start/end time for an arbitrary text substring by scanning forward from the substring's first
timestamped character and backward from its last. **This is a concrete, reusable pattern for any
pipeline mixing multiple ASR token granularities** (e.g. any ASR that timestamps at the
word/subword level inconsistently across languages) — not directly relevant to Twitch English-only
content, but a real technique worth remembering if this project ever needs to align LLM-chosen
text spans back to ASR timestamps and the two don't tokenize identically.

**`backend/services/processing_service.py` confirms the FastAPI backend is a genuine async job
wrapper around the same `VideoClipProcessor` core used by the CLI** — not a separate
reimplementation. It threads `log_callback`/`progress_callback` closures into the processor so a
long-running video job can push live progress (`processing_progress`, `processing_step` columns)
and structured log lines into SQLite as it runs, polled by a frontend, and separately mirrors the
same result to a flat `job_dir/task_info.json` + `segments.json` on disk — i.e. every job is
recoverable/inspectable from disk even without querying the database, a reasonable durability
pattern for a self-hosted tool.

**CLI confirmation (`main.py`, skimmed for structure only): built on `click`, not `argparse`.**
The main `process` subcommand exposes `--by-value`/`--by-value-mode {strict,topk-random}`/
`--value-top-k` (the value-scoring re-rank documented in the original write-up), plus two flags not
previously called out: `--tag-diversity/--no-tag-diversity` (defaults **on**) and
`--align-boundaries/--no-align-boundaries` — confirming the clip-boundary natural-pause snapping
and tag-diversification sampling documented earlier in this file are real, user-facing, and
on-by-default behaviors, not just internal implementation details.

None of this changes the existing three-stage-funnel synthesis recommendation, but it adds one
concrete implementation detail worth folding in: if/when this project builds its own multi-clip
ffmpeg export step, `metaleey`'s single-pass multi-input-seek-and-concat-filter technique
(`merge_segments_direct`) is a better default than the cut-then-concat-files pattern every other
repo in this research uses, especially for producing a single "best-of" highlights reel from many
short clips out of one long VOD.

**Completion note on metaleey's remaining files**, read directly to close out this repo's coverage:
`videoclip/config.py` (`DEFAULT_CONFIG`, 217 lines) and `videoclip/models/schemas.py` (dataclasses,
149 lines), full read; `main.py`'s `process` command body re-checked beyond the options already
listed. `backend/main.py`, `backend/config.py`, and the `backend/models`/`backend/schemas`
CRUD-boilerplate pairs were intentionally not deep-read — they're standard FastAPI
request/response/DB-row shims with no detection or pipeline logic beyond what
`processing_service.py` (already read in full) already exposes; skipping them matches this
project's own stated audit standard (pure plumbing, not application logic).

`videoclip/config.py`'s `DEFAULT_CONFIG` is the single source of truth for nearly every constant
mentioned elsewhere in this file, and reading it directly surfaces two real corrections to what
was written earlier in this same section, plus several previously-unconfirmed exact values:

- **Correction — clip-boundary pad values.** The original write-up (this file's Repo 3 section,
  above) states head/tail pads of "180ms/520ms." The actual shipped default in
  `DEFAULT_CONFIG['video']['clip_boundary_alignment']` is **`head_pad_ms: 500`, `tail_pad_ms: 900`**
  — neither number matches what was previously documented. The other boundary-alignment numbers
  *do* match: `min_gap_ms: 220` (the natural-pause silence threshold), `max_start_shift_ms: 8000`,
  `max_end_shift_ms: 12000`, plus two values not previously listed at all —
  `max_end_backtrack_ms: 2000` and `min_segment_ms: 6000` (a segment shorter than 6s after boundary
  snapping is presumably rejected/re-expanded, though confirming the exact enforcement point would
  require re-reading `clip_boundary.py` itself, which was read by the original pass, not this one).
  Given `clip_boundary.py` wasn't re-read this pass, this may reflect a version drift between when
  the original pass read the code path's own hardcoded fallback (if any) versus this pass reading
  `config.py`'s current shipped default — but the two disagree, and `config.py`'s numbers are what
  actually ships absent a `config.yaml` override, so they're the more load-bearing ones to trust
  going forward.
- **Possible correction — synonym table size.** The original write-up describes tag_normalizer.py's
  synonym table as "~150-entry." `DEFAULT_CONFIG['tagging']['synonyms']` — the actual default
  synonym dict shipped in `config.py` — has **14 entries**, not ~150. This doesn't necessarily mean
  the original count was wrong (`tag_normalizer.py` itself, read by the original pass and not
  re-read here, could maintain a much larger hardcoded table independent of this config default,
  since the write-up's phrasing implies the ~150 count came from reading that file directly) — but
  it's worth flagging as a discrepancy between the two sources rather than silently repeating the
  bigger number. `allowed_tags` (the hard-constrained top-level tag vocabulary) is confirmed exactly
  as previously described: **15 entries** (`开场/产品介绍/产品演示/使用教学/效果展示/对比验证/技术讲解/场景应用/用户反馈/答疑互动/促销信息/购买引导/售后保障/总结预告/其他`).
- **Previously-unconfirmed exact defaults, now pinned down:** LLM provider defaults to `dashscope`
  (Alibaba), model `qwen-plus`, `temperature: 0.3`, `max_tokens: 4096`, `timeout: 120`s,
  `max_retries: 3`. Chunking defaults to the `duration_window` strategy (40–90s band, 60s target,
  `single_segment_per_chunk: true`) with the older `sliding_window` strategy available as an
  explicit config toggle (`chunk_size_minutes: 10`, `overlap_minutes: 2`,
  `overlap_threshold: 0.5` — the exact dedup threshold for that mode, not previously given — and an
  `on_chunk_failure: skip|abort` setting controlling whether one bad chunk aborts the whole run or
  is silently dropped). Video encode defaults: `codec: auto`, `crf: 23`, `preset: fast`,
  `audio_codec: aac` — matches what direct reading of `video.py` already showed. Value-scoring
  weights confirmed exactly as previously documented: `transaction_count: 0.4, comment_count: 0.3,
  avg_watch_duration: 0.2, viewer_count: 0.1`.
- `load_config()`'s merge behavior is a real, reusable pattern: it starts from `DEFAULT_CONFIG`,
  loads `config.yaml` if present, and recursively deep-merges the user file over the defaults
  key-by-key (`_deep_merge`, only descending into nested dicts, otherwise the user's value wins
  outright) — so a `config.yaml` only needs to specify the handful of keys it wants to override, not
  reproduce the entire schema. Missing/unreadable config file falls back to defaults with a printed
  warning rather than crashing.
- `videoclip/models/schemas.py` is straightforward dataclasses (`SRTEntry`, `ValueScore`,
  `VideoSegment`, `ProcessingResult`) with no surprising logic — the one thing worth noting is
  `VideoSegment` carries both `tags` (post-normalization) and an optional `raw_tags` (pre-normalization,
  kept only if `keep_raw_tags: true` in config) side by side, i.e. the three-layer tag-normalization
  pipeline documented earlier deliberately preserves what the LLM originally said alongside what it
  got mapped to, for auditability.

This closes out `metaleey/AI-auto-segment-edit-video-pipeline`'s real application-logic files. What
remains unread (frontend Vue components, README variants, architecture markdown docs, FastAPI
CRUD boilerplate) is genuinely out of scope per this project's own audit standard.

**Note on `lay295/TwitchDownloader` (Repo 1, above):** given its size (311 files — by far the
largest of all six repos audited across this research) and that it was flagged as the single
highest-priority gap, it is being audited in a separate, dedicated pass rather than folded into
this section; see the file for that pass's own findings once complete, appended near the Repo 1
section above.

---

## Cross-repo synthesis: do these three suggest a third real strategy?

`verified_tools_catalog.md` currently frames the decision as two strategies:
**(1) DIY/self-hosted** (faster-whisper → LLM moment-scoring → ffmpeg/NCA →
cross-poster, near-zero recurring cost) vs. **(2) SaaS-chained** (Opus
Clip/Submagic/NexusClips + Blotato/Metricool/Repurpose.io, $30-100+/mo).
These three repos don't overturn that framing — all three are unambiguously
on the DIY/self-hosted side of the line, no new commercial-SaaS-chaining
pattern emerged — but together they sharpen strategy (1) with a concrete,
previously-missing **third architectural axis that cuts across both named
strategies: how much of the detection work an LLM should actually be asked
to do, versus how much cheaper statistical/behavioral signals can do first.**

Three data points converge on the same refinement:

1. **`stream-clipper` proves a zero-LLM detector is a real, shippable
   product.** Its entire detection pipeline — audio RMS+VAD spikes, chat
   rate/keyword/emote spikes, combo-bonus overlap scoring — runs locally
   with no AI API calls at all, and it's sold commercially. This means our
   own pipeline's *candidate generation* stage doesn't need to be LLM-based
   at all — the same signals (audio energy, chat message rate, from our own
   TwitchDownloader-format chat JSON) can pre-filter a multi-hour VOD down
   to a shortlist of candidate windows entirely offline, for free.
2. **`metaleey`'s value-scoring module proves the same "cheap signal narrows
   the field, LLM only does what only LLM can do" idea, but from the
   opposite direction**: instead of a signal *generating* candidates, it
   *re-ranks* LLM-generated semantic segments using an independent
   behavioral time series joined by timestamp. Applied to Twitch: chat
   velocity/viewer-count could re-rank (not just help generate) the output
   of an LLM semantic pass.
3. **`deep_dive_openshorts.md`'s two-stage score→detail LLM pattern (cheap
   0-100 score call on every window, expensive detail call only on
   finalists) is the same cost-optimization instinct already independently
   discovered by the strongest full-pipeline reference in our research.**

The concrete, actionable synthesis for our own pipeline design: **a
three-stage funnel, not two.** (a) Statistical pre-filter — combine
`stream-clipper`'s audio-RMS+VAD spike detector and chat-rate/keyword/emote
spike detector (both directly portable to Python, zero API cost, run on the
full VOD) into a candidate-window list, with `stream-clipper`'s combo-bonus
logic giving early confidence weighting to windows where both signals agree;
(b) LLM semantic pass, openshorts-style two-stage score→detail, but **only
run against the statistically-pre-filtered candidates**, not the full
transcript — cutting LLM spend roughly in proportion to how aggressively
stage (a) narrows the field; (c) optional `metaleey`-style value-rescoring
if/when we have any real behavioral time series beyond chat (concurrent
viewer count over time, sub/bit events) to cross-reference against the
LLM-selected clips before final ranking. This funnel is strictly cheaper than
"LLM scores every window" (the pattern most of our other sources default to)
while keeping the LLM's judgment where a keyword/volume heuristic can't
substitute for it (does this moment actually cohere as a story, is the
title/hook any good, is it duplicate-content of another clip already
selected). Worth writing up as a concrete architecture proposal, not just a
research note.

### Addendum from the audit pass [2026-07-29]

Two findings from the audit pass above change/sharpen this synthesis and
deserve to be called out here explicitly rather than left buried in the
Repo 1 addendum section:

1. **The "does Twitch expose native highlight markers" question is now
   answered, and the answer is no — but there's a concrete free substitute.**
   `HighlightIcons.cs` was read in full specifically to check this (its name
   suggested a native highlight API). It does not expose one: Twitch's public
   chapter/moments feed only tracks `GAME_CHANGE` (category-switch) events,
   confirmed by re-reading `FfmpegMetadata.cs`'s chapter filter alongside it.
   What *does* exist, and is directly usable in stage (a) of the three-stage
   funnel above, is a **free, zero-LLM, zero-extra-API-call event
   classifier**: raids, gifted-sub bombs, charity donations, hype-train
   combos, and watch-streak milestones are all detectable today by
   string-matching Twitch's literal IRC system-message templates against
   `Comment.message.body` (see `HighlightIcons.GetHighlightType` above) —
   these are ordinary rows already present in the same chat JSON our
   pre-filter stage is already scanning for message-rate/keyword/emote
   spikes. Recommendation: fold this classifier into stage (a) as a fourth,
   free signal source alongside audio-RMS+VAD and chat-rate/keyword/emote —
   a raid or a sub-bomb landing inside or near a statistically-detected spike
   window is exactly the kind of "two independent signals agree" case
   `stream-clipper`'s combo-bonus logic was designed to reward.

2. **Clip-native portrait-crop data is a real, free alternative to building
   our own smart-crop/face-tracking for 9:16 output — but only for content
   that started life as a Twitch clip, not a raw VOD segment.**
   `ClipDownloader.cs`'s actual GQL response
   (`GqlShareClipRenderStatusResponse`, operation `ShareClipRenderStatus`)
   carries `portraitMetadata` with explicit top-left/bottom-right crop-box
   percentages per clip asset, meaning Twitch has already computed a
   subject-aware vertical crop for some clips. This does **not** change the
   core VOD-download-then-cut recommendation for our primary pipeline (we're
   cutting arbitrary moments out of a full VOD, which never has this
   metadata — only clips created through Twitch's own clip-creation flow
   do), but it is worth keeping in mind as a secondary, opportunistic
   optimization: if our pipeline ever ingests existing Twitch clips (e.g. as
   a supplementary source alongside VOD-derived clips, or if a detected
   highlight window happens to overlap with a clip a viewer already created
   during the stream), pulling that clip's native portrait crop instead of
   running our own crop/reframe logic on it is strictly cheaper and
   Twitch-endorsed. Not a reason to change strategy, but a free win to grab
   opportunistically if we ever add clip ingestion as an input source.
