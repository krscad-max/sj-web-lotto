Web Lotto MVP

Files under this directory:
- index.html, styles.css, app.js : static single-page app
- data/lotto_649.csv, data/lotto_max.csv : initial historical data (CSV, date first)
- scripts/fetch_magayo.py : simple fetcher to append latest draw to CSV (uses magayo pages)
- scripts/run_fetch.sh : wrapper for cron

Quick start (local)
1. Serve files: python3 -m http.server 8000 (from web-lotto directory) and open http://localhost:8000
2. To fetch and append latest results: cd scripts && ./run_fetch.sh

Cron suggestion (local machine):
# fetch daily at 21:30
30 21 * * * /Users/sj/.openclaw/workspace/web-lotto/scripts/run_fetch.sh

Notes & AdSense guidance
- Add About/Contact/Privacy pages before applying to AdSense.
- Do not promise winnings. Add clear disclaimer.
- Prefer a custom domain for higher AdSense approval odds.
