"""
mBank SA (WSE: MBK)
====================
Thesis: PARENT_DISPOSITION + CHF_RESOLUTION

mBank is Poland's 4th-largest bank by assets and one of the most profitable
(ROE 16.4%, cost-to-income <30%). It is a wholly-owned subsidiary of
Commerzbank AG (Germany), which owns ~69%.

Two overlapping, independently-sufficient theses:

THESIS 1: CHF_RESOLUTION (Near-term, high certainty)
  mBank carries legacy Swiss franc mortgage exposure from the 2000s.
  Polish courts have been siding with borrowers → banks provisioned heavily.
  mBank has the HIGHEST provision coverage ratio in the sector at 51.6%.
  CHF risk costs fell >50% year-on-year in 2025.
  The CHF portfolio is nearly run off — new lawsuits declining rapidly.
  As the overhang lifts: capital released, P/E normalises.

  Current P/E: 12.4x. Polish banking sector ex-CHF trades at 14-16x.
  DCF fair value (Alpha Spread model): PLN 1,221 vs price PLN 1,013 = +20.5%
  No CHF discount needed soon → simple P/E expansion to 14-15x = +14-21%.

THESIS 2: PARENT_DISPOSITION (Medium-term, binary)
  UniCredit (Italy) is pursuing Commerzbank. Owns ~26-29%, approaching 30%.
  If UniCredit acquires Commerzbank, what happens to mBank?
  Two scenarios:
    A. UniCredit keeps mBank → strategic fit (UniCredit is expanding in CEE)
    B. UniCredit divests mBank → forces sale; mBank as standalone/target

  Scenario B is more likely because:
    - UniCredit is already entering Poland via Vodeno (Polish Banking-as-a-Service)
    - Maintaining two Polish banking operations is inefficient
    - ECB/KNF regulatory pressure on concentration
    - mBank at PLN 43bn market cap = UniCredit could IPO or sell to Polish PE/bank

  If mBank is sold or listed independently:
    - Premium paid for control: typically 20-40% for banking acquisitions
    - Acquirer candidates: PKO BP, Pekao, Santander Poland, ING BSK (size)
    - Or: PE + IPO (KKR type deal, similar to mBank's own digital banking model)

  mBank's own digital bank (mBank technology) was named "best digital bank in CEE"
  multiple times. The franchise is worth MORE than the current banking multiples imply.

Key financials (data as of early 2026):
  Price: PLN 1,013/share (January 2026)
  Market cap: PLN 43,079m (~€8.7bn)
  P/E: 12.4x
  ROE: 16.4%
  Cost-to-income: <30% (one of the best in Poland)
  Revenue TTM: PLN 12.04bn
  CHF provision coverage: 51.6% (highest in sector)
  CHF legal cost YoY decline: >50% in 2025
  Parent: Commerzbank AG (German, ~69% stake)
  Commerzbank status: UniCredit has ~29% stake, approaching takeover threshold

Data as of: March 2026
Sources:
  - mBank annual report 2024/2025 (mbank.pl/ir)
  - Alpha Spread DCF: PLN 1,221 vs PLN 791 (May 2025 model)
  - S&P Global: "Swiss franc legal risk costs dropped >50% YoY"
  - Bloomberg: Commerzbank / UniCredit coverage
  - PGGM credit risk sharing: mBank + PGGM PLN 9bn transaction (de-risks CHF)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.models import (
    Company, PivotSignal, PriceScenario, PivotType,
    SignalStrength, ScoringWeights
)
from framework.scoring import score_company
from framework.pivot_types import suggest_pivot_types
from framework.report import print_report
from framework.margin_of_safety import (
    SafetyComponent, UpsideMechanism,
    analyse_margin_of_safety, print_margin_of_safety_report,
)
from framework.idea_types import IdeaType, identify_idea_types


# ──────────────────────────────────────────────────────────────────────
# Company profile
# ──────────────────────────────────────────────────────────────────────
# Shares: PLN 43,079m market cap / PLN 1,013 price = ~42.5m shares
# Note: mBank is a large-cap (€8.7bn) — not a micro-cap. Different risk profile.
# This idea is more event-driven / special situation than value micro-cap.

mbank = Company(
    name="mBank SA",
    ticker="MBK",
    exchange="WSE",
    sector="Commercial Banking (Digital-First)",
    country="Poland",

    current_price=1013.00,         # PLN per share (January 2026)
    market_cap_m=43_079,           # PLN millions (~€8.7bn)
    currency="PLN",

    # Balance sheet
    book_value_per_share=None,     # Banks: use P/BV and ROE instead
    net_cash_per_share=None,       # N/A for banks
    hidden_asset_value_per_share=0.0,

    # Earnings profile
    ebitda_margin_pct=None,        # Banks use NIM, not EBITDA
    revenue_growth_yoy_pct=5,      # Revenue Q1-Q3 2025 up 5% YoY
    roe_pct=16.4,                  # One of the highest ROE banks in Poland

    # Ownership
    insider_ownership_pct=1,
    institutional_ownership_pct=20,    # Float shareholders
    float_pct=31,                      # Commerzbank ~69%, public ~31%

    pivot_types=[
        PivotType.OWNERSHIP_CHANGE,    # Commerzbank/UniCredit M&A
        PivotType.CAPITAL_STRUCTURE,   # CHF resolution → capital release
    ],

    thesis_summary=(
        "mBank is Poland's best digital bank: ROE 16.4%, cost-to-income <30%, "
        "revenue growing despite interest rate headwinds. "
        "TWO independent theses — either alone justifies the investment: "
        "(1) CHF resolution: provision costs fell >50% YoY in 2025; with 51.6% "
        "coverage ratio (highest in sector), the legal overhang is nearly resolved. "
        "As the discount disappears, P/E expands from 12.4x toward sector 14-16x. "
        "(2) UniCredit pursuing Commerzbank (which owns 69% of mBank): if UniCredit "
        "succeeds, it will likely divest mBank (already entering Poland via Vodeno). "
        "Forced sale = 20-40% acquisition premium over current price. "
        "You get the M&A option on top of already-cheap fundamental valuation."
    ),

    key_risks=[
        "CHF legal escalation: new Supreme Court ruling expanding bank liability",
        "Polish government retroactive bank tax on CHF portfolio",
        "UniCredit-Commerzbank deal stalls (German government opposition persists)",
        "Polish interest rate cuts accelerate (NIM compression reduces ROE)",
        "mBank kept by UniCredit with no premium for Polish minorities",
        "Macro: Polish GDP slowdown reduces loan growth",
    ],

    time_horizon_years=2.0,
)


# ──────────────────────────────────────────────────────────────────────
# Signals
# ──────────────────────────────────────────────────────────────────────

mbank.signals = [

    PivotSignal(
        name="CHF legal costs fell >50% YoY in 2025 — overhang lifting",
        description=(
            "Swiss franc mortgage legal provision costs declined by >50% year-on-year "
            "in 2025. The CHF portfolio is nearly run off. New lawsuits are declining "
            "as the statute of limitations runs and cases are settled. "
            "mBank entered a PLN 9bn credit risk sharing transaction with Dutch "
            "pension fund PGGM — one of the first of this type in Poland. "
            "This signals: insiders believe the CHF tail is manageable."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="catalyst",
        source="S&P Global Market Intelligence; mBank Q3 2025 results; mBank-PGGM announcement",
        confidence=0.95,
    ),

    PivotSignal(
        name="mBank 51.6% CHF provision coverage — highest in sector",
        description=(
            "mBank has provisioned 51.6% of its CHF portfolio — the highest "
            "coverage ratio among Polish banks. Bank Millennium: 41.3%. "
            "BNP Paribas Bank Polska: 36.9%. "
            "More provisioned = less downside risk from future adverse rulings. "
            "If CHF fully resolved: provisioned capital returns as distributable earnings."
        ),
        strength=SignalStrength.DEFINITIVE,
        category="fundamentals",
        confidence=1.0,
    ),

    PivotSignal(
        name="UniCredit at ~29% of Commerzbank — approaching 30% threshold",
        description=(
            "UniCredit owns ~26% directly + financial instruments = ~29% total. "
            "30% threshold triggers mandatory public takeover offer in Germany. "
            "UniCredit CEO Orcel may decide by 2027. "
            "German government (12% Commerzbank) remains opposed but cannot block "
            "indefinitely. Regulatory landscape shifting. "
            "If UniCredit acquires Commerzbank: what happens to mBank is the question."
        ),
        strength=SignalStrength.STRONG,
        category="smart_money",
        source="Bloomberg; S&P Global; UniCredit investor communications",
        confidence=0.85,
    ),

    PivotSignal(
        name="UniCredit already entering Poland via Vodeno (Banking-as-a-Service)",
        description=(
            "UniCredit is acquiring Vodeno, a Polish Banking-as-a-Service provider. "
            "This strongly implies UniCredit is building a Polish presence and "
            "would NOT want to maintain two Polish banking operations (Vodeno + mBank). "
            "Strategic logic: sell mBank, build new on Vodeno's technology platform. "
            "This is the key signal that mBank would be divested, not kept."
        ),
        strength=SignalStrength.STRONG,
        category="catalyst",
        source="UniCredit press releases; Polish fintech media (2025)",
        confidence=0.80,
    ),

    PivotSignal(
        name="ROE 16.4%, cost-to-income <30% — outstanding operational metrics",
        description=(
            "mBank's ROE of 16.4% and cost-to-income ratio below 30% are among the "
            "best of any Polish bank. 'Best digital bank in CEE' multiple awards. "
            "This quality is NOT reflected in the P/E of 12.4x. "
            "Polish banks with lower ROE trade at similar or higher multiples. "
            "Any buyer would be getting a premium-quality banking franchise."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.95,
    ),

    PivotSignal(
        name="DCF value PLN 1,221 vs price PLN 1,013 — 20% fundamental undervaluation",
        description=(
            "Alpha Spread DCF model (May 2025): fair value PLN 1,221 vs price PLN 791 "
            "at time of model (currently PLN 1,013). Even at current price: "
            "+20.5% undervaluation on DCF basis alone, BEFORE M&A premium. "
            "The thesis doesn't need the UniCredit event — cheap on fundamentals."
        ),
        strength=SignalStrength.MODERATE,
        category="fundamentals",
        confidence=0.70,
    ),

    PivotSignal(
        name="mBank Q3 2025: net profit +46% YoY, revenue +5% despite rate cuts",
        description=(
            "Q3 2025: net profit PLN 837m (+46% YoY despite -13% QoQ seasonality). "
            "Revenue PLN 3bn+ per quarter. CET1 well above regulatory requirements. "
            "The underlying business is performing strongly — the CHF and ownership "
            "clouds are concealing a genuinely improving bank."
        ),
        strength=SignalStrength.STRONG,
        category="fundamentals",
        confidence=0.95,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Price scenarios
# ──────────────────────────────────────────────────────────────────────

mbank.scenarios = [

    PriceScenario(
        label="bear",
        price_target=700.00,    # PLN 700, -31%
        probability=0.20,
        rationale=(
            "UniCredit-Commerzbank deal collapses; new Polish Supreme Court ruling "
            "expands CHF bank liability; mBank forced to increase provisions again. "
            "P/E compresses to 8x on reduced earnings. PLN 1,013 × 0.69 = PLN 699. "
            "Note: even in this scenario, mBank is STILL a profitable bank — "
            "not a zero. The downside is meaningful but limited."
        ),
        time_horizon_years=2.0,
        irr=-18.0,
    ),

    PriceScenario(
        label="base",
        price_target=1350.00,   # PLN 1,350, +33%
        probability=0.55,
        rationale=(
            "CHF overhang largely resolved (PLN 1,221 DCF fair value reached). "
            "P/E re-rates from 12.4x to 14x as CHF provision costs normalise. "
            "Commerzbank/UniCredit situation progresses: mBank put on strategic review. "
            "No full acquisition, but RUMOUR of sale = +20-30% market expectation. "
            "Combined: fundamental + sentiment = PLN 1,300-1,400."
        ),
        time_horizon_years=2.0,
        irr=18.0,
    ),

    PriceScenario(
        label="bull",
        price_target=1750.00,   # PLN 1,750, +73%
        probability=0.25,
        rationale=(
            "UniCredit acquires Commerzbank; announces mBank strategic review; "
            "binding offer from PKO BP / Pekao / ING BSK at 30-40% premium "
            "to P/E fair value (PLN 1,221 × 1.35 = PLN 1,648). "
            "Or: Commerzbank IPOs mBank minority stake with control premium. "
            "Polish banking M&A precedents: premiums of 25-40% over pre-bid price. "
            "PLN 1,013 × 1.73 = PLN 1,752."
        ),
        time_horizon_years=2.0,
        irr=32.0,
    ),
]


# ──────────────────────────────────────────────────────────────────────
# Margin of safety (banks: use P/BV and earnings, not SOTP)
# ──────────────────────────────────────────────────────────────────────

MBANK_SAFETY = [
    SafetyComponent(
        name="Earnings power (PLN 3.3bn annual net profit pace)",
        value_per_share=700.00,   # At 9x bear P/E: still PLN 700+
        confidence=0.85,
        description=(
            "Q3 2025 net profit PLN 837m → annualised PLN 3.35bn. "
            "At P/E 9x (extreme distress): PLN 3.35bn × 9 = PLN 30.1bn market cap. "
            "/ 42.5m shares = PLN 708/share. Floor even in worst-case P/E scenario."
        ),
        how_to_verify="mBank quarterly results",
        is_liquid=False,
    ),
    SafetyComponent(
        name="CHF provision coverage (51.6%) — worst already provisioned",
        value_per_share=150.00,   # Incremental protection from highest sector coverage
        confidence=0.80,
        description=(
            "51.6% coverage vs sector average 41%. Incremental 10.6% over-provisioning "
            "relative to peers provides cushion against adverse rulings. "
            "If courts maintain current trend, over-provisioning reverses to earnings."
        ),
        how_to_verify="mBank H1 2025 results — CHF legal reserve disclosures",
        is_liquid=False,
    ),
    SafetyComponent(
        name="Commerzbank strategic value of mBank (won't sell below book)",
        value_per_share=163.00,   # Floor at book value
        confidence=0.70,
        description=(
            "Commerzbank would not accept a sale of mBank below book value — "
            "this would damage Commerzbank's own capital ratios. "
            "Book value per mBank share provides a hard floor on any transaction."
        ),
        how_to_verify="mBank annual report — equity per share calculation",
        is_liquid=False,
    ),
]

MBANK_UPSIDE = [
    UpsideMechanism(
        name="CHF resolution → P/E normalises to 14x",
        price_target=1320.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "Polish banking sector ex-CHF trades at 14-16x P/E. "
            "mBank at 12.4x with the highest CHF coverage in sector. "
            "When CHF risk is provably over: re-rates to 14x. "
            "Annualised EPS ~PLN 94 × 14 = PLN 1,316. "
            "This requires no M&A, no growth — just CHF cost normalisation."
        ),
        probability=0.65,
        observable_trigger="mBank reports CHF legal costs < PLN 100m/quarter for 2+ consecutive quarters",
        months_to_trigger_estimate=12,
    ),
    UpsideMechanism(
        name="Acquisition by Polish or foreign bank at 30% premium",
        price_target=1700.00,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "UniCredit acquires Commerzbank; mBank put up for sale. "
            "Transaction at 30% premium to pre-bid PLN 1,013 = PLN 1,317. "
            "Or: transaction at 1.4x P/BV (standard Polish bank M&A premium) = "
            "PLN ~1,750. PKO BP, Pekao or foreign buyer."
        ),
        probability=0.30,
        observable_trigger="Commerzbank press release: 'strategic review of Polish subsidiary'",
        months_to_trigger_estimate=24,
    ),
    UpsideMechanism(
        name="Full re-rating: CHF resolved + M&A premium + digital bank multiple",
        price_target=2200.00,
        requires_future_growth=True,
        growth_required_description=(
            "Requires: CHF fully resolved, UniCredit deal completed, mBank "
            "acquirer pays premium for 'best digital bank in CEE' franchise. "
            "mBank valued at 2x P/BV (premium digital bank) vs 1.2x current."
        ),
        correction_logic=(
            "Book value × 2.0x (premium digital bank multiple) = PLN 2,200+. "
            "Compared to N26 (German digital bank) at 5x+ P/BV pre-IPO. "
            "mBank is the most likely Polish banking unicorn equivalent."
        ),
        probability=0.15,
        observable_trigger="mBank announces partnership with international tech company or Neo-bank pivot",
        months_to_trigger_estimate=36,
    ),
]


def run():
    sep  = "═" * 76
    thin = "─" * 76

    print(f"\n{sep}")
    print("  mBANK SA (WSE: MBK)")
    print("  Parent Disposition + CHF Resolution — Two Overlapping Theses")
    print(sep)

    # ── Idea type identification ──────────────────────────────────────
    idea_types = identify_idea_types(
        has_analyst_coverage=True,      # Well covered by Polish brokers
        market_cap_m_eur=8_700,         # Large cap
        institutional_pct=20,
        has_parent_under_pressure=True, # Commerzbank under UniCredit
        has_frozen_stake=False,
        defense_revenue_pct=0,
        has_government_pipeline=False,
        has_sotp_discount=False,
        has_ip_catalog=False,
        has_insider_cluster=False,
        chf_exposure=True,              # Key thesis component
        in_conflict_zone=False,
    )
    print(f"\n  IDENTIFIED IDEA TYPES:")
    print(thin)
    for idea_type, confidence in idea_types:
        print(f"  [{confidence:.0%}] {idea_type.value}: {idea_type.name}")

    # ── Ownership situation ───────────────────────────────────────────
    print(f"\n\n  OWNERSHIP CHESS GAME")
    print(thin)
    print("""
  mBank ownership:
    Commerzbank AG (Germany)    : ~69%   ← under M&A pressure from UniCredit
    Free float / institutional  : ~31%   ← trades on WSE

  UniCredit / Commerzbank status (March 2026):
    UniCredit holds: ~26% direct + instruments = ~29% total
    30% threshold : triggers mandatory public takeover offer (German law)
    CEO Orcel says : decision by 2027; Feb 2026 = can now offer stock-only
    German govt (12%): opposed but weakening (Commerzbank outperforming)

  Scenario tree:
    [60%] UniCredit acquires Commerzbank
      [40%] UniCredit keeps mBank → integrates with Vodeno
        → mBank minorities continue as UniCredit subsidiary shareholders
        → No immediate premium; some future upside from UniCredit integration
      [60%] UniCredit divests mBank → BINDING SALE PROCESS
        → 30-40% acquisition premium over market price
        → Buyers: PKO BP, Pekao, ING BSK, or PE + re-IPO

    [40%] UniCredit does NOT acquire Commerzbank
      → Commerzbank remains independent, mBank status quo
      → CHF resolution thesis plays out on its own timeline (+12-21%)

  Expected value from tree (rough):
    Scenario 1a (keeps): 60% × 40% × 0% premium = 0
    Scenario 1b (divests): 60% × 60% × 35% premium = +12.6% additional
    Scenario 2 (no deal): 40% × +12% CHF = +4.8%
    ─────────────────────────────────
    Additional M&A option value: ~17% on top of standalone CHF thesis
