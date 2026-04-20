#!/usr/bin/env python3
"""Build a 15-slide .pptx presentation for ICU prediction talk."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Colours ──────────────────────────────────────────────────────────────────
DARK_BG   = RGBColor(0x1B, 0x1B, 0x2F)   # deep navy
MED_BG    = RGBColor(0x24, 0x24, 0x3E)   # slightly lighter navy
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT    = RGBColor(0x4E, 0xC9, 0xB0)   # teal green
ACCENT2   = RGBColor(0xE0, 0x5C, 0x5C)   # warm red
LIGHT     = RGBColor(0xCC, 0xCC, 0xCC)   # light grey for body
GOLD      = RGBColor(0xFF, 0xD7, 0x00)   # highlight
SOFT_BLUE = RGBColor(0x6C, 0xA0, 0xDC)   # soft blue

FIGDIR = 'icu_figures'

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

W = prs.slide_width
H = prs.slide_height


# ── Helpers ──────────────────────────────────────────────────────────────────
def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=WHITE, bold=False, alignment=PP_ALIGN.LEFT,
                font_name='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return tf


def add_para(tf, text, font_size=18, color=WHITE, bold=False,
             alignment=PP_ALIGN.LEFT, space_before=Pt(6), font_name='Calibri'):
    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    if space_before:
        p.space_before = space_before
    return p


def add_bullet_slide(slide, left, top, width, height, bullets,
                     font_size=20, color=WHITE, bullet_color=ACCENT,
                     spacing=Pt(10)):
    """Add a textbox with bullet points."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        # Use a coloured bullet character
        run1 = p.add_run()
        run1.text = "●  "
        run1.font.size = Pt(font_size - 4)
        run1.font.color.rgb = bullet_color
        run1.font.name = 'Calibri'
        run2 = p.add_run()
        run2.text = bullet
        run2.font.size = Pt(font_size)
        run2.font.color.rgb = color
        run2.font.name = 'Calibri'
        p.space_before = spacing
    return tf


def add_highlight_box(slide, left, top, width, height, text,
                      fill_color=RGBColor(0x2E, 0x86, 0xAB), text_color=WHITE,
                      font_size=18, bold=True):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = text_color
    p.font.bold = bold
    p.font.name = 'Calibri'
    # vertical centering
    tf.paragraphs[0].space_before = Pt(4)
    return tf


def title_bar(slide, title_text, subtitle_text=None):
    """Add a consistent title bar at top."""
    # Title
    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(11), Inches(0.8),
                title_text, font_size=36, color=WHITE, bold=True)
    # Thin accent line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                  Inches(0.8), Inches(1.05), Inches(2.5), Pt(3))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT
    line.line.fill.background()
    if subtitle_text:
        add_textbox(slide, Inches(0.8), Inches(1.15), Inches(11), Inches(0.6),
                    subtitle_text, font_size=18, color=LIGHT, bold=False)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
set_slide_bg(slide, DARK_BG)

add_textbox(slide, Inches(1.5), Inches(1.5), Inches(10), Inches(1.2),
            "Will They Go to ICU?",
            font_size=48, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(1.5), Inches(2.8), Inches(10), Inches(1.0),
            "Predicting Unplanned ICU Admission\nfrom Intraoperative Blood Pressure Patterns",
            font_size=28, color=ACCENT, bold=False, alignment=PP_ALIGN.CENTER)

# Accent line
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                              Inches(5), Inches(4.0), Inches(3.3), Pt(3))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT
line.line.fill.background()

add_textbox(slide, Inches(1.5), Inches(4.3), Inches(10), Inches(0.6),
            "Dr Idris",
            font_size=24, color=LIGHT, bold=False, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(1.5), Inches(5.0), Inches(10), Inches(0.5),
            "Data: VitalDB  ·  100 surgical cases  ·  Seoul National University Hospital",
            font_size=16, color=LIGHT, bold=False, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE CLINICAL PROBLEM
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "The Clinical Problem")

add_bullet_slide(slide, Inches(0.8), Inches(1.6), Inches(7), Inches(4.5), [
    "Every anaesthetist faces this at case end:\n\"Does this patient need ICU or can they go to the ward?\"",
    "The decision is usually based on gut feeling + experience",
    "Getting it wrong matters:",
    "    Missed ICU → patient deteriorates on the ward",
    "    Over-triage → wasted ICU bed in a scarce resource",
], font_size=22, spacing=Pt(14))

