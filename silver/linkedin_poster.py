"""
LinkedIn Auto-Poster — Silver Tier
Posts business updates to LinkedIn to generate sales/visibility.
Uses LinkedIn API via OAuth 2.0.

Setup required:
1. Go to https://www.linkedin.com/developers/apps → Create App
2. Add "Share on LinkedIn" and "Sign In with LinkedIn" products
3. Copy Client ID and Client Secret to .env:
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
4. Run auth flow once: uv run python linkedin_poster.py --auth
5. Token saved to linkedin_token.json (in .gitignore)

Usage:
   uv run python linkedin_poster.py --post "Your post text here"
   uv run python linkedin_poster.py --from-file path/to/post.txt
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime

TOKEN_FILE = Path(__file__).parent / "linkedin_token.json"
VAULT_PATH = Path("/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault")


def load_env():
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def get_auth_url() -> str:
    client_id = os.environ["LINKEDIN_CLIENT_ID"]
    redirect_uri = "http://localhost:8080/callback"
    scope = "openid profile w_member_social"
    return (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code&client_id={client_id}"
        f"&redirect_uri={redirect_uri}&scope={scope}"
    )


def exchange_code_for_token(code: str) -> dict:
    client_id = os.environ["LINKEDIN_CLIENT_ID"]
    client_secret = os.environ["LINKEDIN_CLIENT_SECRET"]
    resp = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8080/callback",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    resp.raise_for_status()
    return resp.json()


def get_person_urn(access_token: str) -> str:
    resp = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp.raise_for_status()
    return f"urn:li:person:{resp.json()['sub']}"


def post_to_linkedin(text: str) -> dict:
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(
            "LinkedIn token not found. Run: uv run python linkedin_poster.py --auth"
        )

    token_data = json.loads(TOKEN_FILE.read_text())
    access_token = token_data["access_token"]
    person_urn = get_person_urn(access_token)

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    resp = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()


def log_post(text: str, result: dict):
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = VAULT_PATH / "Logs" / f"{today}.md"
    time_str = datetime.now().strftime("%H:%M")
    entry = f"\n## {time_str} — linkedin-post\n- Post: {text[:80]}...\n- Result: {result}\n"
    with open(log_file, "a") as f:
        f.write(entry)


def auth_flow():
    """Interactive OAuth flow — run once to get token."""
    load_env()
    print("\n1. Open this URL in your browser and authorize:")
    print(get_auth_url())
    print("\n2. After authorizing, paste the 'code' parameter from the redirect URL:")
    code = input("Code: ").strip()
    token = exchange_code_for_token(code)
    TOKEN_FILE.write_text(json.dumps(token, indent=2))
    print(f"\nToken saved to {TOKEN_FILE}. You can now post to LinkedIn.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Auto-Poster")
    parser.add_argument("--auth", action="store_true", help="Run OAuth setup flow")
    parser.add_argument("--post", type=str, help="Post text directly")
    parser.add_argument("--from-file", type=str, help="Read post text from a file")
    args = parser.parse_args()

    if args.auth:
        auth_flow()
    elif args.post:
        load_env()
        result = post_to_linkedin(args.post)
        log_post(args.post, result)
        print(f"Posted successfully: {result}")
    elif args.from_file:
        load_env()
        text = Path(args.from_file).read_text().strip()
        result = post_to_linkedin(text)
        log_post(text, result)
        print(f"Posted successfully: {result}")
    else:
        parser.print_help()
