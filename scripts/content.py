# Guide content. Tokens like [[PRIME]], [[SBA_MAX_SMALL]] are filled at build time from data/rates.json.

GUIDES = [
{
"slug": "sba-7a-loans",
"title": "SBA 7(a) Loans: Rates, Limits and How to Qualify",
"short": "SBA 7(a) loans explained",
"desc": "Current SBA 7(a) maximum rates, loan limits, guaranty percentages, eligibility and the documents lenders ask for.",
"tool": ("/tools/sba-loan-calculator/", "SBA loan calculator"),
"product": "sba",
"body": """
<p>The SBA 7(a) program is the cheapest widely available debt for established small businesses in the United States. The Small Business Administration does not lend the money. It guarantees part of a loan made by a bank or approved lender. That guarantee lets lenders approve borrowers they would otherwise turn down, and the SBA caps how much they can charge.</p>

<h2 id="rates">Maximum 7(a) interest rates today</h2>
<p>7(a) rates are pegged to the WSJ Prime Rate, which is currently <strong>[[PRIME]]%</strong>. For variable-rate loans the SBA sets these maximum spreads over the base rate:</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Loan amount</th><th class="num">Max spread</th><th class="num">Max rate today</th></tr></thead>
<tbody>
<tr><td>$50,000 or less</td><td class="num">Prime + 6.5%</td><td class="num">[[SBA_T1]]%</td></tr>
<tr><td>$50,001 to $250,000</td><td class="num">Prime + 6.0%</td><td class="num">[[SBA_T2]]%</td></tr>
<tr><td>$250,001 to $350,000</td><td class="num">Prime + 4.5%</td><td class="num">[[SBA_T3]]%</td></tr>
<tr><td>Over $350,000</td><td class="num">Prime + 3.0%</td><td class="num">[[SBA_T4]]%</td></tr>
</tbody></table></div>
<p class="small muted">Rates update automatically when the prime rate changes. Fixed-rate maximums are published separately by the SBA and run slightly higher. Upfront guaranty fees and packaging fees are extra.</p>

<h2 id="limits">Loan limits, terms and guaranty</h2>
<ul>
<li><strong>Maximum loan:</strong> $5 million for a standard 7(a). SBA Express caps at $500,000.</li>
<li><strong>Terms:</strong> up to 10 years for working capital and equipment, up to 25 years when real estate is financed.</li>
<li><strong>Guaranty:</strong> 85% on loans up to $150,000 and 75% above that (50% for SBA Express).</li>
</ul>
<p>The guaranty protects the lender, not you. If the business defaults, you are still personally liable. Anyone owning 20% or more must sign a personal guarantee.</p>

<h2 id="qualify">Who qualifies</h2>
<p>You must be a for-profit business operating in the US, meet SBA size standards, show you can repay from cash flow, and have used other reasonable financing sources first. In practice, lenders look for:</p>
<ul>
<li><strong>Time in business:</strong> usually 2+ years. Startups can qualify, but expect more scrutiny and a larger equity injection.</li>
<li><strong>Credit:</strong> personal FICO in the high 600s or better for most lenders. The SBA's own screening score (FICO SBSS) matters for smaller loans.</li>
<li><strong>Cash flow:</strong> a debt service coverage ratio of about 1.25x or higher. <a href="/tools/dscr-calculator/">Check yours here</a>.</li>
<li><strong>Clean history:</strong> no recent defaults on government-backed debt.</li>
</ul>

<h2 id="docs">Documents to prepare</h2>
<ol>
<li>Business and personal tax returns (usually 3 years)</li>
<li>Year-to-date profit and loss statement and balance sheet</li>
<li>Business debt schedule</li>
<li>SBA Form 1919 (borrower information)</li>
<li>Personal financial statement (SBA Form 413)</li>
<li>Business plan and projections if the business is new or the loan funds an acquisition</li>
</ol>

<h2 id="speed">How long it takes</h2>
<p>Expect 30 to 90 days from application to funding. Preferred Lenders (PLP) can approve in-house and move faster. If you need money this week, a 7(a) is the wrong tool. Use a line of credit as a bridge and refinance into SBA later.</p>

<h2 id="verdict">Bottom line</h2>
<p>If you have two years of history, decent credit and positive cash flow, start with SBA. The rate gap between a 7(a) and an online term loan can be 10 or more percentage points, which on a $250,000 loan is tens of thousands of dollars over the term.</p>
""",
"faqs": [
("Can I use an SBA 7(a) loan to buy a business?", "Yes. Business acquisitions are one of the most common uses. Lenders typically require a 10% equity injection and will analyze the target's historical cash flow."),
("Is the SBA rate fixed or variable?", "Either. Most 7(a) loans are variable and move with the prime rate. Fixed options exist but carry higher maximum spreads."),
("Do I need collateral?", "Lenders must take available collateral on loans over $50,000, but the SBA will not decline a loan solely because collateral is short."),
]
},
{
"slug": "business-loan-bad-credit",
"title": "Business Loans With Bad Credit: What Actually Works",
"short": "Bad-credit business funding",
"desc": "Which funding options accept low credit scores, what they cost, and how to avoid the debt traps aimed at struggling businesses.",
"tool": ("/tools/business-loan-calculator/", "Business loan calculator"),
"product": "term",
"body": """
<p>A personal credit score under roughly 620 closes the door on banks and most SBA lenders. It does not close the door on funding. It changes what you pay and which products make sense. Revenue matters more than credit for most alternative lenders.</p>

<h2 id="options">Options ranked by cost</h2>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Option</th><th>Typical minimum credit</th><th>Relative cost</th><th>Best for</th></tr></thead>
<tbody>
<tr><td>Equipment financing</td><td>~550+</td><td>Low to moderate</td><td>Buying machinery, vehicles, tech</td></tr>
<tr><td>Invoice factoring</td><td>Your customers' credit matters more</td><td>Moderate</td><td>B2B firms with slow-paying invoices</td></tr>
<tr><td>SBA Microloan (via nonprofits)</td><td>Flexible</td><td>Low</td><td>Loans up to $50,000</td></tr>
<tr><td>Online term loan or line of credit</td><td>~580 to 625+</td><td>Moderate to high</td><td>Working capital with steady revenue</td></tr>
<tr><td>Revenue-based financing</td><td>Flexible</td><td>High</td><td>Online businesses with recurring revenue</td></tr>
<tr><td>Merchant cash advance</td><td>~500+</td><td>Very high</td><td>True emergencies only</td></tr>
</tbody></table></div>

<h2 id="why">Why collateral-backed options win</h2>
<p>Equipment loans and factoring work because the lender's risk sits in an asset or a receivable, not in your credit file. If you need capital for something that has resale value, finance that asset directly rather than taking unsecured cash.</p>

<h2 id="traps">The traps</h2>
<ul>
<li><strong>Factor rates disguised as interest.</strong> A 1.35 factor rate over six months is not 35% a year. It is often above 100% APR. <a href="/tools/mca-apr-calculator/">Convert it here</a>.</li>
<li><strong>Stacking.</strong> Taking a second advance to cover the first one's daily payments is how businesses fail. Some contracts prohibit it and can trigger default.</li>
<li><strong>Confessions of judgment.</strong> Read the contract. Some funders ask you to pre-agree to a court judgment if you miss payments.</li>
<li><strong>Upfront "guarantee" fees.</strong> Legitimate lenders deduct fees from funding. They do not ask you to wire money first.</li>
</ul>

<h2 id="improve">Improve your odds in 60 to 90 days</h2>
<ol>
<li>Separate business and personal banking so lenders can see clean revenue.</li>
<li>Keep average daily balances up and avoid overdrafts. Lenders read your last 3 to 6 bank statements line by line.</li>
<li>Pay down revolving balances to under 30% utilization.</li>
<li>Open trade lines that report to business credit bureaus (Dun &amp; Bradstreet, Experian Business, Equifax Business).</li>
<li>Dispute errors on your personal report through the bureaus.</li>
</ol>

<h2 id="verdict">Bottom line</h2>
<p>With bad credit and strong revenue, you can get funded. Pick the option tied to an asset or invoice if you can, borrow the smallest amount that solves the problem, and refinance into cheaper debt once your profile improves.</p>
""",
"faqs": [
("What is the lowest credit score for a business loan?", "Some merchant cash advance providers go as low as 500, and factoring companies focus on your customers' credit. Term loans typically start around 580 to 625."),
("Will applying hurt my credit?", "Many online lenders prequalify with a soft pull. A hard inquiry usually happens only when you accept an offer."),
]
},
{
"slug": "merchant-cash-advance-vs-loan",
"title": "Merchant Cash Advance vs. Business Loan: The Real Cost",
"short": "MCA vs. loan",
"desc": "How merchant cash advances work, how to convert a factor rate to APR, and when an MCA is ever the right call.",
"tool": ("/tools/mca-apr-calculator/", "MCA APR calculator"),
"product": "loc",
"body": """
<p>A merchant cash advance is not legally a loan. It is a purchase of your future receivables at a discount. That structure is why MCAs escape many lending regulations, why they approve almost anyone with card or bank deposits, and why they are so expensive.</p>

<h2 id="how">How an MCA works</h2>
<p>The funder gives you a lump sum, say $50,000. You agree to repay a fixed amount set by a <strong>factor rate</strong>, say 1.30, so you owe $65,000. Repayment comes out daily or weekly, either as a percentage of card sales (a holdback) or a fixed ACH debit.</p>

<h2 id="apr">Factor rate to APR</h2>
<p>Because you repay fast and the cost is fixed, the effective annual rate is much higher than the factor rate suggests:</p>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Factor rate</th><th class="num">Repaid over 6 months</th><th class="num">Repaid over 12 months</th></tr></thead>
<tbody>[[MCA_TABLE]]</tbody></table></div>
<p class="small muted">Approximate APR, assuming equal payments every business day, $0 extra fees. Calculated from the actual cash-flow schedule.</p>

<h2 id="compare">Side by side</h2>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th></th><th>Merchant cash advance</th><th>Online term loan / LOC</th><th>SBA 7(a)</th></tr></thead>
<tbody>
<tr><td>Speed</td><td>24 to 48 hours</td><td>1 to 7 days</td><td>30 to 90 days</td></tr>
<tr><td>Credit needed</td><td>Very low</td><td>Fair</td><td>Good</td></tr>
<tr><td>Cost</td><td>Often 40% to 150%+ APR</td><td>Often 10% to 50% APR</td><td>Capped near prime + 3% to 6.5%</td></tr>
<tr><td>Payments</td><td>Daily or weekly</td><td>Weekly or monthly</td><td>Monthly</td></tr>
<tr><td>Early payoff savings</td><td>Usually none</td><td>Often yes</td><td>Yes (prepayment fee may apply in early years on long terms)</td></tr>
</tbody></table></div>

<h2 id="when">When an MCA makes sense</h2>
<p>Rarely, and only when the math works: a short-term, high-margin opportunity (inventory you will sell within weeks at a strong markup) where the return clearly exceeds the cost, and you have been declined for cheaper options. Using an MCA to cover payroll shortfalls or losses usually makes the underlying problem worse.</p>

<h2 id="exit">Already in an MCA?</h2>
<ul>
<li>Ask for an early-payoff discount in writing. Some funders offer one.</li>
<li>Refinance into a term loan or line of credit once you have 6+ months of clean statements.</li>
<li>Do not stack a second advance. It compounds the daily drain.</li>
</ul>
""",
"faqs": [
("Is a factor rate the same as an interest rate?", "No. A factor rate is a flat multiplier on the amount advanced. Because repayment happens over a short period, the equivalent APR is far higher."),
("Can an MCA hurt my credit?", "Most MCA funders do not report to credit bureaus, but default can lead to collections, lawsuits, or frozen bank accounts depending on the contract."),
]
},
{
"slug": "equipment-financing",
"title": "Equipment Financing: Loans vs. Leases and What You'll Pay",
"short": "Equipment financing",
"desc": "How equipment loans and leases work, typical terms, and how to decide between buying and leasing.",
"tool": ("/tools/equipment-financing-calculator/", "Equipment loan vs. lease calculator"),
"product": "equipment",
"body": """
<p>Equipment financing is one of the easiest types of business credit to get because the equipment secures the debt. If you stop paying, the lender takes the asset back. That lowers risk, which means lower rates and looser credit requirements than unsecured loans.</p>

<h2 id="types">Loan vs. lease</h2>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th></th><th>Equipment loan</th><th>$1 buyout lease</th><th>Fair market value lease</th></tr></thead>
<tbody>
<tr><td>Ownership</td><td>You own it from day one</td><td>You own it at the end for $1</td><td>Return, renew, or buy at market value</td></tr>
<tr><td>Down payment</td><td>Often 0% to 20%</td><td>Often first and last payment</td><td>Often first payment</td></tr>
<tr><td>Monthly cost</td><td>Moderate</td><td>Highest</td><td>Lowest</td></tr>
<tr><td>Best for</td><td>Long-life assets</td><td>Long-life assets, cash-light</td><td>Tech that goes obsolete fast</td></tr>
</tbody></table></div>

<h2 id="terms">Typical terms</h2>
<ul>
<li>Financing up to 100% of the equipment cost, sometimes including soft costs like installation and shipping.</li>
<li>Terms usually match useful life: 2 to 7 years is common; heavy equipment can go longer.</li>
<li>Rates vary widely by credit, time in business and asset type. Strong borrowers can see single-digit rates. Startups and weaker credit profiles pay considerably more.</li>
</ul>

<h2 id="tax">Tax angle</h2>
<p>Section 179 and bonus depreciation can let businesses deduct much or all of qualifying equipment costs in the year the asset is placed in service, even if it was financed. Limits change, so confirm the current year's thresholds with your accountant before you sign.</p>

<h2 id="decide">How to decide</h2>
<ol>
<li>Will the equipment still be useful when the financing ends? If yes, buy. If it will be obsolete, consider an FMV lease.</li>
<li>Compare total cost of ownership, not monthly payment. <a href="/tools/equipment-financing-calculator/">Run both scenarios</a>.</li>
<li>Check for prepayment penalties and end-of-lease return conditions.</li>
</ol>
""",
"faqs": [
("Can a startup get equipment financing?", "Yes. Because the equipment is collateral, many lenders fund businesses under two years old, typically at higher rates or with a larger down payment."),
("Can I finance used equipment?", "Yes, though lenders may cap the term based on the asset's age and remaining useful life."),
]
},
{
"slug": "invoice-factoring",
"title": "Invoice Factoring: How It Works and What It Costs",
"short": "Invoice factoring",
"desc": "Factoring vs. invoice financing, advance rates, fee structures and the effective annual cost of turning invoices into cash.",
"tool": ("/tools/invoice-factoring-calculator/", "Invoice factoring calculator"),
"product": "factoring",
"body": """
<p>If your customers pay on 30, 60 or 90-day terms, you are effectively lending them money. Invoice factoring sells those unpaid invoices to a factoring company in exchange for cash now.</p>

<h2 id="how">How factoring works</h2>
<ol>
<li>You invoice your customer as usual.</li>
<li>The factor advances a percentage of the invoice, commonly 70% to 95%, often within 1 to 2 business days.</li>
<li>Your customer pays the factor directly.</li>
<li>The factor sends you the remainder (the rebate) minus its fee.</li>
</ol>

<h2 id="cost">Fees</h2>
<p>Factoring fees are often quoted per 30 days, commonly in the 1% to 5% range of the invoice value. Some factors charge tiered fees that increase the longer an invoice stays unpaid. A "2% fee" on a 60-day invoice is 4%, and measured against the cash you actually received, the annualized cost is much higher. <a href="/tools/invoice-factoring-calculator/">Calculate yours</a>.</p>

<h2 id="types">Recourse vs. non-recourse</h2>
<ul>
<li><strong>Recourse:</strong> if the customer does not pay, you buy the invoice back. Cheaper.</li>
<li><strong>Non-recourse:</strong> the factor absorbs the loss if the customer becomes insolvent. Costs more, and usually does not cover disputes.</li>
</ul>

<h2 id="vs">Factoring vs. invoice financing</h2>
<p>With invoice financing, you borrow against invoices but keep collecting from customers yourself. It is more discreet, since customers are not told, but requires stronger financials.</p>

<h2 id="fit">Who it fits</h2>
<p>Staffing agencies, trucking companies, manufacturers, wholesalers and B2B service firms with creditworthy customers and slow payment cycles. It does not work for consumer-facing businesses that get paid at the point of sale.</p>

<h2 id="watch">Watch for</h2>
<ul>
<li>Minimum monthly volume commitments and long contracts with termination fees</li>
<li>Extra charges: application, due diligence, ACH/wire, and lockbox fees</li>
<li>Requirements to factor all invoices, not just the ones you choose ("spot factoring" avoids this)</li>
</ul>
""",
"faqs": [
("Does my credit score matter for factoring?", "Less than for a loan. The factor cares most about whether your customers pay reliably."),
("Will my customers know?", "With traditional factoring, yes. Payment instructions change to the factor. Invoice financing keeps it confidential."),
]
},
{
"slug": "business-line-of-credit",
"title": "Business Line of Credit: The Most Flexible Capital You Can Get",
"short": "Business lines of credit",
"desc": "How business lines of credit work, requirements, costs, and how they compare with term loans.",
"tool": ("/tools/business-loan-calculator/", "Business loan calculator"),
"product": "loc",
"body": """
<p>A business line of credit gives you a borrowing limit you can draw against as needed. You pay interest only on what you use, and as you repay, the credit becomes available again. For uneven cash flow, it is usually the best tool available.</p>

<h2 id="vs">Line of credit vs. term loan</h2>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th></th><th>Line of credit</th><th>Term loan</th></tr></thead>
<tbody>
<tr><td>Funds</td><td>Draw as needed</td><td>Lump sum upfront</td></tr>
<tr><td>Interest</td><td>Only on the balance drawn</td><td>On the full amount from day one</td></tr>
<tr><td>Best for</td><td>Payroll gaps, inventory, seasonality</td><td>One-time investment: expansion, acquisition</td></tr>
<tr><td>Typical sizes</td><td>$10,000 to $250,000 online; more from banks</td><td>$25,000 to $5M+</td></tr>
</tbody></table></div>

<h2 id="requirements">Typical requirements</h2>
<ul>
<li><strong>Banks:</strong> 2+ years in business, good credit, strong financials, sometimes collateral. Lowest rates.</li>
<li><strong>Online lenders:</strong> often 6 to 12 months in business, a minimum monthly revenue threshold, and fair credit. Faster, pricier.</li>
</ul>

<h2 id="costs">What it costs</h2>
<p>Bank lines are usually priced as prime plus a margin. With prime at [[PRIME]]%, well-qualified borrowers can see rates in the high single digits to low teens. Online lines range much higher. Watch for draw fees, maintenance fees and short repayment windows (some online lines require each draw to be repaid over 6 to 12 months, which behaves more like a series of short loans).</p>

<h2 id="use">Use it well</h2>
<ol>
<li>Open the line before you need it. Approval is easiest when your numbers look good.</li>
<li>Draw for short-term needs that pay themselves back: inventory before peak season, bridging receivables.</li>
<li>Do not fund long-term losses with a revolving line.</li>
</ol>
""",
"faqs": [
("Secured or unsecured?", "Both exist. Secured lines are backed by receivables, inventory or real estate and cost less. Unsecured lines usually require a personal guarantee."),
("Does an unused line cost anything?", "Some lenders charge an annual or maintenance fee even if you never draw. Ask before signing."),
]
},
{
"slug": "revenue-based-financing",
"title": "Revenue-Based Financing: Growth Capital Without Giving Up Equity",
"short": "Revenue-based financing",
"desc": "How revenue-based financing works for SaaS and e-commerce, typical caps, and how it compares with venture capital and loans.",
"tool": ("/tools/startup-runway-calculator/", "Runway calculator"),
"product": "rbf",
"body": """
<p>Revenue-based financing (RBF) gives you capital in exchange for a fixed percentage of future revenue until a set total, the cap, is repaid. There is no equity dilution and no fixed monthly payment. When revenue dips, payments shrink.</p>

<h2 id="how">The mechanics</h2>
<ul>
<li><strong>Advance:</strong> often sized as a multiple of monthly recurring revenue or a share of annual revenue.</li>
<li><strong>Repayment cap:</strong> commonly 1.1x to 1.5x of the amount advanced, though terms vary.</li>
<li><strong>Revenue share:</strong> a percentage of monthly revenue until the cap is hit.</li>
</ul>

<h2 id="example">Example</h2>
<p>You receive $200,000 with a 1.2x cap, so you owe $240,000 total, repaid at 8% of monthly revenue. At $150,000 monthly revenue you pay $12,000 a month and finish in 20 months. If revenue grows, you finish sooner, and the effective annual rate rises because the same cost is compressed into less time.</p>

<h2 id="fit">Who it fits</h2>
<ul>
<li>SaaS with predictable MRR and healthy gross margins</li>
<li>E-commerce brands financing inventory or ad spend with a proven return on ad spend</li>
<li>Founders who want to delay or avoid an equity round</li>
</ul>

<h2 id="vs">RBF vs. venture capital vs. bank debt</h2>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th></th><th>RBF</th><th>Venture capital</th><th>Bank loan</th></tr></thead>
<tbody>
<tr><td>Dilution</td><td>None</td><td>Yes</td><td>None</td></tr>
<tr><td>Personal guarantee</td><td>Often not required</td><td>No</td><td>Usually</td></tr>
<tr><td>Speed</td><td>Days to weeks</td><td>Months</td><td>Weeks to months</td></tr>
<tr><td>Cost</td><td>Moderate to high</td><td>Highest if you succeed</td><td>Lowest</td></tr>
</tbody></table></div>

<h2 id="verdict">Bottom line</h2>
<p>RBF is excellent when each dollar deployed returns more than it costs within the repayment window, like ad spend with known payback. It is a poor fit for pre-revenue companies or thin-margin businesses, where the revenue share can starve operations.</p>
""",
"faqs": [
("Is revenue-based financing debt?", "It is usually treated as debt or a receivables purchase depending on structure. It does not give the investor ownership."),
("What revenue do I need?", "Many providers look for at least several months of consistent revenue history and connect directly to your payment, banking and accounting data to underwrite."),
]
},
{
"slug": "startup-funding-options",
"title": "Startup Funding Options: From Bootstrapping to Venture Capital",
"short": "Startup funding options",
"desc": "Every realistic way to fund a startup, what each costs in equity or interest, and which stage each option fits.",
"tool": ("/tools/startup-runway-calculator/", "Startup runway calculator"),
"product": "equity",
"body": """
<p>Most startups are not venture-backable, and that is fine. The right funding depends on how fast the business can grow, how much capital it needs before it earns revenue, and how much control the founders want to keep.</p>

<h2 id="ladder">The funding ladder</h2>
<div class="tbl-wrap"><table class="tbl">
<thead><tr><th>Source</th><th>Typical stage</th><th>What it costs you</th></tr></thead>
<tbody>
<tr><td>Bootstrapping / customer revenue</td><td>Day one</td><td>Speed</td></tr>
<tr><td>Friends and family</td><td>Idea to prototype</td><td>Equity or convertible notes, plus relationships</td></tr>
<tr><td>Grants and competitions</td><td>Any, if eligible</td><td>Time spent applying</td></tr>
<tr><td>SBA Microloans, equipment financing</td><td>Early revenue</td><td>Interest, personal guarantee</td></tr>
<tr><td>Angel investors</td><td>Pre-seed to seed</td><td>Equity, often via SAFEs</td></tr>
<tr><td>Accelerators</td><td>Pre-seed</td><td>Equity, usually a single-digit percentage</td></tr>
<tr><td>Venture capital</td><td>Seed onward, high growth</td><td>Equity, board seats, growth expectations</td></tr>
<tr><td>Revenue-based financing</td><td>Recurring revenue</td><td>A capped share of revenue</td></tr>
</tbody></table></div>

<h2 id="safe">SAFEs and convertible notes</h2>
<p>Early rounds often use a SAFE (Simple Agreement for Future Equity) or a convertible note. Investors give cash now and receive equity at the next priced round, typically at a discount or subject to a valuation cap. Understand the cap: stacking several SAFEs at different caps can dilute founders more than expected.</p>

<h2 id="vc">Should you raise venture capital?</h2>
<p>Only if the business can plausibly return a large multiple of the fund's investment, which in practice means a large market and a path to very rapid growth. VC is rocket fuel with an expectation to go big or go out. If your realistic outcome is a profitable business earning a few million a year, debt, RBF and customer revenue are better tools.</p>

<h2 id="runway">Know your runway</h2>
<p>Fundraising commonly takes 3 to 6 months. Start raising with at least 6 to 9 months of cash left. <a href="/tools/startup-runway-calculator/">Calculate your runway</a>.</p>

<h2 id="pitch">What investors check first</h2>
<ol>
<li>Team: why you are the people to win this market</li>
<li>Traction: revenue, growth rate, retention</li>
<li>Market size and why now</li>
<li>Unit economics: customer acquisition cost vs. lifetime value</li>
<li>How much you are raising and the milestones it buys</li>
</ol>
""",
"faqs": [
("How much equity do founders give up in a seed round?", "It varies widely, but many seed rounds sell somewhere in the 10% to 25% range of the company."),
("Can a startup get a bank loan?", "It is hard without revenue. SBA Microloans, equipment financing and personally guaranteed credit are the usual starting points."),
]
},
]

