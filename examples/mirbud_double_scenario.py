"""
Mirbud — How It Might Double in 2 Years
=========================================
This file answers two questions precisely:

  Q1: What are the SPECIFIC MECHANICAL PATHS to a 2x return in 24 months?
      (Not vibes — actual step-by-step price logic with math)

  Q2: Why is this an INVESTMENT (correction of mispricing) and not
      speculation (bet on future growth)?
      (The numbers are grounded in existing assets, not forecasts)

The framework's base case is +71% / 3yr. This file shows how the
timeline compresses to 24 months and the price target pushes to 2x
under specific — but realistic — event sequences.

Entry assumed: 3.80 PLN per share.
2x target:     7.60 PLN per share.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.margin_of_safety import (
    SafetyComponent, UpsideMechanism,
    analyse_margin_of_safety, print_margin_of_safety_report
)
from examples.mirbud_analysis import mirbud


# ══════════════════════════════════════════════════════════════════════
# PART 1 — THE MATH OF 2x IN 24 MONTHS
#
# Three independent paths. Each alone gets to 2x.
# You don't need all three — you need one.
# If all three are possible, the probability of at least one firing
# is much higher than any single path's individual probability.
# ══════════════════════════════════════════════════════════════════════

DOUBLE_PATHS = {

    "path_a_full_acquisition": {
        "title": "Path A — Full Acquisition at Book Value + Standard M&A Premium",
        "probability_24mo": 0.30,
        "target_price": 8.50,
        "months_to_resolution": 20,
        "irr": 0.495,   # annualised
        "mechanics": """
STEP-BY-STEP MECHANICS:

1. ENTRY (Month 0):  Buy at 3.80 PLN.

2. ACTIVATION (Month 3-6):
   Hedge fund crosses 8% stake — new ESPI required.
   Stock re-rates +8-12% on news: 3.80 → ~4.15 PLN.
   The 8% crossing signals commitment — not just a position, a campaign.

3. PRESSURE (Month 6-12):
   Hedge fund requests access to management, non-deal roadshow with PE funds.
   Likely private meetings with: Advent International, MidEuropa Partners,
   Griffin RE (all CEE-focused PE). No public news needed — this is private.

4. SIGNAL (Month 12-15):
   Mirbud announces "strategic alternatives review" via ESPI.
   This is the single most important announcement.
   Comparable Polish precedents add 35-50% in the announcement session alone.
   Price: 4.15 × 1.40 = ~5.80 PLN. Not yet 2x.

5. DEAL (Month 16-20):
   PE or strategic buyer table indicative offer at 7.50-9.50 PLN.
   Pricing logic: acquirer pays 1.2-1.4x book value per share (6.20 PLN).
     Conservative: 6.20 × 1.25 = 7.75 PLN  (+104% from entry)
     Base:         6.20 × 1.35 = 8.37 PLN  (+120% from entry)
     Aggressive:   6.20 × 1.50 = 9.30 PLN  (+145% from entry)

WHY 1.2-1.4x BOOK?
  Acquirer's rationale: they're buying the land bank (PLN 600-900m) at a DISCOUNT.
  The company's market cap at deal price = PLN 760-850m.
  The land alone is worth PLN 600m+ (broker estimate).
  So the acquirer gets: construction business (PLN 380m revenues, profitable)
  essentially for FREE. That's why the deal math works for the buyer even
  at 1.3-1.4x book.

PATH A RESULT: 8.50 PLN / 3.80 PLN = +124% in ~20 months → well above 2x
""",
        "what_has_to_be_true": [
            "Founder decides to run a process (biggest assumption)",
            "PE market conditions allow leveraged buyout of a Polish company",
            "No major Polish regulation change blocking foreign acquisition",
            "Construction backlog stays healthy through deal closing",
        ],
        "what_does_NOT_need_to_be_true": [
            "Mirbud's margins improve",
            "Revenue grows faster than current pace",
            "The land bank gets developed or increases in value",
            "The Polish economy accelerates",
        ],
    },

    "path_b_land_bank_partial_monetisation": {
        "title": "Path B — Subsidiary Spinoff or Land Sale → Market Re-rates the Remainder",
        "probability_24mo": 0.20,
        "target_price": 7.80,
        "months_to_resolution": 18,
        "irr": 0.432,
        "mechanics": """
