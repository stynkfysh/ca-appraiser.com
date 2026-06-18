#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CA-Appraiser.com static site generator.
Generates all core, service, legal, and 132 area pages plus SEO/AI files
from shared templates. Run: python3 build.py
"""
import os, html, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://www.ca-appraiser.com"
BRAND = "CA-Appraiser.com"
EMAIL = "brian@brianward.com"
TODAY = datetime.date(2026, 6, 17)
ISO = TODAY.isoformat()

NAV = [
    ("/", "Home"),
    ("/services-fees", "Services &amp; Fees"),
    ("/service-area", "Service Area"),
    ("/market-reports", "Market Reports"),
    ("/faq", "FAQ"),
    ("/reviews", "Reviews"),
]

def header(active):
    links = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        links.append(f'                    <a href="{href}"{cls}>{label}</a>')
    links.append('                    <a href="/contact" class="nav-cta">Request Appraisal</a>')
    nav = "\n".join(links)
    return f"""    <header class="header">
        <div class="header-content">
            <div class="logo-container">
                <a href="/" style="text-decoration:none;">
                    <span class="logo-title">CA-Appraiser<span class="dot">.com</span></span>
                    <span class="logo-sub">Certified CA Real Estate Appraiser</span>
                </a>
            </div>
            <button class="mobile-nav-toggle" aria-label="Toggle navigation menu" aria-expanded="false">&#9776; Menu</button>
            <nav class="top-nav" aria-label="Main Navigation">
                <div class="top-nav-inner">
{nav}
                </div>
            </nav>
        </div>
    </header>"""

FOOTER = f"""    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h4>CA-Appraiser.com</h4>
                <p>Certified Residential Real Estate Appraiser</p>
                <p>Brian Ward, Certified Appraiser</p>
                <p>15877 Paseo Del Sur<br>San Diego, CA 92127</p>
                <p>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
                <p><a href="/contact">Request an appraisal online &rarr;</a></p>
            </div>
            <div class="footer-section">
                <h4>Services</h4>
                <ul>
                    <li><a href="/date-of-death-appraisal">Date of Death</a></li>
                    <li><a href="/divorce-appraisal">Divorce</a></li>
                    <li><a href="/bankruptcy-appraisal">Bankruptcy</a></li>
                    <li><a href="/estate-appraisal">Estate &amp; Trust</a></li>
                    <li><a href="/prop-19-appraisal">Prop 19 Transfers</a></li>
                    <li><a href="/expert-witness">Expert Witness</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Company</h4>
                <ul>
                    <li><a href="/services-fees">Services &amp; Fees</a></li>
                    <li><a href="/service-area">Service Area</a></li>
                    <li><a href="/contact">Contact</a></li>
                    <li><a href="/faq">FAQ</a></li>
                    <li><a href="/reviews">Reviews</a></li>
                    <li><a href="/terms-of-use">Terms</a> &middot; <a href="/privacy-policy">Privacy</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 CA-Appraiser.com. All rights reserved. Certified Residential Real Estate Appraiser serving California.</p>
        </div>
    </footer>"""

def page(path, title, description, keywords, body, active="",
         schema="", canonical=None, og_type="website", hero=None, h1_in_hero=False):
    """Assemble a full HTML document. `path` is the clean URL (e.g. /contact)."""
    canonical = canonical or (SITE + (path if path != "/" else "/"))
    hero_html = ""
    if hero:
        img, alt, headline, sub, cta = hero
        tag = "h1" if h1_in_hero else "h2"
        cta_html = f'\n            <a href="{cta[1]}" class="cta-button">{cta[0]}</a>' if cta else ""
        hero_html = f"""
    <section class="hero-banner">
        <img src="{img}" alt="{alt}" class="hero-image" width="1180" height="440">
        <div class="hero-overlay">
            <{tag} class="hero-headline">{headline}</{tag}>
            <p class="hero-sub">{sub}</p>{cta_html}
        </div>
    </section>"""
    schema_block = ("\n    " + schema.strip()) if schema else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{html.escape(description, quote=True)}">
    <meta name="keywords" content="{html.escape(keywords, quote=True)}">
    <meta name="author" content="CA-Appraiser.com — Brian Ward, Certified Appraiser">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">

    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="{html.escape(description, quote=True)}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="CA-Appraiser.com">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{html.escape(title, quote=True)}">
    <meta name="twitter:description" content="{html.escape(description, quote=True)}">

    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">
    <link rel="stylesheet" href="/css/style.css?v=20260617">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
</head>
<body>
    <a href="#main-content" class="skip-to-content">Skip to main content</a>{schema_block}
{header(active)}{hero_html}
    <main id="main-content" class="page-wrapper">
        <section class="main-content">
{body}
        </section>
    </main>
{FOOTER}
    <script src="/js/main.js"></script>
</body>
</html>
"""

