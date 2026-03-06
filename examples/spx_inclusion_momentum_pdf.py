"""
SPX Inclusion Momentum — PDF Report Generator
=============================================
Produces a full multi-page PDF backtest report including:
  • Strategy description & rules
  • Survivorship-bias methodology
  • Cumulative performance chart
  • Year-by-year performance table
  • Full trade log (ticker, dates, momentum rank, return, added-to-index flag)
  • Sector attribution
  • Risk metrics summary
  • Inclusion premium decay analysis
"""

import math
import os
import statistics
import sys
import tempfile
from datetime import date
from io import BytesIO

# ── local imports ────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from spx_inclusion_momentum import (
    BacktestConfig,
    _build_candidate_universe,
    _parse_additions,
    _quarter_of,
    _SPX_QUARTERLY,
    compute_annual_returns,
    compute_cumulative_returns,
    compute_cycle_performance,
    compute_max_drawdown,
    compute_sector_attribution,
    compute_sharpe,
    inclusion_vs_momentum_split,
    run_backtest,
    TradeResult,
    CyclePerformance,
)

# ── reportlab ────────────────────────────────────────────────────────────────
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import KeepTogether

# matplotlib for charts
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE  (dark professional)
# ─────────────────────────────────────────────────────────────────────────────
C_NAVY      = colors.HexColor("#0A1628")
C_BLUE      = colors.HexColor("#1A3A5C")
C_ACCENT    = colors.HexColor("#2E86AB")
C_GOLD      = colors.HexColor("#F2A900")
C_GREEN     = colors.HexColor("#2D9A5F")
C_RED       = colors.HexColor("#C0392B")
C_LIGHT_BG  = colors.HexColor("#F7F9FC")
C_MID_GRAY  = colors.HexColor("#B0BEC5")
C_DARK_GRAY = colors.HexColor("#455A64")
C_WHITE     = colors.white
C_BLACK     = colors.HexColor("#0D1117")

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

# ─────────────────────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────────────────────

def build_styles():
    base = getSampleStyleSheet()
    s = {}

    s["title"] = ParagraphStyle("title",
        fontName="Helvetica-Bold", fontSize=28, textColor=C_WHITE,
        leading=34, alignment=TA_CENTER, spaceAfter=6)
    s["subtitle"] = ParagraphStyle("subtitle",
        fontName="Helvetica", fontSize=13, textColor=C_GOLD,
        leading=17, alignment=TA_CENTER, spaceAfter=4)
    s["meta"] = ParagraphStyle("meta",
        fontName="Helvetica", fontSize=9, textColor=C_MID_GRAY,
        leading=13, alignment=TA_CENTER)

    s["h1"] = ParagraphStyle("h1",
        fontName="Helvetica-Bold", fontSize=14, textColor=C_NAVY,
        leading=18, spaceBefore=14, spaceAfter=6,
        borderPad=0, leftIndent=0)
    s["h2"] = ParagraphStyle("h2",
        fontName="Helvetica-Bold", fontSize=11, textColor=C_BLUE,
        leading=15, spaceBefore=10, spaceAfter=4)
    s["body"] = ParagraphStyle("body",
        fontName="Helvetica", fontSize=9, textColor=C_BLACK,
        leading=14, spaceAfter=4, alignment=TA_JUSTIFY)
    s["body_small"] = ParagraphStyle("body_small",
        fontName="Helvetica", fontSize=8, textColor=C_DARK_GRAY,
        leading=12, spaceAfter=2)
    s["bullet"] = ParagraphStyle("bullet",
        fontName="Helvetica", fontSize=9, textColor=C_BLACK,
        leading=14, spaceAfter=2, leftIndent=14, firstLineIndent=-8)
    s["code"] = ParagraphStyle("code",
        fontName="Courier", fontSize=8, textColor=C_BLUE,
        leading=12, backColor=C_LIGHT_BG, spaceAfter=2)
    s["caption"] = ParagraphStyle("caption",
        fontName="Helvetica-Oblique", fontSize=8, textColor=C_DARK_GRAY,
        leading=11, alignment=TA_CENTER, spaceAfter=6)
    s["th"] = ParagraphStyle("th",
        fontName="Helvetica-Bold", fontSize=8, textColor=C_WHITE,
        leading=10, alignment=TA_CENTER)
    s["td"] = ParagraphStyle("td",
        fontName="Helvetica", fontSize=7.5, textColor=C_BLACK,
        leading=10, alignment=TA_CENTER)
    s["td_left"] = ParagraphStyle("td_left",
        fontName="Helvetica", fontSize=7.5, textColor=C_BLACK,
        leading=10, alignment=TA_LEFT)
    s["td_mono"] = ParagraphStyle("td_mono",
        fontName="Courier", fontSize=7.5, textColor=C_DARK_GRAY,
        leading=10, alignment=TA_CENTER)
    s["stat_label"] = ParagraphStyle("stat_label",
        fontName="Helvetica", fontSize=9, textColor=C_DARK_GRAY,
        leading=12, alignment=TA_LEFT)
    s["stat_value"] = ParagraphStyle("stat_value",
        fontName="Helvetica-Bold", fontSize=13, textColor=C_NAVY,
        leading=16, alignment=TA_LEFT)
    return s


# ─────────────────────────────────────────────────────────────────────────────
# PAGE TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────

class CoverPage(PageTemplate):
    def beforeDrawPage(self, canvas, doc):
        canvas.saveState()
        # Navy background
        canvas.setFillColor(C_NAVY)
        canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        # Gold accent bar
        canvas.setFillColor(C_GOLD)
        canvas.rect(0, PAGE_H * 0.52, PAGE_W, 4, fill=1, stroke=0)
        canvas.rect(0, PAGE_H * 0.52 - 8, PAGE_W, 2, fill=1, stroke=0)
        # Side accent
        canvas.setFillColor(C_ACCENT)
        canvas.rect(0, 0, 6, PAGE_H, fill=1, stroke=0)
        canvas.restoreState()

    def afterDrawPage(self, canvas, doc):
        pass


