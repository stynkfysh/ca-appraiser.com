# -*- coding: utf-8 -*-
"""Technical SEO + AI-inclusion files for CA-Appraiser.com."""
import os
from content_area import SLUGS

CORE = [
    ("/", "1.0", "weekly"),
    ("/services-fees", "0.9", "monthly"),
    ("/service-area", "0.9", "monthly"),
    ("/contact", "0.8", "monthly"),
    ("/faq", "0.7", "monthly"),
    ("/reviews", "0.6", "monthly"),
    ("/market-reports", "0.6", "weekly"),
]
SERVICES = [
    "/date-of-death-appraisal", "/divorce-appraisal", "/bankruptcy-appraisal", "/estate-appraisal",
    "/tax-appraisal", "/pre-purchase-appraisal", "/pre-sale-appraisal", "/family-transaction-appraisal",
    "/insurance-appraisal", "/bonds-appraisal", "/prop-19-appraisal", "/expert-witness", "/pmi-removal",
]
LEGAL = ["/terms-of-use", "/privacy-policy"]


def build(g):
    SITE, EMAIL = g["SITE"], g["EMAIL"]
    ROOT = g["ROOT"]
    ISO = g["ISO"]
    CITIES = g["CITIES"]

    def w(rel, content):
        full = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(full) if os.path.dirname(full) else ROOT, exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)

    # -------------------------------------------------------------- sitemap.xml
    urls = []
    for path, pr, freq in CORE:
        urls.append((path, pr, freq))
    for path in SERVICES:
        urls.append((path, "0.8", "monthly"))
    for slug in SLUGS:
        urls.append(("/areas/" + slug, "0.7", "monthly"))
    for path in LEGAL:
        urls.append((path, "0.3", "yearly"))

    body = "\n".join(
        f"  <url>\n    <loc>{SITE}{p if p != '/' else '/'}</loc>\n"
        f"    <lastmod>{ISO}</lastmod>\n    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{pr}</priority>\n  </url>"
        for p, pr, freq in urls)
    w("sitemap.xml",
      '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + body + "\n</urlset>\n")

    # ---------------------------------------------------------------- robots.txt
    w("robots.txt",
      "User-agent: *\nAllow: /\n\n"
      "# AI crawlers welcome\nUser-agent: GPTBot\nAllow: /\n"
      "User-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n"
      "User-agent: Google-Extended\nAllow: /\n\n"
      f"Sitemap: {SITE}/sitemap.xml\n")

    # ------------------------------------------------------------------ _headers
    w("_headers",
      "# Cloudflare Pages headers — security + caching\n"
      "/*\n  X-Frame-Options: SAMEORIGIN\n  X-Content-Type-Options: nosniff\n"
      "  Referrer-Policy: strict-origin-when-cross-origin\n"
      "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n"
      "  X-XSS-Protection: 1; mode=block\n  Cache-Control: public, max-age=3600, must-revalidate\n\n"
      "/css/*\n  Cache-Control: public, max-age=31536000, immutable\n\n"
      "/js/*\n  Cache-Control: public, max-age=31536000, immutable\n\n"
      "/images/*\n  Cache-Control: public, max-age=2592000\n\n"
      "/favicon.ico\n  Cache-Control: public, max-age=2592000\n\n"
      "/sitemap.xml\n  Cache-Control: public, max-age=86400\n\n"
      "/robots.txt\n  Cache-Control: public, max-age=86400\n\n"
      "/llms.txt\n  Cache-Control: public, max-age=86400\n\n"
      "/llms-full.txt\n  Cache-Control: public, max-age=86400\n")

    # ---------------------------------------------------------------- _redirects
    w("_redirects",
      "# Cloudflare Pages redirects — canonicalize to clean URLs\n"
      "/index.html / 301\n"
      "/index / 301\n")

    # ------------------------------------------------------------------ llms.txt
    svc_lines = "\n".join(
        f"- [{label}]({SITE}{path}): {desc}"
        for path, label, desc in [
            ("/date-of-death-appraisal", "Date of Death Appraisal", "Retrospective valuations for IRS step-up in basis, estate tax, and probate"),
            ("/divorce-appraisal", "Divorce Appraisal", "Neutral property valuations for equitable division; two-party option and expert testimony"),
            ("/bankruptcy-appraisal", "Bankruptcy Appraisal", "Court-ready valuations for Chapter 7, 11, and 13 filings"),
            ("/estate-appraisal", "Estate & Trust Appraisal", "Fair market valuations for probate, trusts, and estate planning"),
            ("/prop-19-appraisal", "Proposition 19 Appraisal", "Reassessment-exposure valuations for inherited California property"),
            ("/tax-appraisal", "Tax Appraisal", "Property-tax appeals and IRS-compliant valuations"),
            ("/pre-purchase-appraisal", "Pre-Purchase Appraisal", "Independent value before buying a home"),
            ("/pre-sale-appraisal", "Pre-Sale Appraisal", "Independent value before listing a home"),
            ("/family-transaction-appraisal", "Family Transaction Appraisal", "Arm's-length value for transfers between relatives"),
            ("/insurance-appraisal", "Insurance Dispute Appraisal", "Independent value for insurance claim disputes"),
            ("/bonds-appraisal", "Bonds Appraisal", "Equity valuations for bail and surety bonds"),
            ("/expert-witness", "Expert Witness & Litigation", "Qualified testimony and appraisal review"),
            ("/pmi-removal", "PMI Removal Appraisal", "Value documentation to cancel private mortgage insurance"),
        ])
    w("llms.txt",
      f"""# CA-Appraiser.com

> CA-Appraiser.com is the California real estate appraisal practice of Brian Ward, a certified residential appraiser with 22 years of experience and more than 7,000 completed appraisals. The practice specializes in non-lender (non-mortgage) appraisals: date of death and step-up in basis, divorce, bankruptcy, estate and trust, Proposition 19 transfers, tax matters, and pre-purchase/pre-sale valuations, plus qualified expert witness testimony. In-person appraisals are available in San Diego and Riverside Counties; desktop appraisals are available statewide across California.

## Business Information

- Name: CA-Appraiser.com (Brian Ward, Certified Appraiser)
- Email: {EMAIL}
- Website: {SITE}
- Contact: web form at {SITE}/contact (no phone — online and email only)
- Address: 15877 Paseo Del Sur, San Diego, CA 92127
- Service Area: In-person in San Diego and Riverside Counties; desktop appraisals statewide across California (130+ communities, 16 counties)
- Price Range: $299 - $725
- Experience: 22 years, 7,000+ appraisals, established 2004

## Pricing (single-family homes & condos)

- Basic Desktop Appraisal: $299 (restricted-use report, no inspection)
- Desktop Appraisal: $449 (comprehensive report, no inspection) — most popular
- Drive-By Appraisal: $575 (desktop plus exterior observation)
- Standard Appraisal: $625 (full interior & exterior inspection)
- 2-4 Unit Desktop: $550 | 2-4 Unit Standard: $725
- Add-ons: Square-footage measurement $35/1,500 sf; Rush +30%; Two-client fee $100

## Appraisal Services

{svc_lines}

## Key Pages

- [Home]({SITE}/)
- [Services & Fees]({SITE}/services-fees)
- [Service Area]({SITE}/service-area)
- [Contact / Request an Appraisal]({SITE}/contact)
- [FAQ]({SITE}/faq)
- [Reviews]({SITE}/reviews)
- [Market Reports]({SITE}/market-reports)

## Optional

- [Full LLM context]({SITE}/llms-full.txt)
""")

    # ------------------------------------------------------------- llms-full.txt
    area_lines = []
    for slug in SLUGS:
        c = CITIES[slug]
        tier = "in-person & desktop" if c["inperson"] else "desktop"
        area_lines.append(f"- {c['name']}, {c['county']} ({tier}): {SITE}/areas/{slug}")
    areas_block = "\n".join(area_lines)
    w("llms-full.txt",
      f"""# CA-Appraiser.com — Full Reference

## Overview

CA-Appraiser.com is the California real estate appraisal practice of Brian Ward, a certified residential real estate appraiser (established 2004) with 22 years of experience and more than 7,000 completed appraisals. The firm focuses exclusively on appraisals NOT related to obtaining a mortgage. Reports are written in plain, logical language so that non-appraisers — families, attorneys, CPAs, trustees, judges, and the IRS — can understand and rely on them. Contact is by web form ({SITE}/contact) or email ({EMAIL}); the practice does not publish a phone number.

## Specialties

- Date of Death / Step-Up in Basis: retrospective valuations dated to the date of passing, prepared to meet IRS requirements for adjusting the cost basis of inherited property and for estate-tax filings.
- Divorce: neutral valuations for equitable division in a community-property state; current or retrospective (date-of-separation) values; two-party reports both spouses can share; expert testimony.
- Bankruptcy: defensible valuations for Chapter 7, 11, and 13 filings; petition-date values; lien-stripping support.
- Estate & Trust: probate, trust funding and administration, estate planning, equitable distribution among heirs.
- Proposition 19: fair-market-value analysis to understand reassessment exposure when inherited California property transfers between parents and children.
- Tax: assessment appeals, step-up in basis, estate and gift tax support.
- Pre-Purchase / Pre-Sale: independent values for buyers and sellers, including for-sale-by-owner transactions.
- Family Transactions: arm's-length values for sales and transfers between relatives, gift-of-equity documentation.
- Insurance Disputes: independent market-value analysis for contested claims.
- Bonds: equity valuations for bail and surety bonds, often expedited.
- Expert Witness & Litigation: qualified testimony, deposition, and appraisal review.
- PMI Removal: current-value documentation to cancel private mortgage insurance.

## Report Types & Pricing

- Basic Desktop ($299): restricted-use report; full comparable-sales analysis; USPAP & IRS compliant; no site visit. Popular for date-of-death and estate values.
- Desktop ($449): comprehensive report with property description, comparable-sale photos, location/neighborhood maps, and market-conditions analysis; no site visit. Most popular overall.
- Drive-By ($575): desktop analysis plus exterior photographs and neighborhood observation.
- Standard ($625): full in-person interior and exterior inspection, photographs, and condition assessment. Strongest for court, IRS, and buyer reliance.
- 2-4 Unit: Desktop $550 / Standard $725.
- Add-ons: square-footage measurement $35 per 1,500 sf; rush delivery +30%; two-client fee $100.
- All fees are starting prices; the exact fee is quoted in writing before the client commits.

## How Fees Are Determined

Three factors: property complexity (acreage, unusual features, non-standard construction), time required for research and report preparation, and intended use (court or IRS submission carries greater professional responsibility).

## Service Area

In-person appraisals: San Diego County and Riverside County (full interior/exterior, drive-by, and desktop reports). Desktop appraisals: statewide across California, including Los Angeles, Orange, San Bernardino, Ventura, Santa Clara, Alameda, Contra Costa, Sacramento, Solano, San Francisco, San Mateo, Santa Barbara, Placer, Monterey, and Stanislaus Counties.

### Communities Served

{areas_block}

## Contact

- Web form: {SITE}/contact
- Email: {EMAIL}
- Address: 15877 Paseo Del Sur, San Diego, CA 92127
- No phone number; inquiries are handled online and by email.
""")

    print("seo/ai files written")
