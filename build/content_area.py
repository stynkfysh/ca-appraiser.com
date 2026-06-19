# -*- coding: utf-8 -*-
"""Service-area page + 132 community pages for CA-Appraiser.com."""
import json, hashlib

# Canonical slug list (132) — order matches site map generation.
SLUGS = [
    "aguanga","alpine","anaheim","antioch","anza","banning","beaumont","berkeley","bonita","burbank",
    "calimesa","canyon-lake","cardiff","carlsbad","carmel-valley","cathedral-city","chino-hills","chino",
    "chula-vista","clairemont","coachella","concord","corona","coronado","costa-mesa","de-luz","del-mar",
    "descanso","desert-hot-springs","downey","eastvale","el-cajon","elk-grove","encinitas","escondido",
    "fairfield","fallbrook","fontana","fremont","french-valley","fullerton","garden-grove","glendale",
    "hayward","hemet","hesperia","hillcrest","hollywood","huntington-beach","imperial-beach","indian-wells",
    "indio","inglewood","jamul","jurupa-valley","la-jolla","la-mesa","la-quinta","lake-elsinore","lakeside",
    "lancaster","lemon-grove","long-beach","los-angeles","menifee","mira-mesa","modesto","moreno-valley",
    "mountain-view","murrieta","national-city","newport-beach","norco","north-park","oceanside","ontario",
    "orange","oxnard","pacific-beach","palm-desert","palm-springs","palmdale","pasadena","perris","pomona",
    "poway","ramona","rainbow","rancho-bernardo","rancho-cucamonga","rancho-mirage","rancho-santa-fe",
    "redlands","rialto","richmond","riverside","roseville","sacramento","salinas","san-diego","san-francisco",
    "san-jacinto","san-jose","san-marcos","san-mateo","san-ysidro","santa-ana","santa-barbara","santa-clara",
    "santa-clarita","santa-monica","santee","simi-valley","solana-beach","spring-valley","sun-city","sunnyvale",
    "temecula","thousand-oaks","thousand-palms","torrance","university-city","upland","vacaville","vallejo",
    "valley-center","ventura","victorville","vista","wildomar","winchester","yucaipa",
]

APPRAISAL_LINKS = [
    ("/date-of-death-appraisal", "Date of Death Appraisals"),
    ("/divorce-appraisal", "Divorce Appraisals"),
    ("/estate-appraisal", "Estate &amp; Trust Appraisals"),
    ("/bankruptcy-appraisal", "Bankruptcy Appraisals"),
    ("/prop-19-appraisal", "Proposition 19 Transfers"),
    ("/family-transaction-appraisal", "Family Transaction Appraisals"),
    ("/pre-purchase-appraisal", "Pre-Purchase Appraisals"),
    ("/pre-sale-appraisal", "Pre-Sale Appraisals"),
    ("/tax-appraisal", "Tax Appraisals"),
    ("/expert-witness", "Expert Witness &amp; Litigation"),
]


def _hash(slug):
    return int(hashlib.md5(slug.encode()).hexdigest(), 16)


