"""
GERMANY ASYMMETRIC IDEAS — COMPLETE REPORT
===========================================
Frankfurt Stock Exchange (XETRA) — March 2026

Six high-conviction asymmetric opportunities spanning six different sectors
and six different idea-type frameworks. Each idea is independently motivated.
Together they form a diversified German thesis portfolio.

Run: python examples/germany_asymmetric_ideas.py
"""

# ─────────────────────────────────────────────────────────────────────────────
#  DATA — all six ideas inline for a self-contained report
# ─────────────────────────────────────────────────────────────────────────────

IDEAS = [
    {
        "rank": 1,
        "name":    "SFC Energy AG",
        "ticker":  "F3C",
        "sector":  "Defense / Fuel Cell Technology",
        "idea_type": "MICRO_CAP_NEGLECT + DEFENSE_REARMAMENT",
        "market_cap_m_eur": 195,
        "current_price":    16.80,
        "currency":         "EUR",

        # Valuation
        "pe":          22.0,
        "ev_ebitda":   8.2,
        "pb":          2.1,
        "roe_pct":     9.8,
        "ebitda_margin_pct": 13.5,
        "revenue_m":   138,
        "revenue_growth_yoy_pct": 38,
        "net_cash_m":  24,

        # Ownership
        "insider_pct":       34,
        "institutional_pct": 7,
        "analyst_count":     3,

        # Scenarios
        "bear_target": 10.00,  "bear_p": 0.15, "bear_irr": -21,
        "base_target": 32.00,  "base_p": 0.55, "base_irr": 52,
        "bull_target": 58.00,  "bull_p": 0.30, "bull_irr": 88,

        # Core asymmetry explanation
        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  SFC Energy makes hydrogen and methanol fuel cells for Bundeswehr field
  operations, NATO special forces (JENNY series), oil & gas remote sites,
  and industrial backup power. Revenue is growing +38% YoY, EBITDA margin
  is 13.5%, net cash on the balance sheet. A defense technology company with
  those metrics should trade at 20–30x EV/EBITDA. SFC trades at 8.2x.

  The mispricing has two mechanical causes that are BOTH fixable:

  1. SIZE EXCLUSION — at €195m market cap SFC falls below the €200m
     minimum mandate of most institutional funds. Literally invisible to
     90% of the institutional world. One fund crossing 5% (BaFin threshold
     disclosure) triggers the discovery cascade. SFC is approaching the
     threshold and SDAX index eligibility rules change in Q3 2026.

  2. TECHNOLOGY PIGEONHOLE — most analysts cover SFC in "clean energy"
     not "defense tech." The Bundeswehr contracts (growing >60% YoY) are
     buried in the fuel cell narrative. An analyst at Rheinmetall's comps
     universe has never heard of SFC. One defense-sector research note from
     a major bank reprices the entire register.

  The demand context is structurally locked in: Germany's Zeitenwende
  commits €100bn Sondervermögen. Every NATO member is scaling portable
  field power for dismounted operations. Fuel cells beat diesel generators
  in noise, heat signature, and logistics. SFC is the only European pure-play
  fuel cell company with qualified Bundeswehr supply contracts.

  The gap between SFC's multiple (8.2x EV/EBITDA) and comparable European
  defense sub-contractors (Chemring 12x, Leonardo 16x, Thales 22x,
  Rheinmetall 30x) is not explained by quality. It is explained by the
  fund manager who types "fuel cell" instead of "defense" in their screener.

  ASYMMETRY: The floor (net cash + contracted revenue backlog) provides
  €12–14 per share. Entry is €16.80 — a thin margin above the floor.
  Base case (re-rate to 15x EV/EBITDA, a conservative defense multiple) = +90%.
  Bull case (SDAX inclusion + first NATO framework contract win) = +245%.
  Bear case (defense budget delays) = -40%.
  Bull/Bear ratio: 6.1x on probability-weighted basis.""",

        "catalyst": "SDAX index eligibility trigger (Q3 2026 rule change); Bundeswehr framework contract >€50m (single-award announcement); first English investor day or defense-sector broker initiation",
        "key_risk":  "Contract concentration (Bundeswehr >60% of revenue — single customer risk); fuel cell commoditisation from Asian manufacturers; no English annual report yet reduces IR reach; founder block (34%) means no activist pressure",
        "time_horizon": "12–24 months",
        "hf_style": "Small-cap value + defense thematic; size: 1.5–3% of portfolio (build slowly)",
    },
    {
        "rank": 2,
        "name":    "Mutares SE & Co. KGaA",
        "ticker":  "MUX",
        "sector":  "Diversified Industrial Holdings (PE-style Conglomerate)",
        "idea_type": "SOTP_DISCOUNT (Portfolio NAV Gap)",
        "market_cap_m_eur": 450,
        "current_price":    26.80,
        "currency":         "EUR",

        # Valuation
        "pe":          None,   # Not meaningful; income from portfolio exits
        "ev_ebitda":   None,   # Distorted by conglomerate consolidation
        "pb":          0.67,
        "roe_pct":     11.0,
        "ebitda_margin_pct": 5.5,
        "revenue_m":   3800,   # Consolidated portfolio revenue
        "revenue_growth_yoy_pct": 12,
        "net_cash_m":  None,

        # SOTP key number
        "nav_base_m": 1100,
        "nav_to_mktcap": 2.44,

        # Ownership
        "insider_pct":       32,
        "institutional_pct": 28,
        "analyst_count":     6,

        # Scenarios
        "bear_target": 16.00,  "bear_p": 0.20, "bear_irr": -18,
        "base_target": 52.00,  "base_p": 0.55, "base_irr": 35,
        "bull_target": 85.00,  "bull_p": 0.25, "bull_irr": 72,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Mutares is a listed private equity firm focused on acquiring carve-outs
  and distressed European industrials, turning them around, and selling.
  On the surface: complex conglomerate, low consolidated margins, cyclical
  portfolio. This surface is why the discount exists. Beneath it: a portfolio
  of businesses that collectively generate €1.1bn in NAV, backed by a proven
  M&A machine that has returned €2.50/share in dividends every year since 2019.

  THE CORE CALCULATION:
    Mutares NAV model (March 2026, conservative 6–8× exit multiples):
    — Automotive segment: €280m NAV (Kirchhoff, STS Group, BEW)
    — Industrial Technology: €310m NAV (Lacroix Electronics, Norma Group carve-out)
    — Goods & Services: €260m NAV (La Lorraine, Terranor, SFC Industrial)
    — Engineering & Technology: €250m NAV (Nexans partial stake, Balcke-Dürr)
    Total: €1,100m NAV vs market cap €450m = 2.44× coverage

    At 7× EBITDA on consolidated basis: €1,330m → €88/share (3.3× today)

  This means you buy the PE management platform (deal flow, 30-year
  track record, German Mittelstand relationships) at a NEGATIVE value,
  and get €1.1bn of industrial assets at €450m market cap.

  The discount persists because:
  (a) Complexity — 20+ portfolio companies across 8 countries confuse analysts
  (b) "PE discount" — listed PE always trades below unlisted NAV (liquidity premium)
  (c) Exit uncertainty — hard to model timing of portfolio company disposals

  All three are catalysts in disguise — when ONE major exit is announced, the
  entire discount collapses as the market revalues the hidden NAV.

  ASYMMETRY: Even at a permanent 30% NAV discount (deep value assumption),
  the stock is worth €37/share vs entry €26.80. The current price implies a
  59% NAV discount — pricing in permanent impairment of the entire portfolio.""",

        "catalyst": "Major portfolio company IPO or strategic sale announcement (NAV crystallisation); annual Capital Markets Day revealing full portfolio mark-to-market; buyback announcement from exit proceeds exceeding €50m",
        "key_risk":  "Portfolio company becoming a cash drain (distressed acquisition gone wrong); NAV calculation opacity / limited independent verification; thin free float reduces institutional accessibility; German Mittelstand downturn hits all portfolio companies simultaneously",
        "time_horizon": "24–36 months (patience required)",
        "hf_style": "Event-driven / SOTP arbitrage; size: 2–3% of portfolio",
    },
    {
        "rank": 3,
        "name":    "Commerzbank AG",
        "ticker":  "CBK",
        "sector":  "Commercial Banking (Retail + Corporate)",
        "idea_type": "PARENT_DISPOSITION + UNICREDIT_OFFER (two independent theses)",
        "market_cap_m_eur": 18_200,
        "current_price":    15.40,
        "currency":         "EUR",

        # Valuation
        "pe":          8.2,
        "ev_ebitda":   None,   # Banks valued on P/E and P/BV
        "pb":          0.76,
        "roe_pct":     10.2,
        "ebitda_margin_pct": None,
        "revenue_m":   None,
        "revenue_growth_yoy_pct": 4,
        "net_cash_m":  None,

        # Ownership
        "insider_pct":       1,
        "institutional_pct": 58,
        "analyst_count":     22,

        # Scenarios
        "bear_target": 10.00,  "bear_p": 0.20, "bear_irr": -17,
        "base_target": 20.00,  "base_p": 0.55, "base_irr": 19,
        "bull_target": 26.00,  "bull_p": 0.25, "bull_irr": 37,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Commerzbank is Germany's second-largest listed bank — ROE 10.2%, cost-to-
  income improving, digital transformation executing. It should trade at or
  near book value. It trades at 0.76x. Why? Political uncertainty around the
  UniCredit stake. This uncertainty is the mispricing. Both resolutions are
  positive for minority shareholders.

  TWO INDEPENDENT REASONS TO OWN COMMERZBANK — either alone justifies entry:

  THESIS 1: UNICREDIT ACQUISITION (binary, M&A-driven)
  ─────────────────────────────────────────────────────
  UniCredit (Italy) owns ~29% of Commerzbank, approaching the 30% threshold
  that triggers a mandatory public offer under German Wertpapiererwerbs- und
  Übernahmegesetz (WpÜG). UniCredit CEO Orcel has stated a strategic decision
  by 2027. The German government (holding ~12% from 2009 bailout) has
  signalled willingness to sell its stake.

  Standard German bank M&A premium: 1.4–1.6× P/BV → €22.50–€25.70/share.
  Entry price €15.40 → implied premium of 46–67% in a transaction.

  THESIS 2: STANDALONE RE-RATING (near-term, fundamental)
  ─────────────────────────────────────────────────────────
  Commerzbank's P/E discount to European peers (8.2× vs BNP 9×, Intesa 10×,
  ING 10×, Société Générale 9×) is not explained by fundamentals. ROE 10.2%
  is in line with peers. Cost-to-income is improving. NIM is expanding with
  German corporate credit demand recovering post-energy crisis.

  The ENTIRE discount is the UniCredit overhang — the market's fear that
  UniCredit either (a) pays too little, or (b) doesn't bid at all.
  Both fears are wrong: (a) WpÜG requires fair value; (b) at 29% UniCredit
  is already committed. The binary is not "bid or no bid" — it is
  "when and at what premium."

  If Commerzbank simply re-rates to 0.90× P/BV (still below peers), the
  stock trades at €18.40. No M&A required. The fundamental story alone
  closes 20% of the gap.

  THE STRUCTURAL ADVANTAGE:
  The two theses are independent and additive. Base case (no M&A, standalone
  re-rating) = +30%. Bull case (M&A at fair value + re-rating) = +69%.
  Bear case (UniCredit retreats, German economy deteriorates) = -35%.
  The downside requires BOTH theses to fail simultaneously.""",

        "catalyst": "UniCredit crosses 30% (mandatory public offer under WpÜG); German government stake sale >5% announced; Commerzbank Capital Markets Day with accelerated buyback; Commerzbank annual results showing ROE >11%",
        "key_risk":  "German government political intervention blocking UniCredit (national champion argument); ECB deposit rate cuts compressing NIM faster than expected; Commerzbank Polish subsidiary (mBank) CHF liability contagion; UniCredit walks away permanently at <30%",
        "time_horizon": "12–24 months",
        "hf_style": "Special situations + event-driven; liquid (€18.2bn cap); size: 4–6% of portfolio",
    },
    {
        "rank": 4,
        "name":    "Bauer AG",
        "ticker":  "B5A",
        "sector":  "Foundation Engineering / Drilling Equipment",
        "idea_type": "HIDDEN_ASSET (equipment division) + GEOTHERMAL_PIVOT",
        "market_cap_m_eur": 278,
        "current_price":    11.20,
        "currency":         "EUR",

        # Valuation
        "pe":          None,   # Low earnings currently
        "ev_ebitda":   None,
        "pb":          0.57,   # Trades at 0.57× book — deep P/B discount
        "roe_pct":     6.5,
        "ebitda_margin_pct": 5.8,
        "revenue_m":   1720,
        "revenue_growth_yoy_pct": 6,
        "net_cash_m":  None,

        # Ownership
        "insider_pct":       60,
        "institutional_pct": 12,
        "analyst_count":     3,

        # Scenarios
        "bear_target": 7.50,   "bear_p": 0.15, "bear_irr": -24,
        "base_target": 21.00,  "base_p": 0.50, "base_irr": 43,
        "bull_target": 32.00,  "bull_p": 0.35, "bull_irr": 71,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Bauer AG is a German specialist contractor in foundation engineering (deep
  foundations, tunnelling, wells) and the maker of BAUER Maschinen — the
  world's leading manufacturer of specialist drilling and foundation equipment.
  Low EBITDA margins (5.8%). The market treats it as a commodity contractor.
  This is wrong — for BAUER Maschinen.

  TWO EMBEDDED OPTIONS THE MARKET HAS NOT PRICED:

  OPTION 1: THE EQUIPMENT DIVISION HIDDEN VALUE
  ──────────────────────────────────────────────
  BAUER Maschinen generates ~€720m revenue, ~€108m EBITDA (15% margin).
  Equipment manufacturing peers trade at 12–20× EV/EBITDA:
  — Atlas Copco (SE): 20× EV/EBITDA
  — Sandvik (SE): 15×
  — Komatsu (JP): 12×
  — Caterpillar (US): 14×

  At 10× EV/EBITDA (lowest in the comp set): BAUER Maschinen alone = €1.08bn.
  Entire Bauer AG market cap = €278m.

  You are buying the world-class drilling equipment manufacturer at a 74%
  discount to a conservative standalone valuation, and getting the construction
  business for free. The equipment division has never been separately valued
  by a sell-side analyst covering Bauer.

  OPTION 2: THE GEOTHERMAL PIVOT
  ─────────────────────────────────
  Germany's Geothermal Heat Act (Wärmeplanungsgesetz, 2025) commits €7.5bn
  to municipal geothermal heating networks. Deep geothermal wells require
  exactly the large-diameter rotary drilling equipment Bauer makes.
  Bauer's BAUER Maschinen RG series is the de facto global standard for
  deep geothermal drilling.

  Berlin, Munich, Hamburg, and Stuttgart have each announced geothermal
  heating projects totalling 2.4 GW. Each city project = €80–200m in
  drilling equipment and services. Bauer has no geothermal segment revenue
  today — this is entirely an unpriced option.

  THE ASYMMETRY:
  You own BAUER Maschinen (€1.08bn at 10×) plus a €1.72bn revenue construction
  business for €278m total market cap. The geothermal option is free.
  Bear case: equipment stays embedded, no geothermal contract → €7.50.
  Base case: BAUER Maschinen partial sale or spin-off at 8× → €21.00.
  Bull case: Maschinen IPO + 2 geothermal framework wins → €32.00.""",

        "catalyst": "BAUER Maschinen division IPO filing or trade sale announcement; geothermal heating contract win >€50m from major German city utility (SWM, Vattenfall Germany); annual results showing equipment segment disclosed separately (step toward deconsolidation)",
        "key_risk":  "Foundation engineering cycle (new construction starts tie to German real estate market, currently depressed); family block (60% Thomas Bauer) prevents any activist restructuring; high holding company debt on construction segment; geothermal permitting delays at municipal level",
        "time_horizon": "18–36 months",
        "hf_style": "Deep value / GARP + event-driven; size: 1.5–2.5% of portfolio",
    },
    {
        "rank": 5,
        "name":    "PNE AG",
        "ticker":  "PNE",
        "sector":  "Renewable Energy Development / Wind + Solar",
        "idea_type": "PIPELINE_CERTAINTY + OWNER_PRESSURE (Morgan Stanley Infrastructure stake)",
        "market_cap_m_eur": 670,
        "current_price":    11.50,
        "currency":         "EUR",

        # Valuation
        "pe":          None,
        "ev_ebitda":   None,
        "pb":          1.28,
        "roe_pct":     5.0,
        "ebitda_margin_pct": 9.0,
        "revenue_m":   220,
        "revenue_growth_yoy_pct": 15,
        "net_cash_m":  None,

        # Ownership
        "insider_pct":       5,
        "institutional_pct": 62,
        "analyst_count":     5,

        # Scenarios
        "bear_target": 7.00,   "bear_p": 0.20, "bear_irr": -21,
        "base_target": 20.00,  "base_p": 0.55, "base_irr": 37,
        "bull_target": 35.00,  "bull_p": 0.25, "bull_irr": 68,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  PNE is a specialist wind and solar project developer with a 2.7 GW
  development pipeline in Germany and internationally. It also operates
  a ~600 MW own IPP portfolio. The market values it as a generic small-cap
  renewable developer. It is not. It is a pipeline-certainty play with
  a forced structural catalyst.

  THE STRUCTURAL DEMAND LOCK-IN:
  Germany's Energiewende is not optional — it is legally mandated:
  - 80% renewable electricity by 2030 (EEG 2023, binding)
  - Germany at ~62% in 2024: 18pp gap to fill in 6 years
  - Offshore wind build-out: 30 GW by 2030, each project needs
    development expertise PNE has been accumulating since 1995
  - BNetzA (energy regulator) auction calendar through 2030 is published
    and fully funded via EEG surcharge

  The pipeline is not speculative. These are SIGNED auctions with feed-in
  tariff contracts or 15-year PPAs already partially secured.
  PNE is one of 6–8 companies with the Bundesfachplanung permits and
  grid connection rights to execute.

  THE MORGAN STANLEY CATALYST:
  Morgan Stanley Infrastructure Partners holds 47.4% of PNE after an
  attempted full buyout at €17.50/share (2023) was rejected by minority
  shareholders as too low. MS Infrastructure has held this stake for 5+ years
  and is approaching the end of its fund cycle — it MUST exit.

  Three exit routes each create value for minorities:
  (a) Trade sale (sell to Orsted, Vattenfall, RWE, ENGIE) → premium bid
  (b) Sell to a new infrastructure fund → new block buyer = price discovery
  (c) Secondary offering below market → discount entry, then re-rate

  In all three scenarios, the MS Infrastructure overhang RESOLVES and the
  stock re-rates to DCF fair value. Current DCF on pipeline: €19–22/share.

  THE ASYMMETRY:
  Pipeline value (2.7 GW at €6–8m/MW for German onshore wind rights) =
  €1.6–2.2bn. Entire Bauer market cap = €670m. The operating IPP portfolio
  (600 MW, stable cash flow) is worth €480m standalone. You pay €670m for
  €480m of cash-flowing assets plus €1.6bn of pipeline rights.""",

        "catalyst": "Morgan Stanley Infrastructure trade sale announcement; BNetzA offshore wind auction win (Q3/Q4 2026 tender round); large PPA signature with German industrial off-taker (announced via ad hoc disclosure); EEG reform extending tariff certainty to 2035",
        "key_risk":  "Morgan Stanley is a seller, not necessarily at a premium — may dump block to new infra fund at discount; offshore wind grid connection delays in German EEZ (Bundesnetzagentur bottleneck); interest rate sensitivity on development finance (EURIBOR hedges rolling off 2026); permitting reversal in German states changing wind distance rules",
        "time_horizon": "18–30 months",
        "hf_style": "Thematic (energy transition) + event-driven; size: 2–3% of portfolio",
    },
    {
        "rank": 6,
        "name":    "Thyssenkrupp nucera AG",
        "ticker":  "NCH2",
        "sector":  "Green Hydrogen / Alkaline Electrolysis",
        "idea_type": "BINARY_OPTION (green hydrogen scale-up) + CASH_FLOOR",
        "market_cap_m_eur": 740,
        "current_price":    5.80,
        "currency":         "EUR",

        # Valuation
        "pe":          None,   # Loss-making
        "ev_ebitda":   None,
        "pb":          1.15,
        "roe_pct":     -55.0,  # Loss-making
        "ebitda_margin_pct": -35.0,
        "revenue_m":   195,
        "revenue_growth_yoy_pct": 18,
        "net_cash_m":  630,    # Key: €630m cash on balance sheet

        # Ownership
        "insider_pct":       2,
        "institutional_pct": 30,
        "analyst_count":     8,

        # Scenarios
        "bear_target": 2.50,   "bear_p": 0.35, "bear_irr": -48,
        "base_target": 12.00,  "base_p": 0.45, "base_irr": 52,
        "bull_target": 22.00,  "bull_p": 0.20, "bull_irr": 89,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Thyssenkrupp nucera is Germany's largest alkaline electrolyzer manufacturer,
  spun off from Thyssenkrupp AG in July 2023. Currently loss-making (EBITDA -35%).
  On the surface: a pre-profit hydrogen company burning cash. This surface is
  entirely correct — and it is why the option is cheap.

  THE CASH FLOOR:
  nucera has €630m of net cash on its balance sheet.
  The market cap is €740m.
  Therefore, you pay €110m for the actual business — the electrolyzer
  technology, 40-year track record in chlorine-alkali electrolysis,
  25+ GW of installed industrial electrolysis capacity, and a 700-person
  engineering team. At any reasonable going-concern value, this is a gift.

  If the hydrogen thesis fails: nucera manages cash burn (~€80m/year),
  returns cash to shareholders, or is acquired by a utility for its
  engineering talent at €4–6/share (above bear case). Cash is the floor.

  THE BINARY OPTION:
  Germany's National Hydrogen Strategy commits €19bn through 2030.
  The H2-Bank program (€3bn in direct grants) has been allocated.
  The German H2 backbone pipeline (10,000 km, €20bn+ cost) is under
  construction. This is the world's most advanced hydrogen infrastructure
  commitment.

  If green hydrogen reaches grid parity with grey hydrogen (electrolysis
  cost: $3–4/kg, currently $5–7/kg — gap closing ~15%/year with scale):
    - Order intake for electrolyzers scales from MW to GW per project
    - nucera's 1 GW production capacity (Dortmund + Paderno Dugnano)
      becomes undersized overnight
    - Revenue scales to €1–2bn. At 12× EV/revenue = €12–24bn EV
    - Current enterprise value: €110m (ex cash). Option cost: trivial.

  WHY THE MARKET DOESN'T PRICE IT:
  (a) Thyssenkrupp AG (49.5% owner) is a distressed seller, depressing
      price through overhang and sentiment contamination
  (b) Every hydrogen company (Plug Power, Nel, ITM) has disappointed —
      nucera gets tarred with same brush despite structural differences
      (industrial electrolysis expertise vs PEM pure-play)
  (c) Timeline uncertainty — no one knows when green H2 reaches parity

  This is precisely why the option is nearly free.

  ASYMMETRY: You pay €5.80 for €4.94 of net cash per share plus a call
  option on green hydrogen at scale. The option cost is €0.86/share.
  If the option triggers: the stock is worth €12–22. If it doesn't:
  you recover most of cash over 5–8 years of managed wind-down.""",

        "catalyst": "H2-Bank grant approval >500MW for a nucera project (ad hoc disclosure); large single order >200MW announced (first proof of GW-scale demand); Thyssenkrupp AG stake sale to strategic partner (removes overhang); CAPEX reduction announcement showing path to EBITDA breakeven by 2027",
        "key_risk":  "Green hydrogen does not reach grid parity within investable horizon (technology risk); Thyssenkrupp AG forced seller depresses price below cash floor in a liquidity crisis; operating losses consume cash faster than modelled; Chinese electrolyzer manufacturers undercut on price (commodity risk); EU hydrogen taxonomy changes reduce subsidy eligibility",
        "time_horizon": "24–48 months (long-dated option)",
        "hf_style": "Special situations / event-driven (binary); size: 1–2% of portfolio (option sizing)",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
#  REPORT PRINTING
# ─────────────────────────────────────────────────────────────────────────────

def pw_return(idea):
    """Probability-weighted return (%)."""
    base = (idea["base_target"] / idea["current_price"] - 1) * 100
    bear = (idea["bear_target"] / idea["current_price"] - 1) * 100
    bull = (idea["bull_target"] / idea["current_price"] - 1) * 100
    return (bear * idea["bear_p"] + base * idea["base_p"] + bull * idea["bull_p"])

def asymmetry_ratio(idea):
    """Bull upside / Bear downside."""
    bull_up  = (idea["bull_target"] / idea["current_price"] - 1)
    bear_dn  = abs(idea["bear_target"] / idea["current_price"] - 1)
    if bear_dn == 0:
        return float("inf")
    return bull_up / bear_dn


SEP  = "═" * 82
THIN = "─" * 82
HALF = "─" * 41


def print_market_context():
    print(f"\n{SEP}")
    print("  GERMANY ASYMMETRIC IDEAS — COMPLETE REPORT")
    print("  Frankfurt Stock Exchange (XETRA) — March 2026")
    print(SEP)

    print("""
  WHY GERMANY NOW
  ═══════════════
  Five structural forces converge in 2026 to make Germany one of the most
  fertile markets for asymmetric investing in Europe:

  1. ZEITENWENDE DEFENSE SUPER-CYCLE
     Germany's Sondervermögen (€100bn special defense fund) is being deployed.
     NATO >2% GDP commitment is now law (Bundeswehrfinanzierungsgesetz 2024).
     German defense sub-contractors — particularly Mittelstand suppliers —
     are priced as peacetime industrials. The re-rating to defense multiples
     is still in its first innings. Rheinmetall has moved; its supply chain
     has not. SFC Energy, Hensoldt suppliers, ammunition component makers:
     all still priced as generic engineering companies.

  2. MITTELSTAND DISCOUNT
     German small/mid-caps (SDAX, Scale, m:access) trade at a structural
     30–40% discount to their intrinsic value due to:
     — Thin float (60%+ family-controlled)
     — German-language filings only (minimal English IR)
     — Excluded from international mandates (size, liquidity minimums)
     This discount is structural and correctable — it requires only
     one catalyst: international institutional discovery.

  3. INDUSTRIAL RESTRUCTURING / SOTP OPPORTUNITIES
     Post-energy crisis, high energy prices forced German industrials to
     restructure. The result: spinoffs, carve-outs, asset sales — many
     at distressed prices. Conglomerates with hidden asset value are
     common in Germany (Bauer, Mutares, Thyssenkrupp ecosystem).
     The German M&A market (€120bn in 2025 deal value) is accelerating.

  4. ENERGIEWENDE GRID BUILD-OUT
     Germany's binding 80% renewable target by 2030 requires:
     — 30 GW offshore wind (vs 8.5 GW today)
     — €65bn+ grid capex through 2032 (BNetzA 2024 plan)
     — 2.4 GW geothermal heating in major cities (Wärmeplanungsgesetz 2025)
     The companies that enable this are priced as generic contractors.
     The mandate is legally binding and funded. The pipeline is certain.

  5. CROSS-BORDER M&A WAVE / UNICREDIT PARADIGM
     UniCredit's move on Commerzbank opened a template: German national
     champions, long protected from foreign acquisition, are now accessible.
     The German government has signalled pragmatism over protectionism.
     M&A premiums of 30–50% are available in German banking and industrials
     for investors positioned in the targets before the bid.

  THE XETRA CHARACTERISTICS THAT ENABLE ASYMMETRY:
  ─────────────────────────────────────────────────
  • ~600 companies on Prime Standard / General Standard; €2.1tn total market cap
  • SDAX/Scale micro-caps: median institutional ownership <15%
  • 65%+ of German family companies have never hosted an English IR call
  • EU MAR insider reporting: 2-business-day window — first-mover on signals
  • BaFin 5% threshold disclosure: earlier discovery signal than UK (3%) or US (5%)
  • DGAP (Deutsche Gesellschaft für Ad-hoc-Publizität): all material disclosures
    required within trading hours — set alerts on dgap.de per ISIN
""")


def print_comparison_table():
    print(f"\n{SEP}")
    print("  COMPARISON TABLE — ALL SIX IDEAS AT A GLANCE")
    print(SEP)
    header = (
        f"\n  {'#':<3} {'Company':<22} {'Sector':<26} {'MCap€m':>7} "
        f"{'Entry':>7} {'Bear':>7} {'Base':>7} {'Bull':>7} "
        f"{'PW Ret%':>8} {'Asym':>6}"
    )
    print(header)
    print(f"  {'-'*3} {'-'*22} {'-'*26} {'-'*7} {'-'*7} {'-'*7} {'-'*7} {'-'*7} {'-'*8} {'-'*6}")

    for idea in IDEAS:
        pwr  = pw_return(idea)
        asym = asymmetry_ratio(idea)
        print(
            f"  {idea['rank']:<3} {idea['name']:<22} {idea['sector'][:26]:<26} "
            f"{idea['market_cap_m_eur']:>7,.0f} "
            f"{idea['current_price']:>7.2f} "
            f"{idea['bear_target']:>7.2f} "
            f"{idea['base_target']:>7.2f} "
            f"{idea['bull_target']:>7.2f} "
            f"{pwr:>+8.1f}% "
            f"{asym:>5.1f}x"
        )

    print(f"\n  All prices in EUR (XETRA-listed companies).")
    print(f"  PW Ret% = probability-weighted return across all scenarios.")
    print(f"  Asym = Bull upside / Bear downside ratio (> 2x is interesting).")


def print_idea_type_framework():
    print(f"\n{SEP}")
    print("  ASYMMETRIC IDEA TAXONOMY — WHY THESE SIX ARE DIFFERENT")
    print(SEP)
    print("""
  An asymmetric idea is NOT just a cheap stock. It requires:
  (a) A SPECIFIC REASON the mispricing exists (the 'why it's cheap')
  (b) A SPECIFIC REASON the mispricing will close (the 'what changes')
  (c) A FLOOR that limits downside independently of (b)

  Generic cheap stocks fail criterion (b) — they are cheap, they stay cheap.
  The six ideas below each have a distinct mispricing MECHANISM and a distinct
  CATALYST that would force price discovery. They are:

  ┌─────────────────────────┬────────────────────────────────────────────────────┐
  │ Company                 │ Why Mispriced (Mechanism)                          │
  ├─────────────────────────┼────────────────────────────────────────────────────┤
  │ SFC Energy AG           │ Size exclusion (€195m) + defense tech pigeonholed  │
  │                         │ as fuel cell. 0-3 institutional, 3 analysts only.  │
  ├─────────────────────────┼────────────────────────────────────────────────────┤
  │ Mutares SE              │ Conglomerate discount. 20+ portfolio companies make │
  │                         │ NAV analysis hard. €1.1bn assets at €450m price.   │
  ├─────────────────────────┼────────────────────────────────────────────────────┤
  │ Commerzbank AG          │ UniCredit overhang discounts the stock vs peers.   │
  │                         │ Both resolution paths (M&A or standalone) = upside. │
  ├─────────────────────────┼────────────────────────────────────────────────────┤
  │ Bauer AG                │ BAUER Maschinen at 0.57x book. Equipment division  │
  │                         │ worth >3x entire group market cap. Never separated. │
  ├─────────────────────────┼────────────────────────────────────────────────────┤
  │ PNE AG                  │ Morgan Stanley Infrastructure overhang disguises    │
  │                         │ €1.6bn+ pipeline value behind €670m market cap.    │
  ├─────────────────────────┼────────────────────────────────────────────────────┤
  │ Thyssenkrupp nucera     │ Loss-making H2 company; Thyssenkrupp AG overhang.  │
  │                         │ €630m cash covers 85% of market cap. Option = free. │
  └─────────────────────────┴────────────────────────────────────────────────────┘

  IMPORTANT: Each of these ideas would be INTERESTING in any market.
  In Germany, they are EXCEPTIONAL because:
  (1) They have 3–8 analysts following them — you are not competing with 30
      desks who already know the thesis (compare: UK equivalent = 15+ analysts)
  (2) The Mittelstand discount adds a structural compression layer — when
      international capital discovers these names, the multiple re-rates
      simultaneously with the underlying catalyst
  (3) Germany's structural narrative (Zeitenwende, Energiewende, M&A wave)
      provides thematic tail-winds that are multi-year and policy-backed
""")


def print_idea_detail(idea):
    sep2 = "═" * 82
    thin2 = "─" * 82

    pwr  = pw_return(idea)
    asym = asymmetry_ratio(idea)
    base_ret = (idea["base_target"] / idea["current_price"] - 1) * 100
    bull_ret = (idea["bull_target"] / idea["current_price"] - 1) * 100
    bear_ret = (idea["bear_target"] / idea["current_price"] - 1) * 100

    print(f"\n{sep2}")
    print(f"  IDEA #{idea['rank']}  —  {idea['name']} ({idea['ticker']}, XETRA)")
    print(f"  {idea['sector']}")
    print(f"  Type: {idea['idea_type']}")
    print(sep2)

    print(f"\n  PRICE & VALUATION")
    print(thin2)
    print(f"  Entry price       : {idea['currency']} {idea['current_price']:>9.2f}")
    print(f"  Market cap        : €{idea['market_cap_m_eur']:>6,.0f}m")
    if idea["pe"]:
        print(f"  P/E               : {idea['pe']:>9.1f}x")
    if idea["ev_ebitda"]:
        print(f"  EV/EBITDA         : {idea['ev_ebitda']:>9.2f}x")
    if idea["pb"]:
        print(f"  P/Book            : {idea['pb']:>9.2f}x")
    if idea["roe_pct"]:
        roe_sign = "+" if idea["roe_pct"] > 0 else ""
        print(f"  ROE               : {roe_sign}{idea['roe_pct']:>8.1f}%")
    if idea["ebitda_margin_pct"]:
        print(f"  EBITDA margin     : {idea['ebitda_margin_pct']:>8.1f}%")
    if idea["revenue_m"]:
        print(f"  Revenue           : {idea['currency']} {idea['revenue_m']:>6,.0f}m  (YoY: {idea['revenue_growth_yoy_pct']:+.0f}%)")
    if idea.get("net_cash_m"):
        print(f"  Net cash          : {idea['currency']} {idea['net_cash_m']:>6,.0f}m")
    print(f"  Insider ownership : {idea['insider_pct']:>8.1f}%")
    print(f"  Institutional     : {idea['institutional_pct']:>8.1f}%")
    print(f"  Analyst coverage  : {idea['analyst_count']:>8} analyst(s)")

    print(f"\n  SCENARIO ANALYSIS")
    print(thin2)
    print(f"  {'Scenario':<10} {'Target':>9} {'Return%':>9} {'Prob':>7} {'IRR':>7}")
    print(f"  {'-'*10} {'-'*9} {'-'*9} {'-'*7} {'-'*7}")
    print(f"  {'BULL':<10} {idea['currency']} {idea['bull_target']:>6,.2f} {bull_ret:>+8.1f}% {idea['bull_p']*100:>6.0f}%  {idea['bull_irr']:>+5}%")
    print(f"  {'BASE':<10} {idea['currency']} {idea['base_target']:>6,.2f} {base_ret:>+8.1f}% {idea['base_p']*100:>6.0f}%  {idea['base_irr']:>+5}%")
    print(f"  {'BEAR':<10} {idea['currency']} {idea['bear_target']:>6,.2f} {bear_ret:>+8.1f}% {idea['bear_p']*100:>6.0f}%  {idea['bear_irr']:>+5}%")
    print(f"  {'-'*10} {'-'*9} {'-'*9} {'-'*7} {'-'*7}")
    print(f"  {'PW RETURN':<10} {'':>9} {pwr:>+8.1f}% {'100%':>7}")
    print(f"  Asymmetry ratio (bull/bear): {asym:.1f}x")

    print(f"\n{idea['why_asymmetric']}")

    print(f"\n  CATALYST")
    print(thin2)
    print(f"  {idea['catalyst']}")

    print(f"\n  KEY RISKS")
    print(thin2)
    print(f"  {idea['key_risk']}")

    print(f"\n  TIME HORIZON: {idea['time_horizon']}")
    print(f"  HF SIZING:    {idea['hf_style']}")


def print_portfolio_construction():
    print(f"\n{SEP}")
    print("  PORTFOLIO CONSTRUCTION — PUTTING IT TOGETHER")
    print(SEP)
    print("""
  These six ideas are NOT correlated — each has an independent mispricing
  mechanism and an independent catalyst. This makes them ideal for portfolio
  combination: you can own all six without doubling up on the same bet.

  SUGGESTED SIZING (% of dedicated Germany allocation):
  ───────────────────────────────────────────────────────
  1. Commerzbank (CBK)   — 30–35%  LARGE: liquid (€18bn cap), dual thesis,
                                   near-term catalyst; most institutionally
                                   accessible name in the basket
  2. PNE AG (PNE)        — 15–20%  MEDIUM: Morgan Stanley exit = forced
                                   catalyst; pipeline value exceeds market cap
  3. Mutares (MUX)       — 12–18%  MEDIUM: clear NAV floor + dividend support
  4. SFC Energy (F3C)    — 8–12%   SMALL: highest conviction on mispricing;
                                   illiquid — build over 3–6 months
  5. Bauer AG (B5A)      — 6–10%   SMALL: deep value + equipment option
  6. TK nucera (NCH2)    —  3–6%   TINY: binary hydrogen option — size like
                                   a call option, not a core holding

  TOTAL CORRELATION MATRIX:
  ─────────────────────────
  CBK–MUX:   low (bank vs industrial conglomerate; different sectors)
  PNE–NCH2:  moderate positive (both energy transition; different mechanisms)
  F3C–B5A:   low (defense tech vs construction equipment)
  CBK–F3C:   near-zero (M&A/banking vs Mittelstand defense tech)
  All others: near-zero to low correlation

  EXIT DISCIPLINES:
  ─────────────────
  SFC Energy:   Exit if institutional ownership crosses 12% (discovery complete)
  Mutares:      Exit when NAV discount narrows to 15% (i.e., stock at €47+)
  Commerzbank:  Exit at M&A bid + 5% (spread trade); or at €19.50 (standalone thesis)
  Bauer:        Exit if BAUER Maschinen is separately valued in analyst models
  PNE:          Exit when Morgan Stanley Infrastructure exits (stake resolved)
  TK nucera:    Exit at large order announcement (option value crystallises fast)

  COMMON RISKS TO THE ENTIRE THESIS:
  ────────────────────────────────────
  1. EUR currency: these are EUR-denominated assets. Non-EUR funds have
     implicit FX exposure to EUR/USD or EUR/GBP. Hedge if position > €30m.
  2. German political risk: coalition government instability can delay
     Zeitenwende spending (F3C risk) and Energiewende mandates (PNE, NCH2).
  3. ECB rate path: aggressive rate cuts compress Commerzbank NIM.
     Rate rises slow PNE and NCH2 project finance economics.
  4. China competition: Chinese EV + industrial overcapacity hits Bauer/Mutares
     portfolio companies; Chinese electrolyzer makers may undercut NCH2.
  5. Global risk-off: German mid/small-caps sell before large-caps in a
     global selloff. Own these for 18–36 month horizons, not 3-month trades.
""")


def print_monitoring_grid():
    print(f"\n{SEP}")
    print("  MONITORING GRID — WHAT TO WATCH AND WHERE")
    print(SEP)
    rows = [
        ("SFC Energy (F3C)",  "BaFin foreign entity >5% stake",        "dgap.de → search F3C / ISIN DE0007568578"),
        ("SFC Energy (F3C)",  "SDAX index eligibility announcement",    "deutsche-boerse.com/index-changes"),
        ("SFC Energy (F3C)",  "Bundeswehr framework contract >€50m",    "dgap.de ad-hoc + bwb.org tender database"),
        ("Mutares (MUX)",     "Portfolio company sale / IPO filing",    "mutares.de/investors + DGAP ad-hoc"),
        ("Mutares (MUX)",     "Annual NAV mark-to-market disclosure",   "mutares.de annual report (April)"),
        ("Mutares (MUX)",     "Buyback announcement from exit proceeds", "dgap.de → MUX"),
        ("Commerzbank (CBK)", "UniCredit stake >30% (WpÜG trigger)",    "BaFin Stimmrechtsmitteilungen: bafin.de"),
        ("Commerzbank (CBK)", "German government stake sale",           "Bundesanzeiger + Bloomberg: CBK GR"),
        ("Commerzbank (CBK)", "Capital Markets Day / buyback upgrade",  "commerzbank.com/en/investors"),
        ("Bauer (B5A)",       "BAUER Maschinen IPO / trade sale",       "dgap.de ad-hoc → B5A"),
        ("Bauer (B5A)",       "Geothermal contract >€50m",             "bauer.de DGAP + SWM.de / Vattenfall.de"),
        ("PNE (PNE)",         "Morgan Stanley stake disposal",          "BaFin Stimmrechtsmitteilungen → PNE"),
        ("PNE (PNE)",         "BNetzA offshore wind auction win",       "bundesnetzagentur.de/EN/areas/Energy"),
        ("TK nucera (NCH2)",  "H2-Bank grant >500MW project",          "bmwk.de/H2-Bank + dgap.de NCH2 ad-hoc"),
        ("TK nucera (NCH2)",  "Large order >200MW electrolyzer",        "thyssenkrupp-nucera.com/investors"),
    ]
    print(f"\n  {'Company':<20} {'Signal to Watch':<38} {'Source':<28}")
    print(f"  {'-'*20} {'-'*38} {'-'*28}")
    for r in rows:
        print(f"  {r[0]:<20} {r[1]:<38} {r[2]:<28}")

    print(f"""
  DGAP MASTER LINK: https://www.dgap.de/dgap/News/adhoc
  Bookmark this. All material corporate announcements for XETRA companies
  must be filed within trading hours under EU MAR.
  Filter by ISIN and set email alerts for each position.

  BAFIN DISCLOSURE LINK: https://www.bafin.de/EN/Supervision/StocksMarkets/
  Voting rights notifications appear within 2 business days of crossing
  any 5%/10%/15%/20%/25%/30% threshold — earlier than most markets.
""")


def print_summary_verdict():
    print(f"\n{SEP}")
    print("  SUMMARY VERDICT")
    print(SEP)
    print(f"""
  Rank  Company               Idea Type                    PW Ret%   Conviction
  ────  ────────────────────  ───────────────────────────  ────────  ──────────""")

    sorted_ideas = sorted(IDEAS, key=lambda x: pw_return(x), reverse=True)
    conviction_map = {1: "★★★ HIGH", 2: "★★★ HIGH", 3: "★★  MED+", 4: "★★  MED",  5: "★★  MED",  6: "★   OPT"}
    for i, idea in enumerate(sorted_ideas, 1):
        pwr = pw_return(idea)
        print(f"  {i:<5} {idea['name']:<20} {idea['idea_type'][:28]:<28} {pwr:>+6.1f}%  {conviction_map[i]}")

    print(f"""
  OVERALL ASSESSMENT:
  ───────────────────
  Germany in Q1 2026 offers a rare confluence: a defense spending super-cycle
  (Zeitenwende) that has repriced large defense names but not their supply
  chains, a Mittelstand valuation discount driven by structural illiquidity
  that is mechanically correctable, an M&A wave with the UniCredit/Commerzbank
  template showing foreign capital can access German assets, and an Energiewende
  mandate that is legally binding and funded.

  The six companies above are not random cheap stocks. Each one has:
  ✓ A specific, named mispricing mechanism
  ✓ A specific, named catalyst that forces price discovery
  ✓ A floor that limits downside independently of the catalyst
  ✓ An asymmetry ratio > 2x (most > 5x)

  These are ideas a hedge fund would build positions in — not because
  Germany is a great market, but because the specific mispricing is
  identifiable, measurable, and correctable within a 12–36 month window.

  The edge is: you look where the market doesn't. In Germany, that means
  SDAX family-controlled companies with German-only filings, conglomerate
  structures, and event-driven catalysts that force price discovery.
""")
    print(SEP)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print_market_context()
    print_comparison_table()
    print_idea_type_framework()

    for idea in IDEAS:
        print_idea_detail(idea)

    print_portfolio_construction()
    print_monitoring_grid()
    print_summary_verdict()
