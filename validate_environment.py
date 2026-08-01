"""Pre-flight checks for automated-clipper-bot.

Run this BEFORE writing or running any real pipeline code. Modeled directly
on validate_api_keys() in the youtube-auto-videos repo (pipeline.py:3888) -
same reason: prove every hard dependency actually works, with a real API
call, before a real run can waste time or money on something that was never
going to work.

Usage: python validate_environment.py
"""
import asyncio
import os
import subprocess
import sys

import requests

IS_COLAB = "google.colab" in sys.modules

# Ported from pipeline.py:381/383/389 - accumulates real token usage across
# this run so pre-flight validation's own cost is visible, not invisible.
_session_tokens = {"total": 0}


def _track_tokens(resp) -> None:
    try:
        _session_tokens["total"] += resp.usage_metadata.total_token_count
    except Exception:
        pass  # some response shapes (or a mocked/test response) may not carry usage_metadata


def get_session_tokens() -> int:
    return _session_tokens["total"]


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
        install = subprocess.run(
            ["apt-get", "install", "-y", "-qq", "ffmpeg"],
            capture_output=True, text=True, check=False,
        )
        if install.returncode != 0:
            print(f"   ⚠️ apt-get install ffmpeg failed (exit {install.returncode}):")
            if install.stderr.strip():
                print(f"      {install.stderr.strip()[:500]}")
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


async def _test_text_model_candidate(client, model_name: str) -> tuple[bool, str]:
    """3-attempt retry with backoff (pipeline.py:3894-3898 - a single call
    used to hard-exit the whole run on any error, including a transient
    network blip on just this validation ping itself). Success = the call
    returned without raising - requiring literal reply text is too fragile
    (pipeline.py:3909-3919: resp.text came back None on one model and ""
    on another in real runs, neither meaning the key/model was broken)."""
    last_error = None
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents="Say OK.",
                config={"temperature": 0, "max_output_tokens": 50},
            )
            _track_tokens(resp)
            return True, "OK - call succeeded (real API response, text not required)."
        except Exception as e:
            last_error = str(e)
            if attempt < 2:
                await asyncio.sleep(2)
    return False, last_error


async def check_google_api_key() -> tuple[bool, str]:
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
        passed, detail = await _test_text_model_candidate(client, model)
        if passed:
            return True, f"Real generate_content call succeeded (model: {model}, {len(candidates)} candidates found)"
        errors.append(f"{model}: {detail}")
    return False, f"All {len(errors)} tested candidates failed: " + " | ".join(errors)


def _fetch_twitch_token(client_id: str, client_secret: str) -> tuple[str | None, str]:
    """Single source of truth for the client_credentials token exchange -
    called once per run; check_twitch_credentials and check_twitch_get_clips
    both reuse the same token instead of each doing their own POST."""
    try:
        resp = requests.post(
            "https://id.twitch.tv/oauth2/token",
            params={"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"},
            timeout=15,
        )
        if resp.status_code != 200:
            return None, f"Token exchange failed: HTTP {resp.status_code} - {resp.text[:200]}"
        token = resp.json().get("access_token")
        if not token:
            return None, f"Token exchange returned 200 but no access_token: {resp.text[:200]}"
        return token, "Real client_credentials token exchange succeeded"
    except Exception as e:
        return None, f"Token exchange request failed: {e}"


def check_twitch_credentials(access_token: str | None = None) -> tuple[bool, str]:
    """Real app-access-token exchange via Twitch's documented client_credentials
    flow (https://id.twitch.tv/oauth2/token) - the standard way to get an app
    access token for public Helix endpoints (Get Clips, Get Videos, Get Users),
    no user login/OAuth redirect needed, just Client ID + Secret from a Twitch
    Developer Console app the user creates themselves.

    If access_token is passed in (already fetched once this run via
    _fetch_twitch_token), validates it directly instead of re-fetching -
    guards against a None/empty token ever being treated as valid."""
    if access_token is not None:
        if not access_token:
            return False, "Twitch access token is empty - cannot proceed"
        return True, "Reusing already-fetched client_credentials token"

    client_id = get_secret("TWITCH_CLIENT_ID")
    client_secret = get_secret("TWITCH_CLIENT_SECRET")
    if not client_id or not client_secret:
        return False, "TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET not set (Colab secret or env var)"
    token, detail = _fetch_twitch_token(client_id, client_secret)
    return (token is not None), detail


