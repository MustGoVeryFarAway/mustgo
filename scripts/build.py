#!/usr/bin/env python3
"""Validate data/claims.json, fetch tweet video thumbnails, write data/claims.js.

Usage: python3 scripts/build.py [--no-fetch]

Thumbnails come from the public fxtwitter API (api.fxtwitter.com), so no X API
key is needed. Fetched thumbnails are cached back into claims.json.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "claims.json"
OUT = ROOT / "data" / "claims.js"

VERDICTS = {"False", "Misleading", "Broken promise", "Unproven"}
REQUIRED = ("id", "title", "quote", "verdict", "reality", "factcheck_url")
TWEET_RE = re.compile(r"^https://(?:x|twitter)\.com/\w+/status/(\d+)")


def validate(claims):
    errors, seen = [], set()
    for i, c in enumerate(claims):
        where = c.get("id") or f"#{i}"
        for k in REQUIRED:
            if not c.get(k):
                errors.append(f"{where}: missing {k}")
        if c.get("verdict") not in VERDICTS:
            errors.append(f"{where}: verdict must be one of {sorted(VERDICTS)}")
        if c.get("tweet_url") and not TWEET_RE.match(c["tweet_url"]):
            errors.append(f"{where}: tweet_url is not an x.com/twitter.com status URL")
        if c.get("id") in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(c.get("id"))
    return errors


def fetch_thumb(tweet_url):
    m = TWEET_RE.match(tweet_url)
    req = urllib.request.Request(
        f"https://api.fxtwitter.com/status/{m.group(1)}",
        headers={"User-Agent": "ruto-receipts/1.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        tweet = json.load(r).get("tweet") or {}
    media = tweet.get("media") or {}
    for v in media.get("videos") or []:
        if v.get("thumbnail_url"):
            return v["thumbnail_url"]
    for p in media.get("photos") or []:
        if p.get("url"):
            return p["url"]
    return None


def main():
    claims = json.loads(SRC.read_text())
    errors = validate(claims)
    if errors:
        print("Validation failed:\n  " + "\n  ".join(errors), file=sys.stderr)
        sys.exit(1)

    if "--no-fetch" not in sys.argv:
        for c in claims:
            if c.get("tweet_url") and not c.get("thumbnail"):
                try:
                    c["thumbnail"] = fetch_thumb(c["tweet_url"])
                    print(f"{c['id']}: {'thumbnail ok' if c['thumbnail'] else 'no media'}")
                except Exception as e:
                    print(f"{c['id']}: fetch failed ({e})", file=sys.stderr)
        SRC.write_text(json.dumps(claims, indent=2, ensure_ascii=False) + "\n")

    OUT.write_text("window.CLAIMS = " + json.dumps(claims, indent=2, ensure_ascii=False) + ";\n")
    with_video = sum(1 for c in claims if c.get("tweet_url"))
    print(f"Wrote {len(claims)} claims ({with_video} with video) to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
