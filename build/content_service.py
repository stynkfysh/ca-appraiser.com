# -*- coding: utf-8 -*-
"""Appraisal-type (service) pages for CA-Appraiser.com."""
import json


def build(g):
    page, write = g["page"], g["write"]
    SITE, EMAIL = g["SITE"], g["EMAIL"]

    def service_page(slug, name, hero_img, hero_headline, hero_sub, meta_desc, keywords, body_inner):
        breadcrumb = json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "/services-fees"},
                {"@type": "ListItem", "position": 3, "name": name, "item": SITE + slug},
            ],
        }, indent=4)
        service = json.dumps({
            "@context": "https://schema.org", "@type": "Service",
            "serviceType": name, "name": name + " — CA-Appraiser.com",
            "description": meta_desc, "url": SITE + slug,
            "areaServed": [{"@type": "AdministrativeArea", "name": "San Diego County, CA"},
                           {"@type": "AdministrativeArea", "name": "Riverside County, CA"},
                           {"@type": "State", "name": "California"}],
            "provider": {"@type": "LocalBusiness", "name": "CA-Appraiser.com",
                         "email": EMAIL, "url": SITE, "priceRange": "$299 - $725"},
        }, indent=4)
        schema = ('<script type="application/ld+json">\n' + breadcrumb + '\n</script>\n    '
                  '<script type="application/ld+json">\n' + service + '\n</script>')
        body = f"""            <nav class="breadcrumb" aria-label="Breadcrumb"><ul><li><a href="/">Home</a></li><li><a href="/services-fees">Services</a></li><li><span aria-current="page">{name}</span></li></ul></nav>
            <div class="service-detail-section narrow">
{body_inner}
            </div>
            <div class="services-pricing-section">
                <h3>Pricing for a {name}</h3>
                <p>Most {name.lower()} assignments are handled with our Basic Desktop ($299) or Desktop ($449) report; a Standard report with in-person inspection ($625) is available when the situation calls for it. Your exact fee is quoted before you commit.</p>
                <p><a href="/services-fees">See full pricing &rarr;</a></p>
            </div>
            <div class="cta-banner">
                <h2>Request a {name}</h2>
                <p>Tell us about the property and your timeline. We'll confirm the right report and send a firm quote.</p>
                <a href="/contact" class="cta-button">Request an Appraisal</a>
                <span class="cta-phone">or email <a href="mailto:{EMAIL}">{EMAIL}</a></span>
            </div>"""
        write(slug, page(slug, f"{name} | CA-Appraiser.com", meta_desc, keywords, body,
                         schema=schema, og_type="business.business",
                         hero=(hero_img, hero_headline, hero_headline, hero_sub, ("Request an Appraisal", "/contact"))))

    # 1. Date of Death
    service_page("/date-of-death-appraisal", "Date of Death Appraisal",
        "/images/hero-estate.jpg", "Date of Death Appraisals",
        "Retrospective valuations for step-up in basis, estate tax, and probate",
        "Date of death real estate appraisal in California for step-up in basis, estate tax, and probate. Retrospective valuations dated to the date of passing, prepared to meet IRS requirements.",
        "date of death appraisal California, step up in basis appraisal, retrospective appraisal, estate tax appraisal, probate appraisal",
        """                <h1>Date of Death Real Estate Appraisals in California</h1>
                <p>When someone passes away, the property they owned generally receives a new cost basis equal to its fair market value as of the date of death — the "step-up in basis." Establishing that value correctly can save heirs a significant amount in capital-gains tax when the property is later sold, and the IRS expects it to be supported by a credible, retrospective appraisal.</p>
                <p>A date-of-death appraisal is <strong>retrospective</strong>: it estimates value as of a specific past date, not today. We analyze the comparable sales that were actually available in the market as of the date of passing and document our reasoning so the report withstands review by the IRS, a CPA, or the probate court.</p>
                <h3>When you need one</h3>
                <ul class="reset">
                    <li>Establishing a step-up in basis to minimize future capital-gains tax</li>
                    <li>Filing an estate tax return (Form 706) or supporting a trust</li>
                    <li>Probate administration and equitable distribution among heirs</li>
                    <li>Documenting basis years after the fact, when records are needed retroactively</li>
                </ul>
                <h3>What you receive</h3>
                <p>A USPAP-compliant written report stating the property's fair market value as of the date of death, the comparable sales relied upon, and a clear explanation of the analysis. Most clients choose the Basic Desktop or Desktop report; no interior inspection is required for a retrospective value, though we can perform one when the estate is also being divided.</p>""")

    # 2. Divorce
    service_page("/divorce-appraisal", "Divorce Appraisal",
        "/images/hero-keys.jpg", "Divorce Appraisals",
        "Neutral, defensible property values for equitable division",
        "Divorce real estate appraisal in California. Impartial property valuations for equitable division, with a two-party option so both spouses can rely on one neutral report. Expert testimony available.",
        "divorce appraisal California, marital home appraisal, equitable division appraisal, divorce property valuation, separation date appraisal",
        """                <h1>Divorce Real Estate Appraisals in California</h1>
                <p>Dividing a marital home requires a value both spouses — and both attorneys — can trust. We prepare impartial, well-supported appraisals designed specifically for family-law matters, whether the home will be sold, refinanced, or bought out by one party.</p>
                <p>Because California is a community-property state, the date of valuation matters. We can appraise as of the current date, the date of separation, or another date your attorney specifies, analyzing the comparable sales available as of that date.</p>
                <h3>Built for family law</h3>
                <ul class="reset">
                    <li><strong>Two-party reports:</strong> one neutral appraisal both spouses share, avoiding the cost and conflict of dueling appraisers</li>
                    <li><strong>Retrospective values</strong> as of a separation or other date when required</li>
                    <li><strong>Expert testimony and deposition</strong> support when a value is contested</li>
                    <li>Clear, readable reporting that holds up in mediation and in court</li>
                </ul>
                <p>When both spouses agree to share one report, our two-client option keeps the process efficient and even-handed. When values are disputed, the same report is built to support testimony.</p>""")

    # 3. Bankruptcy
    service_page("/bankruptcy-appraisal", "Bankruptcy Appraisal",
        "/images/hero-documents.jpg", "Bankruptcy Appraisals",
        "Court-ready valuations for Chapter 7, 11, and 13 filings",
        "Bankruptcy real estate appraisal in California for Chapter 7, 11, and 13 filings. Defensible, court-ready property valuations that satisfy the trustee and the bankruptcy court.",
        "bankruptcy appraisal California, Chapter 7 appraisal, Chapter 13 appraisal, bankruptcy property valuation, trustee appraisal",
        """                <h1>Bankruptcy Real Estate Appraisals in California</h1>
                <p>In a bankruptcy filing, the value of real property affects exemptions, the treatment of secured debt, and whether there is equity for the estate. The trustee and the court need a credible, independent appraisal — not an estimate or an automated value.</p>
                <p>We prepare defensible valuations for Chapter 7, 11, and 13 matters, documented clearly enough to satisfy the trustee, debtor's and creditor's counsel, and the bankruptcy court.</p>
                <h3>Common uses</h3>
                <ul class="reset">
                    <li>Establishing equity (or the lack of it) for exemption planning</li>
                    <li>Supporting lien-stripping motions in Chapter 13</li>
                    <li>Valuing property for a Chapter 11 reorganization</li>
                    <li>Responding to a trustee's or creditor's valuation challenge</li>
                </ul>
                <p>We can prepare a retrospective value as of the petition date when required and provide expert testimony if the valuation is contested.</p>""")

    # 4. Estate
    service_page("/estate-appraisal", "Estate Appraisal",
        "/images/hero-estate.jpg", "Estate &amp; Trust Appraisals",
        "Fair market valuations for probate, trusts, and estate planning",
        "Estate and trust real estate appraisal in California for probate, trust administration, estate planning, and equitable distribution. USPAP and IRS compliant.",
        "estate appraisal California, probate appraisal, trust appraisal, estate planning valuation, inheritance appraisal",
        """                <h1>Estate &amp; Trust Real Estate Appraisals in California</h1>
                <p>Settling an estate or administering a trust almost always requires an independent opinion of a property's fair market value. Executors, trustees, attorneys, and CPAs rely on a credible appraisal to value assets fairly, divide them among heirs, and document the estate for tax and court purposes.</p>
                <p>We prepare clear, well-supported valuations for probate, trust funding and administration, estate planning, and equitable distribution. When the value is needed as of a date of death, see our <a href="/date-of-death-appraisal">date-of-death appraisal</a> page for the retrospective approach.</p>
                <h3>Who we work with</h3>
                <ul class="reset">
                    <li>Executors and administrators settling a probate estate</li>
                    <li>Trustees funding, administering, or dividing a trust</li>
                    <li>Estate-planning and probate attorneys</li>
                    <li>CPAs and financial advisors documenting estate assets</li>
                    <li>Heirs seeking a fair, neutral value before dividing property</li>
                </ul>
                <p>Reports are USPAP-compliant and written to be understood by non-appraisers — the people who actually have to act on them.</p>""")

    # 5. Tax
    service_page("/tax-appraisal", "Tax Appraisal",
        "/images/hero-documents.jpg", "Tax Appraisals",
        "Valuations for property tax appeals and IRS compliance",
        "Real estate tax appraisal in California for property tax appeals, assessment disputes, and IRS compliance including step-up in basis and charitable contributions.",
        "tax appraisal California, property tax appeal appraisal, assessment appeal, IRS appraisal, step up in basis",
        """                <h1>Tax-Related Real Estate Appraisals in California</h1>
                <p>Property values drive a wide range of tax questions, and an independent appraisal is often the cleanest way to support your position. We prepare valuations for property-tax assessment appeals, IRS step-up in basis and estate documentation, and other tax matters where a credible, defensible value is required.</p>
                <h3>Common tax uses</h3>
                <ul class="reset">
                    <li><strong>Assessment appeals:</strong> documenting that an assessed value exceeds market value</li>
                    <li><strong>Step-up in basis:</strong> retrospective date-of-death values for capital-gains planning</li>
                    <li><strong>Estate and gift tax:</strong> fair market value to support filings</li>
                    <li><strong>Proposition 19 transfers:</strong> understanding reassessment exposure on inherited property</li>
                </ul>
                <p>Each report is prepared to USPAP standards and written to satisfy an assessor, a CPA, or the IRS. For inherited-property reassessment questions, see our <a href="/prop-19-appraisal">Proposition 19 appraisal</a> page.</p>""")

    # 6. Pre-Purchase
    service_page("/pre-purchase-appraisal", "Pre-Purchase Appraisal",
        "/images/hero-keys.jpg", "Pre-Purchase Appraisals",
        "Know the value before you buy — and negotiate with confidence",
        "Pre-purchase real estate appraisal in California. An independent value before you buy a home, so you can negotiate confidently and avoid overpaying. Available statewide as a desktop report.",
        "pre-purchase appraisal California, appraisal before buying a home, buyer appraisal, independent home value, FSBO appraisal",
        """                <h1>Pre-Purchase Real Estate Appraisals in California</h1>
                <p>Before you commit to one of the largest purchases of your life, it helps to know what the property is actually worth — independent of the listing price or the seller's expectations. A pre-purchase appraisal gives you an objective, third-party value you can use to negotiate and to decide with confidence.</p>
                <h3>When it helps most</h3>
                <ul class="reset">
                    <li>Buying directly from a seller (for-sale-by-owner) without an agent's market analysis</li>
                    <li>Considering an all-cash purchase with no lender appraisal involved</li>
                    <li>Worried about overpaying in a fast-moving or thinly traded market</li>
                    <li>Buying from family and needing a defensible arm's-length value</li>
                </ul>
                <p>Because this is for your own decision-making, a desktop report is usually ideal — fast, affordable, and built on the same comparable-sales analysis a lender appraisal uses.</p>""")

    # 7. Pre-Sale
    service_page("/pre-sale-appraisal", "Pre-Sale Appraisal",
        "/images/hero-home.jpg", "Pre-Sale Appraisals",
        "Set the right asking price before you list",
        "Pre-sale real estate appraisal in California. An independent valuation before you list, so you can price your home accurately and avoid leaving money on the table or sitting on the market.",
        "pre-sale appraisal California, appraisal before selling, listing price appraisal, FSBO appraisal, home value before listing",
        """                <h1>Pre-Sale Real Estate Appraisals in California</h1>
                <p>Pricing a home is the single most important decision in a sale. Price too high and the home lingers; price too low and you leave money behind. A pre-sale appraisal gives you an independent, professional opinion of value — separate from any agent's incentive — so you can list with confidence.</p>
                <h3>Why sellers order one</h3>
                <ul class="reset">
                    <li>Setting an accurate, defensible asking price before listing</li>
                    <li>Selling for-sale-by-owner without an agent's pricing analysis</li>
                    <li>Settling a difference of opinion among co-owners or heirs before a sale</li>
                    <li>Anticipating the buyer's lender appraisal and avoiding surprises</li>
                </ul>
                <p>A desktop report is typically the right fit, delivering a full comparable-sales analysis without the cost of a formal inspection.</p>""")

    # 8. Family transaction
    service_page("/family-transaction-appraisal", "Family Transaction Appraisal",
        "/images/hero-home.jpg", "Family Transaction Appraisals",
        "Arm's-length values for sales and transfers between relatives",
        "Family transaction real estate appraisal in California. Fair market value for sales and transfers between relatives, documenting an arm's-length price for the IRS and for family fairness.",
        "family transaction appraisal California, family sale appraisal, gift of equity appraisal, intra-family transfer, fair market value relatives",
        """                <h1>Family Transaction Real Estate Appraisals in California</h1>
                <p>Selling or transferring property between family members raises a fairness question and a tax question at the same time. The IRS expects intra-family transfers to reflect fair market value, and an independent appraisal documents an arm's-length price that protects everyone involved.</p>
                <h3>Common situations</h3>
                <ul class="reset">
                    <li>A parent selling or gifting a home to a child (or the reverse)</li>
                    <li>Buying out a sibling's or co-owner's share of an inherited property</li>
                    <li>Documenting a "gift of equity" for a discounted family sale</li>
                    <li>Transferring property into or out of a family trust or LLC</li>
                </ul>
                <p>For inherited California property, a transfer may also trigger reassessment — see our <a href="/prop-19-appraisal">Proposition 19 appraisal</a> page. We provide a neutral, well-documented value so the transaction is fair and defensible.</p>""")

    # 9. Insurance
    service_page("/insurance-appraisal", "Insurance Appraisal",
        "/images/hero-documents.jpg", "Insurance Dispute Appraisals",
        "Independent valuations for insurance claim disputes",
        "Insurance dispute real estate appraisal in California. Independent property valuations to support or resolve insurance claim disagreements with credible, well-documented analysis.",
        "insurance appraisal California, insurance dispute appraisal, claim valuation, property loss appraisal, insurance claim value",
        """                <h1>Insurance Dispute Real Estate Appraisals in California</h1>
                <p>When a property owner and an insurer disagree about value, an independent appraisal can provide the objective analysis needed to support a claim or move toward resolution. We prepare clear, well-documented valuations for insurance-related disputes.</p>
                <h3>How an appraisal helps</h3>
                <ul class="reset">
                    <li>Documenting market value to support or challenge a claim position</li>
                    <li>Establishing pre-loss value as of a specific date</li>
                    <li>Providing a neutral third-party analysis in a contested matter</li>
                    <li>Supporting expert testimony where the dispute proceeds to litigation</li>
                </ul>
                <p>Note that we appraise real-property market value; we do not adjust claims or estimate construction-replacement cost. We'll tell you up front whether an appraisal is the right tool for your situation.</p>""")

    # 10. Bonds
    service_page("/bonds-appraisal", "Bonds Appraisal",
        "/images/hero-documents.jpg", "Bond Appraisals",
        "Property valuations for bail and surety bond purposes",
        "Bond real estate appraisal in California. Property valuations to support bail and surety bonds, documenting equity for the bond agent or the court — often on a fast timeline.",
        "bond appraisal California, bail bond appraisal, surety bond appraisal, property equity appraisal, bail property bond",
        """                <h1>Bond Real Estate Appraisals in California</h1>
                <p>When real property is pledged to secure a bail or surety bond, the bond agent or the court needs to know how much equity the property holds. We provide credible, well-supported valuations for bond purposes, often on an expedited timeline.</p>
                <h3>What's involved</h3>
                <ul class="reset">
                    <li>Establishing current market value and available equity</li>
                    <li>Documenting value clearly enough for a bond agent or the court</li>
                    <li>Fast turnaround when a bond is time-sensitive (rush service available)</li>
                </ul>
                <p>A desktop report is usually sufficient and the quickest path; a full inspection is available when required. Tell us your deadline and we'll confirm what's achievable.</p>""")

    # 11. Prop 19
    service_page("/prop-19-appraisal", "Proposition 19 Appraisal",
        "/images/hero-estate.jpg", "Proposition 19 Transfer Appraisals",
        "Understand reassessment exposure on inherited California property",
        "Proposition 19 real estate appraisal in California. Fair market valuations to help families understand property tax reassessment exposure when inherited homes transfer between parents and children.",
        "Prop 19 appraisal California, Proposition 19 appraisal, parent child transfer appraisal, inherited property reassessment, Prop 19 fair market value",
        """                <h1>Proposition 19 Transfer Appraisals in California</h1>
                <p>California's Proposition 19 changed how inherited property is taxed. When a home transfers from parent to child (or grandparent to grandchild), the property is generally reassessed to current market value unless the child moves in as a primary residence — and even then, only a limited amount of the prior assessed value is protected. The difference between the old assessed value and today's market value can mean a substantial change in property taxes.</p>
                <p>A current fair-market-value appraisal helps families understand their reassessment exposure <strong>before</strong> making decisions about keeping, transferring, or selling an inherited property.</p>
                <h3>When it helps</h3>
                <ul class="reset">
                    <li>Planning an inheritance and estimating the future property-tax impact</li>
                    <li>Deciding whether a child will occupy the home to preserve part of the base-year value</li>
                    <li>Documenting market value at the time of transfer</li>
                    <li>Weighing whether to keep or sell an inherited property</li>
                </ul>
                <p>We provide the market-value analysis; your CPA or attorney applies the specific Prop 19 calculations to your situation. This is an area where a clear, defensible appraisal pays for itself.</p>""")

    # 12. Expert witness
    service_page("/expert-witness", "Expert Witness Appraisal",
        "/images/hero-documents.jpg", "Expert Witness &amp; Litigation Support",
        "Qualified testimony and litigation-ready valuation reports",
        "Real estate expert witness and litigation support in California. Qualified appraisal testimony, appraisal review, and court-ready valuation reports for divorce, probate, and bankruptcy matters.",
        "expert witness appraiser California, real estate litigation support, appraisal review, court testimony appraiser, deposition appraisal",
        """                <h1>Expert Witness &amp; Litigation Support in California</h1>
                <p>When a property's value is contested in court, the quality of the appraisal — and the credibility of the appraiser — matters enormously. With 22 years of experience and more than 7,000 appraisals, we provide litigation-ready reports and qualified expert testimony for matters where value is in dispute.</p>
                <h3>Litigation services</h3>
                <ul class="reset">
                    <li><strong>Expert testimony</strong> at deposition, trial, arbitration, or mediation</li>
                    <li><strong>Appraisal review</strong> — analyzing an opposing appraiser's report for errors or unsupported conclusions</li>
                    <li><strong>Retrospective valuations</strong> as of a separation, petition, or other relevant date</li>
                    <li>Clear, defensible reports built to withstand cross-examination</li>
                </ul>
                <p>We support divorce, probate and estate, bankruptcy, partnership-dissolution, and other contested valuation matters. Appraisal fees are quoted per assignment; testimony, deposition, and review time are billed separately at an hourly rate. <a href="/contact">Contact us</a> to discuss your case.</p>""")

    # 13. PMI removal
    service_page("/pmi-removal", "PMI Removal Appraisal",
        "/images/hero-home.jpg", "PMI Removal Appraisals",
        "Document your home's value to drop private mortgage insurance",
        "PMI removal real estate appraisal in California. Document your home's current value to cancel private mortgage insurance once you've built sufficient equity.",
        "PMI removal appraisal California, cancel PMI appraisal, private mortgage insurance removal, home equity appraisal",
        """                <h1>PMI Removal Appraisals in California</h1>
                <p>If your home has appreciated or you've paid down your loan, you may be able to cancel private mortgage insurance (PMI) — often saving hundreds of dollars a month. Most lenders require a current appraisal to confirm you've reached the necessary equity threshold (commonly around 20% to 25%).</p>
                <h3>How it works</h3>
                <ul class="reset">
                    <li>Confirm your lender's PMI-cancellation requirements and the value or equity needed</li>
                    <li>We prepare a current market-value appraisal of your home</li>
                    <li>You submit the report to your lender to request cancellation</li>
                </ul>
                <p>Check whether your lender requires a specific report type or an interior inspection before ordering; we'll match the report to their requirement. A modest appraisal fee can unlock substantial monthly savings.</p>""")

    print("service pages written")
