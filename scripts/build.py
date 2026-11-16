#!/usr/bin/env python3
"""Validate all JSON datasets in data/, fetch missing tweet video thumbnails,
and compile JS globals (claims.js, mps.js, impunity.js, memorial.js).

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
DATA_DIR = ROOT / "data"

VERDICTS = {"False", "Misleading", "Broken promise", "Unproven"}
CLAIM_REQUIRED = ("id", "title", "quote", "verdict", "reality", "factcheck_url")
MP_REQUIRED = ("id", "name", "constituency", "county", "finance_bill_2024")
IMPUNITY_REQUIRED = ("id", "title", "court", "ruling", "executive_defiance", "status")
MEMORIAL_REQUIRED = ("id", "name", "circumstances", "justice_status")
TWEET_RE = re.compile(r"^https://(?:x|twitter)\.com/\w+/status/(\d+)")


def validate_list(items, required, label):
    errors, seen = [], set()
    for i, item in enumerate(items):
        where = f"{label}:{item.get('id') or f'#{i}'}"
        for k in required:
            if not item.get(k):
                errors.append(f"{where}: missing {k}")
        item_id = item.get("id")
        if item_id in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(item_id)
    return errors


def validate_claims(claims):
    errors = validate_list(claims, CLAIM_REQUIRED, "claims")
    for i, c in enumerate(claims):
        where = f"claims:{c.get('id') or f'#{i}'}"
        if c.get("verdict") not in VERDICTS:
            errors.append(f"{where}: verdict must be one of {sorted(VERDICTS)}")
        if c.get("tweet_url") and not TWEET_RE.match(c["tweet_url"]):
            errors.append(f"{where}: tweet_url is not an x.com/twitter.com status URL")
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


def write_js(path, global_name, data):
    path.write_text(
        f"window.{global_name} = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )


def main():
    claims_src = DATA_DIR / "claims.json"
    mps_src = DATA_DIR / "mps.json"
    impunity_src = DATA_DIR / "impunity.json"
    memorial_src = DATA_DIR / "memorial.json"

    claims = json.loads(claims_src.read_text(encoding="utf-8"))
    mps = json.loads(mps_src.read_text(encoding="utf-8"))
    impunity = json.loads(impunity_src.read_text(encoding="utf-8"))
    memorial = json.loads(memorial_src.read_text(encoding="utf-8"))

    errors = []
    errors.extend(validate_claims(claims))
    errors.extend(validate_list(mps, MP_REQUIRED, "mps"))
    errors.extend(validate_list(impunity, IMPUNITY_REQUIRED, "impunity"))
    errors.extend(validate_list(memorial, MEMORIAL_REQUIRED, "memorial"))

    if errors:
        print("Validation failed:\n  " + "\n  ".join(errors), file=sys.stderr)
        sys.exit(1)

    if "--no-fetch" not in sys.argv:
        changed = False
        for c in claims:
            if c.get("tweet_url") and not c.get("thumbnail"):
                try:
                    thumb = fetch_thumb(c["tweet_url"])
                    if thumb:
                        c["thumbnail"] = thumb
                        changed = True
                    print(f"{c['id']}: {'thumbnail ok' if thumb else 'no media'}")
                except Exception as e:
                    print(f"{c['id']}: fetch failed ({e})", file=sys.stderr)
        if changed:
            claims_src.write_text(
                json.dumps(claims, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    write_js(DATA_DIR / "claims.js", "CLAIMS", claims)
    write_js(DATA_DIR / "mps.js", "MPS", mps)
    write_js(DATA_DIR / "impunity.js", "IMPUNITY_CASES", impunity)
    write_js(DATA_DIR / "memorial.js", "MEMORIAL_RECORDS", memorial)

    with_video = sum(1 for c in claims if c.get("tweet_url"))
    print(f"Validated & wrote {len(claims)} claims ({with_video} with video), {len(mps)} MPs, {len(impunity)} impunity cases, {len(memorial)} memorial records.")


if __name__ == "__main__":
    main()
