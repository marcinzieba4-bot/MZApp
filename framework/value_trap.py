"""
Value Trap Detector
====================
Not every cheap stock is a pivot candidate. Many are "value traps" —
companies that look cheap on paper but have structural reasons to stay cheap
or get cheaper. This module quantifies the trap risk alongside the pivot score.

The central question:  Is the cheapness TEMPORARY (fixable) or PERMANENT (structural)?

A stock is a value trap when:
  - The assets cannot be independently monetised
  - Management extracts value rather than creating it for minorities
  - The discount has persisted for years with no catalyst change
  - Cheapness reflects a structural competitive deterioration, not mispricing

A stock is a genuine pivot candidate when:
  - A specific external force can compel monetisation (activist, acquirer, market event)
  - The founder's incentives are genuinely aligned with a sale NOW (not eventually)
  - Downside is floored by tangible, verifiable, liquid-ish assets
  - Sector tailwinds mean the business isn't deteriorating while you wait
"""

from dataclasses import dataclass, field
from typing import Optional
from .models import Company


# ──────────────────────────────────────────────
# Trap risk flags — each one is a yellow/red flag
# that raises the probability of permanent discount
# ──────────────────────────────────────────────

@dataclass
class TrapFlag:
    name: str
    severity: str           # "yellow" | "red"
    description: str
    mitigant: str           # What would reduce this flag's weight


# ──────────────────────────────────────────────
# Cheap-company species taxonomy
# ──────────────────────────────────────────────

CHEAP_SPECIES = {
    "cigar_butt": {
        "label": "Cigar Butt (Terminal Decline)",
        "description": (
            "Cheap because the business is dying. One last puff of earnings "
            "or asset liquidation, then it goes to zero."
        ),
        "common_sectors": ["Print media", "Physical retail", "Legacy telecoms", "Coal mining"],
        "typical_outcome": "Steady erosion. Cheap today, cheaper tomorrow.",
        "pivot_fit": "Very low — no pivot improves a structurally dying business.",
        "key_differentiator": "Revenue declining >15%/yr with no cost offset",
    },
    "pure_value_trap": {
        "label": "Pure Value Trap (Permanent Family Discount)",
        "description": (
            "Family-controlled, dividends minimal, economic value extracted "
            "via salaries and related-party deals. The 'cheap' is the market "
            "correctly pricing minority shareholders' lack of power."
        ),
        "common_sectors": ["Eastern European industrials", "Asian family conglomerates",
                            "Korean chaebols with cross-holdings"],
        "typical_outcome": "Stays cheap for decades. Occasionally bought out at a small premium.",
        "pivot_fit": "Low unless activist OR founder's incentives change.",
        "key_differentiator": "P/B discount persists >5 years without improvement",
    },
    "quality_at_discount": {
        "label": "Quality at a Discount (Temporarily Depressed)",
        "description": (
            "Great business at a bad price due to temporary headwind "
            "(macro, one-time charge, industry cycle). Earnings power is intact."
        ),
        "common_sectors": ["Consumer staples in recession", "Banks post-crisis",
                            "Travel post-COVID"],
        "typical_outcome": "Re-rates when headwind passes. Safest of the species.",
        "pivot_fit": "Medium — no explicit pivot needed, just time.",
        "key_differentiator": "ROE historically >15%, temp disruption identifiable",
    },
    "asset_play": {
        "label": "Asset Play (Real Assets Above Market Cap)",
        "description": (
            "The business is mediocre but the assets on (or off) the balance sheet "
            "are worth more than the whole company. Value requires monetisation event."
        ),
        "common_sectors": ["Construction with land banks", "Holding companies",
                            "Mining with reserves", "Old-economy real estate"],
        "typical_outcome": "Stays cheap UNTIL a forced monetisation event. IRR depends entirely on timing.",
        "pivot_fit": "HIGH — this IS the classic pivot setup. Mirbud is here.",
        "key_differentiator": "Hidden asset value > market cap, concrete realisability path",
    },
    "activist_target": {
        "label": "Activist Target (Value + External Force)",
        "description": (
            "Any of the above, but an external force (activist, regulatory change, "
            "event-driven catalyst) is credibly positioned to compel change. "
            "This is the highest-conviction version of an asset play."
        ),
        "common_sectors": ["Any, but especially fragmented industries and family cos"],
        "typical_outcome": "Bimodal: home-run (deal done) or slow grind (activist exits).",
        "pivot_fit": "HIGHEST — external catalyst removes founder optionality.",
        "key_differentiator": "Activist with track record, sufficient stake, credible path",
    },
}


# ──────────────────────────────────────────────
# Trap flag detector
# ──────────────────────────────────────────────

