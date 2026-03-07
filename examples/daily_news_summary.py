"""
Daily World Intelligence Brief — March 6, 2026
3-page PDF: Causal thinking · Systems · Mental models
Output: daily_news_summary_2026_03_06.pdf

Design philosophy:
  Every story follows the same explanatory structure:
  TRIGGER → ROOT CAUSE → HIDDEN DRIVER → WHO BENEFITS → LESSON
  The goal is not to inform — it is to build lasting mental models.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.pdfgen import canvas
import os

# ─── COLOUR PALETTE ────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0B1D35")
GOLD    = colors.HexColor("#C9A84C")
STEEL   = colors.HexColor("#1E3A5F")
SILVER  = colors.HexColor("#8FA3B1")
LIGHT   = colors.HexColor("#F4F6F9")
WHITE   = colors.white
GREEN   = colors.HexColor("#1B5E20")
RED     = colors.HexColor("#B71C1C")
AMBER   = colors.HexColor("#E65100")
TEAL    = colors.HexColor("#004D5B")
PURPLE  = colors.HexColor("#311B92")
WARM    = colors.HexColor("#FFF8EE")
ROSE    = colors.HexColor("#FCE4EC")
MINT    = colors.HexColor("#E8F5E9")

PAGE_W, PAGE_H = A4
MARGIN   = 1.75 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "daily_news_summary_2026_03_06.pdf")


# ─── STYLES ────────────────────────────────────────────────────────────────────
def S():
    s = {}
    def p(name, **kw):
        s[name] = ParagraphStyle(name, **kw)

    p("cover_title",  fontName="Helvetica-Bold",   fontSize=26, textColor=WHITE,
      leading=32, alignment=TA_CENTER)
    p("cover_sub",    fontName="Helvetica",         fontSize=11, textColor=GOLD,
      leading=16, alignment=TA_CENTER, spaceAfter=2)
    p("cover_date",   fontName="Helvetica",         fontSize=9,  textColor=SILVER,
      leading=13, alignment=TA_CENTER)
    p("cover_mission",fontName="Helvetica-Oblique", fontSize=10, textColor=colors.HexColor("#CCE0F0"),
      leading=15, alignment=TA_CENTER, spaceAfter=0)

    p("page_head",    fontName="Helvetica-Bold",    fontSize=15, textColor=NAVY,
      leading=20, spaceAfter=2)
    p("section",      fontName="Helvetica-Bold",    fontSize=11, textColor=WHITE,
      leading=15, spaceAfter=0)
    p("section_dark", fontName="Helvetica-Bold",    fontSize=11, textColor=NAVY,
      leading=15, spaceAfter=4, spaceBefore=10)

    p("body",         fontName="Helvetica",         fontSize=9,  textColor=colors.HexColor("#1A1A2E"),
      leading=13.5, spaceAfter=5, alignment=TA_JUSTIFY)
    p("body_b",       fontName="Helvetica-Bold",    fontSize=9,  textColor=NAVY,
      leading=13.5, spaceAfter=4)
    p("body_i",       fontName="Helvetica-Oblique", fontSize=9,  textColor=STEEL,
      leading=13.5, spaceAfter=4, leftIndent=8)
    p("small",        fontName="Helvetica",         fontSize=7.5,textColor=SILVER,
      leading=11, alignment=TA_CENTER)
    p("small_b",      fontName="Helvetica-Bold",    fontSize=7.5,textColor=NAVY,
      leading=11)
    p("tag",          fontName="Helvetica-Bold",    fontSize=7.5,textColor=WHITE,
      leading=10, alignment=TA_CENTER)
    p("lesson_num",   fontName="Helvetica-Bold",    fontSize=16, textColor=GOLD,
      leading=20, alignment=TA_CENTER)
    p("lesson_head",  fontName="Helvetica-Bold",    fontSize=10, textColor=NAVY,
      leading=14, spaceAfter=2)
    p("lesson_body",  fontName="Helvetica",         fontSize=8.5,textColor=colors.HexColor("#2A2A3E"),
      leading=13, alignment=TA_JUSTIFY)
    p("chain_label",  fontName="Helvetica-Bold",    fontSize=7,  textColor=WHITE,
      leading=9,  alignment=TA_CENTER)
    p("chain_text",   fontName="Helvetica",         fontSize=8,  textColor=colors.HexColor("#1A1A2E"),
      leading=11.5, alignment=TA_JUSTIFY)
    p("footer",       fontName="Helvetica-Oblique", fontSize=6.5,textColor=SILVER,
      leading=9, alignment=TA_CENTER)
    return s


# ─── HEADER/FOOTER CANVAS ──────────────────────────────────────────────────────
class HF(canvas.Canvas):
    def __init__(self, *a, **kw):
        self._pn = 0
        super().__init__(*a, **kw)

    def showPage(self):
        self._pn += 1
        if self._pn > 1:
            # top bar
            self.setFillColor(NAVY)
            self.rect(0, PAGE_H - 1.0*cm, PAGE_W, 1.0*cm, fill=1, stroke=0)
            self.setFillColor(GOLD)
            self.rect(0, PAGE_H - 1.0*cm, 0.3*cm, 1.0*cm, fill=1, stroke=0)
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(WHITE)
            self.drawString(0.55*cm, PAGE_H - 0.65*cm,
                            "DAILY WORLD INTELLIGENCE BRIEF  ·  Explain the World  ·  March 6, 2026")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(SILVER)
            self.drawRightString(PAGE_W - 0.55*cm, PAGE_H - 0.65*cm, f"Page {self._pn} of 3")
            # gold accent top-right
            self.setFillColor(GOLD)
            self.rect(PAGE_W - 0.3*cm, PAGE_H - 1.0*cm, 0.3*cm, 1.0*cm, fill=1, stroke=0)
            # bottom bar
            self.setFillColor(NAVY)
            self.rect(0, 0, PAGE_W, 0.7*cm, fill=1, stroke=0)
            self.setFont("Helvetica-Oblique", 6.5)
            self.setFillColor(SILVER)
            self.drawCentredString(PAGE_W / 2, 0.23*cm,
                "For educational purposes only — Sources: Wikipedia, Atlantic Council, CSIS, Yale Budget Lab, "
                "CBO, ScienceDaily, WEF, UN News  ·  © 2026 Daily Brief")
        super().showPage()

    def save(self):
        super().save()


# ─── SECTION HEADER ────────────────────────────────────────────────────────────
def sec_header(title, styles, bg=NAVY, accent=GOLD):
    data = [[Paragraph(title, styles["section"])]]
    t = Table(data, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("LINEBELOW",    (0,0), (-1,-1), 2, accent),
    ]))
    return t


# ─── CAUSAL CHAIN BLOCK ────────────────────────────────────────────────────────
# Shows: TRIGGER → ROOT CAUSE → HIDDEN DRIVER → WHO BENEFITS
def causal_chain(trigger, root, hidden, benefits, styles):
    labels = ["TRIGGER", "ROOT CAUSE", "HIDDEN DRIVER", "WHO BENEFITS"]
    values = [trigger, root, hidden, benefits]
    bg_cols = [RED, AMBER, STEEL, GREEN]

    label_cells = [Paragraph(l, styles["chain_label"]) for l in labels]
    value_cells = [Paragraph(v, styles["chain_text"]) for v in values]

    cw = CONTENT_W / 4
    # Arrow spacer between columns handled by padding
    t = Table(
        [label_cells, value_cells],
        colWidths=[cw] * 4,
        rowHeights=[0.52*cm, None],
    )
    t.setStyle(TableStyle([
        # label row backgrounds
        ("BACKGROUND", (0,0), (0,0), RED),
        ("BACKGROUND", (1,0), (1,0), AMBER),
        ("BACKGROUND", (2,0), (2,0), STEEL),
        ("BACKGROUND", (3,0), (3,0), GREEN),
        # value row
        ("BACKGROUND", (0,1), (-1,-1), LIGHT),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING",(0,0), (-1,-1), 5),
        ("LINEAFTER",  (0,0), (2,1), 0.5, WHITE),
        ("GRID",       (0,0), (-1,-1), 0.3, SILVER),
    ]))
    return t


# ─── MYTH BOX ──────────────────────────────────────────────────────────────────
def myth_box(myth, reality, styles, accent=RED):
    rows = [
        [Paragraph(f"✗  WHAT MOST PEOPLE BELIEVE", styles["chain_label"]),
         Paragraph(f"✔  WHAT THE EVIDENCE SHOWS", styles["chain_label"])],
        [Paragraph(myth, styles["chain_text"]),
         Paragraph(reality, styles["chain_text"])],
    ]
    t = Table(rows, colWidths=[CONTENT_W*0.5, CONTENT_W*0.5])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), accent),
        ("BACKGROUND", (1,0), (1,0), GREEN),
        ("BACKGROUND", (0,1), (0,1), ROSE),
        ("BACKGROUND", (1,1), (1,1), MINT),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LINEAFTER",    (0,0), (0,1), 1, WHITE),
        ("GRID",         (0,0), (-1,-1), 0.3, SILVER),
    ]))
    return t


# ─── LESSON BOX ────────────────────────────────────────────────────────────────
def lesson_box(number, headline, body_text, styles, color=NAVY):
    num_cell  = Paragraph(str(number), styles["lesson_num"])
    head_cell = Paragraph(headline, styles["lesson_head"])
    body_cell = Paragraph(body_text, styles["lesson_body"])

    num_t = Table([[num_cell]], colWidths=[1.1*cm])
    num_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), color),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    content = Table(
        [[head_cell], [body_cell]],
        colWidths=[CONTENT_W - 1.3*cm],
    )
    content.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,0), LIGHT),
        ("BACKGROUND",   (0,1), (0,1), WHITE),
        ("LEFTPADDING",  (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LINEBELOW",    (0,1), (0,1), 0.5, SILVER),
    ]))
    outer = Table([[num_t, content]], colWidths=[1.3*cm, CONTENT_W - 1.3*cm])
    outer.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
    ]))
    return outer


# ─── COVER PAGE ────────────────────────────────────────────────────────────────
def cover(s):
    story = []

    # ── Full-width banner ─────────────────────────────────────────────────────
    def banner_cell(text, style, bg, padT=10, padB=8):
        t = Table([[Paragraph(text, s[style])]], colWidths=[CONTENT_W])
        t.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), bg),
            ("TOPPADDING",   (0,0), (-1,-1), padT),
            ("BOTTOMPADDING",(0,0), (-1,-1), padB),
            ("LEFTPADDING",  (0,0), (-1,-1), 14),
            ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ]))
        return t

    story.append(banner_cell("DAILY WORLD INTELLIGENCE BRIEF", "cover_title", NAVY, 24, 10))
    story.append(banner_cell(
        "Why things happen · Who drives the outcome · What to update in your mental model",
        "cover_mission", STEEL, 8, 8))
    story.append(banner_cell("Friday, March 6, 2026  ·  Edition #1", "cover_date",
                              colors.HexColor("#0D1F3C"), 5, 6))
    story.append(Spacer(1, 0.45*cm))

    # ── HOW TO READ THIS BRIEF ────────────────────────────────────────────────
    story.append(sec_header("HOW TO READ THIS BRIEF", s, bg=STEEL, accent=GOLD))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Most news tells you <b>what</b> happened. This brief tells you <b>why</b> it happened, "
        "<b>who</b> benefits, and <b>what mental model</b> the event should update. "
        "Three pages. Three stories. Each analysed with the same four-step framework:",
        s["body"],
    ))
    story.append(Spacer(1, 0.15*cm))

    framework = [
        ["TRIGGER",      RED,    "The visible event that captured headlines."],
        ["ROOT CAUSE",   AMBER,  "The deeper structural condition that made it inevitable."],
        ["HIDDEN DRIVER",STEEL,  "The incentive or actor most coverage ignores."],
        ["WHO BENEFITS", GREEN,  "Follow the beneficiaries — they often explain the cause."],
    ]
    fw_rows = []
    for label, color, desc in framework:
        tag = Table([[Paragraph(label, s["tag"])]], colWidths=[2.5*cm], rowHeights=[0.48*cm])
        tag.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), color),
            ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING",   (0,0), (-1,-1), 2),
            ("BOTTOMPADDING",(0,0), (-1,-1), 2),
            ("LEFTPADDING",  (0,0), (-1,-1), 4),
            ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ]))
        fw_rows.append([tag, Paragraph(desc, s["body"])])

    fw_t = Table(fw_rows, colWidths=[2.7*cm, CONTENT_W - 2.7*cm])
    fw_t.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [WHITE, LIGHT]),
        ("LINEBELOW",    (0,-1),(-1,-1), 0.5, SILVER),
        ("LINEABOVE",    (0, 0),(-1, 0), 0.5, SILVER),
    ]))
    story.append(fw_t)
    story.append(Spacer(1, 0.35*cm))

    # ── TODAY'S THREE STORIES ─────────────────────────────────────────────────
    story.append(sec_header("TODAY'S THREE STORIES — WHAT THEY REALLY TELL US", s))
    story.append(Spacer(1, 0.2*cm))

    cards = [
        (RED,    "PAGE 2 · STORY 1",
         "The War on Iran",
         "Why a war that had 'last-minute diplomatic breakthrough' headlines still happened — "
         "and what that reveals about how military decisions are actually made."),
        (TEAL,   "PAGE 2 · STORY 2",
         "US Tariffs — A $1,500 Tax on Every Household",
         "How a policy sold as protecting workers mathematically shifts income upward "
         "while making the people it claims to help poorer."),
        (GREEN,  "PAGE 3 · STORY 3",
         "Science: Fusion, CRISPR & Solar at 34%",
         "Three breakthroughs that most people think are 'decades away' — and why "
         "that belief is wrong and will cost you in decisions made this decade."),
    ]
    card_rows = []
    for color, label, title, desc in cards:
        tag = Table([[Paragraph(label, s["tag"])]], colWidths=[CONTENT_W * 0.3],
                    rowHeights=[0.45*cm])
        tag.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), color),
            ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING",   (0,0), (-1,-1), 2),
            ("BOTTOMPADDING",(0,0), (-1,-1), 2),
            ("LEFTPADDING",  (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ]))
        content = Table(
            [[Paragraph(f"<b>{title}</b>", s["body_b"])],
             [Paragraph(desc, s["body"])]],
            colWidths=[CONTENT_W * 0.7],
        )
        content.setStyle(TableStyle([
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ("TOPPADDING",   (0,0), (-1,-1), 4),
            ("BOTTOMPADDING",(0,0), (-1,-1), 4),
            ("BACKGROUND",   (0,0), (-1,-1), WHITE),
        ]))
        outer = Table([[tag, content]],
                      colWidths=[CONTENT_W*0.3, CONTENT_W*0.7])
        outer.setStyle(TableStyle([
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("TOPPADDING",   (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0), (-1,-1), 0),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("LINEBELOW",    (0,0), (-1,-1), 0.5, SILVER),
        ]))
        card_rows.append(outer)
        story.append(outer)

    story.append(Spacer(1, 0.4*cm))

    # ── WHAT THIS BRIEF IS NOT ────────────────────────────────────────────────
    story.append(sec_header("WHAT THIS BRIEF IS NOT", s, bg=colors.HexColor("#1C1C1C"), accent=GOLD))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "It is not balanced reporting. It is analytical — it takes the evidence seriously "
        "and draws conclusions. It is not cynical — the goal is not to say 'everything is corrupt' "
        "but to build a more accurate map of how power, incentives, and systems actually operate. "
        "<b>A better map leads to better decisions.</b>",
        s["body"],
    ))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "<i>\"The map is not the territory — but a wrong map is worse than no map.\"</i>  — Alfred Korzybski",
        s["body_i"],
    ))

    story.append(PageBreak())
    return story


# ─── PAGE 2: WAR & TARIFFS ─────────────────────────────────────────────────────
def page2(s):
    story = []
    story.append(Spacer(1, 1.2*cm))

    # ══ STORY 1: Iran War ═════════════════════════════════════════════════════
    story.append(Paragraph("PAGE 2  ·  POWER & MONEY", s["page_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=2, color=GOLD, spaceAfter=10))

    story.append(sec_header(
        "STORY 1  ·  THE WAR ON IRAN — WHY DIPLOMACY FAILED AT THE LAST SECOND", s, bg=RED))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        "On February 27, 2026 — <b>one day before</b> the US-Israeli bombing campaign — "
        "Oman's Foreign Minister announced a 'breakthrough': Iran had agreed to zero uranium "
        "stockpiling and full IAEA verification. Peace was declared 'within reach.' "
        "The next morning, Operation Epic Fury launched against 153 Iranian cities. "
        "The strikes killed Supreme Leader Khamenei and approximately 49 senior commanders. "
        "Why did a diplomatic agreement produce a war?",
        s["body"],
    ))
    story.append(Spacer(1, 0.15*cm))

    story.append(causal_chain(
        trigger="Iran accepted zero-enrichment + IAEA verification (Feb 27). Strikes launched anyway (Feb 28).",
        root="The decision had already been made. Military planning for 'Operation Epic Fury' had run for months. "
             "The diplomatic offer came too late to enter the decision loop — or was seen as unverifiable.",
        hidden="Israel's strategic window: Iran's proxy network (Hezbollah, Hamas, Houthis) had been "
               "severely degraded in 2023–2025. The nuclear programme was at 460kg of 60%-enriched uranium. "
               "This was the last moment to act before Iran crossed the threshold — or rebuilt its proxies.",
        benefits="Israel achieves strategic depth for a generation. US arms manufacturers (F-35 sorties, "
                 "JDAM kits, naval assets deployed). Russia: higher oil prices fill its war chest. "
                 "China: US attention shifts from Taiwan.",
        styles=s,
    ))
    story.append(Spacer(1, 0.25*cm))

    story.append(myth_box(
        myth="Diplomacy failed because Iran was not serious. Authoritarian regimes cannot be trusted to negotiate.",
        reality="Iran's offer was verified by Oman (a trusted intermediary used in prior deals). "
                "The evidence suggests the decision to strike was already locked in before the diplomatic "
                "signal could change the calculus. States — including democracies — sometimes use "
                "diplomacy as cover for predetermined military action.",
        styles=s, accent=RED,
    ))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("<b>What this tells us about how the world works:</b>", s["body_b"]))
    story.append(Paragraph(
        "Military decisions are not made at the last minute based on the latest information. "
        "They are made weeks or months in advance, driven by strategic windows, alliance commitments, "
        "and domestic political calendars. By the time a 'diplomatic breakthrough' is announced, "
        "the military option has often already been authorised. "
        "<b>The lesson: watch the timeline of military preparation, not the diplomatic statements.</b>",
        s["body"],
    ))
    story.append(Spacer(1, 0.15*cm))

    story.append(Paragraph(
        "<i>Further risk:</i> Iran's Rial hit 1.75 million per USD. Basic food costs rose ~70% in a month. "
        "An internal power vacuum (49 senior leaders killed, no clear succession) now creates "
        "fragmentation risk: Kurdish, Azeri, and Baluchi autonomy movements are activating. "
        "A fragmented Iran is potentially worse for regional stability than an intact adversarial one.",
        s["body_i"],
    ))
    story.append(Spacer(1, 0.35*cm))

    # ══ STORY 2: Tariffs ══════════════════════════════════════════════════════
    story.append(sec_header(
        "STORY 2  ·  TARIFFS — WHO ACTUALLY PAYS AND WHY THIS IS A REGRESSIVE TAX", s, bg=AMBER))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        "The Trump administration's tariff regime — a 15% global tariff plus targeted levies — "
        "is described as protecting American workers from unfair foreign competition. "
        "The empirical data from Yale's Budget Lab, the CBO, and Stanford SIEPR tells a different story.",
        s["body"],
    ))
    story.append(Spacer(1, 0.15*cm))

    story.append(causal_chain(
        trigger="15% global tariff + targeted China/steel/auto levies. Average US effective tariff rate: "
                "highest since 1936.",
        root="US deindustrialisation since 1990s left manufacturing communities economically desperate "
             "and politically responsive to 'protect jobs' framing — regardless of whether the mechanism works.",
        hidden="Tariff revenue ($194.8B above baseline) flows to the US Treasury — NOT to workers. "
               "The distributional impact is regressive: lower-income households lose 2.6× more "
               "(as % of income) than top earners.",
        benefits="US Treasury (short-term revenue). Domestic steel/aluminium producers (a tiny sector). "
                 "Politicians who can claim action. NOT: manufacturing workers — 77,000 mfg jobs lost "
                 "Apr–Dec 2025.",
        styles=s,
    ))
    story.append(Spacer(1, 0.25*cm))

    story.append(myth_box(
        myth="Tariffs protect workers and bring manufacturing jobs back home. Foreign countries pay the tariff.",
        reality="Foreign exporters adjust prices but the tariff is paid by US importers — then passed to consumers. "
                "Yale: avg household cost $1,500/yr. Steel-consuming jobs outnumber steel-producing jobs 80:1. "
                "Manufacturing lost 77,000 jobs under the tariff regime. The bottom income decile pays "
                "2.3% of income; top decile pays 0.9%. This is a consumption tax that hits the poor hardest.",
        styles=s, accent=AMBER,
    ))
    story.append(Spacer(1, 0.2*cm))

    # Data table
    data_rows = [
        ["Metric", "Value", "Source"],
        ["Avg household cost (2026)", "~$1,500/year", "Yale Budget Lab"],
        ["Consumer price level increase", "+0.6% to +1.0%", "CBO / Yale"],
        ["Manufacturing jobs lost (2025)", "77,000", "BLS via Yale"],
        ["Unemployment rate impact", "+0.3 pp by end-2026", "Yale Budget Lab"],
        ["Long-run GDP effect", "Persistently –0.1% smaller", "CBO"],
        ["Burden: 2nd income decile", "–2.3% of disposable income", "Yale Budget Lab"],
        ["Burden: top income decile", "–0.9% of disposable income", "Yale Budget Lab"],
        ["Tariff revenue 2026–2035", "~$1.1–1.3 trillion (gross)", "CBO"],
    ]
    cw = [CONTENT_W*0.38, CONTENT_W*0.32, CONTENT_W*0.30]
    dt = Table(data_rows, colWidths=cw, repeatRows=1)
    dt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",    (0,1), (-1,-1), colors.HexColor("#1A1A2E")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT]),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("GRID",         (0,0), (-1,-1), 0.3, SILVER),
        ("BACKGROUND",   (1,7), (1,7), colors.HexColor("#FFEBEE")),
        ("BACKGROUND",   (1,8), (1,8), MINT),
    ]))
    story.append(dt)
    story.append(Spacer(1, 0.15*cm))

    story.append(Paragraph(
        "<b>What this tells us about how the world works:</b> "
        "Economic policy is not primarily designed by economists — it is designed by political strategists. "
        "The beneficiary of a policy and the stated beneficiary are often different people. "
        "<b>The test: follow the money.</b> If a policy generates $1.3T in government revenue "
        "while costing low-income households 2.3% of their income, the policy is a redistribution mechanism "
        "— regardless of what it is called.",
        s["body"],
    ))

    story.append(PageBreak())
    return story


# ─── PAGE 3: SCIENCE & MENTAL MODELS ──────────────────────────────────────────
def page3(s):
    story = []
    story.append(Spacer(1, 1.2*cm))
    story.append(Paragraph("PAGE 3  ·  SCIENCE & THE ART OF UPDATING YOUR BELIEFS", s["page_head"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=2, color=GOLD, spaceAfter=10))

    # ══ STORY 3: Science ══════════════════════════════════════════════════════
    story.append(sec_header(
        "STORY 3  ·  THREE BREAKTHROUGHS — AND WHY YOU UNDERESTIMATE THEM", s, bg=GREEN))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        "The systematic bias in how humans evaluate scientific progress is called <b>linear thinking</b>. "
        "We assume tomorrow will look roughly like today, adjusted by a small increment. "
        "Exponential systems — where each step compounds the previous one — violate this expectation "
        "consistently. Below: three breakthroughs, each misunderstood as distant, each measurably closer than assumed.",
        s["body"],
    ))
    story.append(Spacer(1, 0.2*cm))

    # Sub-story A: Fusion
    story.append(sec_header("A.  FUSION ENERGY — THE DENSITY BARRIER IS GONE", s, bg=TEAL, accent=GOLD))
    story.append(Spacer(1, 0.15*cm))
    story.append(causal_chain(
        trigger="China's EAST 'artificial sun' achieved stable plasma above the theoretical density "
                "limit — a barrier plasma physicists have tried to break for 40 years.",
        root="The 'density limit' (Greenwald limit) has been the primary engineering wall between "
             "experimental fusion and a sustained commercial reaction. Exceeding it means plasma can "
             "be maintained at conditions closer to the ignition threshold.",
        hidden="China has invested $1B+/year in fusion since 2020. This is not pure science — it is "
               "energy sovereignty strategy. The country that masters fusion sets the terms of the "
               "next energy geopolitical era.",
        benefits="China (strategic energy independence). The whole world (eventually — if open-sourced). "
                 "Bad news for petrostates whose leverage evaporates when fusion reaches grid scale.",
        styles=s,
    ))
    story.append(Spacer(1, 0.15*cm))
    story.append(myth_box(
        myth="Fusion has always been '30 years away' and will always be. It is not a practical near-term energy source.",
        reality="The Greenwald density limit — one of the two main engineering barriers — was just broken. "
                "NIF achieved ignition (energy out > energy in) in 2022. Private companies (Commonwealth "
                "Fusion, Helion) are targeting 2030s commercial reactors. The '30 years away' joke is based "
                "on 1970s physics. The physics has fundamentally changed.",
        styles=s, accent=TEAL,
    ))
    story.append(Spacer(1, 0.25*cm))

    # Sub-story B: CRISPR
    story.append(sec_header("B.  CRISPR WITHOUT CUTS — MEDICINE'S PERMISSION SYSTEM IS BEING REWRITTEN", s, bg=PURPLE, accent=GOLD))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "Traditional CRISPR (Cas9) physically cuts DNA to edit genes — powerful, but risks "
        "off-target cuts that can cause cancer-like mutations. The new approach removes chemical 'tags' "
        "(methyl groups) that act as molecular silencers — no cuts required. Applied to sickle cell disease, "
        "it reactivates fetal haemoglobin, which the body naturally suppresses after birth. "
        "<b>Why this matters beyond sickle cell:</b> the same methyl-tag mechanism controls hundreds of "
        "genes across all human diseases. This is not a sickle cell therapy — it is a new class of "
        "tool for switching the body's gene expression on demand.",
        s["body"],
    ))
    story.append(myth_box(
        myth="Gene editing is dangerous and decades from clinical use. It is the realm of science fiction.",
        reality="The first CRISPR sickle-cell therapy (Casgevy) was FDA-approved in Dec 2023 and is now "
                "in clinical use. This new cut-free method is already in trial stages. The question is "
                "not whether gene editing will be used in medicine — it is being used now. "
                "The question is who will have access to it, at what price.",
        styles=s, accent=PURPLE,
    ))
    story.append(Spacer(1, 0.25*cm))

    # Sub-story C: Solar
    story.append(sec_header("C.  34%-EFFICIENCY SOLAR — THE ARITHMETIC OF ENERGY TRANSITION", s, bg=colors.HexColor("#1A6B3A"), accent=GOLD))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "Standard silicon solar panels convert ~22–24% of sunlight to electricity. "
        "New tandem perovskite-silicon cells hit 34% in lab conditions. "
        "At commercial scale (even at 28–30%), the arithmetic changes radically: "
        "the same rooftop or solar farm produces 25–40% more electricity from identical hardware. "
        "Combined with battery storage cost curves (still falling ~18%/year), this makes solar the "
        "<b>cheapest source of electricity in history</b> — and the gap widens every year.",
        s["body"],
    ))
    story.append(myth_box(
        myth="Renewables are expensive and unreliable. We need fossil fuels for baseline power.",
        reality="New utility-scale solar is already cheaper than any new fossil fuel plant in most of the world. "
                "The 'intermittency' problem is being solved by storage, grid balancing, and geographic "
                "distribution — not by keeping coal plants open. China earned more from renewable energy "
                "exports in 2025 than the US earned from hydrocarbon exports. The transition is "
                "not ideological — it is economic.",
        styles=s, accent=colors.HexColor("#1A6B3A"),
    ))
    story.append(Spacer(1, 0.35*cm))

    # ══ MENTAL MODELS — THE TAKEAWAYS ═════════════════════════════════════════
    story.append(sec_header("SIX MENTAL MODELS TO CARRY FORWARD", s, bg=NAVY, accent=GOLD))
    story.append(Spacer(1, 0.2*cm))

    lessons = [
        (NAVY,   "Military decisions are made weeks before the diplomacy.",
         "Watching diplomatic statements to predict war is like watching a weather forecast "
         "for yesterday. The predictive signal is in military movement, deployment logistics, "
         "and alliance coordination — all of which precede any public announcement by months."),
        (RED,    "Follow the money, not the stated beneficiary.",
         "When a policy claims to help workers but the empirical outcome consistently benefits "
         "capital over labour, the stated intent and the actual mechanism are different. "
         "This is not conspiracy — it is how political economies work. Always ask: "
         "who captures the revenue? Who bears the cost?"),
        (TEAL,   "Exponential systems punish linear thinking.",
         "Fusion, solar, AI, and gene editing are all on exponential curves. "
         "Every year you update your timeline based on last year's news, you are already behind. "
         "The correct mental model: these technologies will arrive faster than your intuition predicts."),
        (AMBER,  "State fragmentation is more dangerous than state adversarialism.",
         "A coherent Iran — even a hostile one — is more stable and predictable than a fragmenting Iran. "
         "The most dangerous outcome of the war is not Iranian retaliation. It is a failed state "
         "in a country of 87 million with a nuclear programme and four autonomy movements."),
        (GREEN,  "Energy independence is the new geopolitics.",
         "Every major power — US, EU, China, India — is reorganising trade, alliances, "
         "and industrial policy around energy security. This is the meta-trend underneath "
         "tariffs, the Iran war, and fusion investment. If you understand one country's energy "
         "position, you understand most of its foreign policy."),
        (PURPLE, "Access — not invention — is the next frontier.",
         "CRISPR therapies exist. Sickle cell can now be cured. The therapy costs $2.2 million. "
         "The scientific breakthrough and the human benefit are separated by an access gap "
         "that only politics and economics can close. Science solves the technical problem; "
         "society decides who benefits."),
    ]
    for i, (color, head, body_text) in enumerate(lessons, 1):
        story.append(lesson_box(i, head, body_text, s, color=color))
        story.append(Spacer(1, 0.15*cm))

    story.append(HRFlowable(width=CONTENT_W, thickness=0.5, color=SILVER, spaceAfter=5))
    story.append(Paragraph(
        "Sources: Wikipedia Portal:Current Events · Atlantic Council · CSIS War with Iran Analysis · "
        "Yale Budget Lab · CBO Tariff Report · Stanford SIEPR · ScienceDaily · WEF Davos 2026 · "
        "UN News · Oxford Economics Iran Conflict 2026",
        s["footer"],
    ))

    return story


# ─── BUILD ────────────────────────────────────────────────────────────────────
def build():
    output_path = os.path.abspath(OUTPUT)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN + 0.5*cm,
        title="Daily World Intelligence Brief — March 6, 2026",
        author="Daily Brief",
        subject="Explain the World — Causal analysis of today's most important events",
        canvasmaker=HF,
    )
    styles = S()
    story = cover(styles) + page2(styles) + page3(styles)
    doc.build(story)
    print(f"✓  PDF saved → {output_path}")


if __name__ == "__main__":
    build()
