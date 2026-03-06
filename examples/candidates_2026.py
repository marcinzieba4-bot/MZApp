"""
MSCI Poland — Prospective Candidates for 2026 Reviews
======================================================

Report date: March 2026
Knowledge cutoff: August 2025
─────────────────────────────────────────────────────────────────────────────

IMPORTANT EPISTEMIC DISCLAIMER
──────────────────────────────
This analysis was written in March 2026. The model's training data ends in
August 2025. Therefore:

  KNOWN (up to Aug 2025):
    • May 2025 SAR confirmed additions / weight changes (XTB, KRU, BDX)
    • Fundamental trends: EU KPO spending, NBP rate path, NPL cycle, XTB growth
    • Momentum trajectories as of Aug 2025

  UNKNOWN / ESTIMATED:
    • Nov 2025 SAR outcome (between Aug 2025 and today)
    • Current prices, market caps, RS percentiles (extrapolated from trends)
    • Whether momentum has been sustained from Aug 2025 to Mar 2026

  Estimated figures are flagged with [EST] in the data below.
  Users MUST verify market cap, float-adj cap, and RS percentile from
  live WSE/stooq data before opening any position.

REVIEW CALENDAR — 2026
───────────────────────
  May 2026 SAR:
    Screen window:     NOW (early Jan – mid-Apr 2026)  ← we are in this window
    Announcement:      ~28 April 2026
    Effective date:    ~29 May 2026
    T−45 entry close:  ~14 March 2026  ← approximately today

  Nov 2026 SAR:
    Screen window:     Jul – mid-Oct 2026
    Announcement:      ~28 October 2026
    Effective date:    ~30 November 2026
    T−45 entry close:  ~16 September 2026

CONFIRMED MSCI POLAND STANDARD MEMBERS (as of May 2025 SAR):
  PKO BP, PKN Orlen, PZU, PEKAO, LPP, Allegro.eu, Dino Polska, KGHM,
  CD Projekt, Mbank, Santander Bank Polska, Kruk, Budimex, XTB,
  Pepco Group, CCC S.A., Cyfrowy Polsat, Żabka Group (EM SC → monitoring)

NOV 2025 SAR (BLIND SPOT — estimated changes):
  Likely weight increases: XTB, Kruk, Budimex, PKO BP (continued outperformers)
  Possible new addition: Bank Millennium (if BCP stake resolved)
  Deletion risk: Cyfrowy Polsat (ATVR and cap declining), PKP Cargo (confirmed risk)
"""

from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# Prospective candidate dataclass
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ProspectiveCandidate:
    """
    A prospective MSCI inclusion / weight-change candidate for 2026.
    Fields marked [EST] are estimated; must be verified from live data.
    """
    ticker: str
    company: str
    sector: str
    target_review: str           # "May 2026" or "Nov 2026"
    event_type: str              # "Standard Add", "Weight Increase", "SC Add", "Deletion Risk"

    # Market cap & eligibility [EST] — estimated from Aug 2025 trends
    full_cap_usd_m: float        # [EST]
    float_adj_cap_usd_m: float   # [EST]
    atvr_3m_pct: float           # [EST]
    pct_above_threshold: float   # [EST] — positive = above, negative = below

    # Momentum [EST]
    rs_percentile: float         # [EST] trailing 12-1M vs WIG-ALL
    above_200d_ma: bool          # [EST]
    momentum_12m_pct: float      # [EST]
    benchmark_12m_pct: float = 15.0   # WIG-ALL benchmark [EST]

    # Conviction
    conviction: str = "WATCH"    # "HIGH", "MEDIUM", "WATCH", "AVOID/SHORT"
    momentum_passes_filter: bool = False

    # Est. forced buying
    est_forced_buying_usd_m: float = 0.0
    est_adv_days: float = 0.0

    # Context
    thesis: str = ""
    key_risks: list = field(default_factory=list)
    data_verification_needed: list = field(default_factory=list)
    estimated_entry_price_pln: float = 0.0
    estimated_target_price_pln: float = 0.0    # inclusion-driven target

    # Deletion / avoid fields
    deletion_probability: str = ""   # "LOW", "MEDIUM", "HIGH"

    def compute(self) -> None:
        self.momentum_passes_filter = (
            self.rs_percentile >= 60.0 and self.above_200d_ma
        )
        if self.momentum_passes_filter:
            if self.pct_above_threshold >= 20:
                self.conviction = "HIGH"
            elif self.pct_above_threshold >= 5:
                self.conviction = "MEDIUM"
            else:
                self.conviction = "WATCH"
        else:
            self.conviction = "WATCH" if self.rs_percentile >= 45 else "AVOID"


