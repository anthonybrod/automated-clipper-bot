"""Pre-flight checks for automated-clipper-bot.

Run this BEFORE writing or running any real pipeline code. Modeled directly
on validate_api_keys() in the youtube-auto-videos repo (pipeline.py:3888) -
same reason: prove every hard dependency actually works, with a real API
call, before a real run can waste time or money on something that was never
going to work.

Usage: python validate_environment.py
"""
import os
import subprocess
import sys

import requests

IS_COLAB = "google.colab" in sys.modules


def get_secret(key: str) -> str:
    """Ported from pipeline.py:74 - Colab userdata first, then env var."""
    if IS_COLAB:
        try:
            from google.colab import userdata
            val = userdata.get(key)
            if val:
                return val
        except Exception:
            pass
    return os.environ.get(key, "")


def check_ffmpeg() -> tuple[bool, str]:
    if IS_COLAB:
        subprocess.run(["apt-get", "install", "-y", "-qq", "ffmpeg"], check=False)
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            first_line = result.stdout.splitlines()[0] if result.stdout else "ffmpeg found"
            return True, first_line
        return False, "ffmpeg found on PATH but returned a non-zero exit code"
    except FileNotFoundError:
        return False, "ffmpeg not found on PATH (install it, or run this inside Colab which auto-installs it)"


def _model_quality_rank(name: str) -> tuple[int, int]:
    # Ported verbatim from pipeline.py:610 (youtube-auto-videos) - same
    # ranking, not reinvented: prefer "pro" over "flash" over "lite", and
    # non-preview over preview (less likely to be deprecated mid-project -
    # confirmed twice now: it already happened in the sibling project, and
    # again here on 2026-07-30 when gemini-2.5-flash itself got restricted).
    n = name.lower()
    tier = 0 if "pro" in n else (1 if "lite" not in n else 2)
    preview_penalty = 1 if "preview" in n else 0
    return (tier, preview_penalty)


def _test_text_model_candidate(client, model_name: str) -> tuple[bool, str]:
    # Same shape as pipeline.py:620's _test_image_model_candidate /
    # pipeline.py:651's _test_tts_model_candidate, adapted for plain text -
    # those two exist because "listed in models.list()" doesn't prove a model
    # is actually usable (confirmed there: three Imagen tiers 404'd for new
    # users despite being listed). Same discipline here: real call, not just
    # a catalog check.
    try:
        resp = client.models.generate_content(model=model_name, contents="Say OK.")
        if resp and getattr(resp, "text", None):
            return True, "OK - real text response returned."
        return False, "Call succeeded but returned no text."
    except Exception as e:
        return False, str(e)


def check_google_api_key() -> tuple[bool, str]:
    """Queries the REAL current model catalog via client.models.list() (the
    proven pattern from pipeline.py:674's discover_best_working_models(),
    ported here rather than re-derived) instead of guessing names, then
    tests real candidates best-first with an actual generate_content call
    until one genuinely succeeds."""
    api_key = get_secret("GOOGLE_API_KEY")
    if not api_key:
        return False, "GOOGLE_API_KEY not set (Colab secret or env var)"
    try:
        from google import genai
    except Exception as e:
        return False, f"google-genai import failed: {e}"

    client = genai.Client(api_key=api_key)
    try:
        all_models = list(client.models.list())
    except Exception as e:
        return False, f"models.list() failed - can't even query the catalog: {e}"

    candidates = sorted(
        {m.name.split("/")[-1] for m in all_models
         if "generateContent" in (m.supported_actions or []) and "gemini" in (m.name or "").lower()
         and "embedding" not in (m.name or "").lower()},
        key=_model_quality_rank,
    )
    if not candidates:
        return False, "models.list() returned no gemini text-generation models for this key at all"

    errors = []
    for model in candidates[:8]:  # cap attempts - real ping, not exhaustive search
        passed, detail = _test_text_model_candidate(client, model)
        if passed:
            return True, f"Real generate_content call succeeded (model: {model}, {len(candidates)} candidates found)"
        errors.append(f"{model}: {detail}")
    return False, f"All {len(errors)} tested candidates failed: " + " | ".join(errors)


