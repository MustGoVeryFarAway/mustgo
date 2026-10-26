# MustGo.co.ke · Ruto Receipts

A high-performance, static civic archive for **[mustgo.co.ke](https://mustgo.co.ke)** that collects President William Ruto's public statements on camera and sets each one against an independent fact-check or official state record (Africa Check, PesaCheck, KNBS, Hansard).

*"What was said on camera vs. what the record shows. The internet remembers."*

---

## Key Features

- **The Record Scorecard**: Live truth meter displaying total tracked statements and the distribution of verdicts (False, Misleading, Broken Promise, Unproven) with interactive filtering.
- **Deep-Linking & Hash Routing**: Every claim has its own permanent URL hash (e.g. `mustgo.co.ke/#unga-ksh100-june-2024`). Opening or sharing a link automatically opens the clip and fact-check.
- **Downloadable Receipt Slip Generator**: An on-device HTML5 Canvas generator that creates high-resolution, pixel-crisp receipt image cards ready to share on WhatsApp Status, Instagram, and X.
- **Direct WhatsApp & Social Sharing**: Pre-formatted, one-click sharing buttons for WhatsApp chats/groups and X (Twitter) threads.
- **Media Resilience & Fallbacks**: Clips without videos display an editorial "Official Press / Speech Record" plaque with crowdsourcing prompts, and X embeds gracefully degrade if blocked by ad-blockers.
- **Sequential Navigation**: Browse through receipts with `←` and `→` keyboard shortcuts or on-screen controls.
- **Crowdsourced Submissions**: Built-in modal allowing contributors to submit new statements with links to fact-checks, formatted as GitHub Issues.
- **Mobile-First UX**: Responsive bottom-sheet modal drawer on smartphones.

---

## Run Locally

```bash
# Validate data and write data/claims.js
python3 scripts/build.py --no-fetch

# Start a local web server
python3 -m http.server 8000
```

Then open `http://localhost:8000`. Opening `index.html` directly from disk also works.

---

## Adding a Clip

Add an object to `data/claims.json`:

```json
{
  "id": "short-unique-slug",
  "title": "Neutral one-line headline",
  "quote": "What was said, as close to verbatim as the source allows",
  "date": "2024-06-30",
  "context": "Where it was said (e.g. State House roundtable, national address)",
  "verdict": "False | Misleading | Broken promise | Unproven",
  "reality": "One or two sentences on what the independent record shows",
  "tweet_url": "https://x.com/<account>/status/<id>",
  "factcheck_url": "https://... (required)",
  "tags": ["economy", "cost-of-living"],
  "clip_note": "Optional note on the clip context"
}
```

Then regenerate `data/claims.js`:

```bash
python3 scripts/build.py
```

### Standards
- `factcheck_url` is required. The verdict belongs to accredited fact-checkers (Africa Check, PesaCheck) or official state statistics (KNBS, Auditor General), not editorial opinion.
- `tweet_url` should link to a verified video post (e.g., from Citizen TV, NTV, KTN, Nation, Standard). Use `null` if the official transcript is verified but video has not yet been located.

---

## Deployment

The project consists entirely of static HTML, CSS, JavaScript, and JSON. It deploys with zero build steps on:
- **Cloudflare Pages** (Recommended for DDoS mitigation and global edge caching)
- **GitHub Pages**
- **Netlify / Vercel**
