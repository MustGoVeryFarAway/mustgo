#!/usr/bin/env python3
"""Check all external links in data/claims.json (factcheck_url and tweet_url).
Reports response status codes, redirects, and flags broken/dead links.
"""
import concurrent.futures
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAIMS_FILE = ROOT / "data" / "claims.json"

TWEET_RE = re.compile(r"^https://(?:x|twitter)\.com/\w+/status/(\d+)")

# SSL context that allows certificates without strict local trust store issues
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    pass


def check_url(url, timeout=12):
    """Check standard HTTP/HTTPS URL, following redirects."""
    try:
        req = urllib.request.Request(url, headers=HEADERS, method="GET")
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return {
                "url": url,
                "status": resp.status,
                "ok": 200 <= resp.status < 400,
                "final_url": resp.geturl(),
                "error": None
            }
    except urllib.error.HTTPError as e:
        # Some servers (e.g. Cloudflare, 403 on scraping) reject python bot headers
        return {
            "url": url,
            "status": e.code,
            "ok": e.code in (200, 301, 302, 307, 308, 403), # 403 often means Cloudflare / anti-bot on existing page
            "final_url": url,
            "error": f"HTTP {e.code}: {e.reason}"
        }
    except urllib.error.URLError as e:
        return {
            "url": url,
            "status": None,
            "ok": False,
            "final_url": url,
            "error": f"URLError: {e.reason}"
        }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "ok": False,
            "final_url": url,
            "error": str(e)
        }


def check_tweet(url, timeout=12):
    """Check tweet status via public syndication / fxtwitter API."""
    m = TWEET_RE.match(url)
    if not m:
        return {
            "url": url,
            "status": 400,
            "ok": False,
            "final_url": url,
            "error": "Invalid tweet URL pattern"
        }
    tweet_id = m.group(1)
    
    # Check 1: fxtwitter API
    fx_url = f"https://api.fxtwitter.com/status/{tweet_id}"
    try:
        req = urllib.request.Request(fx_url, headers={"User-Agent": "ruto-receipts/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            data = json.load(resp)
            code = data.get("code")
            if code == 200:
                tweet = data.get("tweet") or {}
                return {
                    "url": url,
                    "status": 200,
                    "ok": True,
                    "final_url": url,
                    "tweet_author": tweet.get("author", {}).get("screen_name"),
                    "has_media": bool(tweet.get("media", {}).get("videos") or tweet.get("media", {}).get("photos")),
                    "error": None
                }
            elif code == 404:
                return {
                    "url": url,
                    "status": 404,
                    "ok": False,
                    "final_url": url,
                    "error": "Tweet not found or deleted (fxtwitter 404)"
                }
    except Exception as e:
        # Fallback to Twitter oEmbed
        pass

    # Check 2: Twitter publish oEmbed API
    oembed_url = f"https://publish.twitter.com/oembed?url={urllib.parse.quote(url)}"
    try:
        req = urllib.request.Request(oembed_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return {
                "url": url,
                "status": resp.status,
                "ok": resp.status == 200,
                "final_url": url,
                "error": None
            }
    except urllib.error.HTTPError as e:
        return {
            "url": url,
            "status": e.code,
            "ok": False,
            "final_url": url,
            "error": f"Twitter oEmbed HTTP {e.code}"
        }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "ok": False,
            "final_url": url,
            "error": f"Tweet check failed: {e}"
        }


def main():
    claims = json.loads(CLAIMS_FILE.read_text(encoding="utf-8"))
    print(f"Checking external URLs for {len(claims)} claims...\n")

    factcheck_tasks = []
    tweet_tasks = []

    for c in claims:
        cid = c["id"]
        fc_url = c.get("factcheck_url")
        tw_url = c.get("tweet_url")
        if fc_url:
            factcheck_tasks.append((cid, fc_url))
        if tw_url:
            tweet_tasks.append((cid, tw_url))

    print(f"Total Fact-Check URLs: {len(factcheck_tasks)}")
    print(f"Total Video / Tweet URLs: {len(tweet_tasks)}")
    print("Running parallel network verification (this takes ~10-15s)...\n")

    fc_results = {}
    tw_results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_fc = {executor.submit(check_url, url): (cid, url) for cid, url in factcheck_tasks}
        future_to_tw = {executor.submit(check_tweet, url): (cid, url) for cid, url in tweet_tasks}

        for future in concurrent.futures.as_completed(future_to_fc):
            cid, url = future_to_fc[future]
            try:
                fc_results[cid] = future.result()
            except Exception as exc:
                fc_results[cid] = {"url": url, "status": None, "ok": False, "error": str(exc)}

        for future in concurrent.futures.as_completed(future_to_tw):
            cid, url = future_to_tw[future]
            try:
                tw_results[cid] = future.result()
            except Exception as exc:
                tw_results[cid] = {"url": url, "status": None, "ok": False, "error": str(exc)}

    # Analysis
    fc_ok = [cid for cid, r in fc_results.items() if r["ok"]]
    fc_failed = [cid for cid, r in fc_results.items() if not r["ok"]]

    tw_ok = [cid for cid, r in tw_results.items() if r["ok"]]
    tw_failed = [cid for cid, r in tw_results.items() if not r["ok"]]

    print("=" * 70)
    print("VERIFICATION RESULTS SUMMARY")
    print("=" * 70)
    print(f"Fact-Check URLs : {len(fc_ok)} OK / {len(fc_failed)} ISSUES (Total: {len(factcheck_tasks)})")
    print(f"Video/Tweet URLs: {len(tw_ok)} OK / {len(tw_failed)} ISSUES (Total: {len(tweet_tasks)})")
    print("=" * 70)

    if fc_failed:
        print("\n[!] FACT-CHECK URLS REQUIRING ATTENTION:")
        for cid in fc_failed:
            r = fc_results[cid]
            print(f"  • Claim: {cid}")
            print(f"    URL:   {r['url']}")
            print(f"    Issue: {r['error']} (Status: {r['status']})\n")

    if tw_failed:
        print("\n[!] TWEET/VIDEO URLS REQUIRING ATTENTION:")
        for cid in tw_failed:
            r = tw_results[cid]
            print(f"  • Claim: {cid}")
            print(f"    URL:   {r['url']}")
            print(f"    Issue: {r['error']} (Status: {r['status']})\n")

    # Save detailed report to json
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_claims": len(claims),
        "factcheck_summary": {"total": len(factcheck_tasks), "ok": len(fc_ok), "failed": len(fc_failed)},
        "tweet_summary": {"total": len(tweet_tasks), "ok": len(tw_ok), "failed": len(tw_failed)},
        "fc_results": fc_results,
        "tw_results": tw_results,
        "fc_failed": fc_failed,
        "tw_failed": tw_failed
    }
    Path(ROOT / "data" / "url_verification_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote detailed verification report to data/url_verification_report.json")


if __name__ == "__main__":
    main()