add_highlight_box(slide, Inches(1.0), Inches(5.5), Inches(11), Inches(1.0),
                  "Can we use data already being recorded to help make this call?",
                  fill_color=RGBColor(0x2E, 0x86, 0xAB), font_size=24)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 3 — WHAT DATA DO WE ALREADY HAVE?
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "What Data Do We Already Have?")

add_bullet_slide(slide, Inches(0.8), Inches(1.6), Inches(7), Inches(4), [
    "Every patient with an arterial line has continuous MAP\nrecorded every 2 seconds",
    "By end of case: thousands of blood pressure readings\nwe currently ignore",
    "Plus: blood loss, fluids given, vasopressor use\n— all routinely documented",
], font_size=22, spacing=Pt(16))

add_highlight_box(slide, Inches(1.0), Inches(5.2), Inches(11), Inches(1.2),
                  "We are sitting on a goldmine of data\nwe already collect but don't systematically use",
                  fill_color=RGBColor(0x4E, 0x6A, 0x8A), font_size=22)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 4 — STUDY DESIGN
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "Study Design")

# Left column — data source
add_textbox(slide, Inches(0.8), Inches(1.6), Inches(5.5), Inches(0.5),
            "Data Source", font_size=22, color=ACCENT, bold=True)
add_bullet_slide(slide, Inches(0.8), Inches(2.1), Inches(5.5), Inches(2.5), [
    "VitalDB — open-access surgical database",
    "100 cases with complete arterial line recordings",
    "51 went to ICU, 49 to ward",
    "Beat-averaged MAP at ~2-second resolution",
], font_size=19, spacing=Pt(10))

# Right column — two models
add_textbox(slide, Inches(7), Inches(1.6), Inches(5.5), Inches(0.5),
            "Two Models Compared", font_size=22, color=ACCENT, bold=True)

add_highlight_box(slide, Inches(7), Inches(2.2), Inches(5.5), Inches(1.3),
                  "Model A — Intraop Only\n16 features from surgery alone\n(MAP metrics + blood loss + fluids + vasopressors)",
                  fill_color=RGBColor(0x27, 0xAE, 0x60), font_size=16, bold=False)

add_highlight_box(slide, Inches(7), Inches(3.7), Inches(5.5), Inches(1.3),
                  "Model B — Full Model\n22 features = Model A + age, BMI,\nASA, emergency status, comorbidities",
                  fill_color=RGBColor(0x2E, 0x86, 0xAB), font_size=16, bold=False)

add_highlight_box(slide, Inches(1.0), Inches(5.5), Inches(11), Inches(1.2),
                  "Key question: Does knowing who the patient is before surgery\nadd anything to what we observe during surgery?",
                  fill_color=RGBColor(0x4E, 0x6A, 0x8A), font_size=20)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 5 — FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "What Did We Measure from Blood Pressure?",
          "Turning a continuous MAP signal into interpretable numbers")

# Two columns of features
features_left = [
    ("Average MAP", "Overall perfusion pressure"),
    ("% time MAP < 65 mmHg", "Total hypotension burden"),
    ("% time MAP < 55 mmHg", "Severe hypotension (organ damage)"),
    ("Number of hypotensive episodes", "How many times BP dropped"),
]
features_right = [
    ("Longest episode duration", "Sustained hypoperfusion"),
    ("Time to first episode", "Early fragility marker"),
    ("MAP variability (SD, IQR)", "Haemodynamic lability"),
    ("MAP trend (slope)", "Getting worse or stable?"),
]

y_start = Inches(1.8)
for i, (feat, desc) in enumerate(features_left):
    y = y_start + Inches(i * 0.85)
    tf = add_textbox(slide, Inches(0.8), y, Inches(5.5), Inches(0.8),
                     feat, font_size=20, color=ACCENT, bold=True)
    add_para(tf, desc, font_size=16, color=LIGHT, space_before=Pt(2))