# ─────────────────────────────────────────────────────────────────────────────
# 2026 Candidate Definitions
# ─────────────────────────────────────────────────────────────────────────────

def build_2026_candidates() -> list[ProspectiveCandidate]:
    """
    Prospective MSCI Poland candidates for May 2026 and Nov 2026 SARs.
    Market caps, prices, and RS percentiles are [EST] — extrapolated from
    trends known up to August 2025. Verify before trading.
    """
    candidates = []

    # ─── MAY 2026 SAR CANDIDATES ─────────────────────────────────────────

    candidates.append(ProspectiveCandidate(
        ticker="XTB",
        company="XTB S.A.",
        sector="Financials — Online Brokerage",
        target_review="May 2026",
        event_type="Weight Increase",
        # Market cap has grown rapidly; RS was 96th pct at May 2025
        # Extrapolating: if growth continued at half the 2024-25 rate,
        # full cap could be ~USD 4.5–6B by Jan 2026
        full_cap_usd_m=5_200,           # [EST] was $3.2B Mar 2025, grew ~60% in 12M
        float_adj_cap_usd_m=2_450,      # [EST] founder ~35% → float ~65%
        atvr_3m_pct=44.0,               # [EST] active retail + institutional
        pct_above_threshold=108.0,      # well above Standard; weight grows with cap
        rs_percentile=88,               # [EST] strong but slightly off peak 96th
        above_200d_ma=True,             # [EST]
        momentum_12m_pct=62.0,          # [EST] slowing from +145% but still top-quintile
        est_forced_buying_usd_m=280,
        est_adv_days=13.0,
        thesis=(
            "★ TOP PICK — May 2026 weight increase ★\n"
            "XTB entered MSCI Poland Standard in 2024-25 cycle. By May 2026, "
            "cap outperformance vs other Standard members drives further weight increase. "
            "Business: 1.5M+ retail clients, zero-commission stock app launch, "
            "expanding to new markets (UAE, India). Crypto/CFD volumes elevated. "
            "RS estimated 88th pct [EST] — strong outperformer. Weight increase is "
            "mechanical: if XTB grows faster than the MSCI Poland index, its weight "
            "rises at each SAR. Forced buying from passive funds ~$280M [EST].\n"
            "Backtest analogue: XTB weight increases in Nov 2024 (+17.9%) and "
            "May 2025 (+14.5%) — both generated strong alpha with momentum filter."
        ),
        key_risks=[
            "Retail trading volumes cyclical — a low-volatility 2026 could hurt revenue",
            "ESMA leverage restrictions tightened further could impair CFD margins",
            "Founder stake reduction creates float overhang (but also increases FIF)",
            "Momentum already partially priced — RS was 96th at May 2025; drift from peak",
        ],
        data_verification_needed=[
            "Current share price (PLN) and mktcap",
            "RS percentile vs WIG-ALL as of Jan 2026 (T-45 date)",
            "Whether XTB is above 200d MA",
            "ATVR for Oct-Dec 2025 period",
            "Nov 2025 SAR outcome: was XTB weight increased again?",
        ],
        estimated_entry_price_pln=92.0,    # [EST]
        estimated_target_price_pln=108.0,  # [EST] ~17% inclusion alpha
    ))

    candidates.append(ProspectiveCandidate(
        ticker="KRU",
        company="Kruk S.A.",
        sector="Financials — Debt Collection",
        target_review="May 2026",
        event_type="Weight Increase",
        full_cap_usd_m=4_500,           # [EST] was $3.85B Mar 2025
        float_adj_cap_usd_m=2_500,      # [EST]
        atvr_3m_pct=36.0,               # [EST]
        pct_above_threshold=80.0,
        rs_percentile=82,               # [EST]
        above_200d_ma=True,             # [EST]
        momentum_12m_pct=38.0,          # [EST] slower than 2023-24 but solid
        est_forced_buying_usd_m=220,
        est_adv_days=11.0,
        thesis=(
            "★ TOP PICK — May 2026 weight increase ★\n"
            "Kruk has been a serial MSCI Poland outperformer since Standard inclusion "
            "(May 2023). Each SAR brings weight increases as NPL business grows. "
            "European NPL market remains elevated: Italian, Spanish, German banks "
            "continue portfolio disposals. Kruk's AUM growing ~20% p.a. "
            "NBP rate cuts (expected 2025-26) are double-edged: "
            "  [+] lower borrowing cost → Kruk's spread widens\n"
            "  [-] sellers less motivated → NPL supply could slow\n"
            "Net: modest tailwind. RS estimated 82nd pct [EST] — above filter threshold. "
            "Weight increase alpha is smaller than new-addition but more reliable: "
            "backtest avg for weight increases = +13.2% T-45→effective (100% win rate)."
        ),
        key_risks=[
            "NBP rate cuts reduce NPL seller motivation; portfolio supply could slow",
            "Southern European recession could increase NPL supply too fast (credit losses)",
            "Weight increase magnitude shrinks as Kruk's cap stabilises vs index",
            "FTSE EM was likely added in Jun 2025 — dual-index alpha may be exhausted",
        ],
        data_verification_needed=[
            "Current price and mktcap in PLN",
            "Nov 2025 SAR outcome: weight increase confirmed?",
            "RS percentile vs WIG-ALL as of Jan 2026",
            "NBP rate decision path — check current NBP guidance",
        ],
        estimated_entry_price_pln=498.0,   # [EST]
        estimated_target_price_pln=565.0,  # [EST]
    ))

    candidates.append(ProspectiveCandidate(
        ticker="BDX",
        company="Budimex S.A.",
        sector="Industrials — Construction",
        target_review="May 2026",
        event_type="Weight Increase",
        full_cap_usd_m=5_100,           # [EST] was $4.35B Mar 2025; EU KPO accelerating
        float_adj_cap_usd_m=2_395,      # [EST] Ferrovial ~53%; float 47%
        atvr_3m_pct=28.0,               # [EST]
        pct_above_threshold=104.0,
        rs_percentile=80,               # [EST] slightly off peak
        above_200d_ma=True,             # [EST]
        momentum_12m_pct=32.0,          # [EST]
        est_forced_buying_usd_m=195,
        est_adv_days=8.0,
        thesis=(
            "★ TOP PICK — May 2026 weight increase ★\n"
            "Budimex is Poland's dominant construction company, added to MSCI Standard "
            "Nov 2024 and FTSE EM Dec 2024. By May 2026 SAR, it enters its second "
            "weight-increase cycle as a Standard member. Structural tailwinds intact:\n"
            "  • EU KPO (National Recovery Plan): PLN 76B disbursed through 2026-27\n"
            "  • NATO defence infrastructure: Poland 4%+ GDP = record construction\n"
            "  • Rail: PLN 100B CPK central airport rail project procurement live\n"
            "Ferrovial ownership (53%) stabilises but limits float — FIF 0.47. "
            "Weight increase confirmed [EST]: cap grew vs other Standard members. "
            "RS estimated 80th pct [EST] — above 60th filter threshold."
        ),
        key_risks=[
            "Ferrovial reducing stake would increase float (positive for MSCI weight) "
            "but creates supply overhang — monitor KNF disclosures",
            "EU KPO disbursement delays: Brussels slow approval could defer project starts",
            "Labour cost inflation: Poland near-full employment, wage pressure on margins",
            "Already dual-listed in MSCI + FTSE — incremental passive demand is weight-change only",
        ],
        data_verification_needed=[
            "Ferrovial stake — any block sale in H2 2025?",
            "Current price and market cap",
            "Nov 2025 SAR weight change confirmed?",
            "KPO project awards announced — check Budimex IR",
        ],
        estimated_entry_price_pln=535.0,   # [EST]
        estimated_target_price_pln=610.0,  # [EST]
    ))

    candidates.append(ProspectiveCandidate(
        ticker="ZAB",
        company="Żabka Group S.A.",
        sector="Consumer Staples — Convenience Retail",
        target_review="May 2026",
        event_type="Standard Add",      # EM SC → Standard upgrade candidate
        full_cap_usd_m=4_200,           # [EST] was ~$3.6B at IPO Oct 2024
        float_adj_cap_usd_m=1_850,      # [EST] CVC overhang clearing
        atvr_3m_pct=24.0,               # [EST] improved from 18% at Nov 2024
        pct_above_threshold=68.0,       # well above Standard full-cap threshold
        rs_percentile=68,               # [EST] improved; was 31st at Nov 2024
        above_200d_ma=True,             # [EST] if momentum has recovered
        momentum_12m_pct=25.0,          # [EST]
        est_forced_buying_usd_m=390,
        est_adv_days=14.0,
        thesis=(
            "MEDIUM — EM SC → MSCI Poland Standard upgrade candidate\n"
            "Żabka was added to MSCI EM Small Cap at Nov 2024 review (but our strategy "
            "SKIPPED it — RS 31st, below 200d MA at screen date → CORRECTLY avoided −2.9%). "
            "Key question for May 2026: has momentum recovered from IPO overhang?\n"
            "CVC private equity exit: lock-up typically 180 days post-IPO (Apr 2025), "
            "then 12-month follow-on. If CVC block sold through H1 2025, the overhang "
            "should be clearing by now [EST]. Full cap $4.2B >> $2.5B Standard gate.\n"
            "Float-adj $1.85B [EST] >> $1.3B Standard float-adj gate.\n"
            "The trade: EM SC → Standard creates DUAL DEMAND — the same setup that "
            "generated +25.7% for Allegro (May 2021), +18.6% for Kruk (May 2023), "
            "+15.1% for Budimex (Nov 2024).\n"
            "CONDITION: only enter if RS ≥ 60th pct + above 200d MA at T-45. "
            "If still RS < 50th → skip, repeat at Nov 2026."
        ),
        key_risks=[
            "CVC overhang: if CVC has NOT fully exited by Jan 2026, RS will remain weak → SKIP",
            "E-commerce competition from Allegro, Shein, Temu eroding convenience store model",
            "Polish consumer spending slowdown — 2026 elections uncertainty",
            "EM SC → Standard upgrade not guaranteed: MSCI may defer if float-adj cap volatile",
        ],
        data_verification_needed=[
            "CRITICAL: RS percentile as of Jan 2026 — must be ≥ 60th to enter",
            "CVC stake level — check latest KNF notifications",
            "Is Żabka above its 200d MA?",
            "ATVR for Oct-Dec 2025 — must be ≥ 15%",
            "Nov 2025 SAR outcome: was Żabka upgraded to Standard already?",
        ],
        estimated_entry_price_pln=23.0,    # [EST]
        estimated_target_price_pln=28.0,   # [EST]
    ))

    candidates.append(ProspectiveCandidate(
        ticker="LPP",
        company="LPP S.A.",
        sector="Consumer Discretionary — Fashion Retail",
        target_review="May 2026",
        event_type="Weight Increase",
        full_cap_usd_m=8_800,           # [EST] was $8.2B May 2024
        float_adj_cap_usd_m=4_400,      # [EST]
        atvr_3m_pct=26.0,               # [EST]
        pct_above_threshold=252.0,
        rs_percentile=72,               # [EST]
        above_200d_ma=True,             # [EST]
        momentum_12m_pct=22.0,          # [EST] moderate
        est_forced_buying_usd_m=310,
        est_adv_days=9.0,
        thesis=(
            "MEDIUM — weight increase (existing large Standard member)\n"
            "LPP is one of the largest MSCI Poland Standard members by market cap. "
            "Russia exit fully completed; now focused on CEE and Western European expansion. "
            "Reserved brand (offline fast fashion), Mohito, House, Cropp — growing. "
            "Weight increase is mechanical if LPP outperforms MSCI Poland index. "
            "RS estimated 72nd pct [EST] — above filter. "
            "Passive demand ~$310M [EST] but over a 2-3 year accumulation context. "
            "Solid fundamental story + moderate momentum = MEDIUM conviction."
        ),
        key_risks=[
            "Shein/Temu fast-fashion disruption in CEE markets",
            "FX: PLN strength vs EUR hurts LPP EUR-denominated revenue translation",
            "Weight increase alpha is incremental — no 'new addition' demand spike",
        ],
        data_verification_needed=[
            "Current share price (LPP trades at PLN 12,000–20,000 range — very high per share)",
            "RS percentile vs WIG-ALL",
            "LPP Russia exit — any residual book value writedowns?",
        ],
        estimated_entry_price_pln=19_800,  # [EST]
        estimated_target_price_pln=22_500, # [EST]
    ))

    # ─── NOV 2026 SAR CANDIDATES ─────────────────────────────────────────

    candidates.append(ProspectiveCandidate(
        ticker="MIL",
        company="Bank Millennium S.A.",
        sector="Financials — Retail Banking",
        target_review="Nov 2026",
        event_type="Standard Add",
        full_cap_usd_m=3_100,           # [EST] was $2.65B May 2025
        float_adj_cap_usd_m=1_380,      # [EST] depends on BCP stake
        atvr_3m_pct=24.0,               # [EST] improved
        pct_above_threshold=24.0,       # above Standard full-cap
        rs_percentile=62,               # [EST] recovering
        above_200d_ma=True,             # [EST]
        momentum_12m_pct=24.0,          # [EST]
        est_forced_buying_usd_m=190,
        est_adv_days=10.0,
        thesis=(
            "WATCH → potential MEDIUM for Nov 2026\n"
            "Bank Millennium was the near-miss of May 2025 SAR: float-adj cap "
            "marginally above threshold but BCP classification issue blocked inclusion. "
            "By Nov 2026: two scenarios:\n"
            "  [+] BCP reduces stake below 50% → FIF increases → float-adj cap "
            "comfortably above $1.3B threshold → STANDARD ADDITION. "
            "This would be the high-conviction entry point.\n"
            "  [-] BCP maintains 50.1% → float-adj stays borderline → deferred again.\n"
            "CHF mortgage provisions: by 2026 this should be substantially resolved "
            "(Swiss franc portfolio largely wound down through court settlements). "
            "ROE recovering to 14–16% as provisioning normalises.\n"
            "STRATEGY: screen in September 2026 (T-45 for Nov SAR). "
            "Only enter if: (1) RS ≥ 60th pct, (2) BCP stake < 50%, "
            "(3) float-adj cap clearly > $1.4B with buffer."
        ),
        key_risks=[
            "BINARY: BCP stake decision is the single biggest variable",
            "If BCP does NOT reduce stake, this is again a false positive",
            "Macro: NBP rate cuts could compress NIM and reduce earnings momentum",
            "CHF residual: some courts still awarding unfavourable rulings",
        ],
        data_verification_needed=[
            "BCP stake level — check KNF/WSE disclosures by Aug 2026",
            "Float-adj cap precise calculation at Sep 2026 T-45 date",
            "RS percentile at T-45 — must be ≥ 60th",
            "CHF mortgage total provisions remaining",
        ],
        estimated_entry_price_pln=11.0,    # [EST]
        estimated_target_price_pln=13.5,   # [EST]
    ))

    candidates.append(ProspectiveCandidate(
        ticker="APR",
        company="Auto Partner S.A.",
        sector="Consumer Discretionary — Auto Parts Distribution",
        target_review="Nov 2026",
        event_type="SC Add",
        full_cap_usd_m=520,             # [EST] growing; approaching EM SC threshold
        float_adj_cap_usd_m=290,        # [EST]
        atvr_3m_pct=17.0,               # [EST]
        pct_above_threshold=38.0,       # above $127M EM SC full-cap threshold
        rs_percentile=72,               # [EST] consistent outperformer
        above_200d_ma=True,             # [EST]
        momentum_12m_pct=32.0,          # [EST]
        est_forced_buying_usd_m=42,
        est_adv_days=7.0,
        thesis=(
            "WATCH — EM Small Cap addition candidate for Nov 2026\n"
            "Auto Partner = Poland's largest independent auto parts distributor "
            "(non-OEM aftermarket). 800+ delivery vans, 350,000+ SKUs, "
            "serving garages and retailers across Poland and CEE. "
            "Revenue growing ~18% p.a. as fleet age increases post-COVID. "
            "Full cap ~$520M [EST] >> $127M EM SC threshold. "
            "Float-adj ~$290M [EST] >> $95M EM SC float-adj minimum. "
            "ATVR ~17% [EST] > 15% minimum.\n"
            "RS estimated 72nd pct [EST] — above filter. "
            "SMALL FORCED BUYING: EM SC addition generates only $42M [EST] passive demand "
            "(only 7 ADV days) — lower alpha than Standard events. "
            "Expected return: +7–12% T-45→effective (EM SC historical range). "
            "LOWER priority than Standard events — position smaller."
        ),
        key_risks=[
            "Electric vehicle transition: EV requires fewer aftermarket parts (long-term risk)",
            "Small cap: ATVR can slip below 15% minimum in low-volume periods",
            "Float-adj cap only 3× the EM SC minimum — no large buffer",
            "Limited analyst coverage (4-6 analysts) means less pre-announcement awareness",
        ],
        data_verification_needed=[
            "Current market cap and ATVR",
            "RS percentile vs WIG-ALL",
            "Float structure — any large block holders?",
            "MSCI EM SC cut-off date vs current liquidity",
        ],
        estimated_entry_price_pln=58.0,    # [EST]
        estimated_target_price_pln=66.0,   # [EST]
    ))

    candidates.append(ProspectiveCandidate(
        ticker="BSY",
        company="Benefit Systems S.A.",
        sector="Consumer Discretionary — Corporate Benefits / Wellness",
        target_review="Nov 2026",
        event_type="SC Add",
        full_cap_usd_m=680,             # [EST]
        float_adj_cap_usd_m=420,        # [EST]
        atvr_3m_pct=14.5,               # [EST] borderline — watch closely
        pct_above_threshold=82.0,
        rs_percentile=65,               # [EST]
        above_200d_ma=True,             # [EST]
        momentum_12m_pct=24.0,          # [EST]
        est_forced_buying_usd_m=55,
        est_adv_days=8.5,
        thesis=(
            "WATCH — EM Small Cap candidate, but ATVR is borderline\n"
            "Benefit Systems = operator of MultiSport (corporate gym memberships) "
            "and broader employee benefits platform. 3M+ card holders in Poland. "
            "Expanding to Czech Republic, Slovakia, Bulgaria, Serbia. "
            "Full cap $680M [EST] >> $127M EM SC threshold. "
            "Float-adj $420M [EST] >> $95M minimum.\n"
            "⚠ ATVR WARNING: estimated 14.5% [EST] — just below 15% minimum. "
            "This is the same issue that trapped Ciech and Orange Polska in the backtest. "
            "If ATVR stays below 15% at MSCI cut-off, it is a false positive. "
            "ONLY initiate if ATVR has clearly sustained above 15% for 3+ months "
            "before the screen date."
        ),
        key_risks=[
            "ATVR BORDERLINE — this is the #1 risk; entire thesis fails if ATVR < 15%",
            "Corporate benefits market saturation in Poland — growth slowing",
            "Price per share high (PLN 5,000+) — institutional but not retail driven",
            "Smaller position: EM SC alpha is 6-10%, lower than Standard events",
        ],
        data_verification_needed=[
            "ATVR for Oct-Dec 2026 period — must be > 15.5% with clear buffer",
            "Current market cap and RS percentile",
            "Any large shareholder exits creating overhang?",
        ],
        estimated_entry_price_pln=6_200,   # [EST]
        estimated_target_price_pln=6_850,  # [EST]
    ))

    # ─── DELETION / WEIGHT DECREASE RISKS (avoid longs; potential shorts) ──

    candidates.append(ProspectiveCandidate(
        ticker="CPS",
        company="Cyfrowy Polsat S.A.",
        sector="Communication Services — Telecom/Media",
        target_review="May 2026",
        event_type="Deletion Risk",
        full_cap_usd_m=1_800,           # [EST] declining from $2.9B (2022)
        float_adj_cap_usd_m=780,        # [EST]
        atvr_3m_pct=13.0,               # [EST] declining — approaching <15% danger zone
        pct_above_threshold=-28.0,      # NEGATIVE: below Standard minimum
        rs_percentile=18,               # [EST] bottom quintile
        above_200d_ma=False,            # [EST]
        momentum_12m_pct=-22.0,         # [EST]
        deletion_probability="HIGH",
        thesis=(
            "⚠ AVOID LONGS / DELETION RISK — potential tactical short\n"
            "Cyfrowy Polsat has been in structural decline since 2022. "
            "Full cap $1.8B [EST] — now BELOW the $2.5B Standard threshold. "
            "ATVR estimated 13% [EST] — below 15% minimum. "
            "Both eligibility gates are failing simultaneously.\n"
            "MSCI deletion is likely at May 2026 or Nov 2026 SAR:\n"
            "  Deletion announcement: ~−3.5% average (from backtest deletion events)\n"
            "  Pre-announcement drift: ~−2.0% (early sellers)\n"
            "  Post-deletion reversal: ~+1.5% (cover shorts post-effective)\n"
            "TACTICAL SHORT: short around T-45, cover at effective date. "
            "Long portfolio: REMOVE any CPS exposure immediately. "
            "RS 18th pct [EST] — momentum filter would exclude any long consideration."
        ),
        key_risks=[
            "State rescue or Polsat media group restructuring could temporarily support price",
            "Zygmunt Solorz-Żak controlling shareholder may prevent deletion via buyout",
            "Short squeeze risk if borrow cost is high on WSE",
            "Deletion timing uncertain — MSCI may give one more cycle grace period",
        ],
        data_verification_needed=[
            "Current ATVR — has it recovered above 15%?",
            "Current full cap vs $2.5B / $1.9B threshold (MSCI uses 50% buffer for deletions)",
            "Any restructuring news from Polsat/Solorz group",
        ],
        estimated_entry_price_pln=11.0,    # [EST] for short entry
        estimated_target_price_pln=9.0,    # [EST] post-deletion
    ))

    # Compute all
    for c in candidates:
        c.compute()
        # Override conviction for deletion plays
        if c.event_type == "Deletion Risk":
            c.conviction = "AVOID/SHORT"

    return candidates