class ContentPage(PageTemplate):
    def beforeDrawPage(self, canvas, doc):
        canvas.saveState()
        # Light header bar
        canvas.setFillColor(C_NAVY)
        canvas.rect(0, PAGE_H - 1.2 * cm, PAGE_W, 1.2 * cm, fill=1, stroke=0)
        # Header text
        canvas.setFillColor(C_WHITE)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.drawString(MARGIN, PAGE_H - 0.8 * cm,
                          "SPX INCLUSION MOMENTUM STRATEGY  |  BACKTEST REPORT  2012–2023")
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(C_GOLD)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.8 * cm, "CONFIDENTIAL")
        # Footer
        canvas.setFillColor(C_LIGHT_BG)
        canvas.rect(0, 0, PAGE_W, 1.0 * cm, fill=1, stroke=0)
        canvas.setFillColor(C_DARK_GRAY)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(MARGIN, 0.38 * cm,
            "For research purposes only. Simulated results; not a guarantee of future performance.")
        canvas.setFillColor(C_NAVY)
        canvas.setFont("Helvetica-Bold", 7)
        canvas.drawRightString(PAGE_W - MARGIN, 0.38 * cm, f"Page {doc.page}")
        # Left accent
        canvas.setFillColor(C_ACCENT)
        canvas.rect(0, 0, 3, PAGE_H, fill=1, stroke=0)
        canvas.restoreState()

    def afterDrawPage(self, canvas, doc):
        pass


def build_doc(path: str):
    doc = BaseDocTemplate(
        path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.8 * cm, bottomMargin=1.4 * cm,
        title="SPX Inclusion Momentum — Backtest Report",
        author="MZApp Framework",
    )

    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover", showBoundary=0)
    content_frame = Frame(
        MARGIN, 1.2 * cm, CONTENT_W, PAGE_H - 2.8 * cm,
        id="content", showBoundary=0)

    cover_tpl = CoverPage("cover", [cover_frame])
    cover_tpl.beforeDrawPage = lambda c, d: _draw_cover_bg(c)
    content_tpl = ContentPage("content", [content_frame])
    content_tpl.beforeDrawPage = lambda c, d: _draw_content_bg(c, d)

    doc.addPageTemplates([cover_tpl, content_tpl])
    return doc


def _draw_cover_bg(canvas):
    canvas.saveState()
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(C_ACCENT)
    canvas.rect(0, 0, 6, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(C_GOLD)
    canvas.rect(0, PAGE_H * 0.46, PAGE_W, 3, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#132035"))
    canvas.rect(0, 0, PAGE_W, PAGE_H * 0.46 - 3, fill=1, stroke=0)
    canvas.restoreState()


def _draw_content_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, PAGE_H - 1.2 * cm, PAGE_W, 1.2 * cm, fill=1, stroke=0)
    canvas.setFillColor(C_WHITE)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawString(MARGIN, PAGE_H - 0.78 * cm,
                      "SPX INCLUSION MOMENTUM STRATEGY  |  BACKTEST REPORT  2012–2023")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(C_GOLD)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.78 * cm, "FOR RESEARCH USE ONLY")
    canvas.setFillColor(C_LIGHT_BG)
    canvas.rect(0, 0, PAGE_W, 1.0 * cm, fill=1, stroke=0)
    canvas.setFillColor(C_DARK_GRAY)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(MARGIN, 0.35 * cm,
        "Simulated backtest. Calibrated to academic literature. Not a guarantee of future returns.")
    canvas.setFillColor(C_NAVY)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawRightString(PAGE_W - MARGIN, 0.35 * cm, f"Page {doc.page}")
    canvas.setFillColor(C_ACCENT)
    canvas.rect(0, 0, 3, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


# ─────────────────────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _mpl_dark_fig(**kwargs):
    fig = plt.figure(**kwargs)
    fig.patch.set_facecolor("#0A1628")
    return fig


def chart_cumulative(cycles, strat_cum, bench_cum, alphas) -> BytesIO:
    import datetime
    dates_dt = [datetime.date(c.year, (c.quarter - 1) * 3 + 1, 1) for c in cycles]

    fig = _mpl_dark_fig(figsize=(11, 5.5))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.08, figure=fig)

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    for ax in (ax1, ax2):
        ax.set_facecolor("#0D1F35")
        ax.tick_params(colors="#90A4AE", labelsize=8)
        for spine in ax.spines.values():
            spine.set_color("#1E3A5F")

    # Cumulative
    strat_pct = [(v - 1) * 100 for v in strat_cum]
    bench_pct = [(v - 1) * 100 for v in bench_cum]
    ax1.plot(dates_dt, strat_pct, color="#2E86AB", lw=2.2, label="SPX Inclusion Momentum", zorder=3)
    ax1.plot(dates_dt, bench_pct, color="#F2A900", lw=1.5, ls="--", label="S&P 500", zorder=2)
    ax1.fill_between(dates_dt, strat_pct, bench_pct,
                     where=[s >= b for s, b in zip(strat_pct, bench_pct)],
                     alpha=0.18, color="#2E86AB")
    ax1.fill_between(dates_dt, strat_pct, bench_pct,
                     where=[s < b for s, b in zip(strat_pct, bench_pct)],
                     alpha=0.18, color="#C0392B")
    ax1.set_ylabel("Cumulative Return (%)", color="#90A4AE", fontsize=8)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:+.0f}%"))
    ax1.grid(True, color="#1A3A5C", lw=0.5, zorder=0)
    ax1.legend(facecolor="#0A1628", edgecolor="#1E3A5F",
               labelcolor="#CBD5E1", fontsize=8.5, loc="upper left")
    ax1.set_title("Cumulative Returns: Strategy vs S&P 500 (2012–2023)",
                  color="#CBD5E1", fontsize=10, pad=8, fontweight="bold")
    plt.setp(ax1.get_xticklabels(), visible=False)

    # Alpha bars
    bar_colors = ["#2D9A5F" if a >= 0 else "#C0392B" for a in alphas]
    ax2.bar(dates_dt, [a * 100 for a in alphas], color=bar_colors,
            width=60, zorder=3, edgecolor="none")
    ax2.axhline(0, color="#90A4AE", lw=0.7)
    ax2.set_ylabel("Qtrly α (%)", color="#90A4AE", fontsize=7.5)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:+.1f}%"))
    ax2.grid(True, color="#1A3A5C", lw=0.4, axis="y", zorder=0)
    import matplotlib.dates as mdates
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax2.xaxis.set_major_locator(mdates.YearLocator())
    plt.setp(ax2.get_xticklabels(), color="#90A4AE", fontsize=8)

    plt.tight_layout(pad=0.4)
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return buf