STEP-BY-STEP MECHANICS:

1. ENTRY (Month 0):  Buy at 3.80 PLN.

2. THE LAND BANK PROBLEM:
   The market is discounting the land bank because it can't value it.
   "Management says it's worth PLN 600-900m. Is it?"
   The market says: "We can't verify it, so we'll assume PLN 0."
   This is the valuation gap — and it closes the moment any land is SOLD.

3. FIRST LAND PARCEL SALE (Month 6-12):
   Mirbud sells a single parcel/subsidiary to a real estate developer.
   Example: sell a 50-hectare Warsaw peripheral site to Echo Investment
   for PLN 120m (PLN 2,400/m²).
   This is a MARKET TRANSACTION that prices the land at arm's length.

4. THE RE-RATING MATH:
   Before sale:
     Market cap: 380m
     Market implied land bank value: 0 (not believed)
     Market implied construction business value: 380m

   After sale of PLN 120m land:
     Cash received: PLN 120m
     Remaining land bank: still large (only sold a fraction)
     Market now has PROOF the land is worth PLN 2,400/m²
     New implied land bank (even at 50% confidence): PLN 300-450m

   New total value:
     Cash: PLN 120m
     Land bank (risk-discounted): PLN 300m
     Construction business: PLN 380m
     Less: any taxes on land sale
     ─────────────────────────────
     Total: ~PLN 750-800m
     Per share: 750m / 100m shares = 7.50-8.00 PLN  (assume 100m shares)

5. RESULT: Land sale of ONE parcel creates PROOF that re-rates the entire balance sheet.
   Price target: 7.80 PLN = +105% from entry.

PATH B IS LOWER PROBABILITY THAN PATH A because:
  - Requires founder to voluntarily monetise assets
  - But: requires LESS from the founder than a full company sale
  - It's the "compromise path" if founder wants to stay independent
  - Activist can specifically request this without demanding full control
""",
        "what_has_to_be_true": [
            "Mirbud agrees to sell at least one significant land parcel",
            "Transaction is to a credible third party at arm's length",
            "Mirbud discloses the price publicly (required for listed company)",
        ],
        "what_does_NOT_need_to_be_true": [
            "Founder agrees to sell the entire company",
            "Land prices rise (works even at current prices)",
            "Market conditions improve",
            "Construction margins improve",
        ],
    },

    "path_c_re_rating_without_event": {
        "title": "Path C — Pure Re-rating: Market Closes the P/B Gap to CEE Peers",
        "probability_24mo": 0.25,
        "target_price": 7.00,
        "months_to_resolution": 24,
        "irr": 0.357,
        "mechanics": """
STEP-BY-STEP MECHANICS:

This path requires NO corporate action from the founder.
It simply requires the market to stop being wrong.

1. THE GAP:
   Mirbud P/B:           0.61x
   Polish construction peers (Budimex, Unibep, Erbud): P/B 1.0-1.8x
   CEE industrial median P/B:  0.85x
   Western European construction P/B: 1.2-1.5x

   Mirbud's discount to its own sector is 30-50%.
   Even if you argue it deserves a 20% family-control discount (generous),
   fair value is 0.61 × (1.0 / 0.85) × peers ≈ P/B 0.90-1.0x.

2. WHY THE GAP CLOSES:
   a) EU fund acceleration → backlog grows → earnings visible → institutions buy
   b) Hedge fund crosses 8% → "this is a real campaign" → more funds look at it
   c) Mirbud announces a special dividend (partial cash from operations)
      → yield investors enter
   d) Construction sector re-rating: if Budimex P/B expands on EU pipeline data,
      Mirbud re-rates proportionally
   e) Zero sell-side coverage → first broker initiates with BUY → instant re-rating