def check_twitch_credentials() -> tuple[bool, str]:
    """Real app-access-token exchange via Twitch's documented client_credentials
    flow (https://id.twitch.tv/oauth2/token). This is the standard way to get
    an app access token for public Helix endpoints (Get Clips, Get Videos,
    Get Users) - no user login/OAuth redirect needed, just Client ID + Secret
    from a Twitch Developer Console app the user creates themselves."""
    client_id = get_secret("TWITCH_CLIENT_ID")
    client_secret = get_secret("TWITCH_CLIENT_SECRET")
    if not client_id or not client_secret:
        return False, "TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET not set (Colab secret or env var)"
    try:
        resp = requests.post(
            "https://id.twitch.tv/oauth2/token",
            params={"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"},
            timeout=15,
        )
        if resp.status_code != 200:
            return False, f"Token exchange failed: HTTP {resp.status_code} - {resp.text[:200]}"
        token = resp.json().get("access_token")
        if not token:
            return False, f"Token exchange returned 200 but no access_token: {resp.text[:200]}"
        return True, "Real client_credentials token exchange succeeded"
    except Exception as e:
        return False, f"Token exchange request failed: {e}"


def check_twitch_get_clips(broadcaster_login: str | None = None) -> tuple[bool, str]:
    """Real call to the Get Clips endpoint - the proposed primary highlight
    signal (see reference/gemini_suggestions.md). Soft-checked only: requires
    a broadcaster login to test against, which we don't have until the user
    names a target channel."""
    if not broadcaster_login:
        return True, "SKIPPED - no target broadcaster configured yet (set one to actually test this endpoint)"
    client_id = get_secret("TWITCH_CLIENT_ID")
    client_secret = get_secret("TWITCH_CLIENT_SECRET")
    if not client_id or not client_secret:
        return False, "Cannot test - Twitch credentials missing (see check_twitch_credentials)"
    try:
        token_resp = requests.post(
            "https://id.twitch.tv/oauth2/token",
            params={"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"},
            timeout=15,
        )
        token = token_resp.json().get("access_token")
        headers = {"Client-Id": client_id, "Authorization": f"Bearer {token}"}
        user_resp = requests.get(
            "https://api.twitch.tv/helix/users",
            params={"login": broadcaster_login}, headers=headers, timeout=15,
        )
        users = user_resp.json().get("data", [])
        if not users:
            return False, f"No Twitch user found for login '{broadcaster_login}'"
        broadcaster_id = users[0]["id"]
        clips_resp = requests.get(
            "https://api.twitch.tv/helix/clips",
            params={"broadcaster_id": broadcaster_id, "first": 5}, headers=headers, timeout=15,
        )
        clips = clips_resp.json().get("data", [])
        return True, f"Real Get Clips call succeeded - {len(clips)} clip(s) returned for '{broadcaster_login}'"
    except Exception as e:
        return False, f"Get Clips check failed: {e}"


def main():
    print(f"Running in Colab: {IS_COLAB}\n")
    checks = [
        ("ffmpeg", check_ffmpeg(), True),
        ("GOOGLE_API_KEY (real generate_content call)", check_google_api_key(), True),
        ("TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET (real token exchange)", check_twitch_credentials(), True),
        ("Twitch Get Clips endpoint", check_twitch_get_clips(os.environ.get("TARGET_BROADCASTER")), False),
    ]

    hard_failed = False
    for name, (passed, detail), is_hard in checks:
        status = "PASS" if passed else ("FAIL" if is_hard else "WARN")
        print(f"[{status}] {name}: {detail}")
        if not passed and is_hard:
            hard_failed = True

    print()
    if hard_failed:
        print("BLOCKED: one or more hard-required checks failed. Fix before writing/running pipeline code.")
        sys.exit(1)
    print("All hard-required checks passed.")


if __name__ == "__main__":
    main()