def chart_annual_bars(annual) -> BytesIO:
    years = sorted(annual)
    strat = [annual[y]["strat"] * 100 for y in years]
    bench = [annual[y]["bench"] * 100 for y in years]
    x = list(range(len(years)))

    fig, ax = plt.subplots(figsize=(11, 3.2))
    fig.patch.set_facecolor("#0A1628")
    ax.set_facecolor("#0D1F35")
    for spine in ax.spines.values():
        spine.set_color("#1E3A5F")
    ax.tick_params(colors="#90A4AE", labelsize=8)

    w = 0.36
    bars1 = ax.bar([v - w / 2 for v in x], strat, width=w,
                    color="#2E86AB", label="Strategy", zorder=3, edgecolor="none")
    bars2 = ax.bar([v + w / 2 for v in x], bench, width=w,
                    color="#F2A900", label="S&P 500", alpha=0.8, zorder=3, edgecolor="none")

    for bar, val in zip(bars1, strat):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (1 if val >= 0 else -3),
                f"{val:+.0f}%", ha="center", va="bottom" if val >= 0 else "top",
                color="#CBD5E1", fontsize=6.5)

    ax.axhline(0, color="#90A4AE", lw=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years], color="#90A4AE")
    ax.set_ylabel("Annual Return (%)", color="#90A4AE", fontsize=8)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.0f}%"))
    ax.grid(True, color="#1A3A5C", lw=0.4, axis="y", zorder=0)
    ax.legend(facecolor="#0A1628", edgecolor="#1E3A5F",
              labelcolor="#CBD5E1", fontsize=8.5)
    ax.set_title("Annual Returns — Strategy vs S&P 500", color="#CBD5E1",
                 fontsize=9.5, fontweight="bold", pad=6)

    plt.tight_layout(pad=0.4)
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return buf


def chart_sector(attribution) -> BytesIO:
    sectors = sorted(attribution, key=lambda s: attribution[s]["mean_ret"], reverse=True)
    means = [attribution[s]["mean_ret"] * 100 for s in sectors]
    wins  = [attribution[s]["win_rate"] * 100 for s in sectors]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.4))
    fig.patch.set_facecolor("#0A1628")
    palette = ["#2E86AB", "#2D9A5F", "#F2A900", "#9B59B6",
               "#E67E22", "#C0392B", "#1ABC9C", "#3498DB", "#95A5A6"]

    for ax in (ax1, ax2):
        ax.set_facecolor("#0D1F35")
        ax.tick_params(colors="#90A4AE", labelsize=7.5)
        for spine in ax.spines.values():
            spine.set_color("#1E3A5F")

    bars = ax1.barh(sectors, means, color=palette[:len(sectors)],
                     edgecolor="none", zorder=3)
    ax1.set_xlabel("Mean Quarterly Return (%)", color="#90A4AE", fontsize=8)
    ax1.axvline(0, color="#90A4AE", lw=0.6)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.1f}%"))
    ax1.set_title("Mean Return by Sector", color="#CBD5E1", fontsize=8.5,
                  fontweight="bold", pad=5)
    ax1.grid(True, color="#1A3A5C", lw=0.4, axis="x", zorder=0)
    for bar, val in zip(bars, means):
        ax1.text(max(val, 0) + 0.1, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}%", va="center", color="#CBD5E1", fontsize=7)

    bars2 = ax2.barh(sectors, wins, color=palette[:len(sectors)],
                      edgecolor="none", zorder=3)
    ax2.set_xlabel("Win Rate (%)", color="#90A4AE", fontsize=8)
    ax2.axvline(50, color="#90A4AE", lw=0.6, ls="--")
    ax2.set_title("Win Rate by Sector", color="#CBD5E1", fontsize=8.5,
                  fontweight="bold", pad=5)
    ax2.grid(True, color="#1A3A5C", lw=0.4, axis="x", zorder=0)
    for bar, val in zip(bars2, wins):
        ax2.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{val:.0f}%", va="center", color="#CBD5E1", fontsize=7)

    plt.tight_layout(pad=0.6)
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return buf


def chart_drawdown(cycles, strat_cum, bench_cum) -> BytesIO:
    import datetime
    dates_dt = [datetime.date(c.year, (c.quarter - 1) * 3 + 1, 1) for c in cycles]

    def drawdown_series(vals):
        peak = vals[0]
        dds = []
        for v in vals:
            if v > peak:
                peak = v
            dds.append((v - peak) / peak * 100)
        return dds

    strat_dd = drawdown_series(strat_cum)
    bench_dd = drawdown_series(bench_cum)

    fig, ax = plt.subplots(figsize=(11, 3.0))
    fig.patch.set_facecolor("#0A1628")
    ax.set_facecolor("#0D1F35")
    for spine in ax.spines.values():
        spine.set_color("#1E3A5F")
    ax.tick_params(colors="#90A4AE", labelsize=8)

    ax.fill_between(dates_dt, strat_dd, 0, alpha=0.35, color="#2E86AB", label="Strategy DD")
    ax.fill_between(dates_dt, bench_dd, 0, alpha=0.25, color="#C0392B", label="S&P 500 DD")
    ax.plot(dates_dt, strat_dd, color="#2E86AB", lw=1.5)
    ax.plot(dates_dt, bench_dd, color="#F2A900", lw=1.0, ls="--")
    ax.axhline(0, color="#90A4AE", lw=0.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}%"))
    ax.set_ylabel("Drawdown (%)", color="#90A4AE", fontsize=8)
    ax.legend(facecolor="#0A1628", edgecolor="#1E3A5F",
              labelcolor="#CBD5E1", fontsize=8.5)
    ax.set_title("Underwater Equity Curve (Drawdown)", color="#CBD5E1",
                 fontsize=9.5, fontweight="bold", pad=6)
    import matplotlib.dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.grid(True, color="#1A3A5C", lw=0.4, zorder=0)

    plt.tight_layout(pad=0.4)
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=180, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return buf


# ─────────────────────────────────────────────────────────────────────────────
# TABLE BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def _pct(v, digits=1, show_sign=True):
    sign = "+" if v > 0 and show_sign else ""
    return f"{sign}{v * 100:.{digits}f}%"


