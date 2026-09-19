#!/usr/bin/env python3
"""Static site generator for capital.partners. Stdlib only.
Reads data/site.json (monetization config) and data/rates.json (auto-updated),
writes the full site to public/."""
import json, os, shutil, html, datetime
from content import GUIDES, TOOLS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
CFG = json.load(open(os.path.join(ROOT, "data/site.json")))
RATES = json.load(open(os.path.join(ROOT, "data/rates.json")))
PRIME = float(RATES["prime"])
TODAY = datetime.date.today().isoformat()
DOMAIN = CFG["domain"].rstrip("/")
YEAR = datetime.date.today().year
MONTH = datetime.date.today().strftime("%B %Y")
PAGES = []  # for sitemap

esc = html.escape
def f2(x): return f"{x:.2f}"
def usd(x): return "${:,.0f}".format(x)

# ---------- finance helpers ----------
def pmt(P, apr, n):
    r = apr / 100 / 12
    return P / n if r == 0 else P * r / (1 - (1 + r) ** -n)

def irr(net, pay, n):
    lo, hi = 0.0, 1.0
    if pay * n <= net: return 0.0
    for _ in range(200):
        m = (lo + hi) / 2
        pv = pay * n if m == 0 else pay * (1 - (1 + m) ** -n) / m
        lo, hi = (m, hi) if pv > net else (lo, m)
    return (lo + hi) / 2

def mca_apr(factor, bdays):
    adv = 10000
    return irr(adv, adv * factor / bdays, bdays) * 252 * 100

TOKENS = {
    "[[PRIME]]": f2(PRIME),
    "[[SBA_T1]]": f2(PRIME + 6.5), "[[SBA_T2]]": f2(PRIME + 6.0),
    "[[SBA_T3]]": f2(PRIME + 4.5), "[[SBA_T4]]": f2(PRIME + 3.0),
    "[[MCA_TABLE]]": "".join(
        f'<tr><td>{fr:.2f}</td><td class="num">{mca_apr(fr,126):.0f}%</td><td class="num">{mca_apr(fr,252):.0f}%</td></tr>'
        for fr in (1.10, 1.20, 1.30, 1.40, 1.50)),
}
def fill(s):
    for k, v in TOKENS.items(): s = s.replace(k, v)
    return s

# ---------- monetization blocks ----------
ADS_ON = bool(CFG.get("adsense_client"))
def ad(slot_name="inline"):
    if not ADS_ON: return ""
    slot = CFG.get("adsense_slot_inline", "")
    if slot:
        return (f'<div class="ad"><span class="adlbl">Advertisement</span><ins class="adsbygoogle" style="display:block" '
                f'data-ad-client="{esc(CFG["adsense_client"])}" data-ad-slot="{esc(slot)}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
                '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>')
    return ""  # Auto ads handle placement when no slot ID is set

def partner_cta(product, headline=None, sub=None):
    p = CFG["partners"].get(product) or {}
    if p.get("url"):
        href, label, rel = p["url"], f"Check your rates with {esc(p['name'])}", ' rel="sponsored noopener" target="_blank"'
    else:
        href, label, rel = "/match/", "Find my best funding option", ""
    return (f'<div class="cta-box"><div><h3>{esc(headline or "See what you qualify for")}</h3>'
            f'<p>{esc(sub or "Answer six questions. Get matched to the funding type that fits your numbers.")}</p></div>'
            f'<a class="btn" href="{esc(href)}"{rel} data-product="{product}">{label}</a></div>')

# ---------- layout ----------
LOGO = ('<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#b8893b"/>'
        '<text x="16" y="21.5" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="14" fill="#0d1b2a">CP</text></svg>')