def build(g):
    page, write = g["page"], g["write"]
    SITE, EMAIL = g["SITE"], g["EMAIL"]
    CITIES = g["CITIES"]
    COUNTY_ORDER_INPERSON = g["COUNTY_ORDER_INPERSON"]
    COUNTY_ORDER_DESKTOP = g["COUNTY_ORDER_DESKTOP"]

    # sanity: every slug present
    missing = [s for s in SLUGS if s not in CITIES]
    if missing:
        raise SystemExit("Missing city data for: " + ", ".join(missing))

    # ---------------------------------------------------------- SERVICE AREA PAGE
    by_county = {}
    for slug in SLUGS:
        c = CITIES[slug]
        by_county.setdefault(c["county"], []).append((slug, c["name"]))
    for k in by_county:
        by_county[k].sort(key=lambda x: x[1])

    def county_block(county, desktop=False):
        items = by_county.get(county, [])
        if not items:
            return ""
        links = "\n".join(
            f'                    <li><a href="/areas/{s}">{n}</a></li>' for s, n in items)
        tag = "Desktop appraisals" if desktop else "In-person &amp; desktop appraisals"
        return f"""            <div class="county-block">
                <h2>{county}</h2>
                <p class="county-meta">{len(items)} communities &middot; {tag}</p>
                <ul class="area-links">
{links}
                </ul>
            </div>"""

    inperson_html = "\n".join(county_block(c, desktop=False) for c in COUNTY_ORDER_INPERSON)
    desktop_html = "\n".join(county_block(c, desktop=True) for c in COUNTY_ORDER_DESKTOP)
    total = len(SLUGS)
    sa_schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": "CA-Appraiser.com", "url": SITE, "email": EMAIL, "priceRange": "$299 - $725",
        "areaServed": [{"@type": "AdministrativeArea", "name": c} for c in (COUNTY_ORDER_INPERSON + COUNTY_ORDER_DESKTOP)],
    }, indent=4) + '\n</script>'
    sa_body = f"""            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><span aria-current="page">Service Area</span></li></ul></nav>
            <h1>Where We Appraise in California</h1>
            <p class="narrow">CA-Appraiser.com provides in-person appraisals throughout <strong>San Diego County</strong> and <strong>Riverside County</strong>, and desktop appraisals across the rest of California — {total} communities in 16 counties. Backed by 22 years of experience and more than 7,000 completed reports, every appraisal reflects firsthand knowledge of the local market.</p>

            <h2 style="margin-top:8px;">In-Person &amp; Desktop Counties</h2>
            <p class="narrow">Full-service area: interior/exterior inspections, drive-by, and desktop reports are all available here.</p>
{inperson_html}

            <h2>Desktop Appraisals Across California</h2>
            <p class="narrow">Beyond our in-person counties, we prepare USPAP-compliant desktop appraisals statewide. Desktop reports draw on MLS data, public records, aerial imagery, and full market analysis, and are accepted by the IRS, courts, attorneys, and financial institutions for estate, divorce, bankruptcy, and tax matters.</p>
{desktop_html}

            <div class="callout">
                <p><strong>Don't see your city?</strong> We cover the entire state with desktop appraisals — even communities not listed here. For in-person work we serve San Diego and Riverside Counties. <a href="/contact">Ask us</a> and we'll confirm the best option for your property.</p>
            </div>
            <div class="cta-banner"><h2>Request an Appraisal</h2><p>Tell us where the property is and what the appraisal is for.</p><a href="/contact" class="cta-button">Get Started</a></div>"""
    write("/service-area", page(
        "/service-area", "Service Area — California | CA-Appraiser.com",
        f"CA-Appraiser.com serves {total}+ California communities. In-person appraisals in San Diego and Riverside Counties; desktop appraisals statewide including Los Angeles, Orange, the Bay Area, and Sacramento.",
        "appraisal service area California, San Diego appraiser, Riverside appraiser, desktop appraisal California, statewide appraiser",
        sa_body, active="/service-area", schema=sa_schema,
        hero=("/images/hero-aerial.jpg", "Aerial view of California residential neighborhoods",
              "Service Area", f"{total}+ communities across California", None)))

    # ---------------------------------------------------------------- AREA PAGES
    intro_variants = [
        ("CA-Appraiser.com provides certified real estate appraisal services throughout {city} and the surrounding {county} area. {blurb}",
         "With 22 years of experience and more than 7,000 completed appraisals, the practice specializes in non-lender valuations — date-of-death and step-up in basis, divorce, bankruptcy, estate and trust, and pre-purchase or pre-sale appraisals — written to be clear and defensible for {city} families, attorneys, and CPAs.",
         "The {city} housing stock includes {homes}, and every report reflects firsthand familiarity with how these properties trade in the local market."),
        ("Looking for a real estate appraiser in {city}? CA-Appraiser.com prepares certified, non-lender appraisals across {county}, led by Brian Ward. {blurb}",
         "Whether you're settling an estate, dividing property in a divorce, supporting a bankruptcy filing, or simply establishing what a home is worth, our reports are built to withstand scrutiny from the IRS, the courts, and opposing counsel.",
         "From {homes}, {city}'s market has its own character — and selecting the right comparable sales is what makes a valuation here credible."),
        ("CA-Appraiser.com serves {city} and the rest of {county} with certified residential real estate appraisals for purposes other than lending. {blurb}",
         "Our specialty is valuations that real people and institutions rely on: step-up in basis for inherited property, equitable division in divorce, probate and trust administration, and Proposition 19 transfers — each delivered in plain, well-supported language.",
         "Because {city} includes {homes}, an appraisal here demands local knowledge of how condition, location, and property type drive value."),
    ]

    market_variants = [
        "Residential values in {county} reflect the broader California market: shifting inventory, interest-rate movement, and steady long-term demand. Rather than rely on automated estimates, every {city} appraisal is built from the specific comparable sales that best reflect the subject property as of the relevant date. For a current opinion of value on a particular {city} property, <a href=\"/contact\">request an appraisal</a>.",
        "The {city} market moves with conditions across {county} — available supply, financing costs, and buyer demand all shape what homes actually sell for. We analyze the closed sales most comparable to your property rather than a one-size-fits-all index, which is what makes a report defensible. See our <a href=\"/market-reports\">California market notes</a> for context, or <a href=\"/contact\">request a property-specific value</a>.",
        "Like much of {county}, {city} has seen the inventory and pricing shifts playing out across California. Because a credible valuation depends on the right comparables — not a generic market average — we tailor every {city} report to the subject property and its effective date. <a href=\"/contact\">Contact us</a> for a current opinion of value.",
    ]

    for slug in SLUGS:
        c = CITIES[slug]
        city, county, blurb, homes, inperson = c["name"], c["county"], c["blurb"], c["homes"], c["inperson"]
        h = _hash(slug)
        iv = intro_variants[h % len(intro_variants)]
        mv = market_variants[(h // 7) % len(market_variants)]
        intro = "\n                ".join(
            f"<p>{para.format(city=city, county=county, blurb=blurb, homes=homes)}</p>" for para in iv)

        # service framing
        if inperson:
            service_line = (f"In {city}, every report type is available — Basic Desktop, Desktop, Drive-By, and a "
                            f"full Standard appraisal with in-person interior and exterior inspection.")
            hero_sub = f"Certified in-person &amp; desktop appraisals in {city}"
        else:
            service_line = (f"For {city} we provide USPAP-compliant desktop appraisals — built from MLS data, public "
                            f"records, and photographs — accepted by the IRS, courts, attorneys, and financial institutions.")
            hero_sub = f"Certified desktop appraisals for {city}, {county}"

        appr_items = "\n".join(
            f'                    <li><a href="{href}">{label}</a></li>' for href, label in APPRAISAL_LINKS)

        # featured pricing varies by tier
        if inperson:
            pricing_cards = """                    <div class="pricing-summary-card"><span class="pricing-summary-price">$299</span><strong>Basic Desktop</strong><p>Concise restricted-use report with full comparable-sales analysis. USPAP &amp; IRS compliant.</p></div>
                    <div class="pricing-summary-card pricing-summary-featured"><span class="pricing-summary-badge">Popular</span><span class="pricing-summary-price">$449</span><strong>Desktop</strong><p>Comprehensive report with property description, comp photos, maps, and market analysis.</p></div>
                    <div class="pricing-summary-card"><span class="pricing-summary-price">$575</span><strong>Drive-By</strong><p>Desktop analysis plus exterior photos and neighborhood observation.</p></div>
                    <div class="pricing-summary-card"><span class="pricing-summary-price">$625</span><strong>Standard</strong><p>Full interior &amp; exterior inspection with photos and condition assessment.</p></div>"""
        else:
            pricing_cards = """                    <div class="pricing-summary-card"><span class="pricing-summary-price">$299</span><strong>Basic Desktop</strong><p>Concise restricted-use report with full comparable-sales analysis. USPAP &amp; IRS compliant.</p></div>
                    <div class="pricing-summary-card pricing-summary-featured"><span class="pricing-summary-badge">Popular</span><span class="pricing-summary-price">$449</span><strong>Desktop</strong><p>Comprehensive report with property description, comp photos, maps, and market analysis.</p></div>
                    <div class="pricing-summary-card"><span class="pricing-summary-price">$550</span><strong>Desktop 2-4 Unit</strong><p>Full desktop appraisal for duplexes through fourplexes.</p></div>
                    <div class="pricing-summary-card"><span class="pricing-summary-price">$449</span><strong>Retrospective</strong><p>Date-of-death and prior-date values for estate, tax, and divorce matters.</p></div>"""

        market = mv.format(city=city, county=county)

        body = f"""            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><a href="/service-area">Service Area</a></li><li><span aria-current="page">{city}</span></li></ul></nav>

            <article class="city-intro-section">
                <h1>Real Estate Appraisal Services in {city}, {county}, California</h1>
                {intro}
                <p>{service_line}</p>
            </article>

            <article class="appraisal-types-section">
                <h3>Appraisal Types Available in {city}</h3>
                <p>We prepare the following non-lender appraisals for {city} property owners, attorneys, and CPAs:</p>
                <ul class="appraisal-types-list">
{appr_items}
                </ul>
            </article>

            <article class="market-snapshot-section">
                <h3>{city} Market Context</h3>
                <p>{market}</p>
            </article>

            <article class="services-pricing-section">
                <h3>Appraisal Services &amp; Pricing in {city}</h3>
                <p>Your fee is quoted up front before you commit — no hidden costs.</p>
                <div class="pricing-summary-grid">
{pricing_cards}
                </div>
                <div class="pricing-summary-extras">
                    <p><strong>2-4 Unit Properties:</strong> Desktop from $550 &nbsp;|&nbsp; Standard from $725</p>
                    <p><strong>Add-Ons:</strong> Sq ft measurement $35/1,500 sf &nbsp;|&nbsp; Rush +30% &nbsp;|&nbsp; Two-client fee $100</p>
                </div>
                <p style="margin-top:14px;"><a href="/services-fees">View full pricing details &rarr;</a></p>
            </article>

            <article class="contact-cta-section">
                <h3>Need an Appraisal in {city}?</h3>
                <p>Contact CA-Appraiser.com for a free consultation. We'll help you determine the right report for your situation and send a firm quote.</p>
                <div class="contact-info">
                    <p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
                    <p><a href="/contact" class="cta-button">Request an Appraisal Online</a></p>
                </div>
            </article>"""

        # schema
        lb = json.dumps({
            "@context": "https://schema.org/", "@type": "LocalBusiness",
            "name": "CA-Appraiser.com", "image": SITE + "/images/og-default.jpg",
            "description": f"Real estate appraisal services in {city}, {county} specializing in date-of-death, divorce, estate, bankruptcy, and other non-lender appraisals.",
            "address": {"@type": "PostalAddress", "streetAddress": "15877 Paseo Del Sur",
                        "addressLocality": "San Diego", "addressRegion": "CA",
                        "postalCode": "92127", "addressCountry": "US"},
            "email": EMAIL, "url": SITE + "/areas/" + slug, "priceRange": "$299 - $725",
            "serviceArea": {"@type": "GeoShape", "areaServed": f"{city}, {county}, CA"},
            "areaServed": {"@type": "City", "name": city + ", CA"},
            "knowsAbout": ["Real Estate Appraisal", "Date of Death Appraisal", "Divorce Appraisal",
                           "Estate Appraisal", "Bankruptcy Appraisal", "Proposition 19 Appraisal",
                           "Expert Witness Testimony"],
            "hasCredential": {"@type": "EducationalOccupationalCredential",
                              "name": "Certified Residential Real Estate Appraiser",
                              "credentialCategory": "Professional License"},
            "founder": {"@type": "Person", "name": "Brian Ward"}, "foundingDate": "2004",
            "parentOrganization": {"@type": "Organization", "name": "Brian Ward Appraisal", "url": "https://www.brianward.com"},
            "sameAs": ["https://www.brianward.com"],
        }, indent=4)
        bc = json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Service Area", "item": SITE + "/service-area"},
                {"@type": "ListItem", "position": 3, "name": city, "item": SITE + "/areas/" + slug},
            ],
        }, indent=4)
        schema = ('<script type="application/ld+json">\n' + lb + '\n</script>\n    '
                  '<script type="application/ld+json">\n' + bc + '\n</script>')

        title = f"{city} Real Estate Appraiser | Date of Death, Divorce & Estate | CA-Appraiser.com"
        desc = (f"Certified real estate appraisals in {city}, {county}, California. Date-of-death, divorce, "
                f"estate, bankruptcy, and Prop 19 valuations. {'In-person & desktop.' if inperson else 'Desktop appraisals.'} Request online.")
        kw = (f"{city} appraisal, {city} real estate appraiser, {county} appraiser, date of death appraisal {city}, "
              f"divorce appraisal {city}, estate appraisal {city}, bankruptcy appraisal {city}")

        write("/areas/" + slug, page(
            "/areas/" + slug, title, desc, kw, body, schema=schema, og_type="business.business",
            hero=(f"/images/areas/{slug}.jpg", f"Residential real estate in {city}, {county}",
                  f"{city} Real Estate Appraiser", hero_sub, ("Request an Appraisal", "/contact"))))

    print(f"area pages written: {len(SLUGS)} + service-area")
