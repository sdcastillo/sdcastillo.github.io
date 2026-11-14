#!/usr/bin/env python3
"""
Generate the Sam Castle (Predictive AI) 16:9 PowerPoint Template Deck (.pptx).

Outputs:
  /cursor/stores/bc-622bfb9f-f257-4fe1-bb55-ec4adf87cbba/docs/castle-template-deck.pptx
"""

from __future__ import annotations

import io
import os
from pathlib import Path

import numpy as np
from PIL import Image
from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
STORE_ROOT = Path("/cursor/stores/bc-622bfb9f-f257-4fe1-bb55-ec4adf87cbba")
BRAND_DIR = STORE_ROOT / "internal" / "castle-brand"
OUTPUT_PPTX = STORE_ROOT / "docs" / "castle-template-deck.pptx"

ROOK_NAVY_GOLD_PATH = BRAND_DIR / "rook_logo_navy_gold.png"
SAM_HEADSHOT_PATH = BRAND_DIR / "sam_headshot_circle.png"


# ---------------------------------------------------------------------------
# Brand Tokens
# ---------------------------------------------------------------------------
NAVY_PRIMARY = RGBColor(0x0B, 0x1F, 0x3A)   # #0B1F3A
NAVY_MID = RGBColor(0x16, 0x33, 0x54)       # #163354
NAVY_DEEP = RGBColor(0x08, 0x15, 0x26)      # #081526 (scrim / dark card)
NAVY_BORDER = RGBColor(0x27, 0x49, 0x72)    # #274972 (subtle dark border)
GOLD = RGBColor(0xD4, 0xAF, 0x37)           # #D4AF37
GOLD_DARK = RGBColor(0x8C, 0x6B, 0x14)      # #8C6B14 (rook outline / light-bg gold)
MONO_BLACK = RGBColor(0x11, 0x11, 0x11)     # #111111
CHARCOAL = RGBColor(0x2A, 0x2A, 0x2A)       # #2A2A2A
MUTED_SLATE = RGBColor(0x52, 0x60, 0x71)    # #526071
OFF_WHITE = RGBColor(0xF7, 0xF7, 0xF7)      # #F7F7F7
WHITE = RGBColor(0xFF, 0xFF, 0xFF)          # #FFFFFF
CARD_BORDER = RGBColor(0xD5, 0xDC, 0xE6)    # #D5DCE6
ROW_ALT = RGBColor(0xF7, 0xF7, 0xF7)        # #F7F7F7
LIGHT_MUTED = RGBColor(0xCB, 0xD5, 0xE1)    # #CBD5E1 (secondary text on dark)

FONT_FAMILY = "Liberation Sans"

SLIDE_W = Inches(13.333333)
SLIDE_H = Inches(7.5)

WEBSITE_TEXT = "www.PredictiveInsightsAI.com"
DATE_TEXT = "November 14, 2026"


# ---------------------------------------------------------------------------
# Image Helpers
# ---------------------------------------------------------------------------
def extract_rook_transparent_bytes(scale: int = 3) -> bytes:
    """
    Extract the exact geometric rook silhouette from rook_logo_navy_gold.png
    with a fully transparent background, scaled cleanly using nearest-neighbor
    so all orthogonal edges remain razor-sharp.
    """
    im = Image.open(ROOK_NAVY_GOLD_PATH).convert("RGBA")
    arr = np.array(im)

    # Crop inside outer border (known rook bounds: x 203..596, y 125..694)
    # Add small 4px transparent padding around the rook
    crop = arr[121:699, 199:601].copy()

    # Keep gold fill (#D4AF37) and dark gold outline (#8C6B14); make navy bg transparent
    is_gold_fill = (crop[:, :, 0] == 212) & (crop[:, :, 1] == 175) & (crop[:, :, 2] == 55)
    is_gold_edge = (crop[:, :, 0] == 140) & (crop[:, :, 1] == 107) & (crop[:, :, 2] == 20)
    keep = is_gold_fill | is_gold_edge

    crop[~keep] = [0, 0, 0, 0]
    out = Image.fromarray(crop, mode="RGBA")
    if scale > 1:
        out = out.resize((out.width * scale, out.height * scale), Image.Resampling.NEAREST)

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    return buf.getvalue()


def get_headshot_bytes() -> bytes:
    """Load sam_headshot_circle.png bytes cleanly."""
    with open(SAM_HEADSHOT_PATH, "rb") as f:
        return f.read()


# ---------------------------------------------------------------------------
# XML / Shape Styling Helpers
# ---------------------------------------------------------------------------
def set_shape_alpha(shape, alpha_pct: int) -> None:
    """Set fill transparency on a solid-filled shape (alpha_pct 0..100)."""
    spPr = shape._element.spPr
    solidFill = spPr.find(qn("a:solidFill"))
    if solidFill is None:
        return
    srgb = solidFill.find(qn("a:srgbClr"))
    if srgb is None:
        return
    for existing in srgb.findall(qn("a:alpha")):
        srgb.remove(existing)
    alpha_el = etree.SubElement(srgb, qn("a:alpha"))
    alpha_el.set("val", str(int(alpha_pct * 1000)))


def set_no_line(shape) -> None:
    shape.line.fill.background()


def add_rect(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    fill_color: RGBColor | None = None,
    line_color: RGBColor | None = None,
    line_pt: float = 1.0,
    rounded: bool = False,
    radius: float = 0.04,
    alpha_pct: int | None = None,
):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded:
        shp.adjustments[0] = radius
    if fill_color is not None:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill_color
        if alpha_pct is not None:
            set_shape_alpha(shp, alpha_pct)
    else:
        shp.fill.background()

    if line_color is not None:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(line_pt)
    else:
        set_no_line(shp)
    return shp


def add_textbox(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str = "",
    font_size: float = 14,
    bold: bool = False,
    italic: bool = False,
    color: RGBColor = CHARCOAL,
    align: PP_ALIGN = PP_ALIGN.LEFT,
    valign: MSO_ANCHOR = MSO_ANCHOR.TOP,
    line_spacing: float = 1.15,
    margin_lr: float = 0.04,
    margin_tb: float = 0.02,
):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(margin_lr)
    tf.margin_right = Inches(margin_lr)
    tf.margin_top = Inches(margin_tb)
    tf.margin_bottom = Inches(margin_tb)

    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    run.font.name = FONT_FAMILY
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return tb