for i, (feat, desc) in enumerate(features_right):
    y = y_start + Inches(i * 0.85)
    tf = add_textbox(slide, Inches(7), y, Inches(5.5), Inches(0.8),
                     feat, font_size=20, color=ACCENT, bold=True)
    add_para(tf, desc, font_size=16, color=LIGHT, space_before=Pt(2))

add_textbox(slide, Inches(0.8), Inches(5.8), Inches(11), Inches(0.6),
            "+ Clinical variables: estimated blood loss, urine output, crystalloid/colloid, vasopressors, transfusion",
            font_size=16, color=LIGHT)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 6 — ICU vs WARD COMPARISON (figure)
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, MED_BG)
title_bar(slide, "ICU vs Ward: What Looks Different?")

fig_path = os.path.join(FIGDIR, '01_feature_comparison.png')
slide.shapes.add_picture(fig_path, Inches(0.5), Inches(1.4), Inches(12.3), Inches(4.8))

add_highlight_box(slide, Inches(1.0), Inches(6.3), Inches(11), Inches(0.8),
                  "No single number perfectly separates ICU from ward — "
                  "the combination of features provides discriminative power",
                  fill_color=RGBColor(0x4E, 0x6A, 0x8A), font_size=18)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 7 — ML APPROACH (SIMPLE)
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "The Machine Learning Approach",
          "Keeping it simple")

add_bullet_slide(slide, Inches(0.8), Inches(1.8), Inches(11), Inches(3.5), [
    "Random Forest = a committee of 300 decision trees",
    "Each tree asks simple yes/no questions:\n    \"Is MAP < 70?\"  \"Episodes > 3?\"  \"Blood loss > 500 mL?\"",
    "All 300 trees vote → majority rules → ICU or Ward",
    "Validated with 5-fold cross-validation:\n    Train on 80%, test on 20% — repeated 5 times\n    so every patient gets tested on data the model hasn't seen",
], font_size=22, spacing=Pt(16))

# Three algorithm boxes
for i, (name, col) in enumerate([
    ("Logistic Regression\n(linear baseline)", RGBColor(0x6A, 0x5A, 0xCD)),
    ("Random Forest\n(committee of trees)", RGBColor(0x27, 0xAE, 0x60)),
    ("Gradient Boosting\n(learns from mistakes)", RGBColor(0xE6, 0x7E, 0x22)),
]):
    add_highlight_box(slide, Inches(1.0 + i * 3.9), Inches(5.5), Inches(3.5), Inches(1.2),
                      name, fill_color=col, font_size=16)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 8 — ROC RESULTS (figure)
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, MED_BG)
title_bar(slide, "Results: How Well Does It Work?")

fig_path = os.path.join(FIGDIR, '02_roc_pr_curves.png')
slide.shapes.add_picture(fig_path, Inches(0.3), Inches(1.3), Inches(12.7), Inches(4.2))

# Key result boxes
add_highlight_box(slide, Inches(0.5), Inches(5.7), Inches(5.8), Inches(1.3),
                  "AUC = 0.789 (Intraop Only, Random Forest)\n"
                  "\"Pick one ICU + one ward patient at random →\n"
                  "model identifies which is which 79% of the time\"",
                  fill_color=RGBColor(0x27, 0xAE, 0x60), font_size=17)

add_highlight_box(slide, Inches(7), Inches(5.7), Inches(5.8), Inches(1.3),
                  "Intraop-only model BEAT the full model!\n"
                  "What happens during surgery predicts ICU\n"
                  "better than who the patient was before surgery",
                  fill_color=RGBColor(0xE0, 0x5C, 0x5C), font_size=17)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 9 — FEATURE IMPORTANCE (figure)
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, MED_BG)
title_bar(slide, "What Matters Most?",
          "Feature importance from Random Forest")

fig_path = os.path.join(FIGDIR, '03_feature_importance_calibration.png')
slide.shapes.add_picture(fig_path, Inches(0.3), Inches(1.4), Inches(12.7), Inches(4.3))

# Key findings
tf = add_textbox(slide, Inches(0.8), Inches(5.8), Inches(11.5), Inches(1.5),
                 "#1  Number of hypotensive episodes — not total time hypotensive!",
                 font_size=20, color=GOLD, bold=True)
add_para(tf, "#2  Severe hypotension (MAP < 55) — below autoregulation threshold",
         font_size=18, color=WHITE, bold=False, space_before=Pt(6))
