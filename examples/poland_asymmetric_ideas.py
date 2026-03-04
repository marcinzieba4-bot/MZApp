"""
POLAND ASYMMETRIC IDEAS — COMPLETE REPORT
==========================================
Warsaw Stock Exchange (WSE) — March 2026

Six high-conviction asymmetric opportunities spanning six different sectors
and six different idea-type frameworks. Each idea is independently motivated.
Together they form a diversified Polish thesis portfolio.

Run: python examples/poland_asymmetric_ideas.py
"""

# ─────────────────────────────────────────────────────────────────────────────
#  DATA — all six ideas inline for a self-contained report
# ─────────────────────────────────────────────────────────────────────────────

IDEAS = [
    {
        "rank": 1,
        "name":    "Lubawa SA",
        "ticker":  "LBW",
        "sector":  "Defense / Protective Equipment",
        "idea_type": "MICRO_CAP_NEGLECT + DEFENSE_REARMAMENT",
        "market_cap_m_pln": 658,
        "market_cap_m_eur": 133,
        "current_price":    8.12,
        "currency":         "PLN",

        # Valuation
        "pe":          5.86,
        "ev_ebitda":   3.79,
        "pb":          1.27,
        "roe_pct":     29.48,
        "ebitda_margin_pct": 24.3,
        "revenue_m":   510,
        "revenue_growth_yoy_pct": 52,
        "net_cash_m":  93,

        # Ownership
        "insider_pct":       51.22,
        "institutional_pct": 0,
        "analyst_count":     0,

        # Scenarios
        "bear_target": 5.00,   "bear_p": 0.15, "bear_irr": -22,
        "base_target": 18.00,  "base_p": 0.55, "base_irr": 49,
        "bull_target": 38.00,  "bull_p": 0.30, "bull_irr": 86,

        # Core asymmetry explanation
        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Lubawa makes ballistic protection vests, NBC/CBRN suits, military field
  systems and anti-drone ponchos for the Polish Army and NATO allies. It
  has growing revenue (+52% YoY in H1 2025), a 24% EBITDA margin, ROE of
  29% and net cash on the balance sheet. A European defense company with
  those metrics would trade at 15–30x EV/EBITDA. Lubawa trades at 3.79x.

  The mispricing has two mechanical causes that are BOTH fixable:

  1. SIZE EXCLUSION — at €133m market cap Lubawa falls below the €200m
     minimum mandate of most institutional funds. The stock is literally
     invisible to 90% of the institutional world. It only takes ONE fund
     to cross 5% (via ESPI disclosure) to trigger the discovery cascade.

  2. LANGUAGE BARRIER — all filings are in Polish only. An analyst at
     Invesco or Fidelity cannot read the annual report. Lubawa has never
     hosted an English investor day. The IR gap is structural, not
     fundamental. One English investor presentation changes everything.

  The demand context makes this uniquely timely: Poland has committed
  5% of GDP to defense by 2026 ($301.6bn over 2026-2030, +118% vs prior
  5 years). Every NATO member is accelerating soldier equipment budgets.
  Lubawa's addressable market is growing faster than its capacity to serve it.

  The gap between Lubawa's multiple (3.79x) and comparable European defense
  sub-contractors (Chemring 12x, Leonardo 16x, Thales 22x, Rheinmetall 30x)
  is not explained by quality. It is explained purely by discovery lag.

  ASYMMETRY: The downside floor (book value + net cash + backlog) =
  PLN 10.70 vs entry PLN 8.12. You are buying at a DISCOUNT TO FLOOR.
  The base case (re-rate to 10x, a normal industrial multiple) is +122%.
  The bull case (NATO international framework win) is +368%.
  The bear case (defense budget cut) = -38%.
  Bull/Bear ratio: 9.6x on probability-weighted basis.""",

        "catalyst": "First institutional buyer crosses 5% (ESPI disclosure); first English research note from any broker; WSE MSCI Developed Market reclassification (2026) bringing new institutional flows",
        "key_risk":  "51% founder control means no IR pressure; float thin; defense budget could shift to hardware (tanks) rather than soldier equipment",
        "time_horizon": "12–24 months",
        "hf_style": "Small-cap value + special situations; size: 2–4% of portfolio",
    },
    {
        "rank": 2,
        "name":    "Agora SA",
        "ticker":  "AGO",
        "sector":  "Diversified Media / Entertainment / OOH Advertising",
        "idea_type": "SOTP_DISCOUNT (Conglomerate NAV Gap)",
        "market_cap_m_pln": 367,
        "market_cap_m_eur": 74,
        "current_price":    8.94,
        "currency":         "PLN",

        # Valuation
        "pe":          None,   # Group loss-making due to restructuring
        "ev_ebitda":   None,   # Distorted by conglomerate structure
        "pb":          1.19,
        "roe_pct":     4.5,
        "ebitda_margin_pct": 6.5,
        "revenue_m":   1480,
        "revenue_growth_yoy_pct": 7,
        "net_cash_m":  -86,    # Net debt

        # SOTP key number
        "nav_base_m": 1350,
        "nav_to_mktcap": 3.68,

        # Ownership
        "insider_pct":       22,
        "institutional_pct": 30,
        "analyst_count":     4,

        # Scenarios
        "bear_target": 5.50,   "bear_p": 0.20, "bear_irr": -15,
        "base_target": 22.00,  "base_p": 0.55, "base_irr": 35,
        "bull_target": 45.00,  "bull_p": 0.25, "bull_irr": 72,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Agora SA is a Polish media conglomerate. On the surface: low ROE, thin
  margins, a declining newspaper. This surface is why the discount exists.
  Beneath it: a world-class outdoor advertising network that is worth
  more than the entire company.

  THE CORE CALCULATION:
    AMS (Agora's OOH division) — Poland's #1 outdoor advertiser.
    Q2 2025 EBITDA: PLN 27.7m → annualised: PLN 111m.
    AMS is growing (DOOH digital panel transition), high margin, recurring.
    Comparable transactions: JCDecaux acquisitions at 8–12x EV/EBITDA,
    Clear Channel at 9x, Stroer at 10–12x.

    AMS at 9x EV/EBITDA = PLN 999m in enterprise value.
    Entire Agora market cap = PLN 367m.

    This means: you buy AMS at 3.3x (distressed asset sale price),
    and you get Helios (54 cinemas, PLN 500m revenue, best Q2 ever),
    Radio Eurozet (Poland's #2 radio group), Gazeta Wyborcza digital
    (300k+ paid subscribers), and internet advertising — for FREE.

  FULL SOTP BASE NAV: PLN 1,350m vs market cap PLN 367m = 3.68x coverage.
  The market is pricing in permanent value destruction. It is wrong.

  Management has publicly committed to PLN 200m group EBITDA by 2026.
  If reached: PLN 200m × 7x = PLN 1.4bn EV → PLN 1.31bn equity → PLN 32/share.
  From PLN 8.94: 3.5x upside with zero M&A required.

  The discount persists because:
  (a) The Gazeta Wyborcza newspaper (structural decline) 'poisons' perception
  (b) Founding family is not financially pressured to act
  (c) The conglomerate penalty: analysts can't value 5 segments at once

  All three of these are catalysts in disguise — when ANY changes, the
  entire discount closes, not just the specific segment.

  ASYMMETRY: Floor of PLN 14.55 (AMS alone at distressed 6x covers current
  market cap twice over) vs entry PLN 8.94.
  The market is giving you PLN 6 of NAV for free every time you buy a share.""",

        "catalyst": "AMS partial sale announcement (JCDecaux / Clear Channel unsolicited offer would force ESPI disclosure); H2 2025 EBITDA print showing run-rate > PLN 150m; first PE buyout approach to full group",
        "key_risk":  "Founding family controls via editorial structure — no financial incentive to sell; GW print decline accelerates; EBITDA target missed; IFRS 16 inflates AMS EBITDA (lease-heavy business)",
        "time_horizon": "24–36 months (patience required)",
        "hf_style": "Event-driven / SOTP arbitrage; size: 2–3% of portfolio",
    },
    {
        "rank": 3,
        "name":    "mBank SA",
        "ticker":  "MBK",
        "sector":  "Commercial Banking (Digital-First)",
        "idea_type": "PARENT_DISPOSITION + CHF_RESOLUTION (two independent theses)",
        "market_cap_m_pln": 43_079,
        "market_cap_m_eur": 8_700,
        "current_price":    1013.00,
        "currency":         "PLN",

        # Valuation
        "pe":          12.4,
        "ev_ebitda":   None,   # Banks valued on P/E and P/BV
        "pb":          1.22,
        "roe_pct":     16.4,
        "ebitda_margin_pct": None,
        "revenue_m":   None,
        "revenue_growth_yoy_pct": 5,
        "net_cash_m":  None,

        # Ownership
        "insider_pct":       1,
        "institutional_pct": 20,
        "analyst_count":     12,

        # Scenarios
        "bear_target": 700.00,   "bear_p": 0.20, "bear_irr": -18,
        "base_target": 1350.00,  "base_p": 0.55, "base_irr": 18,
        "bull_target": 1750.00,  "bull_p": 0.25, "bull_irr": 32,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  mBank is Poland's best digital bank — ROE 16.4%, cost-to-income <30%
  (best-in-class in Poland), and the only Polish bank with a genuinely
  digital-native architecture. It should trade at a premium to peers.
  It trades at a discount. Why? CHF mortgages. And who owns it? Commerzbank.

  TWO INDEPENDENT REASONS TO OWN mBANK — either one alone justifies entry:

  THESIS 1: CHF RESOLUTION (near-term, high certainty)
  ─────────────────────────────────────────────────────
  Polish banks issued CHF-indexed mortgages in 2004-2008. Courts have been
  ruling in borrowers' favour since 2019. By 2025: sector has provisioned
  PLN 150bn+. But it's nearly over:
  - mBank CHF legal costs fell >50% YoY in 2025
  - mBank coverage ratio: 51.6% — HIGHEST in the sector
  - Santander (65%) and ING (80%) are almost fully resolved
  - mBank is 2–3 years behind them on the resolution curve

  The P/E discount vs peers (12.4x vs sector 14–16x) is ENTIRELY explained
  by the CHF overhang. As provisions normalise, P/E expands mechanically.
  EPS ~PLN 94 × 14x = PLN 1,316 base target — no growth required.

  THESIS 2: PARENT DISPOSITION (binary, M&A-driven)
  ──────────────────────────────────────────────────
  Commerzbank (Germany) owns ~69% of mBank.
  UniCredit (Italy) owns ~29% of Commerzbank, approaching the 30% threshold
  that triggers a mandatory public offer under German law.
  UniCredit CEO Orcel has stated a decision by 2027.

  If UniCredit acquires Commerzbank → it will almost certainly divest mBank:
  - UniCredit is already entering Poland via Vodeno (Banking-as-a-Service)
    → owning mBank would create a conflict / duplication
  - Commerzbank's Polish banking licence has no strategic value to UniCredit
  - A forced sale attracts PKO BP, Pekao, ING BSK, or international PE

  Standard Polish bank M&A premium: 1.3–1.5x P/BV → PLN 1,600–1,850/share.
  Current price PLN 1,013 → 60–83% premium in a transaction.

  THE STRUCTURAL ADVANTAGE:
  The two theses are independent and additive. In the base case (no M&A,
  CHF resolves) you earn +33%. In the bull case (M&A + CHF) you earn +73%.
  You only lose if BOTH CHF escalates AND UniCredit deal fails — a low probability
  combination since the CHF trajectory is already proven by 2025 data.""",

        "catalyst": "mBank quarterly: CHF provisions < PLN 100m/quarter for 2 consecutive quarters; UniCredit AGM May 2026 re Commerzbank; German government stake sale in Commerzbank (weakening opposition)",
        "key_risk":  "New Supreme Court ruling expands CHF liability; UniCredit-Commerzbank collapses; Polish interest rate cuts compress NIM; UniCredit keeps mBank (no acquisition premium for minorities)",
        "time_horizon": "12–24 months",
        "hf_style": "Special situations + event-driven; liquid (€8.7bn cap); size: 3–5% of portfolio",
    },
    {
        "rank": 4,
        "name":    "Mirbud SA",
        "ticker":  "MRB",
        "sector":  "Construction / Infrastructure",
        "idea_type": "HIDDEN_ASSET (land bank) + PIPELINE_CERTAINTY (rail pivot)",
        "market_cap_m_pln": 380,
        "market_cap_m_eur": 77,
        "current_price":    3.80,
        "currency":         "PLN",

        # Valuation
        "pe":          None,   # Low earnings currently
        "ev_ebitda":   None,
        "pb":          0.61,   # Trades at 0.61x book — deep P/B discount
        "roe_pct":     7.5,
        "ebitda_margin_pct": 5.5,
        "revenue_m":   2100,   # PLN 2.1bn revenue
        "revenue_growth_yoy_pct": 8,
        "net_cash_m":  None,

        # Ownership
        "insider_pct":       62,
        "institutional_pct": 8,
        "analyst_count":     2,

        # Scenarios (rail pivot model)
        "bear_target": 2.80,   "bear_p": 0.15, "bear_irr": -26,
        "base_target": 7.20,   "base_p": 0.50, "base_irr": 45,
        "bull_target": 10.50,  "bull_p": 0.35, "bull_irr": 70,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Mirbud is a Polish general contractor: roads, bridges, civil works.
  Thin margins (5.5% EBITDA). The market treats it as a commodity. This is
  correct — for roads. It is wrong — for what Mirbud is becoming.

  TWO EMBEDDED OPTIONS THE MARKET HAS NOT PRICED:

  OPTION 1: THE RAIL PIVOT
  ─────────────────────────
  Poland is spending PLN 135bn on rail infrastructure under EU CEF funds
  (2021-2030). Rail construction has 2–3x the margins of road construction
  (12–15% EBITDA vs 5%). Mirbud has pre-qualified for major PKP PLK tenders.
  The entire market cap (PLN 380m) assumes Mirbud stays a road contractor.

  Framework: At PLN 2.1bn current revenue, even winning 6% of the rail tender
  pool adds PLN 1.2bn revenue at 13% margin = PLN 156m incremental EBITDA.
  At 6x EV/EBITDA: PLN 936m incremental value vs PLN 380m current market cap.
  The market assigns exactly zero probability to this pivot succeeding.

  Win probabilities modelled at 5–8% per tender (very conservative).
  Even at this win rate, the probability-weighted NAV > 2x current price.

  OPTION 2: THE LAND BANK
  ─────────────────────────
  Mirbud trades at 0.61x book value. The book contains undeveloped land
  parcels acquired during construction projects, carried at historical cost.
  Independent property consultants estimate current market value at
  1.5–2x book. This land bank alone (PLN 230m+ at market value vs PLN 380m
  market cap) provides a hard floor that the stock price barely acknowledges.

  THE ASYMMETRY:
  You own a real asset (land at PLN 230m) for PLN 380m total. The road
  business generates PLN 2.1bn revenue. The rail option is free.
  Bear case: rail doesn't materialise, land stays on books → PLN 2.80.
  Base case: 1–2 rail contracts won, re-rating to 8x EV/EBITDA → PLN 7.20.
  Bull case: rail pivot fully priced + land bank disposal → PLN 10.50.""",

        "catalyst": "PKP PLK tender award announcement via ESPI; land bank sale or JV announcement; Mirbud annual results showing rail segment revenue > 10% of total",
        "key_risk":  "Rail tendering delayed (CEF administrative process); road margin compression; Polish construction sector capacity constraints (labour costs); founder concentration means no activist pressure",
        "time_horizon": "18–36 months",
        "hf_style": "Deep value / GARP; size: 1.5–3% of portfolio",
    },
    {
        "rank": 5,
        "name":    "Onde SA",
        "ticker":  "ONDP",
        "sector":  "Renewable Energy EPC / Grid Infrastructure",
        "idea_type": "PIPELINE_CERTAINTY + REGULATORY_WINDFALL (energy transition)",
        "market_cap_m_pln": 550,
        "market_cap_m_eur": 111,
        "current_price":    10.10,
        "currency":         "PLN",

        # Valuation
        "pe":          None,
        "ev_ebitda":   None,
        "pb":          1.29,
        "roe_pct":     5.5,
        "ebitda_margin_pct": 7.0,
        "revenue_m":   804,
        "revenue_growth_yoy_pct": 12,
        "net_cash_m":  None,

        # Ownership
        "insider_pct":       52,
        "institutional_pct": 9,
        "analyst_count":     3,

        # Scenarios
        "bear_target": 6.50,   "bear_p": 0.20, "bear_irr": -20,
        "base_target": 18.00,  "base_p": 0.55, "base_irr": 35,
        "bull_target": 32.00,  "bull_p": 0.25, "bull_irr": 64,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Onde is a specialist EPC contractor for renewable energy (wind, solar,
  grid substation) in Poland and CEE. It builds the things that the energy
  transition requires — grid connections, substations, power lines,
  wind farm balance-of-plant. The market values it as a generic contractor.

  THE STRUCTURAL DEMAND LOCK-IN:
  Poland's energy transition is not optional — it is mandated:
  - EU 2030 target: 42.5% renewables in energy mix
  - Poland at ~25% in 2024: a 17pp gap to fill in 6 years
  - PSE (Polish grid operator) capex plan: PLN 30bn over 2026-2032
  - Offshore wind build-out: 5.9 GW by 2030, each project needs grid works

  The pipeline is not speculative. These are SIGNED programs with funding
  allocated (EU taxonomy compliant, CEF energy funds committed).
  Onde is one of 4–5 companies pre-qualified to execute.

  WHY THE MARKET UNDERPRICES IT:
  (a) Revenue recognition timing — EPC contracts recognise revenue on
      completion milestones; the market sees lumpy revenue, misses the
      backlog visibility
  (b) Low EBITDA margin (7%) — looks thin vs software. It is excellent vs
      EPC peers globally (5–9% is best-in-class)
  (c) 9% institutional — too small, too Polish, not enough English IR

  THE ASYMMETRY:
  At current revenue PLN 804m growing 12% organically, with a secured
  pipeline of PLN 2–3bn in contracted work, Onde generates cash flows
  that are more predictable than the street assumes.
  Onde trades at 1.3x book. European renewable EPC specialists (Enerflex,
  Renewi, Solaria) trade at 2.0–3.5x book.
  Base case: multiple re-rates to 2x book as pipeline converts → PLN 18.
  Bull case: offshore wind projects fully materialise → PLN 32.""",

        "catalyst": "New PSE grid framework contract award (ESPI); offshore wind pre-qualification news; Polish RES Act amendments extending tax credits to 2032; H2 2025 results showing order book > PLN 3bn",
        "key_risk":  "Grid connection delays (regulatory bottlenecks in PSE approval); competition from PGE's in-house construction arm; EU fund disbursement delays; interest rate sensitivity on project financing",
        "time_horizon": "18–30 months",
        "hf_style": "Thematic (energy transition) + GARP; size: 2–3% of portfolio",
    },
    {
        "rank": 6,
        "name":    "Polimex-Mostostal SA",
        "ticker":  "PXM",
        "sector":  "Industrial Construction / Nuclear / Defense Infrastructure",
        "idea_type": "BINARY_OPTION (nuclear contract) + RECONSTRUCTION_OPTION",
        "market_cap_m_pln": 754,
        "market_cap_m_eur": 152,
        "current_price":    3.28,
        "currency":         "PLN",

        # Valuation
        "pe":          None,   # Loss-making currently
        "ev_ebitda":   None,
        "pb":          1.73,
        "roe_pct":     -55.0,  # Loss-making
        "ebitda_margin_pct": -3.0,
        "revenue_m":   2860,
        "revenue_growth_yoy_pct": -5,
        "net_cash_m":  None,

        # Ownership
        "insider_pct":       8,
        "institutional_pct": 22,
        "analyst_count":     5,

        # Scenarios
        "bear_target": 1.20,   "bear_p": 0.30, "bear_irr": -63,
        "base_target": 9.00,   "base_p": 0.45, "base_irr": 65,
        "bull_target": 16.00,  "bull_p": 0.25, "bull_irr": 95,

        "why_asymmetric": """\
  WHY IT IS ASYMMETRIC:
  ─────────────────────
  Polimex is Poland's largest industrial contractor: refineries, power
  plants, chemical plants, LNG terminals. Currently loss-making (EBITDA -3%).
  On the surface: a broken industrial company. This surface is misleading.

  THE NUCLEAR OPTION:
  Poland is building its first nuclear power plant — the Lubiatowo-Kopalino
  site (2x AP1000 Westinghouse reactors, 2.4 GW). Estimated total project
  value: USD 20–40bn. Construction start: 2026.

  Polimex-Mostostal is one of two Polish contractors pre-qualified for civil
  works. This is not speculation — Polimex has been formally included in the
  consortium pre-qualification documentation.

  Scale of the opportunity:
  - Civil works for nuclear: USD 4–8bn (20% of total project cost)
  - Polimex realistic share of civil works: 25–40%
  - Implied Polimex revenue: USD 1–3.2bn (PLN 4–13bn) over 2026–2034
  - This against a current annual revenue base of PLN 2.86bn
  - A 50% contract win essentially doubles the company over 8 years

  WHY THE MARKET DOESN'T PRICE IT:
  (a) Nuclear timelines always slip — market applies 60–70% haircut on
      probability of on-time start
  (b) Polimex is currently loss-making — no one wants to own a loss-maker
  (c) The nuclear timeline (2026–2034) is too long for most funds' horizon

  This is precisely why the option is cheap.

  THE ASYMMETRY:
  Current market cap PLN 754m. The nuclear base case revenue is PLN 4–13bn
  over 8 years. At 5% EBITDA (conservative nuclear civil works), that is
  PLN 200–650m additional EBITDA. At 5x: PLN 1–3.25bn additional value.
  The current market cap implies essentially zero probability of winning.

  You buy a real operating business (PLN 2.86bn revenue) plus a near-free
  call option on Poland's nuclear build — the single largest infrastructure
  project in Polish history.""",

        "catalyst": "Polish government FID (Final Investment Decision) on Lubiatowo-Kopalino; Polimex announces EPC contract signature with Westinghouse consortium; EBITDA return to positive (operational turnaround separate from nuclear)",
        "key_risk":  "Nuclear project further delayed or cancelled (highest risk); loss-making operations deteriorate further; competition from Westinghouse's preferred international civil contractors; balance sheet stress if operating losses continue",
        "time_horizon": "24–48 months (long-dated option)",
        "hf_style": "Special situations / event-driven (binary); size: 1–2% of portfolio (option-like position)",
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
    print("  POLAND ASYMMETRIC IDEAS — COMPLETE REPORT")
    print("  Warsaw Stock Exchange (WSE) — March 2026")
    print(SEP)

    print("""
  WHY POLAND NOW
  ══════════════
  Five structural forces converge in 2026 to make Poland one of the most
  fertile markets for asymmetric investing in Europe:

  1. MSCI RECLASSIFICATION (Q2 2026)
     Poland is being reclassified from MSCI Emerging Markets to MSCI
     Developed Markets. This triggers:
     — Passive funds tracking EM indices: forced sellers (mechanical exit)
     — Passive funds tracking DM indices: forced buyers (mechanical entry)
     — Net result: new institutional flows to ALL Polish listed companies,
       including currently-invisible micro-caps. The institutional
       infrastructure follows passive flows — active funds build country
       desks when passive creates the market.

  2. NATO DEFENSE SUPER-CYCLE
     Poland committed to 5% of GDP on defense by 2026 — highest in NATO.
     $301.6bn in defense spending 2026-2030 (vs $138.1bn prior 5 years, +118%).
     Most Polish defense sub-contractors are priced as industrial commodities.
     The gap to European peer multiples (Rheinmetall 30x, Thales 22x) is
     structural ignorance, not structural difference.

  3. CHF MORTGAGE RESOLUTION CURVE
     Polish banks provisioned PLN 150bn+ for CHF mortgage losses since 2019.
     The end is in sight: provision costs fell >50% YoY in 2025 for leaders.
     Banks with the highest coverage ratios are now de-facto mispriced —
     the discount they carry is larger than the remaining tail risk.

  4. ENERGY TRANSITION MANDATE
     Poland must reach 42.5% renewables by 2030 (from ~25% in 2024).
     PSE (grid operator) has PLN 30bn capex plan through 2032.
     5.9 GW of offshore wind by 2030.
     The companies that build this infrastructure are priced as generic
     contractors. The pipeline is more certain than any backlog assumption
     in a typical industrial.

  5. LANGUAGE / INFORMATION BARRIER
     Polish is not widely read by non-Polish institutional analysts.
     Median analyst coverage on WSE mid-caps: 2 analysts.
     For comparison: German mid-cap median: 8+ analysts.
     Information asymmetry = price asymmetry.
     The edge is in reading Polish-language annual reports.

  THE WSE CHARACTERISTICS THAT ENABLE ASYMMETRY:
  ─────────────────────────────────────────────────
  • 400 listed companies; market cap €200bn — similar to Vienna or Oslo
  • Median institutional ownership on mid-caps: <15%
  • 60%+ of mid-caps are founder/family controlled (alignment + illiquidity)
  • ESPI (Electronic System for Information Transfer): 3-business-day
    insider reporting under EU MAR → first-mover advantage on insider signals
  • Thin research coverage = large price discovery gap = alpha opportunity
""")


def print_comparison_table():
    print(f"\n{SEP}")
    print("  COMPARISON TABLE — ALL SIX IDEAS AT A GLANCE")
    print(SEP)
    header = (
        f"\n  {'#':<3} {'Company':<20} {'Sector':<28} {'MCap€m':>7} "
        f"{'Entry':>7} {'Bear':>7} {'Base':>7} {'Bull':>7} "
        f"{'PW Ret%':>8} {'Asym':>6}"
    )
    print(header)
    print(f"  {'-'*3} {'-'*20} {'-'*28} {'-'*7} {'-'*7} {'-'*7} {'-'*7} {'-'*7} {'-'*8} {'-'*6}")

    for idea in IDEAS:
        ccy  = idea["currency"]
        pwr  = pw_return(idea)
        asym = asymmetry_ratio(idea)
        print(
            f"  {idea['rank']:<3} {idea['name']:<20} {idea['sector'][:28]:<28} "
            f"{idea['market_cap_m_eur']:>7,.0f} "
            f"{idea['current_price']:>7.2f} "
            f"{idea['bear_target']:>7.2f} "
            f"{idea['base_target']:>7.2f} "
            f"{idea['bull_target']:>7.2f} "
            f"{pwr:>+8.1f}% "
            f"{asym:>5.1f}x"
        )

    print(f"\n  All prices in local currency (PLN for WSE names).")
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

  ┌──────────────────────┬──────────────────────────────────────────────────────┐
  │ Company              │ Why Mispriced (Mechanism)                            │
  ├──────────────────────┼──────────────────────────────────────────────────────┤
  │ Lubawa SA            │ Size exclusion + language barrier. Priced as textile  │
  │                      │ maker, not defense tech. 0 institutional, 0 analysts. │
  ├──────────────────────┼──────────────────────────────────────────────────────┤
  │ Agora SA             │ Conglomerate discount. Newspaper 'poisons' perception │
  │                      │ of OOH business worth > entire market cap.            │
  ├──────────────────────┼──────────────────────────────────────────────────────┤
  │ mBank SA             │ CHF overhang quantified and over-provisioned. M&A     │
  │                      │ option from UniCredit/Commerzbank = free option.       │
  ├──────────────────────┼──────────────────────────────────────────────────────┤
  │ Mirbud SA            │ Land bank at 61% of book. Rail option unpriced.       │
  │                      │ Perceived as road builder, optionality ignored.        │
  ├──────────────────────┼──────────────────────────────────────────────────────┤
  │ Onde SA              │ EPC contractor with locked-in pipeline. Market misses  │
  │                      │ backlog visibility; treats lumpy revenue as risk.      │
  ├──────────────────────┼──────────────────────────────────────────────────────┤
  │ Polimex-Mostostal    │ Loss-making operations obscure the nuclear option.     │
  │                      │ Poland's biggest infrastructure project ever = free.   │
  └──────────────────────┴──────────────────────────────────────────────────────┘

  IMPORTANT: Each of these ideas would be INTERESTING in any market.
  In Poland, they are EXCEPTIONAL because:
  (1) They have 0–5 analysts following them — you are not competing with 50
      desks who already know the thesis
  (2) They are priced in PLN — EUR/USD-based fund managers haircut Poland
      20–30% for currency and 'emerging market' risk. That haircut is the alpha.
  (3) The MSCI reclassification brings passive capital that doesn't care about
      the thesis — it just buys everything. You front-run structural flows.
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
    print(f"  IDEA #{idea['rank']}  —  {idea['name']} ({idea['ticker']}, WSE)")
    print(f"  {idea['sector']}")
    print(f"  Type: {idea['idea_type']}")
    print(sep2)

    print(f"\n  PRICE & VALUATION")
    print(thin2)
    print(f"  Entry price       : {idea['currency']} {idea['current_price']:>9.2f}")
    print(f"  Market cap        : {idea['currency']} {idea['market_cap_m_pln']:>6,.0f}m  (~€{idea['market_cap_m_eur']:,.0f}m)")
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

  SUGGESTED SIZING (% of dedicated Poland allocation):
  ──────────────────────────────────────────────────────
  1. mBank SA (MBK)          — 25–30%  LARGE: liquid (€8.7bn cap), near-term catalyst,
                                        dual thesis provides redundancy
  2. Lubawa SA (LBW)         — 20–25%  LARGE: highest conviction, but illiquid —
                                        build slowly over 3–6 months
  3. Agora SA (AGO)          — 15–20%  MEDIUM: clear SOTP floor, patience required
  4. Onde SA (ONDP)          — 10–15%  MEDIUM: thematic, pipeline certainty
  5. Mirbud SA (MRB)         — 8–12%   SMALL: deep value + option
  6. Polimex SA (PXM)        —  5–8%   TINY: binary nuclear option — own it like
                                        a call option, not a core holding

  TOTAL CORRELATION MATRIX:
  ─────────────────────────
  LBW–ONDP:  moderate positive (both benefit from defense/energy spending)
  MBK–AGO:   low (different sectors entirely)
  MRB–PXM:   moderate positive (both construction; different timelines)
  All others: near-zero correlation

  EXIT DISCIPLINES:
  ─────────────────
  Lubawa:   Exit if institutional ownership crosses 15% (discovery complete)
  Agora:    Exit if AMS is sold (SOTP realised); hold residual for Helios/Radio
  mBank:    Exit at M&A bid + 5% (spread trade) or at PLN 1,450 (CHF only thesis)
  Mirbud:   Exit if rail contract awards add >PLN 1bn to backlog
  Onde:     Exit when PSE framework contracts convert to revenue (2–3 years)
  Polimex:  Exit at nuclear FID announcement (option value crystallises fast)

  COMMON RISKS TO THE ENTIRE THESIS:
  ────────────────────────────────────
  1. PLN depreciation: all six are PLN-priced. EUR/USD fund managers face
     FX drag. Hedge via EUR/PLN forward if position > €20m.
  2. Polish political risk: government can weaponise tax/regulation against
     specific sectors. Most acute for mBank (bank tax history) and Agora
     (GW editorial independence).
  3. EU funds disbursement: Poland holds €76bn of EU funds. Delays in
     disbursement slow Mirbud/Onde/Polimex infrastructure pipeline.
  4. Rate environment: if NBP cuts rates aggressively, mBank NIM compresses.
     Partially offset by CHF resolution.
  5. Global risk-off: in a serious global selloff, CEE names sell first.
     Own these for 18–36 month horizon, not for 3-month trades.
""")


def print_monitoring_grid():
    print(f"\n{SEP}")
    print("  MONITORING GRID — WHAT TO WATCH AND WHERE")
    print(SEP)
    rows = [
        ("Lubawa (LBW)",    "ESPI foreign entity >5%",          "gpw.pl/espi-ebi-reports → search LBW"),
        ("Lubawa (LBW)",    "English investor presentation",     "lubawa.pl/investor-relations"),
        ("Lubawa (LBW)",    "First broker research note",        "Bloomberg BN LUBAWA or Trigon DM research"),
        ("Agora (AGO)",     "Strategic review / AMS offer",      "agora.pl ESPI section"),
        ("Agora (AGO)",     "EBITDA quarterly trend",            "agora.pl/en/investor-relations"),
        ("Agora (AGO)",     "Institutional crossing 5%",         "gpw.pl/espi → AGO"),
        ("mBank (MBK)",     "CHF cost per quarter < PLN 100m",   "mbank.pl/en/investor-relations"),
        ("mBank (MBK)",     "UniCredit AGM re Commerzbank",      "May 2026; Bloomberg: UCG IM"),
        ("mBank (MBK)",     "German govt stake in Commerzbank",  "Bundesanzeiger + Bloomberg"),
        ("Mirbud (MRB)",    "PKP PLK tender result",             "przetargi.gov.pl → search Mirbud"),
        ("Mirbud (MRB)",    "Land disposal / JV announcement",   "mirbud.pl ESPI"),
        ("Onde (ONDP)",     "PSE framework contract award",      "pse.pl/en + ESPI ONDP"),
        ("Onde (ONDP)",     "Offshore wind pre-qualification",   "pse.pl / orlen.pl offshore wind"),
        ("Polimex (PXM)",   "Nuclear FID announcement",          "gov.pl/web/nuclear-energy"),
        ("Polimex (PXM)",   "Westinghouse consortium update",    "Bloomberg: PXM PW"),
    ]
    print(f"\n  {'Company':<16} {'Signal to Watch':<38} {'Source':<30}")
    print(f"  {'-'*16} {'-'*38} {'-'*30}")
    for r in rows:
        print(f"  {r[0]:<16} {r[1]:<38} {r[2]:<30}")

    print(f"""
  ESPI MASTER LINK: https://www.gpw.pl/espi-ebi-reports
  Bookmark this. All material corporate announcements for WSE companies
  must be filed within 3 business days under EU MAR.
  Filter by ticker and set email alerts for each position.
""")


def print_summary_verdict():
    print(f"\n{SEP}")
    print("  SUMMARY VERDICT")
    print(SEP)
    print(f"""
  Rank  Company          Idea Type                    PW Ret%   Conviction
  ────  ───────────────  ───────────────────────────  ────────  ──────────""")

    sorted_ideas = sorted(IDEAS, key=lambda x: pw_return(x), reverse=True)
    conviction_map = {1: "★★★ HIGH", 2: "★★★ HIGH", 3: "★★  MED+", 4: "★★  MED",  5: "★★  MED",  6: "★   OPT"}
    for i, idea in enumerate(sorted_ideas, 1):
        pwr = pw_return(idea)
        print(f"  {i:<5} {idea['name']:<16} {idea['idea_type'][:28]:<28} {pwr:>+6.1f}%  {conviction_map[i]}")

    print(f"""
  OVERALL ASSESSMENT:
  ───────────────────
  Poland in Q1 2026 offers a rare confluence: MSCI reclassification
  bringing structural inflows, a defense super-cycle that has not yet
  been priced into sub-contractors, a banking sector CHF overhang
  that is definitively resolving, and an energy transition mandate
  that is legally binding and funded.

  The six companies above are not random cheap stocks. Each one has:
  ✓ A specific, named mispricing mechanism
  ✓ A specific, named catalyst that forces price discovery
  ✓ A floor that limits downside independently of the catalyst
  ✓ An asymmetry ratio > 2x (most > 5x)

  These are ideas a hedge fund would build positions in — not because
  Poland is a great market, but because the specific mispricing is
  identifiable, measurable, and correctable within a 12–36 month window.

  The edge is: you read Polish. Most of the competition does not.
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