def add_paragraph(
    tf,
    text: str,
    font_size: float = 12,
    bold: bool = False,
    color: RGBColor = CHARCOAL,
    align: PP_ALIGN = PP_ALIGN.LEFT,
    space_before: float = 0,
    space_after: float = 4,
    line_spacing: float = 1.18,
):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    run.font.name = FONT_FAMILY
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p


# ---------------------------------------------------------------------------
# Shared Brand Chrome (Chess Grid, Light Header + Corner Badge, Footer)
# ---------------------------------------------------------------------------
def add_chess_grid_background(slide, cols: int = 16, rows: int = 9) -> None:
    """
    Fill slide background with primary navy (#0B1F3A) and overlay alternating
    mid-navy (#163354) squares in a 16x9 grid matching channel_banner_draft.png.
    """
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = NAVY_PRIMARY

    sq_w = 13.333333 / cols
    sq_h = 7.5 / rows
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 1:
                add_rect(
                    slide,
                    x=c * sq_w,
                    y=r * sq_h,
                    w=sq_w + 0.004,
                    h=sq_h + 0.004,
                    fill_color=NAVY_MID,
                    line_color=None,
                )


def add_light_slide_chrome(
    slide,
    eyebrow: str,
    title: str,
    rook_bytes: bytes,
) -> None:
    """
    Standard off-white content slide canvas with top navy+gold accent bar,
    clean eyebrow + title, and top-right navy/gold corner rook badge.
    """
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = OFF_WHITE

    # Top full-bleed navy bar + thin gold underline
    add_rect(slide, 0.0, 0.0, 13.333333, 0.08, fill_color=NAVY_PRIMARY)
    add_rect(slide, 0.0, 0.08, 13.333333, 0.03, fill_color=GOLD)

    # Left accent pip next to header
    add_rect(slide, 0.65, 0.28, 0.07, 0.68, fill_color=GOLD)

    # Eyebrow + Slide Title
    add_textbox(
        slide,
        x=0.84,
        y=0.23,
        w=10.5,
        h=0.26,
        text=eyebrow.upper(),
        font_size=10.5,
        bold=True,
        color=GOLD_DARK,
        margin_lr=0.0,
        margin_tb=0.0,
    )
    add_textbox(
        slide,
        x=0.84,
        y=0.47,
        w=10.8,
        h=0.52,
        text=title,
        font_size=26,
        bold=True,
        color=NAVY_PRIMARY,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Subtle header bottom rule
    add_rect(slide, 0.65, 1.07, 12.03, 0.015, fill_color=CARD_BORDER)

    # Top-right corner rook badge
    badge_x, badge_y, badge_s = 12.06, 0.25, 0.64
    add_rect(
        slide,
        badge_x,
        badge_y,
        badge_s,
        badge_s,
        fill_color=NAVY_PRIMARY,
        line_color=GOLD,
        line_pt=1.5,
        rounded=True,
        radius=0.12,
    )
    # Rook aspect ratio ~ 402/578 = 0.6955
    rook_h = 0.46
    rook_w = rook_h * (402.0 / 578.0)
    slide.shapes.add_picture(
        io.BytesIO(rook_bytes),
        Inches(badge_x + (badge_s - rook_w) / 2.0),
        Inches(badge_y + (badge_s - rook_h) / 2.0),
        height=Inches(rook_h),
    )


def add_footer(slide, slide_num: int, dark: bool) -> None:
    """
    Consistent footer across all slides:
      Left:  www.PredictiveInsightsAI.com
      Right: November 14, 2026 (editable standalone text box)  |  0X
    """
    rule_color = NAVY_BORDER if dark else CARD_BORDER
    text_color = LIGHT_MUTED if dark else CHARCOAL
    num_color = GOLD if dark else NAVY_PRIMARY

    add_rect(slide, 0.65, 7.00, 12.03, 0.012, fill_color=rule_color)

    # Left: website
    add_textbox(
        slide,
        x=0.65,
        y=7.07,
        w=4.8,
        h=0.28,
        text=WEBSITE_TEXT,
        font_size=10,
        bold=False,
        color=text_color,
        align=PP_ALIGN.LEFT,
        valign=MSO_ANCHOR.MIDDLE,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Right: editable date text element
    add_textbox(
        slide,
        x=9.10,
        y=7.07,
        w=2.92,
        h=0.28,
        text=DATE_TEXT,
        font_size=10,
        bold=False,
        color=text_color,
        align=PP_ALIGN.RIGHT,
        valign=MSO_ANCHOR.MIDDLE,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Gold separator pip
    add_rect(slide, 12.14, 7.12, 0.025, 0.18, fill_color=GOLD)

    # Slide number
    add_textbox(
        slide,
        x=12.24,
        y=7.07,
        w=0.44,
        h=0.28,
        text=f"{slide_num:02d}",
        font_size=10.5,
        bold=True,
        color=num_color,
        align=PP_ALIGN.RIGHT,
        valign=MSO_ANCHOR.MIDDLE,
        margin_lr=0.0,
        margin_tb=0.0,
    )


# ---------------------------------------------------------------------------
# Slide 1: Cover / Title Slide
# ---------------------------------------------------------------------------
def build_slide_01_cover(prs: Presentation, rook_bytes: bytes) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chess_grid_background(slide)

    # Central dark scrim panel echoing channel_banner_draft.png safe zone
    panel_x, panel_y, panel_w, panel_h = 0.95, 1.50, 11.43, 4.40
    add_rect(
        slide,
        panel_x,
        panel_y,
        panel_w,
        panel_h,
        fill_color=NAVY_DEEP,
        line_color=NAVY_BORDER,
        line_pt=1.25,
        alpha_pct=84,
    )
    # Left gold vertical accent bar on the hero panel
    add_rect(slide, panel_x, panel_y, 0.10, panel_h, fill_color=GOLD)

    # Geometric gold rook mark on left side of hero lockup
    rook_h = 2.75
    rook_w = rook_h * (402.0 / 578.0)
    slide.shapes.add_picture(
        io.BytesIO(rook_bytes),
        Inches(1.65),
        Inches(panel_y + (panel_h - rook_h) / 2.0),
        height=Inches(rook_h),
    )

    # Right side lockup: Eyebrow, Gold Title, Gold Underline Bar, White Subtitle, Brand Line
    tx = 4.10
    tw = 7.75

    add_textbox(
        slide,
        x=tx,
        y=1.90,
        w=tw,
        h=0.28,
        text="PRESENTATION TEMPLATE  |  STRATEGIC BRIEFING",
        font_size=11,
        bold=True,
        color=LIGHT_MUTED,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    add_textbox(
        slide,
        x=tx,
        y=2.24,
        w=tw,
        h=1.24,
        text="Executive Presentation Title",
        font_size=38,
        bold=True,
        color=GOLD,
        valign=MSO_ANCHOR.BOTTOM,
        line_spacing=1.10,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Gold underline bar directly under title (echoing channel_banner_draft.png)
    add_rect(slide, tx, 3.66, 2.35, 0.065, fill_color=GOLD)

    # White subtitle
    add_textbox(
        slide,
        x=tx,
        y=3.90,
        w=tw,
        h=0.78,
        text="Actionable Intelligence, Predictive Modeling & Executive Strategy",
        font_size=20,
        bold=True,
        color=OFF_WHITE,
        line_spacing=1.2,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Brand attribution line: Sam Castle | Predictive AI
    add_textbox(
        slide,
        x=tx,
        y=4.92,
        w=tw,
        h=0.40,
        text="Sam Castle | Predictive AI",
        font_size=15,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    add_footer(slide, slide_num=1, dark=True)


# ---------------------------------------------------------------------------
# Slide 2: Section Divider / Agenda Slide
# ---------------------------------------------------------------------------
def build_slide_02_agenda(prs: Presentation, rook_bytes: bytes) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chess_grid_background(slide)

    # Left dark architectural panel for section title
    add_rect(
        slide,
        0.65,
        0.75,
        4.45,
        5.85,
        fill_color=NAVY_DEEP,
        line_color=NAVY_BORDER,
        line_pt=1.0,
        alpha_pct=88,
    )
    add_rect(slide, 0.65, 0.75, 4.45, 0.08, fill_color=GOLD)

    # Small gold rook mark inside top of left panel
    slide.shapes.add_picture(
        io.BytesIO(rook_bytes),
        Inches(1.02),
        Inches(1.15),
        height=Inches(0.68),
    )

    # Bold gold section number
    add_textbox(
        slide,
        x=1.00,
        y=1.92,
        w=3.75,
        h=0.98,
        text="01",
        font_size=64,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    add_textbox(
        slide,
        x=1.00,
        y=3.14,
        w=3.75,
        h=0.28,
        text="SECTION DIVIDER & AGENDA",
        font_size=11,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    add_textbox(
        slide,
        x=1.00,
        y=3.48,
        w=3.75,
        h=1.05,
        text="Agenda &\nKey Focus Areas",
        font_size=30,
        bold=True,
        color=OFF_WHITE,
        line_spacing=1.12,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    add_rect(slide, 1.00, 4.70, 1.55, 0.055, fill_color=GOLD)

    add_textbox(
        slide,
        x=1.00,
        y=4.94,
        w=3.75,
        h=1.20,
        text="Use this layout to open the deck with a clear roadmap or introduce a major section transition.",
        font_size=13.5,
        bold=False,
        color=LIGHT_MUTED,
        line_spacing=1.3,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Right dark scrim panel for clean 5-item agenda list
    add_rect(
        slide,
        5.40,
        0.75,
        7.28,
        5.85,
        fill_color=NAVY_DEEP,
        line_color=NAVY_BORDER,
        line_pt=1.0,
        alpha_pct=88,
    )

    agenda_items = [
        ("01", "Executive Summary & Headline Metrics", "Core findings, financial impact, and strategic direction."),
        ("02", "Comparative & Scenario Analysis", "Side-by-side trade-offs across baseline and target states."),
        ("03", "Quantitative Performance & Trends", "Empirical model trajectory against benchmark targets."),
        ("04", "Financial Matrix & Sensitivity", "Structured unit economics and scenario sensitivity table."),
        ("05", "Implementation Roadmap & Next Steps", "Four-phase execution plan, owners, and key milestones."),
    ]

    start_y = 1.05
    row_h = 1.06
    for idx, (num, heading, desc) in enumerate(agenda_items):
        ry = start_y + idx * row_h

        # Gold badge pill for number
        add_rect(
            slide,
            5.78,
            ry + 0.08,
            0.56,
            0.44,
            fill_color=GOLD,
            rounded=True,
            radius=0.16,
        )
        add_textbox(
            slide,
            x=5.78,
            y=ry + 0.08,
            w=0.56,
            h=0.44,
            text=num,
            font_size=14,
            bold=True,
            color=NAVY_PRIMARY,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        # Heading + subtitle
        add_textbox(
            slide,
            x=6.52,
            y=ry + 0.02,
            w=5.82,
            h=0.34,
            text=heading,
            font_size=16,
            bold=True,
            color=OFF_WHITE,
            margin_lr=0.0,
            margin_tb=0.0,
        )
        add_textbox(
            slide,
            x=6.52,
            y=ry + 0.37,
            w=5.82,
            h=0.36,
            text=desc,
            font_size=12,
            bold=False,
            color=LIGHT_MUTED,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        if idx < len(agenda_items) - 1:
            add_rect(slide, 5.78, ry + 0.88, 6.55, 0.012, fill_color=NAVY_BORDER)

    add_footer(slide, slide_num=2, dark=True)


# ---------------------------------------------------------------------------
# Slide 3: Executive Summary / Key Takeaways
# ---------------------------------------------------------------------------
def build_slide_03_exec_summary(prs: Presentation, rook_bytes: bytes) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_light_slide_chrome(
        slide,
        eyebrow="Executive Summary",
        title="Key Takeaways & Strategic Impact",
        rook_bytes=rook_bytes,
    )

    # 4 structured KPI / insight cards
    cards = [
        (
            "METRIC 01",
            "+$4.2M",
            "Projected Annual Value",
            "Quantified revenue lift or cost reduction captured within the first 12 months of rollout.",
        ),
        (
            "METRIC 02",
            "3.4x",
            "Return on Investment",
            "Expected capital efficiency ratio relative to baseline manual workflows and legacy tooling.",
        ),
        (
            "METRIC 03",
            "94.8%",
            "Forecast Accuracy",
            "Validated out-of-sample model precision across core operating segments and horizons.",
        ),
        (
            "METRIC 04",
            "16 wks",
            "Time to Production",
            "End-to-end delivery from data ingestion and model calibration to live decision support.",
        ),
    ]

    margin_x = 0.65
    gap = 0.24
    card_w = (12.03 - 3 * gap) / 4.0  # ~2.8275"
    card_y = 1.32
    card_h = 3.85

    for idx, (tag, kpi, label, body) in enumerate(cards):
        cx = margin_x + idx * (card_w + gap)
        add_rect(
            slide,
            cx,
            card_y,
            card_w,
            card_h,
            fill_color=WHITE,
            line_color=CARD_BORDER,
            line_pt=1.0,
        )
        # Gold top accent bar
        add_rect(slide, cx, card_y, card_w, 0.08, fill_color=GOLD)

        # Tag pill
        add_textbox(
            slide,
            x=cx + 0.22,
            y=card_y + 0.26,
            w=card_w - 0.44,
            h=0.25,
            text=tag,
            font_size=10,
            bold=True,
            color=GOLD_DARK,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        # Large KPI value
        add_textbox(
            slide,
            x=cx + 0.22,
            y=card_y + 0.62,
            w=card_w - 0.44,
            h=0.68,
            text=kpi,
            font_size=36,
            bold=True,
            color=NAVY_PRIMARY,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        # KPI title
        add_textbox(
            slide,
            x=cx + 0.22,
            y=card_y + 1.42,
            w=card_w - 0.44,
            h=0.45,
            text=label,
            font_size=14,
            bold=True,
            color=NAVY_MID,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        # Divider inside card
        add_rect(slide, cx + 0.22, card_y + 1.96, card_w - 0.44, 0.015, fill_color=CARD_BORDER)

        # Body insight text
        add_textbox(
            slide,
            x=cx + 0.22,
            y=card_y + 2.12,
            w=card_w - 0.44,
            h=1.45,
            text=body,
            font_size=12,
            bold=False,
            color=CHARCOAL,
            line_spacing=1.28,
            margin_lr=0.0,
            margin_tb=0.0,
        )

    # Bottom synthesis callout bar
    syn_y = 5.42
    syn_h = 1.28
    add_rect(slide, 0.65, syn_y, 12.03, syn_h, fill_color=NAVY_PRIMARY)
    add_rect(slide, 0.65, syn_y, 0.10, syn_h, fill_color=GOLD)

    add_textbox(
        slide,
        x=0.95,
        y=syn_y + 0.16,
        w=11.45,
        h=0.28,
        text="EXECUTIVE SYNTHESIS",
        font_size=10.5,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )
    add_textbox(
        slide,
        x=0.95,
        y=syn_y + 0.46,
        w=11.45,
        h=0.68,
        text=(
            "Consolidating fragmented signals into a unified predictive decision layer unlocks "
            "measurable margin expansion while preserving strict governance and human-in-the-loop oversight."
        ),
        font_size=13.5,
        bold=False,
        color=OFF_WHITE,
        line_spacing=1.25,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    add_footer(slide, slide_num=3, dark=False)


# ---------------------------------------------------------------------------
# Slide 4: Two-Column Comparison / Split Analysis
# ---------------------------------------------------------------------------
def build_slide_04_comparison(prs: Presentation, rook_bytes: bytes) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_light_slide_chrome(
        slide,
        eyebrow="Comparative Analysis",
        title="Two-Column Strategic Comparison",
        rook_bytes=rook_bytes,
    )

    col_w = 5.84
    col_gap = 0.35
    col_y = 1.32
    col_h = 5.42
    header_h = 0.86

    columns = [
        {
            "x": 0.65,
            "header_bg": NAVY_PRIMARY,
            "badge_text": "OPTION A",
            "title": "Current Baseline Architecture",
            "items": [
                ("Data Cadence", "Batch weekly extracts across siloed reporting tables with manual reconciliation."),
                ("Forecasting Method", "Static spreadsheet heuristics and trailing moving averages with limited sensitivity."),
                ("Decision Latency", "5-7 business days from signal detection to executive review and operational action."),
                ("Risk & Governance", "Ad-hoc version control and inconsistent audit trails across regional teams."),
            ],
        },
        {
            "x": 0.65 + col_w + col_gap,
            "header_bg": NAVY_MID,
            "badge_text": "OPTION B",
            "title": "Recommended Predictive AI State",
            "items": [
                ("Data Cadence", "Automated daily pipelines unifying operational, financial, and external market feeds."),
                ("Forecasting Method", "Calibrated probabilistic models with scenario bands and feature attribution."),
                ("Decision Latency", "Real-time exception alerts and sub-hour refresh for priority operational levers."),
                ("Risk & Governance", "Versioned model registry, automated drift checks, and auditable decision logs."),
            ],
        },
    ]

    for col in columns:
        cx = col["x"]
        # Card background
        add_rect(
            slide,
            cx,
            col_y,
            col_w,
            col_h,
            fill_color=WHITE,
            line_color=CARD_BORDER,
            line_pt=1.0,
        )
        # Header band
        add_rect(slide, cx, col_y, col_w, header_h, fill_color=col["header_bg"])
        # Gold bottom accent rule under header
        add_rect(slide, cx, col_y + header_h, col_w, 0.055, fill_color=GOLD)

        # Option tag + column title
        add_textbox(
            slide,
            x=cx + 0.28,
            y=col_y + 0.12,
            w=col_w - 0.56,
            h=0.22,
            text=col["badge_text"],
            font_size=10,
            bold=True,
            color=GOLD,
            margin_lr=0.0,
            margin_tb=0.0,
        )
        add_textbox(
            slide,
            x=cx + 0.28,
            y=col_y + 0.36,
            w=col_w - 0.56,
            h=0.40,
            text=col["title"],
            font_size=18,
            bold=True,
            color=WHITE,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        # 4 structured bullet rows
        row_start_y = col_y + header_h + 0.26
        row_step = 1.06
        for r_idx, (subhead, detail) in enumerate(col["items"]):
            ry = row_start_y + r_idx * row_step

            # Gold square marker
            add_rect(slide, cx + 0.28, ry + 0.06, 0.14, 0.14, fill_color=GOLD)

            add_textbox(
                slide,
                x=cx + 0.54,
                y=ry,
                w=col_w - 0.82,
                h=0.28,
                text=subhead,
                font_size=13.5,
                bold=True,
                color=NAVY_PRIMARY,
                margin_lr=0.0,
                margin_tb=0.0,
            )
            add_textbox(
                slide,
                x=cx + 0.54,
                y=ry + 0.28,
                w=col_w - 0.82,
                h=0.58,
                text=detail,
                font_size=11.5,
                bold=False,
                color=CHARCOAL,
                line_spacing=1.22,
                margin_lr=0.0,
                margin_tb=0.0,
            )

            if r_idx < len(col["items"]) - 1:
                add_rect(
                    slide,
                    cx + 0.28,
                    ry + 0.94,
                    col_w - 0.56,
                    0.012,
                    fill_color=CARD_BORDER,
                )

    add_footer(slide, slide_num=4, dark=False)


# ---------------------------------------------------------------------------
# Slide 5: Data & Chart Layout
# ---------------------------------------------------------------------------
def build_slide_05_chart(prs: Presentation, rook_bytes: bytes) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_light_slide_chrome(
        slide,
        eyebrow="Quantitative Analysis",
        title="Data & Forecast Performance Layout",
        rook_bytes=rook_bytes,
    )

    # Left chart container card
    chart_card_x, chart_card_y, chart_card_w, chart_card_h = 0.65, 1.32, 7.65, 5.42
    add_rect(
        slide,
        chart_card_x,
        chart_card_y,
        chart_card_w,
        chart_card_h,
        fill_color=WHITE,
        line_color=CARD_BORDER,
        line_pt=1.0,
    )
    add_rect(slide, chart_card_x, chart_card_y, chart_card_w, 0.06, fill_color=NAVY_PRIMARY)

    add_textbox(
        slide,
        x=chart_card_x + 0.26,
        y=chart_card_y + 0.18,
        w=7.10,
        h=0.30,
        text="Quarterly Index Performance ($M, Editable Native Chart)",
        font_size=14,
        bold=True,
        color=NAVY_PRIMARY,
        margin_lr=0.0,
        margin_tb=0.0,
    )
    add_textbox(
        slide,
        x=chart_card_x + 0.26,
        y=chart_card_y + 0.48,
        w=7.10,
        h=0.24,
        text="Baseline vs. Mid-Tier Optimization vs. Predictive AI Target",
        font_size=10.5,
        bold=False,
        color=MUTED_SLATE,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Native editable PowerPoint clustered column chart
    chart_data = CategoryChartData()
    chart_data.categories = ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"]
    chart_data.add_series("Baseline", (18.4, 19.6, 21.0, 22.3))
    chart_data.add_series("Current Forecast", (20.1, 22.8, 25.4, 28.1))
    chart_data.add_series("Predictive AI Target", (22.5, 26.4, 31.2, 36.8))

    chart_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(chart_card_x + 0.22),
        Inches(chart_card_y + 0.82),
        Inches(chart_card_w - 0.44),
        Inches(chart_card_h - 1.02),
        chart_data,
    )
    chart = chart_frame.chart
    chart.has_title = False
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False
    chart.legend.font.name = FONT_FAMILY
    chart.legend.font.size = Pt(10.5)
    chart.legend.font.color.rgb = CHARCOAL

    plot = chart.plots[0]
    plot.gap_width = 110
    plot.overlap = -15

    # Series brand colors: #2A2A2A (charcoal baseline), #163354 (mid-navy), #D4AF37 (gold target)
    series_colors = [CHARCOAL, NAVY_MID, GOLD]
    for s_idx, col in enumerate(series_colors):
        series = plot.series[s_idx]
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = col
        series.format.line.fill.background()

    # Axis styling
    val_axis = chart.value_axis
    val_axis.has_major_gridlines = True
    val_axis.major_gridlines.format.line.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
    val_axis.major_gridlines.format.line.width = Pt(0.75)
    val_axis.tick_labels.font.name = FONT_FAMILY
    val_axis.tick_labels.font.size = Pt(10)
    val_axis.tick_labels.font.color.rgb = CHARCOAL
    val_axis.minimum_scale = 0
    val_axis.maximum_scale = 40

    cat_axis = chart.category_axis
    cat_axis.tick_labels.font.name = FONT_FAMILY
    cat_axis.tick_labels.font.size = Pt(10.5)
    cat_axis.tick_labels.font.bold = True
    cat_axis.tick_labels.font.color.rgb = NAVY_PRIMARY

    # Right-hand insight callout panel
    rx = 8.58
    rw = 4.10

    # Top dark navy hero insight card
    add_rect(slide, rx, 1.32, rw, 1.86, fill_color=NAVY_PRIMARY)
    add_rect(slide, rx, 1.32, rw, 0.08, fill_color=GOLD)

    add_textbox(
        slide,
        x=rx + 0.25,
        y=1.54,
        w=rw - 0.50,
        h=0.24,
        text="HEADLINE OUTCOME",
        font_size=10,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )
    add_textbox(
        slide,
        x=rx + 0.25,
        y=1.82,
        w=rw - 0.50,
        h=0.58,
        text="+65% Uplift by Q4",
        font_size=26,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )
    add_textbox(
        slide,
        x=rx + 0.25,
        y=2.42,
        w=rw - 0.50,
        h=0.62,
        text="Predictive AI target outperforms baseline trajectory across every quarter as model calibration compounds.",
        font_size=11.5,
        bold=False,
        color=OFF_WHITE,
        line_spacing=1.22,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Two light analytical callout cards below
    callouts = [
        (
            "01  |  PRIMARY GROWTH DRIVER",
            "Dynamic demand elasticity scoring captures high-intent segments 3 weeks ahead of trailing indicators.",
        ),
        (
            "02  |  DOWNSIDE PROTECTION",
            "Automated variance thresholds flag underperforming cohorts early, cutting wasted spend by 22%.",
        ),
    ]
    for idx, (ctitle, cbody) in enumerate(callouts):
        cy = 3.38 + idx * 1.78
        ch = 1.58
        add_rect(
            slide,
            rx,
            cy,
            rw,
            ch,
            fill_color=WHITE,
            line_color=CARD_BORDER,
            line_pt=1.0,
        )
        add_rect(slide, rx, cy, 0.08, ch, fill_color=GOLD)

        add_textbox(
            slide,
            x=rx + 0.24,
            y=cy + 0.20,
            w=rw - 0.44,
            h=0.28,
            text=ctitle,
            font_size=11.5,
            bold=True,
            color=NAVY_PRIMARY,
            margin_lr=0.0,
            margin_tb=0.0,
        )
        add_textbox(
            slide,
            x=rx + 0.24,
            y=cy + 0.54,
            w=rw - 0.44,
            h=0.88,
            text=cbody,
            font_size=11.5,
            bold=False,
            color=CHARCOAL,
            line_spacing=1.25,
            margin_lr=0.0,
            margin_tb=0.0,
        )

    add_footer(slide, slide_num=5, dark=False)


# ---------------------------------------------------------------------------
# Slide 6: Structured Table / Financial Matrix
# ---------------------------------------------------------------------------
def build_slide_06_table(prs: Presentation, rook_bytes: bytes) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_light_slide_chrome(
        slide,
        eyebrow="Financial Matrix",
        title="Structured Performance & Scenario Table",
        rook_bytes=rook_bytes,
    )

    tbl_x, tbl_y, tbl_w, tbl_h = 0.65, 1.32, 12.03, 4.35
    rows_data = [
        ["Metric / Line Item", "FY25 Actual", "FY26 Base", "FY26 Predictive", "YoY Delta", "Confidence"],
        ["Gross Recurring Revenue ($M)", "$42.8", "$49.2", "$58.6", "+36.9%", "High (95%)"],
        ["Gross Margin (%)", "71.4%", "73.0%", "76.8%", "+540 bps", "High (92%)"],
        ["Customer Acquisition Cost ($)", "$1,420", "$1,310", "$1,085", "-23.6%", "Medium-High"],
        ["Net Dollar Retention (%)", "112%", "116%", "124%", "+12 pts", "High (94%)"],
        ["Operating Leverage Ratio", "1.18x", "1.34x", "1.62x", "+0.44x", "Medium-High"],
        ["Free Cash Flow Margin (%)", "14.2%", "18.5%", "24.1%", "+990 bps", "High (90%)"],
        ["Total Net Impact ($M)", "$6.1", "$9.1", "$14.1", "+131.1%", "Validated"],
    ]

    n_rows = len(rows_data)
    n_cols = len(rows_data[0])
    table_shape = slide.shapes.add_table(
        n_rows, n_cols, Inches(tbl_x), Inches(tbl_y), Inches(tbl_w), Inches(tbl_h)
    )
    table = table_shape.table
    table.first_row = True
    table.horz_banding = False

    col_widths = [3.63, 1.55, 1.55, 1.75, 1.60, 1.95]
    for c_idx, cw in enumerate(col_widths):
        table.columns[c_idx].width = Inches(cw)

    header_h = 0.56
    body_h = (tbl_h - header_h) / (n_rows - 1)
    table.rows[0].height = Inches(header_h)
    for r_idx in range(1, n_rows):
        table.rows[r_idx].height = Inches(body_h)

    for r_idx, row_vals in enumerate(rows_data):
        is_header = r_idx == 0
        is_total = r_idx == n_rows - 1
        for c_idx, val in enumerate(row_vals):
            cell = table.cell(r_idx, c_idx)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.16)
            cell.margin_right = Inches(0.16)
            cell.margin_top = Inches(0.06)
            cell.margin_bottom = Inches(0.06)

            cell.fill.solid()
            if is_header:
                cell.fill.fore_color.rgb = NAVY_PRIMARY
            elif is_total:
                cell.fill.fore_color.rgb = NAVY_MID
            elif r_idx % 2 == 1:
                cell.fill.fore_color.rgb = WHITE
            else:
                cell.fill.fore_color.rgb = ROW_ALT

            p = cell.text_frame.paragraphs[0]
            if c_idx == 0:
                p.alignment = PP_ALIGN.LEFT
            elif c_idx == n_cols - 1:
                p.alignment = PP_ALIGN.CENTER
            else:
                p.alignment = PP_ALIGN.RIGHT

            run = p.add_run()
            run.text = val
            run.font.name = FONT_FAMILY
            run.font.size = Pt(12 if is_header or is_total else 11.5)
            run.font.bold = is_header or is_total or (c_idx == 0)

            if is_header:
                run.font.color.rgb = WHITE
            elif is_total:
                run.font.color.rgb = GOLD if c_idx in (3, 4) else WHITE
            elif c_idx == 4:
                run.font.color.rgb = NAVY_PRIMARY
            else:
                run.font.color.rgb = CHARCOAL

    # Gold accent rule right below header row (always crisp in PowerPoint & LibreOffice)
    add_rect(slide, tbl_x, tbl_y + header_h, tbl_w, 0.05, fill_color=GOLD)

    # Bottom 3 assumption / footnote cards
    notes = [
        ("MODEL ASSUMPTIONS", "Baseline assumes historical 14% organic growth without automated scoring."),
        ("SCENARIO SENSITIVITY", "Predictive case reflects conservative 65% adoption across Tier-1 accounts."),
        ("DATA GOVERNANCE", "All figures reconciled against audited ledger snapshots as of Q3 close."),
    ]
    note_gap = 0.24
    note_w = (12.03 - 2 * note_gap) / 3.0
    note_y = 5.88
    note_h = 0.88
    for idx, (ntitle, nbody) in enumerate(notes):
        nx = 0.65 + idx * (note_w + note_gap)
        add_rect(
            slide,
            nx,
            note_y,
            note_w,
            note_h,
            fill_color=WHITE,
            line_color=CARD_BORDER,
            line_pt=1.0,
        )
        add_rect(slide, nx, note_y, 0.07, note_h, fill_color=GOLD)
        add_textbox(
            slide,
            x=nx + 0.20,
            y=note_y + 0.10,
            w=note_w - 0.34,
            h=0.22,
            text=ntitle,
            font_size=9.5,
            bold=True,
            color=NAVY_PRIMARY,
            margin_lr=0.0,
            margin_tb=0.0,
        )
        add_textbox(
            slide,
            x=nx + 0.20,
            y=note_y + 0.34,
            w=note_w - 0.34,
            h=0.46,
            text=nbody,
            font_size=10.5,
            bold=False,
            color=CHARCOAL,
            line_spacing=1.18,
            margin_lr=0.0,
            margin_tb=0.0,
        )

    add_footer(slide, slide_num=6, dark=False)


# ---------------------------------------------------------------------------
# Slide 7: Timeline / Roadmap
# ---------------------------------------------------------------------------
def build_slide_07_roadmap(prs: Presentation, rook_bytes: bytes) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_light_slide_chrome(
        slide,
        eyebrow="Execution Roadmap",
        title="Four-Phase Implementation Timeline",
        rook_bytes=rook_bytes,
    )

    phases = [
        {
            "badge": "PHASE 01",
            "window": "Weeks 1 - 4",
            "title": "Discovery & Audit",
            "bullets": [
                "Map core data sources & schemas",
                "Establish KPI baseline benchmarks",
                "Define governance & success criteria",
            ],
            "owner": "Owner: Data Engineering",
        },
        {
            "badge": "PHASE 02",
            "window": "Weeks 5 - 8",
            "title": "Model Prototyping",
            "bullets": [
                "Engineer predictive feature pipeline",
                "Backtest candidate model architectures",
                "Validate lift against holdout cohorts",
            ],
            "owner": "Owner: Applied AI Lead",
        },
        {
            "badge": "PHASE 03",
            "window": "Weeks 9 - 12",
            "title": "Pilot Integration",
            "bullets": [
                "Embed scores into operator workflow",
                "Run shadow-mode decision reviews",
                "Calibrate alert thresholds & SLAs",
            ],
            "owner": "Owner: Product & Ops",
        },
        {
            "badge": "PHASE 04",
            "window": "Weeks 13 - 16",
            "title": "Scale & Monitoring",
            "bullets": [
                "Full rollout across priority segments",
                "Automate drift & accuracy telemetry",
                "Quarterly executive ROI readout",
            ],
            "owner": "Owner: Executive Sponsor",
        },
    ]

    margin_x = 0.65
    gap = 0.25
    col_w = (12.03 - 3 * gap) / 4.0

    # Horizontal gold connector spine behind milestone nodes
    spine_y = 2.22
    first_center = margin_x + col_w / 2.0
    last_center = margin_x + 3 * (col_w + gap) + col_w / 2.0
    add_rect(slide, first_center, spine_y, last_center - first_center, 0.05, fill_color=GOLD)

    for idx, ph in enumerate(phases):
        px = margin_x + idx * (col_w + gap)
        cx = px + col_w / 2.0

        # Gold phase badge pill at top
        badge_w = 1.48
        add_rect(
            slide,
            cx - badge_w / 2.0,
            1.36,
            badge_w,
            0.38,
            fill_color=GOLD,
            rounded=True,
            radius=0.22,
        )
        add_textbox(
            slide,
            x=cx - badge_w / 2.0,
            y=1.36,
            w=badge_w,
            h=0.38,
            text=ph["badge"],
            font_size=11,
            bold=True,
            color=NAVY_PRIMARY,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        # Timeframe label
        add_textbox(
            slide,
            x=px,
            y=1.80,
            w=col_w,
            h=0.26,
            text=ph["window"],
            font_size=11,
            bold=True,
            color=NAVY_MID,
            align=PP_ALIGN.CENTER,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        # Milestone circular node on the spine
        node_d = 0.28
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(cx - node_d / 2.0),
            Inches(spine_y - (node_d - 0.05) / 2.0),
            Inches(node_d),
            Inches(node_d),
        )
        node.fill.solid()
        node.fill.fore_color.rgb = NAVY_PRIMARY
        node.line.color.rgb = GOLD
        node.line.width = Pt(2.25)

        # Navy milestone card
        card_y = 2.58
        card_h = 4.14
        card_bg = NAVY_PRIMARY if idx % 2 == 0 else NAVY_MID
        add_rect(slide, px, card_y, col_w, card_h, fill_color=card_bg)
        add_rect(slide, px, card_y, col_w, 0.08, fill_color=GOLD)

        # Phase title
        add_textbox(
            slide,
            x=px + 0.22,
            y=card_y + 0.24,
            w=col_w - 0.44,
            h=0.62,
            text=ph["title"],
            font_size=16,
            bold=True,
            color=WHITE,
            line_spacing=1.12,
            margin_lr=0.0,
            margin_tb=0.0,
        )

        add_rect(slide, px + 0.22, card_y + 0.94, 0.90, 0.035, fill_color=GOLD)

        # Bullet deliverables
        tb = add_textbox(
            slide,
            x=px + 0.22,
            y=card_y + 1.12,
            w=col_w - 0.44,
            h=2.25,
            text=f"▪  {ph['bullets'][0]}",
            font_size=11.5,
            bold=False,
            color=OFF_WHITE,
            line_spacing=1.22,
            margin_lr=0.0,
            margin_tb=0.0,
        )
        tf = tb.text_frame
        tf.paragraphs[0].space_after = Pt(10)
        for b_text in ph["bullets"][1:]:
            add_paragraph(
                tf,
                text=f"▪  {b_text}",
                font_size=11.5,
                bold=False,
                color=OFF_WHITE,
                space_after=10,
                line_spacing=1.22,
            )

        # Bottom owner strip inside card
        add_rect(
            slide,
            px + 0.16,
            card_y + card_h - 0.56,
            col_w - 0.32,
            0.40,
            fill_color=NAVY_DEEP,
            line_color=NAVY_BORDER,
            line_pt=0.75,
        )
        add_textbox(
            slide,
            x=px + 0.24,
            y=card_y + card_h - 0.56,
            w=col_w - 0.48,
            h=0.40,
            text=ph["owner"],
            font_size=10,
            bold=True,
            color=GOLD,
            valign=MSO_ANCHOR.MIDDLE,
            margin_lr=0.0,
            margin_tb=0.0,
        )

    add_footer(slide, slide_num=7, dark=False)


# ---------------------------------------------------------------------------
# Slide 8: Closing / Speaker Bio Slide
# ---------------------------------------------------------------------------
def build_slide_08_closing(prs: Presentation, rook_bytes: bytes, headshot_bytes: bytes) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_chess_grid_background(slide)

    # Full central dark scrim card
    card_x, card_y, card_w, card_h = 0.85, 0.95, 11.63, 5.65
    add_rect(
        slide,
        card_x,
        card_y,
        card_w,
        card_h,
        fill_color=NAVY_DEEP,
        line_color=NAVY_BORDER,
        line_pt=1.25,
        alpha_pct=88,
    )
    add_rect(slide, card_x, card_y, card_w, 0.08, fill_color=GOLD)

    # Framed circular headshot on the left with crisp gold ring
    photo_d = 3.20
    ring_d = photo_d + 0.16
    ring_x = 1.55
    ring_y = card_y + (card_h - ring_d) / 2.0

    ring = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(ring_x),
        Inches(ring_y),
        Inches(ring_d),
        Inches(ring_d),
    )
    ring.fill.solid()
    ring.fill.fore_color.rgb = GOLD
    set_no_line(ring)

    slide.shapes.add_picture(
        io.BytesIO(headshot_bytes),
        Inches(ring_x + 0.08),
        Inches(ring_y + 0.08),
        width=Inches(photo_d),
        height=Inches(photo_d),
    )

    # Right column: Rook mark + Eyebrow, Sam Castle | Predictive AI, Bio, Contact details
    rx = 5.45
    rw = 6.45

    # Small geometric gold rook mark aligned with eyebrow
    slide.shapes.add_picture(
        io.BytesIO(rook_bytes),
        Inches(rx),
        Inches(1.36),
        height=Inches(0.56),
    )
    add_textbox(
        slide,
        x=rx + 0.54,
        y=1.46,
        w=5.8,
        h=0.34,
        text="THANK YOU  |  SPEAKER & CONTACT",
        font_size=11.5,
        bold=True,
        color=GOLD,
        valign=MSO_ANCHOR.MIDDLE,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Name
    add_textbox(
        slide,
        x=rx,
        y=2.04,
        w=rw,
        h=0.66,
        text="Sam Castle",
        font_size=38,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Gold underline bar (clear separation below name baseline)
    add_rect(slide, rx, 2.84, 2.00, 0.055, fill_color=GOLD)

    # Brand subtitle
    add_textbox(
        slide,
        x=rx,
        y=3.04,
        w=rw,
        h=0.42,
        text="Sam Castle | Predictive AI",
        font_size=20,
        bold=True,
        color=OFF_WHITE,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Speaker Bio Placeholder
    add_textbox(
        slide,
        x=rx,
        y=3.60,
        w=rw,
        h=1.22,
        text=(
            "Founder and principal advisor focused on predictive modeling, applied AI systems, "
            "and executive decision intelligence. Partnering with leadership teams to convert "
            "complex operational data into durable, measurable competitive advantage."
        ),
        font_size=13,
        bold=False,
        color=LIGHT_MUTED,
        line_spacing=1.28,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    # Contact / Date info strip cards
    info_y = 5.04
    info_h = 0.88
    left_info_w = 3.70
    right_info_w = 2.52

    add_rect(
        slide,
        rx,
        info_y,
        left_info_w,
        info_h,
        fill_color=NAVY_MID,
        line_color=NAVY_BORDER,
        line_pt=1.0,
    )
    add_rect(slide, rx, info_y, 0.08, info_h, fill_color=GOLD)
    add_textbox(
        slide,
        x=rx + 0.22,
        y=info_y + 0.14,
        w=left_info_w - 0.34,
        h=0.22,
        text="ONLINE",
        font_size=9.5,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )
    add_textbox(
        slide,
        x=rx + 0.22,
        y=info_y + 0.40,
        w=left_info_w - 0.34,
        h=0.32,
        text=WEBSITE_TEXT,
        font_size=13.5,
        bold=True,
        color=WHITE,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    dx = rx + left_info_w + 0.23
    add_rect(
        slide,
        dx,
        info_y,
        right_info_w,
        info_h,
        fill_color=NAVY_MID,
        line_color=NAVY_BORDER,
        line_pt=1.0,
    )
    add_rect(slide, dx, info_y, 0.08, info_h, fill_color=GOLD)
    add_textbox(
        slide,
        x=dx + 0.22,
        y=info_y + 0.14,
        w=right_info_w - 0.34,
        h=0.22,
        text="DATE",
        font_size=9.5,
        bold=True,
        color=GOLD,
        margin_lr=0.0,
        margin_tb=0.0,
    )
    add_textbox(
        slide,
        x=dx + 0.22,
        y=info_y + 0.40,
        w=right_info_w - 0.34,
        h=0.32,
        text=DATE_TEXT,
        font_size=13.5,
        bold=True,
        color=WHITE,
        margin_lr=0.0,
        margin_tb=0.0,
    )

    add_footer(slide, slide_num=8, dark=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    OUTPUT_PPTX.parent.mkdir(parents=True, exist_ok=True)

    rook_bytes = extract_rook_transparent_bytes(scale=3)
    headshot_bytes = get_headshot_bytes()

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    build_slide_01_cover(prs, rook_bytes)
    build_slide_02_agenda(prs, rook_bytes)
    build_slide_03_exec_summary(prs, rook_bytes)
    build_slide_04_comparison(prs, rook_bytes)
    build_slide_05_chart(prs, rook_bytes)
    build_slide_06_table(prs, rook_bytes)
    build_slide_07_roadmap(prs, rook_bytes)
    build_slide_08_closing(prs, rook_bytes, headshot_bytes)

    prs.save(str(OUTPUT_PPTX))
    print(f"Saved {OUTPUT_PPTX} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