def head(title, desc, path, schema=None, noindex=False):
    url = DOMAIN + path
    tags = [
        '<!doctype html><html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(desc)}">',
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="{esc(CFG["name"])}">',
        '<meta name="twitter:card" content="summary">',
        '<meta name="theme-color" content="#0d1b2a">',
        '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">',
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;600&display=swap" rel="stylesheet">',
        f'<link rel="stylesheet" href="/assets/style.css?v={TODAY}">',
    ]
    if noindex: tags.append('<meta name="robots" content="noindex">')
    if ADS_ON:
        tags.append(f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={esc(CFG["adsense_client"])}" crossorigin="anonymous"></script>')
    if CFG.get("ga4_id"):
        g = esc(CFG["ga4_id"])
        tags.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script>'
                    f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{g}');</script>")
    for s in (schema or []):
        tags.append(f'<script type="application/ld+json">{json.dumps(s)}</script>')
    pub_cfg = {"partners": CFG["partners"]}
    tags.append(f"<script>window.CP_RATES={json.dumps(RATES)};window.CP_CONFIG={json.dumps(pub_cfg)};</script>")
    tags.append("</head><body>")
    return "".join(tags)

def header():
    return f'''<header class="site-head"><div class="wrap">
<a class="logo" href="/">{LOGO}<span class="wm">Capital<span>.</span>Partners</span></a>
<button class="menu-toggle" aria-expanded="false" aria-label="Menu">Menu</button>
<nav class="nav"><a href="/tools/">Calculators</a><a href="/guides/">Guides</a><a href="/compare/">Compare</a><a href="/loan-payments/">Loan payments</a><a class="btn sm" href="/match/">Get matched</a></nav>
</div></header>
<div class="ticker"><div class="wrap">
<span>WSJ Prime <b>{f2(PRIME)}%</b></span>
<span>SBA 7(a) max, over $350K <b>{f2(PRIME+3)}%</b></span>
<span>SBA 7(a) max, $50K or less <b>{f2(PRIME+6.5)}%</b></span>
<span>Updated <b>{esc(RATES.get("as_of", TODAY))}</b></span>
</div></div>'''

def footer():
    tools = "".join(f'<li><a href="/tools/{t["slug"]}/">{esc(t["short"])}</a></li>' for t in TOOLS[:6])
    guides = "".join(f'<li><a href="/guides/{g["slug"]}/">{esc(g["short"])}</a></li>' for g in GUIDES[:6])
    return f'''<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="/">{LOGO}<span class="wm">Capital<span>.</span>Partners</span></a>
<p style="margin-top:12px">Independent calculators and plain-English guides to help small businesses find and compare funding.</p></div>
<div><h4>Calculators</h4><ul>{tools}</ul></div>
<div><h4>Guides</h4><ul>{guides}</ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About</a></li><li><a href="/advertiser-disclosure/">Advertiser disclosure</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms</a></li><li><a href="/contact/">Contact</a></li></ul></div>
</div>
<div class="fine">&copy; {YEAR} Capital Partners. Capital Partners is an independent publisher, not a lender, broker or investment adviser, and does not make credit decisions. Content is for general information and is not financial, legal or tax advice. Rates and terms are estimates and change often; confirm them with the provider. Some links are affiliate links, and we may be compensated when you click or apply. That does not change our calculators' math. See our <a href="/advertiser-disclosure/">advertiser disclosure</a>.</div>
</div></footer>
<script src="/assets/app.js?v={TODAY}" defer></script></body></html>'''

def write(path, body, title, desc, schema=None, priority="0.7", noindex=False):
    full = head(title, desc, path, schema, noindex) + header() + body + footer()
    dest = os.path.join(OUT, path.strip("/"), "index.html") if path != "/404" else os.path.join(OUT, "404.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w").write(full)
    if not noindex: PAGES.append((path, priority))

def crumbs(*items):
    parts = ['<a href="/">Home</a>'] + [f'<a href="{h}">{esc(n)}</a>' if h else esc(n) for n, h in items]
    return '<div class="crumbs">' + " / ".join(parts) + "</div>"

def crumb_schema(*items):
    lst = [("Home", "/")] + list(items)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + h} for i, (n, h) in enumerate(lst)]}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

# ---------- matcher ----------
def chips(name, opts):
    return '<div class="chips">' + "".join(
        f'<input type="radio" id="{name}-{v}" name="{name}" value="{v}"><label for="{name}-{v}">{esc(l)}</label>' for v, l in opts) + "</div>"

