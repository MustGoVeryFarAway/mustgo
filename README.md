# MustGo.co.ke · Ruto Receipts

A high-performance, static civic archive for **[mustgo.co.ke](https://mustgo.co.ke)** that collects President William Ruto's public statements on camera and sets each one against an independent fact-check or official state record (Africa Check, PesaCheck, KNBS, Hansard).

*"What was said on camera vs. what the record shows. The internet remembers."*

---

## Key Features

- **6 Thematic Campaign Dossiers**: Organized by major areas of misrule:
  1. ⚖️ **Constitutional Violations & Impunity** (High Court rulings, 50 illegal CASs, unconstitutional Housing Levy & SHIF, illegal KDF deployment, ICC witness tampering mistrial).
  2. 💸 **Reckless Spending & Opulence** (KSh 200M Boeing 737 luxury jet, KSh 1.5B State House renovations, 62+ foreign trips, spouse budgets).
  3. 🚨 **Killings, Abductions & Brutality** (Rex Masai, Evans Kiratu, Parliament live ammunition, Mukuru Kware quarry bodies, ICC witness deaths including Meshack Yebei).
  4. 💼 **Corruption Scandals & Mega-Deals** (Secret Adani JKIA & Ketraco concessions, fake subsidised fertiliser, KNTC cooking oil, dropped graft cases, ICC Article 70 witness bribery syndicate).
  5. 📉 **Economic Ruin & Broken Promises** (KSh 100 Unga, 16% fuel VAT, dollar crash to 163, borrowing escalation, Hustler Fund 8% interest).
  6. 👥 **Abuse of Power & Tribalism** (Ethnic shareholding doctrine, State House MP patronage, illegal TSC appointment letters, subverting ICC investigations).
- **The Executive Charge Sheet & Factsheet Generator**: An interactive indictment dashboard presenting overall statistics and allowing one-click copying of pre-formatted, bulleted campaign factsheets ready to share across WhatsApp, Telegram, and social media.
- **The Record Scorecard**: Live truth meter displaying total tracked statements (74 verified claims) and the distribution of verdicts (False, Misleading, Broken Promise, Unproven) with interactive filtering.
- **Deep-Linking & Hash Routing**: Every claim and dossier has its own permanent URL hash (e.g. `mustgo.co.ke/#dossier=corruption` or `mustgo.co.ke/#icc-witness-meshack-yebei-murder-denial`). Opening or sharing a link automatically filters or opens the receipt.
- **Downloadable Receipt Slip Generator**: An on-device HTML5 Canvas generator that creates high-resolution, pixel-crisp receipt image cards ready to share on WhatsApp Status, Instagram, and X.
- **Direct WhatsApp & Social Sharing**: Pre-formatted, one-click sharing buttons for WhatsApp chats/groups and X (Twitter) threads.
- **Media Resilience & Fallbacks**: Clips without videos display an editorial "Official Press / Speech Record" plaque with crowdsourcing prompts, and X embeds gracefully degrade if blocked by ad-blockers.
- **Sequential Navigation**: Browse through receipts with `←` and `→` keyboard shortcuts or on-screen controls.
- **Print / PDF Dossier**: Built-in `@media print` stylesheet allowing activists and organizers to print cleanly formatted physical dossiers for barazas, leafleting, and community education.

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