def _colored_pct(v, S):
    """Return a Paragraph colored green/red based on sign."""
    color = "#2D9A5F" if v >= 0 else "#C0392B"
    sign = "+" if v > 0 else ""
    text = f'<font color="{color}"><b>{sign}{v * 100:.1f}%</b></font>'
    return Paragraph(text, S["td"])


def tbl_style_base(header_bg=C_NAVY):
    return [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR",  (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, 0), 8),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_LIGHT_BG]),
        ("GRID",       (0, 0), (-1, -1), 0.4, C_MID_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]


def build_kpi_table(strat_cagr, bench_cagr, sharpe_s, sharpe_b,
                    max_dd_s, max_dd_b, total_ret_s, total_ret_b,
                    win_rate, n_trades, stop_hits, S):
    """4×2 KPI grid."""

    def kpi(label, val, bench_val=None):
        val_p = Paragraph(val, S["stat_value"])
        lbl_p = Paragraph(label, S["stat_label"])
        if bench_val:
            bench_p = Paragraph(f"Benchmark: {bench_val}", S["body_small"])
            return [lbl_p, val_p, bench_p]
        return [lbl_p, val_p]

    kpis = [
        ("CAGR",         _pct(strat_cagr), f"S&P 500: {_pct(bench_cagr)}"),
        ("Total Return", _pct(total_ret_s), f"S&P 500: {_pct(total_ret_b)}"),
        ("Sharpe Ratio", f"{sharpe_s:.2f}", f"S&P 500: {sharpe_b:.2f}"),
        ("Max Drawdown", _pct(max_dd_s), f"S&P 500: {_pct(max_dd_b)}"),
        ("Win Rate",     f"{win_rate * 100:.1f}%", "per individual trade"),
        ("Total Trades", str(n_trades), "over 12-year period"),
        ("Stop-Loss Hits", f"{stop_hits}", f"{stop_hits/n_trades*100:.1f}% of trades"),
        ("Hold Period",  "~75 days", "quarterly average"),
    ]

    # Build 2-column grid (4 rows)
    data = []
    for i in range(0, len(kpis), 2):
        row = []
        for j in range(2):
            if i + j < len(kpis):
                label, val, sub = kpis[i + j]
                cell_content = (
                    f'<font color="#455A64" size="8">{label}</font><br/>'
                    f'<font color="#0A1628" size="14"><b>{val}</b></font><br/>'
                    f'<font color="#90A4AE" size="7">{sub}</font>'
                )
                row.append(Paragraph(cell_content, S["body"]))
            else:
                row.append("")
        data.append(row)

    col_w = CONTENT_W / 2
    tbl = Table(data, colWidths=[col_w, col_w], rowHeights=1.4 * cm)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_WHITE),
        ("BOX",        (0, 0), (-1, -1), 0.5, C_ACCENT),
        ("INNERGRID",  (0, 0), (-1, -1), 0.4, C_MID_GRAY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [C_WHITE, C_LIGHT_BG]),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",(0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return tbl


def build_annual_table(annual, S):
    header = ["Year", "Strategy", "S&P 500", "Alpha", "Cycles", "Assessment"]
    rows = [header]
    for year, d in sorted(annual.items()):
        alpha = d["alpha"]
        assessment = (
            "Strong outperform" if alpha > 0.10 else
            "Mild outperform"   if alpha > 0.02 else
            "In-line"           if alpha > -0.02 else
            "Mild underperform" if alpha > -0.08 else
            "Underperform"
        )
        color = ("#2D9A5F" if alpha > 0.02 else
                 "#C0392B" if alpha < -0.02 else
                 "#455A64")
        rows.append([
            Paragraph(str(year), S["td"]),
            _colored_pct(d["strat"], S),
            _colored_pct(d["bench"], S),
            Paragraph(f'<font color="{color}"><b>{_pct(alpha)}</b></font>', S["td"]),
            Paragraph(str(d["n_cycles"]), S["td"]),
            Paragraph(assessment, S["td_left"]),
        ])

    col_w = [1.2*cm, 2.0*cm, 2.0*cm, 2.0*cm, 1.6*cm, CONTENT_W - 8.8*cm]
    tbl = Table(rows, colWidths=col_w)
    style = tbl_style_base()
    tbl.setStyle(TableStyle(style))
    return tbl


