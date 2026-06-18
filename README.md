# CA-Appraiser.com

Static marketing site for **CA-Appraiser.com** — the California real estate appraisal practice of
Brian Ward, certified residential appraiser. Non-lender appraisals (date of death, divorce, estate,
bankruptcy, Prop 19, expert witness) with in-person service in San Diego & Riverside Counties and
desktop appraisals statewide.

## Stack
- Hand-built static HTML/CSS/JS, generated from templates in `build/`.
- Contact form handled by a Cloudflare Pages Function (`functions/api/contact.js`) that emails leads via Resend.
- Hosted on Cloudflare Pages, auto-deployed from `main`.

## Regenerating pages
```bash
cd build
python3 build.py            # regenerate all HTML + SEO files
python3 gen_placeholders.py # regenerate placeholder images
```

## Structure
- `index.html`, `services-fees.html`, `service-area.html`, `contact.html`, `faq.html`, `reviews.html`, `market-reports.html`
- `*-appraisal.html` + `expert-witness.html`, `pmi-removal.html` — service pages
- `areas/*.html` — 132 city/community pages
- `css/`, `js/`, `images/`, `functions/`
- `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, `_headers`, `_redirects`

## Environment variables (Cloudflare Pages)
- `RESEND_API_KEY` — Resend API key
- `RESEND_FROM` — verified sender (e.g. `CA-Appraiser <noreply@brianward.com>`)
- `RESEND_TO` — lead destination (`brian@brianward.com`)
