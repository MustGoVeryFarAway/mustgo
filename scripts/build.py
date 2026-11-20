#!/usr/bin/env python3
"""Validate all JSON datasets in data/, fetch missing tweet video thumbnails,
and compile JS globals (claims.js, mps.js, impunity.js, memorial.js).

Usage: python3 scripts/build.py [--no-fetch]

Thumbnails come from the public fxtwitter API (api.fxtwitter.com), so no X API
key is needed. Fetched thumbnails are cached back into claims.json.
"""
import html
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

VERDICTS = {"False", "Misleading", "Broken promise", "Unproven"}
CLAIM_REQUIRED = ("id", "title", "quote", "verdict", "reality", "factcheck_url")
MP_REQUIRED = ("id", "name", "constituency", "county", "finance_bill_2024")
IMPUNITY_REQUIRED = ("id", "title", "court", "ruling", "executive_defiance", "status")
MEMORIAL_REQUIRED = ("id", "name", "circumstances", "justice_status")
SCANDAL_REQUIRED = ("id", "category", "title", "impact", "oversight_body", "summary", "status", "source_url")
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


VERDICT_ORDER = ("False", "Misleading", "Broken promise", "Unproven")
DOSSIERS = [
    ("Constitutional Violations & Impunity", "⚖️", {"constitution", "judiciary", "rule-of-law", "justice"}, {
        "cas-50-appointments-unconstitutional", "housing-levy-unconstitutional-ruling",
        "kdf-deployment-protesters-unconstitutional", "judiciary-threats-defiance-court-orders",
        "shif-sha-healthcare-unconstitutional", "cabinet-50pct-women",
        "finance-bill-2024-criminal-infiltrators-claim", "icc-cases-witness-tampering-vindication-claim",
        "icc-paul-gicheru-witness-tampering-denial", "dp-muteshi-pev-land-ruling-2013",
    }),
    ("Reckless Spending & Executive Opulence", "💸", {"reckless-spending", "opulence", "austerity"}, {
        "luxury-jet-us-state-visit-cheaper-claim", "state-house-renovations-ksh1-5bn",
        "office-of-first-lady-budget-broken-promise", "foreign-trips-presidential-travel-austerity",
        "controller-of-budget-budgeted-corruption", "universities-budget-ksh40bn",
    }),
    ("Killings, Abductions & Police Brutality", "🚨", {"police-brutality", "extrajudicial-killings", "human-rights", "killings"}, {
        "rex-masai-live-ammunition-denial", "ssu-disbandment-river-yala-promise",
        "parliament-shootings-restraint-claim", "abductions-give-me-names-kisumu",
        "kware-quarry-transparent-investigation", "maandamano-2023-police-professionalism",
        "protest-death-toll-19", "protest-deaths-six", "no-extrajudicial-killings",
        "no-known-abductions", "dp-baby-pendo-police-denial-2017",
        "icc-witness-meshack-yebei-murder-denial", "icc-cases-witness-tampering-vindication-claim",
    }),
    ("Corruption Scandals & Secret Mega-Deals", "💼", {"corruption", "mega-deals", "adani"}, {
        "adani-jkia-deal-secrecy-denial", "adani-ketraco-power-lines-deal",
        "fake-fertiliser-scandal-denial", "kntc-kemsa-cooking-oil-scandal",
        "dpp-withdrawal-graft-cases-allies", "dp-arror-kimwarer-7bn-2019",
        "minister-maize-subsidized-allocation-2009", "dp-weston-hotel-land-2018",
        "tsc-letters-mps-state-house-distribution", "controller-of-budget-budgeted-corruption",
        "shif-sha-healthcare-unconstitutional", "icc-paul-gicheru-witness-tampering-denial",
        "dp-muteshi-pev-land-ruling-2013",
    }),
    ("Economic Ruin & Broken Promises", "📉", {"cost-of-living", "debt", "currency", "taxes", "finance-bill"}, {
        "unga-ksh100-june-2024", "campaign-fuel-price-reduction-2022",
        "campaign-dollar-fall-to-120", "campaign-no-more-borrowing-2022",
        "campaign-2022-hustler-fund-interest-free", "sona-2023-unga-145-175",
        "dp-stadiums-six-months-2017", "dp-laptops-class-one-2013",
        "dp-galana-kulalu-1m-acres", "dp-jubilee-1-3m-jobs-2017",
        "dp-free-secondary-education-2014", "dp-57-mega-dams-2016",
        "jss-intern-teachers-permanent-promise",
    }),
    ("Abuse of Power, Co-optation & Tribalism", "👥", {"abuse-of-power", "shareholding", "ethnicity", "patronage"}, {
        "shareholding-government-equal-service-denial", "vernacular-mobilization-one-kenya-contradiction",
        "buying-opposition-mps-cooptation-denial", "tsc-letters-mps-state-house-distribution",
        "judiciary-threats-defiance-court-orders", "dpp-withdrawal-graft-cases-allies",
        "cas-50-appointments-unconstitutional", "icc-paul-gicheru-witness-tampering-denial",
        "icc-cases-witness-tampering-vindication-claim",
    }),
]


def fmt_date(raw):
    if not raw:
        return "Date unknown"
    approx = raw.startswith("~")
    clean = raw.lstrip("~")
    out = clean
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            dt = datetime.strptime(clean, fmt)
            out = f"{dt.day} {dt.strftime('%b %Y')}"
            break
        except ValueError:
            continue
    return f"c. {out}" if approx else out


