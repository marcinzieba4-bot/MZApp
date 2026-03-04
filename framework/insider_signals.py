"""
Insider Signal Analysis
========================
Formalises the analysis of insider transactions reported via:
  - ESPI (Poland / WSE)     — 3-business-day reporting under MAR
  - PDMR filings (UK / FCA) — under MAR Regulation
  - SEC Form 4 (US)          — within 2 business days of transaction

Why insider cluster buying is one of the strongest signals in investing:
  1. Multiple independent decision-makers agree the stock is cheap
  2. Legally barred from trading on MNPI → only buy when confident
  3. Open-market cash purchases ≠ option exercises or inheritance
  4. Pattern: insiders buy at 52-week lows, BEFORE recovery; not after
  5. On the WSE (less efficient market), signal decays slowly (~6-12 months)

Sources for Polish insider data:
  - gpw.pl/espi-ebi-reports (ESPI portal — all PDMR/insider transactions)
  - notoria.fis.pl (aggregator of ESPI filings, searchable)
  - Polish SEC equivalent: UKNF.gov.pl notifications

Cluster definition used here:
  CLUSTER = ≥2 different insiders buying within the same 30-day window
  STRONG CLUSTER = ≥3 insiders, or ≥2 with CEO/CFO included, same 30-day window
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import date, timedelta
from enum import Enum


class InsiderRole(Enum):
    CEO           = "CEO / President"
    CFO           = "CFO / Finance Director"
    COO           = "COO / Operations"
    BOARD_EXEC    = "Executive Board Member"
    SUPERVISORY   = "Supervisory Board Member"
    MAJOR_SHAREHOLDER = "Major Shareholder (>5%)"
    RELATED_PARTY = "Related Party (family member, affiliate)"


class TransactionType(Enum):
    OPEN_MARKET_BUY   = "open_market_buy"     # Strongest signal
    OPEN_MARKET_SELL  = "open_market_sell"     # Potential negative signal
    OPTION_EXERCISE   = "option_exercise"      # Weak signal (forced)
    INHERITANCE       = "inheritance"          # No signal
    GIFT              = "gift"                 # No signal
    PERFORMANCE_SHARE = "performance_share"    # Weak signal (granted)


@dataclass
class InsiderTransaction:
    """Single insider transaction as filed with regulator."""
    insider_name:     str
    role:             InsiderRole
    transaction_type: TransactionType
    date:             date
    shares:           int
    price_per_share:  float            # In local currency
    total_value:      float            # In local currency (shares × price)
    currency:         str = "PLN"
    espi_reference:   str = ""         # ESPI report number or Form 4 accession
    notes:            str = ""

    @property
    def is_buy_signal(self) -> bool:
        """True if this transaction is a genuine buy signal."""
        return self.transaction_type == TransactionType.OPEN_MARKET_BUY

    @property
    def signal_weight(self) -> float:
        """Weight of this transaction as a buy signal (0-1)."""
        weights = {
            TransactionType.OPEN_MARKET_BUY:   1.0,
            TransactionType.OPEN_MARKET_SELL:  0.0,  # Counted separately
            TransactionType.OPTION_EXERCISE:   0.2,
            TransactionType.PERFORMANCE_SHARE: 0.1,
            TransactionType.INHERITANCE:       0.0,
            TransactionType.GIFT:              0.0,
        }
        return weights[self.transaction_type]

    @property
    def role_weight(self) -> float:
        """Higher weight for more senior insiders."""
        weights = {
            InsiderRole.CEO:              1.0,
            InsiderRole.CFO:              0.90,
            InsiderRole.COO:              0.80,
            InsiderRole.BOARD_EXEC:       0.70,
            InsiderRole.SUPERVISORY:      0.60,
            InsiderRole.MAJOR_SHAREHOLDER:0.70,
            InsiderRole.RELATED_PARTY:    0.40,
        }
        return weights[self.role]


@dataclass
class InsiderCluster:
    """A group of transactions within a defined window = a 'cluster'."""
    company_name:       str
    ticker:             str
    exchange:           str
    transactions:       list    # list[InsiderTransaction]
    window_days:        int = 30          # Default: 30-day window
    current_price:      float = 0.0
    price_52w_high:     float = 0.0
    price_52w_low:      float = 0.0
    currency:           str = "PLN"

    # Computed by analyse_cluster()
    cluster_score:      float = 0.0
    signal_strength:    str = ""
    conviction_tier:    str = ""
    notes:              list = field(default_factory=list)

    @property
    def buy_transactions(self) -> list:
        return [t for t in self.transactions if t.is_buy_signal]

    @property
    def sell_transactions(self) -> list:
        return [t for t in self.transactions
                if t.transaction_type == TransactionType.OPEN_MARKET_SELL]

    @property
    def n_buyers(self) -> int:
        return len(set(t.insider_name for t in self.buy_transactions))

    @property
    def n_sellers(self) -> int:
        return len(set(t.insider_name for t in self.sell_transactions))

    @property
    def total_buy_value(self) -> float:
        return sum(t.total_value for t in self.buy_transactions)

    @property
    def total_sell_value(self) -> float:
        return sum(t.total_value for t in self.sell_transactions)

    @property
    def avg_buy_price(self) -> float:
        buys = self.buy_transactions
        if not buys:
            return 0.0
        total_shares = sum(t.shares for t in buys)
        total_value  = sum(t.total_value for t in buys)
        return total_value / total_shares if total_shares else 0.0

    @property
    def has_c_suite_buyer(self) -> bool:
        """True if CEO or CFO is in the buying cluster."""
        senior = {InsiderRole.CEO, InsiderRole.CFO, InsiderRole.COO}
        return any(t.role in senior for t in self.buy_transactions)

    @property
    def buy_vs_52w_low_pct(self) -> Optional[float]:
        """How much above 52-week low is the avg buy price?"""
        if self.price_52w_low <= 0 or self.avg_buy_price <= 0:
            return None
        return (self.avg_buy_price - self.price_52w_low) / self.price_52w_low

    @property
    def buy_vs_52w_high_pct(self) -> Optional[float]:
        """How much below 52-week high is the avg buy price?"""
        if self.price_52w_high <= 0 or self.avg_buy_price <= 0:
            return None
        return (self.price_52w_high - self.avg_buy_price) / self.price_52w_high


def analyse_cluster(cluster: InsiderCluster) -> InsiderCluster:
    """
    Score and classify an insider cluster.
    Returns the cluster with score, signal_strength, and conviction_tier filled in.
    """
    buys    = cluster.buy_transactions
    sells   = cluster.sell_transactions
    notes   = []
    score   = 0.0

    if not buys:
        cluster.cluster_score   = 0.0
        cluster.signal_strength = "NO_SIGNAL"
        cluster.conviction_tier = "IGNORE"
        cluster.notes           = ["No open-market buy transactions in cluster"]
        return cluster

    # ── 1. Number of independent buyers ───────────────────────────
    n = cluster.n_buyers
    if n >= 4:
        score += 4.0; notes.append(f"{n} independent insiders buying — exceptional cluster")
    elif n == 3:
        score += 3.0; notes.append(f"{n} independent insiders buying — strong cluster")
    elif n == 2:
        score += 1.5; notes.append(f"{n} independent insiders buying — cluster signal")
    else:
        score += 0.5; notes.append("Single insider buying — weak individual signal")

    # ── 2. C-suite participation ───────────────────────────────────
    if cluster.has_c_suite_buyer:
        score += 2.0; notes.append("CEO/CFO/COO included — highest-conviction signal")

    # ── 3. Total buy value (materiality) ──────────────────────────
    buy_val = cluster.total_buy_value
    if buy_val >= 5_000_000:
        score += 2.5; notes.append(f"Total buy: {cluster.currency} {buy_val/1e6:.1f}m — very material")
    elif buy_val >= 1_000_000:
        score += 1.5; notes.append(f"Total buy: {cluster.currency} {buy_val/1e6:.1f}m — material")
    elif buy_val >= 200_000:
        score += 0.5; notes.append(f"Total buy: {cluster.currency} {buy_val/1000:.0f}k — moderate")
    else:
        score -= 0.5; notes.append(f"Total buy: {cluster.currency} {buy_val/1000:.0f}k — token size, weak signal")

    # ── 4. Buy price vs 52-week range ─────────────────────────────
    if cluster.buy_vs_52w_high_pct is not None:
        discount_from_high = cluster.buy_vs_52w_high_pct
        if discount_from_high > 0.40:
            score += 2.0; notes.append(f"Buying {discount_from_high:.0%} below 52w high — deep discount = brave signal")
        elif discount_from_high > 0.20:
            score += 1.0; notes.append(f"Buying {discount_from_high:.0%} below 52w high — significant discount")
        elif discount_from_high < 0.05:
            score -= 1.0; notes.append("Buying near 52-week high — less contrarian conviction")

    if cluster.buy_vs_52w_low_pct is not None:
        premium_to_low = cluster.buy_vs_52w_low_pct
        if premium_to_low < 0.10:
            score += 1.0; notes.append(f"Buying near 52-week low ({premium_to_low:.0%} above) — classic contrarian buy")

    # ── 5. Offsetting sells ────────────────────────────────────────
    if cluster.n_sellers > 0:
        sell_val = cluster.total_sell_value
        if sell_val > buy_val * 0.5:
            score -= 2.0; notes.append(f"WARNING: {cluster.n_sellers} insider(s) selling — net signal is mixed")
        else:
            score -= 0.5; notes.append(f"Minor offsetting selling ({cluster.currency} {sell_val/1000:.0f}k)")

    # ── 6. Role quality score ─────────────────────────────────────
    role_weighted = sum(t.role_weight * t.signal_weight * t.total_value
                        for t in buys)
    role_score = role_weighted / max(buy_val, 1)
    if role_score > 0.80:
        score += 0.5; notes.append("Buying dominated by C-suite / exec board")

    # Clamp
    score = max(0.0, min(10.0, score))
    cluster.cluster_score = round(score, 2)
    cluster.notes = notes

    # Classify
    if score >= 7.0:
        cluster.signal_strength = "DEFINITIVE_BUY_CLUSTER"
        cluster.conviction_tier = "ACT"
    elif score >= 5.0:
        cluster.signal_strength = "STRONG_CLUSTER"
        cluster.conviction_tier = "INVESTIGATE"
    elif score >= 3.0:
        cluster.signal_strength = "MODERATE_CLUSTER"
        cluster.conviction_tier = "WATCH"
    elif score >= 1.0:
        cluster.signal_strength = "WEAK_SIGNAL"
        cluster.conviction_tier = "LOG"
    else:
        cluster.signal_strength = "NO_SIGNAL"
        cluster.conviction_tier = "IGNORE"

    return cluster


def print_insider_cluster_report(cluster: InsiderCluster):
    if cluster.cluster_score == 0.0 and not cluster.notes:
        cluster = analyse_cluster(cluster)

    sep  = "═" * 76
    thin = "─" * 76

    print(f"\n{sep}")
    print(f"  INSIDER CLUSTER ANALYSIS — {cluster.company_name} ({cluster.ticker}:{cluster.exchange})")
    print(sep)
    print(f"\n  Cluster Score   : {cluster.cluster_score:.1f} / 10.0  "
          f"  Signal: {cluster.signal_strength}")
    print(f"  Conviction Tier : {cluster.conviction_tier}")
    print(f"  Window          : {cluster.window_days}-day")
    print(f"  Buyers          : {cluster.n_buyers} independent insiders")
    print(f"  Total Buy Value : {cluster.currency} {cluster.total_buy_value/1_000_000:.2f}m")
    if cluster.sell_transactions:
        print(f"  Total Sell Value: {cluster.currency} {cluster.total_sell_value/1_000_000:.2f}m "
              f"  ⚠ ({cluster.n_sellers} sellers)")
    print(f"  Avg Buy Price   : {cluster.currency} {cluster.avg_buy_price:.2f}")
    if cluster.current_price > 0:
        premium = (cluster.current_price / cluster.avg_buy_price - 1) * 100
        print(f"  Current Price   : {cluster.currency} {cluster.current_price:.2f}  "
              f"({'+' if premium >= 0 else ''}{premium:.1f}% vs avg buy)")
    if cluster.price_52w_high > 0:
        print(f"  52-Week Range   : {cluster.currency} {cluster.price_52w_low:.2f} – "
              f"{cluster.currency} {cluster.price_52w_high:.2f}")
        if cluster.buy_vs_52w_high_pct is not None:
            print(f"  Buy price is {cluster.buy_vs_52w_high_pct:.0%} below 52-week high")

    print(f"\n{thin}")
    print("  ANALYSIS NOTES")
    print(thin)
    for note in cluster.notes:
        prefix = "  ✓" if "WARNING" not in note else "  ✗"
        print(f"{prefix}  {note}")

    print(f"\n{thin}")
    print("  INDIVIDUAL TRANSACTIONS")
    print(thin)
    print(f"\n  {'Date':<12} {'Insider':<25} {'Role':<20} {'Type':<20} "
          f"{'Shares':>10} {'Price':>10} {'Value (k)':>12}")
    print(f"  {'-'*12} {'-'*25} {'-'*20} {'-'*20} {'-'*10} {'-'*10} {'-'*12}")

    for t in sorted(cluster.transactions, key=lambda x: x.date):
        type_str = "BUY" if t.transaction_type == TransactionType.OPEN_MARKET_BUY else (
            "SELL" if t.transaction_type == TransactionType.OPEN_MARKET_SELL else
            t.transaction_type.value[:12]
        )
        flag = " ✓" if t.is_buy_signal else ("  ✗" if t.transaction_type == TransactionType.OPEN_MARKET_SELL else "")
        print(f"  {str(t.date):<12} {t.insider_name[:25]:<25} {t.role.value[:20]:<20} "
              f"{type_str:<20} {t.shares:>10,} {t.price_per_share:>10.2f} "
              f"{t.total_value/1000:>10.0f}k{flag}")

    print(f"\n{thin}")
    print("  INTERPRETATION")
    print(thin)

    tier_text = {
        "ACT":         "  → Multiple insiders buying in size — strong pre-catalyst signal. INVESTIGATE immediately.",
        "INVESTIGATE": "  → Meaningful cluster. Worth detailed due diligence on company fundamentals.",
        "WATCH":       "  → Moderate signal. Add to watchlist; monitor for additional insider activity.",
        "LOG":         "  → Weak signal alone, but log for pattern monitoring over 90 days.",
        "IGNORE":      "  → No actionable signal from this window.",
    }
    print(tier_text.get(cluster.conviction_tier, ""))
    print()
    print(f"  ESPI source: gpw.pl/espi-ebi-reports (search by company ticker)")
    print(f"  US equivalent: openinsider.com (SEC Form 4 cluster screener)")
    print(sep)
