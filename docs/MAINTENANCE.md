# Maintenance guide

## Where things live

| Page | Repo file | Live |
|---|---|---|
| sg-haze-live | `index.html` | https://jeremyhuang83.github.io/sg-haze-rox/ |

Hosting: GitHub Pages, deployed from the `main` branch (root folder).

## How the readings are fetched

- Latest PM2.5 → latest PSI → (only if the 24-hour window has gaps) hourly PM2.5 for each missing day.
- Requests run one at a time, 300 ms apart. A refused (HTTP 429), failed or 5xx request is retried once after 1.5–2.5 s.
- If the v2 API fails, the page switches to the v1 API (`date` / `date_time` parameters).
- Saved history is merged with new readings; only the latest 24 hours are kept.
- The 5pm 24-hr PSI is looked up for the SP-CCA section.

## Content-Security-Policy rules (must not be broken)

The page has a `<meta http-equiv="Content-Security-Policy">` that:

- allows the main inline `<script>` and the inline `<style>` blocks **only by SHA-256 hash**;
- allows network requests (`connect-src`) only to `api-open.data.gov.sg` and `api.data.gov.sg`;
- allows fonts only from Google Fonts.

Consequences:

- After editing an inline script or style, recompute its hash
  (`sha256-` + base64 of SHA-256 of the exact text between the tags) and replace it in the CSP —
  or run `python3 tools/check_csp.py --fix`.
- The `<script type="application/json">` data block is not executed and needs no hash.
- A new API host must be added to `connect-src`.
- Inline `style="..."` attributes are not allowed; use classes.
- Text/markup changes outside `<script>` and `<style>` (titles, headings) need no hash change.

## Update routine

1. Edit `index.html`.
2. `python3 tools/check_csp.py` — every block must show `OK`.
3. Check the script parses: extract it and run `node --check`, or open the page and watch the console.
4. Add an entry to `CHANGELOG.md` with the date and time (SGT), commit and push to `main`.
5. After GitHub Pages redeploys, open the live page, tap Refresh, and confirm the reading time and 24 hourly readings.
