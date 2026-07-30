"""One-off script: fetch full real transcripts for all 17 researched videos
via youtube_transcript_api (direct API, not browser scraping - the browser
"Show transcript" click was unreliable in the original research session).
Saves one .txt file per video plus a summary of successes/failures.
"""
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

VIDEOS = [
    ("JhOhaDvOfFk", "1-day-a-week VIDEO CLIPPING SYSTEM that GENERATES LEADS (COMMAND)"),
    ("LiWf_BGg87o", "This AI Machine automatically clips & posts 100+ Shorts from 1 Video (Jay E / RoboNuggets)"),
    ("lge0jth5sl0", "Automate Streamer Clipping with Claude Code + Submagic (Damian Malliaros)"),
    ("pa5LVtcbgD0", "The BEST AI Clipping Tool in 2026: Riverside vs Opus Clip vs Submagic (Julian Eisenkirchner)"),
    ("zNtNYkgCnSA", "How To Auto-Post Twitch Clips to Social Media (Repurpose io)"),
    ("Yj0CAaUhuQM", "How To Make Twitch Clips That Go VIRAL Every Time! (Cal's Creation)"),
    ("1CNVAfY2FKc", "How I made a Fully-Automated Clipping System (Vaika / StreamerBot)"),
    ("oLg-TMlKUKA", "I Let an AI Run My Twitch Clips for 7 Days (Cal's Creation)"),
    ("dOQS2q_ONG0", "The Clip Farm Setup That Gets Your Stream Clips On TikTok In 10 Minutes (Cpaws Music)"),
    ("Yb01G77xscQ", "AI-Powered Viral Clips - 100% Automated, No Editing! (Stephen G. Pope)"),
    ("OHODMrUZlpo", "Best AI Video Editing Tools in 2026 (Youri van Hofwegen)"),
    ("gXXzimVa2A8", "How to Become a Clipper: Learn How to use Free Video Tools (Headliner)"),
    ("IunLg0FY5hY", "How To Make Money with AI Clipping (OpusClip)"),
    ("R8LKMhmyeY4", "3 FREE AI Tools Just KILLED Video Production Agencies (iampauljames)"),
    ("oFneHfcXNGQ", "How to Auto Share Posts to Multiple Social Media Accounts (Nuelink)"),
    ("u8V45xsnkGA", "I Built an AI To Run My Social Media on Autopilot (Creator Magic)"),
    ("av06ZI2bKW4", "How to Automate Cross-Platform Social Media Posting (Pabbly)"),
]

out_dir = Path(__file__).parent / "transcripts"
out_dir.mkdir(exist_ok=True)

api = YouTubeTranscriptApi()
results = []

for video_id, title in VIDEOS:
    try:
        fetched = api.fetch(video_id)
        lines = []
        for snip in fetched.snippets:
            mins, secs = divmod(int(snip.start), 60)
            lines.append(f"[{mins:02d}:{secs:02d}] {snip.text}")
        text = "\n".join(lines)
        out_path = out_dir / f"{video_id}.txt"
        out_path.write_text(f"# {title}\n# https://www.youtube.com/watch?v={video_id}\n\n{text}", encoding="utf-8")
        results.append((video_id, title, "SUCCESS", len(fetched.snippets)))
        print(f"OK  {video_id}  {len(fetched.snippets)} snippets  {title}")
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        results.append((video_id, title, f"NO TRANSCRIPT: {type(e).__name__}", 0))
        print(f"NO-TRANSCRIPT  {video_id}  {type(e).__name__}  {title}")
    except Exception as e:
        results.append((video_id, title, f"ERROR: {e}", 0))
        print(f"ERROR  {video_id}  {e}  {title}")

summary_path = out_dir / "_summary.txt"
summary_lines = [f"{vid}\t{status}\t{count} snippets\t{title}" for vid, title, status, count in results]
summary_path.write_text("\n".join(summary_lines), encoding="utf-8")
success_count = sum(1 for _, _, status, _ in results if status == "SUCCESS")
print(f"\n{success_count}/{len(VIDEOS)} transcripts fetched successfully.")