def write(path_clean, content):
    """path_clean like '/contact' -> contact.html ; '/' -> index.html ; '/areas/x' -> areas/x.html"""
    if path_clean == "/":
        rel = "index.html"
    else:
        rel = path_clean.strip("/") + ".html"
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return rel

# Shared JSON-LD LocalBusiness (no telephone — web form only)
def local_business_schema(extra_desc, area_served=None):
    area = area_served or [
        {"@type": "AdministrativeArea", "name": "San Diego County, CA"},
        {"@type": "AdministrativeArea", "name": "Riverside County, CA"},
        {"@type": "State", "name": "California", "description": "Desktop appraisals available statewide"},
    ]
    import json
    obj = {
        "@context": "https://schema.org/",
        "@type": "LocalBusiness",
        "@id": SITE + "/#business",
        "name": "CA-Appraiser.com",
        "alternateName": "Brian Ward, Certified Appraiser",
        "image": SITE + "/images/og-default.jpg",
        "description": extra_desc,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "15877 Paseo Del Sur",
            "addressLocality": "San Diego",
            "addressRegion": "CA",
            "postalCode": "92127",
            "addressCountry": "US",
        },
        "email": EMAIL,
        "url": SITE,
        "priceRange": "$299 - $725",
        "areaServed": area,
        "knowsAbout": [
            "Date of Death Real Estate Appraisal", "Step-Up in Basis Tax Valuation",
            "Retrospective Real Estate Appraisal", "Divorce Property Appraisal",
            "Bankruptcy Real Estate Appraisal", "Estate and Probate Appraisal",
            "Proposition 19 Transfer Appraisal", "Expert Witness Testimony",
            "Litigation Support Appraisal", "Pre-Purchase Home Appraisal",
            "Pre-Sale Home Appraisal", "Family Transaction Appraisal",
        ],
        "hasCredential": {
            "@type": "EducationalOccupationalCredential",
            "name": "Certified Residential Real Estate Appraiser",
            "credentialCategory": "Professional License",
        },
        "founder": {"@type": "Person", "name": "Brian Ward"},
        "foundingDate": "2004",
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "email": EMAIL,
            "url": SITE + "/contact",
            "areaServed": "US-CA",
            "availableLanguage": "English",
        },
    }
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=4) + '\n</script>'

if __name__ == "__main__":
    import content_data, content_core, content_service, content_area, content_seo
    G = globals()
    G["CITIES"] = content_data.CITIES
    G["DESKTOP_ONLY_CITY_NAMES"] = content_data.DESKTOP_ONLY_CITY_NAMES
    G["BLOG_POSTS"] = content_data.BLOG_POSTS
    G["COUNTY_ORDER_INPERSON"] = content_data.COUNTY_ORDER_INPERSON
    G["COUNTY_ORDER_DESKTOP"] = content_data.COUNTY_ORDER_DESKTOP
    content_core.build(G)
    content_service.build(G)
    content_area.build(G)
    content_seo.build(G)
    print("Build complete.")
