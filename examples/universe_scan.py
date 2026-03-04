"""
Wider Universe Scan — Pivot Opportunity Framework
===================================================
Starting point: Mirbud (MRB, WSE) is the calibration case.

The question: where else does the framework find HIGH-conviction pivot
situations across European & CEE markets?

Methodology
-----------
1. Screen for structural cheapness (P/B < 1.5, EV/EBITDA < 7x, or P/S < 0.5x)
2. Map to a pivot type — what is the MECHANISM for value release?
3. Verify the mechanism has a concrete observable catalyst
4. Reject companies where cheapness is self-explanatory (structural decline,
   accounting fraud risk, no market for assets)
5. Rank by asymmetry: bull upside / bear downside × probability

Universe scanned
----------------
Starting list of 8 companies across 5 exchanges and 5 pivot types.
Coverage: Poland (WSE), UK (LSE), Austria (VIE), Germany/Frankfurt (DB),
Romania (BVB).

NOT an exhaustive screen — these are situations identified through:
  - PKP PLK / GDDKiA procurement calendar overlap
  - EU infrastructure cohesion fund beneficiaries 2021-2027
  - PSE (Polish grid operator) investment plan 2025-2034
  - Network Rail CP7 (UK, 2024-2029)
  - German Energiewende infrastructure pipeline
  - Post-sanctions European ownership dynamics
  - CEE industrial consolidation wave

Data as of: March 2026 (illustrative; verify against primary sources)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ──────────────────────────────────────────────────────────────────────
# Universe — all companies evaluated
# ──────────────────────────────────────────────────────────────────────

UNIVERSE = [
    {
        "name"         : "Trakcja SA",
        "ticker"       : "TRK",
        "exchange"     : "WSE",
        "country"      : "Poland",
        "sector"       : "Rail construction",
        "pivot_thesis" : "PIPELINE_CERTAINTY — PKP PLK rail beneficiary",
        "key_metrics"  : "P/E 38.5x, +110% in 2025, market cap PLN 2.4bn",
        "verdict"      : "REJECT",
        "reason"       : (
            "Already re-rated. Trakcja is the obvious PKP PLK beneficiary and the "
            "market knows it. P/E 38.5x for a construction contractor is already "
            "pricing in full execution of the rail pipeline. No asymmetry left. "
            "This is what Mirbud looks like AFTER the re-rating. "
            "Study Trakcja as the destination, not the entry point."
        ),
    },
    {
        "name"         : "Friedrich Vorwerk Group",
        "ticker"       : "VWK",
        "exchange"     : "Frankfurt (XETRA)",
        "country"      : "Germany",
        "sector"       : "Energy infrastructure (H2, gas, grid)",
        "pivot_thesis" : "REGULATORY_WINDFALL — German Energiewende H2 pipeline",
        "key_metrics"  : "P/E ~28x, EV/EBITDA ~18x, market cap €420m",
        "verdict"      : "REJECT",
        "reason"       : (
            "Interesting thesis (€13.1bn German H2 network build, Vorwerk is a "
            "specialist contractor) but already fully priced. DCF analysis implies "
            "~25-32% overvaluation at current multiple. The market has priced in "
            "Energiewende upside 2-3 years early. "
            "Worth monitoring: if stock corrects 30%+, thesis becomes interesting."
        ),
    },
    {
        "name"         : "Costain Group",
        "ticker"       : "COST",
        "exchange"     : "LSE",
        "country"      : "UK",
        "sector"       : "Infrastructure & engineering",
        "pivot_thesis" : "PIPELINE_CERTAINTY — Network Rail + HS2 + highways",
        "key_metrics"  : "P/B ~0.5x, FTSE Small Cap, market cap £280m",
        "verdict"      : "WATCH",
        "reason"       : (
            "Similar thesis to Kier Group but weaker execution track record and "
            "smaller scale. P/B 0.5x is attractive but Costain has historically "
            "disappointed on margin delivery. UK infrastructure pipeline is real "
            "(Network Rail CP7 + RIS3 highways), but Kier is the better quality "
            "vehicle for this thesis. Selected Kier instead. "
            "If Kier gets expensive, Costain is the fallback."
        ),
    },
    {
        "name"         : "Kier Group plc",
        "ticker"       : "KIE",
        "exchange"     : "LSE",
        "country"      : "UK",
        "sector"       : "Infrastructure, buildings & MEP",
        "pivot_thesis" : "PIPELINE_CERTAINTY + OPERATIONAL_TURN",
        "key_metrics"  : "P/E 10.55x, P/S 0.27x, market cap £1.09bn, HS2 £700m SIGNED",
        "verdict"      : "SELECT",
        "reason"       : (
            "Network Rail CP7 framework supplier (£38bn, 2024-2029) + HS2 £700m "
            "confirmed contracts. Operational turn from loss-making to profitable "
            "under new management. Added to FTSE 250 March 2025 = forced passive "
            "inflows. P/E 10.55x vs UK construction sector ~18x. Stock up 63% "
            "in past year but still cheap. High certainty on revenue existence."
        ),
    },
    {
        "name"         : "Onde SA",
        "ticker"       : "ONDP",
        "exchange"     : "WSE",
        "country"      : "Poland",
        "sector"       : "Renewable energy EPC + developer",
        "pivot_thesis" : "STRATEGIC_REPOSITION + ASSET_RELEASE",
        "key_metrics"  : (
            "Market cap PLN 550m, revenue PLN 804m, EBITDA 7%, "
            "1.36 GW developer portfolio (PLN 680m-1.36bn hidden value)"
        ),
        "verdict"      : "SELECT",
        "reason"       : (
            "Onde is priced as an EPC contractor (P/S 0.68x) but owns a 1.36 GW "
            "developer portfolio worth PLN 680m-1.36bn — more than the entire "
            "market cap. PSE grid investment plan PLN 64-66bn (2025-2034) = "
            "massive EPC pipeline. If developer portfolio is monetised (sale to "
            "IPP or own balance sheet development), stock re-rates to developer "
            "multiples. The hidden asset exceeds the market cap."
        ),
    },
    {
        "name"         : "Polimex-Mostostal SA",
        "ticker"       : "PXM",
        "exchange"     : "WSE",
        "country"      : "Poland",
        "sector"       : "Industrial / energy / infrastructure construction",
        "pivot_thesis" : "REGULATORY_WINDFALL — Polish nuclear programme",
        "key_metrics"  : (
            "Market cap PLN 754m, revenue PLN 2.86bn, net loss PLN -348m (2024), "
            "Mostostal Siedlce pre-qualified by Westinghouse for AP1000 nuclear"
        ),
        "verdict"      : "SELECT",
        "reason"       : (
            "Distressed core business (net loss PLN 348m, 2024), but subsidiary "
            "Mostostal Siedlce was selected by Westinghouse as a Polish partner for "
            "the AP1000 nuclear programme (3 reactors at Lubiatowo-Kopalino). "
            "Polish nuclear: $15bn+ construction value, state financing committed, "
            "CfD mechanism in place. If Polimex captures 10-15% of nuclear construction "
            "value, it transforms the company. High risk (distressed) but massive "
            "asymmetry. The bet: nuclear timeline materialises before core burns too much."
        ),
    },
    {
        "name"         : "Strabag SE",
        "ticker"       : "STR",
        "exchange"     : "Vienna (VIE)",
        "country"      : "Austria",
        "sector"       : "Pan-European construction",
        "pivot_thesis" : "OWNERSHIP_CHANGE — Rasperia sanctions resolution",
        "key_metrics"  : (
            "~€92/share (near ATH €98.30), market cap ~€10bn, revenue €19.2bn, "
            "EBITDA €1.43bn (7.8%), backlog €30bn+ (record), free float 14.1%"
        ),
        "verdict"      : "SELECT",
        "reason"       : (
            "Rasperia Trading (Deripaska-linked) holds 24.1% frozen under EU sanctions. "
            "EU sanctions package 19 potentially unlocks the stake. If Rasperia stake "
            "is resolved (sold to long-term investor or bought back), free float "
            "increases from 14% and institutional re-rating follows. "
            "Already re-rated +104% in 2025 but still 4-6x EV/EBITDA for "
            "Europe's 3rd-largest contractor with record €30bn backlog. "
            "Residual upside on sanctions normalisation + backlog quality. "
            "The Haselsteiner family (32.5%) provides governance anchor."
        ),
    },
    {
        "name"         : "ROCA Industry SA",
        "ticker"       : "ROC1",
        "exchange"     : "BVB (Bucharest)",
        "country"      : "Romania",
        "sector"       : "Industrial manufacturing (serial acquirer)",
        "pivot_thesis" : "CONSOLIDATION — Romanian industrial roll-up",
        "key_metrics"  : (
            "Market cap RON 178m (~€36m), revenue RON 629m, "
            "EBITDA margin 9.98%, EV/EBITDA ~2.8x, BVB Main Market"
        ),
        "verdict"      : "SELECT",
        "reason"       : (
            "Serial acquirer: BICO, EVOLOR, ECO EURO DOORS, ELECTROPLAST, VELTA DOORS. "
            "Upgraded from AeRO to BVB Main Market (March 2024) = institutional discovery. "
            "EV/EBITDA ~2.8x is extreme cheapness for a growing industrial platform. "
            "RON 140.7m private placement + RON 50m bond issue for next acquisitions. "
            "Romanian GDP still catching up to EU peers = structural tailwind. "
            "Risk: small float, thin liquidity, Romania governance discount. "
            "Reward: correct multiple = 7-10x EV/EBITDA → +150-250% re-rating."
        ),
    },
]


# ──────────────────────────────────────────────────────────────────────
# Screening criteria (what had to be true to get on the list)
# ──────────────────────────────────────────────────────────────────────

SCREENING_CRITERIA = {
    "Cheapness metric"    : "P/B < 1.5 OR EV/EBITDA < 7x OR P/S < 0.5x OR P/E < 15x",
    "Pivot mechanism"     : "Must map to one of the 8 framework PivotTypes",
    "Observable catalyst" : "A specific event that fires the pivot in <36 months",
    "Market existence"    : "Revenue source must be independently verifiable (pipeline/orders/regulated)",
    "Survival floor"      : "Core business can survive 2-3 years while waiting",
    "Asymmetry minimum"   : "Bull upside / Bear downside > 2.0x (probability-weighted)",
    "REJECT: already run" : "Stock re-rated >80% since thesis formed → no asymmetry",
    "REJECT: no catalyst" : "Cheap for 5+ years with no upcoming event → value trap",
}

PIVOT_TYPE_COVERAGE = {
    "PIPELINE_CERTAINTY"   : ["Kier Group"],
    "OPERATIONAL_TURN"     : ["Kier Group"],
    "STRATEGIC_REPOSITION" : ["Onde SA"],
    "ASSET_RELEASE"        : ["Onde SA"],
    "REGULATORY_WINDFALL"  : ["Polimex-Mostostal"],
    "OWNERSHIP_CHANGE"     : ["Strabag SE"],
    "CONSOLIDATION"        : ["ROCA Industry"],
}


def print_universe_scan():
    sep  = "═" * 76
    thin = "─" * 76

    print(f"\n{sep}")
    print("  WIDER UNIVERSE SCAN — Pivot Opportunity Framework")
    print("  European & CEE Markets — March 2026")
    print(sep)

    # Screening criteria
    print(f"\n  SCREENING CRITERIA")
    print(thin)
    for criterion, rule in SCREENING_CRITERIA.items():
        print(f"  {criterion:<25}: {rule}")

    # Full universe table
    print(f"\n\n  UNIVERSE EVALUATED ({len(UNIVERSE)} companies)")
    print(thin)
    selected = [c for c in UNIVERSE if c["verdict"] == "SELECT"]
    rejected = [c for c in UNIVERSE if c["verdict"] == "REJECT"]
    watch    = [c for c in UNIVERSE if c["verdict"] == "WATCH"]

    verdict_symbols = {"SELECT": "✓", "REJECT": "✗", "WATCH": "~"}

    for company in UNIVERSE:
        sym = verdict_symbols[company["verdict"]]
        print(f"\n  {sym} {company['name']:<30} [{company['ticker']}:{company['exchange']}]  "
              f"{company['country']}")
        print(f"    Thesis : {company['pivot_thesis']}")
        print(f"    Metrics: {company['key_metrics']}")
        print(f"    {company['verdict']:<8}: {company['reason'][:100]}...")

    # Final selection
    print(f"\n\n{thin}")
    print("  FINAL SELECTION — 5 COMPANIES")
    print(thin)
    print(f"\n  {'Company':<30} {'Ticker':<8} {'Exchange':<12} {'Pivot Type':<35} {'Key Asymmetry'}")
    print(f"  {'-'*30} {'-'*8} {'-'*12} {'-'*35} {'-'*30}")

    selection_details = [
        ("Kier Group plc",       "KIE",  "LSE",     "PIPELINE_CERTAINTY + OPERATIONAL_TURN",  "P/E 10.55x → 16-18x as turn completes"),
        ("Onde SA",              "ONDP", "WSE",     "STRATEGIC_REPOSITION + ASSET_RELEASE",    "1.36 GW portfolio > market cap"),
        ("Polimex-Mostostal SA", "PXM",  "WSE",     "REGULATORY_WINDFALL (nuclear)",           "Distressed → nuclear renaissance play"),
        ("Strabag SE",           "STR",  "VIE",     "OWNERSHIP_CHANGE (sanctions)",            "Frozen 24.1% → free float doubles"),
        ("ROCA Industry SA",     "ROC1", "BVB",     "CONSOLIDATION (CEE roll-up)",             "2.8x EV/EBITDA → 7-10x re-rating"),
    ]

    for name, ticker, exch, pivot, asym in selection_details:
        print(f"  {name:<30} {ticker:<8} {exch:<12} {pivot:<35} {asym}")

    # Pivot type coverage
    print(f"\n\n{thin}")
    print("  PIVOT TYPE COVERAGE")
    print(thin)
    print(f"\n  {'Pivot Type':<25} {'Companies'}")
    print(f"  {'-'*25} {'-'*35}")
    for pt, companies in PIVOT_TYPE_COVERAGE.items():
        print(f"  {pt:<25} {', '.join(companies)}")

    print(f"\n\n{thin}")
    print("  WHAT WAS NOT FOUND")
    print(thin)
    print("""
  TECH_ADOPTION (0 companies): No legacy European construction/industrial company
    is visibly re-rating from a credible digital/AI adoption story in Q1 2026.
    Closest candidates (Strabag's BRVB digital unit, Zeres robotics) are too small
    to move the needle on parent multiples.

  CAPITAL_STRUCTURE (0 selected): Several Polish family companies have excess cash
    but no catalyst to distribute it. Mirbud itself fits this type as secondary pivot
    but we avoided adding companies where the ONLY thesis is "they should do a buyback"
    — that's not a catalyst, it's a wish.

  Pure activist plays (0): European activist investment is less developed than US.
    Polish minority rights are weak (Warsaw Court of Arbitration jurisdiction applies,
    squeeze-out at 95% threshold, courts slow). No clean activist play identified
    where the path is credible enough to model as primary thesis.
""")

    print(f"\n{thin}")
    print("  GEOGRAPHIC DISTRIBUTION")
    print(thin)
    print("""
  Poland (WSE)  : 3 companies — Onde SA, Polimex-Mostostal, Mirbud (reference)
    Common factor: EU cohesion funds 2021-2027 + PKP PLK + PSE spending pipeline.
    Poland is the single most compelling hunting ground for pipeline-certainty plays.

  UK (LSE)      : 1 company — Kier Group
    Common factor: Network Rail CP7 + HS2. UK is the only other market with a
    comparably well-documented, legally-committed infrastructure pipeline.

  Austria (VIE) : 1 company — Strabag SE
    Single situation: Rasperia sanctions play. Not a country-level thesis.

  Romania (BVB) : 1 company — ROCA Industry
    Emerging market consolidation discount. Romania GDP/capita still ~60% of EU27
    average = structural catch-up + local M&A opportunities.
""")
    print(sep)
    print(f"\n  See individual company files for full models:")
    for c in selected:
        fname = c["name"].lower().replace(" ", "_").replace(".", "").replace(",", "")
        # clean names
        mapping = {
            "kier_group_plc": "kier_group",
            "onde_sa": "onde_sa",
            "polimex-mostostal_sa": "polimex_nuclear",
            "strabag_se": "strabag_se",
            "roca_industry_sa": "roca_industry",
        }
        fname = mapping.get(fname, fname)
        print(f"    examples/{fname}.py")
    print()


if __name__ == "__main__":
    print_universe_scan()