def render_claim_card(c):
    esc = lambda s: html.escape(str(s or ""), quote=True)
    quote = c.get("quote") or ""
    quote_short = quote[:130] + ("…" if len(quote) > 130 else "")
    has_video = bool(c.get("tweet_url"))
    thumb_cls = "thumb" if has_video else "thumb no-video"
    img = f'<img src="{esc(c["thumbnail"])}" alt="" loading="lazy" onerror="this.remove()">' if c.get("thumbnail") else ""
    video_tag = '<span class="video-status-tag">▶ Video Clip</span>' if has_video else '<span class="video-status-tag">📜 Record</span>'

    dossier_badge = ""
    c_tags = set(c.get("tags") or [])
    for name, icon, tags, ids in DOSSIERS:
        if c.get("id") in ids or (c_tags & tags):
            dossier_badge = f'<span class="tag-pill tag-dossier" title="{esc(name)}">{icon} {esc(name.split(" ")[0])}</span>'
            break

    tag_pills = "".join(f'<span class="tag-pill">#{esc(t)}</span>' for t in (c.get("tags") or [])[:2])
    ctx = f" · {esc(c['context'])}" if c.get("context") else ""
    verdict = c.get("verdict") or ""
    return (
        f'<li class="card" tabindex="0">'
        f'<div class="{thumb_cls}">'
        f'<div class="fallback">{esc(quote_short)}</div>'
        f'{img}'
        f'<span class="badge" data-v="{esc(verdict)}">{esc(verdict)}</span>'
        f'<span class="play" aria-hidden="true"></span>'
        f'{video_tag}'
        f'</div>'
        f'<div class="body">'
        f'<h2>{esc(c.get("title"))}</h2>'
        f'<p class="meta">{esc(fmt_date(c.get("date")))}{ctx}</p>'
        f'<div class="tags-list">{dossier_badge}{tag_pills}</div>'
        f'</div>'
        f'</li>'
    )


def prerender_index(claims):
    index_path = ROOT / "index.html"
    if not index_path.exists() or not claims:
        return

    total = len(claims)
    counts = {v: 0 for v in VERDICT_ORDER}
    for c in claims:
        v = c.get("verdict")
        counts[v] = counts.get(v, 0) + 1

    debunked = counts.get("False", 0) + counts.get("Misleading", 0)
    debunked_pct = round((debunked / total) * 100)
    sc_summary = f"{total} Statements · {debunked_pct}% Debunked (False + Misleading)"

    sc_bar = "".join(
        f'<div class="score-seg" data-v="{html.escape(v, quote=True)}" style="width: {(counts[v] / total) * 100:.1f}%" '
        f'title="{html.escape(v, quote=True)}: {counts[v]} ({(counts[v] / total) * 100:.1f}%) - Click to filter"></div>'
        for v in VERDICT_ORDER if counts.get(v)
    )
    sc_pills = "".join(
        f'<button type="button" class="score-pill" data-v="{html.escape(v, quote=True)}" aria-pressed="false">'
        f'<span class="dot"></span><span>{html.escape(v, quote=True)}</span> '
        f'<strong>{counts[v]}</strong> <span class="meta">({round((counts[v] / total) * 100)}%)</span></button>'
        for v in VERDICT_ORDER if counts.get(v)
    )

    sorted_claims = sorted(claims, key=lambda c: (c.get("date") or "").replace("~", ""), reverse=True)
    grid_html = "\n      " + "\n      ".join(render_claim_card(c) for c in sorted_claims) + "\n    "
    count_html = f"{total} of {total} receipts"

    sections = {
        "SC_SUMMARY": sc_summary,
        "SC_BAR": sc_bar,
        "SC_PILLS": sc_pills,
        "COUNT": count_html,
        "GRID": grid_html,
    }

    original = index_path.read_text(encoding="utf-8")
    updated = original
    for key, content in sections.items():
        pattern = re.compile(rf"(<!-- PRERENDER:{key} -->).*?(<!-- /PRERENDER:{key} -->)", re.S)
        updated = pattern.sub(lambda m, val=content: f"{m.group(1)}{val}{m.group(2)}", updated, count=1)

    if updated != original:
        index_path.write_text(updated, encoding="utf-8")


def main():
    claims_src = DATA_DIR / "claims.json"
    mps_src = DATA_DIR / "mps.json"
    impunity_src = DATA_DIR / "impunity.json"
    memorial_src = DATA_DIR / "memorial.json"
    scandals_src = DATA_DIR / "scandals.json"

    claims = json.loads(claims_src.read_text(encoding="utf-8"))
    mps = json.loads(mps_src.read_text(encoding="utf-8"))
    impunity = json.loads(impunity_src.read_text(encoding="utf-8"))
    memorial = json.loads(memorial_src.read_text(encoding="utf-8"))
    scandals = json.loads(scandals_src.read_text(encoding="utf-8")) if scandals_src.exists() else []

    errors = []
    errors.extend(validate_claims(claims))
    errors.extend(validate_list(mps, MP_REQUIRED, "mps"))
    errors.extend(validate_list(impunity, IMPUNITY_REQUIRED, "impunity"))
    errors.extend(validate_list(memorial, MEMORIAL_REQUIRED, "memorial"))
    errors.extend(validate_list(scandals, SCANDAL_REQUIRED, "scandals"))

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
    write_js(DATA_DIR / "scandals.js", "SCANDALS", scandals)
    prerender_index(claims)

    with_video = sum(1 for c in claims if c.get("tweet_url"))
    print(f"Validated & wrote {len(claims)} claims ({with_video} with video), {len(scandals)} scandals, {len(mps)} MPs, {len(impunity)} impunity cases, {len(memorial)} memorial records.")


if __name__ == "__main__":
    main()
