# Ruto Receipts

A static site that collects President William Ruto's public statements on video (from X/Twitter posts) and sets each one against an independent fact-check or the public record.

## Run it

```bash
python3 scripts/build.py            # validate data, fetch thumbnails, write data/claims.js
python3 -m http.server 8000         # then open http://localhost:8000
```

Opening `index.html` directly from disk also works. Videos play through X's official embed when a card is opened.

## Adding a clip

Add an object to `data/claims.json`, then run the build:

```json
{
  "id": "short-slug",
  "title": "Neutral one-line headline",
  "quote": "What he said, as close to verbatim as the source allows",
  "date": "2024-06-25",
  "context": "Where it was said",
  "verdict": "False | Misleading | Broken promise | Unproven",
  "reality": "One or two sentences on what the evidence shows",
  "tweet_url": "https://x.com/<account>/status/<id>",
  "factcheck_url": "https://… (required)",
  "tags": ["economy"],
  "clip_note": "Optional: say if the video is a full broadcast or news report rather than a clip of the exact line"
}
```

Rules:
- `factcheck_url` is required. The verdict belongs to the linked fact-checker or reporting, not to this site.
- `tweet_url` must be a real post you've opened yourself. Never guess status IDs. Use `null` if no clip has been found yet.
- Prefer clips posted by news outlets (NTV, Citizen, KTN, Nation, Standard), since they're less likely to be deleted.

## Deploy

It's plain static files, so it can go on GitHub Pages, Netlify, or Cloudflare Pages with no build step on the host. Commit `data/claims.js` after running the build.
