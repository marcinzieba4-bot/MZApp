"""
Pivot Type Playbooks
====================
Each pivot type has a characteristic pattern of signals, typical time horizons,
base-rate success odds, and example archetypes.

Use these playbooks to:
  1. Quickly triage which pivot thesis fits a company
  2. Know which signals to hunt for
  3. Set realistic return and time expectations
"""

from dataclasses import dataclass, field
from .models import PivotType, SignalStrength


@dataclass
class PivotPlaybook:
    pivot_type: PivotType
    one_liner: str
    how_value_unlocks: str
    key_signals_to_find: list[str]
    typical_return_range: str     # e.g. "30–100%"
    typical_horizon_years: str    # e.g. "1–3"
    base_rate_success: str        # rough historical success rate
    main_risks: list[str]
    archetypes: list[str]         # famous/pattern examples


PLAYBOOKS: dict[PivotType, PivotPlaybook] = {

    PivotType.ASSET_RELEASE: PivotPlaybook(
        pivot_type=PivotType.ASSET_RELEASE,
        one_liner="Company owns more than it shows — a sale or revaluation closes the gap.",
        how_value_unlocks=(
            "Assets held at historical cost (real estate, land, IP, equity stakes) "
            "are sold, separately listed, or revalued. Gap between book and market shrinks."
        ),
        key_signals_to_find=[
            "P/B below 0.7 in asset-heavy sector (construction, real estate, holding co.)",
            "Land bank or property portfolio last appraised >5 years ago",
            "Subsidiaries or equity stakes larger than parent's market cap",
            "Management starts talking about 'capital allocation' or 'portfolio review'",
            "Activist files Schedule 13D citing asset undervaluation",
            "Real estate arm contributes >30% EBITDA but <10% of stated book",
        ],
        typical_return_range="50–200%",
        typical_horizon_years="2–4",
        base_rate_success="~55%",
        main_risks=[
            "Management refuses to unlock assets (entrenched founder)",
            "Market turns before the sale completes (valuation gap widens then closes lower)",
            "Hidden liabilities offset the hidden assets",
            "Tax drag on asset sale consumes most of the gain",
        ],
        archetypes=[
            "Hong Kong holdcos (Henderson Land, Wharf)",
            "Japanese asset plays pre-Buffett (ITOCHU, Marubeni)",
            "Polish construction companies with land banks (Mirbud pattern)",
            "European family conglomerates with listed sub-stakes",
        ],
    ),

    PivotType.OWNERSHIP_CHANGE: PivotPlaybook(
        pivot_type=PivotType.OWNERSHIP_CHANGE,
        one_liner="Control of the company changes hands at a premium.",
        how_value_unlocks=(
            "A buyout (PE, strategic, or management), merger, or activist-forced "
            "sale crystallises value that the market was discounting due to poor capital "
            "allocation, family discount, or strategic misfit."
        ),
        key_signals_to_find=[
            "Hedge fund / PE firm crosses 5% ownership threshold (13D / equivalent filing)",
            "Founder/family aged 65+ with no clear succession plan",
            "Company consistently trades at discount to peers with no stated reason",
            "Peer companies in same sector recently acquired at 30-60% premiums",
            "CEO change to outsider with M&A track record",
            "Informal market rumours confirmed by volume/option spikes",
            "Company hires investment bank for 'strategic review'",
        ],
        typical_return_range="30–80% (takeover premium)",
        typical_horizon_years="0.5–2",
        base_rate_success="~65% when 13D filed by credible activist",
        main_risks=[
            "Antitrust blocks deal",
            "Founder refuses to sell (protective share structure)",
            "Buyer walks away — stock crashes back to pre-rumour levels",
            "Leveraged buyout leaves company over-indebted post-close",
        ],
        archetypes=[
            "Mirbud (hedge funds accumulating, family may sell)",
            "Classic Icahn / Elliott targets",
            "FTSE 250 companies taken private 2010-2020",
            "Family-owned mid-caps in Poland, Italy, Korea, Japan",
        ],
    ),

    PivotType.OPERATIONAL_TURN: PivotPlaybook(
        pivot_type=PivotType.OPERATIONAL_TURN,
        one_liner="Bad management leaves; new team cuts costs and the margin gap to peers closes.",
        how_value_unlocks=(
            "EBITDA margin expands from sub-peer to peer-level. Same revenue, "
            "dramatically higher earnings. Multiple expansion follows as market "
            "re-rates from 'broken' to 'normal'."
        ),
        key_signals_to_find=[
            "EBITDA margin 5–10pp below sector peers for 3+ years",
            "New CEO hire with a track record of operational improvement",
            "Activist takes board seat focused on cost efficiency",
            "Headcount or SG&A well above industry benchmarks",
            "Recent plant closures, division sales, or restructuring announcements",
            "Insiders buying shares after new management announcement",
        ],
        typical_return_range="100–300% (earnings leverage amplifies multiple expansion)",
        typical_horizon_years="2–4",
        base_rate_success="~45% (hardest to execute, highest reward)",
        main_risks=[
            "New management fails to improve margins (structural problem, not operational)",
            "Revenue falls faster than costs are cut",
            "Culture/union resistance to restructuring",
            "Over-levered balance sheet limits management options",
        ],
        archetypes=[
            "GE under Larry Culp (industrial operational turn)",
            "Vodafone under Margherita Della Valle",
            "Many PE portfolio companies post-carve-out",
            "Eastern European industrials with German-style operational upside",
        ],
    ),

    PivotType.STRATEGIC_REPOSITION: PivotPlaybook(
        pivot_type=PivotType.STRATEGIC_REPOSITION,
        one_liner="Company exits a low-value segment and doubles down on a higher-value one.",
        how_value_unlocks=(
            "Revenue mix shifts toward higher-margin or faster-growing business. "
            "Market assigns a higher multiple to the surviving/dominant business. "
            "Often involves divesting a drag business that was hiding the gem."
        ),
        key_signals_to_find=[
            "Company operating in 2+ distinct segments with very different margins",
            "Low-margin segment consuming >50% of management time / capex",
            "New strategy presentation emphasising 'focus' or 'simplification'",
            "Sale or IPO of non-core division announced",
            "Peer pure-plays trade at 40%+ premium to this conglomerate",
            "New CEO hired from a pure-play competitor",
        ],
        typical_return_range="80–250%",
        typical_horizon_years="2–5",
        base_rate_success="~50%",
        main_risks=[
            "Execution risk in new market (under-estimated competition)",
            "Transition period burns cash before new model proves out",
            "Market doesn't re-rate as expected post-divestiture",
        ],
        archetypes=[
            "Danaher (scientific instruments pivot from industrial)",
            "IAC (continuous carve-out / spin-off model)",
            "Nokia (network equipment pivot from mobile phones)",
        ],
    ),

    PivotType.CAPITAL_STRUCTURE: PivotPlaybook(
        pivot_type=PivotType.CAPITAL_STRUCTURE,
        one_liner="Balance sheet optimisation — debt paydown, buybacks, or special dividends unlock equity value.",
        how_value_unlocks=(
            "Excess cash / debt paydown deleverages the equity story. "
            "Buybacks reduce share count so per-share value rises. "
            "Special dividends return trapped cash. All three re-rate the stock."
        ),
        key_signals_to_find=[
            "Net cash > 30% of market cap with no stated use of proceeds",
            "FCF yield > 10% with buyback program announced or rumoured",
            "Debt covenant breach being resolved → equity value swings dramatically",
            "Activist letter demanding capital return",
            "Management uses language like 'return excess capital' or 'optimal leverage'",
            "Recent debt refinancing at lower rate freeing up cash flow",
        ],
        typical_return_range="30–100%",
        typical_horizon_years="1–3",
        base_rate_success="~60%",
        main_risks=[
            "Cash is deployed in a value-destructive acquisition instead",
            "Operating losses erode the cash before it's returned",
            "Debt markets freeze before refinancing completes",
        ],
        archetypes=[
            "Japanese cash-heavy companies post-TSE governance reforms",
            "Post-LBO companies hitting leverage targets and switching to buybacks",
            "Mining companies post-commodity cycle (BHP, Rio 2015–2020)",
        ],
    ),

    PivotType.REGULATORY_WINDFALL: PivotPlaybook(
        pivot_type=PivotType.REGULATORY_WINDFALL,
        one_liner="A policy change creates sudden, unpriced tailwind for a specific sector.",
        how_value_unlocks=(
            "Regulation lifts a structural ceiling (price cap removed, subsidy introduced, "
            "competitor banned). Companies with sunk-cost infrastructure or licences "
            "benefit disproportionately — the capex is already spent."
        ),
        key_signals_to_find=[
            "Pending legislation with specific deadline / election catalyst",
            "Industry lobbying success signals (trade association statements)",
            "Company's revenue structure perfectly positioned for new rule",
            "Competitors cannot quickly replicate the company's regulatory position",
            "Market has not priced the change because the bill hasn't passed yet",
        ],
        typical_return_range="50–400% (binary, like an option)",
        typical_horizon_years="0.5–3",
        base_rate_success="~40% (high variance, size small positions)",
        main_risks=[
            "Regulation fails to pass / reversed",
            "Windfall tax introduced to claw back gains",
            "Sector re-rates quickly — early mover matters",
        ],
        archetypes=[
            "US cannabis companies pre/post state legalisation",
            "European renewable energy companies during FIT subsidy wave",
            "Eastern European construction companies around EU fund cycles",
        ],
    ),

    PivotType.CONSOLIDATION: PivotPlaybook(
        pivot_type=PivotType.CONSOLIDATION,
        one_liner="Fragmented industry rolls up — company is acquirer building scale or the next target.",
        how_value_unlocks=(
            "Either the company buys cheap peers and accretes earnings "
            "(roll-up acquirer) or it gets bought at a control premium "
            "as larger players consolidate the space."
        ),
        key_signals_to_find=[
            "Industry HHI still fragmented (top 5 players < 50% market share)",
            "Recent M&A at 8–12x EBITDA in the same sector",
            "Company is #3 or #4 in a market where #1 has stated consolidation strategy",
            "Access to cheap acquisition financing (low rates, strong stock)",
            "Serial acquirer in adjacent space moving into this market",
        ],
        typical_return_range="40–100%",
        typical_horizon_years="1–3",
        base_rate_success="~55%",
        main_risks=[
            "Integration failures erode synergies",
            "Overpaying for acquisitions destroys acquirer value",
            "Antitrust review delays or blocks",
        ],
        archetypes=[
            "European waste management (Renewi, Biffa)",
            "Polish building materials (Saint-Gobain roll-up of CEE)",
            "Funeral services, veterinary clinics, dental — any fragmented service sector",
        ],
    ),

    PivotType.TECH_ADOPTION: PivotPlaybook(
        pivot_type=PivotType.TECH_ADOPTION,
        one_liner="Legacy company adopts technology ahead of peers — re-rates from value to growth multiple.",
        how_value_unlocks=(
            "Operating leverage from automation/AI/platform technology expands margins. "
            "Market re-rates the stock from a 'legacy' PE to a 'tech-enabled' PE. "
            "The multiple expansion is often as large as the earnings improvement."
        ),
        key_signals_to_find=[
            "Company piloting AI/automation with measurable productivity gain",
            "Tech partnership with a credible platform player (AWS, Microsoft, Salesforce)",
            "CTO/CDO hired from a tech-native company",
            "Competitors are analog — first mover advantage in digitisation",
            "Management calls out 'tech investment' yielding ROI above cost of capital",
        ],
        typical_return_range="100–500% (multiple expansion + earnings growth compound)",
        typical_horizon_years="3–7",
        base_rate_success="~35% (execution risk is highest here)",
        main_risks=[
            "Tech investment produces no measurable return",
            "Disruption accelerates faster than the company can adapt",
            "Wrong technology bet (over-invests in deprecated stack)",
            "Legacy workforce resists change, slowing implementation",
        ],
        archetypes=[
            "John Deere (agriculture → precision farming platform)",
            "Domino's Pizza (food delivery → tech company re-rate)",
            "Commonplace in traditional industries: banking, logistics, manufacturing",
        ],
    ),
}


