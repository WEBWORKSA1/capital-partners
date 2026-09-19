# capital.partners

Small business funding calculators, guides and a funding matcher. Static site, hosted free on GitHub Pages, auto-updating.

## Turn on revenue (edit ONE file: `data/site.json`)
| Field | What to paste |
|---|---|
| `adsense_client` | `ca-pub-XXXXXXXXXXXXXXXX` (ads.txt and the ad code are generated automatically) |
| `adsense_slot_inline` | optional in-content slot ID; leave blank to use Auto ads |
| `ga4_id` | `G-XXXXXXX` (tracks `affiliate_click` and `match_complete` events) |
| `partners.<product>` | `{"name": "Lender", "url": "your affiliate link"}` for sba, term, loc, equipment, factoring, rbf, mca, equity |

Commit the change on GitHub. The `deploy-pages` workflow rebuilds and republishes every page. Each CTA, matcher result and comparison row switches from "Read the guide" to your affiliate link.

## What runs by itself
- **Weekdays:** `autopilot` pulls the WSJ Prime Rate from FRED (series DPRIME), commits `data/rates.json`, which triggers a rebuild. Every SBA rate cap, payment table, ticker value, calculator default and sitemap date updates.
- **Every push:** `deploy-pages` runs `python3 scripts/build.py` and publishes `public/` to GitHub Pages.

## One-time setup
1. Settings → Pages → Source: **GitHub Actions**.
2. Settings → Pages → Custom domain: `capital.partners`, then at the registrar add A records for `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 and a CNAME for `www` → `webworksa1.github.io`. Enforce HTTPS once the certificate is issued.

## Local build
`python3 scripts/build.py` (standard library only) → `public/`

## Layout
- `scripts/build.py` — generator (layout, calculators, SEO, schema)
- `scripts/content.py` — guide and calculator content
- `scripts/update_rates.py` — prime rate fetcher
- `data/site.json` — monetization config
- `data/rates.json` — current prime rate
- `assets/` — CSS, JS, favicon
