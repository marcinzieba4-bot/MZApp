"""
Mirbud — Bear Case & Counterargument Analysis
==============================================
This file deliberately steelmans the case AGAINST Mirbud.

The goal is not to change your mind — it's to force you to know exactly
which bear arguments you are being paid to take the other side of.
If you can't articulate the bear case clearly, you don't understand
the bull case well enough to size a position.

Three questions answered here:
  1. WHY does the owner want to sell, and why NOW (urgency factors)
  2. WHY the "cheap" thesis might be completely wrong (5 specific attacks)
  3. HOW Mirbud differs from other cheap companies (species diagnosis)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from framework.models import (
    Company, PivotSignal, PriceScenario, PivotType, SignalStrength
)
from framework.value_trap import detect_trap, print_trap_report, CHEAP_SPECIES


# ══════════════════════════════════════════════════════════════════════
# PART 1 — WHY THE OWNER MIGHT WANT TO SELL, AND WHY NOW
# ══════════════════════════════════════════════════════════════════════
#
# Urgency is the key variable. A founder "thinking about" selling is
# worth nothing. A founder with FIVE time-bound pressures converging
# simultaneously is a different situation entirely.
#
# ──────────────────────────────────────────────────────────────────────

SELLER_MOTIVATIONS = {

    "eu_infrastructure_window": {
        "title": "The EU Infrastructure Window Is Closing",
        "urgency": "HIGH",
        "rationale": (
            "Poland's 2021-2027 EU cohesion fund tranche is at its deployment peak "
            "in 2024-2026. GDDKiA (Polish road authority) and municipalities are "
            "awarding contracts at the fastest pace in a decade. Mirbud's backlog "
            "is at or near an all-time high RIGHT NOW.\n\n"
            "A strategic buyer acquiring Mirbud in 2025 pays for:\n"
            "  - A full order book with 2-3 years of revenue visibility\n"
            "  - Established relationships with public procurement offices\n"
            "  - A workforce/subcontractor network assembled for peak volume\n\n"
            "The same buyer in 2028-2029 (after the EU fund cycle winds down) pays for:\n"
            "  - A half-empty order book\n"
            "  - A workforce about to face layoffs\n"
            "  - Margins compressed by competition for fewer contracts\n\n"
            "The founder knows this. His best price is available for at most 18 months."
        ),
        "evidence": [
            "Polish infrastructure spending peaked in 2024-2025 per GDDKiA data",
            "EU fund absorption requirement creates urgency for awards before 2026",
            "Sector peers trading at higher multiples than they will post-cycle",
        ],
    },

    "activist_dynamic": {
        "title": "Hedge Fund Presence Changes the Game Irreversibly",
        "urgency": "HIGH",
        "rationale": (
            "Once a 5%+ activist is in the register, life as a private family "
            "fiefdom is over. The activist has already:\n\n"
            "  1. Required mandatory ESPI disclosure (the company is now 'watched')\n"
            "  2. Almost certainly had private conversations with management\n"
            "  3. Started modelling takeover scenarios — and shared those models "
            "     with other potential buyers (PE funds, strategic acquirers)\n\n"
            "The founder now faces a fork:\n"
            "  Path A: Sell now on his terms, receive full negotiating premium,\n"
            "          retain control over buyer selection and employee fate.\n"
            "  Path B: Resist. The activist makes the company public property —\n"
            "          shareholder letters, analyst meetings, press articles.\n"
            "          Governance scrutiny exposes every related-party transaction.\n"
            "          The 'comfortable' Polish family company becomes a contested\n"
            "          governance situation. Stress, legal costs, reputational risk.\n\n"
            "Most founders, when facing Path B in their 60s, choose Path A."
        ),
        "evidence": [
            "Hedge funds in CEE typically approach management before going public",
            "Pattern: Kulczyk group, Polsat, TVN all resolved when founders chose Path A",
            "Polish activist precedents: MCI Capital, Nationale-Nederlanden campaigns",
        ],
    },

    "succession_vacuum": {
        "title": "Succession Without a Plan Is a Forced Sale in Slow Motion",
        "urgency": "MEDIUM-HIGH",
        "rationale": (
            "Running a Polish general contractor is not a passive inheritance. It requires:\n"
            "  - Deep personal relationships with public procurement decision-makers\n"
            "  - Technical credibility with engineers and project managers\n"
            "  - Personal guarantees on performance bonds (often €10-50m+)\n"
            "  - Daily crisis management (construction always has crises)\n\n"
            "If the founder's children are not in the business NOW, they won't be ready "
            "in 5 years. And an external CEO hired to run it will eventually sell it.\n\n"
            "The founder faces a binary:\n"
            "  a) Sell at peak, control the terms, choose the buyer\n"
            "  b) Run it until incapacitated, then let heirs or creditors sell it "
            "     under duress, on worse terms, without his relationships\n\n"
            "This is an estate planning problem masquerading as a stock story."
        ),
        "evidence": [
            "No next-generation family member publicly identified in leadership",
            "Construction family businesses in Poland have high sale rates post-founder",
            "Polish business succession statistics: 70%+ of family companies sold vs. passed",
        ],
    },

    "real_estate_valuation_window": {
        "title": "The Land Bank Is Worth More Today Than It Will Be in 2028",
        "urgency": "MEDIUM",
        "rationale": (
            "Mirbud's most valuable hidden asset (the land bank) is only worth its "
            "theoretical value if:\n"
            "  a) Polish real estate prices hold or rise\n"
            "  b) Planning permissions are granted or maintained\n"
            "  c) A buyer is willing to pay for development optionality\n\n"
            "All three conditions are currently met, but conditions in 2028+:\n"
            "  - Polish NBP interest rates remain elevated → RE prices under pressure\n"
            "  - Demographic pressure: Poland's population is declining and aging\n"
            "  - Warsaw suburban land values may have peaked\n\n"
            "The founder's land bank is an option. Like all options, it loses value "
            "as time passes and uncertainty grows. Selling NOW crystallizes maximum "
            "option value before time decay sets in."
        ),
        "evidence": [
            "NBP rates 5-6% → real estate cap rates expanding (values falling)",
            "Polish population declining -0.3%/year; long-term demand structural question",
            "Warsaw peripheral land saw 15-20% price corrections in 2023-2024",
        ],
    },

    "tax_and_estate_window": {
        "title": "Tax and Estate Planning Creates a Near-Term Optimal Window",
        "urgency": "MEDIUM",
        "rationale": (
            "In Poland, a strategic sale of a private company stake can be structured "
            "with significant tax efficiency IF done before:\n"
            "  - Potential changes to capital gains tax regime\n"
            "  - The founder becomes a non-resident for tax purposes (complex)\n"
            "  - Estate transfer occurs (inheritance vs. sale have different tax profiles)\n\n"
            "PE funds and M&A advisors know how to structure deals to maximise "
            "after-tax proceeds for the founder. This 'financial engineering' argument "
            "is often the tipping point in negotiations with reluctant founders.\n\n"
            "Concretely: if the founder can net PLN 400m after tax via a structured "
            "sale today vs. PLN 300m after tax via inheritance in 10 years, "
            "he has a strong financial incentive to act now."
        ),
        "evidence": [
            "Polish CIT/PIT reform discussions (2024-2025 coalition government)",
            "PE-structured transactions regularly deliver 20-30% tax alpha to sellers",
            "Cross-border sale structures available via Luxembourg holding vehicles",
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════
# PART 2 — THE BEAR CASE: WHY MIRBUD IS NOT ACTUALLY CHEAP
# Five specific attacks on the bull thesis
# ══════════════════════════════════════════════════════════════════════

BEAR_ARGUMENTS = {

    "attack_1_accounting_fiction": {
        "title": "Attack #1: The Book Value Is Built on Construction Accounting Fiction",
        "conviction": "HIGH",
        "argument": (
            "Polish construction companies use IAS 11 / IFRS 15 "
            "percentage-of-completion accounting. Under this method:\n\n"
            "  - Revenue is recognised as a percentage of project completion\n"
            "  - Profit is recognised as estimated final margin × completion %\n"
            "  - The 'Work In Progress' asset on the balance sheet = revenue "
            "    recognised but not yet billed\n\n"
            "The trap: estimated final margin is set by management. If a project "
            "goes over budget (extremely common in Polish fixed-price infrastructure), "
            "the loss isn't recognised until management admits it — often years late.\n\n"
            "PRACTICAL IMPACT ON MIRBUD:\n"
            "  - Contracts signed in 2020-2022 used steel prices of PLN 3,200/t\n"
            "  - By 2022-2024, steel was PLN 4,500-5,000/t — 40-55% higher\n"
            "  - Fixed-price government contracts in Poland are hard to renegotiate\n"
            "  - The WIP asset may contain PLN 50-100m of unrecognised losses\n"
            "  - Real book value could be 15-25% LOWER than stated\n\n"
            "IMPLICATION: P/B of 0.61 may actually be P/B 0.75-0.80 on a clean basis. "
            "That's still a discount, but the margin of safety is much thinner."
        ),
        "probability_of_being_correct": 0.55,
        "impact_on_thesis": "Reduces asset asymmetry score from 8.5 to ~6.5",
        "mitigants": [
            "Compare cash flow from operations to net income — divergence signals WIP inflation",
            "Check 2022-2024 annual reports for margin revisions on projects",
            "GDDKiA contract price adjustment clauses introduced in 2022 may have helped",
        ],
    },

    "attack_2_land_bank_is_analyst_estimate": {
        "title": "Attack #2: The Land Bank Valuation Is An Analyst's Guess, Not a Fact",
        "conviction": "HIGH",
        "argument": (
            "The PLN 600-900m land bank estimate comes from a domestic Polish broker. "
            "Let's decompose what this number actually requires:\n\n"
            "STEP 1: What is the land actually worth?\n"
            "  - Has any independent RICS-certified surveyor appraised it? No public disclosure.\n"
            "  - Is the land zoned for the use assumed in the estimate (residential, commercial)?\n"
            "  - Polish planning permission is granted by gmina (local authority) and can "
            "    change arbitrarily — a new mayor reverses the zoning.\n\n"
            "STEP 2: Infrastructure readiness\n"
            "  - Land without road access, sewage, electricity = raw land\n"
            "  - Raw land → developable land requires PLN 200-500/m² of infrastructure costs\n"
            "  - These costs eat directly into the 'hidden value'\n\n"
            "STEP 3: Timing discount\n"
            "  - Land developed in 5-10 years has NPV far below face value\n"
            "  - At 12% discount rate: PLN 1 received in 7 years = PLN 0.45 today\n"
            "  - The PLN 600-900m gross value becomes PLN 300-450m in NPV terms\n\n"
            "STEP 4: Market absorption\n"
            "  - A company selling PLN 500m of land into the Polish market simultaneously "
            "    depresses the very prices it's trying to realise\n\n"
            "REVISED ESTIMATE: The broker's PLN 600-900m likely has a fair NPV "
            "of PLN 250-350m — still above market cap, but with much lower confidence."
        ),
        "probability_of_being_correct": 0.60,
        "impact_on_thesis": "Hidden asset value per share drops 40-60% — asymmetry ratio falls from 5.4x to ~3.0x",
        "mitigants": [
            "Request independent RICS appraisal (activist can push for this)",
            "Look at Mirbud's subsidiary financial statements for individual land parcel valuations",
            "Compare to actual RE transaction prices in the same locations",
        ],
    },

    "attack_3_founder_veto": {
        "title": "Attack #3: The Founder Controls Everything — Including Whether You Make Money",
        "conviction": "VERY HIGH",
        "argument": (
            "This is the central structural flaw in every asset-play thesis on a "
            "founder-controlled company.\n\n"
            "THE MATHEMATICS OF CONTROL:\n"
            "  - Mucha family: 62% → controls every ordinary AGM resolution (>50% required)\n"
            "  - To BLOCK resolutions (25%+ needed): minority can't even do this\n"
            "  - Activist at 5-10%: can ask questions, file proposals, write letters\n"
            "  - Result: every shareholder demand is purely moral pressure, not legal force\n\n"
            "WHAT THE FOUNDER CAN LEGALLY DO (that harms minority):\n"
            "  ✗ Pay himself PLN 5m/year in salary (legal, no cap)\n"
            "  ✗ Lease office space from his family trust at above-market rent (legal)\n"
            "  ✗ Award contracts to his son's construction supply company (if at market terms)\n"
            "  ✗ Issue new shares to himself at a discount (subject to AGM, which he controls)\n"
            "  ✗ Simply NOT sell the company for 20 more years\n\n"
            "THE ACTIVIST'S ACTUAL LEVERAGE:\n"
            "  1. Reputational pressure: Polish business press, international investor "
            "     relations — moderate effect on a founder who doesn't care about reputation\n"
            "  2. Capital markets access: if Mirbud ever needs to issue bonds/shares, "
            "     minority ire makes it harder — but Mirbud may not need capital markets\n"
            "  3. Moral suasion: the activist can make a compelling financial case — "
            "     this WORKS, but only when the founder was already thinking about selling\n\n"
            "VERDICT: If Jarosław Mucha wakes up tomorrow and decides not to sell, "
            "the entire bull case evaporates. You are essentially buying an option "
            "that the founder exercises at his sole discretion."
        ),
        "probability_of_being_correct": 0.70,
        "impact_on_thesis": "Conviction tier should drop from MEDIUM to WATCH unless founder signals intent",
        "mitigants": [
            "Look for any public statements by the founder about long-term ownership",
            "Track whether the founder has accepted meetings with the activist",
            "Any family member leaving the company is a precursor signal",
        ],
    },

    "attack_4_discount_is_rational": {
        "title": "Attack #4: The Market Is Smarter Than You — The Discount Is Rational",
        "conviction": "MEDIUM",
        "argument": (
            "Contrarian investing's central error: assuming the market is wrong and "
            "you are right. Let's steelman the market's 5-year view on Mirbud:\n\n"
            "If Mirbud has traded at 0.6x book for 5+ years, the market has implicitly "
            "decided that the P/B discount is fair. Why might the market be right?\n\n"
            "HYPOTHESIS A — Extraction Discount:\n"
            "  The market correctly prices that the Mucha family extracts ~4-6% of "
            "  equity value annually via related-party transactions, above-market salaries, "
            "  and sub-optimal capital allocation. After 5 years: 20-30% equity dilution. "
            "  The 'cheap' price accounts for this ongoing dilution.\n\n"
            "HYPOTHESIS B — Quality Signal:\n"
            "  Polish institutional investors (OFE pension funds, TFI mutual funds) "
            "  know Mirbud better than foreign hedge funds do. They have NOT accumulated. "
            "  Why? They have done the work and declined. The foreign activist may be "
            "  buying into a situation the locals know well enough to avoid.\n\n"
            "HYPOTHESIS C — Normalised Earnings Are Much Lower:\n"
            "  The current EU-funded infrastructure boom is temporary. Normalised "
            "  margins for Mirbud ex-boom are 3-4% EBITDA. On normalised earnings, "
            "  the P/B of 0.61 is fair or even slightly expensive.\n\n"
            "The uncomfortable question: what do Polish OFE pension funds know "
            "that a London hedge fund just learning about the company doesn't?"
        ),
        "probability_of_being_correct": 0.40,
        "impact_on_thesis": "Entire re-rating thesis is wrong — stock grinds at current level for years",
        "mitigants": [
            "Identify SPECIFIC reason this year is different from prior 5 years",
            "The specific new fact must be: activist + founder age + backlog peak all converging",
            "Check whether Polish OFEs have been buying recently (ESPI filings)",
        ],
    },

    "attack_5_irr_destruction": {
        "title": "Attack #5: Time Kills the IRR — The Math Doesn't Work Without Speed",
        "conviction": "HIGH",
        "argument": (
            "The bull case projects +71% base / +142% bull over 3 years. "
            "These numbers look great until you account for TIME VALUE.\n\n"
            "SCENARIO: Thesis doesn't fire for 4 years instead of 3\n"
            "  Bull scenario: 9.20 PLN in year 4 → IRR 24% (was 34%)\n"
            "  Base scenario: 6.50 PLN in year 4 → IRR 14% (was 19%)\n"
            "  Bear scenario: 2.80 PLN in year 4 → IRR -7%/yr cumulative\n\n"
            "THETA COST (opportunity cost while waiting):\n"
            "  Polish government bonds yield ~5.5% (Dec 2025)\n"
            "  US treasuries: ~4.5%\n"
            "  Every year without the catalyst: your position underperforms by 5%+\n\n"
            "THE HIDDEN COST OF A WRONG TIME ESTIMATE:\n"
            "  Year 1: No news. -5.5% vs. risk-free. OK.\n"
            "  Year 2: Activist exits (gave up). Stock drops 20%. -25% vs. risk-free.\n"
            "  Year 3: Founder dies. Heirs can't agree. Enters prolonged legal dispute.\n"
            "          Stock discount WIDENS. -40% vs. risk-free.\n\n"
            "THE UNDERLYING ISSUE:\n"
            "  The framework correctly identifies the opportunity but incorrectly treats "
            "  the time horizon as known (3 years). In reality, the range is 0-10+ years "
            "  with the founder controlling the clock. IRR must be modeled with "
            "  a time uncertainty distribution, not a fixed point."
        ),
        "probability_of_being_correct": 0.65,
        "impact_on_thesis": "Probability-weighted IRR drops from 19% to 10-12% when time uncertainty is added",
        "mitigants": [
            "Size position to 2-3% of portfolio — live with slower resolution",
            "Use options (if available on WSE) to define time and capital at risk",
            "Set a hard exit rule: if no material catalyst in 18 months, reassess",
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════
# PART 3 — HOW MIRBUD DIFFERS FROM OTHER 'CHEAP' COMPANIES
# The spectrum from value trap to genuine pivot
# ══════════════════════════════════════════════════════════════════════

SPECIES_COMPARISON = {

    # ── Cheap but wrong species ──────────────────────────────────────
    "cigar_butt_vs_mirbud": {
        "example": "Polish print newspaper publisher (e.g. Agora SA)",
        "superficial_similarity": "Both trade at P/B discount, both family-ish influenced",
        "key_difference": (
            "Agora's revenue is in structural -10%/year decline. The assets (printing presses, "
            "physical newsrooms) are worth less every year. You're buying a melting ice cube. "
            "Mirbud's core business has a multi-year EU-funded tailwind. "
            "The assets (land) can appreciate while you wait."
        ),
        "diagnostic_question": "Is the core revenue stream declining faster than assets can be sold?",
    },

    "pure_value_trap_vs_mirbud": {
        "example": "Random Polish family holding company with no obvious catalyst",
        "superficial_similarity": "Both are founder-controlled, both at P/B discount",
        "key_difference": (
            "A pure value trap has NO external pressure — no activist, no EU cycle ending, "
            "no succession urgency. It's cheap and will stay cheap indefinitely. "
            "Mirbud has FIVE converging urgency factors all pointing at the same 18-month window. "
            "The difference between a value trap and a pivot candidate is the SPECIFICITY "
            "and TIMING of the catalyst."
        ),
        "diagnostic_question": "What is different NOW vs. 3 years ago that makes a catalyst MORE likely?",
    },

    "japanese_net_net_vs_mirbud": {
        "example": "Japanese small-cap trading at 0.5x cash (Buffett Japan trade)",
        "superficial_similarity": "Both trade well below asset value",
        "key_difference": (
            "A Japanese net-net has CASH — the most liquid and independently-valued asset. "
            "You're buying PLN 1 of cash for PLN 0.50. No one controls whether cash exists. "
            "Mirbud's hidden value is in LAND — illiquid, valuation-dependent, founder-controlled. "
            "You're buying the founder's OPTION to sell PLN 1 of land for PLN 0.30. "
            "That's a fundamentally different (worse) risk profile."
        ),
        "diagnostic_question": "Can the hidden value be independently verified and is it liquid?",
    },

    "quality_at_discount_vs_mirbud": {
        "example": "Booking.com during COVID (March 2020)",
        "superficial_similarity": "Both trading at discounts to intrinsic value",
        "key_difference": (
            "Booking.com has structural competitive advantages (network effect, brand, data). "
            "Its earnings power was temporarily impaired but structurally intact. "
            "You don't need a catalyst — just wait for COVID to end. "
            "Mirbud has NO competitive moat. A German contractor (Strabag, Hochtief) "
            "can compete for the same contracts tomorrow. You DO need a catalyst — "
            "without one, the stock just reflects its earnings, which are mediocre."
        ),
        "diagnostic_question": "Would the company's intrinsic value appreciate WITHOUT any external event?",
    },

    # ── Where Mirbud actually sits ───────────────────────────────────
    "mirbud_true_species": {
        "species": "Asset Play with Activist Catalyst — but weaker jurisdiction rights",
        "what_makes_it_genuine": [
            "Tangible assets (land is real, not accounting goodwill)",
            "Specific activist with track record in CEE asset plays",
            "Multiple converging urgency factors (EU cycle, founder age, RE window)",
            "Sector tailwind means the business doesn't deteriorate while waiting",
            "Discount is EXTREME even by Polish standards (0.61x vs. CEE median 0.85x)",
        ],
        "what_keeps_it_from_being_perfect": [
            "Polish minority rights weaker than UK/US — activist leverage is limited",
            "All paths go through the founder's single decision",
            "Land bank valuation is unverified by independent appraiser",
            "Accounting quality 'medium' — WIP may overstate book value",
            "Time horizon is founder-controlled, not market-controlled",
        ],
        "the_honest_summary": (
            "Mirbud is a MEDIUM conviction asset play, not a HIGH conviction one. "
            "It's better than a value trap because there ARE real urgency factors and "
            "real assets. It's worse than a clean activist target because the legal "
            "route to forcing change is limited in Poland.\n\n"
            "The framework correctly scores it 6.7/10. The honest advice: "
            "build a starter (1-2% portfolio) position now, and size UP only when "
            "a specific catalyst event occurs — a confirmed strategic review, "
            "an activist crossing 10%, or a public announcement of asset sale talks. "
            "That event moves Catalyst Clarity from 3.9 to 8.0+, and the total "
            "score jumps from 6.7 to above 8.0 (HIGH conviction)."
        ),
    },
}


# ══════════════════════════════════════════════════════════════════════
# Run full bear case report
# ══════════════════════════════════════════════════════════════════════

def run():
    sep  = "═" * 72
    thin = "─" * 72

    print(f"\n{sep}")
    print("  MIRBUD — BEAR CASE & COUNTERARGUMENT ANALYSIS")
    print(sep)

    # ── Part 1: Why the owner might sell now ────────────────────────
    print("\n\n  PART 1 — WHY THE OWNER MIGHT WANT TO SELL (AND WHY NOW)")
    print(sep)
    for key, item in SELLER_MOTIVATIONS.items():
        urgency_icon = {"HIGH": "🔴", "MEDIUM-HIGH": "🟠", "MEDIUM": "🟡"}.get(item["urgency"], "●")
        print(f"\n  {urgency_icon} [{item['urgency']} URGENCY] {item['title']}")
        print(thin)
        for line in item["rationale"].split("\n"):
            print(f"  {line}")
        if item.get("evidence"):
            print("  Evidence:")
            for e in item["evidence"]:
                print(f"    • {e}")

    # ── Part 2: Bear arguments ───────────────────────────────────────
    print(f"\n\n{sep}")
    print("  PART 2 — WHY MIRBUD MIGHT NOT BE CHEAP AT ALL")
    print("  (Steelmanning the bear case)")
    print(sep)
    for key, attack in BEAR_ARGUMENTS.items():
        p = attack["probability_of_being_correct"]
        bar = "█" * int(p * 10) + "░" * (10 - int(p * 10))
        print(f"\n  {attack['title']}")
        print(f"  Bear conviction: [{bar}] {p*100:.0f}%")
        print(thin)
        for line in attack["argument"].split("\n"):
            print(f"  {line}")
        print(f"\n  Impact if correct: {attack['impact_on_thesis']}")
        print("  Mitigants:")
        for m in attack["mitigants"]:
            print(f"    → {m}")

    # ── Part 3: Species comparison ───────────────────────────────────
    print(f"\n\n{sep}")
    print("  PART 3 — HOW MIRBUD DIFFERS FROM OTHER CHEAP COMPANIES")
    print(sep)
    for key, comparison in SPECIES_COMPARISON.items():
        if key == "mirbud_true_species":
            continue
        print(f"\n  VS: {comparison['example']}")
        print(f"  Superficial similarity: {comparison['superficial_similarity']}")
        print(f"  Key difference:")
        for line in comparison["key_difference"].split("\n"):
            print(f"    {line}")
        print(f"  Diagnostic question: {comparison['diagnostic_question']}")

    # True species
    true = SPECIES_COMPARISON["mirbud_true_species"]
    print(f"\n{sep}")
    print(f"  MIRBUD'S TRUE SPECIES: {true['species']}")
    print(sep)
    print("\n  What makes it a genuine candidate (vs. random cheap):")
    for item in true["what_makes_it_genuine"]:
        print(f"    ✓ {item}")
    print("\n  What keeps it from being HIGH conviction:")
    for item in true["what_keeps_it_from_being_perfect"]:
        print(f"    ✗ {item}")
    print(f"\n  HONEST SUMMARY:")
    for line in true["the_honest_summary"].split("\n"):
        print(f"  {line}")

    # ── Value Trap Analysis ──────────────────────────────────────────
    print(f"\n\n{sep}")
    print("  FORMAL VALUE TRAP ANALYSIS")
    print(sep)

    from examples.mirbud_analysis import mirbud
    trap = detect_trap(
        company=mirbud,
        years_trading_at_discount=5,
        related_party_risk=True,           # Common in Polish family cos
        accounting_quality="medium",       # Construction WIP uncertainty
        activist_path_credible=False,      # Polish law limits activist tools
        sector_structurally_declining=False,
        minority_rights_jurisdiction="medium",
    )
    print_trap_report(trap)


if __name__ == "__main__":
    run()
