# -*- coding: utf-8 -*-
"""Core, legal, and utility pages for CA-Appraiser.com."""
import json

PURPOSE_OPTIONS = [
    ("bankruptcy", "Bankruptcy"), ("date-of-death", "Date of Death"), ("divorce", "Divorce"),
    ("estate", "Estate"), ("tax", "Tax"), ("before-buying", "Before Buying"),
    ("before-selling", "Before Selling"), ("family-transaction", "Family Transaction"),
    ("insurance-dispute", "Insurance Dispute"), ("prop-19", "Proposition 19 Transfer"),
    ("bonds", "Bonds"), ("other", "Other"),
]
TYPE_OPTIONS = [
    ("", "- Select Appraisal Type -"),
    ("basic-desktop", "Basic Desktop Appraisal — $299"),
    ("desktop", "Desktop Appraisal — $449"),
    ("drive-by", "Drive-By Appraisal — $575"),
    ("standard", "Standard Appraisal — $625"),
    ("desktop-2-4", "Desktop 2-4 Unit — $550"),
    ("standard-2-4", "Standard 2-4 Unit — $725"),
    ("not-sure", "Not sure — help me decide"),
]


def build(g):
    page, write, lbs = g["page"], g["write"], g["local_business_schema"]
    SITE, EMAIL = g["SITE"], g["EMAIL"]

    # ---------------------------------------------------------------- HOME
    home_schema = lbs(
        "CA-Appraiser.com is a certified California residential real estate appraisal practice led by "
        "Brian Ward, with 22 years of experience and more than 7,000 completed appraisals. We specialize "
        "in non-lender appraisals — date of death and step-up in basis, divorce, bankruptcy, estate and "
        "trust, Proposition 19 transfers, and pre-purchase/pre-sale valuations — and provide qualified "
        "expert witness testimony. In-person appraisals across San Diego and Riverside Counties; desktop "
        "appraisals statewide across California."
    )
    home_body = f"""            <div class="stats-bar">
                <div class="stat-item"><span class="stat-number">22+</span><span class="stat-label">Years Appraising</span></div>
                <div class="stat-item"><span class="stat-number">7,000+</span><span class="stat-label">Reports Completed</span></div>
                <div class="stat-item"><span class="stat-number">130+</span><span class="stat-label">California Communities</span></div>
            </div>

            <div class="narrow">
                <h2>A Different Kind of Appraisal — Built for People, Not Lenders</h2>
                <p>Most appraisals are written for banks. Ours are written for the people who actually have to read them — the families, attorneys, CPAs, judges, and trustees who need a property value they can understand and defend. CA-Appraiser.com is the California practice of certified appraiser Brian Ward, and every report is prepared to be clear, logical, and able to withstand scrutiny from the IRS, opposing counsel, and the courts.</p>
                <p>We focus exclusively on valuations <em>not</em> tied to a mortgage: settling an estate, dividing property in a divorce, establishing a date-of-death value for a step-up in basis, supporting a bankruptcy filing, or simply knowing what a home is truly worth before you buy or sell. Your fee is quoted up front, and the appraiser who answers your questions is the same one who signs your report.</p>
            </div>

            <div class="services-section">
                <h2>What We Appraise For</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-card-icon">&#9733;</div>
                        <h3>Date of Death &amp; Step-Up</h3>
                        <p>Retrospective valuations dated to the date of passing for IRS step-up in basis, estate tax, probate, and trust administration.</p>
                        <a href="/date-of-death-appraisal" class="learn-more">Learn more</a>
                    </div>
                    <div class="service-card">
                        <div class="service-card-icon">&#9878;</div>
                        <h3>Divorce</h3>
                        <p>Neutral, defensible valuations for equitable division, with a two-party option so both spouses share one impartial report.</p>
                        <a href="/divorce-appraisal" class="learn-more">Learn more</a>
                    </div>
                    <div class="service-card">
                        <div class="service-card-icon">&#9881;</div>
                        <h3>Bankruptcy</h3>
                        <p>Court-ready property valuations for Chapter 7, 11, and 13 filings that hold up before the trustee and the court.</p>
                        <a href="/bankruptcy-appraisal" class="learn-more">Learn more</a>
                    </div>
                    <div class="service-card">
                        <div class="service-card-icon">&#8962;</div>
                        <h3>Estate &amp; Trust</h3>
                        <p>Fair market valuations for probate, trust funding, estate planning, and equitable distribution among heirs.</p>
                        <a href="/estate-appraisal" class="learn-more">Learn more</a>
                    </div>
                    <div class="service-card">
                        <div class="service-card-icon">&#9873;</div>
                        <h3>Proposition 19 Transfers</h3>
                        <p>Valuations that help families understand reassessment exposure when inherited California property changes hands.</p>
                        <a href="/prop-19-appraisal" class="learn-more">Learn more</a>
                    </div>
                    <div class="service-card">
                        <div class="service-card-icon">&#9878;</div>
                        <h3>Expert Witness &amp; Litigation</h3>
                        <p>Qualified testimony, appraisal review, and litigation-ready reports for contested valuation matters.</p>
                        <a href="/expert-witness" class="learn-more">Learn more</a>
                    </div>
                </div>
            </div>

            <div class="cta-banner">
                <h2>Desktop Appraisals Anywhere in California</h2>
                <p>Outside San Diego or Riverside County? We prepare USPAP-compliant desktop appraisals for estate, divorce, bankruptcy, and tax matters in more than 130 communities across 16 California counties — from Los Angeles and Orange County to the Bay Area and Sacramento.</p>
                <a href="/service-area" class="cta-button alt">See where we appraise</a>
            </div>

            <div class="why-section">
                <h2>Why Clients Choose Us</h2>
                <div class="why-grid">
                    <div class="why-item"><strong>Reports that hold up</strong><p>Detailed, clearly written analysis designed to satisfy attorneys, judges, the IRS, and opposing counsel — not just check a box.</p></div>
                    <div class="why-item"><strong>You talk to the appraiser</strong><p>No call centers and no trainees. The certified appraiser who prepares your report is the person you reach with questions.</p></div>
                    <div class="why-item"><strong>Transparent pricing</strong><p>Desktop reports from $299. Your exact fee is quoted before you commit — no surprises, no pressure.</p></div>
                    <div class="why-item"><strong>Deep experience</strong><p>22 years and more than 7,000 appraisals across California's residential markets.</p></div>
                    <div class="why-item"><strong>An honest pledge</strong><p>If we don't believe we can produce a credible valuation for your situation, we'll tell you and decline the assignment.</p></div>
                    <div class="why-item"><strong>Statewide reach</strong><p>In-person service in San Diego and Riverside Counties, desktop appraisals everywhere else in California.</p></div>
                </div>
            </div>

            <div class="cta-banner">
                <h2>Ready to Get Started?</h2>
                <p>Tell us about your property and what the appraisal is for. We'll reply with the right report type and a firm quote — no obligation, no sales pressure.</p>
                <a href="/contact" class="cta-button">Request an Appraisal</a>
                <span class="cta-phone">or email <a href="mailto:{EMAIL}">{EMAIL}</a></span>
            </div>"""
    write("/", page(
        "/", "CA-Appraiser.com | Date of Death, Divorce, Estate & Bankruptcy Appraiser in California",
        "Certified California real estate appraiser with 22 years' experience and 7,000+ appraisals. Date of death, step-up in basis, divorce, bankruptcy, estate, and Prop 19 appraisals. Desktop appraisals statewide. Request online.",
        "California real estate appraiser, date of death appraisal, step up in basis appraisal, divorce appraisal, bankruptcy appraisal, estate appraisal, Prop 19 appraisal, desktop appraisal California, certified residential appraiser",
        home_body, active="/", schema=home_schema,
        hero=("/images/hero-home.jpg", "California residential homes at golden hour",
              "Certified California Appraisals,<br>Written to Be Understood",
              "Date-of-death, divorce, bankruptcy, estate &amp; Prop 19 valuations — in-person in San Diego &amp; Riverside Counties, desktop statewide.",
              ("Request an Appraisal", "/contact")),
        h1_in_hero=True))

    # ------------------------------------------------------------ SERVICES & FEES
    fees_schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "OfferCatalog",
        "name": "Appraisal Services and Fees",
        "url": SITE + "/services-fees",
        "itemListElement": [
            {"@type": "Offer", "name": "Basic Desktop Appraisal", "price": "299", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "Desktop Appraisal", "price": "449", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "Drive-By Appraisal", "price": "575", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "Standard Appraisal", "price": "625", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "Desktop Appraisal (2-4 Unit)", "price": "550", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "Standard Appraisal (2-4 Unit)", "price": "725", "priceCurrency": "USD"},
        ],
    }, indent=4) + '\n</script>'
    fees_body = """            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><span aria-current="page">Services &amp; Fees</span></li></ul></nav>
            <h1>Appraisal Services &amp; Fees</h1>
            <p class="narrow">The prices below cover the great majority of properties we appraise. Every assignment can carry additional fees for unusual location, complexity, or liability — but you will never be surprised. We quote your exact fee in writing before you commit.</p>

            <div class="price-tier-group">
                <h2>Single-Family Homes &amp; Condominiums</h2>
                <div class="pricing-cards">
                    <div class="price-card">
                        <span class="price-amount">$299</span>
                        <h3>Basic Desktop</h3>
                        <div class="price-degree">Restricted-use report</div>
                        <p>The same analytical method and value conclusion as our Desktop report, delivered in a shorter, restricted-use format. USPAP &amp; IRS compliant — a popular choice for date-of-death and estate valuations.</p>
                        <ul><li>Full comparable-sales analysis</li><li>USPAP &amp; IRS compliant</li><li>Revision assurance</li><li>No property visit required</li></ul>
                    </div>
                    <div class="price-card featured">
                        <span class="price-badge">Most Popular</span>
                        <span class="price-amount">$449</span>
                        <h3>Desktop</h3>
                        <div class="price-degree">Comprehensive report</div>
                        <p>A full written report with detailed property description, comparable-sales analysis, market-conditions commentary, location maps, and photographs. The everyday choice for estates, trusts, CPAs, and attorneys.</p>
                        <ul><li>Detailed property description</li><li>Location &amp; neighborhood maps</li><li>Comparable-sale photographs</li><li>Market conditions analysis</li><li>USPAP &amp; IRS compliant</li></ul>
                    </div>
                    <div class="price-card">
                        <span class="price-amount">$575</span>
                        <h3>Drive-By</h3>
                        <div class="price-degree">Exterior observed</div>
                        <p>Everything in the Desktop report, plus the appraiser drives to the property to photograph and observe its exterior condition and immediate neighborhood.</p>
                        <ul><li>Everything in Desktop</li><li>Exterior photographs</li><li>Neighborhood observation</li></ul>
                    </div>
                    <div class="price-card">
                        <span class="price-amount">$625</span>
                        <h3>Standard</h3>
                        <div class="price-degree">Full inspection</div>
                        <p>A complete appraisal with in-person interior and exterior inspection, photographs, and a detailed condition assessment. The strongest choice when a court, the IRS, or a buyer needs to know the appraiser was inside the home.</p>
                        <ul><li>Interior &amp; exterior inspection</li><li>Interior &amp; exterior photographs</li><li>Detailed condition assessment</li><li>Court &amp; IRS ready</li></ul>
                    </div>
                </div>
            </div>

            <div class="price-tier-group">
                <h2>2-4 Unit Properties</h2>
                <p>Duplexes, triplexes, and fourplexes.</p>
                <div class="addon-grid">
                    <div class="addon-card"><span class="price-amount">$550</span><h3>Desktop (2-4 Unit)</h3><p>Full desktop appraisal for 2-4 unit properties based on public records and MLS data.</p></div>
                    <div class="addon-card"><span class="price-amount">$725</span><h3>Standard (2-4 Unit)</h3><p>Full standard appraisal including in-person interior inspection of every unit.</p></div>
                </div>
            </div>

            <div class="price-tier-group">
                <h2>Add-On Services</h2>
                <div class="addon-grid">
                    <div class="addon-card"><span class="price-amount">$35</span><h3>Square-Footage Measurement</h3><p>Laser-measured living area with a certified sketch. Charged per 1,500 sq ft.</p></div>
                    <div class="addon-card"><span class="price-amount">+30%</span><h3>Rush Delivery</h3><p>Expedited turnaround when our schedule allows. Confirmed before you commit.</p></div>
                    <div class="addon-card"><span class="price-amount">$100</span><h3>Two-Client Fee</h3><p>When one report is prepared for two separate clients — for example, both spouses in a divorce.</p></div>
                </div>
            </div>

            <h2>Which Report Do I Need?</h2>
            <div class="callout">
                <p><strong>Basic Desktop ($299)</strong> — Same methodology and conclusion as the Desktop, in a concise restricted-use format without maps, photos, or a full property write-up. Popular for date-of-death and estate values.</p>
                <p><strong>Desktop ($449)</strong> — The comprehensive, well-documented report most people want: property description, maps, comparable-sale photos, and market analysis. Ideal for CPAs, trustees, and the courts.</p>
                <p><strong>Standard ($625)</strong> — Everything in the Desktop, plus an in-person inspection with photographs and a condition assessment. The right call when someone needs to know an appraiser personally walked the property.</p>
                <p style="margin-bottom:0;">Not sure? <a href="/contact">Tell us your situation</a> and we'll recommend the right report — there's no charge for a quick consultation.</p>
            </div>

            <h2>How Fees Are Determined</h2>
            <p>Three things drive a fee: the <strong>complexity</strong> of the property (large acreage, unusual features, or non-standard construction take more research), the <strong>time</strong> involved in research and report preparation, and the <strong>intended use</strong> (reports prepared for court or IRS submission carry greater professional responsibility). The prices above are typical starting points; your exact fee is always quoted before you commit.</p>

            <div class="cta-banner">
                <h2>Get a Firm Quote</h2>
                <p>Send us the property and what the appraisal is for. We'll confirm the right report and your exact price.</p>
                <a href="/contact" class="cta-button">Request a Quote</a>
            </div>"""
    write("/services-fees", page(
        "/services-fees", "Appraisal Services & Fees | CA-Appraiser.com",
        "California appraisal services and fees: Basic Desktop $299, Desktop $449, Drive-By $575, Standard $625, plus 2-4 unit and add-on pricing. Your exact fee is quoted before you commit.",
        "appraisal fees California, appraisal cost, desktop appraisal price, standard appraisal price, date of death appraisal cost, real estate appraisal fees",
        fees_body, active="/services-fees", schema=fees_schema))

    # ----------------------------------------------------------------- CONTACT
    purpose_opts = "\n".join(
        f'                    <option value="{v}">{t}</option>' for v, t in PURPOSE_OPTIONS)
    type_opts = "\n".join(
        f'                    <option value="{v}">{t}</option>' for v, t in TYPE_OPTIONS)
    contact_schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org/",
        "@type": "ContactPage",
        "name": "Contact CA-Appraiser.com",
        "description": "Request a California real estate appraisal or a quote online.",
        "mainEntity": {
            "@type": "LocalBusiness", "name": "CA-Appraiser.com", "email": EMAIL,
            "url": SITE, "priceRange": "$299 - $725",
            "areaServed": ["San Diego County, CA", "Riverside County, CA", "California"],
        },
    }, indent=4) + '\n</script>'
    contact_body = f"""            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><span aria-current="page">Contact</span></li></ul></nav>
            <h1>Request an Appraisal</h1>
            <p class="narrow">The fastest way to reach us is the form below. Tell us about the property and what the appraisal is for, and we'll reply with the right report type and a firm quote. There's no cost or obligation for a consultation, and your information is never shared.</p>

            <div id="form-success" style="display:none; background:#e7f3ec; border:1px solid #2e7d4f; padding:14px 18px; border-radius:8px; margin-bottom:16px; color:#1f5b39;">
                <strong>Thank you!</strong> Your request has been sent. We'll get back to you shortly.
            </div>
            <div id="form-error" style="display:none; background:#fbeae5; border:1px solid #b5532a; padding:14px 18px; border-radius:8px; margin-bottom:16px; color:#8a3c1d;">
                <strong>Something went wrong.</strong> Please try again, or email us directly at <a href="mailto:{EMAIL}">{EMAIL}</a>.
            </div>

            <div class="contact-grid">
                <form class="contact-form" action="/api/contact" method="POST">
                    <label for="name">Name <span style="color:#b5532a;">*</span></label>
                    <input type="text" id="name" name="name" required>

                    <label for="email">Email <span style="color:#b5532a;">*</span></label>
                    <input type="email" id="email" name="email" required>

                    <label for="phone">Phone</label>
                    <input type="tel" id="phone" name="phone">

                    <label for="street-address">Street Address</label>
                    <input type="text" id="street-address" name="street-address">

                    <div style="display:flex; gap:16px;">
                        <div style="flex:1;">
                            <label for="city">City</label>
                            <input type="text" id="city" name="city">
                        </div>
                        <div style="flex:0 0 130px;">
                            <label for="zipcode">Zip Code</label>
                            <input type="text" id="zipcode" name="zipcode" pattern="[0-9]{{5}}" maxlength="5" inputmode="numeric">
                        </div>
                    </div>

                    <label for="appraisal-purpose">Appraisal Purpose <span style="color:#b5532a;">*</span></label>
                    <select id="appraisal-purpose" name="appraisal-purpose" required>
                        <option value="">- Select Appraisal Purpose -</option>
{purpose_opts}
                    </select>

                    <label for="appraisal-type">Appraisal Type</label>
                    <select id="appraisal-type" name="appraisal-type">
{type_opts}
                    </select>
                    <p style="font-size:13px; color:#76817a; margin:6px 0 0;">Fees listed are starting prices. Complex, high-liability, or extended-travel properties may be higher. Your exact fee is quoted before you commit.</p>

                    <label for="message">Additional Information</label>
                    <textarea id="message" name="message" rows="5"></textarea>

                    <button type="submit">Send Request</button>
                </form>

                <aside class="contact-aside">
                    <h3>Prefer email?</h3>
                    <p>Reach the appraiser directly at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
                    <h3 style="margin-top:18px;">What happens next</h3>
                    <p>We review your request, confirm the report type that fits your situation, and send a firm written quote. Once you approve, we schedule the work and keep you updated through delivery.</p>
                    <h3 style="margin-top:18px;">Service area</h3>
                    <p>In-person appraisals across San Diego &amp; Riverside Counties; desktop appraisals statewide across California.</p>
                </aside>
            </div>

            <script>
            (function() {{
                var params = new URLSearchParams(window.location.search);
                var status = params.get('status');
                if (status === 'success') {{
                    document.getElementById('form-success').style.display = 'block';
                    document.querySelector('form').style.display = 'none';
                    document.getElementById('form-success').scrollIntoView({{ behavior: 'smooth' }});
                }} else if (status === 'error') {{
                    document.getElementById('form-error').style.display = 'block';
                    document.getElementById('form-error').scrollIntoView({{ behavior: 'smooth' }});
                }}
            }})();
            </script>
            <script>
            (function() {{
                var desktopOnly = {json.dumps(g["DESKTOP_ONLY_CITY_NAMES"])};
                var allOptions = {json.dumps([{"value": v, "text": t} for v, t in TYPE_OPTIONS])};
                var desktopOptions = allOptions.filter(function(o){{
                    return ['', 'basic-desktop', 'desktop', 'desktop-2-4', 'not-sure'].indexOf(o.value) !== -1;
                }});
                var cityInput = document.getElementById('city');
                var typeSelect = document.getElementById('appraisal-type');
                function update() {{
                    var city = (cityInput.value || '').trim().toLowerCase();
                    var opts = desktopOnly.indexOf(city) !== -1 ? desktopOptions : allOptions;
                    var cur = typeSelect.value;
                    typeSelect.innerHTML = '';
                    opts.forEach(function(o) {{
                        var el = document.createElement('option');
                        el.value = o.value; el.textContent = o.text;
                        if (o.value === cur) el.selected = true;
                        typeSelect.appendChild(el);
                    }});
                }}
                if (cityInput && typeSelect) {{
                    cityInput.addEventListener('input', update);
                    cityInput.addEventListener('change', update);
                }}
            }})();
            </script>"""
    write("/contact", page(
        "/contact", "Request an Appraisal | Contact CA-Appraiser.com",
        "Request a California real estate appraisal online. Tell us about your property and the appraisal's purpose and we'll reply with the right report and a firm quote. Serving San Diego & Riverside Counties in person; desktop statewide.",
        "contact appraiser California, request appraisal, appraisal quote, order appraisal online, San Diego appraiser, Riverside appraiser",
        contact_body, active="/contact", schema=contact_schema, og_type="business.business",
        hero=("/images/hero-contact.jpg", "Request a California real estate appraisal",
              "Contact Us", "Free, no-pressure consultation about your appraisal needs", None)))

    # ------------------------------------------------------------------- FAQ
    faqs = [
        ("What is a non-lender (non-mortgage) appraisal?",
         "It's an appraisal ordered for a reason other than getting a loan — settling an estate, dividing property in a divorce, supporting a bankruptcy filing, establishing a date-of-death value, or simply learning a home's worth before buying or selling. These reports are written for people and institutions like the IRS, attorneys, and the courts rather than for an underwriter."),
        ("Do you need to come inside the house?",
         "Not always. Our Desktop and Basic Desktop reports are prepared from public records, MLS data, and photographs without a site visit, which is often perfectly appropriate for estate and tax matters. When a court, the IRS, or a buyer needs to know an appraiser personally inspected the property, the Standard report includes a full interior and exterior inspection."),
        ("Can you appraise a property for a past date?",
         "Yes. A retrospective appraisal estimates value as of a specific prior date — most commonly a date of death for step-up in basis, or a separation date in a divorce. We analyze the comparable sales that were available as of that date, not today's market."),
        ("How much does an appraisal cost?",
         "Basic Desktop reports start at $299, Desktop at $449, Drive-By at $575, and Standard at $625, with 2-4 unit and add-on pricing available. Your exact fee depends on the property and the intended use, and is always quoted in writing before you commit."),
        ("Are your reports USPAP and IRS compliant?",
         "Yes. Every report is prepared in conformance with the Uniform Standards of Professional Appraisal Practice (USPAP). Our date-of-death and estate reports are written to meet IRS requirements for step-up in basis and estate-tax documentation."),
        ("Will the same appraiser handle my report?",
         "Yes. Every assignment is completed by the certified appraiser — never a trainee or support staff. The person who answers your questions is the person who signs your report."),
        ("Do you provide expert witness testimony?",
         "Yes. We prepare litigation-ready reports and provide qualified expert testimony and appraisal review for divorce, probate, bankruptcy, and other contested valuation matters. Testimony and deposition time are billed separately from the appraisal."),
        ("Where do you work?",
         "We provide in-person appraisals throughout San Diego and Riverside Counties and desktop appraisals statewide across California — more than 130 communities in 16 counties. If your city isn't listed on our service-area page, ask; we can almost always help."),
        ("How long does an appraisal take?",
         "Turnaround depends on the report type, the property, and current workload. We give you a realistic timeframe with your quote, and rush delivery is available for an added fee when our schedule allows."),
        ("How do I get started?",
         "Use our <a href=\"/contact\">online request form</a> or email us directly. Tell us the property address and what the appraisal is for, and we'll reply with the right report type and a firm quote."),
    ]
    faq_schema = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": __import__("re").sub("<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    }, indent=4) + '\n</script>'
    faq_items = "\n".join(
        f'            <div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)
    faq_body = f"""            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><span aria-current="page">FAQ</span></li></ul></nav>
            <h1>Frequently Asked Questions</h1>
            <p class="narrow">Answers to the questions we hear most often about non-lender appraisals in California. Don't see yours? <a href="/contact">Ask us directly</a>.</p>
{faq_items}
            <div class="cta-banner"><h2>Still have questions?</h2><p>We're happy to talk through your situation and recommend the right report — at no charge.</p><a href="/contact" class="cta-button">Contact Us</a></div>"""
    write("/faq", page(
        "/faq", "Appraisal FAQ | CA-Appraiser.com",
        "Answers to common questions about California non-lender appraisals: desktop vs. standard reports, retrospective date-of-death values, USPAP/IRS compliance, costs, expert witness, and turnaround.",
        "appraisal FAQ, desktop vs standard appraisal, retrospective appraisal, USPAP IRS appraisal, appraisal questions California",
        faq_body, active="/faq", schema=faq_schema))

    # ---------------------------------------------------------------- REVIEWS
    reviews = [
        ("Brian's date-of-death appraisal made the step-up in basis painless. Our CPA accepted it without a single question and the IRS never blinked.", "K. Mercer, Trustee — La Jolla"),
        ("We needed one neutral value both attorneys could trust in our divorce. The report was thorough, easy to read, and held up in mediation.", "D. &amp; S. Romero — Temecula"),
        ("Fast, professional, and genuinely helpful. He explained exactly which report I needed instead of upselling me.", "P. Nguyen — Carlsbad"),
        ("The bankruptcy appraisal was exactly what our trustee wanted. Clear comps, clear reasoning, no fluff.", "J. Whitfield — Riverside"),
        ("I ordered a pre-listing appraisal before selling my mother's estate home. It priced perfectly and we sold within two weeks.", "A. Delgado — Escondido"),
        ("Detailed, defensible, and delivered when promised. I've used Brian for three estate files now.", "R. Coleman, Estate Attorney — San Diego"),
    ]
    agg = '<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": "CA-Appraiser.com", "url": SITE,
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": str(len(reviews)), "bestRating": "5"},
        "review": [
            {"@type": "Review", "reviewRating": {"@type": "Rating", "ratingValue": "5"},
             "author": {"@type": "Person", "name": __import__("re").sub(" —.*", "", a).replace("&amp;", "&")},
             "reviewBody": __import__("re").sub("<[^>]+>", "", t)}
            for t, a in reviews
        ],
    }, indent=4) + '\n</script>'
    review_cards = "\n".join(
        f'                <div class="review-card"><div class="review-stars">★★★★★</div><p>&ldquo;{t}&rdquo;</p><p class="review-author">{a}</p></div>'
        for t, a in reviews)
    reviews_body = f"""            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><span aria-current="page">Reviews</span></li></ul></nav>
            <h1>Client Reviews</h1>
            <p class="narrow">Estate attorneys, CPAs, trustees, and homeowners across California rely on our reports. Here's what a few of them have said.</p>
            <div class="reviews-grid">
{review_cards}
            </div>
            <div class="cta-banner"><h2>Experience it yourself</h2><p>Join the families and professionals who trust CA-Appraiser.com for clear, defensible valuations.</p><a href="/contact" class="cta-button">Request an Appraisal</a></div>"""
    write("/reviews", page(
        "/reviews", "Client Reviews | CA-Appraiser.com",
        "Reviews from California estate attorneys, CPAs, trustees, and homeowners who rely on CA-Appraiser.com for date-of-death, divorce, bankruptcy, and estate valuations.",
        "appraiser reviews California, real estate appraisal testimonials, date of death appraiser reviews",
        reviews_body, active="/reviews", schema=agg))

    # ------------------------------------------------------------ MARKET REPORTS
    posts = g["BLOG_POSTS"]
    entries = "\n".join(
        f'                <div class="blog-entry"><div class="blog-meta">{p["date"]}</div><h3>{p["title"]}</h3><p>{p["summary"]}</p></div>'
        for p in posts)
    mr_body = f"""            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><span aria-current="page">Market Reports</span></li></ul></nav>
            <h1>California Housing Market Reports</h1>
            <p class="narrow">Plain-English notes on the residential markets we appraise. These observations provide context for valuations; for a current figure on a specific property, <a href="/contact">request an appraisal</a>.</p>
            <div class="blog-list">
{entries}
            </div>"""
    write("/market-reports", page(
        "/market-reports", "California Housing Market Reports | CA-Appraiser.com",
        "Plain-English California residential housing market commentary from a certified appraiser — inventory, pricing, interest rates, and what they mean for property valuations.",
        "California housing market, San Diego market report, Riverside market trends, home prices California, appraisal market analysis",
        mr_body, active="/market-reports"))

    # --------------------------------------------------------------- LEGAL + 404
    terms_body = """            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><span aria-current="page">Terms of Use</span></li></ul></nav>
            <div class="narrow">
            <h1>Terms of Use</h1>
            <p>By using CA-Appraiser.com you agree to these terms. The content of this website is provided for general information about our appraisal services and does not constitute an appraisal, a valuation, financial advice, legal advice, or tax advice. An appraisal exists only in the form of a signed written report prepared under a specific engagement.</p>
            <h3>No guarantee of value</h3>
            <p>Fees, market commentary, and example figures shown on this site are illustrative and subject to change. Nothing here should be relied upon as the value of any particular property. A property's value can only be established through a completed appraisal engagement.</p>
            <h3>Intellectual property</h3>
            <p>All text, design, and images on this site are the property of CA-Appraiser.com unless otherwise noted and may not be reproduced without permission.</p>
            <h3>Limitation of liability</h3>
            <p>This website is provided "as is" without warranties of any kind. We are not liable for any loss arising from use of, or reliance on, information presented here. Appraisal reports are governed by the terms of their individual engagement letters.</p>
            <h3>Contact</h3>
            <p>Questions about these terms? Email <a href="mailto:brian@brianward.com">brian@brianward.com</a>.</p>
            </div>"""
    write("/terms-of-use", page("/terms-of-use", "Terms of Use | CA-Appraiser.com",
        "Terms of use for CA-Appraiser.com.", "terms of use", terms_body))

    privacy_body = """            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><span aria-current="page">Privacy Policy</span></li></ul></nav>
            <div class="narrow">
            <h1>Privacy Policy</h1>
            <p>CA-Appraiser.com respects your privacy. This policy explains what we collect and how we use it.</p>
            <h3>Information we collect</h3>
            <p>When you submit our contact form we collect the information you provide — name, email, optional phone, property address, the purpose of the appraisal, and any message. We collect this solely to respond to your request and provide our services.</p>
            <h3>How we use it</h3>
            <p>Your information is used only to respond to your inquiry, prepare a quote, and deliver appraisal services. We do not sell, rent, or share your personal information with third parties for marketing. Form submissions are delivered to us by email through a secure transactional email provider.</p>
            <h3>Cookies &amp; analytics</h3>
            <p>This site uses minimal cookies necessary for basic functionality. We do not use your data for advertising.</p>
            <h3>Your choices</h3>
            <p>You may request that we delete the information you submitted at any time by emailing <a href="mailto:brian@brianward.com">brian@brianward.com</a>.</p>
            </div>"""
    write("/privacy-policy", page("/privacy-policy", "Privacy Policy | CA-Appraiser.com",
        "Privacy policy for CA-Appraiser.com.", "privacy policy", privacy_body))

    nf_body = """            <div class="narrow" style="text-align:center; padding:40px 0;">
            <h1>Page Not Found</h1>
            <p>Sorry, we couldn't find that page. It may have moved.</p>
            <p><a href="/" class="cta-button">Return Home</a></p>
            <p style="margin-top:20px;">Or jump to <a href="/services-fees">Services &amp; Fees</a>, <a href="/service-area">Service Area</a>, or <a href="/contact">Contact</a>.</p>
            </div>"""
    write("/404", page("/404", "Page Not Found | CA-Appraiser.com",
        "Page not found.", "404", nf_body))

    print("core pages written")