def matcher(heading=True):
    qs = [
        ("amt", "How much do you need?", [("s", "Under $50K"), ("m", "$50K–$250K"), ("l", "$250K–$1M"), ("xl", "$1M+")]),
        ("use", "What is it for?", [("working", "Working capital"), ("equipment", "Equipment"), ("invoices", "Unpaid invoices"), ("growth", "Growth / expansion")]),
        ("tib", "Time in business", [("0", "Under 1 year"), ("1", "1–2 years"), ("2", "2–5 years"), ("3", "5+ years")]),
        ("rev", "Monthly revenue", [("0", "Under $10K"), ("1", "$10K–$50K"), ("2", "$50K–$250K"), ("3", "$250K+")]),
        ("credit", "Personal credit score", [("0", "Under 580"), ("1", "580–659"), ("2", "660–719"), ("3", "720+")]),
        ("speed", "How fast?", [("now", "This week"), ("month", "Within a month"), ("slow", "I can wait for the best rate")]),
    ]
    h = '<h2>Find your best funding option</h2><p class="small muted">Six questions. No email, no credit check.</p>' if heading else ""
    body = "".join(f'<div class="q"><label class="ql">{esc(t)}</label>{chips(n, o)}</div>' for n, t, o in qs)
    return f'<form class="matcher" id="matcher" onsubmit="return false">{h}{body}<div class="results" id="match-results" aria-live="polite"></div></form>'

# ---------- calculators ----------
def fld(id, label, value, hint="", step="any"):
    h = f'<div class="hint">{esc(hint)}</div>' if hint else ""
    return f'<div class="field"><label for="{id}">{esc(label)}</label><input id="{id}" type="number" inputmode="decimal" step="{step}" value="{value}">{h}</div>'

def out(big_id, big_lbl, rows, note="", warn=False):
    dl = "".join(f'<dt>{esc(l)}</dt><dd id="{i}">—</dd>' for i, l in rows)
    w = '<p id="o-warn" class="note"></p>' if warn else ""
    n = f'<p class="note">{note}</p>' if note else ""
    return f'<div class="out" aria-live="polite"><div class="lbl">{esc(big_lbl)}</div><div class="big" id="{big_id}">—</div><dl>{dl}</dl>{w}{n}</div>'

def calc_ui(kind):
    if kind == "loan":
        f = fld("amount","Loan amount ($)",100000)+fld("apr","Interest rate (APR %)",12)+fld("term","Term (months)",36)+fld("fee","Origination fee (%)",2,"Deducted from funding by many online lenders")
        o = out("o-payment","Monthly payment",[("o-interest","Total interest"),("o-fee","Origination fee"),("o-total","Total cost incl. fee"),("o-eff","True APR incl. fee")])
    elif kind == "sba":
        f = fld("amount","Loan amount ($)",250000)+fld("term","Term (years)",10,"10 years typical; up to 25 with real estate")+fld("rate","Interest rate (%)",f2(PRIME+6),"Defaults to the SBA variable-rate maximum for your amount")
        o = out("o-payment","Monthly payment",[("o-interest","Total interest"),("o-total","Total repaid"),("o-max","SBA max rate"),("o-guar","SBA guaranty")],f"Prime rate {f2(PRIME)}% as of {esc(RATES.get('as_of',TODAY))}. Excludes SBA guaranty and lender fees.",warn=True)
    elif kind == "mca":
        f = fld("advance","Amount advanced ($)",50000)+fld("factor","Factor rate",1.35,"e.g. 1.35 means you repay $1.35 per $1")+fld("days","Repayment term (business days)",126,"About 21 business days per month")+fld("fees","Upfront fees ($)",1000)
        o = out("o-apr","Approximate APR",[("o-payback","Total payback"),("o-daily","Daily payment"),("o-cost","Total cost incl. fees")],"APR estimated from the actual daily payment schedule.",warn=True)
    elif kind == "factoring":
        f = fld("invoice","Invoice amount ($)",25000)+fld("advpct","Advance rate (%)",85)+fld("feepct","Factoring fee per 30 days (%)",3)+fld("days","Days until customer pays",45)
        o = out("o-apr","Effective annual cost",[("o-advance","Cash advanced now"),("o-fee","Factoring fee"),("o-rebate","Rebate when customer pays")],"Fee is applied per started 30-day period. Check your contract for tiers and extra fees.")
    elif kind == "dscr":
        f = fld("noi","Annual net operating income ($)",180000,"EBITDA plus owner add-backs, before debt payments")+fld("existing","Existing annual debt payments ($)",24000)+fld("amount","New loan amount ($)",350000)+fld("apr","New loan rate (%)",f2(PRIME+3))+fld("term","New loan term (months)",120)
        o = out("o-dscr","Debt service coverage ratio",[("o-newds","New loan annual payments"),("o-max","Max new loan at 1.25x")],warn=True)
    elif kind == "equipment":
        f = fld("price","Equipment price ($)",80000)+fld("down","Down payment ($)",8000)+fld("apr","Loan rate (%)",9.5)+fld("term","Term (months)",60)+fld("lease","Lease payment per month ($)",1750)+fld("buyout","Lease buyout at end ($)",1)
        o = out("o-payment","Loan monthly payment",[("o-loantotal","Loan: total cost"),("o-leasetotal","Lease: total cost"),("o-diff","Difference")],"Excludes taxes, insurance and depreciation benefits.")
    elif kind == "valuation":
        f = fld("sde","Seller's discretionary earnings ($/yr)",250000,"Profit + owner salary + one-time and personal expenses")+fld("mlo","Low multiple",2.0,"Many main-street businesses sell for roughly 2x–3.5x SDE")+fld("mhi","High multiple",3.2)+fld("debt","Debt assumed by buyer ($)",0)
        o = out("o-mid","Midpoint value",[("o-low","Low estimate"),("o-high","High estimate"),("o-sba","Approx. SBA-financeable (90%)")],"Illustrative only. Industry, growth, owner dependence and customer concentration move multiples a lot.")
    elif kind == "runway":
        f = fld("cash","Cash in bank ($)",600000)+fld("burn","Monthly expenses ($)",90000)+fld("rev","Monthly revenue ($)",30000)+fld("growth","Monthly revenue growth (%)",5)
        o = out("o-months","Runway",[("o-date","Cash out / break-even"),("o-raise","Fundraising deadline")],"Assumes expenses stay flat. Fundraises commonly take 3–6 months.")
    return f'<form class="calc-form calc" data-calc="{kind}"><div class="card">{f}</div>{o}</form>'