@dataclass
class TrapAnalysis:
    company_name: str
    trap_score: float          # 0 (no trap risk) → 10 (definite trap)
    trap_verdict: str          # "CLEAN" | "CAUTION" | "TRAP"
    flags: list[TrapFlag]
    species: str               # Key from CHEAP_SPECIES
    species_detail: dict
    theta_cost_pct_per_year: float   # Hidden IRR drag from waiting (opportunity cost)
    summary: str


def detect_trap(company: Company,
                years_trading_at_discount: Optional[int] = None,
                related_party_risk: bool = False,
                accounting_quality: str = "medium",    # "high" | "medium" | "low"
                activist_path_credible: bool = False,
                sector_structurally_declining: bool = False,
                minority_rights_jurisdiction: str = "medium"  # "strong" | "medium" | "weak"
                ) -> TrapAnalysis:
    """
    Evaluate value-trap risk and identify which species of 'cheap' this company is.

    Args:
        company: Company profile from models.py
        years_trading_at_discount: How long has the P/B discount persisted?
        related_party_risk: Are there known related-party transactions benefiting insiders?
        accounting_quality: Confidence in the reported book value (construction = medium/low)
        activist_path_credible: Can the activist actually force change in this jurisdiction?
        sector_structurally_declining: Is the business model itself under structural threat?
        minority_rights_jurisdiction: How strong are minority shareholder protections?
    """
    flags: list[TrapFlag] = []
    trap_score = 0.0

    # ── Red flags ────────────────────────────────

    if sector_structurally_declining:
        trap_score += 3.0
        flags.append(TrapFlag(
            name="Sector in structural decline",
            severity="red",
            description="The core business model faces permanent headwinds. "
                        "Cheap today, cheaper tomorrow — the asset value erodes too.",
            mitigant="Pivot to entirely different business (rare success rate)",
        ))

    if related_party_risk:
        trap_score += 2.5
        flags.append(TrapFlag(
            name="Related-party extraction risk",
            severity="red",
            description="Economic value is leaking to insiders via salaries, "
                        "loans, property rents, or subsidiary contracts. "
                        "Minority shareholders own the risk, not the reward.",
            mitigant="Activist board seat with veto over RPTs; binding IFRS RPT disclosures",
        ))

    if accounting_quality == "low":
        trap_score += 2.0
        flags.append(TrapFlag(
            name="Accounting quality: LOW",
            severity="red",
            description="Book value is unreliable. Construction WIP accounting "
                        "(percentage-of-completion) can mask loss-making contracts for years. "
                        "P/B ratio may be based on inflated book value.",
            mitigant="Independent RICS valuation of assets; cash flow > net income trend",
        ))
    elif accounting_quality == "medium":
        trap_score += 0.75
        flags.append(TrapFlag(
            name="Accounting quality: MEDIUM",
            severity="yellow",
            description="Some uncertainty in book value (common in construction, "
                        "real estate development). Verify with cash flow metrics.",
            mitigant="FCF conversion ratio > 80% of net income over 3-year average",
        ))

    if minority_rights_jurisdiction == "weak":
        trap_score += 2.0
        flags.append(TrapFlag(
            name="Weak minority shareholder rights",
            severity="red",
            description="Legal framework provides limited recourse for minority investors. "
                        "Activist pressure is a social/reputational tool only — "
                        "the founder can simply ignore it.",
            mitigant="Supranational listing (EU regulated market) adds some protections; "
                     "activist builds to blocking minority (33%+)",
        ))
    elif minority_rights_jurisdiction == "medium":
        trap_score += 0.75
        flags.append(TrapFlag(
            name="Moderate minority protections",
            severity="yellow",
            description="Minority rights exist but are weaker than Anglo-Saxon markets. "
                        "Activism path is slower and less certain.",
            mitigant="Company's reliance on capital markets (bonds, equity) creates "
                     "reputational incentive to treat minorities fairly",
        ))

    # ── Yellow flags ─────────────────────────────

    if years_trading_at_discount and years_trading_at_discount >= 5:
        trap_score += 2.0
        flags.append(TrapFlag(
            name=f"Discount persistent for {years_trading_at_discount}+ years",
            severity="red" if years_trading_at_discount >= 7 else "yellow",
            description="The market has had years to arbitrage this. The fact that it "
                        "hasn't is information — either the market knows something, "
                        "or there's no catalyst in sight.",
            mitigant="Specific new event (activist entry, management change) breaks "
                     "the persistence pattern",
        ))
    elif years_trading_at_discount and years_trading_at_discount >= 3:
        trap_score += 1.0
        flags.append(TrapFlag(
            name=f"Discount persisted {years_trading_at_discount} years",
            severity="yellow",
            description="Some duration of discount — not yet alarming but warrants explanation.",
            mitigant="Identify exactly what is new/different now vs. prior years",
        ))

    if not activist_path_credible and company.insider_ownership_pct and company.insider_ownership_pct > 50:
        trap_score += 1.5
        flags.append(TrapFlag(
            name="Activist path blocked by concentrated ownership",
            severity="yellow",
            description=f"Insider owns {company.insider_ownership_pct:.0f}% — "
                        "activist at 5-10% cannot force change. Board composition, "
                        "dividend policy, and M&A decisions are entirely at founder's discretion.",
            mitigant="Activist reaches 33%+ (blocking minority) or founder actively "
                     "signals sale interest",
        ))

    if company.float_pct and company.float_pct < 20:
        trap_score += 1.0
        flags.append(TrapFlag(
            name="Illiquid float — exit risk",
            severity="yellow",
            description=f"Only {company.float_pct:.0f}% free float. Any position of size "
                        "faces meaningful slippage on exit. Theoretical returns are "
                        "overstated by 10-30% for institutional positions.",
            mitigant="Size position proportionally; ensure thesis resolves via event "
                     "(deal) rather than gradual re-rating",
        ))

    if company.ebitda_margin_pct and company.ebitda_margin_pct < 5:
        trap_score += 0.75
        flags.append(TrapFlag(
            name="Sub-5% EBITDA margins — time pressure",
            severity="yellow",
            description="Thin margins leave little room for error. Any cost shock "
                        "(material prices, labor) can flip the company to cash-burning. "
                        "The waiting period becomes expensive.",
            mitigant="Backlog visibility covers 2+ years; working capital facilities secured",
        ))

    # ── Trap verdict ─────────────────────────────

    trap_score = min(trap_score, 10.0)

    if trap_score >= 7.0:
        verdict = "TRAP"
    elif trap_score >= 4.0:
        verdict = "CAUTION"
    else:
        verdict = "CLEAN"

    # ── Species classification ────────────────────

    if sector_structurally_declining:
        species = "cigar_butt"
    elif (not activist_path_credible and
          related_party_risk and
          years_trading_at_discount and years_trading_at_discount >= 5):
        species = "pure_value_trap"
    elif activist_path_credible:
        species = "activist_target"
    elif (company.book_value_per_share and
          company.current_price / company.book_value_per_share < 0.8 and
          company.hidden_asset_value_per_share):
        species = "asset_play"
    else:
        species = "quality_at_discount"

    # ── Theta cost (opportunity cost of waiting) ──────────────────

    # Risk-free rate in Poland ~5.5% (NBP reference rate area).
    # Every year the thesis doesn't fire costs you ~5-6% in opportunity cost.
    risk_free_rate = 5.5
    theta_cost_pct_per_year = risk_free_rate  # Simplified: full opportunity cost

    # ── Summary ──────────────────────────────────

    red_count    = sum(1 for f in flags if f.severity == "red")
    yellow_count = sum(1 for f in flags if f.severity == "yellow")
    summary = (
        f"{verdict}: Trap score {trap_score:.1f}/10. "
        f"{red_count} red flag(s), {yellow_count} yellow flag(s). "
        f"Species: {CHEAP_SPECIES[species]['label']}. "
        f"Theta cost: ~{theta_cost_pct_per_year:.1f}%/year opportunity cost while waiting."
    )

    return TrapAnalysis(
        company_name=company.name,
        trap_score=trap_score,
        trap_verdict=verdict,
        flags=flags,
        species=species,
        species_detail=CHEAP_SPECIES[species],
        theta_cost_pct_per_year=theta_cost_pct_per_year,
        summary=summary,
    )


