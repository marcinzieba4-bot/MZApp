"""
PDF Report Generator — MSCI Poland Walk-Forward Backtest
========================================================
Produces a professional PDF with:
  • Cover page with strategy summary
  • Executive summary (key stats comparison table)
  • Full trade log: every position with entry date, exit date, asset, rationale, outcome
  • False positive analysis section
  • Per-cycle performance chart (horizontal bar)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group
from reportlab.graphics import renderPDF

from framework.walkforward_backtest import build_screen_events, simulate_portfolio

# ─────────────────────────────────────────────────────────────────────────────
# Colours
# ─────────────────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#0D1B2A")
BLUE      = colors.HexColor("#1565C0")
TEAL      = colors.HexColor("#00796B")
GREEN     = colors.HexColor("#2E7D32")
RED       = colors.HexColor("#C62828")
AMBER     = colors.HexColor("#E65100")
LGRAY     = colors.HexColor("#F5F5F5")
MGRAY     = colors.HexColor("#E0E0E0")
DGRAY     = colors.HexColor("#757575")
WHITE     = colors.white
BLACK     = colors.black

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm


# ─────────────────────────────────────────────────────────────────────────────
# Styles
# ─────────────────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    s = {}

    s["cover_title"] = ParagraphStyle(
        "cover_title", fontSize=26, leading=32, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", fontSize=13, leading=18, textColor=colors.HexColor("#B0BEC5"),
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4,
    )
    s["cover_meta"] = ParagraphStyle(
        "cover_meta", fontSize=10, leading=14, textColor=colors.HexColor("#90A4AE"),
        fontName="Helvetica", alignment=TA_CENTER,
    )
    s["h1"] = ParagraphStyle(
        "h1", fontSize=15, leading=20, textColor=NAVY, fontName="Helvetica-Bold",
        spaceBefore=14, spaceAfter=6, borderPad=0,
    )
    s["h2"] = ParagraphStyle(
        "h2", fontSize=11, leading=15, textColor=BLUE, fontName="Helvetica-Bold",
        spaceBefore=10, spaceAfter=4,
    )
    s["body"] = ParagraphStyle(
        "body", fontSize=8.5, leading=12, textColor=BLACK, fontName="Helvetica",
        spaceAfter=3,
    )
    s["small"] = ParagraphStyle(
        "small", fontSize=7.5, leading=11, textColor=DGRAY, fontName="Helvetica",
        spaceAfter=2,
    )
    s["caveat"] = ParagraphStyle(
        "caveat", fontSize=7.5, leading=11, textColor=AMBER, fontName="Helvetica-Oblique",
        spaceAfter=2, leftIndent=8,
    )
    s["cell"] = ParagraphStyle(
        "cell", fontSize=7.5, leading=10, textColor=BLACK, fontName="Helvetica",
    )
    s["cell_bold"] = ParagraphStyle(
        "cell_bold", fontSize=7.5, leading=10, textColor=BLACK, fontName="Helvetica-Bold",
    )
    s["cell_gray"] = ParagraphStyle(
        "cell_gray", fontSize=7.5, leading=10, textColor=DGRAY, fontName="Helvetica-Oblique",
    )
    s["cell_green"] = ParagraphStyle(
        "cell_green", fontSize=7.5, leading=10, textColor=GREEN, fontName="Helvetica-Bold",
    )
    s["cell_red"] = ParagraphStyle(
        "cell_red", fontSize=7.5, leading=10, textColor=RED, fontName="Helvetica-Bold",
    )
    s["cell_amber"] = ParagraphStyle(
        "cell_amber", fontSize=7.5, leading=10, textColor=AMBER, fontName="Helvetica-Bold",
    )
    return s


# ─────────────────────────────────────────────────────────────────────────────
# Cover page flowable
# ─────────────────────────────────────────────────────────────────────────────
def cover_page(styles):
    items = []

    # Dark background banner via a drawing
    d = Drawing(PAGE_W - 2 * MARGIN, 7 * cm)
    d.add(Rect(0, 0, PAGE_W - 2 * MARGIN, 7 * cm, fillColor=NAVY, strokeColor=None))
    renderPDF  # just importing; actual render happens via flowable

    items.append(Spacer(1, 1 * cm))

    # Title block — plain paragraphs on white; colour via style
    title_style = ParagraphStyle(
        "ct", fontSize=24, leading=30, textColor=NAVY,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6,
    )
    sub_style = ParagraphStyle(
        "cs", fontSize=12, leading=16, textColor=BLUE,
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        "cm", fontSize=9, leading=13, textColor=DGRAY,
        fontName="Helvetica", alignment=TA_CENTER,
    )

    items.append(HRFlowable(width="100%", thickness=3, color=NAVY, spaceAfter=16))
    items.append(Paragraph("MSCI POLAND WALK-FORWARD BACKTEST", title_style))
    items.append(Paragraph("Index Inclusion Alpha Strategy — Full Trade Log & Performance Report", sub_style))
    items.append(Spacer(1, 0.3 * cm))
    items.append(Paragraph(
        "January 2018 – March 2026  |  15 Review Cycles  |  44 Screened Positions",
        meta_style,
    ))
    items.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceBefore=16, spaceAfter=20))

    # Key metrics boxes
    metrics = [
        ("ALL SCREENED", "+19.0%", "p.a.", "Annualised return\n44 positions"),
        ("MOMENTUM FILTER", "+26.8%", "p.a.", "Annualised return\n27 positions"),
        ("SHARPE (filtered)", "2.12", "", "avg return / std dev\nper position"),
        ("WIN RATE (filtered)", "100%", "", "All filtered positions\nended profitable"),
    ]
    metric_data = [[
        Table(
            [[Paragraph(m[0], ParagraphStyle("ml", fontSize=7, textColor=DGRAY,
                                              fontName="Helvetica-Bold", alignment=TA_CENTER))],
             [Paragraph(m[1], ParagraphStyle("mv", fontSize=22, textColor=NAVY,
                                              fontName="Helvetica-Bold", alignment=TA_CENTER))],
             [Paragraph(m[2] if m[2] else "", ParagraphStyle("mu", fontSize=8, textColor=BLUE,
                                                              fontName="Helvetica", alignment=TA_CENTER))],
             [Paragraph(m[3], ParagraphStyle("md", fontSize=7, textColor=DGRAY,
                                              fontName="Helvetica", alignment=TA_CENTER))]],
            colWidths=[(PAGE_W - 2 * MARGIN) / 4 - 0.3 * cm],
            style=TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.5, MGRAY),
                ("BACKGROUND", (0, 0), (-1, -1), LGRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]),
        )
        for m in metrics
    ]]
    metric_table = Table(metric_data, colWidths=[(PAGE_W - 2 * MARGIN) / 4] * 4)
    metric_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    items.append(metric_table)
    items.append(Spacer(1, 0.6 * cm))

    # Strategy description
    desc_style = ParagraphStyle(
        "desc", fontSize=8.5, leading=13, textColor=colors.HexColor("#37474F"),
        fontName="Helvetica", spaceAfter=4,
    )
    items.append(Paragraph(
        "<b>Strategy:</b> Screen WSE-listed stocks for MSCI Poland eligibility at T−45 before each "
        "Semi-Annual Review effective date. Entry at T−45 close. Exit at effective date for "
        "confirmed inclusions (true positives); exit at announcement date for non-inclusions "
        "(false positives). Momentum filter: RS ≥ 60th percentile vs WIG-ALL + above 200-day MA.",
        desc_style,
    ))
    items.append(Paragraph(
        "<b>No look-ahead bias:</b> All screening decisions use only data observable at T−45 "
        "(market cap, float-adj cap, ATVR, relative strength, MA status). "
        "Prices are approximate (±2–3%); directional conclusions are robust.",
        ParagraphStyle("caveat2", fontSize=8, leading=12, textColor=AMBER,
                       fontName="Helvetica-Oblique"),
    ))
    items.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceBefore=16, spaceAfter=0))

    return items


# ─────────────────────────────────────────────────────────────────────────────
# Summary stats table
# ─────────────────────────────────────────────────────────────────────────────
def summary_section(styles, all_s, filt_s):
    items = []
    items.append(Paragraph("1. Executive Summary", styles["h1"]))

    rows = [
        ["Metric", "All Screened", "Momentum Filtered", "Filter Lift"],
        ["Total positions", str(all_s["n_positions"]), str(filt_s["n_positions"]),
         f"−{all_s['n_positions'] - filt_s['n_positions']} positions removed"],
        ["Review cycles covered", str(all_s["n_cycles"]), str(filt_s["n_cycles"]), "—"],
        ["True positive rate (precision)", f"{all_s['tp_rate_pct']:.0f}%",
         f"{filt_s['tp_rate_pct']:.0f}%", f"+{filt_s['tp_rate_pct'] - all_s['tp_rate_pct']:.0f}pp"],
        ["Win rate (position-level)", f"{all_s['win_rate_pct']:.0f}%",
         f"{filt_s['win_rate_pct']:.0f}%", f"+{filt_s['win_rate_pct'] - all_s['win_rate_pct']:.0f}pp"],
        ["Avg return per position", f"{all_s['avg_return_pct']:+.1f}%",
         f"{filt_s['avg_return_pct']:+.1f}%", f"+{filt_s['avg_return_pct'] - all_s['avg_return_pct']:.1f}pp"],
        ["Std dev (position-level)", f"{all_s['std_return_pct']:.1f}%",
         f"{filt_s['std_return_pct']:.1f}%",
         f"−{all_s['std_return_pct'] - filt_s['std_return_pct']:.1f}pp (tighter)"],
        ["Sharpe ratio", f"{all_s['sharpe']:.2f}", f"{filt_s['sharpe']:.2f}",
         f"+{filt_s['sharpe'] - all_s['sharpe']:.2f}"],
        ["Annualised return (compounded)", f"{all_s['ann_return_pct']:+.1f}%",
         f"{filt_s['ann_return_pct']:+.1f}%",
         f"+{filt_s['ann_return_pct'] - all_s['ann_return_pct']:.1f}pp"],
        ["Total return Jan 2018–Mar 2026", f"{all_s['total_return_pct']:+.1f}%",
         f"{filt_s['total_return_pct']:+.1f}%", ""],
        ["True positive avg return", f"{all_s['tp_avg_return']:+.1f}%",
         f"{filt_s['tp_avg_return']:+.1f}%", ""],
        ["False positive avg return", f"{all_s['fp_avg_return']:+.1f}%",
         f"{filt_s['fp_avg_return']:+.1f}%",
         f"FPs retained: {filt_s['n_fp']} vs {all_s['n_fp']}"],
    ]

    col_w = [(PAGE_W - 2 * MARGIN) * x for x in [0.38, 0.18, 0.22, 0.22]]
    t = Table([[Paragraph(c, styles["cell_bold"] if r == 0 else styles["cell"])
                for c in row] for r, row in enumerate(rows)], colWidths=col_w)

    ts = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGRAY]),
        ("GRID", (0, 0), (-1, -1), 0.3, MGRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        # Highlight filtered column
        ("BACKGROUND", (2, 1), (2, -1), colors.HexColor("#E8F5E9")),
        ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
    ])
    t.setStyle(ts)
    items.append(t)
    items.append(Spacer(1, 0.4 * cm))

    items.append(Paragraph(
        "Momentum filter (RS ≥ 60th pct + above 200d MA): removes 73% of false positives "
        "while retaining 79% of true positives. False positives average only +0.1% return "
        "(drift up during accumulation, give it back on announcement day). "
        "Filtering them out eliminates the main source of alpha drag.",
        styles["body"],
    ))
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Per-cycle bar chart (pure ReportLab Drawing)
# ─────────────────────────────────────────────────────────────────────────────
def cycle_chart(positions, styles):
    items = []
    items.append(Paragraph("2. Per-Cycle Portfolio Returns (Momentum-Filtered)", styles["h1"]))
    items.append(Paragraph(
        "Equal-weight average return across filtered positions in each MSCI SAR cycle. "
        "20 bps round-trip costs included.",
        styles["body"],
    ))

    import statistics as _st
    from framework.walkforward_backtest import build_screen_events

    reviews = {}
    for p in positions:
        reviews.setdefault((p.review_id, p.review_label), []).append(p)

    chart_data = []
    for (rid, label), cpos in sorted(reviews.items(), key=lambda x: x[0][0]):
        filtered = [p for p in cpos if p.momentum_passes_filter]
        if not filtered:
            continue
        avg = _st.mean(p.return_to_exit_pct for p in filtered)
        n_tp = sum(1 for p in filtered if p.was_added)
        n_fp = sum(1 for p in filtered if not p.was_added)
        chart_data.append((label, avg, n_tp, n_fp, len(filtered)))

    dw = PAGE_W - 2 * MARGIN
    bar_h = 14
    gap = 5
    label_w = 2.8 * cm
    max_ret = 28.0
    bar_area = float(dw) - float(label_w) - 40

    chart_h = len(chart_data) * (bar_h + gap) + 30
    d = Drawing(dw, chart_h)

    for i, (label, avg, n_tp, n_fp, n) in enumerate(chart_data):
        y = chart_h - 20 - i * (bar_h + gap)
        bar_len = min(avg / max_ret, 1.0) * bar_area
        bar_color = GREEN if n_fp == 0 else TEAL

        # Label
        d.add(String(float(label_w) - 4, y + 3, label,
                     fontSize=7.5, fontName="Helvetica", fillColor=BLACK,
                     textAnchor="end"))
        # Bar
        d.add(Rect(float(label_w), y, bar_len, bar_h,
                   fillColor=bar_color, strokeColor=None))
        # Return text
        sign = "+" if avg >= 0 else ""
        annot = f"{sign}{avg:.1f}%  ({n_tp}TP/{n_fp}FP  n={n})"
        d.add(String(float(label_w) + bar_len + 4, y + 3, annot,
                     fontSize=7, fontName="Helvetica", fillColor=DGRAY))

    items.append(d)
    items.append(Paragraph(
        "<font color='#2E7D32'>■</font> Green = zero false positives in cycle  "
        "<font color='#00796B'>■</font> Teal = ≥1 false positive (managed)",
        ParagraphStyle("legend", fontSize=7.5, leading=11, textColor=DGRAY,
                       fontName="Helvetica", spaceAfter=6),
    ))
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Full trade log
# ─────────────────────────────────────────────────────────────────────────────
def _entry_rationale(p) -> str:
    """Build a compact why-we-bought string from observable data at screen date."""
    parts = []
    if p.proposed_event_type == "Standard Add":
        parts.append(f"Approaching MSCI Poland Standard (full cap ${p.full_cap_usd_m:,.0f}M "
                     f"vs $2,500M threshold, +{p.pct_above_threshold:.0f}% above)")
    elif p.proposed_event_type == "SC Add":
        parts.append(f"Approaching MSCI EM Small Cap (full cap ${p.full_cap_usd_m:,.0f}M, "
                     f"+{p.pct_above_threshold:.0f}% above $127M threshold)")
    elif p.proposed_event_type == "Weight Increase":
        parts.append(f"MSCI member outperforming peers → weight increase likely "
                     f"(cap ${p.full_cap_usd_m:,.0f}M, {p.pct_above_threshold:+.0f}% vs threshold)")

    parts.append(f"RS {p.rs_percentile:.0f}th pct vs WIG-ALL")
    parts.append(f"{'above' if p.above_200d_ma else 'below'} 200d MA")
    parts.append(f"ATVR {p.atvr_3m_pct:.1f}%")
    parts.append(f"Float-adj ${p.float_adj_cap_usd_m:,.0f}M")
    return "; ".join(parts)


def _exit_rationale(p) -> str:
    if p.was_added:
        return (f"MSCI confirmed inclusion at {p.review_label} review. "
                f"Held to effective date — passive fund demand absorbed at T+0.")
    else:
        fp_short = p.failure_reason[:90] + ("…" if len(p.failure_reason) > 90 else "")
        return f"NOT included at {p.review_label} review. Closed at announcement. Reason: {fp_short}"


def trade_log_section(positions, styles):
    items = []
    items.append(PageBreak())
    items.append(Paragraph("3. Full Trade Log", styles["h1"]))
    items.append(Paragraph(
        "All 44 screened positions. Entry = T−45 close. "
        "True positives (TP) exit at effective date. "
        "False positives (FP) exit at announcement date. "
        "20 bps round-trip cost applied. "
        "Filter column shows whether momentum filter (RS ≥ 60th + above 200d MA) passed.",
        styles["body"],
    ))
    items.append(Spacer(1, 0.3 * cm))

    # Group by review cycle
    reviews = {}
    for p in positions:
        reviews.setdefault((p.review_id, p.review_label), []).append(p)

    import statistics as _st

    for (rid, label), cpos in sorted(reviews.items(), key=lambda x: x[0][0]):
        # Section header
        filtered_pos = [p for p in cpos if p.momentum_passes_filter]
        cycle_ret = _st.mean(p.return_to_exit_pct for p in filtered_pos) if filtered_pos else None
        ret_str = f"{cycle_ret:+.1f}%" if cycle_ret is not None else "—"
        n_tp = sum(1 for p in cpos if p.was_added)
        n_fp = sum(1 for p in cpos if not p.was_added)

        hdr = Table(
            [[Paragraph(f"MSCI SAR — {label}", ParagraphStyle(
                "ch", fontSize=9, fontName="Helvetica-Bold", textColor=WHITE)),
              Paragraph(f"Cycle avg return (filtered): {ret_str}   |   "
                        f"{len(cpos)} positions screened  ({n_tp} TP / {n_fp} FP)",
                        ParagraphStyle("ch2", fontSize=8, fontName="Helvetica",
                                       textColor=colors.HexColor("#B0BEC5"), alignment=TA_RIGHT))]],
            colWidths=[(PAGE_W - 2 * MARGIN) * 0.4, (PAGE_W - 2 * MARGIN) * 0.6],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]),
        )
        items.append(KeepTogether([hdr]))
        items.append(Spacer(1, 0.1 * cm))

        # Trade rows
        col_w = [(PAGE_W - 2 * MARGIN) * x
                 for x in [0.13, 0.12, 0.08, 0.07, 0.06, 0.06, 0.06, 0.42]]

        header_row = [Paragraph(h, ParagraphStyle(
            "th", fontSize=7, fontName="Helvetica-Bold", textColor=WHITE))
            for h in ["Company", "Sector", "Entry date", "Entry PLN",
                      "Exit PLN", "Filter", "Outcome", "Entry rationale / Exit reason"]]

        trade_rows = [header_row]

        for p in sorted(cpos, key=lambda x: -x.rs_percentile):
            filt_s = styles["cell_green"] if p.momentum_passes_filter else styles["cell_gray"]
            filt_txt = Paragraph("✓ PASS" if p.momentum_passes_filter else "✗ skip", filt_s)

            if p.was_added:
                outcome_style = styles["cell_green"]
                outcome_txt = "TP"
            else:
                outcome_style = styles["cell_red"]
                outcome_txt = "FP"

            ret_val = p.return_to_exit_pct
            if ret_val >= 10:
                ret_style = styles["cell_green"]
            elif ret_val >= 0:
                ret_style = styles["cell"]
            else:
                ret_style = styles["cell_red"]

            # Rationale cell: entry on top, exit below with divider
            entry_r = _entry_rationale(p)
            exit_r = _exit_rationale(p)
            rationale_text = (
                f"<b>BUY:</b> {entry_r}<br/>"
                f"<font color='#757575'>──────────────</font><br/>"
                f"<b>{'SELL (TP)' if p.was_added else 'CLOSE (FP)'}:</b> {exit_r}<br/>"
                f"<b>Return: </b>"
            )
            rationale_para = Paragraph(
                f"<b>BUY:</b> {entry_r}<br/>"
                f"<b>{'SELL (TP)' if p.was_added else 'CLOSE (FP)'}:</b> "
                f"<font color='#757575'>{exit_r}</font><br/>"
                f"<b>Return:</b> <b>{ret_val:+.1f}%</b>",
                ParagraphStyle("rat", fontSize=6.8, leading=10, fontName="Helvetica",
                               textColor=BLACK),
            )

            trade_rows.append([
                Paragraph(p.company[:22], styles["cell_bold"]),
                Paragraph(p.sector.split("—")[0].strip()[:18], styles["cell_gray"]),
                Paragraph(p.screen_date, styles["cell"]),
                Paragraph(f"PLN {p.price_at_screen_pln:,.1f}", styles["cell"]),
                Paragraph(f"PLN {p.exit_price_pln:,.1f}", ret_style),
                filt_txt,
                Paragraph(outcome_txt, outcome_style),
                rationale_para,
            ])

        t = Table(trade_rows, colWidths=col_w, repeatRows=1)
        ts = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGRAY]),
            ("GRID", (0, 0), (-1, -1), 0.25, MGRAY),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
        t.setStyle(ts)
        items.append(t)
        items.append(Spacer(1, 0.4 * cm))

    return items


# ─────────────────────────────────────────────────────────────────────────────
# False positive deep-dive
# ─────────────────────────────────────────────────────────────────────────────
def fp_section(positions, styles):
    items = []
    items.append(PageBreak())
    items.append(Paragraph("4. False Positive Analysis", styles["h1"]))
    items.append(Paragraph(
        "False positives (FP) are stocks that passed our T−45 screen but were ultimately "
        "NOT added by MSCI at that review. Managing these is the central challenge of the strategy: "
        "we cannot know at screen time which positions will disappoint. "
        "The momentum filter is our primary tool for reducing FP exposure.",
        styles["body"],
    ))
    items.append(Spacer(1, 0.2 * cm))

    fp_all = [p for p in positions if not p.was_added]
    fp_filt = [p for p in fp_all if p.momentum_passes_filter]
    fp_excl = [p for p in fp_all if not p.momentum_passes_filter]

    import statistics as _st

    summary_data = [
        ["", "Count", "Avg return", "Min return", "Max return"],
        ["All false positives",
         str(len(fp_all)),
         f"{_st.mean(p.return_to_exit_pct for p in fp_all):+.1f}%" if fp_all else "—",
         f"{min(p.return_to_exit_pct for p in fp_all):+.1f}%" if fp_all else "—",
         f"{max(p.return_to_exit_pct for p in fp_all):+.1f}%" if fp_all else "—"],
        ["FPs passing momentum filter (residual)",
         str(len(fp_filt)),
         f"{_st.mean(p.return_to_exit_pct for p in fp_filt):+.1f}%" if fp_filt else "—",
         f"{min(p.return_to_exit_pct for p in fp_filt):+.1f}%" if fp_filt else "—",
         f"{max(p.return_to_exit_pct for p in fp_filt):+.1f}%" if fp_filt else "—"],
        ["FPs excluded by filter ← filter saves these",
         str(len(fp_excl)),
         f"{_st.mean(p.return_to_exit_pct for p in fp_excl):+.1f}%" if fp_excl else "—",
         f"{min(p.return_to_exit_pct for p in fp_excl):+.1f}%" if fp_excl else "—",
         f"{max(p.return_to_exit_pct for p in fp_excl):+.1f}%" if fp_excl else "—"],
    ]
    col_w = [(PAGE_W - 2 * MARGIN) * x for x in [0.44, 0.14, 0.14, 0.14, 0.14]]
    t = Table(
        [[Paragraph(c, styles["cell_bold"] if r == 0 else styles["cell"]) for c in row]
         for r, row in enumerate(summary_data)],
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
        ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#E8F5E9")),
    ]))
    items.append(t)
    items.append(Spacer(1, 0.3 * cm))

    # FP detail table
    items.append(Paragraph("False Positive Detail", styles["h2"]))
    fp_detail_data = [
        [Paragraph(h, styles["cell_bold"]) for h in
         ["Company", "Review", "RS%", "Filter", "Return", "Failure reason"]]
    ]
    for p in sorted(fp_all, key=lambda x: x.return_to_exit_pct):
        filt_s = styles["cell_amber"] if p.momentum_passes_filter else styles["cell_gray"]
        ret_s = styles["cell_red"] if p.return_to_exit_pct < 0 else styles["cell"]
        fp_detail_data.append([
            Paragraph(p.company, styles["cell_bold"]),
            Paragraph(p.review_label, styles["cell"]),
            Paragraph(str(int(p.rs_percentile)), styles["cell"]),
            Paragraph("PASS" if p.momentum_passes_filter else "skip", filt_s),
            Paragraph(f"{p.return_to_exit_pct:+.1f}%", ret_s),
            Paragraph(p.failure_reason[:95] + ("…" if len(p.failure_reason) > 95 else ""),
                      styles["small"]),
        ])
    col_w2 = [(PAGE_W - 2 * MARGIN) * x for x in [0.18, 0.10, 0.06, 0.07, 0.08, 0.51]]
    t2 = Table(fp_detail_data, colWidths=col_w2)
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LGRAY]),
        ("GRID", (0, 0), (-1, -1), 0.25, MGRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    items.append(t2)

    items.append(Spacer(1, 0.3 * cm))
    items.append(Paragraph(
        f"<b>Why false positives still earn ~+0.1% on average:</b> "
        "During the T−45 to announcement window, the stock participates in general market "
        "and sector momentum — it drifts up slightly. On the announcement day, when the stock "
        "is NOT named as a new addition, traders who pre-positioned exit, creating a −2 to −4% "
        "reversal. The net effect is near-zero. The real cost is opportunity cost: capital "
        f"deployed in {len(fp_all)} false positives earned +0.1% vs +13.8% for true positives.",
        styles["body"],
    ))
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Caveats & methodology
# ─────────────────────────────────────────────────────────────────────────────
def methodology_section(styles):
    items = []
    items.append(PageBreak())
    items.append(Paragraph("5. Methodology & Caveats", styles["h1"]))

    method_text = [
        ("<b>Screening criteria (observable at T−45 — no look-ahead):</b>",
         "Market cap within 20% above threshold (MSCI Standard: $2,500M full cap / "
         "$1,300M float-adj; MSCI EM Small Cap: $127M full cap / $95M float-adj). "
         "ATVR ≥ 15% (MSCI minimum liquidity gate). Already-MSCI-members screened for "
         "weight-increase potential based on outperformance vs other members."),
        ("<b>Momentum filter:</b>",
         "RS percentile ≥ 60th vs WIG-ALL universe (trailing 12-month return, "
         "1-month skip) AND price above 200-day MA. Both conditions required. "
         "Academic basis: Jegadeesh & Titman (1993), Carhart (1997). "
         "Practitioner rationale: momentum confirms fundamental improvement; "
         "weak-momentum stocks are more likely to be false positives."),
        ("<b>Entry / exit:</b>",
         "Entry at T−45 closing price (deep accumulation phase; before most institutional "
         "arb flow). True-positive exit at effective date close (T+0) — passive fund "
         "demand absorbed. False-positive exit at announcement date close (position closed "
         "the day MSCI announces without our stock; do not hold through effective date)."),
        ("<b>Transaction costs:</b>",
         "20 bps round-trip (10 bps buy + 10 bps sell). Realistic for institutional "
         "managers on WSE. Retail investors face 20–50 bps; this reduces net returns by "
         "0–0.3pp per trade."),
        ("<b>Portfolio construction:</b>",
         "Equal weight across all positions in a given cycle. Maximum 33% per position "
         "(to limit concentration). Capital is redeployed each cycle (~twice per year)."),
        ("<b>Price data accuracy:</b>",
         "Prices are approximated from WSE/stooq historical data and institutional "
         "research. Accuracy is ±2–3%. Directional conclusions (positive/negative return, "
         "relative ordering of TP vs FP) are robust to this level of approximation."),
        ("<b>Survivorship bias:</b>",
         "The database includes only stocks that were screened. Stocks that were "
         "eligible but not screened are false negatives (missed opportunities). "
         "The strategy cannot be run on a static universe — it requires real-time "
         "market cap monitoring at each T−45 date."),
        ("<b>Sample size limitation:</b>",
         "15 MSCI SAR cycles across 7.25 years. Statistical conclusions should be "
         "treated with caution. The Sharpe ratio of 2.12 (filtered) is computed on "
         "position-level returns, not time-series monthly returns — cannot be directly "
         "compared to fund Sharpe ratios. Cyclically, the strategy concentrates risk "
         "into ~6-week windows around each review cycle."),
    ]

    for bold, body in method_text:
        items.append(Paragraph(bold, styles["h2"]))
        items.append(Paragraph(body, styles["body"]))

    items.append(Spacer(1, 0.4 * cm))
    items.append(HRFlowable(width="100%", thickness=1, color=AMBER, spaceAfter=8))
    items.append(Paragraph(
        "⚠  DISCLAIMER: This report is for informational and research purposes only. "
        "It does not constitute investment advice. Past backtest performance does not "
        "guarantee future results. Index inclusion is a mechanical process but MSCI "
        "retains committee discretion for borderline cases. "
        "All trade data uses approximate historical prices.",
        styles["caveat"],
    ))
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Page numbering
# ─────────────────────────────────────────────────────────────────────────────
def _on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(DGRAY)
    canvas.drawString(MARGIN, 0.7 * cm,
                      "MSCI Poland Walk-Forward Backtest  |  Confidential — For Research Use Only")
    canvas.drawRightString(PAGE_W - MARGIN, 0.7 * cm, f"Page {doc.page}")
    canvas.restoreState()


# ─────────────────────────────────────────────────────────────────────────────
# Main builder
# ─────────────────────────────────────────────────────────────────────────────
def build_pdf(output_path: str = "msci_poland_backtest_report.pdf") -> str:
    positions = build_screen_events()
    all_stats  = simulate_portfolio(positions, use_momentum_filter=False)
    filt_stats = simulate_portfolio(positions, use_momentum_filter=True)
    styles     = build_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=1.4 * cm,
        title="MSCI Poland Walk-Forward Backtest — Trade Log",
        author="MZApp Research",
        subject="Index Inclusion Alpha Strategy",
    )

    story = []
    story += cover_page(styles)
    story.append(PageBreak())
    story += summary_section(styles, all_stats, filt_stats)
    story.append(Spacer(1, 0.4 * cm))
    story += cycle_chart(positions, styles)
    story += trade_log_section(positions, styles)
    story += fp_section(positions, styles)
    story += methodology_section(styles)

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return output_path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "msci_poland_backtest_report.pdf"
    path = build_pdf(out)
    print(f"PDF saved → {path}")
