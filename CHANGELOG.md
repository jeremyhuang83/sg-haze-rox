# Change log

All times are Singapore time (SGT, UTC+8).

## 2026-10-29 14:10 — Live address updated

- Docs now point to the published page at https://jeremyhuang83.github.io/sg-haze-rox/ (README, maintenance guide, change log).
- Checked live: the page loads with no errors, shows the latest hourly reading and all 24 hourly readings.

## 2026-10-29 13:35 — Single page for GitHub Pages

- Repository now holds one page, `index.html` (sg-haze-live v1.1), at the top level so it is the site's home page at https://jeremyhuang83.github.io/sg-haze-rox/; the second page was removed.
- README and maintenance guide rewritten for publishing with GitHub Pages; hosting-specific details removed.
- `tools/check_csp.py` now checks `index.html` by default.
- The page itself is unchanged.

## 2026-10-29 — Repository created

- Page source, maintenance guide, change log and a CSP hash checker (`tools/check_csp.py`) added.

## 2026-10-25 23:12 — sg-haze-live v1.1

**Problem fixed:** missing hours in the 24-hour PM2.5 trend.
data.gov.sg refuses bursts of requests. Each refresh fired 4 requests at once, and when the "today" or "yesterday" history request was refused, the page silently treated it as empty and replaced the whole trend history, dropping hours it already had.

**Changes**
- Requests go one at a time with a short pause, instead of 4 at once.
- A refused or failed request is retried once after 1.5–2.5 s.
- Trend history is merged: saved hours stay, the new hour is added, only the latest 24-hour window is kept.
- Day-by-day history is only requested when the 24-hour window has gaps. A normal refresh is 2 requests instead of 4.
- A failed PSI request falls back to the last saved PSI instead of failing the refresh.
- The 5pm PSI lookup also waits its turn.
- CSP script hash updated to match the new code.

**Not changed:** layout, colours, go/no-go thresholds, page title, 15-minute auto-refresh.

**Checked after deploy (23:11):** the live page loaded the new code with no errors, rebuilt all 24 hourly readings from an empty cache, and a repeat refresh made only 2 requests. CSP hashes match; the script passes a syntax check.

## 2026-10-22 — sg-haze-live v1.0

Original page: live NEA readings via data.gov.sg (v2 API with v1 fallback), region picker, easy-run / hard-session calls, SP-CCA training section, 24-hour trend, pull-to-refresh.