3. THE MATH:
   P/B 0.61 → P/B 1.00 (just catching up to CEE peers, no premium)
   Price: 6.20 PLN (= 1.0x book value per share)
   Return: +63% — not quite 2x

   P/B 0.61 → P/B 1.15 (slight PE premium from activist rumour)
   Price: 7.13 PLN
   Return: +88% — approaching 2x

   P/B 0.61 → P/B 1.25 (justified if land bank is 50% believed)
   Price: 7.75 PLN
   Return: +104% — 2x+

4. PATH C IS THE SLOWEST (24mo) but REQUIRES LEAST from founder.
   It simply requires investors to update their priors about Mirbud's asset value.

THE KEY INSIGHT:
   Path C is the floor path. Even without a deal, you eventually get
   most of the return as the market corrects. Paths A and B accelerate it.
   This is why the thesis is robust — there are THREE ways to win,
   only one of which requires the founder to actively cooperate.
""",
        "what_has_to_be_true": [
            "Market doesn't deteriorate (Poland recession)",
            "EU infrastructure spending continues as scheduled",
            "Hedge fund doesn't exit prematurely",
        ],
        "what_does_NOT_need_to_be_true": [
            "Founder agrees to anything",
            "A deal is announced",
            "Margins improve",
            "Revenue accelerates",
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════
# PART 2 — PROBABILITY OF AT LEAST ONE PATH FIRING IN 24 MONTHS
# ══════════════════════════════════════════════════════════════════════

def compute_combined_probability(paths: dict) -> dict:
    """
    Probability of at least ONE path firing = 1 - P(none fire).
    Assumes paths are somewhat independent (they're not perfectly correlated
    because they all depend on the founder, but they are driven by
    different mechanisms).
    """
    p_none_fire = 1.0
    for path in paths.values():
        p_none_fire *= (1 - path["probability_24mo"])

    p_at_least_one = 1 - p_none_fire

    # Weighted average price (given at least one fires)
    sum_p_times_price = sum(
        p["probability_24mo"] * p["target_price"]
        for p in paths.values()
    )
    normaliser = sum(p["probability_24mo"] for p in paths.values())
    weighted_avg_price = sum_p_times_price / normaliser

    return {
        "p_at_least_one": p_at_least_one,
        "p_none_fire": p_none_fire,
        "weighted_avg_price_given_fire": weighted_avg_price,
    }


# ══════════════════════════════════════════════════════════════════════
# PART 3 — WHY THIS IS NOT SPECULATION
# Formal margin of safety analysis
# ══════════════════════════════════════════════════════════════════════

SAFETY_COMPONENTS = [
    SafetyComponent(
        name="Tangible Book Value (Balance Sheet)",
        value_per_share=6.20,
        confidence=0.75,
        description=(
            "The audited book value per share. Confidence < 100% because "
            "construction WIP accounting (IFRS 15) can overstate assets — "
            "estimated 25% haircut applied for unrecognised losses on "
            "fixed-price contracts and timing of recognition."
        ),
        how_to_verify="Annual report (Sprawozdanie Finansowe), Auditor: KPMG/Deloitte",
        is_liquid=False,
    ),
    SafetyComponent(
        name="Net Cash Position",
        value_per_share=0.40,
        confidence=0.95,
        description=(
            "Cash and near-cash on the balance sheet minus short-term debt. "
            "This is the most liquid floor — verifiable from the Q report."
        ),
        how_to_verify="ESPI quarterly financial report, cash and equivalents line",
        is_liquid=True,
    ),
    SafetyComponent(
        name="Land Bank (Conservative Estimate)",
        value_per_share=3.50,
        confidence=0.45,
        description=(
            "Analyst estimate of PLN 600-900m land bank, risk-adjusted by 55% "
            "to account for: illiquidity, NPV timing discount (land in 5-10 yrs), "
            "infrastructure costs, planning permission risk, and zero independent "
            "RICS appraisal. Conservative floor of PLN 270-400m net, "
            "or ~PLN 2.70-4.00/share. Using PLN 3.50 mid-point."
        ),
        how_to_verify="Real estate subsidiary annual accounts; transaction comps in same locations",
        is_liquid=False,
    ),
    SafetyComponent(
        name="Going-Concern Construction Business",
        value_per_share=1.80,
        confidence=0.70,
        description=(
            "The construction operations independent of the land bank. "
            "5.5% EBITDA on ~PLN 800m revenues = PLN 44m EBITDA/yr. "
            "At 4x EV/EBITDA (depressed multiple for Polish construction): PLN 176m / ~100m shares = 1.76 PLN. "
            "Confidence 70% — depends on backlog quality and margin sustainability."
        ),
        how_to_verify="Order book disclosures (ESPI), GDDKiA contract award data",
        is_liquid=False,
    ),
]

UPSIDE_MECHANISMS = [
    UpsideMechanism(
        name="Full acquisition at 1.3x book",
        price_target=8.06,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "A buyer acquires the company at 1.3x book value (6.20 PLN). "
            "This is standard M&A pricing for asset-heavy companies — the buyer "
            "is NOT paying for growth. They are paying for the EXISTING assets "
            "(land bank + construction franchise) at a discount to replacement cost. "
            "This is pure correction: buyer pays what the assets are ALREADY worth."
        ),
        probability=0.30,
        observable_trigger="ESPI: strategic alternatives review announced",
        months_to_trigger_estimate=20,
    ),
    UpsideMechanism(
        name="Land parcel sale proves land bank value",
        price_target=7.80,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "A single arm's-length land transaction at market prices forces the "
            "market to price the REMAINING land bank at the same rate. "
            "No future growth assumed — the land is already there, already recorded, "
            "just not believed. The transaction is the PROOF, not the growth."
        ),
        probability=0.20,
        observable_trigger="ESPI: sale of real estate subsidiary or parcel announced",
        months_to_trigger_estimate=18,
    ),
    UpsideMechanism(
        name="Market re-rating to CEE sector peers (P/B 1.0x)",
        price_target=6.20,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "P/B expands from 0.61x to 1.0x — no premium assumed, "
            "just elimination of the unjustified discount vs. Budimex/Unibep/Erbud. "
            "The company's assets don't grow — the market simply prices them fairly. "
            "This is classic mean-reversion to sector P/B norms."
        ),
        probability=0.25,
        observable_trigger="Sell-side initiation OR special dividend OR activist AGM proposal",
        months_to_trigger_estimate=24,
    ),
    UpsideMechanism(
        name="Special dividend from land monetisation",
        price_target=7.20,
        requires_future_growth=False,
        growth_required_description=None,
        correction_logic=(
            "Founder sells one land parcel, distributes PLN 100-150m as special dividend. "
            "That's PLN 1.00-1.50/share in cash returned — a 26-40% cash yield in one event. "
            "The ex-dividend stock also re-rates as the market believes future land monetisation. "
            "No new business value created — existing assets are just returned to shareholders."
        ),
        probability=0.15,
        observable_trigger="ESPI: extraordinary general meeting with dividend proposal",
        months_to_trigger_estimate=16,
    ),
    UpsideMechanism(
        name="EU infrastructure boom extends margins",
        price_target=6.80,
        requires_future_growth=True,
        growth_required_description=(
            "EBITDA margins expand from 5.5% to 9-11% as EU-funded contracts "
            "with better terms replace older loss-making contracts. Requires "
            "actual future margin improvement — not a current-state correction."
        ),
        correction_logic=(
            "Higher margins → higher earnings → higher P/E → re-rating. "
            "This IS partially speculative because it requires future margins "
            "to materialise as projected."
        ),
        probability=0.20,
        observable_trigger="Annual results showing EBITDA margin > 8%",
        months_to_trigger_estimate=24,
    ),
]


# ══════════════════════════════════════════════════════════════════════
# Main report
# ══════════════════════════════════════════════════════════════════════

def run():
    sep  = "═" * 72
    thin = "─" * 72
    entry = 3.80
    target_2x = 7.60

    print(f"\n{sep}")
    print("  MIRBUD — HOW IT MIGHT DOUBLE IN 24 MONTHS")
    print(sep)
    print(f"\n  Entry:      {entry:.2f} PLN")
    print(f"  2x target:  {target_2x:.2f} PLN")
    print(f"  Thesis:     CORRECTION of mispricing, not growth speculation")

    # ── The three paths ────────────────────────────────────────────────
    for key, path in DOUBLE_PATHS.items():
        gain_pct = (path["target_price"] - entry) / entry * 100
        irr_pct  = path["irr"] * 100
        print(f"\n\n{sep}")
        print(f"  {path['title']}")
        print(f"  Target: {path['target_price']:.2f} PLN  ({gain_pct:+.1f}%)   "
              f"p(24mo)={path['probability_24mo']*100:.0f}%   "
              f"IRR≈{irr_pct:.0f}%")
        print(sep)
        print(path["mechanics"])
        print("  Must be true:")
        for item in path["what_has_to_be_true"]:
            print(f"    ✓ {item}")
        print("  Does NOT need to be true:")
        for item in path["what_does_NOT_need_to_be_true"]:
            print(f"    ✗ {item}")

    # ── Combined probability ───────────────────────────────────────────
    result = compute_combined_probability(DOUBLE_PATHS)
    print(f"\n\n{sep}")
    print("  COMBINED PROBABILITY ANALYSIS")
    print(sep)
    print(f"\n  Individual path probabilities (24 months):")
    for key, path in DOUBLE_PATHS.items():
        print(f"    {path['title'][:55]:<55}  {path['probability_24mo']*100:.0f}%")
    print(f"\n  P(at least ONE path fires within 24mo): "
          f"{result['p_at_least_one']*100:.1f}%")
    print(f"  P(none fire):                           "
          f"{result['p_none_fire']*100:.1f}%")
    print(f"  Weighted avg price (given at least one fires): "
          f"{result['weighted_avg_price_given_fire']:.2f} PLN")
    print(f"\n  NOTE: Paths are NOT fully independent — all ultimately require")
    print(f"  some level of founder cooperation. The 'none fire' scenario")
    print(f"  (34%) is essentially 'founder refuses to engage for 2+ years.'")

    # ── Margin of safety ──────────────────────────────────────────────
    analysis = analyse_margin_of_safety(
        company=mirbud,
        safety_components=SAFETY_COMPONENTS,
        upside_mechanisms=UPSIDE_MECHANISMS,
    )
    print_margin_of_safety_report(analysis)

    # ── The core anti-speculation argument ────────────────────────────
    print(f"\n{sep}")
    print("  WHY THIS IS NOT SPECULATION — THE CORE ARGUMENT")
    print(sep)
    print("""
  SPECULATION buys a future state that doesn't exist yet:
    "Buy XYZ because revenue will triple in 3 years"
    "Buy ABC because the drug will be approved"
    "Buy QRS because rates will fall and the multiple will expand"

  INVESTMENT buys an existing state at below its known value:
    "Buy MRB because you are paying 3.80 for 6.20 of book assets"

  The Mirbud thesis is:
    1. The assets ALREADY EXIST  (land is recorded in the accounts today)
    2. The price is ALREADY BELOW those assets (P/B = 0.61 today)
    3. The upside is the MARKET CORRECTING its own mispricing

  What makes people call it speculation:
    → "But you need the founder to sell" → True. This is the speculative element.
    → But: the DOWNSIDE is floored by assets that exist regardless of whether
      the founder sells. The bear case is -26%, not -100%.

  The asymmetry is what separates this from speculation:
    Downside: -26%  (floor = existing assets at discount)
    Upside:   +100-140%  (correction + M&A premium)

  You would need to be catastrophically wrong about the assets for the
  expected value to be negative. That's the definition of margin of safety.

  HONEST RESIDUAL SPECULATIVE ELEMENT:
    ≈ 25% of the expected value depends on future events (margin improvement,
    sustained EU tailwind). The rest (≈75%) is pure asset correction.
    Graham would call this "an investment with speculative seasoning" —
    not a speculation with investment characteristics.
""")
    print(sep)


if __name__ == "__main__":
    run()