# ---------- pages ----------
def page_home():
    tools = "".join(f'<a class="card" href="/tools/{t["slug"]}/"><div class="eyebrow">Calculator</div><h3>{esc(t["short"])}</h3><p class="muted small">{esc(t["blurb"])}</p></a>' for t in TOOLS[:6])
    guides = "".join(f'<a class="card" href="/guides/{g["slug"]}/"><div class="eyebrow">Guide</div><h3>{esc(g["title"])}</h3><p class="muted small">{esc(g["desc"])}</p></a>' for g in GUIDES[:6])
    body = f'''<section class="hero"><div class="wrap hero-grid">
<div><div class="eyebrow">Small business funding, decoded</div>
<h1>Find the right capital partner for your business.</h1>
<p class="lede">Compare SBA loans, lines of credit, equipment financing, factoring and investors. Honest math and no sales calls.</p>
<div class="stats"><div><b>{f2(PRIME)}%</b>WSJ Prime today</div><div><b>{f2(PRIME+3)}%</b>Lowest SBA 7(a) cap</div><div><b>8</b>Free calculators</div></div>
</div>{matcher()}</div></section>
{ad()}
<section class="block"><div class="wrap"><div class="eyebrow">Run the numbers</div><h2 style="margin-top:.2em">Funding calculators</h2>
<div class="grid g3">{tools}</div><p style="margin-top:18px"><a href="/tools/">All calculators →</a></p></div></section>
<section class="block alt"><div class="wrap"><div class="eyebrow">Learn before you sign</div><h2 style="margin-top:.2em">Funding guides</h2>
<div class="grid g3">{guides}</div><p style="margin-top:18px"><a href="/guides/">All guides →</a></p></div></section>
<section class="block"><div class="wrap narrow">
<h2>How we make money</h2><p>Capital Partners is free. We earn from advertising and, when you choose to apply through some links, a referral fee from the provider. Our calculators use the same formulas no matter who pays us, and we will always tell you when a cheaper option exists.</p>
{partner_cta("sba")}</div></section>'''
    schema = [{"@context":"https://schema.org","@type":"WebSite","name":CFG["name"],"url":DOMAIN},
              {"@context":"https://schema.org","@type":"Organization","name":CFG["name"],"url":DOMAIN,"logo":DOMAIN+"/assets/favicon.svg"}]
    write("/", body, "Capital Partners | Compare Small Business Loans, SBA Rates & Funding",
          f"Compare small business funding: SBA 7(a) rates (prime {f2(PRIME)}%), lines of credit, equipment financing and factoring, with free calculators and a 60-second funding matcher.", schema, "1.0")

