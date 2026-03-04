"""
Extended Asymmetric Idea Taxonomy
===================================
The PivotType enum in models.py covers 8 construction/industrial pivot types.
This module extends the taxonomy to cover the FULL range of situations that
hedge funds and asymmetric investors look for.

The framework distinguishes between:
  PivotType  — the MECHANISM through which value is released (already built)
  IdeaType   — the STRUCTURAL SETUP that creates mispricing (this module)

Both are orthogonal: a single company can have one IdeaType and one or more
PivotTypes. For example: Strabag has IdeaType=PARENT_DISPOSITION and
PivotType=OWNERSHIP_CHANGE.

IdeaType answers: WHY is this mispriced?
PivotType answers: WHAT will release the value?

IdeaType categories:
  I.  ASSET-BASED MISPRICING
  II. INFORMATION ASYMMETRY
  III. FORCED SELLING / TECHNICAL
  IV. CORPORATE EVENT / BINARY CATALYST
  V.  STRUCTURAL DEMAND / SECTOR
  VI. STAKEHOLDER CONFLICT
  VII. MACRO / GEOPOLITICAL
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class IdeaType(Enum):
    # ────────────────────────────────────────────────────────────────
    # I. ASSET-BASED MISPRICING
    # The stock is cheap because the market misvalues what it owns
    # ────────────────────────────────────────────────────────────────

    SOTP_DISCOUNT = "sotp_discount"
    # Conglomerate / holding company trades below sum-of-parts NAV.
    # Classic activist play. The whole is worth less than the pieces.
    # Example: Agora SA (cinemas + OOH + radio + press: each worth more than total)
    # What to find: conglomerates where any single division > market cap
    # Catalyst: spin-off, partial sale, activist pressure, PE buyout

    HIDDEN_ASSET = "hidden_asset"
    # Off-balance-sheet or book-at-cost asset worth more than market cap.
    # Example: Onde SA developer portfolio (1.36 GW at PLN 500k/MW not on books)
    # Example: Land bank carried at historical cost vs. current market
    # What to find: companies where intangibles/assets carried well below market value
    # Catalyst: asset sale, revaluation, spinoff, or M&A bid based on asset price

    CATALOG_OPTIONALITY = "catalog_optionality"
    # IP / brand / library with recurring value plus a "lumpy" future release option.
    # Example: CD Projekt (Cyberpunk catalog + Witcher 4 call option)
    # Example: Pharmaceutical with patent cliff + pipeline drug option
    # Example: Publisher with back-catalog royalties + upcoming title
    # What to find: low trough value (between releases/launches) + high option premium
    # Catalyst: launch event, pre-order surge, licensing deal

    HOLDING_COMPANY_ORPHAN = "holding_company_orphan"
    # Listed subsidiary orphaned after parent restructuring; no natural owner;
    # trades at discount because institutional mandates don't cover it.
    # Example: spinoffs in the 12 months after parent divestiture
    # Catalyst: index inclusion 12-18 months post-listing, buyer discovered

    # ────────────────────────────────────────────────────────────────
    # II. INFORMATION ASYMMETRY
    # The stock is cheap because the market lacks information
    # ────────────────────────────────────────────────────────────────

    MICRO_CAP_NEGLECT = "micro_cap_neglect"
    # Company too small for institutional research; excellent fundamentals;
    # no analyst coverage; trades at discount to quality.
    # Example: Lubawa SA (LBW, WSE): P/E 5.86x, EV/EBITDA 3.79x, ROE 29%,
    #   revenue +52% YoY, zero analyst coverage, 0% institutional ownership
    # What to find: <€100m market cap, profitable, growing, no coverage
    # Catalyst: First institutional buy, first analyst note, index inclusion

    INSIDER_CLUSTER = "insider_cluster"
    # Multiple corporate insiders buying shares in the open market within
    # a short window — a powerful signal because:
    #   1. Multiple people independently concluded the stock is cheap
    #   2. They're subject to MAR — only buy when confident no MNPI
    #   3. Open market purchases are stronger than option exercises
    # Example: 3+ board members buying in same 30-day window at 52-week low
    # What to find: ESPI in Poland, SEC Form 4 in US, PDMR in UK
    # Catalyst: The buying IS the catalyst — smart insiders front-running recovery

    LANGUAGE_BARRIER = "language_barrier"
    # Company in non-English language jurisdiction (Polish, Romanian, Czech)
    # with no English investor relations; Western funds can't access research.
    # Example: Any Polish micro-cap with ESPI-only reporting
    # What to find: excellent companies with Polish-only IR and annual reports
    # Catalyst: English IR launch, ADR/GDR issuance, IR roadshow to London/NY

    FRONTIER_MARKET_RECLASSIFICATION = "frontier_market_reclassification"
    # Stock exchange being upgraded (Frontier → Emerging Market by MSCI).
    # All index-tracking funds must buy ALL constituents on upgrade.
    # Even tiny allocations = massive demand vs. illiquid float.
    # Example: BVB Bucharest potential MSCI EM upgrade (ROCA Industry)
    # Example: WSE actual MSCI DM upgrade (announced 2025, effective 2026)
    # Catalyst: MSCI announcement, index inclusion date, passive fund buy

    # ────────────────────────────────────────────────────────────────
    # III. FORCED SELLING / TECHNICAL DISCOUNT
    # Stock is cheap because someone HAS TO sell regardless of value
    # ────────────────────────────────────────────────────────────────

    INDEX_FORCED_SELLING = "index_forced_selling"
    # Stock deleted from index: index funds must sell regardless of value.
    # The sale is mechanical, not fundamental. Temporary discount available.
    # Example: Company dropped from FTSE 250 → forced selling by trackers
    # What to find: Companies that recently fell out of an index
    # Catalyst: Selling completes; stock re-qualifies for index

    SANCTIONS_FROZEN_OVERHANG = "sanctions_frozen_overhang"
    # Large frozen stake (sanctions, court order) cannot be sold or voted.
    # Artificial reduction of free float → institutional investors can't buy.
    # Example: Strabag SE (Rasperia 24.1% frozen)
    # Catalyst: Sanctions lifted, stake resolved (sale, buyback, restructuring)

    PARENT_DISPOSITION = "parent_disposition"
    # Parent company forced to sell / divest subsidiary due to:
    #   - Own M&A (acquirer divests acquired assets)
    #   - Regulatory conditions (antitrust, concentration)
    #   - Financial distress (parent needs cash)
    # Example: mBank (WSE: MBK) — Commerzbank under UniCredit pressure
    # Catalyst: Parent announces divestiture, IPO, or sale process

    ESG_EXCLUSION_LIFT = "esg_exclusion_lift"
    # Company excluded from ESG mandates (nuclear, weapons, gambling, coal)
    # triggers institutional forced selling. If exclusion reverses (e.g.
    # EU taxonomy reclassification), the same funds are forced to buy.
    # Example: Nuclear classified as "sustainable" in EU taxonomy (2022) →
    #   ESG funds can now buy nuclear operators and utilities
    # Catalyst: Taxonomy/mandate change announcement

    # ────────────────────────────────────────────────────────────────
    # IV. CORPORATE EVENT / BINARY CATALYST
    # Value crystallised by a specific upcoming event
    # ────────────────────────────────────────────────────────────────

    SPINOFF_ORPHAN = "spinoff_orphan"
    # Post-spinoff stock is orphaned: parent shareholders don't want it,
    # it's too small for institutional ownership, no sell-side coverage.
    # Usually most interesting in first 6-18 months post-separation.
    # What to find: Spinoffs in last 12 months, no analyst coverage

    MERGER_ARBITRAGE = "merger_arbitrage"
    # Announced deal with spread. Risk: deal breaks. Reward: spread closes.
    # Higher-conviction: cash deal by strategic buyer with no financing risk.
    # What to find: Announced deals trading >5% below offer price

    CHF_RESOLUTION = "chf_resolution"
    # Polish banks carry legacy Swiss franc mortgage legal overhang.
    # Courts siding with borrowers → provisions, capital tied up.
    # As portfolio runs off and provisions finalise, capital released.
    # Example: mBank, Bank Millennium, BNP Paribas Bank Polska
    # Catalyst: Final court decisions, settlement announcements

    RIGHTS_ISSUE_MISPRICING = "rights_issue_mispricing"
    # New shares issued at discount; rights trade below theoretical value
    # due to retail investor confusion or institutional selling constraints.
    # Duration: the rights trading period (typically 2-3 weeks)
    # What to find: Rights issues in progress; rights trading below intrinsic

    # ────────────────────────────────────────────────────────────────
    # V. STRUCTURAL DEMAND / SECTOR TAILWIND
    # Company in the path of a large, committed, multi-year demand wave
    # ────────────────────────────────────────────────────────────────

    DEFENSE_REARMAMENT = "defense_rearmament"
    # NATO spending wave (Russia-Ukraine war, 2% → 4-5% GDP commitments).
    # Poland ($301.6bn 2026-2030), Germany (€500bn Sondervermögen),
    # UK, Sweden, Finland, Baltics — all accelerating defense capex.
    # What to find: Defence sub-contractors, logistics, protective equipment
    # priced as industrial/commodity companies despite defense growth rates
    # Example: Lubawa SA — P/E 5.86x, ROE 29%, defense revenue +52% YoY

    PIPELINE_CERTAINTY = "pipeline_certainty"
    # Government-committed multi-year infrastructure spend creates
    # near-certain revenue for contractors/suppliers. Not a forecast.
    # Examples: Network Rail CP7, PKP PLK, PSE grid, KPO funds

    REGULATORY_WINDFALL = "regulatory_windfall"
    # New regulation creates a protected market, monopoly position, or
    # mandatory demand that didn't exist before.
    # Examples: Nuclear CfD in Poland, EU taxonomy nuclear re-classification

    RECONSTRUCTION_OPTION = "reconstruction_option"
    # Post-conflict reconstruction creates massive demand.
    # Requires: conflict to end OR areas in current/prior conflict to rebuild.
    # Example: Ukraine reconstruction (€400-500bn estimated need)
    # What to find: Companies with assets in conflict zones that will operate again

    # ────────────────────────────────────────────────────────────────
    # VI. STAKEHOLDER CONFLICT / GOVERNANCE
    # Value trapped by stakeholder dynamics; catalyst = alignment
    # ────────────────────────────────────────────────────────────────

    MINORITY_SQUEEZE = "minority_squeeze"
    # Majority owner wants to take company private; minority shareholders
    # can hold out for fair value or be squeezed at mandatory offer price.
    # In Poland: 95% threshold triggers mandatory buyout (squeeze-out)
    # What to find: Companies at 80-94% majority ownership

    ACTIVIST_PRESSURE = "activist_pressure"
    # Activist investor has entered or is expected to enter.
    # Forces: spin-offs, buybacks, management change, sale.
    # In Europe: more common in UK/Nordics than CEE.
    # What to find: Cheap companies where activist logic is obvious

    GOVERNANCE_IMPROVEMENT = "governance_improvement"
    # Company with poor governance re-rating as practices improve.
    # Example: New CEO, independent board, formal dividend policy.
    # Example: Family company transitioning to professional management.

    # ────────────────────────────────────────────────────────────────
    # VII. MACRO / GEOPOLITICAL
    # Value dependent on external macro/geopolitical resolution
    # ────────────────────────────────────────────────────────────────

    GEOPOLITICAL_RESOLUTION = "geopolitical_resolution"
    # Binary geopolitical event resolution (peace deal, sanctions lift,
    # election outcome, treaty) that changes asset values fundamentally.
    # Examples: Ukraine ceasefire → Kernel Holding, Ukrainian reconstruction plays
    #           Russia sanctions lift → Strabag Rasperia, Novatek assets
    # Risk: timing unknown; waiting cost can destroy IRR

    CURRENCY_CONVERGENCE = "currency_convergence"
    # Company in emerging market currency; currency appreciating vs EUR/USD
    # creates EUR-denominated return uplift beyond local stock performance.
    # Example: Romanian RON, Polish PLN — both appreciating as EU convergence plays
    # What to find: Good companies priced in undervalued local currencies


# ────────────────────────────────────────────────────────────────────────
# Profiles per idea type
# ────────────────────────────────────────────────────────────────────────

@dataclass
class IdeaProfile:
    idea_type:          IdeaType
    display_name:       str
    setup_description:  str      # What creates the mispricing
    catalyst:           str      # What resolves it
    time_horizon:       str      # "days/weeks" / "months" / "1-2 years" / "2-5 years"
    key_metrics:        list     # What data to look for
    red_flags:          list     # What kills the thesis
    historical_examples: list   # Real world cases
    hf_style:           str      # Which HF strategy typically plays this
    return_profile:     str      # How returns are generated
    optionality:        float    # 0-1: how much upside depends on binary outcome


IDEA_PROFILES: dict[IdeaType, IdeaProfile] = {

    IdeaType.SOTP_DISCOUNT: IdeaProfile(
        idea_type=IdeaType.SOTP_DISCOUNT,
        display_name="Sum-of-Parts / NAV Discount",
        setup_description=(
            "Conglomerate or holding company where the market applies a 'complexity "
            "discount' to the whole. Each division would trade at a higher multiple "
            "independently. The discount exists because: (a) index funds can't "
            "hold every micro-cap division, (b) analysts only cover one segment, "
            "(c) management has conflicting incentives."
        ),
        catalyst=(
            "Spin-off, partial asset sale, strategic review, PE buyout of whole company, "
            "or activist letter demanding break-up. In Poland: SOTP discounts can persist "
            "for years without a catalyst — REQUIRES a specific event."
        ),
        time_horizon="1-3 years",
        key_metrics=[
            "Sum-of-parts NAV / market cap ratio > 1.5x",
            "At least one division > market cap in isolation",
            "Divisions have natural trade buyers (strategic + financial)",
            "Management discusses or hints at strategic review",
        ],
        red_flags=[
            "Controlling shareholder with no financial pressure",
            "Divisions operationally integrated (can't be separated)",
            "Loss-making division that must be carried",
            "No external buyers (illiquid private market for assets)",
        ],
        historical_examples=[
            "Agora SA (Poland) — cinemas + OOH + radio: any single asset > total market cap",
            "Liberty Global — cable assets broken up over 2018-2022",
            "Rolls-Royce — Power Systems break-up thesis (2019-2021)",
        ],
        hf_style="Event-driven, Value, Activist",
        return_profile="Value re-rating upon catalyst; partial sale = price discovery event",
        optionality=0.50,
    ),

    IdeaType.MICRO_CAP_NEGLECT: IdeaProfile(
        idea_type=IdeaType.MICRO_CAP_NEGLECT,
        display_name="Micro-Cap Neglect / Institutional Blindspot",
        setup_description=(
            "Company is simply too small for institutional investors to research. "
            "Zero analyst coverage, <5% institutional ownership, but: profitable, "
            "growing, with high returns on capital. The discount = pure visibility gap. "
            "These are often the highest-quality businesses in the market "
            "priced as if they're risky just because they're small."
        ),
        catalyst=(
            "First analyst note, institutional discovery, index inclusion, "
            "corporate action (buyback, acquisition, IR roadshow). "
            "The catalyst is often the INVESTOR THEMSELVES publishing research."
        ),
        time_horizon="1-3 years",
        key_metrics=[
            "Market cap < €150m",
            "Zero analyst coverage (Bloomberg/FactSet)",
            "< 10% institutional ownership",
            "ROE > 15%, ROIC > 12%",
            "Revenue growing > 15% organically",
            "P/E < 12x despite quality metrics",
        ],
        red_flags=[
            "Illiquid float (< PLN 1m daily volume) — can't build position",
            "Insider ownership so high that float is effectively zero",
            "Family company with no interest in institutional engagement",
            "Single-customer concentration risk",
        ],
        historical_examples=[
            "Lubawa SA (LBW, WSE) — P/E 5.86x, ROE 29%, EV/EBITDA 3.79x, "
            "0 analysts, 0% institutional, defense revenue +52% YoY",
            "Many Nordic and CEE micro-caps before institutional discovery",
        ],
        hf_style="Long-only small-cap, Family office, Fundamental value",
        return_profile="Multiple re-rating as institutional discovers; plus organic growth",
        optionality=0.20,
    ),

    IdeaType.INSIDER_CLUSTER: IdeaProfile(
        idea_type=IdeaType.INSIDER_CLUSTER,
        display_name="Insider Buying Cluster (ESPI / Form 4 / PDMR)",
        setup_description=(
            "Multiple corporate insiders (board members, supervisory board, CFO, CEO) "
            "buying shares in the open market within a short window (30 days). "
            "Powerful because: (1) each person has independently decided the stock "
            "is undervalued, (2) they're legally barred from trading on MNPI, "
            "(3) open-market purchases with personal cash = highest conviction signal."
        ),
        catalyst=(
            "The buying itself is a leading indicator. Insiders know the company "
            "better than anyone. Cluster buying tends to precede: earnings beats, "
            "contract announcements, M&A bids, or simply multiple expansion "
            "as the market 'catches up' to insider conviction."
        ),
        time_horizon="3-18 months",
        key_metrics=[
            "≥ 3 insiders buying in ≤ 30-day window",
            "Total buying > PLN 1m (material amount, not token purchases)",
            "At least one C-suite (CEO/CFO) in the cluster",
            "Buying at or near 52-week low (contrarian signal)",
            "No offsetting insider selling in same window",
        ],
        red_flags=[
            "Option exercises (these are forced; not a buy signal)",
            "Buying at all-time highs (less meaningful than buying at lows)",
            "Single insider only (less conviction than cluster)",
            "Company in media or industry blackout period (ambiguous legality)",
        ],
        historical_examples=[
            "Dino Polska ESPI 12/2025 — supervisory board member purchase",
            "LPP SA ESPI 21/2025 — management share transactions",
            "Many US examples via OpenInsider: CEO + CFO + Director buying same week",
        ],
        hf_style="Quantitative, Event-driven, Fundamental",
        return_profile="Alpha from signal, returns tied to underlying company recovery",
        optionality=0.30,
    ),

    IdeaType.DEFENSE_REARMAMENT: IdeaProfile(
        idea_type=IdeaType.DEFENSE_REARMAMENT,
        display_name="Defense Rearmament — NATO Spending Wave",
        setup_description=(
            "NATO members committing 4-5% of GDP to defense (vs. historic 2%). "
            "Poland alone: $301.6bn in defense spending 2026-2030 (vs. $138.1bn in 2021-25). "
            "Germany: €500bn Sondervermögen. UK, Nordics, Baltics: all accelerating. "
            "Sub-contractors priced as industrial companies despite structural "
            "defence demand curves that bear no resemblance to normal cyclicals."
        ),
        catalyst=(
            "Contract announcements (typically quarterly NATO procurement cycles), "
            "earnings beats on growing defense revenues, analyst initiation. "
            "Unlike construction, defense contracts have 3-10 year delivery schedules "
            "= multi-year revenue visibility."
        ),
        time_horizon="2-5 years",
        key_metrics=[
            "Revenue > 50% from defense / government clients",
            "Backlog / annual revenue > 2x",
            "P/E < 15x despite > 20% revenue growth",
            "EV/EBITDA < 10x vs. defense sector median 15-25x",
            "NATO certification / cleared supplier status",
        ],
        red_flags=[
            "Heavy dependence on single country's defense budget",
            "Commodity products (easily sourced elsewhere by MoD)",
            "High working capital intensive — government slow payer risk",
            "Priced for growth already (Rheinmetall at 30x = no asymmetry)",
        ],
        historical_examples=[
            "Lubawa SA (LBW, WSE) — protective textiles, NATO anti-drone ponchos; "
            "P/E 5.86x, EV/EBITDA 3.79x, 0% institutional, revenue growing 50% YoY",
            "Diehl Defence, KNDS, Thales — major beneficiaries but already re-rated",
        ],
        hf_style="Long/short thematic, Sector specialist",
        return_profile="Multiple expansion as defense sector re-rates; earnings growth",
        optionality=0.25,
    ),

    IdeaType.PARENT_DISPOSITION: IdeaProfile(
        idea_type=IdeaType.PARENT_DISPOSITION,
        display_name="Parent Under Pressure — Forced Subsidiary Sale",
        setup_description=(
            "Parent company faces pressure (M&A, financial distress, regulatory "
            "condition) that forces it to divest a subsidiary. The subsidiary "
            "trades cheaply because the market prices in: uncertainty of whether "
            "it will be sold, who will buy it, at what price. "
            "When the sale materialises, the subsidiary reprices to strategic value."
        ),
        catalyst=(
            "Parent announces strategic review, IPO plans, or binding offer. "
            "Or: parent M&A closes, new parent immediately announces divestiture."
        ),
        time_horizon="1-3 years",
        key_metrics=[
            "Parent under visible pressure (M&A target, distress, antitrust)",
            "Subsidiary profitable and standalone-viable",
            "Strategic buyers exist for the subsidiary",
            "Subsidiary market cap << standalone DCF value",
        ],
        red_flags=[
            "Parent has sole motivation to sell at minimum price (minority damage)",
            "Subsidiary has interco dependencies (can't stand alone easily)",
            "Regulatory approval required and uncertain",
        ],
        historical_examples=[
            "mBank (WSE: MBK) — Commerzbank under UniCredit; if sold, new owner "
            "would likely divest as Poland overlap with UniCredit Vodeno",
            "Strabag ESG situation with Rasperia",
        ],
        hf_style="Event-driven, Special situations",
        return_profile="Buyout premium (typically 20-40%) on transaction announcement",
        optionality=0.65,
    ),

    IdeaType.CHF_RESOLUTION: IdeaProfile(
        idea_type=IdeaType.CHF_RESOLUTION,
        display_name="CHF Mortgage Resolution — Polish Banks",
        setup_description=(
            "Polish banks hold legacy CHF-denominated mortgage portfolios. "
            "Courts have sided with borrowers → banks provisioned heavily, "
            "tying up capital and dragging on earnings. "
            "As the CHF portfolio runs off (loans are being repaid or settled), "
            "the overhang lifts: provisions reverse, capital is released, P/E "
            "normalises."
        ),
        catalyst=(
            "Settlement announcements (bulk CHF resolution vs. individual court cases), "
            "Supreme Court clarifying ruling, CHF provision reversal in earnings. "
            "mBank: CHF risk costs fell >50% YoY in 2025."
        ),
        time_horizon="1-2 years",
        key_metrics=[
            "CHF portfolio as % of total loans (lower = safer)",
            "Provision coverage ratio (higher = safer, more priced in)",
            "P/E discount to European bank peers not carrying CHF risk",
            "CET1 ratio above regulatory minimum + SREP",
        ],
        red_flags=[
            "New adverse Supreme Court ruling expanding bank liability",
            "Polish parliament enacting retroactive legislation",
            "Concentration in CHF (Bank Millennium has 9.4%)",
        ],
        historical_examples=[
            "mBank SA (MBK) — Commerzbank subsidiary; CHF costs -50% YoY in 2025; "
            "P/E 12.4x, ROE 16.4%, cost-to-income <30%. DCF: +20% undervalued.",
            "Bank Millennium, BNP Paribas Bank Polska — similarly affected",
        ],
        hf_style="Value, Event-driven, Sector specialist (banks)",
        return_profile="P/E expansion as legal overhang lifts; dividend resumption",
        optionality=0.35,
    ),

    IdeaType.FRONTIER_MARKET_RECLASSIFICATION: IdeaProfile(
        idea_type=IdeaType.FRONTIER_MARKET_RECLASSIFICATION,
        display_name="Exchange Reclassification (Frontier → Emerging Market)",
        setup_description=(
            "MSCI or FTSE upgrades a stock exchange from Frontier to Emerging Market. "
            "Passive EM funds must buy ALL eligible constituents, often at tiny weights, "
            "but the markets are illiquid → even small allocations = massive demand "
            "relative to free float. "
            "WSE has been classified as Developed Market (MSCI, effective 2026). "
            "BVB Bucharest: applying for MSCI EM upgrade."
        ),
        catalyst="MSCI/FTSE announcement of reclassification (typically June/September review)",
        time_horizon="1-2 years",
        key_metrics=[
            "Exchange currently in MSCI Frontier or not classified",
            "Liquidity improving (MSCI requires minimum turnover)",
            "Number of eligible companies at inclusion",
        ],
        red_flags=[
            "Multiple failed applications (MSCI has rejected BVB before)",
            "Market cap / liquidity criteria not met",
        ],
        historical_examples=[
            "Saudi Arabia upgrade to MSCI EM (2018-2019): stock market +35% in 12 months",
            "Poland: classified as MSCI Developed Market 2026 → passive DM inflows",
            "BVB Bucharest: applying for MSCI EM upgrade",
        ],
        hf_style="Index-aware, Macro/EM, Country specialist",
        return_profile="Passive buying wave + institutional discovery re-rating",
        optionality=0.70,
    ),

    IdeaType.GEOPOLITICAL_RESOLUTION: IdeaProfile(
        idea_type=IdeaType.GEOPOLITICAL_RESOLUTION,
        display_name="Geopolitical Resolution Binary",
        setup_description=(
            "Assets priced near zero due to war/sanctions/conflict. "
            "If resolution occurs, the re-rating is massive. "
            "The key question: what probability does the market assign to resolution? "
            "Often, for very cheap assets, even 20-30% probability of resolution "
            "makes the expected value attractive."
        ),
        catalyst="Peace deal, ceasefire, sanctions lift, election outcome, treaty",
        time_horizon="1-5 years (highly uncertain)",
        key_metrics=[
            "Asset quality: would it be valuable if conflict ended?",
            "Implied resolution probability from current market price",
            "Alternative scenario (no resolution): what is the floor?",
            "Reconstruction funding commitments (EU, US, IMF)",
        ],
        red_flags=[
            "Assets physically destroyed (not just disrupted)",
            "Political resolution impossible (existential conflict)",
            "Legal / title risk in post-conflict environment",
        ],
        historical_examples=[
            "Kernel Holding: Ukraine agri assets — operating profitably during war, "
            "reconstruction option adds massive value if peace arrives",
            "Strabag / Rasperia: sanctions resolution play",
        ],
        hf_style="Macro, Geopolitical specialist, Event-driven",
        return_profile="Binary: massive gain on resolution, significant loss if conflict escalates",
        optionality=0.85,
    ),

    IdeaType.CATALOG_OPTIONALITY: IdeaProfile(
        idea_type=IdeaType.CATALOG_OPTIONALITY,
        display_name="IP Catalog + Future Release Optionality",
        setup_description=(
            "Company owns a valuable IP catalog generating steady 'trough' revenue, "
            "plus a forthcoming release with massive but uncertain upside. "
            "The trough value (catalog without release) provides a floor. "
            "The release (game launch, film, drug approval) is the call option. "
            "Buy when: catalog value + net cash > current stock price. "
            "Then you get the option for free."
        ),
        catalyst="Product launch, pre-order surge, platform deal, licensing announcement",
        time_horizon="1-3 years",
        key_metrics=[
            "Net cash / market cap > 15%",
            "Catalog royalties / licensing: steady, recurring, defensible",
            "Next release: confirmed in production with timeline",
            "Buy price ≤ (net cash + catalog NPV) = you pay 0 for the option",
        ],
        red_flags=[
            "Studio/company in financial stress (can't finish the product)",
            "Franchise fatigue (sequel to bad-reviewed prior release)",
            "Long delay history (Duke Nukem Forever problem)",
        ],
        historical_examples=[
            "CD Projekt (CDR, WSE): PLN 1.4bn net cash + Cyberpunk catalog + Witcher 4 (2027)",
            "Paradox Interactive between major releases",
            "Mid-cap pharma with marketed drug + Phase 3 candidate",
        ],
        hf_style="Long-only growth/value, Sector specialist",
        return_profile="Slow appreciation during trough; explosive gain around launch",
        optionality=0.70,
    ),
}


# ────────────────────────────────────────────────────────────────────────
# Screening questions to identify idea type
# ────────────────────────────────────────────────────────────────────────

SCREENING_QUESTIONS = {
    "Q1: Is there analyst coverage?": {
        "No (0 analysts)": [IdeaType.MICRO_CAP_NEGLECT, IdeaType.SOTP_DISCOUNT],
        "Yes (≥1 analyst)": [],
    },
    "Q2: Is there a corporate event catalyst?": {
        "Parent M&A / forced sale": [IdeaType.PARENT_DISPOSITION],
        "Spin-off (recent)": [IdeaType.HOLDING_COMPANY_ORPHAN],
        "Announced M&A (company is target)": [IdeaType.MERGER_ARBITRAGE],
        "Insider cluster buy (ESPI)": [IdeaType.INSIDER_CLUSTER],
        "None yet": [],
    },
    "Q3: Is there a structural demand tailwind?": {
        "Defense / NATO": [IdeaType.DEFENSE_REARMAMENT],
        "Government infrastructure": [IdeaType.PIPELINE_CERTAINTY],
        "Regulation creates market": [IdeaType.REGULATORY_WINDFALL],
        "Post-conflict rebuild": [IdeaType.RECONSTRUCTION_OPTION],
        "No specific tailwind": [],
    },
    "Q4: Is there a geopolitical / macro binary?": {
        "War / sanctions / conflict": [IdeaType.GEOPOLITICAL_RESOLUTION],
        "Exchange upgrade (MSCI/FTSE)": [IdeaType.FRONTIER_MARKET_RECLASSIFICATION],
        "None": [],
    },
    "Q5: Is cheapness explained by forced selling?": {
        "Index deletion / forced sale": [IdeaType.INDEX_FORCED_SELLING],
        "Parent distress": [IdeaType.PARENT_DISPOSITION],
        "Frozen stake (sanctions)": [IdeaType.SANCTIONS_FROZEN_OVERHANG],
        "No forced seller": [],
    },
    "Q6: Is there a legal / liability overhang?": {
        "CHF mortgages (Polish bank)": [IdeaType.CHF_RESOLUTION],
        "Litigation / regulatory penalty": [],
        "No overhang": [],
    },
}


def identify_idea_types(
    has_analyst_coverage: bool,
    market_cap_m_eur: float,
    institutional_pct: float,
    has_parent_under_pressure: bool,
    has_frozen_stake: bool,
    defense_revenue_pct: float,
    has_government_pipeline: bool,
    has_sotp_discount: bool,
    has_ip_catalog: bool,
    has_insider_cluster: bool,
    chf_exposure: bool,
    in_conflict_zone: bool,
) -> list:
    """
    Identify which IdeaType(s) apply to a company based on key characteristics.
    Returns list of (IdeaType, confidence_score) tuples.
    """
    candidates = []

    if not has_analyst_coverage and market_cap_m_eur < 150 and institutional_pct < 10:
        candidates.append((IdeaType.MICRO_CAP_NEGLECT, 0.90))

    if has_sotp_discount:
        candidates.append((IdeaType.SOTP_DISCOUNT, 0.85))

    if has_insider_cluster:
        candidates.append((IdeaType.INSIDER_CLUSTER, 0.80))

    if defense_revenue_pct > 50:
        candidates.append((IdeaType.DEFENSE_REARMAMENT, 0.85))

    if has_parent_under_pressure:
        candidates.append((IdeaType.PARENT_DISPOSITION, 0.70))

    if has_frozen_stake:
        candidates.append((IdeaType.SANCTIONS_FROZEN_OVERHANG, 0.90))

    if has_government_pipeline:
        candidates.append((IdeaType.PIPELINE_CERTAINTY, 0.80))

    if has_ip_catalog:
        candidates.append((IdeaType.CATALOG_OPTIONALITY, 0.75))

    if chf_exposure:
        candidates.append((IdeaType.CHF_RESOLUTION, 0.70))

    if in_conflict_zone:
        candidates.append((IdeaType.GEOPOLITICAL_RESOLUTION, 0.60))

    # Sort by confidence
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates


def print_idea_type_report(idea_type: IdeaType):
    profile = IDEA_PROFILES.get(idea_type)
    if not profile:
        print(f"  No profile found for {idea_type}")
        return

    sep  = "═" * 76
    thin = "─" * 76
    print(f"\n{sep}")
    print(f"  IDEA TYPE: {profile.display_name}")
    print(sep)
    print(f"\n  Setup   : {profile.setup_description[:120]}...")
    print(f"  Catalyst: {profile.catalyst[:100]}...")
    print(f"  Horizon : {profile.time_horizon}")
    print(f"  HF style: {profile.hf_style}")
    print(f"  Optionality (binary dependence): {profile.optionality:.0%}")
    print(f"\n  Key metrics to find:")
    for m in profile.key_metrics:
        print(f"    • {m}")
    print(f"\n  Red flags:")
    for f_ in profile.red_flags:
        print(f"    ✗ {f_}")
    print(f"\n  Historical examples:")
    for e in profile.historical_examples:
        print(f"    → {e}")
    print(sep)
