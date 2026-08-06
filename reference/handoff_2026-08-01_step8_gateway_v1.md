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

# 📂 AUTO CLIPBOT HANDOFF V1: @LacyCrashOuts

## 📄 SECTION 1: authoritative PROJECT.md
Status: Step 8 Gateway (Persistence & Ingestion Lock)
Current Goal: Move to Phase 2 (Local High-Speed Transcription)

### Core Objectives
1. Monitor Lacy’s live streams for statistical engagement outliers (Z-Score >= 2.5).
2. Harvest 30-60s segments using the "Recorded Source" m3u8 feature for 100% stability.
3. Post-process with dynamic 9:16 cropping and karaoke captions.
4. Auto-publish via Playwright stealth browser contexts.

## 📄 SECTION 2: Authoritative CLAUDE.md (Working Rules)
1. NO CONDENSING: Do not shorten code, use placeholders, or summarize logic.
2. PERSISTENCE FIRST: Use AsyncSqliteSaver for all nodes; ephemeral state is a failure.
3. RESUMPTION: Always check ./checkpoints/ for an existing session before minting new run IDs.
4. BOOTSTRAP PROTOCOL: System-level provisioning must occur before any library imports.

## 📄 SECTION 3: The Step 8 Gateway (Current Working Code)
import sys, os, subprocess, json, asyncio, time
from pathlib import Path

if "google.colab" in sys.modules:
    print("🔧 [BOOTSTRAP] Provisioning Resilient Architecture...")
    subprocess.run(["apt-get", "update", "-qq"], check=False)
    subprocess.run(["apt-get", "install", "-y", "-qq", "ffmpeg"], check=False)
    pkgs = ["google-genai", "langgraph", "aiosqlite", "nest_asyncio", 
            "faster-whisper", "playwright", "playwright-stealth", "tenacity"]
    subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + pkgs, check=True)
    import nest_asyncio
    nest_asyncio.apply()

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

def resolve_thread_id(broadcaster: str) -> str:
    state_file = Path(f"./checkpoints/{broadcaster}_latest_session.json")
    if state_file.exists():
        try:
            stored_id = json.loads(state_file.read_text())["thread_id"]
            return stored_id
        except Exception: pass
    new_id = f"{broadcaster}_{int(time.time())}"
    state_file.write_text(json.dumps({"thread_id": new_id}))
    return new_id

async def stable_probe(channel_name: str) -> str:
    url = f"https://twitch.tv/{channel_name}"
    loop = asyncio.get_event_loop()
    try:
        cmd = ["yt-dlp", "--get-url", "--format", "best", "--no-check-certificates", url]
        res = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: subprocess.run(cmd, capture_output=True, text=True, check=True)),
            timeout=45.0
        )
        source = res.stdout.strip()
        return source if "m3u8" in source else url
    except Exception: return url

if __name__ == "__main__":
    async def gateway():
        for d in ["./checkpoints", "./transcripts", "./clips_out", "./logs"]:
            p = Path(d)
            p.mkdir(parents=True, exist_ok=True)
            (p / ".canary").write_text("test")
        tid = resolve_thread_id("lacy")
        source = await stable_probe("lacy")
        async with AsyncSqliteSaver.from_conn_string("./checkpoints/pipeline.db") as saver:
            print(f"🚀 [GATE] Step 8 Hand-off Complete. Session: {tid}")

    asyncio.run(gateway())

## 📄 SECTION 4: Upcoming Current Assignment
Implement Phase 2: Local High-Speed Transcription.
1. Engine: Initialize faster_whisper.WhisperModel with compute_type="int8".
2. Logic: Implement snap_clip_to_words() utility to align cut timestamps.
3. Resiliency: Port safe_json_parse pattern from salvage inventory.