def page_match():
    body = f'''<section class="article"><div class="wrap narrow">{crumbs(("Funding matcher",None))}
<h1>Business funding matcher</h1><p class="muted">Answer six questions and we rank the funding types that fit your business. No personal details and no credit check.</p>
{matcher(heading=False)}{ad()}
<h2>How the matcher works</h2><p>Lenders weigh time in business, revenue, credit and urgency differently. SBA lenders want history and credit and will make you wait. Asset-based lenders care about the asset. Merchant cash advance funders care about deposits and charge accordingly. The matcher scores each product against those real-world underwriting patterns and shows the cheapest options you are likely to qualify for first.</p>
</div></section>'''
    write("/match/", body, "Business Funding Matcher: Which Loan Fits Your Business?", "Answer six questions to see which small business funding types you're likely to qualify for, ranked by cost.", [crumb_schema(("Funding matcher","/match/"))], "0.9")

def page_tools():
    cards = "".join(f'<a class="card" href="/tools/{t["slug"]}/"><div class="eyebrow">Calculator</div><h3>{esc(t["short"])}</h3><p class="muted small">{esc(t["blurb"])}</p></a>' for t in TOOLS)
    write("/tools/", f'<section class="article"><div class="wrap">{crumbs(("Calculators",None))}<h1>Business funding calculators</h1><p class="muted">Free, no sign-up. Every calculator shows the true cost including fees.</p><div class="grid g3">{cards}</div></div></section>',
          "Free Business Loan & Funding Calculators", "Free business funding calculators: loan payments, SBA 7(a), MCA APR, DSCR, equipment lease vs. loan, invoice factoring, valuation and runway.", [crumb_schema(("Calculators","/tools/"))], "0.9")
    for t in TOOLS:
        g = next(x for x in GUIDES if x["slug"] == t["guide"])
        others = "".join(f'<li><a href="/tools/{o["slug"]}/">{esc(o["title"])}</a></li>' for o in TOOLS if o is not t)
        body = f'''<section class="article"><div class="wrap">{crumbs(("Calculators","/tools/"),(t["short"],None))}
<h1>{esc(t["title"])}</h1><p class="muted" style="max-width:720px">{esc(t["desc"])}</p>
{calc_ui(t["calc"])}
<div class="narrow">{ad()}{partner_cta(t["product"])}
<h2>Learn more</h2><p>Read our guide: <a href="/guides/{g["slug"]}/">{esc(g["title"])}</a>.</p>
<h2>More calculators</h2><ul>{others}</ul></div></div></section>'''
        schema = [crumb_schema(("Calculators","/tools/"),(t["short"],f'/tools/{t["slug"]}/')),
                  {"@context":"https://schema.org","@type":"WebApplication","name":t["title"],"applicationCategory":"FinanceApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"url":f'{DOMAIN}/tools/{t["slug"]}/'}]
        write(f'/tools/{t["slug"]}/', body, f'{t["title"]} ({YEAR})', t["desc"], schema, "0.9")

def page_guides():
    cards = "".join(f'<a class="card" href="/guides/{g["slug"]}/"><div class="eyebrow">Guide</div><h3>{esc(g["title"])}</h3><p class="muted small">{esc(g["desc"])}</p></a>' for g in GUIDES)
    write("/guides/", f'<section class="article"><div class="wrap">{crumbs(("Guides",None))}<h1>Small business funding guides</h1><p class="muted">Plain-English explanations of every major funding type, with the real costs.</p><div class="grid g3">{cards}</div></div></section>',
          "Small Business Funding Guides", "Plain-English guides to SBA loans, lines of credit, equipment financing, invoice factoring, merchant cash advances and startup funding.", [crumb_schema(("Guides","/guides/"))], "0.8")
    for g in GUIDES:
        body_html = fill(g["body"])
        # split roughly in half to place a mid-article ad and CTA
        parts = body_html.split("<h2", 3)
        if len(parts) == 4:
            body_html = parts[0] + "<h2" + parts[1] + "<h2" + parts[2] + ad() + partner_cta(g["product"]) + "<h2" + parts[3]
        import re
        toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>', body_html))
        faqs = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in g["faqs"])
        related = "".join(f'<li><a href="/guides/{o["slug"]}/">{esc(o["title"])}</a></li>' for o in GUIDES if o is not g)[:2000]
        body = f'''<article class="article"><div class="wrap narrow">{crumbs(("Guides","/guides/"),(g["short"],None))}
<h1>{esc(g["title"])}</h1>
<div class="byline">By the Capital Partners editorial team &middot; Updated {MONTH} &middot; Rates refresh automatically</div>
<nav class="toc"><strong>On this page</strong><ol>{toc}<li><a href="#faq">FAQ</a></li></ol></nav>
<div class="content">{body_html}</div>
<div class="callout">Run your own numbers: <a href="{g["tool"][0]}">{esc(g["tool"][1])}</a></div>
<h2 id="faq">Frequently asked questions</h2><div class="faq">{faqs}</div>
{ad()}{partner_cta(g["product"])}
<h2>Related guides</h2><ul>{related}</ul></div></article>'''
        schema = [crumb_schema(("Guides","/guides/"),(g["short"],f'/guides/{g["slug"]}/')), faq_schema(g["faqs"]),
                  {"@context":"https://schema.org","@type":"Article","headline":g["title"],"description":g["desc"],"dateModified":TODAY,"author":{"@type":"Organization","name":CFG["name"]},"publisher":{"@type":"Organization","name":CFG["name"]}}]
        write(f'/guides/{g["slug"]}/', body, f'{g["title"]} ({YEAR})', g["desc"], schema, "0.8")

AMOUNTS = [10000, 25000, 50000, 75000, 100000, 150000, 250000, 500000, 1000000]
def page_payments():
    links = "".join(f'<a class="card" href="/loan-payments/{a}/"><h3>{usd(a)} business loan</h3><p class="muted small">Payments by rate and term</p></a>' for a in AMOUNTS)
    write("/loan-payments/", f'<section class="article"><div class="wrap">{crumbs(("Loan payments",None))}<h1>Business loan payment tables</h1><p class="muted">Monthly payments for common loan sizes across real-world rates and terms.</p><div class="grid g3">{links}</div></div></section>',
          "Business Loan Payment Tables by Amount", "Monthly payment tables for $10,000 to $1,000,000 business loans at current SBA, bank and online lender rates.", [crumb_schema(("Loan payments","/loan-payments/"))], "0.7")
    for a in AMOUNTS:
        spread = 6.5 if a <= 50000 else 6.0 if a <= 250000 else 4.5 if a <= 350000 else 3.0
        sba = PRIME + spread
        rates = sorted({round(sba, 2), 9.0, 12.0, 15.0, 20.0, 30.0})
        terms = [12, 24, 36, 60, 84, 120]
        head_row = "".join(f'<th class="num">{t//12} yr{"s" if t>12 else ""}</th>' for t in terms)
        rows = ""
        for r in rates:
            label = f"{r:.2f}%" + (" (SBA max)" if abs(r - sba) < 0.001 else "")
            rows += f"<tr><td>{label}</td>" + "".join(f'<td class="num">{usd(pmt(a, r, t))}</td>' for t in terms) + "</tr>"
        m60 = pmt(a, sba, 120); total = m60 * 120
        prev = [x for x in AMOUNTS if x < a][-1:] ; nxt = [x for x in AMOUNTS if x > a][:1]
        nav = " · ".join([f'<a href="/loan-payments/{x}/">{usd(x)} loan</a>' for x in prev + nxt])
        fit = ("SBA Express, an online line of credit, or equipment financing" if a <= 50000 else
               "an SBA 7(a), a bank term loan, or an online term loan if speed matters" if a <= 250000 else
               "an SBA 7(a) or bank loan; online lenders rarely go this high unsecured")
        body = f'''<section class="article"><div class="wrap narrow">{crumbs(("Loan payments","/loan-payments/"),(f"{usd(a)} loan",None))}
<h1>{usd(a)} Business Loan Payment Calculator</h1>
<p class="muted">What a {usd(a)} business loan costs per month at today's rates. Prime is {f2(PRIME)}%, so the SBA 7(a) variable-rate maximum for this size is <strong>{f2(sba)}%</strong>.</p>
<div class="card"><p style="margin:0">At the SBA maximum of {f2(sba)}% over 10 years, a {usd(a)} loan costs about <strong>{usd(m60)}/month</strong>, and {usd(total - a)} in total interest.</p></div>
<h2>Monthly payment table</h2>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Rate</th>{head_row}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">Standard amortizing payments, excluding fees. Try exact numbers in the <a href="/tools/business-loan-calculator/">business loan calculator</a>.</p>
{ad()}
<h2>Where to get a {usd(a)} business loan</h2><p>For this amount, the best-value options are usually {fit}. To qualify at good rates, most lenders want to see debt service coverage of 1.25x or better. <a href="/tools/dscr-calculator/">Check whether your cash flow supports {usd(a)}</a>.</p>
{partner_cta("sba" if a > 50000 else "loc")}
<p>{nav}</p></div></section>'''
        write(f"/loan-payments/{a}/", body, f"{usd(a)} Business Loan Payments at Today's Rates ({MONTH})",
              f"Monthly payments on a {usd(a)} business loan at SBA ({f2(sba)}%), bank and online rates over 1 to 10 years.", [crumb_schema(("Loan payments","/loan-payments/"),(f"{usd(a)} loan",f"/loan-payments/{a}/"))], "0.6")

def page_compare():
    rows = [
        ("SBA 7(a)","sba",f"Up to {f2(PRIME+3)}–{f2(PRIME+6.5)}% (variable caps)","30–90 days","Good credit, 2+ yrs","Established businesses wanting the lowest cost"),
        ("Bank line of credit","loc","Prime + margin","2–6 weeks","Good credit, strong financials","Seasonal cash flow"),
        ("Online term loan / LOC","term","Moderate to high","1–7 days","Fair credit, 6–12+ months","Speed with steady revenue"),
        ("Equipment financing","equipment","Low to moderate","2–10 days","Flexible; asset-backed","Buying equipment or vehicles"),
        ("Invoice factoring","factoring","~1–5% per 30 days","1–3 days","Customer credit matters","B2B with slow-paying clients"),
        ("Revenue-based financing","rbf","Cap ~1.1–1.5x","Days to weeks","Recurring revenue","SaaS, e-commerce growth"),
        ("Merchant cash advance","mca","Often 40–150%+ APR","24–48 hours","Very low credit OK","Last resort emergencies"),
        ("Angel / VC equity","equity","Equity dilution","3–6+ months","High-growth potential","Startups chasing scale"),
    ]
    tr = ""
    for n, k, cost, speed, req, best in rows:
        g = {"sba":"sba-7a-loans","loc":"business-line-of-credit","term":"business-line-of-credit","equipment":"equipment-financing","factoring":"invoice-factoring","rbf":"revenue-based-financing","mca":"merchant-cash-advance-vs-loan","equity":"startup-funding-options"}[k]
        p = CFG["partners"].get(k) or {}
        act = f'<a class="btn sm" href="{esc(p["url"])}" rel="sponsored noopener" target="_blank" data-product="{k}">{esc(p["name"])}</a>' if p.get("url") else f'<a href="/guides/{g}/">Guide</a>'
        tr += f"<tr><td><strong>{n}</strong></td><td>{cost}</td><td>{speed}</td><td>{req}</td><td>{best}</td><td>{act}</td></tr>"
    body = f'''<section class="article"><div class="wrap">{crumbs(("Compare",None))}
<h1>Compare small business funding options</h1><p class="muted" style="max-width:720px">Every major funding type side by side: cost, speed and what it takes to qualify. Updated {MONTH}.</p>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Type</th><th>Typical cost</th><th>Speed</th><th>Requirements</th><th>Best for</th><th></th></tr></thead><tbody>{tr}</tbody></table></div>
<div class="narrow">{ad()}<h2>The rule of thumb</h2><p>Take the cheapest money you qualify for, even if it is slower. Use fast, expensive capital only as a short bridge to something cheaper, and only when the return on the money clearly beats its cost.</p>
{partner_cta("sba")}</div></div></section>'''
    write("/compare/", body, f"Compare Business Loans & Funding Options ({YEAR})", "Side-by-side comparison of SBA loans, lines of credit, equipment financing, factoring, revenue-based financing, MCAs and equity.", [crumb_schema(("Compare","/compare/"))], "0.9")

def simple(path, title, desc, inner, pri="0.3", noindex=False):
    write(path, f'<section class="article"><div class="wrap narrow">{crumbs((title,None))}<h1>{esc(title)}</h1><div class="content">{inner}</div></div></section>', f"{title} | Capital Partners", desc, None, pri, noindex)

def page_legal():
    email = esc(CFG["contact_email"])
    simple("/about/", "About Capital Partners", "About Capital Partners, an independent small business funding resource.",
        f"<p>Capital Partners helps small business owners understand and compare funding before they sign anything. We publish free calculators and plain-English guides covering SBA loans, lines of credit, equipment financing, invoice factoring, revenue-based financing and startup capital.</p><h2>Our principles</h2><ul><li><strong>Math first.</strong> Every calculator uses standard amortization and cash-flow formulas and shows true cost including fees.</li><li><strong>Cheapest option first.</strong> We point you toward lower-cost capital even when a more expensive product would pay us more.</li><li><strong>Live data.</strong> Prime-rate-linked figures, including SBA rate caps, update automatically from public data.</li></ul><h2>What we are not</h2><p>We are not a lender, broker or financial adviser, and we do not make credit decisions. Always read the full terms from any provider before accepting an offer.</p><p>Questions: <a href=\"mailto:{email}\">{email}</a></p>")
    simple("/contact/", "Contact", "Contact Capital Partners.", f"<p>Email <a href=\"mailto:{email}\">{email}</a>. We read everything but cannot give individual financial advice or check the status of an application with a provider.</p><p>Lenders and funding providers interested in partnering can reach us at the same address.</p>")
    simple("/advertiser-disclosure/", "Advertiser Disclosure", "How Capital Partners makes money.",
        "<p>Capital Partners is an independent, advertising-supported publisher. We may receive compensation from companies whose products appear on this site, for example when you click a link, submit an application, or are funded. We also display advertising, including ads served by Google.</p><p>Compensation may affect which providers appear and where, but it does not affect our calculators, which use the same formulas for every scenario, or our editorial explanations of how products work and what they cost. We do not include every provider or offer available.</p><p>Links that may earn us compensation are marked with <code>rel=\"sponsored\"</code>.</p>")
    simple("/privacy/", "Privacy Policy", "Capital Partners privacy policy.",
        f"<p>Last updated {MONTH}.</p><h2>What we collect</h2><p>Our calculators and funding matcher run entirely in your browser. We do not receive the numbers you enter. We collect standard analytics such as pages viewed, device type and approximate location through Google Analytics, if enabled.</p><h2>Advertising and cookies</h2><p>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visits. You can opt out of personalized advertising at <a href=\"https://www.google.com/settings/ads\" rel=\"noopener\">Google Ads Settings</a> or <a href=\"https://www.aboutads.info\" rel=\"noopener\">aboutads.info</a>.</p><h2>Affiliate links</h2><p>When you click a partner link, the partner may set cookies to attribute your visit. Their privacy policies govern information you give them.</p><h2>Your rights</h2><p>Depending on where you live, including California, the EU/UK and Canada, you may have rights to access or delete personal data. Contact <a href=\"mailto:{email}\">{email}</a>.</p>")
    simple("/terms/", "Terms of Use", "Capital Partners terms of use.",
        "<p>Content on Capital Partners is for general informational purposes only and is not financial, legal, tax or investment advice. Calculator results are estimates based on the inputs you provide and simplifying assumptions. Rates, terms and program rules change; verify all details with the provider before acting.</p><p>Capital Partners is not a lender or broker and is not responsible for the products, decisions or conduct of third parties linked from this site. The site is provided \"as is\" without warranties. To the fullest extent permitted by law, Capital Partners is not liable for losses arising from use of the site.</p>")
    simple("/404", "Page not found", "Page not found.", '<p>That page does not exist. Try the <a href="/tools/">calculators</a>, the <a href="/guides/">guides</a>, or the <a href="/match/">funding matcher</a>.</p>', noindex=True)

def extras():
    sm = "".join(f"<url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    host = DOMAIN.split("//")[-1]
    open(os.path.join(OUT, "CNAME"), "w").write(host + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    if ADS_ON:
        pub = CFG["adsense_client"].replace("ca-", "")
        open(os.path.join(OUT, "ads.txt"), "w").write(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
    open(os.path.join(OUT, "llms.txt"), "w").write(
        "# Capital Partners\n> Independent small business funding calculators and guides (US).\n\n"
        + "".join(f"- [{t['title']}]({DOMAIN}/tools/{t['slug']}/): {t['desc']}\n" for t in TOOLS)
        + "".join(f"- [{g['title']}]({DOMAIN}/guides/{g['slug']}/): {g['desc']}\n" for g in GUIDES))

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    page_home(); page_match(); page_tools(); page_guides(); page_payments(); page_compare(); page_legal(); extras()
    print(f"Built {len(PAGES)} indexable pages. Prime {PRIME}%. Ads {'ON' if ADS_ON else 'off'}.")

if __name__ == "__main__":
    main()
