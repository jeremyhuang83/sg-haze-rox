# sg-haze-live

Intuitive haze to provide quick decisions for outdoor workouts.

A single-file web page that answers one question during Singapore's haze season: **can I train outdoors right now?**
It pulls NEA's live PM2.5 and PSI readings from data.gov.sg and turns them into a green / amber / red call for an easy Z2 run and for a hard session, with an SP-CCA training section.

**Page:** [`index.html`](index.html) (v1.1) · **Live:** https://jeremyhuang83.github.io/sg-haze-rox/

## How it works

- **No server code.** The page is one `index.html` with inline CSS and JavaScript. The browser calls NEA's open data directly:
  - Primary: `https://api-open.data.gov.sg/v2/real-time/api/` (`pm25`, `psi`)
  - Fallback: `https://api.data.gov.sg/v1/environment/` (`pm25`, `psi`)
- **Refresh:** on open, on the Refresh button (or pull-down), every 15 minutes while visible, and when you come back to the tab after 5 minutes. NEA publishes new figures once an hour.
- **Rate-limit friendly:** requests go one at a time with a retry. A normal refresh is 2 requests; the 24-hour history is only fetched for hours that are missing.
- **Offline-tolerant:** the last good readings are kept in the browser (`localStorage`) and an embedded snapshot is shown until live data arrives.

## The training call

| 1-hr PM2.5 (µg/m³) | NEA band | Easy Z2 run | Hard session |
|---|---|---|---|
| 0–55 | Normal | Go | Go (Shorter if 24-hr PSI > 100) |
| 56–150 | Elevated | Short only | Indoors |
| 151+ | High / Very high | Indoors | Indoors |

Always stop if you get a scratchy throat, a cough or tight breathing, whatever the number says.

## Repository layout

```
index.html                the page
tools/check_csp.py        verifies the Content-Security-Policy hashes
docs/MAINTENANCE.md       how to edit and publish safely
CHANGELOG.md              what changed and when
```

## Editing — read this first

The page uses a strict Content-Security-Policy that only runs inline code whose **SHA-256 hash** is listed in the page. Any edit to an inline `<script>` or `<style>` changes its hash, and the page will load blank or unstyled until the CSP is updated.

```bash
python3 tools/check_csp.py         # check the page
python3 tools/check_csp.py --fix   # rewrite the hashes after an edit
```

See [docs/MAINTENANCE.md](docs/MAINTENANCE.md) for the full routine.

## Publish

Published with GitHub Pages from the `main` branch (root folder); `index.html` is the site's home page. Every push to `main` goes live within a minute or two.

## Data

Air-quality readings: National Environment Agency (NEA) via [data.gov.sg](https://data.gov.sg), used under the Singapore Open Data Licence. Official advisories: [haze.gov.sg](https://www.haze.gov.sg).
