"""Batch 2: fetch transcripts for the 6 videos referenced in the planning
docs that were never transcribed (workstream C).

Same proven approach as fetch_transcripts.py, which fetched 17/17 - reused
rather than re-derived (Rule 1). Two deliberate differences:
  - writes its own _summary_batch2.txt so batch 1's summary is not touched
  - never overwrites an existing .txt; a transcript already on disk is
    reported as SKIP-EXISTS rather than silently replaced

The 3 Lacy videos matter most: they are the only source anywhere for what a
clip-worthy Lacy moment actually looks like, which feeds detection
thresholds and hook patterns.
"""
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, NoTranscriptFound, VideoUnavailable)

VIDEOS = [
    ("mFOoNPFylLI", "Higgsfield / Claude connectors"),
    ("PafYu69s5NA", "Claude + Whop Clipping Workflow"),
    ("QqwNue_KL-4", "Gemini Gems Tutorial"),
    ("cVkFMpDLQrM", "Lacy's Best Streamer University Moments"),
    ("mVqnCvE337E", "How Lacy Got Used On Stream"),
    ("lYafPAHVOno", "Lacy's Content Strategy Breakdown"),
]

out_dir = Path(__file__).parent / "transcripts"
out_dir.mkdir(exist_ok=True)

api = YouTubeTranscriptApi()
results = []

for video_id, title in VIDEOS:
    out_path = out_dir / f"{video_id}.txt"
    if out_path.exists():
        results.append((video_id, title, "SKIP-EXISTS", 0))
        print(f"SKIP  {video_id}  already on disk  {title}")
        continue
    try:
        fetched = api.fetch(video_id)
        lines = []
        for snip in fetched.snippets:
            mins, secs = divmod(int(snip.start), 60)
            lines.append(f"[{mins:02d}:{secs:02d}] {snip.text}")
        text = "\n".join(lines)
        out_path.write_text(
            f"# {title}\n# https://www.youtube.com/watch?v={video_id}\n\n{text}",
            encoding="utf-8")
        results.append((video_id, title, "SUCCESS", len(fetched.snippets)))
        print(f"OK  {video_id}  {len(fetched.snippets)} snippets  {title}")
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        results.append((video_id, title, f"NO TRANSCRIPT: {type(e).__name__}", 0))
        print(f"NO-TRANSCRIPT  {video_id}  {type(e).__name__}  {title}")
    except Exception as e:
        results.append((video_id, title, f"ERROR: {type(e).__name__}: {e}", 0))
        print(f"ERROR  {video_id}  {type(e).__name__}: {e}  {title}")

summary_path = out_dir / "_summary_batch2.txt"
summary_path.write_text(
    "\n".join(f"{vid}\t{status}\t{count} snippets\t{title}"
              for vid, title, status, count in results),
    encoding="utf-8")

ok = sum(1 for _, _, s, _ in results if s == "SUCCESS")
print(f"\n{ok}/{len(VIDEOS)} transcripts fetched.")
for vid, title, status, _ in results:
    if status != "SUCCESS":
        print(f"  FAILED -> {vid}  {status}  ({title})")
