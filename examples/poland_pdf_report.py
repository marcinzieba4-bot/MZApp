"""
Generate a polished PDF report: Poland Asymmetric Ideas — March 2026.
Output: poland_asymmetric_ideas.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import BalancedColumns
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
import os

# ─── COLOUR PALETTE ───────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0A1628")
GOLD    = colors.HexColor("#C9A84C")
STEEL   = colors.HexColor("#1E3A5F")
SILVER  = colors.HexColor("#8FA3B1")
LIGHT   = colors.HexColor("#F2F5F8")
WHITE   = colors.white
GREEN   = colors.HexColor("#2E7D32")
RED     = colors.HexColor("#C62828")
AMBER   = colors.HexColor("#E65100")
BGROW   = colors.HexColor("#EEF3F7")

PAGE_W, PAGE_H = A4
MARGIN_L, MARGIN_R = 1.8*cm, 1.8*cm
MARGIN_T, MARGIN_B = 2.0*cm, 2.0*cm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# ─── DATA ─────────────────────────────────────────────────────────────────────
IDEAS = [
    {
        "rank": 1, "name": "Lubawa SA", "peers": [("Chemring UK","EV/EBITDA","12×"),("Leonardo IT","EV/EBITDA","16×"),("Rheinmetall DE","EV/EBITDA","30×"),("Thales FR","EV/EBITDA","22×")], "peer_label": "vs LBW 3.8×",
        "ticker": "LBW",
        "sector": "Defense / Protective Equipment",
        "type_short": "Micro-Cap Neglect + Defense",
        "mktcap_eur": 133, "mktcap_pln": 658,
        "entry": 8.12, "currency": "PLN",
        "pe": 5.86, "pb": 1.27, "roe": 29.5, "ebitda_m": 24.3,
        "rev": 510, "rev_g": 52, "insider": 51.2, "inst": 0, "analysts": 0,
        "bear": 5.00, "bear_p": 0.15,
        "base": 18.00, "base_p": 0.55,
        "bull": 38.00, "bull_p": 0.30,
        "horizon": "12–24 months", "conviction": "HIGH",
        "catalyst": "First institutional buyer crosses 5% (ESPI disclosure); first English broker note; MSCI DM reclassification passive flows",
        "key_risk": "Founder 51% control / no IR pressure; defense budget shifts to hardware (tanks) vs. soldier equipment; thin free float",
        "summary": (
            "Poland's #1 ballistic-protection maker. ROE 29%, margins 24%, revenue +52% YoY, net cash. "
            "European defense peers trade at 15–30× EV/EBITDA. Lubawa trades at 3.8×. "
            "The gap is 100% mechanical: zero institutional ownership (size exclusion at €133m) "
            "and zero English IR. One investor crossing 5% triggers the discovery cascade. "
            "Entry is below the hard asset floor (net cash + backlog)."
        ),
        "asymmetry_note": "You buy at a discount to floor. Bull/Bear ratio: 9.6×.",
    },
    {
        "rank": 2, "name": "Agora SA", "peers": [("JCDecaux FR","EV/EBITDA","10×"),("Ströer DE","EV/EBITDA","11×"),("Clear Channel US","EV/EBITDA","8×"),("Kinetic AU","EV/EBITDA","9×")], "peer_label": "vs AMS implied 3.3×",
        "ticker": "AGO",
        "sector": "Diversified Media / OOH Advertising",
        "type_short": "SOTP Conglomerate Discount",
        "mktcap_eur": 74, "mktcap_pln": 367,
        "entry": 8.94, "currency": "PLN",
        "pe": None, "pb": 1.19, "roe": 4.5, "ebitda_m": 6.5,
        "rev": 1480, "rev_g": 7, "insider": 22.0, "inst": 30, "analysts": 4,
        "bear": 5.50, "bear_p": 0.20,
        "base": 22.00, "base_p": 0.55,
        "bull": 45.00, "bull_p": 0.25,
        "horizon": "24–36 months", "conviction": "HIGH",
        "catalyst": "AMS partial sale announcement (JCDecaux / Clear Channel approach); group EBITDA > PLN 150m print; PE buyout approach",
        "key_risk": "Founding family has no financial pressure to unlock value; GW print accelerates decline; IFRS 16 inflates AMS EBITDA; EBITDA target missed",
        "summary": (
            "Poland's #1 outdoor advertiser (AMS) is worth PLN 999m at 9× EV/EBITDA — "
            "yet the entire Agora group trades at PLN 367m. "
            "AMS alone covers market cap 2.7×. Helios (54 cinemas), Radio Eurozet, "
            "Gazeta Wyborcza digital (300k+ paid subs) are free. "
            "The newspaper 'poisons' the perception. One strategic sale or spin-off "
            "of AMS collapses the 3.7× SOTP-to-market-cap gap instantly."
        ),
        "asymmetry_note": "SOTP base NAV PLN 1,350m vs market cap PLN 367m = 3.68× coverage.",
    },
    {
        "rank": 3, "name": "mBank SA", "peers": [("PKO BP PL","P/E","10×"),("Pekao PL","P/E","11×"),("Santander PL","P/E","13×"),("ING BSK PL","P/E","12×")], "peer_label": "vs MBK 12.4×",
        "ticker": "MBK",
        "sector": "Digital Banking",
        "type_short": "Parent Disposition + CHF Resolution",
        "mktcap_eur": 8700, "mktcap_pln": 43079,
        "entry": 1013.0, "currency": "PLN",
        "pe": 12.4, "pb": 1.22, "roe": 16.4, "ebitda_m": None,
        "rev": None, "rev_g": 5, "insider": 1.0, "inst": 20, "analysts": 12,
        "bear": 700.0, "bear_p": 0.20,
        "base": 1350.0, "base_p": 0.55,
        "bull": 1750.0, "bull_p": 0.25,
        "horizon": "12–24 months", "conviction": "HIGH",
        "catalyst": "CHF provisions < PLN 100m/qtr for 2 consecutive quarters; UniCredit AGM May 2026 re Commerzbank; German govt stake sale in CBK",
        "key_risk": "New Supreme Court ruling expanding CHF liability; UniCredit-Commerzbank deal collapse; Polish rate cuts compressing NIM; UniCredit retains mBank",
        "summary": (
            "Poland's best digital bank: ROE 16.4%, cost-to-income <30%, fully digital-native. "
            "Should trade at a premium — trades at a discount solely due to CHF mortgage overhang. "
            "CHF costs fell >50% YoY in 2025. Thesis 1: CHF resolves → P/E expands from 12.4× to 14–16×. "
            "Thesis 2: UniCredit acquires Commerzbank (69% MBK owner) → forced mBank sale at 1.4–1.5× P/BV. "
            "Two independent theses; each alone justifies entry."
        ),
        "asymmetry_note": "Two independent theses; only lose if BOTH CHF escalates AND M&A collapses.",
    },
    {
        "rank": 4, "name": "Mirbud SA", "peers": [("Budimex PL","EV/EBITDA","12×"),("Strabag AT","EV/EBITDA","8×"),("Balfour Beatty UK","EV/EBITDA","9×"),("Ferrovial ES","EV/EBITDA","14×")], "peer_label": "vs MRB road ~5×",
        "ticker": "MRB",
        "sector": "Construction / Infrastructure",
        "type_short": "Hidden Asset + Rail Pivot",
        "mktcap_eur": 77, "mktcap_pln": 380,
        "entry": 3.80, "currency": "PLN",
        "pe": None, "pb": 0.61, "roe": 7.5, "ebitda_m": 5.5,
        "rev": 2100, "rev_g": 8, "insider": 62.0, "inst": 8, "analysts": 2,
        "bear": 2.80, "bear_p": 0.15,
        "base": 7.20, "base_p": 0.50,
        "bull": 10.50, "bull_p": 0.35,
        "horizon": "18–36 months", "conviction": "MEDIUM+",
        "catalyst": "PKP PLK tender award via ESPI; land bank disposal or JV announcement; rail revenue > 10% of total",
        "key_risk": "Rail tendering delayed (CEF administrative process); road margin compression; labour cost inflation; no activist pressure with 62% founder stake",
        "summary": (
            "Road contractor priced as a commodity at 0.61× book. Two embedded options: "
            "(1) Land bank at historical cost — independent property value = 1.5–2× book, "
            "provides a hard floor above current price. "
            "(2) Rail pivot — pre-qualified for PKP PLK tenders worth PLN 135bn. "
            "Rail margins (12–15% EBITDA) are 2–3× road margins. "
            "Market assigns zero probability to the pivot. "
            "Even a 6% win rate in tenders creates PLN 936m of incremental value vs PLN 380m market cap."
        ),
        "asymmetry_note": "Land bank alone worth ~PLN 230m. Rail option is genuinely free.",
    },
    {
        "rank": 5, "name": "Onde SA", "peers": [("Elecnor ES","EV/EBITDA","8×"),("Prysmian IT","EV/EBITDA","11×"),("Nexans FR","EV/EBITDA","9×"),("Renew Holdings UK","EV/EBITDA","10×")], "peer_label": "vs ONDP ~7×",
        "ticker": "ONDP",
        "sector": "Renewable Energy EPC / Grid",
        "type_short": "Pipeline Certainty + Energy Mandate",
        "mktcap_eur": 111, "mktcap_pln": 550,
        "entry": 10.10, "currency": "PLN",
        "pe": None, "pb": 1.29, "roe": 5.5, "ebitda_m": 7.0,
        "rev": 804, "rev_g": 12, "insider": 52.0, "inst": 9, "analysts": 3,
        "bear": 6.50, "bear_p": 0.20,
        "base": 18.00, "base_p": 0.55,
        "bull": 32.00, "bull_p": 0.25,
        "horizon": "18–30 months", "conviction": "MEDIUM+",
        "catalyst": "New PSE grid framework contract award; offshore wind pre-qualification; Polish RES Act 2032 extension; order book > PLN 3bn",
        "key_risk": "PSE grid connection bottlenecks; PGE in-house construction competition; EU fund disbursement delays; project finance rate sensitivity",
        "summary": (
            "Specialist EPC contractor for Polish renewables and grid infrastructure. "
            "Poland has a legally binding mandate: 42.5% renewables by 2030 vs 25% today. "
            "PSE capex: PLN 30bn through 2032. Onde is one of 4–5 pre-qualified contractors. "
            "The pipeline is not speculative — it is signed and funded. "
            "Market prices Onde as a generic contractor (1.3× book). "
            "European renewable EPC peers trade at 2.0–3.5× book. "
            "The gap is purely discovery and language barrier."
        ),
        "asymmetry_note": "Regulatory mandate is the floor. Miss on execution = only downside.",
    },
    {
        "rank": 6, "name": "Polimex-Mostostal SA", "peers": [("Skanska SE","EV/EBITDA","11×"),("Vinci FR","EV/EBITDA","12×"),("BWXT US","EV/EBITDA","18×"),("Babcock UK","EV/EBITDA","8×")], "peer_label": "vs PXM loss-making",
        "ticker": "PXM",
        "sector": "Industrial Construction / Nuclear",
        "type_short": "Binary Nuclear Option",
        "mktcap_eur": 152, "mktcap_pln": 754,
        "entry": 3.28, "currency": "PLN",
        "pe": None, "pb": 1.73, "roe": -55.0, "ebitda_m": -3.0,
        "rev": 2860, "rev_g": -5, "insider": 8.0, "inst": 22, "analysts": 5,
        "bear": 1.20, "bear_p": 0.30,
        "base": 9.00, "base_p": 0.45,
        "bull": 16.00, "bull_p": 0.25,
        "horizon": "24–48 months", "conviction": "OPTION",
        "catalyst": "Polish govt FID on Lubiatowo-Kopalino nuclear plant; EPC contract signature with Westinghouse; EBITDA return to positive (operational turnaround)",
        "key_risk": "Nuclear further delayed or cancelled; operating losses deteriorate balance sheet; international contractors displace Polimex in consortium; loss of pre-qualification",
        "summary": (
            "Poland's largest industrial contractor — currently loss-making, hence the price. "
            "Hidden within: pre-qualification for Poland's first nuclear power plant "
            "(Lubiatowo-Kopalino, 2× AP1000, USD 20–40bn total). "
            "Civil works alone: USD 4–8bn. Polimex realistic share: 25–40% = USD 1–3.2bn over 8 years, "
            "against a current revenue base of PLN 2.86bn/year. "
            "Market cap = PLN 754m. The nuclear option is priced at essentially zero. "
            "Size it as a call option (1–2% of portfolio), not a core holding."
        ),
        "asymmetry_note": "Single biggest infrastructure project in Polish history. Option = free.",
    },
]

CONTEXT_POINTS = [
    ("MSCI Reclassification Q2 2026",
     "Poland moves from Emerging to Developed Markets. Passive DM funds are forced buyers of "
     "ALL Polish listed names. Institutional infrastructure (active desks, research) follows passive flows."),
    ("NATO Defense Super-Cycle",
     "Poland commits 5% of GDP to defense — highest in NATO. $301.6bn over 2026-2030, +118% vs prior "
     "five years. Defense sub-contractors still priced as industrial commodities vs Rheinmetall (30×), Thales (22×)."),
    ("CHF Mortgage Resolution",
     "Polish banks provisioned PLN 150bn+ since 2019. Provision costs fell >50% YoY in 2025 for leading "
     "banks. Sector-wide discount is now larger than the remaining tail risk."),
    ("Energy Transition Mandate",
     "EU law: 42.5% renewables by 2030 (Poland at ~25% today). PSE grid capex PLN 30bn, 5.9 GW offshore "
     "wind. The infrastructure pipeline is signed and funded — not speculative."),
    ("Language / Information Barrier",
     "Median WSE mid-cap analyst coverage: 2 (vs 8+ for German peers). All filings in Polish only. "
     "Information asymmetry directly translates to price asymmetry. Reading Polish is the edge."),
]

PORTFOLIO_ROWS = [
    ("1", "mBank (MBK)",      "25–30%", "Liquid (€8.7bn), dual thesis, near-term catalyst"),
    ("2", "Lubawa (LBW)",     "20–25%", "Highest conviction; build slowly over 3–6 months (illiquid)"),
    ("3", "Agora (AGO)",      "15–20%", "Clear SOTP floor; patience required for catalyst"),
    ("4", "Onde (ONDP)",      "10–15%", "Thematic; pipeline certainty supports allocation"),
    ("5", "Mirbud (MRB)",      "8–12%", "Deep value + rail option"),
    ("6", "Polimex (PXM)",     " 5–8%", "Binary option sizing — treat like a call, not a bond"),
]


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def pw_ret(idea):
    b = (idea["base"] / idea["entry"] - 1) * 100
    be = (idea["bear"] / idea["entry"] - 1) * 100
    bu = (idea["bull"] / idea["entry"] - 1) * 100
    return be * idea["bear_p"] + b * idea["base_p"] + bu * idea["bull_p"]

def asym(idea):
    up = (idea["bull"] / idea["entry"] - 1)
    dn = abs(idea["bear"] / idea["entry"] - 1)
    return up / dn if dn else 99.0

def ret_pct(a, b):
    return (b / a - 1) * 100


# ─── PAGE TEMPLATE ────────────────────────────────────────────────────────────

class ReportCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._page_number = 0

    def showPage(self):
        self._page_number += 1
        self._draw_footer()
        super().showPage()

    def save(self):
        # showPage() already drew the footer on the last real page — just finalize
        super().save()

    def _draw_footer(self):
        self.saveState()
        # Bottom bar
        self.setFillColor(NAVY)
        self.rect(0, 0, PAGE_W, 1.0*cm, fill=1, stroke=0)
        # Page number
        self.setFillColor(SILVER)
        self.setFont("Helvetica", 7)
        self.drawRightString(PAGE_W - MARGIN_R, 0.35*cm,
                             f"CONFIDENTIAL — FOR PROFESSIONAL INVESTORS ONLY  |  Page {self._page_number}")
        # Left footer text
        self.setFillColor(GOLD)
        self.drawString(MARGIN_L, 0.35*cm, "Poland Asymmetric Ideas — March 2026")
        self.restoreState()


# ─── STYLES ───────────────────────────────────────────────────────────────────

def make_styles():
    base = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "h1": S("h1", fontName="Helvetica-Bold", fontSize=22, textColor=WHITE,
                 leading=26, spaceAfter=6, alignment=TA_LEFT),
        "h1sub": S("h1sub", fontName="Helvetica", fontSize=11, textColor=GOLD,
                   leading=14, spaceAfter=4, alignment=TA_LEFT),
        "h2": S("h2", fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,
                leading=16, spaceBefore=14, spaceAfter=4),
        "h3": S("h3", fontName="Helvetica-Bold", fontSize=10, textColor=STEEL,
                leading=13, spaceBefore=8, spaceAfter=3),
        "body": S("body", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#222222"),
                  leading=13, spaceAfter=4, alignment=TA_JUSTIFY),
        "body_sm": S("body_sm", fontName="Helvetica", fontSize=7.5,
                     textColor=colors.HexColor("#333333"), leading=11, spaceAfter=3),
        "label": S("label", fontName="Helvetica-Bold", fontSize=7.5, textColor=STEEL, leading=10),
        "tag_gold": S("tag", fontName="Helvetica-Bold", fontSize=7, textColor=GOLD, leading=10),
        "tag_green": S("tag_g", fontName="Helvetica-Bold", fontSize=7, textColor=GREEN, leading=10),
        "tag_red": S("tag_r", fontName="Helvetica-Bold", fontSize=7, textColor=RED, leading=10),
        "num": S("num", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY,
                 leading=12, alignment=TA_RIGHT),
        "footer_note": S("fn", fontName="Helvetica-Oblique", fontSize=6.5,
                         textColor=SILVER, leading=9, spaceAfter=0),
        "bullet": S("bullet", fontName="Helvetica", fontSize=8.5,
                    textColor=colors.HexColor("#222222"), leading=13,
                    leftIndent=10, spaceAfter=3,
                    bulletIndent=0, bulletFontName="Helvetica",
                    bulletFontSize=9, alignment=TA_JUSTIFY),
        "conviction_high": S("cv_h", fontName="Helvetica-Bold", fontSize=7,
                              textColor=WHITE, leading=9),
        "conviction_med": S("cv_m", fontName="Helvetica-Bold", fontSize=7,
                             textColor=WHITE, leading=9),
        "table_hdr": S("th", fontName="Helvetica-Bold", fontSize=7.5,
                       textColor=WHITE, leading=10, alignment=TA_CENTER),
        "table_cell": S("tc", fontName="Helvetica", fontSize=7.5,
                        textColor=NAVY, leading=10, alignment=TA_CENTER),
        "table_cell_l": S("tcl", fontName="Helvetica", fontSize=7.5,
                          textColor=NAVY, leading=10, alignment=TA_LEFT),
        "table_cell_b": S("tcb", fontName="Helvetica-Bold", fontSize=7.5,
                          textColor=NAVY, leading=10, alignment=TA_CENTER),
        "idea_title": S("it", fontName="Helvetica-Bold", fontSize=14,
                        textColor=WHITE, leading=17),
        "idea_sub": S("is", fontName="Helvetica", fontSize=8.5,
                      textColor=GOLD, leading=12),
    }


# ─── FLOWABLE HELPERS ─────────────────────────────────────────────────────────

def hline(color=NAVY, thickness=0.8, space_before=4, space_after=4):
    return [
        Spacer(1, space_before),
        HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=space_after),
    ]


def gold_bar(text, styles):
    data = [[Paragraph(text, ParagraphStyle("gb", fontName="Helvetica-Bold",
                                            fontSize=10, textColor=WHITE, leading=13))]]
    t = Table(data, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 2, GOLD),
    ]))
    return t


def section_header(text, styles):
    data = [[Paragraph(text, styles["h2"])]]
    t = Table(data, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 1.5, GOLD),
        ("TOPPADDING",   (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
    ]))
    return t


def conviction_badge(label):
    color = GREEN if label == "HIGH" else (AMBER if label == "MEDIUM+" else STEEL)
    data = [[Paragraph(f"  {label}  ", ParagraphStyle(
        "badge", fontName="Helvetica-Bold", fontSize=7, textColor=WHITE, leading=9))]]
    t = Table(data)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("ROUNDEDCORNERS", [3]),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
    ]))
    return t


# ─── COVER PAGE ───────────────────────────────────────────────────────────────

def build_cover(styles):
    story = []

    # Top navy banner
    banner_data = [[
        Paragraph("POLAND", ParagraphStyle("cov1", fontName="Helvetica-Bold",
                                           fontSize=40, textColor=WHITE, leading=44)),
    ]]
    banner = Table(banner_data, colWidths=[CONTENT_W])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBELOW", (0, 0), (-1, -1), 4, GOLD),
        ("LEFTPADDING",  (0, 0), (-1, -1), 14),
        ("TOPPADDING",   (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
    ]))
    story.append(banner)

    sub_data = [[
        Paragraph(
            "ASYMMETRIC IDEAS REPORT<br/>"
            "<font size=12 color='#C9A84C'>Warsaw Stock Exchange (WSE) — March 2026</font>",
            ParagraphStyle("cov2", fontName="Helvetica-Bold", fontSize=18,
                           textColor=WHITE, leading=24)),
    ]]
    sub = Table(sub_data, colWidths=[CONTENT_W])
    sub.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING",  (0, 0), (-1, -1), 14),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 20),
    ]))
    story.append(sub)
    story.append(Spacer(1, 0.6*cm))

    # Summary blurb
    intro = (
        "Six high-conviction asymmetric opportunities across six independent sectors, "
        "each with a distinct mispricing <i>mechanism</i>, a distinct <i>catalyst</i>, and a hard "
        "downside floor. Together they form a diversified Polish alpha portfolio exploiting "
        "five structural forces: MSCI reclassification, NATO rearmament, CHF resolution, "
        "energy transition mandate, and persistent language/information barriers."
    )
    story.append(Paragraph(intro, ParagraphStyle("intro", fontName="Helvetica", fontSize=10,
                                                  textColor=NAVY, leading=15, alignment=TA_JUSTIFY)))
    story.append(Spacer(1, 0.5*cm))

    # Quick-view table on cover
    hdr = ["#", "Company", "Ticker", "Sector", "Mkt Cap €m",
           "Entry", "Bear", "Base", "Bull", "PW Ret%", "Asym"]
    rows = [hdr]
    for idea in IDEAS:
        pwr = pw_ret(idea)
        a   = asym(idea)
        rows.append([
            str(idea["rank"]),
            idea["name"],
            idea["ticker"],
            idea["sector"][:24],
            f"€{idea['mktcap_eur']:,}m",
            f"{idea['entry']:.2f}",
            f"{idea['bear']:.2f}",
            f"{idea['base']:.2f}",
            f"{idea['bull']:.2f}",
            f"{pwr:+.1f}%",
            f"{a:.1f}×",
        ])

    col_ws = [0.6*cm, 2.7*cm, 1.1*cm, 3.5*cm, 1.6*cm,
              1.45*cm, 1.45*cm, 1.45*cm, 1.45*cm, 1.4*cm, 1.0*cm]

    def p(txt, bold=False, align=TA_CENTER, color=NAVY, size=7.5):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        return Paragraph(txt, ParagraphStyle("tc", fontName=fn, fontSize=size,
                                             textColor=color, leading=10, alignment=align))

    formatted = []
    for i, row in enumerate(rows):
        if i == 0:
            formatted.append([p(c, bold=True, color=WHITE) for c in row])
        else:
            idea  = IDEAS[i - 1]
            pwr   = pw_ret(idea)
            a_val = asym(idea)
            pwr_c = GREEN if pwr > 0 else RED
            formatted.append([
                p(row[0], bold=True),
                p(row[1], align=TA_LEFT, bold=True),
                p(row[2]),
                p(row[3], align=TA_LEFT),
                p(row[4]),
                p(row[5]),
                p(row[6], color=RED),
                p(row[7], bold=True),
                p(row[8], color=GREEN),
                p(row[9], bold=True, color=pwr_c),
                p(row[10], bold=True, color=GOLD),
            ])

    tbl = Table(formatted, colWidths=col_ws, repeatRows=1)
    ts = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, BGROW]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("LINEBELOW", (0, 0), (-1, 0), 2, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])
    tbl.setStyle(ts)
    story.append(tbl)

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "PW Ret% = probability-weighted return. Asym = bull upside ÷ bear downside. "
        "All prices in PLN. This report is for professional investors only.",
        ParagraphStyle("fn", fontName="Helvetica-Oblique", fontSize=6.5,
                       textColor=SILVER, leading=9)))

    story.append(Spacer(1, 0.4*cm))

    # Key thesis box — fills blank space at bottom of cover
    thesis_items = [
        ("<b>Why now?</b>  MSCI reclassification (Q2 2026) brings mandatory passive inflows to every WSE name. "
         "Institutional desks follow passive flows — the discovery cycle begins this year."),
        ("<b>Why these six?</b>  Each has a <i>named</i> mispricing mechanism, a <i>named</i> catalyst, and a hard "
         "downside floor. They are not simply cheap — they are structurally mispriced with a known fix."),
        ("<b>Why Poland specifically?</b>  Median analyst coverage: 2 per stock. All filings in Polish only. "
         "60%+ founder-controlled. Information asymmetry directly equals price asymmetry."),
        ("<b>Edge:</b>  You read Polish. 90% of the institutional world does not."),
    ]
    thesis_cells = [[Paragraph("KEY THESIS PREMISES", ParagraphStyle(
        "tph", fontName="Helvetica-Bold", fontSize=8, textColor=GOLD, leading=11))]]
    for item in thesis_items:
        thesis_cells.append([Paragraph(f"▸  {item}", ParagraphStyle(
            "tpb", fontName="Helvetica", fontSize=8.5, textColor=WHITE,
            leading=13, leftIndent=6, spaceAfter=3, alignment=TA_JUSTIFY))])

    thesis_t = Table([[c] for c in thesis_cells], colWidths=[CONTENT_W])
    # flatten: thesis_cells is already list of [Paragraph]
    thesis_flat = [[item[0]] for item in thesis_cells]
    thesis_t = Table(thesis_flat, colWidths=[CONTENT_W])
    thesis_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.3, STEEL),
        ("LINEBEFORE",    (0, 0), (-1, -1), 3, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("BACKGROUND",    (0, 0), (-1,  0), STEEL),  # header row darker
    ]))
    story.append(thesis_t)
    story.append(PageBreak())
    return story


# ─── MARKET CONTEXT PAGE ──────────────────────────────────────────────────────

def build_context(styles):
    story = []
    story.append(gold_bar("  SECTION 1 — WHY POLAND NOW", styles))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(
        "Five structural forces converge in 2026 to make the Warsaw Stock Exchange one of "
        "Europe's most fertile markets for asymmetric investing. These forces are <b>independent</b> "
        "of each other — they do not all have to materialise for the thesis to work.",
        styles["body"]))
    story.append(Spacer(1, 0.3*cm))

    for i, (title, desc) in enumerate(CONTEXT_POINTS, 1):
        row_data = [[
            Paragraph(f"{i}", ParagraphStyle("num_badge", fontName="Helvetica-Bold",
                                             fontSize=16, textColor=GOLD,
                                             alignment=TA_CENTER, leading=20)),
            [Paragraph(title, styles["h3"]),
             Paragraph(desc, styles["body"])],
        ]]
        row_t = Table(row_data, colWidths=[1.0*cm, CONTENT_W - 1.0*cm])
        row_t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (0, 0), LIGHT),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ]))
        story.append(row_t)
        story.append(Spacer(1, 0.1*cm))

    story.append(Spacer(1, 0.4*cm))
    story.append(section_header("WSE STRUCTURAL CHARACTERISTICS", styles))
    story.append(Spacer(1, 0.2*cm))

    chars = [
        ("400", "listed companies; similar scale to Vienna or Oslo"),
        ("<15%", "median institutional ownership on WSE mid-caps"),
        ("60%+", "of mid-caps are founder/family controlled"),
        ("2", "median analyst coverage for WSE mid-caps (vs 8+ for German peers)"),
        ("3 days", "EU MAR insider reporting window via ESPI — first-mover advantage"),
        ("FX", "language barrier creates persistent information asymmetry = alpha (all filings in Polish)"),
    ]
    char_data = [[
        Paragraph(v, ParagraphStyle("bign", fontName="Helvetica-Bold", fontSize=13,
                                    textColor=GOLD, leading=18, alignment=TA_CENTER)),
        Paragraph(d, styles["body_sm"]),
    ] for v, d in chars]

    # 2-column grid
    for i in range(0, len(char_data), 2):
        row = char_data[i:i+2]
        if len(row) < 2:
            row.append(["", ""])
        chunk = [row[0] + row[1]]
        t = Table(chunk, colWidths=[1.8*cm, (CONTENT_W/2 - 1.8*cm - 0.2*cm),
                                    1.8*cm, (CONTENT_W/2 - 1.8*cm)])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BACKGROUND", (0, 0), (0, 0), LIGHT),
            ("BACKGROUND", (2, 0), (2, 0), LIGHT),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.15*cm))

    story.append(PageBreak())
    return story


# ─── ASYMMETRY FRAMEWORK ──────────────────────────────────────────────────────

def build_framework(styles):
    story = []
    story.append(gold_bar("  SECTION 2 — WHAT MAKES THESE IDEAS ASYMMETRIC", styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "A genuine asymmetric idea is <b>not</b> simply a cheap stock. It requires three elements "
        "simultaneously:", styles["body"]))

    three = [
        ("A", "MECHANISM", "A specific, identifiable reason the stock is mispriced — size exclusion, "
         "language barrier, conglomerate discount, binary event overhang, accounting distortion."),
        ("B", "CATALYST", "A specific event that forces price discovery. Without a catalyst, cheap "
         "stocks stay cheap indefinitely. The catalyst can be internal (M&A, earnings) or external "
         "(regulatory, macro, ownership change)."),
        ("C", "FLOOR", "An independently derivable downside limit that holds regardless of whether "
         "the catalyst materialises — asset value, replacement cost, backlog value, or regulatory entitlement."),
    ]

    for letter, title, desc in three:
        row = [[
            Paragraph(letter, ParagraphStyle("let", fontName="Helvetica-Bold", fontSize=20,
                                             textColor=WHITE, alignment=TA_CENTER, leading=24)),
            [Paragraph(title, ParagraphStyle("ftitle", fontName="Helvetica-Bold", fontSize=9,
                                              textColor=STEEL, leading=12)),
             Paragraph(desc, styles["body"])],
        ]]
        t = Table(row, colWidths=[1.0*cm, CONTENT_W - 1.0*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), NAVY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, GOLD),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.15*cm))

    story.append(Spacer(1, 0.3*cm))
    story.append(section_header("IDEA TYPE MATRIX — HOW EACH IDEA IS MISPRICED", styles))
    story.append(Spacer(1, 0.2*cm))

    matrix = [
        ["Company", "Mispricing Mechanism", "Catalyst", "Floor"],
        ["Lubawa\n(LBW)",
         "Size exclusion (€133m) + zero English IR.\nMarket treats it as textile, not defense.",
         "First institutional 5% crossing (ESPI disclosure). First English broker note.",
         "Net cash + backlog > market cap. Entry below asset value."],
        ["Agora\n(AGO)",
         "Conglomerate discount. GW newspaper 'poisons' perception of OOH business.",
         "AMS partial sale or strategic review. EBITDA > PLN 150m print.",
         "AMS alone at 6× EV/EBITDA covers full market cap twice."],
        ["mBank\n(MBK)",
         "CHF overhang over-provisioned. Parent (Commerzbank) = forced seller if UniCredit wins.",
         "CHF costs < PLN 100m/qtr. UniCredit AGM 2026 re Commerzbank.",
         "Book value PLN 830/share vs entry PLN 1,013 (cushion)."],
        ["Mirbud\n(MRB)",
         "Road contractor perception ignores rail option and land bank at 0.61× book.",
         "PKP PLK tender award. Land bank disposal/JV announcement.",
         "Land bank at historical cost > PLN 230m. Book value > entry."],
        ["Onde\n(ONDP)",
         "Generic EPC contractor perception despite locked-in regulatory pipeline.",
         "PSE framework contract. Offshore wind pre-qualification.",
         "Legally mandated EU energy pipeline = quasi-regulatory floor."],
        ["Polimex\n(PXM)",
         "Operating losses obscure nuclear pre-qualification option (priced at zero).",
         "Polish govt FID on Lubiatowo-Kopalino. Westinghouse EPC contract.",
         "Revenue base PLN 2.86bn + nuclear civil works = USD 1–3.2bn option."],
    ]

    col_ws = [1.5*cm, 4.7*cm, 4.0*cm, 4.0*cm]

    def mc(txt, bold=False, size=7.0, align=TA_LEFT, color=NAVY):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        return Paragraph(txt.replace("\n", "<br/>"),
                         ParagraphStyle("mc", fontName=fn, fontSize=size,
                                        textColor=color, leading=10, alignment=align))

    table_data = []
    for i, row in enumerate(matrix):
        if i == 0:
            table_data.append([mc(c, bold=True, color=WHITE, align=TA_CENTER) for c in row])
        else:
            table_data.append([
                mc(row[0], bold=True, size=7.5),
                mc(row[1]),
                mc(row[2], color=STEEL),
                mc(row[3], color=GREEN),
            ])

    t = Table(table_data, colWidths=col_ws, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, BGROW]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("LINEBELOW", (0, 0), (-1, 0), 2, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)
    return story


# ─── SCENARIO RANGE VISUALISER ────────────────────────────────────────────────

def make_price_range_viz(idea):
    """
    Full-width horizontal bar showing BEAR / ENTRY / BASE / BULL price markers.
    Colour zones: red (loss), amber (below base), green (above base).
    """
    from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle

    d_w = CONTENT_W
    d_h = 3.2 * cm
    d = Drawing(d_w, d_h)

    # Light background
    d.add(Rect(0, 0, d_w, d_h, fillColor=LIGHT, strokeColor=None))

    pad_l, pad_r = 2.4 * cm, 2.0 * cm
    axis_y = d_h * 0.52
    ax0 = pad_l
    ax1 = d_w - pad_r
    ax_w = ax1 - ax0

    # Price → x-pixel mapping
    lo = idea["bear"]  * 0.90
    hi = idea["bull"]  * 1.08
    span = hi - lo

    def px(price):
        return ax0 + (price - lo) / span * ax_w

    bx = px(idea["bear"])
    ex = px(idea["entry"])
    sx = px(idea["base"])
    lx = px(idea["bull"])

    # Coloured zones
    d.add(Rect(bx, axis_y - 6, ex - bx, 12, fillColor=colors.HexColor("#FFDDDD"), strokeColor=None))
    d.add(Rect(ex, axis_y - 6, sx - ex, 12, fillColor=colors.HexColor("#FFF3DD"), strokeColor=None))
    d.add(Rect(sx, axis_y - 6, lx - sx, 12, fillColor=colors.HexColor("#DDFFDD"), strokeColor=None))

    # Axis spine
    d.add(Line(ax0, axis_y, ax1, axis_y,
               strokeColor=colors.HexColor("#AAAAAA"), strokeWidth=0.8))

    def marker(x, price, label, rp, color, above):
        d.add(Line(x, axis_y - 12, x, axis_y + 12, strokeColor=color, strokeWidth=2))
        d.add(Circle(x, axis_y, 4, fillColor=color, strokeColor=WHITE, strokeWidth=1))
        ny = axis_y + 18 if above else axis_y - 26
        py2 = axis_y + 29 if above else axis_y - 37
        rp_str = f"({rp:+.0f}%)" if rp != 0 else "(entry)"
        d.add(String(x, ny,  label,
                     fontSize=7.5, fillColor=color,
                     textAnchor="middle", fontName="Helvetica-Bold"))
        d.add(String(x, py2, f"PLN {price:.0f}  {rp_str}",
                     fontSize=6.5, fillColor=color,
                     textAnchor="middle", fontName="Helvetica"))

    marker(bx, idea["bear"],  "BEAR",  ret_pct(idea["entry"], idea["bear"]),  RED,   False)
    marker(ex, idea["entry"], "ENTRY", 0,                                      GOLD,  True)
    marker(sx, idea["base"],  "BASE",  ret_pct(idea["entry"], idea["base"]),   STEEL, False)
    marker(lx, idea["bull"],  "BULL",  ret_pct(idea["entry"], idea["bull"]),   GREEN, True)

    return d


# ─── PEER MULTIPLES TABLE ─────────────────────────────────────────────────────

def make_peer_table(idea, styles):
    """
    Mini table comparing idea's current multiple to 4 European/global peers.
    Renders as a compact full-width table with a gold left bar on the subject row.
    """
    peers   = idea.get("peers", [])
    plabel  = idea.get("peer_label", "")
    metric  = peers[0][1] if peers else "Multiple"

    def pc(txt, bold=False, color=NAVY, align=TA_LEFT, size=7.5):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        return Paragraph(txt, ParagraphStyle(
            "pt", fontName=fn, fontSize=size, textColor=color,
            leading=10, alignment=align))

    hdr = [pc("Peer / Subject", bold=True, color=WHITE, align=TA_CENTER),
           pc("Geography", bold=True, color=WHITE, align=TA_CENTER),
           pc(metric,      bold=True, color=WHITE, align=TA_CENTER),
           pc("Gap",        bold=True, color=WHITE, align=TA_CENTER)]

    rows = [hdr]
    for name, _, val in peers:
        # Split "Chemring UK" into name + geo
        parts = name.rsplit(" ", 1)
        pname = parts[0] if len(parts) == 2 else name
        geo   = parts[1] if len(parts) == 2 else ""
        rows.append([pc(pname), pc(geo, align=TA_CENTER),
                     pc(val, bold=True, align=TA_CENTER, color=STEEL),
                     pc("", align=TA_CENTER)])

    # Subject (this idea) row
    if idea.get("pe"):
        subj_val = f"{idea['pe']:.1f}×  (P/E)"
    elif idea.get("pb"):
        subj_val = f"{idea['pb']:.2f}×  (P/B)"
    else:
        subj_val = "N/M"
    rows.append([
        pc(f"► {idea['ticker']} (subject)", bold=True, color=NAVY),
        pc("PL", align=TA_CENTER),
        pc(subj_val, bold=True, align=TA_CENTER, color=GOLD),
        pc(plabel, align=TA_CENTER, size=7, color=RED),
    ])

    col_ws = [4.5*cm, 2.0*cm, 3.5*cm, CONTENT_W - 10.0*cm]
    rh = [0.48*cm] * len(rows)
    t = Table(rows, colWidths=col_ws, rowHeights=rh, repeatRows=1)
    num_data_rows = len(rows)
    subject_row   = num_data_rows - 1  # 0-indexed last row

    style = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), STEEL),
        ("ROWBACKGROUNDS",(0, 1), (-1, subject_row - 1), [WHITE, BGROW]),
        ("BACKGROUND",    (0, subject_row), (-1, subject_row), colors.HexColor("#FEF9EC")),
        ("LINEBEFORE",    (0, subject_row), (0, subject_row), 3, GOLD),
        ("LINEBELOW",     (0, subject_row), (-1, subject_row), 1.5, GOLD),
        ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("LINEBELOW",     (0, 0), (-1, 0), 1.5, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ])
    t.setStyle(style)
    return t


# ─── SINGLE IDEA PAGE ─────────────────────────────────────────────────────────

def build_idea_page(idea, styles):
    story = []
    bear_r = ret_pct(idea["entry"], idea["bear"])
    base_r = ret_pct(idea["entry"], idea["base"])
    bull_r = ret_pct(idea["entry"], idea["bull"])
    pwr    = pw_ret(idea)
    a_val  = asym(idea)

    # ── Title banner ──
    rank_p = Paragraph(f"#{idea['rank']}", ParagraphStyle(
        "rank", fontName="Helvetica-Bold", fontSize=28, textColor=GOLD, leading=32))
    title_p = Paragraph(idea["name"],
                        ParagraphStyle("it", fontName="Helvetica-Bold", fontSize=18,
                                       textColor=WHITE, leading=22))
    ticker_p = Paragraph(
        f"<b>{idea['ticker']}</b> &nbsp; WSE &nbsp;|&nbsp; {idea['sector']}<br/>"
        f"<font color='#C9A84C'>{idea['type_short']}</font>",
        ParagraphStyle("is", fontName="Helvetica", fontSize=9,
                       textColor=SILVER, leading=13))

    conv_color = {"HIGH": GREEN, "MEDIUM+": AMBER, "OPTION": STEEL}[idea["conviction"]]
    conv_p = Paragraph(f"Conviction: <b>{idea['conviction']}</b> &nbsp;|&nbsp; "
                       f"Horizon: <b>{idea['horizon']}</b>",
                       ParagraphStyle("conv", fontName="Helvetica", fontSize=8,
                                      textColor=GOLD, leading=11))

    banner_data = [[rank_p, [title_p, ticker_p, Spacer(1, 4), conv_p]]]
    banner = Table(banner_data, colWidths=[1.6*cm, CONTENT_W - 1.6*cm])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBELOW",  (0, 0), (-1, -1), 3, GOLD),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    story.append(banner)
    story.append(Spacer(1, 0.3*cm))

    # ── Left column: metrics + scenarios | Right column: summary + catalyst ──
    def metric_row(label, value, sub=None):
        rows = [[
            Paragraph(label, ParagraphStyle("ml", fontName="Helvetica", fontSize=7,
                                            textColor=SILVER, leading=9)),
            Paragraph(str(value), ParagraphStyle("mv", fontName="Helvetica-Bold", fontSize=10,
                                                 textColor=NAVY, leading=12, alignment=TA_RIGHT)),
        ]]
        if sub:
            rows.append([Paragraph("", styles["body_sm"]),
                         Paragraph(sub, ParagraphStyle("ms", fontName="Helvetica-Oblique",
                                                       fontSize=6.5, textColor=SILVER,
                                                       leading=8, alignment=TA_RIGHT))])
        t = Table(rows, colWidths=[2.5*cm, 2.0*cm])
        t.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#EEEEEE")),
            ("TOPPADDING",    (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        return t

    # Build metrics
    metrics_block = []
    metrics_block.append(Paragraph("KEY METRICS", ParagraphStyle(
        "mhdr", fontName="Helvetica-Bold", fontSize=7.5, textColor=STEEL, leading=10)))
    metrics_block.append(Spacer(1, 0.15*cm))
    metrics_block.append(metric_row("Market Cap", f"PLN {idea['mktcap_pln']:,}m / €{idea['mktcap_eur']:,}m"))
    metrics_block.append(metric_row("Entry Price", f"PLN {idea['entry']:.2f}"))
    if idea.get("pe"):
        metrics_block.append(metric_row("P/E", f"{idea['pe']:.1f}×"))
    if idea.get("pb"):
        metrics_block.append(metric_row("P/Book", f"{idea['pb']:.2f}×"))
    roe_str = f"{idea['roe']:+.1f}%" if idea['roe'] else "N/M"
    metrics_block.append(metric_row("ROE", roe_str))
    if idea.get("ebitda_m"):
        metrics_block.append(metric_row("EBITDA Margin", f"{idea['ebitda_m']:.1f}%"))
    if idea.get("rev"):
        g = f"YoY: {idea['rev_g']:+.0f}%"
        metrics_block.append(metric_row("Revenue PLNm", f"{idea['rev']:,}m", g))
    metrics_block.append(metric_row("Insider %", f"{idea['insider']:.1f}%"))
    metrics_block.append(metric_row("Institutional %", f"{idea['inst']:.1f}%"))
    metrics_block.append(metric_row("Analyst Coverage", str(idea["analysts"]), "analyst(s)"))

    metrics_block.append(Spacer(1, 0.3*cm))
    metrics_block.append(Paragraph("SCENARIO ANALYSIS", ParagraphStyle(
        "mhdr2", fontName="Helvetica-Bold", fontSize=7.5, textColor=STEEL, leading=10)))
    metrics_block.append(Spacer(1, 0.15*cm))

    scen_data = [
        [Paragraph("Scenario", styles["table_hdr"]),
         Paragraph("Target", styles["table_hdr"]),
         Paragraph("Return", styles["table_hdr"]),
         Paragraph("Prob", styles["table_hdr"])],
        [Paragraph("BULL", ParagraphStyle("sc", fontName="Helvetica-Bold", fontSize=7.5,
                                          textColor=GREEN, leading=10, alignment=TA_CENTER)),
         Paragraph(f"PLN {idea['bull']:.2f}", styles["table_cell"]),
         Paragraph(f"{bull_r:+.0f}%", ParagraphStyle("sr", fontName="Helvetica-Bold",
                                                       fontSize=7.5, textColor=GREEN,
                                                       leading=10, alignment=TA_CENTER)),
         Paragraph(f"{idea['bull_p']*100:.0f}%", styles["table_cell"])],
        [Paragraph("BASE", ParagraphStyle("sc", fontName="Helvetica-Bold", fontSize=7.5,
                                          textColor=STEEL, leading=10, alignment=TA_CENTER)),
         Paragraph(f"PLN {idea['base']:.2f}", styles["table_cell"]),
         Paragraph(f"{base_r:+.0f}%", ParagraphStyle("sr", fontName="Helvetica-Bold",
                                                       fontSize=7.5, textColor=STEEL,
                                                       leading=10, alignment=TA_CENTER)),
         Paragraph(f"{idea['base_p']*100:.0f}%", styles["table_cell"])],
        [Paragraph("BEAR", ParagraphStyle("sc", fontName="Helvetica-Bold", fontSize=7.5,
                                          textColor=RED, leading=10, alignment=TA_CENTER)),
         Paragraph(f"PLN {idea['bear']:.2f}", styles["table_cell"]),
         Paragraph(f"{bear_r:+.0f}%", ParagraphStyle("sr", fontName="Helvetica-Bold",
                                                       fontSize=7.5, textColor=RED,
                                                       leading=10, alignment=TA_CENTER)),
         Paragraph(f"{idea['bear_p']*100:.0f}%", styles["table_cell"])],
        [Paragraph("PW RETURN", ParagraphStyle("pw", fontName="Helvetica-Bold", fontSize=7.5,
                                               textColor=WHITE, leading=10, alignment=TA_CENTER)),
         Paragraph("", styles["table_cell"]),
         Paragraph(f"{pwr:+.1f}%", ParagraphStyle("pwr", fontName="Helvetica-Bold",
                                                    fontSize=9, textColor=WHITE,
                                                    leading=10, alignment=TA_CENTER)),
         Paragraph("100%", styles["table_cell"])],
    ]

    scen_t = Table(scen_data, colWidths=[1.6*cm, 1.5*cm, 1.4*cm, 1.0*cm])
    scen_t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), STEEL),
        ("BACKGROUND",  (0, 4), (-1, 4), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, 3), [WHITE, BGROW, WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING",   (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 3),
    ]))
    metrics_block.append(scen_t)
    metrics_block.append(Spacer(1, 0.2*cm))

    asym_label = Paragraph(
        f"Asymmetry ratio: <b>{a_val:.1f}×</b><br/>"
        f"<font color='#8FA3B1' size=6.5>(Bull upside ÷ Bear downside)</font>",
        ParagraphStyle("ar", fontName="Helvetica", fontSize=8, textColor=NAVY, leading=12))
    metrics_block.append(asym_label)

    # Right column
    right_block = []
    right_block.append(Paragraph("WHY IT IS ASYMMETRIC", ParagraphStyle(
        "whdr", fontName="Helvetica-Bold", fontSize=8, textColor=STEEL, leading=11)))
    right_block.append(Spacer(1, 0.1*cm))
    right_block.append(Paragraph(idea["summary"], styles["body"]))
    right_block.append(Spacer(1, 0.1*cm))

    # Asymmetry note in gold box
    note_data = [[Paragraph(f"<b>Asymmetry note:</b> {idea['asymmetry_note']}",
                             ParagraphStyle("an", fontName="Helvetica", fontSize=8,
                                            textColor=NAVY, leading=12))]]
    note_t = Table(note_data, colWidths=[CONTENT_W * 0.56])
    note_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FEF9EC")),
        ("LINEBELOW",  (0, 0), (-1, -1), 1.5, GOLD),
        ("LINEBEFORE", (0, 0), (-1, -1), 3, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    right_block.append(note_t)
    right_block.append(Spacer(1, 0.25*cm))

    right_block.append(Paragraph("CATALYST", ParagraphStyle(
        "chdr", fontName="Helvetica-Bold", fontSize=8, textColor=STEEL, leading=11)))
    right_block.append(Spacer(1, 0.05*cm))
    right_block.append(Paragraph(idea["catalyst"], styles["body_sm"]))
    right_block.append(Spacer(1, 0.2*cm))

    right_block.append(Paragraph("KEY RISKS", ParagraphStyle(
        "rhdr", fontName="Helvetica-Bold", fontSize=8, textColor=RED, leading=11)))
    right_block.append(Spacer(1, 0.05*cm))
    right_block.append(Paragraph(idea["key_risk"], styles["body_sm"]))

    # Two-column layout
    left_w  = 4.7*cm
    right_w = CONTENT_W - left_w - 0.4*cm

    layout = Table(
        [[metrics_block, right_block]],
        colWidths=[left_w, right_w]
    )
    layout.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("COLPADDING",   (0, 0), (0, 0), 0),
    ]))
    story.append(layout)

    # ── Price scenario range visualiser ──
    story.append(Spacer(1, 0.20*cm))
    viz_hdr_data = [[Paragraph(
        "PRICE SCENARIO RANGE  —  bear / entry / base / bull",
        ParagraphStyle("vzh", fontName="Helvetica-Bold", fontSize=7.5,
                       textColor=STEEL, leading=10))]]
    viz_hdr_t = Table(viz_hdr_data, colWidths=[CONTENT_W])
    viz_hdr_t.setStyle(TableStyle([
        ("LINEBELOW",     (0, 0), (-1, -1), 1.0, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(viz_hdr_t)
    story.append(Spacer(1, 0.1*cm))
    story.append(make_price_range_viz(idea))
    story.append(Paragraph(
        "Zone colours: red = loss territory  |  amber = below base case  |  "
        "green = above base case.  All prices in PLN.",
        ParagraphStyle("vzcap", fontName="Helvetica-Oblique", fontSize=6.5,
                       textColor=SILVER, leading=9)))

    # ── Peer multiples comparison ──
    story.append(Spacer(1, 0.15*cm))
    peer_hdr_data = [[Paragraph(
        "PEER MULTIPLES — HOW THE ENTRY MULTIPLE COMPARES",
        ParagraphStyle("peh", fontName="Helvetica-Bold", fontSize=7.5,
                       textColor=STEEL, leading=10))]]
    peer_hdr_t = Table(peer_hdr_data, colWidths=[CONTENT_W])
    peer_hdr_t.setStyle(TableStyle([
        ("LINEBELOW",     (0, 0), (-1, -1), 1.0, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    peer_cap = Paragraph(
        "Peers are selected European or global comparables in the same sector. "
        "Multiples from Bloomberg consensus, March 2026.",
        ParagraphStyle("pecap", fontName="Helvetica-Oblique", fontSize=6.5,
                       textColor=SILVER, leading=9))
    story.append(KeepTogether([
        peer_hdr_t, Spacer(1, 0.1*cm),
        make_peer_table(idea, styles),
        peer_cap,
    ]))

    story.append(PageBreak())
    return story


# ─── PORTFOLIO CONSTRUCTION ───────────────────────────────────────────────────

def build_portfolio(styles):
    story = []
    story.append(gold_bar("  SECTION 4 — PORTFOLIO CONSTRUCTION", styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "The six ideas span six independent sectors and six distinct mispricing types. "
        "Correlation between them is low — owning all six does not concentrate the bet.",
        styles["body"]))
    story.append(Spacer(1, 0.3*cm))

    story.append(section_header("SUGGESTED SIZING (% of dedicated Poland allocation)", styles))
    story.append(Spacer(1, 0.2*cm))

    port_hdr = ["#", "Company", "Weight", "Rationale"]
    port_rows = [port_hdr] + PORTFOLIO_ROWS

    def pc(txt, bold=False, align=TA_LEFT, color=NAVY, size=8):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        return Paragraph(txt, ParagraphStyle("pc", fontName=fn, fontSize=size,
                                             textColor=color, leading=11, alignment=align))

    port_data = []
    for i, row in enumerate(port_rows):
        if i == 0:
            port_data.append([pc(c, bold=True, color=WHITE, align=TA_CENTER) for c in row])
        else:
            port_data.append([
                pc(row[0], bold=True, align=TA_CENTER),
                pc(row[1], bold=True),
                pc(row[2], bold=True, align=TA_CENTER, color=GOLD),
                pc(row[3]),
            ])

    pt = Table(port_data, colWidths=[0.7*cm, 3.8*cm, 2.0*cm, CONTENT_W - 6.5*cm], repeatRows=1)
    pt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, BGROW]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("LINEBELOW", (0, 0), (-1, 0), 2, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(pt)
    story.append(Spacer(1, 0.4*cm))

    # Exit disciplines
    story.append(section_header("EXIT DISCIPLINES", styles))
    story.append(Spacer(1, 0.2*cm))
    exits = [
        ("Lubawa (LBW)", "Exit if institutional ownership crosses 15% — discovery complete."),
        ("Agora (AGO)",  "Exit if AMS is sold (SOTP realised); hold residual for Helios/Radio."),
        ("mBank (MBK)",  "Exit at M&A bid +5% (spread trade) or PLN 1,450 (CHF-only thesis)."),
        ("Mirbud (MRB)", "Exit if rail backlog crosses PLN 1bn confirmed awards."),
        ("Onde (ONDP)",  "Exit when PSE framework contracts convert to revenue (2–3 years)."),
        ("Polimex (PXM)","Exit at nuclear FID — option value crystallises fast post-announcement."),
    ]
    for company, rule in exits:
        row = [[
            Paragraph(company, ParagraphStyle("ec", fontName="Helvetica-Bold", fontSize=8,
                                              textColor=STEEL, leading=11)),
            Paragraph(rule, styles["body_sm"]),
        ]]
        t = Table(row, colWidths=[2.8*cm, CONTENT_W - 2.8*cm])
        t.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDDDDD")),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ]))
        story.append(t)

    story.append(Spacer(1, 0.4*cm))

    # Common risks
    story.append(section_header("COMMON RISKS TO THE ENTIRE THESIS", styles))
    story.append(Spacer(1, 0.15*cm))
    common_risks = [
        ("PLN Currency", "All six positions are PLN-denominated. Hedge via EUR/PLN forward if exposure > €20m."),
        ("Polish Politics", "Government can weaponise sector taxes (bank levy, media law). Most acute for mBank and Agora."),
        ("EU Fund Delays", "Poland holds €76bn of EU funds. Disbursement delays slow Mirbud / Onde / Polimex pipeline."),
        ("Rate Environment", "Aggressive NBP rate cuts compress mBank NIM (partially offset by CHF resolution)."),
        ("Global Risk-Off", "CEE names sell first in global selloffs. Size for 18–36 month horizon, not 3-month trades."),
    ]
    for risk, desc in common_risks:
        row = [[
            Paragraph(f"⚠ {risk}", ParagraphStyle("rr", fontName="Helvetica-Bold", fontSize=8,
                                                    textColor=RED, leading=11)),
            Paragraph(desc, styles["body_sm"]),
        ]]
        t = Table(row, colWidths=[2.8*cm, CONTENT_W - 2.8*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF5F5")),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#FFCCCC")),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.08*cm))

    story.append(Spacer(1, 0.4*cm))

    # Visual allocation bar chart
    # header and bars are kept together below — no standalone header here

    # Use ticker so names never wrap in the narrow label column
    bar_data = [(idea["ticker"], pw_ret(idea)) for idea in IDEAS]
    bar_data.sort(key=lambda x: x[1], reverse=True)

    max_val = max(v for _, v in bar_data)
    bar_total_w = CONTENT_W - 3.5*cm

    # Build all bars as rows in ONE table so they never split across pages
    all_bar_rows = []
    for name, val in bar_data:
        bar_w = max(0.3*cm, (val / max_val) * bar_total_w)
        bar_color = GREEN if val > 25 else (AMBER if val > 10 else STEEL)
        # Inline rect via a coloured cell with fixed width; pad remaining space in same cell
        name_p = Paragraph(
            name, ParagraphStyle("bn", fontName="Helvetica-Bold", fontSize=8,
                                 textColor=NAVY, leading=10))
        # Bar: colour the cell bg, fix its width via a nested table
        bar_inner = Table([[""]], colWidths=[bar_w], rowHeights=[0.48*cm])
        bar_inner.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bar_color)]))
        val_p = Paragraph(
            f"<b>{val:+.0f}%</b>",
            ParagraphStyle("bv", fontName="Helvetica-Bold", fontSize=9,
                           textColor=bar_color, leading=11, alignment=TA_RIGHT))
        all_bar_rows.append([name_p, bar_inner, val_p])

    bar_table = Table(
        all_bar_rows,
        colWidths=[1.6*cm, bar_total_w, 1.6*cm],
        rowHeights=[0.65*cm] * len(all_bar_rows),
    )
    bar_table.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [WHITE, BGROW]),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.3, colors.HexColor("#EEEEEE")),
    ]))
    bar_hdr_p = Paragraph(
        "VISUALISED ALLOCATION — PROBABILITY-WEIGHTED RETURNS",
        ParagraphStyle("barhdr2", fontName="Helvetica-Bold", fontSize=9,
                       textColor=NAVY, leading=12))
    bar_hdr_line = HRFlowable(width="100%", thickness=1.5, color=GOLD, spaceAfter=6)
    story.append(KeepTogether([bar_hdr_p, bar_hdr_line, Spacer(1, 0.15*cm), bar_table]))

    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "Bar length proportional to probability-weighted return across bear / base / bull scenarios.",
        ParagraphStyle("bcap", fontName="Helvetica-Oblique", fontSize=6.5,
                       textColor=SILVER, leading=9)))
    # No PageBreak — monitoring section flows on the same page if room permits
    return story


# ─── MONITORING GRID ──────────────────────────────────────────────────────────

def build_monitoring(styles):
    story = []
    story.append(gold_bar("  SECTION 5 — MONITORING GRID & VERDICT", styles))
    story.append(Spacer(1, 0.3*cm))

    mon_rows = [
        ["Lubawa (LBW)",   "Foreign entity >5% stake (ESPI)",         "gpw.pl/espi-ebi-reports → LBW"],
        ["Lubawa (LBW)",   "First English investor presentation",       "lubawa.pl/investor-relations"],
        ["Lubawa (LBW)",   "First broker research note (any language)",  "Bloomberg BN LUBAWA"],
        ["Agora (AGO)",    "Strategic review / AMS sale approach",       "agora.pl ESPI section"],
        ["Agora (AGO)",    "EBITDA quarterly trend vs PLN 150m target",  "agora.pl/en/investor-relations"],
        ["mBank (MBK)",    "CHF cost per quarter < PLN 100m",           "mbank.pl/en/investor-relations"],
        ["mBank (MBK)",    "UniCredit AGM re Commerzbank (May 2026)",    "Bloomberg: UCG IM Equity"],
        ["mBank (MBK)",    "German govt stake sale in Commerzbank",      "Bundesanzeiger + Bloomberg"],
        ["Mirbud (MRB)",   "PKP PLK tender result (ESPI)",              "przetargi.gov.pl → Mirbud"],
        ["Mirbud (MRB)",   "Land disposal / JV announcement",           "mirbud.pl ESPI"],
        ["Onde (ONDP)",    "PSE framework contract award",              "pse.pl/en + ESPI ONDP"],
        ["Onde (ONDP)",    "Offshore wind pre-qualification",           "pse.pl / orlen.pl"],
        ["Polimex (PXM)",  "Nuclear FID announcement",                  "gov.pl/web/nuclear-energy"],
        ["Polimex (PXM)",  "Westinghouse consortium EPC update",        "Bloomberg: PXM PW Equity"],
    ]

    def mc(txt, bold=False, size=7.5, align=TA_LEFT, color=NAVY):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        return Paragraph(txt, ParagraphStyle("mg", fontName=fn, fontSize=size,
                                             textColor=color, leading=10, alignment=align))

    hdr = [mc("Company", bold=True, color=WHITE, align=TA_CENTER),
           mc("Signal to Monitor", bold=True, color=WHITE, align=TA_CENTER),
           mc("Data Source", bold=True, color=WHITE, align=TA_CENTER)]
    data = [hdr] + [[mc(r[0], bold=True), mc(r[1]), mc(r[2], color=STEEL)] for r in mon_rows]

    t = Table(data, colWidths=[2.6*cm, 6.0*cm, 5.6*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, BGROW]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("LINEBELOW", (0, 0), (-1, 0), 2, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Master ESPI link: gpw.pl/espi-ebi-reports — bookmark and set email alerts per ticker.",
        ParagraphStyle("espi", fontName="Helvetica-Oblique", fontSize=7.5,
                       textColor=SILVER, leading=10)))
    story.append(Spacer(1, 0.5*cm))

    # Final verdict
    story.append(section_header("FINAL VERDICT — RANKED BY PROBABILITY-WEIGHTED RETURN", styles))
    story.append(Spacer(1, 0.2*cm))

    sorted_ideas = sorted(IDEAS, key=lambda x: pw_ret(x), reverse=True)
    verd_hdr = ["Rank", "Company", "Ticker", "Idea Type", "PW Ret%", "Conviction", "Horizon"]
    verd_data = [[Paragraph(c, ParagraphStyle("vh", fontName="Helvetica-Bold", fontSize=7.5,
                                               textColor=WHITE, leading=10, alignment=TA_CENTER))
                  for c in verd_hdr]]
    for i, idea in enumerate(sorted_ideas, 1):
        pwr = pw_ret(idea)
        pwr_c = GREEN if pwr > 20 else (AMBER if pwr > 0 else RED)
        conv_c = {"HIGH": GREEN, "MEDIUM+": AMBER, "OPTION": STEEL}[idea["conviction"]]
        verd_data.append([
            Paragraph(str(i), ParagraphStyle("vn", fontName="Helvetica-Bold", fontSize=8,
                                              textColor=NAVY, leading=10, alignment=TA_CENTER)),
            Paragraph(idea["name"] if len(idea["name"]) <= 12 else idea["ticker"] + " SA", ParagraphStyle("vn2", fontName="Helvetica-Bold", fontSize=8,
                                                    textColor=NAVY, leading=10)),
            Paragraph(idea["ticker"], ParagraphStyle("vt", fontName="Helvetica", fontSize=8,
                                                      textColor=STEEL, leading=10, alignment=TA_CENTER)),
            Paragraph(idea["type_short"], ParagraphStyle("vts", fontName="Helvetica", fontSize=7.5,
                                                          textColor=NAVY, leading=10)),
            Paragraph(f"{pwr:+.1f}%", ParagraphStyle("vr", fontName="Helvetica-Bold", fontSize=9,
                                                       textColor=pwr_c, leading=10, alignment=TA_CENTER)),
            Paragraph(idea["conviction"], ParagraphStyle("vc", fontName="Helvetica-Bold", fontSize=8,
                                                          textColor=conv_c, leading=10, alignment=TA_CENTER)),
            Paragraph(idea["horizon"], ParagraphStyle("vh2", fontName="Helvetica", fontSize=7.5,
                                                       textColor=NAVY, leading=10, alignment=TA_CENTER)),
        ])

    vt = Table(verd_data, colWidths=[1.0*cm, 2.8*cm, 1.4*cm, 3.8*cm, 1.8*cm, 2.0*cm, 2.8*cm],
               repeatRows=1)
    vt.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, BGROW]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("LINEBELOW", (0, 0), (-1, 0), 2, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(vt)
    story.append(Spacer(1, 0.4*cm))

    # Closing note
    closing = (
        "<b>Overall Assessment.</b> Poland in Q1 2026 offers a rare confluence of structural inflows "
        "(MSCI reclassification), a defense super-cycle not yet priced into sub-contractors, a banking "
        "sector CHF overhang that is definitively resolving, and an energy transition mandate that is "
        "legally binding and funded. The six companies in this report are not random cheap stocks — each "
        "has a specific named mispricing mechanism, a specific named catalyst, and a hard downside floor. "
        "The edge: you read Polish. Most of the competition does not."
    )
    close_data = [[Paragraph(closing, ParagraphStyle("cl", fontName="Helvetica", fontSize=8.5,
                                                      textColor=NAVY, leading=13, alignment=TA_JUSTIFY))]]
    close_t = Table(close_data, colWidths=[CONTENT_W])
    close_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("LINEBEFORE",  (0, 0), (-1, -1), 4, GOLD),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
    ]))
    story.append(close_t)

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "DISCLAIMER: This report is for informational purposes only and does not constitute investment advice. "
        "All figures are illustrative and based on publicly available data. Past performance is not indicative "
        "of future results. Invest only what you can afford to lose. For professional investors only.",
        ParagraphStyle("disc", fontName="Helvetica-Oblique", fontSize=6.5,
                       textColor=SILVER, leading=9)))
    return story


# ─── MAIN BUILD ───────────────────────────────────────────────────────────────

def build_pdf(output_path="poland_asymmetric_ideas.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B + 1.1*cm,  # space for footer
        title="Poland Asymmetric Ideas — March 2026",
        author="MZApp Framework",
        subject="WSE Asymmetric Equity Ideas",
    )

    styles = make_styles()
    story  = []

    story += build_cover(styles)
    story += build_context(styles)
    story += build_framework(styles)
    story.append(PageBreak())   # ensure framework ends cleanly; first idea on fresh page

    for idea in IDEAS:
        story += build_idea_page(idea, styles)

    story += build_portfolio(styles)
    story += build_monitoring(styles)

    doc.build(story, canvasmaker=ReportCanvas)
    print(f"\n  PDF generated: {os.path.abspath(output_path)}")
    print(f"  Size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    build_pdf("poland_asymmetric_ideas.pdf")