add_para(tf, "#3  Case duration — proxy for surgical complexity",
         font_size=18, color=WHITE, bold=False, space_before=Pt(6))


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 10 — MAP TRAJECTORY ATLAS (figure)
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, MED_BG)
title_bar(slide, "The MAP Trajectory Atlas",
          "Comparing blood pressure patterns throughout the entire case")

fig_path = os.path.join(FIGDIR, '05_map_trajectory_atlas.png')
slide.shapes.add_picture(fig_path, Inches(0.3), Inches(1.4), Inches(12.7), Inches(4.0))

add_bullet_slide(slide, Inches(0.8), Inches(5.5), Inches(11.5), Inches(1.8), [
    "ICU patients have persistently lower MAP throughout — not just at isolated moments",
    "Biggest gap during the maintenance phase (middle of surgery)",
    "Mean MAP: ICU 79.1 vs Ward 83.9 mmHg (p = 0.036) — even 5 mmHg matters",
], font_size=18, spacing=Pt(8))


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 11 — CLINICAL PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "Clinical Performance",
          "At the optimal decision threshold (0.50)")

# Performance metrics as highlight boxes
metrics = [
    ("Sensitivity\n(Catches ICU patients)", "77%", RGBColor(0x27, 0xAE, 0x60)),
    ("Specificity\n(Correctly clears ward)", "67%", RGBColor(0x2E, 0x86, 0xAB)),
    ("F1 Score\n(Overall balance)", "0.74", RGBColor(0x6A, 0x5A, 0xCD)),
    ("Accuracy\n(Overall correct)", "72%", RGBColor(0xE6, 0x7E, 0x22)),
]

for i, (label, value, col) in enumerate(metrics):
    x = Inches(0.8 + i * 3.1)
    add_highlight_box(slide, x, Inches(1.8), Inches(2.8), Inches(2.2),
                      f"{value}", fill_color=col, font_size=48, bold=True)
    add_textbox(slide, x, Inches(4.1), Inches(2.8), Inches(0.9),
                label, font_size=16, color=LIGHT, alignment=PP_ALIGN.CENTER)

# Confusion matrix figure
fig_path = os.path.join(FIGDIR, '04_threshold_confusion.png')
slide.shapes.add_picture(fig_path, Inches(1.5), Inches(5.0), Inches(10), Inches(2.3))


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 12 — EPISODE COUNT MESSAGE
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "The Key Clinical Message")

add_textbox(slide, Inches(1.5), Inches(2.0), Inches(10), Inches(1.2),
            "Count the Dips, Not Just the Duration",
            font_size=44, color=GOLD, bold=True, alignment=PP_ALIGN.CENTER)

add_bullet_slide(slide, Inches(1.5), Inches(3.5), Inches(10), Inches(3.5), [
    "The #1 predictor was number of hypotensive episodes\n— not total time spent hypotensive",
    "Repeated drops and recoveries (ischaemia-reperfusion cycles)\nmay be more injurious than one sustained dip",
    "This aligns with emerging evidence on episodic vs\ncumulative hypotension burden",
    "Clinically: a patient who dips below MAP 65 six times\nmay be at higher risk than one who stays at MAP 60 for 10 minutes",
], font_size=20, spacing=Pt(14), bullet_color=GOLD)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 13 — PRACTICAL IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "How Would This Work in Practice?")

steps = [
    ("1", "Arterial line MAP is already recorded in the AIMS", RGBColor(0x27, 0xAE, 0x60)),
    ("2", "At case end, algorithm automatically calculates risk score", RGBColor(0x2E, 0x86, 0xAB)),
    ("3", "Score ≥ 50% triggers a clinical review alert", RGBColor(0xE6, 0x7E, 0x22)),
    ("4", "Anaesthetist reviews MAP trajectory + clinical data", RGBColor(0x6A, 0x5A, 0xCD)),
    ("5", "Final ICU decision remains with the clinician", RGBColor(0xE0, 0x5C, 0x5C)),
]

for i, (num, text, col) in enumerate(steps):
    y = Inches(1.8 + i * 0.95)
    # Number circle
    add_highlight_box(slide, Inches(1.5), y, Inches(0.6), Inches(0.6),
                      num, fill_color=col, font_size=24, bold=True)
    # Text
    add_textbox(slide, Inches(2.4), y + Inches(0.05), Inches(9), Inches(0.6),
                text, font_size=22, color=WHITE)

