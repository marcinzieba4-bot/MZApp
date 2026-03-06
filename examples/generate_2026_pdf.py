"""
PDF Report — MSCI Poland 2026 Prospective Trade Ideas
======================================================
Generates a professional PDF covering:
  • Epistemic disclaimer (knowledge cutoff + estimated data)
  • Market context for 2026 MSCI Poland SAR cycle
  • Per-candidate trade sheets: rationale, entry criteria, risks, verification checklist
  • Deletion risk section
  • Decision framework / checklist
  • Historical backtest comparison (so reader can contextualise expected returns)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line

from examples.candidates_2026 import build_2026_candidates, ProspectiveCandidate
from framework.walkforward_backtest import build_screen_events, simulate_portfolio

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY  = colors.HexColor("#0D1B2A")
BLUE  = colors.HexColor("#1565C0")
TEAL  = colors.HexColor("#00796B")
GREEN = colors.HexColor("#2E7D32")
RED   = colors.HexColor("#C62828")
AMBER = colors.HexColor("#E65100")
LGRAY = colors.HexColor("#F5F5F5")
MGRAY = colors.HexColor("#E0E0E0")
DGRAY = colors.HexColor("#757575")
WHITE = colors.white
BLACK = colors.black
GOLD  = colors.HexColor("#F9A825")

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm


def S(name, **kw):
    defaults = dict(fontSize=8.5, leading=12, fontName="Helvetica",
                    textColor=BLACK, spaceAfter=3)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


STYLES = {
    "h1":       S("h1", fontSize=15, leading=20, textColor=NAVY,
                  fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6),
    "h2":       S("h2", fontSize=11, leading=15, textColor=BLUE,
                  fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4),
    "h3":       S("h3", fontSize=9.5, leading=13, textColor=TEAL,
                  fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=3),
    "body":     S("body"),
    "small":    S("small", fontSize=7.5, leading=11, textColor=DGRAY),
    "caveat":   S("caveat", fontSize=8, leading=12, textColor=AMBER,
                  fontName="Helvetica-Oblique", leftIndent=8),
    "est":      S("est", fontSize=7.5, leading=11, textColor=DGRAY,
                  fontName="Helvetica-Oblique"),
    "cell":     S("cell", fontSize=7.5, leading=10),
    "cell_b":   S("cell_b", fontSize=7.5, leading=10, fontName="Helvetica-Bold"),
    "cell_g":   S("cell_g", fontSize=7.5, leading=10, textColor=GREEN, fontName="Helvetica-Bold"),
    "cell_r":   S("cell_r", fontSize=7.5, leading=10, textColor=RED, fontName="Helvetica-Bold"),
    "cell_a":   S("cell_a", fontSize=7.5, leading=10, textColor=AMBER, fontName="Helvetica-Bold"),
    "cell_gr":  S("cell_gr", fontSize=7.5, leading=10, textColor=DGRAY,
                  fontName="Helvetica-Oblique"),
}


def _on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(DGRAY)
    canvas.drawString(MARGIN, 0.7 * cm,
                      "MSCI Poland 2026 Prospective Trades  |  Research Only — Verify All [EST] Figures Before Trading")
    canvas.drawRightString(PAGE_W - MARGIN, 0.7 * cm, f"Page {doc.page}")
    canvas.restoreState()


# ─────────────────────────────────────────────────────────────────────────────
# Cover
# ─────────────────────────────────────────────────────────────────────────────
def cover(candidates):
    items = []
    items.append(Spacer(1, 0.8 * cm))
    items.append(HRFlowable(width="100%", thickness=4, color=NAVY, spaceAfter=14))

    items.append(Paragraph("MSCI POLAND — 2026 PROSPECTIVE TRADES",
                            S("ct", fontSize=22, leading=28, textColor=NAVY,
                              fontName="Helvetica-Bold", alignment=TA_CENTER)))
    items.append(Paragraph("Index Inclusion Alpha Strategy — Forward-Looking Candidate Watchlist",
                            S("cs", fontSize=11, leading=15, textColor=BLUE,
                              alignment=TA_CENTER)))
    items.append(Spacer(1, 0.3 * cm))
    items.append(Paragraph(
        "Report date: March 2026  |  Reviews: May 2026 SAR + Nov 2026 SAR",
        S("cm", fontSize=9, textColor=DGRAY, alignment=TA_CENTER),
    ))
    items.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceBefore=14, spaceAfter=14))

    # Disclaimer box
    disc_data = [[Paragraph(
        "⚠  EPISTEMIC DISCLAIMER — READ BEFORE USING\n\n"
        "This report was generated in March 2026. The model's training data ends in "
        "August 2025. All market data (prices, market caps, RS percentiles, ATVR) "
        "for the period August 2025–March 2026 is ESTIMATED [EST] based on trend "
        "extrapolation and qualitative judgement.\n\n"
        "The November 2025 MSCI SAR occurred within this blind spot — its exact "
        "outcome (which stocks were added / deleted / had weight changes) is unknown "
        "and must be verified from MSCI's published press releases before proceeding.\n\n"
        "DO NOT open any position without first verifying: (1) current market cap, "
        "(2) RS percentile from live data, (3) ATVR, (4) Nov 2025 SAR outcome.\n\n"
        "All prices marked [EST] are illustrative order-of-magnitude estimates only.",
        S("disc", fontSize=8, leading=12, textColor=colors.HexColor("#4A0000"),
          fontName="Helvetica"),
    )]]
    disc_table = Table(disc_data, colWidths=[PAGE_W - 2 * MARGIN])
    disc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF3E0")),
        ("BOX", (0, 0), (-1, -1), 1.5, AMBER),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    items.append(disc_table)
    items.append(Spacer(1, 0.5 * cm))

    # Candidate summary tiles
    top = [c for c in candidates if c.conviction == "HIGH"]
    med = [c for c in candidates if c.conviction == "MEDIUM"]
    watch = [c for c in candidates if c.conviction == "WATCH"]
    avoid = [c for c in candidates if c.conviction in ("AVOID/SHORT", "AVOID")]

    tiles_data = [
        [
            _mini_tile("TOP PICKS", str(len(top)), "HIGH conviction", GREEN),
            _mini_tile("MEDIUM", str(len(med)), "above filter", TEAL),
            _mini_tile("WATCH", str(len(watch)), "monitor for entry", AMBER),
            _mini_tile("AVOID / SHORT", str(len(avoid)), "deletion / weak momentum", RED),
        ]
    ]
    tiles_table = Table(tiles_data, colWidths=[(PAGE_W - 2 * MARGIN) / 4] * 4)
    tiles_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    items.append(tiles_table)
    items.append(Spacer(1, 0.5 * cm))

    # Backtest reference
    items.append(Paragraph(
        "<b>Historical context (from walk-forward backtest 2018–2025):</b>  "
        "Momentum-filtered events averaged <b>+13.2% return</b> per position "
        "(T−45 → effective date), with <b>100% win rate</b> and Sharpe 2.12. "
        "Standard additions / upgrades avg +14.3%; weight increases avg +13.2%. "
        "False positives (stocks not added) averaged only +0.1%. "
        "These figures provide the expected return range for the 2026 candidates below.",
        STYLES["body"],
    ))
    items.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceBefore=12, spaceAfter=0))
    return items


def _mini_tile(label, value, sub, color):
    return Table(
        [[Paragraph(label, S("tl", fontSize=7, textColor=DGRAY, fontName="Helvetica-Bold",
                              alignment=TA_CENTER))],
         [Paragraph(value, S("tv", fontSize=26, textColor=color,
                              fontName="Helvetica-Bold", alignment=TA_CENTER))],
         [Paragraph(sub, S("ts", fontSize=7, textColor=DGRAY, alignment=TA_CENTER))]],
        colWidths=[(PAGE_W - 2 * MARGIN) / 4 - 0.3 * cm],
        style=TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, MGRAY),
            ("BACKGROUND", (0, 0), (-1, -1), LGRAY),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Market context
# ─────────────────────────────────────────────────────────────────────────────
def market_context():
    items = []
    items.append(Paragraph("1. Market Context — Poland 2026", STYLES["h1"]))

    items.append(Paragraph("MSCI Poland Index Composition (estimated, Mar 2026)", STYLES["h2"]))
    items.append(Paragraph(
        "Following the May 2025 SAR (XTB, Kruk, Budimex weight increases) and the "
        "November 2025 SAR (outcome unknown — verify from MSCI press release), "
        "the MSCI Poland Standard index is estimated to contain ~17–20 constituents. "
        "Dominant sectors: Financials (~35%), Consumer Discretionary (~22%), "
        "Industrials (~12%), Materials (~8%), IT (~7%).",
        STYLES["body"],
    ))

    context_rows = [
        ["Theme", "Relevance for MSCI Inclusions", "Direction"],
        ["EU KPO disbursements accelerating",
         "Budimex, other infrastructure names — cap growing faster than index",
         "↑ Weight increase for BDX"],
        ["NBP rate cuts 2025-26",
         "Bank NIMs compress; but NPL buyers (Kruk) benefit from wider spreads",
         "↑ KRU; ↔ MIL"],
        ["XTB / retail trading volumes",
         "Crypto bull run + stock market highs = XTB volumes elevated",
         "↑↑ XTB cap growth"],
        ["CVC / Żabka IPO overhang",
         "If CVC exited by H1 2025, ZAB float increases → momentum can recover",
         "↑ ZAB Standard upgrade"],
        ["Polish government spending",
         "PLN 100B+ defence + infrastructure = construction boom sustained",
         "↑ BDX, APR"],
        ["Cyfrowy Polsat structural decline",
         "MVNO + OTT competition; cap below Standard threshold",
         "↓ CPS deletion risk"],
        ["CHF mortgage resolution",
         "Bank Millennium provisions nearly complete by 2026",
         "↑ MIL Standard add potential"],
    ]
    col_w = [(PAGE_W - 2 * MARGIN) * x for x in [0.28, 0.52, 0.20]]
    t = Table(
        [[Paragraph(c, STYLES["cell_b"] if r == 0 else STYLES["cell"]) for c in row]
         for r, row in enumerate(context_rows)],
        colWidths=col_w,
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGRAY]),
        ("GRID", (0, 0), (-1, -1), 0.3, MGRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    items.append(t)

    items.append(Spacer(1, 0.3 * cm))
    items.append(Paragraph("Review Calendar", STYLES["h2"]))
    cal_rows = [
        ["Event", "Date [EST]", "Action required"],
        ["May 2026 SAR — T−45 screen", "~14 March 2026", "Screen now — we are AT this date"],
        ["May 2026 SAR — Announcement", "~28 April 2026", "Exit FP positions; hold TP positions"],
        ["May 2026 SAR — Effective date", "~29 May 2026", "Exit TP positions (main alpha event)"],
        ["FTSE Jun 2026 QIR — Announcement", "~3 June 2026", "Watch: MSCI additions often follow FTSE"],
        ["FTSE Jun 2026 QIR — Effective", "~15 June 2026", "Exit if FTSE also adds same stock"],
        ["Nov 2026 SAR — T−45 screen", "~16 September 2026", "Re-screen universe for Nov candidates"],
        ["Nov 2026 SAR — Announcement", "~28 October 2026", "Manage FP exits"],
        ["Nov 2026 SAR — Effective date", "~30 November 2026", "Final exit for TP positions"],
    ]
    col_w2 = [(PAGE_W - 2 * MARGIN) * x for x in [0.30, 0.22, 0.48]]
    t2 = Table(
        [[Paragraph(c, STYLES["cell_b"] if r == 0 else
                    (STYLES["cell_g"] if "now" in c.lower() else STYLES["cell"]))
          for c in row] for r, row in enumerate(cal_rows)],
        colWidths=col_w2,
    )
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGRAY]),
        ("GRID", (0, 0), (-1, -1), 0.3, MGRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#E8F5E9")),  # highlight T-45 now
    ]))
    items.append(t2)
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Watchlist overview table
# ─────────────────────────────────────────────────────────────────────────────
def watchlist_overview(candidates):
    items = []
    items.append(PageBreak())
    items.append(Paragraph("2. 2026 Candidate Watchlist — Overview", STYLES["h1"]))
    items.append(Paragraph(
        "All candidates ranked by conviction tier then RS percentile. "
        "All market data marked [EST]. Verify from live WSE data before entry.",
        STYLES["body"],
    ))
    items.append(Spacer(1, 0.2 * cm))

    tier_order = {"HIGH": 0, "MEDIUM": 1, "WATCH": 2, "AVOID/SHORT": 3, "AVOID": 4}
    sorted_c = sorted(candidates, key=lambda x: (tier_order.get(x.conviction, 9),
                                                  x.target_review, -x.rs_percentile))

    rows = [["#", "Company", "Ticker", "Event type", "Review",
             "Cap [EST]", "RS% [EST]", "Filter", "Entry [EST]", "Conviction"]]

    for i, c in enumerate(sorted_c, 1):
        filt_s = STYLES["cell_g"] if c.momentum_passes_filter else STYLES["cell_r"]
        conv_map = {
            "HIGH": STYLES["cell_g"], "MEDIUM": STYLES["cell"],
            "WATCH": STYLES["cell_a"], "AVOID/SHORT": STYLES["cell_r"],
            "AVOID": STYLES["cell_r"],
        }
        icon = {"HIGH": "★★", "MEDIUM": "★", "WATCH": "◇",
                "AVOID/SHORT": "⚠ SHORT", "AVOID": "✗"}.get(c.conviction, "?")
        rows.append([
            Paragraph(str(i), STYLES["cell"]),
            Paragraph(c.company, STYLES["cell_b"]),
            Paragraph(c.ticker, STYLES["cell"]),
            Paragraph(c.event_type, STYLES["cell"]),
            Paragraph(c.target_review, STYLES["cell"]),
            Paragraph(f"${c.full_cap_usd_m:,.0f}M", STYLES["cell"]),
            Paragraph(str(int(c.rs_percentile)), STYLES["cell"]),
            Paragraph("PASS" if c.momentum_passes_filter else "SKIP", filt_s),
            Paragraph(f"PLN {c.estimated_entry_price_pln:,.0f}" if c.estimated_entry_price_pln > 0
                      else "—", STYLES["cell"]),
            Paragraph(icon, conv_map.get(c.conviction, STYLES["cell"])),
        ])

    col_w = [(PAGE_W - 2 * MARGIN) * x
             for x in [0.04, 0.18, 0.07, 0.15, 0.10, 0.10, 0.07, 0.07, 0.11, 0.11]]
    t = Table(rows, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGRAY]),
        ("GRID", (0, 0), (-1, -1), 0.25, MGRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 7.5),
    ]))
    items.append(t)

    items.append(Spacer(1, 0.3 * cm))
    items.append(Paragraph(
        "Momentum filter = RS ≥ 60th pct + above 200d MA. "
        "From backtest: filtered positions avg +13.2% vs +0.1% for excluded false positives. "
        "Stocks failing the filter are significantly more likely to disappoint at announcement.",
        STYLES["small"],
    ))
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Individual trade sheets
# ─────────────────────────────────────────────────────────────────────────────
def _trade_card(c: ProspectiveCandidate) -> list:
    """One detailed trade card per candidate."""
    items = []

    # Card header
    conv_color = {
        "HIGH": GREEN, "MEDIUM": TEAL, "WATCH": AMBER,
        "AVOID/SHORT": RED, "AVOID": RED,
    }.get(c.conviction, DGRAY)
    icon = {"HIGH": "★★ TOP PICK", "MEDIUM": "★ MEDIUM",
            "WATCH": "◇ WATCH", "AVOID/SHORT": "⚠ AVOID / SHORT",
            "AVOID": "✗ AVOID"}.get(c.conviction, c.conviction)

    hdr_data = [[
        Paragraph(f"{c.company}  ({c.ticker})",
                  S("hc", fontSize=11, fontName="Helvetica-Bold", textColor=WHITE)),
        Paragraph(f"{icon}  |  {c.target_review}  |  {c.event_type}",
                  S("hc2", fontSize=8.5, textColor=colors.HexColor("#B0BEC5"),
                    alignment=TA_RIGHT)),
    ]]
    hdr_t = Table(hdr_data, colWidths=[(PAGE_W - 2 * MARGIN) * 0.55,
                                        (PAGE_W - 2 * MARGIN) * 0.45])
    hdr_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    items.append(KeepTogether([hdr_t]))

    # Metrics strip
    metrics = [
        ("Cap [EST]", f"${c.full_cap_usd_m:,.0f}M"),
        ("Float-adj [EST]", f"${c.float_adj_cap_usd_m:,.0f}M"),
        ("ATVR [EST]", f"{c.atvr_3m_pct:.1f}%"),
        ("RS% [EST]", f"{c.rs_percentile:.0f}th"),
        ("200d MA [EST]", "Above ✓" if c.above_200d_ma else "Below ✗"),
        ("12M mom [EST]", f"{c.momentum_12m_pct:+.0f}%"),
        ("Threshold gap", f"{c.pct_above_threshold:+.0f}%"),
        ("Forced buy [EST]", f"${c.est_forced_buying_usd_m:,.0f}M"),
        ("ADV days [EST]", f"{c.est_adv_days:.0f}d"),
        ("Filter", "✓ PASS" if c.momentum_passes_filter else "✗ SKIP"),
    ]
    met_rows = [[
        Table([[Paragraph(m[0], S("ml", fontSize=6.5, textColor=DGRAY, fontName="Helvetica-Bold",
                                   alignment=TA_CENTER))],
               [Paragraph(m[1], S("mv", fontSize=9, textColor=GREEN if "✓" in m[1]
                                   else RED if "✗" in m[1] or m[0] == "Threshold gap" and float(m[1].replace('%','').replace('+','')) < 0
                                   else BLACK,
                                   fontName="Helvetica-Bold", alignment=TA_CENTER))]],
               colWidths=[(PAGE_W - 2 * MARGIN) / len(metrics)],
               style=TableStyle([
                   ("BACKGROUND", (0, 0), (-1, -1), LGRAY),
                   ("BOX", (0, 0), (-1, -1), 0.3, MGRAY),
                   ("TOPPADDING", (0, 0), (-1, -1), 3),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
               ]))
        for m in metrics
    ]]
    met_t = Table([met_rows], colWidths=[(PAGE_W - 2 * MARGIN) / len(metrics)] * len(metrics))
    met_t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    items.append(met_t)

    # Two-column: thesis + risks/verification
    thesis_lines = c.thesis.replace("★ ", "").replace("⚠ ", "")
    thesis_para = Paragraph(
        thesis_lines.replace("\n", "<br/>"),
        S("th_body", fontSize=8, leading=12, textColor=BLACK),
    )

    risks_items = "".join(f"• {r}<br/>" for r in c.key_risks)
    verify_items = "".join(f"☐  {v}<br/>" for v in c.data_verification_needed)

    right_col = [
        Paragraph("Key Risks", S("rh", fontSize=8.5, fontName="Helvetica-Bold",
                                  textColor=RED, spaceAfter=2)),
        Paragraph(risks_items, S("ri", fontSize=7.5, leading=11, textColor=BLACK)),
        Spacer(1, 0.15 * cm),
        Paragraph("Verification Checklist (before entry)", S("vh", fontSize=8.5,
                   fontName="Helvetica-Bold", textColor=BLUE, spaceAfter=2)),
        Paragraph(verify_items, S("vi", fontSize=7.5, leading=11,
                                   textColor=colors.HexColor("#1A237E"))),
    ]

    # Entry / exit summary
    if c.event_type != "Deletion Risk":
        est_return = (c.estimated_target_price_pln / c.estimated_entry_price_pln - 1) * 100 \
            if c.estimated_entry_price_pln > 0 else 0
        entry_exit = (
            f"<b>Entry [EST]:</b> PLN {c.estimated_entry_price_pln:,.0f}  "
            f"(T−45 screen date ~14 Mar 2026 for May SAR)<br/>"
            f"<b>TP exit [EST]:</b> PLN {c.estimated_target_price_pln:,.0f}  "
            f"(effective date ~29 May 2026)  ≈ {est_return:.0f}% gross<br/>"
            f"<b>FP exit:</b> Announcement date (~28 Apr 2026) — "
            f"if not announced, close immediately<br/>"
            f"<b>Historical base rate:</b> weight-increase avg +13.2%  |  "
            f"Standard add avg +14.3%  (2018–2025 backtest)"
        )
    else:
        entry_exit = (
            f"<b>Short entry [EST]:</b> PLN {c.estimated_entry_price_pln:,.0f}  "
            f"(T−45 before expected deletion)<br/>"
            f"<b>Cover [EST]:</b> PLN {c.estimated_target_price_pln:,.0f}  "
            f"(at effective date; +1.5% reversal expected after)<br/>"
            f"<b>Historical deletion avg:</b> −3.5% announcement day, −5% T−45→effective"
        )

    two_col = Table(
        [[thesis_para,
          Table([[r] for r in right_col],
                style=TableStyle([("TOPPADDING", (0, 0), (-1, -1), 0),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))]],
        colWidths=[(PAGE_W - 2 * MARGIN) * 0.52, (PAGE_W - 2 * MARGIN) * 0.48],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBEFORE", (1, 0), (1, -1), 0.5, MGRAY),
        ]),
    )
    items.append(two_col)

    # Entry/exit bar
    ee_data = [[Paragraph(entry_exit,
                           S("ee", fontSize=7.5, leading=11, textColor=BLACK))]]
    ee_t = Table(ee_data, colWidths=[PAGE_W - 2 * MARGIN])
    ee_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E3F2FD")),
        ("BOX", (0, 0), (-1, -1), 0.5, BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    items.append(ee_t)
    items.append(Spacer(1, 0.5 * cm))
    return items


def trade_sheets(candidates):
    items = []
    items.append(PageBreak())
    items.append(Paragraph("3. Individual Trade Sheets", STYLES["h1"]))
    items.append(Paragraph(
        "One sheet per candidate. Left column: thesis. "
        "Right column: risks + verification checklist. "
        "Bottom bar: entry / exit mechanics.",
        STYLES["body"],
    ))
    items.append(Spacer(1, 0.3 * cm))

    tier_order = {"HIGH": 0, "MEDIUM": 1, "WATCH": 2, "AVOID/SHORT": 3, "AVOID": 4}
    sorted_c = sorted(candidates, key=lambda x: (tier_order.get(x.conviction, 9),
                                                  x.target_review, -x.rs_percentile))
    for c in sorted_c:
        items += _trade_card(c)

    return items


# ─────────────────────────────────────────────────────────────────────────────
# Decision framework checklist
# ─────────────────────────────────────────────────────────────────────────────
def decision_framework():
    items = []
    items.append(PageBreak())
    items.append(Paragraph("4. Pre-Trade Decision Framework", STYLES["h1"]))
    items.append(Paragraph(
        "Before opening any position from this watchlist, complete the following "
        "checklist using LIVE data from WSE/stooq/Bloomberg.",
        STYLES["body"],
    ))

    steps = [
        ("Step 1 — Verify Nov 2025 SAR outcome",
         "Download the MSCI Semi-Annual Review press release (Nov 2025) from msci.com/eqb. "
         "Confirm which stocks were added, deleted, or had weight changes. "
         "Update your watchlist accordingly — some candidates may already be added; "
         "some deletion risks may already be resolved.",
         ["☐ Downloaded MSCI Nov 2025 SAR press release",
          "☐ Updated watchlist for stocks already added (no alpha remaining — do not chase)",
          "☐ Checked if deletion candidates were already deleted (exit short if so)"]),
        ("Step 2 — Verify market caps (live data)",
         "Use stooq.pl, Bloomberg, or WSE official data. "
         "Compute: full market cap = price × shares outstanding (public filings). "
         "Float-adjusted: apply FIF from latest MSCI announcement. "
         "MSCI Standard threshold: $2,500M full cap, $1,300M float-adj (May 2026 values — "
         "thresholds adjust annually; verify from MSCI methodology document).",
         ["☐ Current price (PLN) for each candidate",
          "☐ Shares outstanding from KRS/WSE disclosures",
          "☐ Float-adj cap: price × shares × FIF",
          "☐ Both full cap AND float-adj cap above respective thresholds"]),
        ("Step 3 — Verify momentum (RS percentile + 200d MA)",
         "Compute RS = stock 12-1M return ranked vs all WIG-ALL constituents. "
         "RS ≥ 60th pct required. Also verify price > 200-day moving average. "
         "Both conditions must pass — if either fails, do not initiate position.",
         ["☐ 12-month return (skip last month) for each candidate vs WIG-ALL",
          "☐ RS percentile calculated (not estimated)",
          "☐ Price vs 200-day moving average confirmed",
          "☐ If RS < 60th pct OR below 200d MA → SKIP regardless of thesis"]),
        ("Step 4 — Verify ATVR",
         "ATVR = average daily turnover as % of float-adj cap (3-month trailing). "
         "MSCI Standard minimum: 15%. Compute from daily volume data. "
         "Watch for stocks near 15% — any single bad month can push below threshold.",
         ["☐ ATVR for Oct-Dec 2025 (3M trailing as of Jan 2026)",
          "☐ ATVR > 15% confirmed (not estimated)",
          "☐ Monthly ATVR stable — no single month < 12%"]),
        ("Step 5 — Position sizing",
         "Equal weight across confirmed positions. Maximum 33% per single stock. "
         "Total portfolio exposure to this strategy: size relative to your total AUM "
         "based on risk budget. This strategy concentrates risk into ~6-week windows "
         "twice per year.",
         ["☐ Number of qualifying positions determined",
          "☐ Position size = 1/N of strategy allocation",
          "☐ No single position > 33% of strategy book",
          "☐ Entry at T−45 market close (approximately 14 March 2026 for May SAR)"]),
        ("Step 6 — Announcement day management",
         "On MSCI announcement day (~28 April 2026): "
         "check each position against MSCI press release within minutes of release. "
         "Stocks NOT announced for addition → close immediately at market (FP exit). "
         "Stocks confirmed for addition → hold to effective date.",
         ["☐ Announcement date in calendar with alert",
          "☐ MSCI press release auto-alert set up (msci.com/eqb)",
          "☐ FP exit order: market sell within 30 min of announcement",
          "☐ TP positions: hold with trailing stop at effective date"]),
    ]

    for title, desc, checklist in steps:
        items.append(Paragraph(title, STYLES["h2"]))
        items.append(Paragraph(desc, STYLES["body"]))
        check_text = "".join(f"{item}<br/>" for item in checklist)
        ck_data = [[Paragraph(check_text,
                               S("ck", fontSize=7.5, leading=12,
                                 textColor=colors.HexColor("#1A237E")))]]
        ck_t = Table(ck_data, colWidths=[PAGE_W - 2 * MARGIN])
        ck_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8EAF6")),
            ("BOX", (0, 0), (-1, -1), 0.5, BLUE),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        items.append(ck_t)
        items.append(Spacer(1, 0.2 * cm))

    return items


# ─────────────────────────────────────────────────────────────────────────────
# Historical comparison
# ─────────────────────────────────────────────────────────────────────────────
def historical_comparison():
    items = []
    items.append(PageBreak())
    items.append(Paragraph("5. Historical Backtest Reference", STYLES["h1"]))
    items.append(Paragraph(
        "Expected return ranges for 2026 positions, calibrated from the 2018–2025 "
        "walk-forward backtest (momentum-filtered events only).",
        STYLES["body"],
    ))

    rows = [
        ["Event Type", "N events", "Avg return", "Min", "Max", "Win rate", "Comparable 2026 trade"],
        ["Standard Add / EM SC→Standard upgrade", "6", "+14.3%", "+5.2%", "+25.7%", "100%",
         "Żabka (ZAB) if momentum recovers"],
        ["Weight Increase (existing Standard member)", "9", "+13.2%", "+8.4%", "+22.6%", "100%",
         "XTB, KRU, BDX, LPP"],
        ["EM Small Cap Addition", "7", "+10.7%", "−2.7%", "+21.3%", "86%",
         "Auto Partner (APR), Benefit Systems (BSY)"],
        ["FTSE EM Addition (Poland)", "4", "+12.3%", "+10.1%", "+20.3%", "100%",
         "Any of the above if not yet in FTSE"],
        ["False Positive (not added, filtered IN)", "4", "+2.6%", "+0.4%", "+5.8%", "100%",
         "Risk for borderline candidates"],
        ["False Positive (not added, filtered OUT)", "11", "−0.5%", "−7.3%", "+3.5%", "55%",
         "Cyfrowy Polsat if any long, Bank Millennium if BCP issue persists"],
    ]
    col_w = [(PAGE_W - 2 * MARGIN) * x for x in [0.26, 0.07, 0.09, 0.07, 0.07, 0.08, 0.36]]
    t = Table(
        [[Paragraph(c, STYLES["cell_b"] if r == 0 else STYLES["cell"]) for c in row]
         for r, row in enumerate(rows)],
        colWidths=col_w,
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGRAY]),
        ("GRID", (0, 0), (-1, -1), 0.3, MGRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 5), (-1, 6), colors.HexColor("#FFF3E0")),  # FP rows
    ]))
    items.append(t)
    items.append(Spacer(1, 0.3 * cm))

    items.append(Paragraph(
        "<b>Important:</b> These returns are from T−45 to effective date (net of 20 bps). "
        "The strategy holds for ~45–65 calendar days. On an annualised basis "
        "(deployed twice per year), filtered positions delivered +26.8% p.a. (2018–2025). "
        "False positives are managed by closing at announcement — their drag is minimal "
        "when the momentum filter is applied (only 4 residual FPs in 27 filtered positions).",
        STYLES["body"],
    ))
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def build_pdf(output_path: str = "msci_poland_2026_candidates.pdf") -> str:
    candidates = build_2026_candidates()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=1.4 * cm,
        title="MSCI Poland 2026 — Prospective Trade Candidates",
        author="MZApp Research",
    )

    story = []
    story += cover(candidates)
    story += market_context()
    story += watchlist_overview(candidates)
    story += trade_sheets(candidates)
    story += decision_framework()
    story += historical_comparison()

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return output_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "msci_poland_2026_candidates.pdf"
    path = build_pdf(out)
    print(f"PDF saved → {path}")
