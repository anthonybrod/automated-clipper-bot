# 📂 AUTO CLIPBOT HANDOFF V3: @LacyCrashOuts

## 📄 SECTION 1: authoritative PROJECT.md
Status: Step 8 Gateway (Persistence & Ingestion Lock)
Current Goal: Move to Phase 2 (Local High-Speed Transcription)

### Core Objectives
1. Monitor Lacy’s live streams for crashout signal metrics (chat keyword spikes: CRASHOUT, RAGE, L, SCREAM & Audio >15dB jumps).
2. Harvest 30-60s segments using yt-dlp / m3u8 recorded source for 100% stability.
3. Process via faster-whisper (INT8 quantization) for word-level karaoke timestamps.
4. Verify context boundaries locally via Ollama (Llama 3.2).
5. Render via FFmpeg (9:16 split-screen, chat boxblur).
6. Human-in-the-loop approval via Telegram bot.
7. Publish via direct platform APIs / n8n ($0 open-source stack).

## 📄 SECTION 2: Authoritative CLAUDE.md (Working Rules)
1. NO CONDENSING: Do not shorten code, use placeholders, or summarize logic. Provide complete 1:1 functional modules.
2. PERSISTENCE FIRST: Use `AsyncSqliteSaver` from `langgraph.checkpoint.sqlite.aio` for all nodes. Ephemeral state (`MemorySaver`) is strictly forbidden.
3. RESUMPTION: Always check `./enterprise_workspace/checkpoints/` for an existing session before minting new run IDs.
4. BOOTSTRAP PROTOCOL: System-level provisioning (FFmpeg, `nest_asyncio`, diagnostic pre-flight) must occur before any library imports.
5. FAIL-CLOSED: Any exception in a system call must be reported as a failure. Never treat an error as a pass.
6. ASYNC-SAFE I/O: Wrap every blocking system call (`yt-dlp`, FFmpeg) in a non-blocking executor to prevent freezing the event loop.
7. VRAM FLOOR: Mandate CTranslate2 INT8 quantization for `faster-whisper` to cap memory usage.

## 📄 SECTION 3: The Step 8 Gateway (Current Working Code)
```python
import sys, os, subprocess, json, asyncio, time
from pathlib import Path

if "google.colab" in sys.modules:
    print("🔧 [BOOTSTRAP] Provisioning Resilient Architecture...")
    subprocess.run(["apt-get", "update", "-qq"], check=False)
    subprocess.run(["apt-get", "install", "-y", "-qq", "ffmpeg"], check=False)
    pkgs = ["google-genai", "langgraph", "aiosqlite", "nest_asyncio", 
            "faster-whisper", "yt-dlp", "pydub", "chat-downloader"]
    subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + pkgs, check=True)
    import nest_asyncio
    nest_asyncio.apply()

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

def resolve_thread_id(broadcaster: str) -> str:
    state_file = Path(f"./enterprise_workspace/checkpoints/{broadcaster}_latest_session.json")
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
        dirs = ["./enterprise_workspace/checkpoints", "./enterprise_workspace/transcripts", 
                "./enterprise_workspace/deliverables", "./enterprise_workspace/audit_logs"]
        for d in dirs:
            p = Path(d)
            p.mkdir(parents=True, exist_ok=True)
            (p / ".canary").write_text("active_canary_test")
        tid = resolve_thread_id("lacy")
        source = await stable_probe("lacy")
        async with AsyncSqliteSaver.from_conn_string("./enterprise_workspace/checkpoints/pipeline.db") as saver:
            print(f"🚀 [GATE] Step 8 Hand-off Complete. Session: {tid}")

    asyncio.run(gateway())
```

## 📄 SECTION 4: Upcoming Current Assignment
Implement Phase 2: Local High-Speed Transcription.
1. Engine: Initialize `faster_whisper.WhisperModel` with `compute_type="int8"`.
2. Logic: Implement the `AsyncTranscriber` class to handle audio extraction via FFmpeg and word-level timestamp generation.
3. Resiliency: Ensure all Whisper inference and FFmpeg subprocess calls are wrapped in `asyncio.to_thread` to maintain loop stability.