add_highlight_box(slide, Inches(1.5), Inches(6.0), Inches(10), Inches(0.9),
                  "No new equipment  ·  No manual data entry  ·  Decision support, not replacement",
                  fill_color=RGBColor(0x4E, 0x6A, 0x8A), font_size=20)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 14 — LIMITATIONS
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "Limitations")

add_bullet_slide(slide, Inches(0.8), Inches(1.6), Inches(11), Inches(5), [
    "Small sample size (100 cases) — needs external validation",
    "Enriched ICU prevalence (51% vs real-world ~15–20%)\n→ requires prevalence recalibration before deployment",
    "Single-centre data (Seoul) — generalisability to other\npopulations and practice patterns unknown",
    "Retrospective design — no proof yet that it changes outcomes",
    "Missing variables: cardiac output, depth of anaesthesia,\ntemperature, regional anaesthesia techniques",
], font_size=22, spacing=Pt(14))


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 15 — KEY TAKEAWAYS
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)
title_bar(slide, "Key Takeaways")

takeaways = [
    ("1", "Intraoperative MAP patterns predict ICU admission\nwith AUC = 0.789",
     RGBColor(0x27, 0xAE, 0x60)),
    ("2", "What happens during surgery matters more than\nwho the patient was before surgery",
     RGBColor(0x2E, 0x86, 0xAB)),
    ("3", "Count the dips — episode count beats total\nhypotension duration as a predictor",
     GOLD),
    ("4", "Even a 5 mmHg sustained MAP difference is\nprognostically meaningful",
     RGBColor(0xE6, 0x7E, 0x22)),
    ("5", "This could be automated with zero additional\nmonitoring equipment",
     RGBColor(0x6A, 0x5A, 0xCD)),
]

for i, (num, text, col) in enumerate(takeaways):
    y = Inches(1.6 + i * 1.1)
    add_highlight_box(slide, Inches(0.8), y, Inches(0.7), Inches(0.7),
                      num, fill_color=col, font_size=28, bold=True)
    add_textbox(slide, Inches(1.8), y + Inches(0.05), Inches(10.5), Inches(0.8),
                text, font_size=22, color=WHITE)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 16 — THANK YOU
# ═══════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, DARK_BG)

add_textbox(slide, Inches(1.5), Inches(2.0), Inches(10), Inches(1.2),
            "Thank You",
            font_size=52, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                              Inches(5.5), Inches(3.3), Inches(2.3), Pt(3))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT
line.line.fill.background()

add_textbox(slide, Inches(1.5), Inches(3.6), Inches(10), Inches(0.5),
            "Questions?",
            font_size=32, color=ACCENT, bold=False, alignment=PP_ALIGN.CENTER)

tf = add_textbox(slide, Inches(1.5), Inches(4.8), Inches(10), Inches(2),
                 "Data: VitalDB (vitaldb.net) — open access",
                 font_size=16, color=LIGHT, alignment=PP_ALIGN.CENTER)
add_para(tf, "", font_size=10, color=LIGHT, alignment=PP_ALIGN.CENTER)
add_para(tf, "Key references:", font_size=16, color=LIGHT,
         alignment=PP_ALIGN.CENTER, bold=True, space_before=Pt(8))
add_para(tf, "Walsh et al. Anesthesiology 2013 — MAP thresholds & outcomes",
         font_size=14, color=LIGHT, alignment=PP_ALIGN.CENTER, space_before=Pt(4))
add_para(tf, "Wesselink et al. BJA 2018 — Hypotension & adverse outcomes review",
         font_size=14, color=LIGHT, alignment=PP_ALIGN.CENTER, space_before=Pt(2))
add_para(tf, "Lee et al. Sci Data 2022 — VitalDB dataset",
         font_size=14, color=LIGHT, alignment=PP_ALIGN.CENTER, space_before=Pt(2))


# ── Save ─────────────────────────────────────────────────────────────────────
out_path = 'ICU_Prediction_Presentation.pptx'
prs.save(out_path)
print(f'Saved: {out_path}')
print(f'Slides: {len(prs.slides)}')