""")

    # ── CHF sector comparison ─────────────────────────────────────────
    print(f"  CHF PROVISION COVERAGE — POLISH BANK SECTOR COMPARISON")
    print(thin)
    chf_data = [
        ("Bank Millennium (MIL)",     9.4,  41.3, "Highest CHF exposure!"),
        ("mBank SA (MBK)",            5.4,  51.6, "Highest coverage ratio → safest"),
        ("BNP Paribas Bank Polska (BNP)", 4.7, 36.9, "Still provisioning"),
        ("Santander Bank Polska (SPL)", 2.1, 65.0, "Almost fully covered"),
        ("ING BSK (ING)",             1.2,  80.0, "Essentially resolved"),
        ("PKO BP (PKO)",              1.8,  72.0, "Mostly resolved"),
    ]
    print(f"\n  {'Bank':<32} {'CHF %':>8} {'Coverage %':>12}  {'Status'}")
    print(f"  {'-'*32} {'-'*8} {'-'*12}  {'-'*25}")
    for name, pct, cov, status in chf_data:
        arrow = " ←" if "mBank" in name else ""
        print(f"  {name:<32} {pct:>8.1f} {cov:>12.1f}  {status}{arrow}")
    print(f"\n  The banks with higher coverage ratios are SAFER — their worst is already provisioned.")
    print(f"  mBank at 51.6% vs Bank Millennium at 41.3% = meaningfully less tail risk.")

    # ── Margin of safety ──────────────────────────────────────────────
    mos = analyse_margin_of_safety(
        company=mbank,
        safety_components=MBANK_SAFETY,
        upside_mechanisms=MBANK_UPSIDE,
    )
    print_margin_of_safety_report(mos)

    # ── Framework score ───────────────────────────────────────────────
    # Override weights for bank: no asset asymmetry or hidden assets
    weights = ScoringWeights(
        asset_asymmetry     = 0.05,
        smart_money_signals = 0.25,   # UniCredit pursuit = the smart money signal
        catalyst_clarity    = 0.30,   # CHF resolution timeline is visible
        downside_protection = 0.20,
        business_quality    = 0.15,
        sentiment_discount  = 0.05,
    )

    result    = score_company(mbank, weights)
    suggested = suggest_pivot_types(mbank)
    print_report(mbank, result, suggested)

    print(f"\n{sep}")
    print("  MONITORING CHECKLIST")
    print(sep)
    print("""
  What to watch weekly:

  CHF Thesis:
    □ mBank quarterly results: CHF provision cost trend (looking for < PLN 100m/quarter)
    □ Polish Supreme Court (SN) CHF rulings — any new chambers or guidance
    □ Bank Millennium and BNP results: if theirs are improving, mBank follows
    □ mBank + PGGM credit risk sharing: look for additional risk transfer deals

  Ownership / M&A Thesis:
    □ UniCredit AGM decisions re Commerzbank (next: May 2026)
    □ German government elections/coalition agreements re Commerzbank privatisation
    □ Commerzbank ESPI-equivalent (Deutsche Bundesanzeiger) for stake change notifications
    □ mBank ESPI: any "material information" disclosure from Commerzbank
    □ UniCredit Vodeno integration progress (KNF approval) — if approved,
      UniCredit no longer needs mBank
    □ PKO BP / Pekao M&A statements (potential acquirers announcing interest in growth)

  Key source: Bloomberg news alerts for "Commerzbank UniCredit mBank"
""")
    print(sep)


if __name__ == "__main__":
    run()