TOOLS = [
{"slug":"business-loan-calculator","calc":"loan","title":"Business Loan Calculator","short":"Business loan","desc":"Calculate monthly payments, total interest and the true APR of a business loan including origination fees.","blurb":"Monthly payment, total interest and true APR after fees.","guide":"business-line-of-credit","product":"term"},
{"slug":"sba-loan-calculator","calc":"sba","title":"SBA 7(a) Loan Calculator","short":"SBA 7(a) loan","desc":"Estimate SBA 7(a) payments using today's prime rate and the SBA maximum rate for your loan size.","blurb":"Uses today's prime rate and SBA rate caps automatically.","guide":"sba-7a-loans","product":"sba"},
{"slug":"mca-apr-calculator","calc":"mca","title":"Merchant Cash Advance APR Calculator","short":"MCA to APR","desc":"Convert a merchant cash advance factor rate into a true APR and see the real daily payment.","blurb":"Convert a factor rate into the APR it really is.","guide":"merchant-cash-advance-vs-loan","product":"loc"},
{"slug":"dscr-calculator","calc":"dscr","title":"DSCR Calculator: How Much Can You Borrow?","short":"DSCR / borrowing power","desc":"Calculate your debt service coverage ratio and the maximum loan lenders will likely approve at 1.25x.","blurb":"Your coverage ratio and maximum loan at 1.25x.","guide":"sba-7a-loans","product":"sba"},
{"slug":"equipment-financing-calculator","calc":"equipment","title":"Equipment Financing Calculator: Loan vs. Lease","short":"Equipment loan vs. lease","desc":"Compare the total cost of an equipment loan against a lease, including down payment and buyout.","blurb":"Total cost of buying vs. leasing, side by side.","guide":"equipment-financing","product":"equipment"},
{"slug":"invoice-factoring-calculator","calc":"factoring","title":"Invoice Factoring Calculator","short":"Invoice factoring","desc":"Calculate your factoring advance, fees, rebate and the effective annual cost of factoring an invoice.","blurb":"Advance, fees, rebate and effective annual cost.","guide":"invoice-factoring","product":"factoring"},
{"slug":"business-valuation-calculator","calc":"valuation","title":"Small Business Valuation Calculator (SDE Multiple)","short":"Business valuation","desc":"Estimate what a small business is worth using seller's discretionary earnings and a market multiple.","blurb":"Estimate a sale price from SDE and a market multiple.","guide":"sba-7a-loans","product":"sba"},
{"slug":"startup-runway-calculator","calc":"runway","title":"Startup Runway Calculator","short":"Startup runway","desc":"Calculate how many months of cash you have left, when you break even, and when to start fundraising.","blurb":"Months of cash left and when to start raising.","guide":"startup-funding-options","product":"equity"},
]