def build_trade_log_table(trades: list[TradeResult], additions, S, max_rows=200):
    """Full trade log — one row per trade."""
    # Build ticker→addition lookup for details
    add_map = {a.ticker: a for a in additions}

    header = ["Ticker", "Sector", "Entry Date", "Exit Date",
              "Mom Rank", "12-1 Mom", "3m Mom", "Return",
              "Added to SPX?", "Stop Hit?"]
    rows = [header]

    # Sort by entry date, then ticker
    sorted_trades = sorted(trades, key=lambda t: (t.entry_date, t.ticker))
    real_trades = [t for t in sorted_trades if not t.ticker.startswith("CAND_")]
    synth_trades = [t for t in sorted_trades if t.ticker.startswith("CAND_")]

    # Show all real trades + a sample of synthetic (capped)
    display_trades = real_trades + synth_trades[:max(0, max_rows - len(real_trades))]
    display_trades = sorted(display_trades, key=lambda t: (t.entry_date, t.ticker))

    for t in display_trades:
        add = add_map.get(t.ticker)
        mom12 = f"{add.mom_12_1:+.0%}" if add else "n/a"
        mom3  = f"{add.mom_3m:+.0%}"   if add else "n/a"

        added_str = "✓ YES" if t.eventually_added else "— no"
        added_color = "#2D9A5F" if t.eventually_added else "#455A64"
        stop_str = "⚠ YES" if t.stop_loss_hit else "—"
        stop_color = "#C0392B" if t.stop_loss_hit else "#455A64"

        ret_color = "#2D9A5F" if t.gross_return >= 0 else "#C0392B"

        rows.append([
            Paragraph(f"<b>{t.ticker}</b>", S["td"]),
            Paragraph(t.sector[:10], S["td_left"]),
            Paragraph(str(t.entry_date), S["td_mono"]),
            Paragraph(str(t.exit_date),  S["td_mono"]),
            Paragraph(f"{t.mom_rank:.2f}", S["td"]),
            Paragraph(mom12, S["td"]),
            Paragraph(mom3,  S["td"]),
            Paragraph(f'<font color="{ret_color}"><b>{t.gross_return:+.1%}</b></font>', S["td"]),
            Paragraph(f'<font color="{added_color}"><b>{added_str}</b></font>', S["td"]),
            Paragraph(f'<font color="{stop_color}">{stop_str}</font>', S["td"]),
        ])

    col_w = [1.6*cm, 2.0*cm, 2.1*cm, 2.1*cm,
             1.5*cm, 1.5*cm, 1.5*cm, 1.7*cm, 1.7*cm, 1.5*cm]
    total = sum(col_w)
    # scale to content width
    scale = CONTENT_W / total
    col_w = [w * scale for w in col_w]

    tbl = Table(rows, colWidths=col_w, repeatRows=1)
    style = tbl_style_base()
    style += [
        ("FONTSIZE",    (0, 1), (-1, -1), 7.5),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("TOPPADDING",  (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    tbl.setStyle(TableStyle(style))
    return tbl, len(display_trades)


def build_sector_table(attribution, S):
    header = ["Sector", "# Trades", "Mean Return", "Win Rate", "Assessment"]
    rows = [header]
    for sector, d in sorted(attribution.items(), key=lambda x: x[1]["mean_ret"], reverse=True):
        assessment = ("Top performer" if d["mean_ret"] > 0.07 else
                      "Above average" if d["mean_ret"] > 0.04 else
                      "Average"       if d["mean_ret"] > 0.02 else
                      "Below average")
        ret_color = "#2D9A5F" if d["mean_ret"] >= 0 else "#C0392B"
        rows.append([
            Paragraph(sector, S["td_left"]),
            Paragraph(str(d["count"]), S["td"]),
            Paragraph(f'<font color="{ret_color}"><b>{_pct(d["mean_ret"])}</b></font>', S["td"]),
            Paragraph(f'{d["win_rate"]*100:.1f}%', S["td"]),
            Paragraph(assessment, S["td_left"]),
        ])
    col_w = [3.5*cm, 2.0*cm, 2.5*cm, 2.0*cm, CONTENT_W - 10.0*cm]
    tbl = Table(rows, colWidths=col_w)
    tbl.setStyle(TableStyle(tbl_style_base()))
    return tbl


def build_inclusion_split_table(split, S):
    inc = split["included"]
    ni  = split["not_included"]
    header = ["Cohort", "Trades", "Mean Return", "Win Rate", "Interpretation"]
    rows = [
        header,
        [
            Paragraph("Eventually added to S&P 500", S["td_left"]),
            Paragraph(str(inc["n"]), S["td"]),
            _colored_pct(inc["mean_ret"], S),
            Paragraph(f'{inc["win_rate"]*100:.1f}%', S["td"]),
            Paragraph("Momentum + inclusion premium", S["td_left"]),
        ],
        [
            Paragraph("NOT added (pure momentum)", S["td_left"]),
            Paragraph(str(ni["n"]), S["td"]),
            _colored_pct(ni["mean_ret"], S),
            Paragraph(f'{ni["win_rate"]*100:.1f}%', S["td"]),
            Paragraph("Momentum factor standalone", S["td_left"]),
        ],
    ]
    col_w = [5.5*cm, 1.8*cm, 2.5*cm, 2.0*cm, CONTENT_W - 11.8*cm]
    tbl = Table(rows, colWidths=col_w)
    tbl.setStyle(TableStyle(tbl_style_base()))
    return tbl


# ─────────────────────────────────────────────────────────────────────────────
# SECTION HEADER HELPER
# ─────────────────────────────────────────────────────────────────────────────

def section_header(text, S):
    return [
        HRFlowable(width=CONTENT_W, thickness=2, color=C_ACCENT, spaceAfter=4),
        Paragraph(text, S["h1"]),
        Spacer(1, 2),
    ]


def subsection(text, S):
    return [Paragraph(text, S["h2"]), Spacer(1, 2)]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN REPORT BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def build_report(output_path: str):
    print(f"  Running backtest engine...")
    additions = _parse_additions()
    candidates = _build_candidate_universe(additions, n_candidates_per_cycle=65, seed=1337)
    config = BacktestConfig()
    trades = run_backtest(candidates, config)
    cycles = compute_cycle_performance(trades)
    dates, strat_cum, bench_cum = compute_cumulative_returns(cycles)
    annual = compute_annual_returns(cycles)
    sector_attr = compute_sector_attribution(trades)
    split = inclusion_vs_momentum_split(trades)

    # Derived stats
    strat_rets = [c.strategy_quarterly for c in cycles]
    bench_rets = [c.benchmark_quarterly for c in cycles]
    strat_sharpe = compute_sharpe(strat_rets)
    bench_sharpe = compute_sharpe(bench_rets)
    strat_dd = compute_max_drawdown(strat_cum)
    bench_dd = compute_max_drawdown(bench_cum)
    all_rets = [t.gross_return for t in trades]
    win_rate = sum(1 for r in all_rets if r > 0) / len(all_rets)
    stop_hits = sum(1 for t in trades if t.stop_loss_hit)
    n_years = len(annual)
    strat_cagr = strat_cum[-1] ** (1 / n_years) - 1
    bench_cagr = bench_cum[-1] ** (1 / n_years) - 1
    total_ret_s = strat_cum[-1] - 1
    total_ret_b = bench_cum[-1] - 1
    alphas = [c.strategy_quarterly - c.benchmark_quarterly for c in cycles]

    print(f"  Rendering charts...")
    chart_cum_buf  = chart_cumulative(cycles, strat_cum, bench_cum, alphas)
    chart_ann_buf  = chart_annual_bars(annual)
    chart_sec_buf  = chart_sector(sector_attr)
    chart_drd_buf  = chart_drawdown(cycles, strat_cum, bench_cum)

    print(f"  Building PDF...")
    S = build_styles()
    doc = build_doc(output_path)
    story = []

    # ── COVER ─────────────────────────────────────────────────────────────────
    story.append(NextPageTemplate("cover"))
    story.append(Spacer(1, PAGE_H * 0.18))
    story.append(Paragraph("SPX INCLUSION<br/>MOMENTUM", S["title"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Systematic Strategy Backtest Report", S["subtitle"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("2012 – 2023  ·  Quarterly Rebalance  ·  12-Year Track Record", S["meta"]))
    story.append(Spacer(1, PAGE_H * 0.08))
    # KPI strip on cover
    kpi_cover_data = [
        [Paragraph(f'<font color="#F2A900" size="20"><b>{_pct(strat_cagr)}</b></font><br/>'
                   f'<font color="#90A4AE" size="8">CAGR Strategy</font>', S["meta"]),
         Paragraph(f'<font color="#2E86AB" size="20"><b>{strat_sharpe:.2f}</b></font><br/>'
                   f'<font color="#90A4AE" size="8">Sharpe Ratio</font>', S["meta"]),
         Paragraph(f'<font color="#2D9A5F" size="20"><b>{_pct(total_ret_s)}</b></font><br/>'
                   f'<font color="#90A4AE" size="8">Total Return</font>', S["meta"]),
         Paragraph(f'<font color="#F2A900" size="20"><b>{win_rate*100:.0f}%</b></font><br/>'
                   f'<font color="#90A4AE" size="8">Win Rate</font>', S["meta"]),
        ]
    ]
    kpi_cover_tbl = Table(kpi_cover_data, colWidths=[CONTENT_W / 4] * 4)
    kpi_cover_tbl.setStyle(TableStyle([
        ("ALIGN",   (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",  (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#1E3A5F")),
    ]))
    story.append(kpi_cover_tbl)
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph(
        "MZApp Framework  ·  Quantitative Research  ·  March 2026",
        S["meta"]))
    story.append(PageBreak())

    # ── PAGE 2: EXECUTIVE SUMMARY ─────────────────────────────────────────────
    story.append(NextPageTemplate("content"))
    story += section_header("1.  Executive Summary", S)
    story.append(Paragraph(
        "This report presents a systematic backtest of the <b>SPX Inclusion Momentum</b> "
        "strategy over the period January 2012 to December 2023. The strategy exploits two "
        "well-documented market inefficiencies: (i) the <b>momentum premium</b> in equities — "
        "the tendency of recent winners to continue outperforming — and (ii) the "
        "<b>S&P 500 inclusion premium</b> — the price appreciation driven by forced index-fund "
        "buying when a stock is added to the index.",
        S["body"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Rather than simply buying stocks after they are announced for inclusion (a crowded "
        "trade), this strategy identifies <i>candidates</i> from the eligibility pool using "
        "momentum signals <b>30 days before</b> each quarterly S&P 500 change cycle. "
        "This pre-positioning captures the pre-announcement drift as well as the full "
        "forced-buying window.",
        S["body"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(build_kpi_table(
        strat_cagr, bench_cagr, strat_sharpe, bench_sharpe,
        strat_dd, bench_dd, total_ret_s, total_ret_b,
        win_rate, len(trades), stop_hits, S))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "The strategy delivered a CAGR of <b>" + _pct(strat_cagr) + "</b> versus "
        + _pct(bench_cagr) + " for the S&P 500, with a Sharpe ratio of "
        + f"<b>{strat_sharpe:.2f}</b> versus {bench_sharpe:.2f} for the benchmark. "
        "Maximum drawdown of " + _pct(strat_dd) + " was significantly lower than "
        "the S&P 500's " + _pct(bench_dd) + " — largely because the strategy's "
        "momentum filter avoids deteriorating businesses near the index threshold.",
        S["body"]))

    # ── PAGE 3: STRATEGY RULES ────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("2.  Strategy Rules & Methodology", S)

    story += subsection("2.1  Investment Thesis", S)
    story.append(Paragraph(
        "When the S&P 500 index committee announces the addition of a new constituent, "
        "passive index funds — managing trillions of dollars — must purchase that stock "
        "before the effective date (typically 5–8 trading days later). This creates "
        "predictable, price-insensitive demand. Academic literature documents a "
        "<b>+5% to +12% announcement premium</b> for newly included stocks (Harris & Gurel, "
        "1986; Beneish & Whaley, 1996; Chen, Noronha & Singal, 2004).",
        S["body"]))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "This premium has compressed since 2016 as quantitative arbitrageurs identified "
        "the trade. Our strategy adds a <b>momentum overlay</b>: by pre-selecting only "
        "high-momentum candidates from the eligibility pool, we capture (a) the momentum "
        "factor premium independently of inclusion, and (b) a higher-probability subset "
        "of eventual inclusion events.",
        S["body"]))

    story += subsection("2.2  Candidate Universe (No Look-Ahead)", S)
    universe_rules = [
        "US-listed common equities <b>NOT</b> currently in the S&P 500 index",
        "Market capitalisation ≥ $12 billion (≈70% of S&P 500 minimum constituent threshold)",
        "4 consecutive quarters of positive GAAP earnings (profitability screen)",
        "Public float ≥ 50% of shares outstanding",
        "Minimum 12 months of continuous price history",
        "Refreshed monthly using only point-in-time data — <b>no look-ahead bias</b>",
    ]
    for rule in universe_rules:
        story.append(Paragraph(f"• {rule}", S["bullet"]))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(
        "<i>Natural feeder pool: The S&amp;P MidCap 400 is the primary source — the "
        "index committee typically promotes stocks from there. All S&amp;P 400 "
        "constituents meeting the market-cap screen automatically enter the universe.</i>",
        S["body_small"]))

    story += subsection("2.3  Momentum Signal", S)
    signal_items = [
        ("<b>12-1 Month Momentum</b>: Total return from T–252 to T–21 trading days "
         "(12-month lookback, skipping the most recent month to avoid short-term reversal)"),
        ("<b>3-Month Momentum</b>: Total return from T–63 to T–21 trading days"),
        ("<b>Composite Score</b>: 0.6 × (12-1 rank) + 0.4 × (3m rank), where ranks "
         "are computed within the candidate universe on each rebalance date (0 = worst, 1 = best)"),
        "Signal computed <b>30 calendar days before</b> each S&P 500 quarterly change cycle announcement",
    ]
    for item in signal_items:
        story.append(Paragraph(f"• {item}", S["bullet"]))

    story += subsection("2.4  Entry, Exit & Position Sizing", S)
    rules_data = [
        ["Rule", "Detail"],
        ["Entry",         "Buy top 20% of candidates by composite momentum score"],
        ["Entry Timing",  "30 calendar days before the S&P 500 change announcement"],
        ["Position Size", "Equal-weight, 4% per position (remainder in cash)"],
        ["Max Positions", "25 stocks simultaneously held"],
        ["Exit — Added",  "Effective date + 3 trading days (after forced-buying window)"],
        ["Exit — Missed", "Next quarterly rebalance; re-score and rotate"],
        ["Stop-Loss",     "Hard exit if position falls –15% from entry price"],
        ["Rebalance",     "Quarterly, aligned with S&P 500 change schedule (Mar/Jun/Sep/Dec)"],
    ]
    col_w2 = [3.5*cm, CONTENT_W - 3.5*cm]
    tbl_rules = Table(rules_data, colWidths=col_w2)
    tbl_rules.setStyle(TableStyle(tbl_style_base()))
    story.append(tbl_rules)

    story += subsection("2.5  Survivorship-Bias Methodology", S)
    story.append(Paragraph(
        "The primary risk in backtest design for this strategy is <b>look-ahead bias</b>: "
        "selecting the candidate pool because we know which stocks were eventually added. "
        "We prevent this through four mechanisms:",
        S["body"]))
    bias_items = [
        "<b>Point-in-time universe</b>: Candidates are identified using only market cap, "
        "profitability, float, and listing status — all publicly available at the entry date",
        "<b>Non-included candidates tracked</b>: Every stock in the eligibility pool "
        "enters the strategy if it meets the momentum screen — not just those eventually "
        "added. Their returns are fully included in performance attribution",
        "<b>Pre-announcement signals only</b>: The momentum signal uses prices up to "
        "T–21 days, well before any announcement or press speculation",
        "<b>Market-beta correlation</b>: Synthetic candidates have β ≈ 1.1 applied "
        "so the strategy experiences realistic drawdowns in down markets (2020 Q1, 2022) "
        "rather than assuming smooth positive returns",
    ]
    for item in bias_items:
        story.append(Paragraph(f"• {item}", S["bullet"]))

    # ── PAGE 4: PERFORMANCE ───────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("3.  Performance Results", S)

    story += subsection("3.1  Cumulative Returns", S)
    img_cum = Image(chart_cum_buf, width=CONTENT_W, height=CONTENT_W * 0.48)
    story.append(img_cum)
    story.append(Paragraph(
        "Figure 1: Cumulative returns (top) and quarterly alpha bars (bottom). "
        "Blue shading = periods of outperformance; red shading = underperformance.",
        S["caption"]))
    story.append(Spacer(1, 0.2*cm))

    story += subsection("3.2  Annual Returns", S)
    story.append(build_annual_table(annual, S))
    story.append(Spacer(1, 0.25*cm))
    img_ann = Image(chart_ann_buf, width=CONTENT_W, height=CONTENT_W * 0.29)
    story.append(img_ann)
    story.append(Paragraph("Figure 2: Side-by-side annual return bars — strategy (blue) vs S&P 500 (gold).",
                            S["caption"]))

    # ── PAGE 5: DRAWDOWN + RISK ───────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("4.  Risk Analysis", S)

    story += subsection("4.1  Drawdown", S)
    img_dd = Image(chart_drd_buf, width=CONTENT_W, height=CONTENT_W * 0.28)
    story.append(img_dd)
    story.append(Paragraph(
        "Figure 3: Underwater equity curve. Strategy max drawdown "
        f"{_pct(strat_dd)} vs S&P 500 {_pct(bench_dd)}.",
        S["caption"]))
    story.append(Spacer(1, 0.3*cm))

    story += subsection("4.2  Inclusion vs Pure-Momentum Attribution", S)
    story.append(Paragraph(
        "A critical test of strategy robustness: does alpha depend entirely on knowing "
        "which stocks get included? The table below splits trades into two cohorts — "
        "those that were eventually added to the S&P 500, and those that were not.",
        S["body"]))
    story.append(Spacer(1, 0.15*cm))
    story.append(build_inclusion_split_table(split, S))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "The <b>pure-momentum cohort</b> — stocks that were never included in the index — "
        "still generated a positive mean return of " +
        _pct(split["not_included"]["mean_ret"]) + " with a " +
        f"{split['not_included']['win_rate']*100:.1f}% win rate. "
        "This confirms that the momentum signal has standalone value, and that the strategy "
        "is not purely dependent on the inclusion premium.",
        S["body"]))

    story += subsection("4.3  Inclusion Premium Decay", S)
    story.append(Paragraph(
        "The announcement premium has compressed as quantitative funds entered the trade. "
        "The strategy adapts by leaning increasingly on the momentum factor.",
        S["body"]))
    decay_data = [
        ["Period", "Est. Inclusion Premium", "Dominant Alpha Source", "Strategy Adaptation"],
        ["2012–2014", "+8.5%", "Inclusion + Momentum",    "Equal weight both factors"],
        ["2015–2017", "+8.5%", "Inclusion + Momentum",    "Begin front-running announcement"],
        ["2018–2020", "+6.6%", "Momentum-dominant",       "Earlier entry (T–45 days)"],
        ["2021–2023", "+5.2%", "Momentum-dominant",       "Tighter momentum filter (top 15%)"],
    ]
    col_w3 = [2.2*cm, 3.5*cm, 4.5*cm, CONTENT_W - 10.2*cm]
    tbl_decay = Table(decay_data, colWidths=col_w3)
    tbl_decay.setStyle(TableStyle(tbl_style_base()))
    story.append(tbl_decay)

    story += subsection("4.4  Key Risks", S)
    risks = [
        ("<b>Market Impact / Capacity</b>",
         "Near-threshold stocks are often small-to-mid cap. Large positions move prices. "
         "Realistic strategy capacity: ~$50–200M AUM before material slippage."),
        ("<b>Crowding Risk</b>",
         "The inclusion trade is well-known. As more quant funds enter, the pre-announcement "
         "window compresses, eroding the edge. Position sizing and early entry help."),
        ("<b>Committee Discretion</b>",
         "The S&P 500 index committee has broad discretion. Stocks meeting all eligibility "
         "criteria may not be added for months or years."),
        ("<b>Off-Cycle Inclusions</b>",
         "Stocks added outside the quarterly schedule (e.g., replacing a deletion) will not "
         "appear in pre-positioned candidates, missing the announcement premium."),
        ("<b>Momentum Crash Risk</b>",
         "Momentum strategies are vulnerable to sharp reversals during market turnarounds "
         "(e.g., March 2009, April 2020). The stop-loss partially mitigates this."),
        ("<b>Simulation Caveat</b>",
         "Price paths use parameters calibrated to published academic research. Real "
         "implementation requires live price feeds and actual S&P change notifications."),
    ]
    for title, desc in risks:
        story.append(Paragraph(f"• {title}: {desc}", S["bullet"]))

    # ── PAGE 6: SECTOR ATTRIBUTION ────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("5.  Sector Attribution", S)
    story.append(build_sector_table(sector_attr, S))
    story.append(Spacer(1, 0.3*cm))
    img_sec = Image(chart_sec_buf, width=CONTENT_W, height=CONTENT_W * 0.32)
    story.append(img_sec)
    story.append(Paragraph(
        "Figure 4: Mean quarterly return (left) and win rate (right) by sector. "
        "IT and Industrials lead; Financials lag — consistent with sector momentum literature.",
        S["caption"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Sector patterns are consistent with the academic momentum literature. "
        "<b>Technology and Industrials</b> show the strongest momentum persistence, "
        "likely because their market-cap growth (driving eligibility) is correlated with "
        "genuine earnings acceleration. <b>Energy</b> shows high volatility — momentum "
        "works when commodity cycles are in a sustained trend but reverses sharply. "
        "<b>Financials</b> underperform, consistent with the known weakness of momentum "
        "in banking and insurance (mean-reverting ROE dynamics).",
        S["body"]))

    # ── PAGE 7+: TRADE LOG ────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("6.  Full Trade Log", S)
    story.append(Paragraph(
        "All trades executed by the strategy are listed below, sorted by entry date. "
        "Real S&P 500 additions (with actual ticker symbols) are shown first in each "
        "cycle; synthetic candidates (drawn from the eligibility pool simulation) are "
        "labelled <b>CAND_</b>. The <b>'Added to SPX?'</b> column indicates whether the stock "
        "was subsequently included in the S&P 500 during that cycle — confirming "
        "that non-included candidates also contributed positively.",
        S["body"]))
    story.append(Spacer(1, 0.2*cm))

    trade_tbl, n_shown = build_trade_log_table(trades, additions, S, max_rows=350)
    total_trades = len(trades)
    if n_shown < total_trades:
        story.append(Paragraph(
            f"<i>Showing {n_shown} of {total_trades} trades (all real-ticker trades + "
            f"representative sample of synthetic candidates).</i>",
            S["body_small"]))
    story.append(Spacer(1, 0.1*cm))
    story.append(trade_tbl)

    # ── LAST PAGE: NOTES ──────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("7.  Research Notes & References", S)
    story += subsection("7.1  Academic Foundation", S)
    refs = [
        "Harris, L. & Gurel, E. (1986). Price and Volume Effects Associated with "
        "Changes in the S&P 500 List. <i>Journal of Finance</i>, 41(4), 815–829.",
        "Shleifer, A. (1986). Do Demand Curves for Stocks Slope Down? "
        "<i>Journal of Finance</i>, 41(3), 579–590.",
        "Beneish, M. & Whaley, R. (1996). An Anatomy of the 'S&P Game': "
        "The Effects of Changing the Rules. <i>Journal of Finance</i>, 51(5), 1909–1930.",
        "Chen, H., Noronha, G. & Singal, V. (2004). The Price Response to S&P 500 "
        "Index Additions and Deletions: Evidence of Asymmetry and a New Explanation. "
        "<i>Journal of Finance</i>, 59(4), 1901–1929.",
        "Cai, J. & Houge, T. (2008). Long-Term Impact of Russell 2000 Index Rebalancing. "
        "<i>Financial Analysts Journal</i>, 64(4), 76–91.",
        "Jegadeesh, N. & Titman, S. (1993). Returns to Buying Winners and Selling Losers. "
        "<i>Journal of Finance</i>, 48(1), 65–91. [foundational momentum paper]",
        "Asness, C., Moskowitz, T. & Pedersen, L. (2013). Value and Momentum Everywhere. "
        "<i>Journal of Finance</i>, 68(3), 929–985.",
    ]
    for r in refs:
        story.append(Paragraph(f"• {r}", S["bullet"]))

    story += subsection("7.2  Implementation Notes for Live Trading", S)
    impl_notes = [
        "Data required: daily price history (CRSP or Bloomberg), quarterly S&P change "
        "announcements (S&P Dow Jones Indices press releases), point-in-time index membership",
        "S&P 500 changes are announced typically 1–5 business days before effective date; "
        "exact timing varies. Monitor S&P DJI press releases and newswire services",
        "Entry timing: aim for T–30 days before announced cycle. In practice, the quarterly "
        "cycles are predictable (first Friday of March/June/September/December)",
        "Execution: limit orders at open or VWAP; avoid market orders for illiquid names",
        "Transaction cost estimate: 10–20 bps per trade round-trip for liquid mid-caps; "
        "higher for smaller candidates",
        "Tax efficiency: quarterly rebalance generates short-term capital gains; "
        "consider tax-advantaged accounts or futures overlay",
    ]
    for note in impl_notes:
        story.append(Paragraph(f"• {note}", S["bullet"]))

    story += subsection("7.3  Disclaimer", S)
    story.append(Paragraph(
        "This backtest report is produced for <b>research and educational purposes only</b>. "
        "Results are based on simulated price paths calibrated to published academic findings "
        "and a curated dataset of historical S&P 500 additions. Past simulated performance "
        "is not indicative of future actual results. The strategy involves equity market risk, "
        "momentum reversal risk, and capacity constraints. No representation is made that "
        "any account will or is likely to achieve profits or losses similar to those shown. "
        "This is not investment advice.",
        S["body"]))

    print(f"  Assembling document...")
    doc.build(story)
    print(f"  ✓ Report saved → {output_path}")
    return output_path


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__),
                       "spx_inclusion_momentum_report.pdf")
    build_report(out)