def get_playbook(pivot_type: PivotType) -> PivotPlaybook:
    return PLAYBOOKS[pivot_type]


def suggest_pivot_types(company) -> list[PivotType]:
    """
    Heuristic: given a company's data, suggest which pivot playbooks fit best.
    Returns a ranked list (most likely first).
    """
    suggestions = []

    # Asset release: asset-heavy + P/B discount
    if (company.book_value_per_share and
            company.current_price / company.book_value_per_share < 0.8):
        suggestions.append((PivotType.ASSET_RELEASE, 3))

    if company.hidden_asset_value_per_share:
        suggestions.append((PivotType.ASSET_RELEASE, 2))

    # Ownership change: smart money signals
    smart_money = [s for s in company.signals if s.category == "smart_money"]
    if any(s.strength in (SignalStrength.STRONG, SignalStrength.DEFINITIVE)
           for s in smart_money):
        suggestions.append((PivotType.OWNERSHIP_CHANGE, 3))

    # Operational turn: low margins
    if (company.ebitda_margin_pct is not None and
            company.ebitda_margin_pct < 8):
        suggestions.append((PivotType.OPERATIONAL_TURN, 2))

    # Capital structure: net cash heavy
    if (company.net_cash_per_share and company.current_price and
            company.net_cash_per_share / company.current_price > 0.3):
        suggestions.append((PivotType.CAPITAL_STRUCTURE, 2))

    # Consolidation: catalyst signals related to M&A
    catalyst = [s for s in company.signals if s.category == "catalyst"]
    if any("acqui" in s.name.lower() or "merger" in s.name.lower()
           or "consolidat" in s.name.lower() for s in catalyst):
        suggestions.append((PivotType.CONSOLIDATION, 2))

    # Aggregate and rank
    from collections import defaultdict
    score_map: dict[PivotType, int] = defaultdict(int)
    for pt, score in suggestions:
        score_map[pt] += score

    return [pt for pt, _ in sorted(score_map.items(),
                                   key=lambda x: x[1], reverse=True)]