def check_twitch_get_clips(
    broadcaster_login: str | None = None,
    access_token: str | None = None,
    client_id: str | None = None,
) -> tuple[bool, str]:
    """Real call to the Get Clips endpoint - the proposed primary highlight
    signal (see reference/gemini_suggestions.md). Soft-checked only: requires
    a broadcaster login to test against, which we don't have until the user
    names a target channel.

    Accepts an optional pre-fetched access_token (and its matching client_id)
    to reuse instead of performing a second, duplicate OAuth token exchange -
    if either is missing/empty, fails immediately rather than constructing a
    'Bearer None' header and making doomed downstream requests."""
    if not broadcaster_login:
        return True, "SKIPPED - no target broadcaster configured yet (set one to actually test this endpoint)"

    if not access_token or not client_id:
        return False, "Cannot test - no valid Twitch access token available (see check_twitch_credentials)"

    try:
        headers = {"Client-Id": client_id, "Authorization": f"Bearer {access_token}"}
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


async def main():
    print(f"Running in Colab: {IS_COLAB}\n")
    hard_failed = False

    # ffmpeg
    passed, detail = check_ffmpeg()
    print(f"[{'PASS' if passed else 'FAIL'}] ffmpeg: {detail}")
    hard_failed = hard_failed or not passed

    # GOOGLE_API_KEY
    passed, detail = await check_google_api_key()
    print(f"[{'PASS' if passed else 'FAIL'}] GOOGLE_API_KEY (real generate_content call): {detail}")
    hard_failed = hard_failed or not passed

    # Twitch credentials - fetch the token ONCE here, reuse it below.
    # check_twitch_credentials is only called when a real token was obtained -
    # calling it with access_token=None on a failed fetch would be
    # indistinguishable from "no token argument was passed at all" (Python
    # can't tell "explicitly None" from "used the default"), which would
    # silently trigger a second, duplicate token-fetch attempt inside it -
    # exactly the bug requirement #7 exists to eliminate, just moved into
    # the failure path. Caught by re-reviewing this file after committing it.
    client_id = get_secret("TWITCH_CLIENT_ID")
    client_secret = get_secret("TWITCH_CLIENT_SECRET")
    token = None
    if not client_id or not client_secret:
        creds_passed, creds_detail = False, "TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET not set (Colab secret or env var)"
    else:
        token, token_detail = _fetch_twitch_token(client_id, client_secret)
        if token:
            creds_passed, creds_detail = check_twitch_credentials(access_token=token)
        else:
            creds_passed, creds_detail = False, token_detail
    print(f"[{'PASS' if creds_passed else 'FAIL'}] TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET (real token exchange): {creds_detail}")
    hard_failed = hard_failed or not creds_passed

    # Twitch Get Clips - short-circuit immediately if credentials already failed.
    if not creds_passed:
        print("[WARN] Twitch Get Clips endpoint: SKIPPED (Credentials check failed)")
    else:
        passed, detail = check_twitch_get_clips(
            get_secret("TARGET_BROADCASTER"), access_token=token, client_id=client_id,
        )
        print(f"[{'PASS' if passed else 'WARN'}] Twitch Get Clips endpoint: {detail}")

    print()
    if hard_failed:
        print("BLOCKED: one or more hard-required checks failed. Fix before writing/running pipeline code.")
        sys.exit(1)
    print("All hard-required checks passed.")


if __name__ == "__main__":
    asyncio.run(main())
