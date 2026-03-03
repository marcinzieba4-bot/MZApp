"""
Core data models for the Pivot Opportunity Framework.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ──────────────────────────────────────────────
# Enumerations
# ──────────────────────────────────────────────

class PivotType(Enum):
    """
    The mechanism by which value gets unlocked.

    ASSET_RELEASE       - Company sits on undervalued/hidden assets (land bank,
                          real estate at historical cost, IP, cash).
                          Pivot = sale, spinoff, or revaluation event.

    OWNERSHIP_CHANGE    - Family/founder sells to PE, strategic buyer, or
                          activist forces a transaction. Typical premium 30-60%.

    OPERATIONAL_TURN    - New management cuts bloat, improves margins.
                          Often follows activist accumulation.

    STRATEGIC_REPOSITION- Company exits low-margin segment, enters higher-value
                          market. Often triggered by CEO change or M&A.

    CAPITAL_STRUCTURE   - Leverage reduction, buybacks, or special dividend
                          unlocks value that was hidden by suboptimal balance sheet.

    REGULATORY_WINDFALL - Policy change, deregulation, or subsidy creates a
                          sudden tailwind (e.g. energy, healthcare, construction).

    CONSOLIDATION       - Industry rolls up; company is either acquirer building
                          scale or the obvious acquisition target.

    TECH_ADOPTION       - Legacy company adopts technology ahead of peers,
                          re-rates from value to growth multiple.
    """
    ASSET_RELEASE       = "asset_release"
    OWNERSHIP_CHANGE    = "ownership_change"
    OPERATIONAL_TURN    = "operational_turn"
    STRATEGIC_REPOSITION = "strategic_reposition"
    CAPITAL_STRUCTURE   = "capital_structure"
    REGULATORY_WINDFALL = "regulatory_windfall"
    CONSOLIDATION       = "consolidation"
    TECH_ADOPTION       = "tech_adoption"


class SignalStrength(Enum):
    """How loud the signal is. Combine multiple STRONG signals for highest conviction."""
    WEAK     = 1   # Interesting but not actionable alone
    MODERATE = 2   # Meaningful, warrants research
    STRONG   = 3   # High conviction signal; few of these matter more than many weak ones
    DEFINITIVE = 4 # Event has occurred / is confirmed (e.g. 13D filed, deal announced)


class RiskLevel(Enum):
    LOW    = "low"
    MEDIUM = "medium"
    HIGH   = "high"


# ──────────────────────────────────────────────
# Signal primitives
# ──────────────────────────────────────────────

@dataclass
class PivotSignal:
    """
    A single observable fact that suggests a pivot may be underway.
    Signals compound — the framework scores their aggregate weight.
    """
    name: str
    description: str
    strength: SignalStrength
    category: str                    # "smart_money" | "fundamentals" | "catalyst" | "sentiment"
    source: Optional[str] = None     # Where you found it (filing, news, analyst note)
    confidence: float = 1.0          # 0-1 modifier on strength if uncertain


@dataclass
class PriceScenario:
    """
    One branch of the probability-weighted outcome tree.
    The framework computes asymmetry from the spread of these scenarios.
    """
    label: str           # "base" | "bull" | "bear"
    price_target: float  # Absolute price target or NAV estimate
    probability: float   # Must sum to 1.0 across all scenarios for a company
    rationale: str
    time_horizon_years: float = 3.0
    irr: Optional[float] = None      # Annualised return at this scenario price


# ──────────────────────────────────────────────
# Main company model
# ──────────────────────────────────────────────

@dataclass
class Company:
    """
    Full profile of a pivot candidate.
    Populate from public filings, market data, and field research.
    """
    # Identity
    name: str
    ticker: Optional[str]
    exchange: Optional[str]
    sector: str
    country: str

    # Price / size
    current_price: float
    market_cap_m: float              # Market cap in millions (local currency)
    currency: str = "USD"

    # Balance sheet anchors
    book_value_per_share: Optional[float] = None
    net_cash_per_share: Optional[float] = None
    hidden_asset_value_per_share: Optional[float] = None   # Analyst estimate of off-book value

    # Earnings profile
    ebitda_margin_pct: Optional[float] = None
    revenue_growth_yoy_pct: Optional[float] = None
    roe_pct: Optional[float] = None

    # Ownership
    insider_ownership_pct: Optional[float] = None
    institutional_ownership_pct: Optional[float] = None
    float_pct: Optional[float] = None                      # Tradeable float as % of shares out

    # Signals and thesis
    pivot_types: list[PivotType] = field(default_factory=list)
    signals: list[PivotSignal] = field(default_factory=list)
    scenarios: list[PriceScenario] = field(default_factory=list)

    # Qualitative
    thesis_summary: str = ""
    key_risks: list[str] = field(default_factory=list)
    time_horizon_years: float = 3.0

    # Computed (filled by scoring engine)
    pivot_score: Optional[float] = None
    asymmetry_ratio: Optional[float] = None
    conviction_tier: Optional[str] = None     # "HIGH" | "MEDIUM" | "WATCH"


# ──────────────────────────────────────────────
# Scoring dimension weights (tunable)
# ──────────────────────────────────────────────

@dataclass
class ScoringWeights:
    """
    Controls the relative importance of each scoring dimension.
    Calibrate these weights by back-testing against known pivots.
    Default weights are informed by Mirbud-style situations.
    """
    asset_asymmetry: float    = 0.25   # How much hidden / undervalued asset exists
    smart_money_signals: float = 0.25  # Quality of institutional interest signals
    catalyst_clarity: float   = 0.20  # How concrete and near-term is the trigger
    downside_protection: float = 0.15  # How floored is the bear case
    business_quality: float   = 0.10  # Core business can survive while we wait
    sentiment_discount: float = 0.05  # More ignored = more opportunity

    def validate(self) -> bool:
        total = (self.asset_asymmetry + self.smart_money_signals +
                 self.catalyst_clarity + self.downside_protection +
                 self.business_quality + self.sentiment_discount)
        return abs(total - 1.0) < 0.001