def print_trap_report(analysis: TrapAnalysis) -> None:
    sep  = "═" * 72
    thin = "─" * 72

    verdict_color = {"CLEAN": "✓", "CAUTION": "⚠", "TRAP": "✗"}[analysis.trap_verdict]

    print(f"\n{sep}")
    print(f"  VALUE TRAP ANALYSIS — {analysis.company_name}")
    print(sep)
    print(f"  Trap Score   : {analysis.trap_score:.1f} / 10   "
          f"{verdict_color} {analysis.trap_verdict}")
    print(f"  Theta Cost   : ~{analysis.theta_cost_pct_per_year:.1f}% per year (opportunity cost while waiting)")
    print(f"\n  Species: {analysis.species_detail['label']}")
    print(f"  {analysis.species_detail['description']}")
    print(f"  Typical outcome: {analysis.species_detail['typical_outcome']}")
    print(f"  Pivot fit:       {analysis.species_detail['pivot_fit']}")

    print(f"\n{thin}")
    print("  FLAGS")
    print(thin)
    for flag in analysis.flags:
        icon = "🔴" if flag.severity == "red" else "🟡"
        print(f"\n  {icon} [{flag.severity.upper()}] {flag.name}")
        print(f"     {flag.description}")
        print(f"     Mitigant: {flag.mitigant}")

    print(f"\n{thin}")
    print("  VERDICT")
    print(thin)
    print(f"  {analysis.summary}")
    print(f"\n{sep}\n")