# ─────────────────────────────────────────────────────────────────────────────
# Summary printer
# ─────────────────────────────────────────────────────────────────────────────

def print_candidates_2026(candidates: list[ProspectiveCandidate]) -> None:
    W = 72
    print()
    print("═" * W)
    print("  MSCI POLAND 2026 — PROSPECTIVE TRADE CANDIDATES")
    print("  Report date: March 2026  |  Knowledge cutoff: August 2025")
    print("  [EST] = estimated value — must verify from live data before trading")
    print("═" * W)

    tier_order = {"HIGH": 0, "MEDIUM": 1, "WATCH": 2, "AVOID/SHORT": 3, "AVOID": 4}
    sorted_c = sorted(candidates, key=lambda x: (tier_order.get(x.conviction, 9),
                                                  x.target_review, -x.rs_percentile))

    print(f"\n  {'#':<3} {'Stock':<22} {'Event':<20} {'Review':<10} "
          f"{'RS%':<6} {'Filter':<7} {'Conv.'}")
    print("  " + "─" * 68)

    for i, c in enumerate(sorted_c, 1):
        filt = "✓ PASS" if c.momentum_passes_filter else "✗ skip"
        tier_icon = {
            "HIGH": "★★", "MEDIUM": "★", "WATCH": "◇",
            "AVOID/SHORT": "⚠", "AVOID": "✗"
        }.get(c.conviction, "?")
        print(f"  {i:<3} {c.company:<22} {c.event_type:<20} {c.target_review:<10} "
              f"{c.rs_percentile:<6.0f} {filt:<7} {tier_icon} {c.conviction}")

    print()
    print("  TOP PICKS (HIGH conviction, momentum filter passed):")
    for c in sorted_c:
        if c.conviction == "HIGH":
            print(f"\n  ── {c.company} ({c.ticker}) ──────────────────────────────")
            for line in c.thesis.split("\n"):
                print(f"     {line}")
            print(f"     Est. entry: PLN {c.estimated_entry_price_pln:,.0f} [EST]")
            print(f"     Est. target: PLN {c.estimated_target_price_pln:,.0f} [EST] "
                  f"(~{(c.estimated_target_price_pln/c.estimated_entry_price_pln-1)*100:.0f}%)")
            print(f"     Est. forced buying: ${c.est_forced_buying_usd_m:,.0f}M "
                  f"/ {c.est_adv_days:.0f} ADV days")
            print(f"     Verify: {' | '.join(c.data_verification_needed[:2])}")

    print()
    print("  AVOID / SHORT (negative momentum, deletion risk):")
    for c in sorted_c:
        if c.conviction in ("AVOID/SHORT", "AVOID"):
            print(f"\n  ⚠  {c.company} ({c.ticker}) — {c.target_review}")
            print(f"     RS {c.rs_percentile:.0f}th pct [EST], "
                  f"deletion prob: {c.deletion_probability}")
            print(f"     {c.thesis.split(chr(10))[0]}")

    print()
    print("  ⚠  ALL FIGURES MARKED [EST] ARE EXTRAPOLATED FROM AUG 2025 TRENDS.")
    print("  ⚠  VERIFY MARKET CAP, RS PERCENTILE, ATVR FROM LIVE WSE DATA BEFORE")
    print("  ⚠  OPENING ANY POSITION. PRICES WILL DIFFER FROM ESTIMATES.")
    print("═" * W)
    print()
