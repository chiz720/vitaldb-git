#!/usr/bin/env python3
"""Build a conference abstract as .docx."""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document()

# ── Page setup ───────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15


# ── Helpers ──────────────────────────────────────────────────────────────────
def add_heading_run(paragraph, text, bold=True, size=Pt(12), italic=False):
    run = paragraph.add_run(text)
    run.bold = bold
    run.font.size = size
    run.font.name = 'Times New Roman'
    run.italic = italic
    return run


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    return p


def add_body(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
    return p


# ── Title ────────────────────────────────────────────────────────────────────
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(6)
run = title.add_run(
    "Intraoperative Blood Pressure Patterns Predict Unplanned ICU Admission: "
    "A Machine Learning Analysis of the VitalDB Dataset"
)
run.bold = True
run.font.size = Pt(14)
run.font.name = 'Times New Roman'

# ── Author ───────────────────────────────────────────────────────────────────
author = doc.add_paragraph()
author.alignment = WD_ALIGN_PARAGRAPH.CENTER
author.paragraph_format.space_after = Pt(2)
run = author.add_run("Dr Idris")
run.font.size = Pt(12)
run.font.name = 'Times New Roman'

# ── Separator ────────────────────────────────────────────────────────────────
sep = doc.add_paragraph()
sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
sep.paragraph_format.space_before = Pt(8)
sep.paragraph_format.space_after = Pt(8)
run = sep.add_run("─" * 40)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
run.font.size = Pt(8)

# ── Background ───────────────────────────────────────────────────────────────
add_section_heading(doc, "Background")
add_body(doc,
    "Decisions about postoperative ICU admission are often made at the end of surgery "
    "based on clinical judgement alone. Continuous arterial blood pressure monitoring "
    "generates thousands of data points per case that are routinely recorded but rarely "
    "used systematically for disposition planning. We investigated whether intraoperative "
    "haemodynamic patterns, derived entirely from data already collected during surgery, "
    "can predict which patients will require ICU admission."
)

# ── Methods ──────────────────────────────────────────────────────────────────
add_section_heading(doc, "Methods")
add_body(doc,
    "We analysed 100 surgical cases from VitalDB, an open-access database of high-fidelity "
    "intraoperative physiological recordings from Seoul National University Hospital. "
    "Beat-averaged mean arterial pressure (MAP) waveforms recorded at 2-second resolution "
    "were reduced to 12 interpretable haemodynamic burden features, including mean MAP, "
    "percentage of time below 65 mmHg and 55 mmHg, number of discrete hypotensive episodes, "
    "maximum episode duration, and MAP variability. These were combined with intraoperative "
    "clinical variables (estimated blood loss, fluid administration, vasopressor use). "
    "Two models were compared using 5-fold stratified cross-validation: Model A "
    "(16 intraoperative features only) and Model B (22 features including preoperative age, "
    "BMI, ASA classification, and comorbidities). Three classifiers were evaluated: "
    "logistic regression, random forest, and gradient boosting."
)

# ── Results ──────────────────────────────────────────────────────────────────
add_section_heading(doc, "Results")
add_body(doc,
    "Fifty-one patients (51%) required ICU admission. The best-performing model was the "
    "intraoperative-only random forest (Model A), achieving an area under the receiver "
    "operating characteristic curve (AUC) of 0.789 (\u00b1 0.044), sensitivity of 77%, "
    "specificity of 67%, and F1 score of 0.74. Adding preoperative demographics did not "
    "improve performance (Model B AUC = 0.768). The single most important predictor was "
    "the number of discrete hypotensive episodes (Gini importance 0.172), followed by "
    "percentage of time with severe hypotension (MAP < 55 mmHg) and case duration. "
    "ICU patients had significantly lower mean MAP throughout the entire case "
    "(79.1 vs 83.9 mmHg, p = 0.036), with the greatest divergence during the surgical "
    "maintenance phase."
)

# ── Conclusions ──────────────────────────────────────────────────────────────
add_section_heading(doc, "Conclusions")
add_body(doc,
    "Intraoperative haemodynamic patterns predict ICU admission more accurately than models "
    "incorporating preoperative patient characteristics, suggesting that cumulative "
    "physiological insult during surgery dominates over baseline patient risk. Notably, "
    "the number of discrete hypotensive episodes was a stronger predictor than total "
    "hypotension duration, consistent with an ischaemia-reperfusion injury mechanism. "
    "This approach requires no additional monitoring equipment and could be embedded into "
    "existing anaesthesia information management systems as an automated end-of-case ICU "
    "triage tool. External validation in larger, multi-centre cohorts with general surgical "
    "prevalence rates is needed."
)

# ── Keywords ─────────────────────────────────────────────────────────────────
kw = doc.add_paragraph()
kw.paragraph_format.space_before = Pt(12)
kw.paragraph_format.space_after = Pt(4)
run_label = kw.add_run("Keywords: ")
run_label.bold = True
run_label.font.size = Pt(11)
run_label.font.name = 'Times New Roman'
run_kw = kw.add_run(
    "intraoperative hypotension, ICU admission, machine learning, "
    "haemodynamic monitoring, clinical decision support"
)
run_kw.italic = True
run_kw.font.size = Pt(11)
run_kw.font.name = 'Times New Roman'

# ── Data source ──────────────────────────────────────────────────────────────
ds = doc.add_paragraph()
ds.paragraph_format.space_before = Pt(16)
run = ds.add_run(
    "Data source: VitalDB (vitaldb.net) \u2014 Seoul National University Hospital. "
    "All analyses performed on the open-access dataset under the VitalDB data use agreement."
)
run.font.size = Pt(10)
run.font.name = 'Times New Roman'
run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

# ── Word count footer ───────────────────────────────────────────────────────
wc_text = (
    "Decisions about postoperative ICU admission are often made at the end of surgery "
    "based on clinical judgement alone Continuous arterial blood pressure monitoring "
    "generates thousands of data points per case that are routinely recorded but rarely "
    "used systematically for disposition planning We investigated whether intraoperative "
    "haemodynamic patterns derived entirely from data already collected during surgery "
    "can predict which patients will require ICU admission "
    "We analysed 100 surgical cases from VitalDB an open-access database of high-fidelity "
    "intraoperative physiological recordings from Seoul National University Hospital "
    "Beat-averaged mean arterial pressure MAP waveforms recorded at 2-second resolution "
    "were reduced to 12 interpretable haemodynamic burden features including mean MAP "
    "percentage of time below 65 mmHg and 55 mmHg number of discrete hypotensive episodes "
    "maximum episode duration and MAP variability These were combined with intraoperative "
    "clinical variables estimated blood loss fluid administration vasopressor use "
    "Two models were compared using 5-fold stratified cross-validation Model A "
    "16 intraoperative features only and Model B 22 features including preoperative age "
    "BMI ASA classification and comorbidities Three classifiers were evaluated "
    "logistic regression random forest and gradient boosting "
    "Fifty-one patients 51 required ICU admission The best-performing model was the "
    "intraoperative-only random forest Model A achieving an area under the receiver "
    "operating characteristic curve AUC of 0.789 0.044 sensitivity of 77 "
    "specificity of 67 and F1 score of 0.74 Adding preoperative demographics did not "
    "improve performance Model B AUC 0.768 The single most important predictor was "
    "the number of discrete hypotensive episodes Gini importance 0.172 followed by "
    "percentage of time with severe hypotension MAP 55 mmHg and case duration "
    "ICU patients had significantly lower mean MAP throughout the entire case "
    "79.1 vs 83.9 mmHg p 0.036 with the greatest divergence during the surgical "
    "maintenance phase "
    "Intraoperative haemodynamic patterns predict ICU admission more accurately than models "
    "incorporating preoperative patient characteristics suggesting that cumulative "
    "physiological insult during surgery dominates over baseline patient risk Notably "
    "the number of discrete hypotensive episodes was a stronger predictor than total "
    "hypotension duration consistent with an ischaemia-reperfusion injury mechanism "
    "This approach requires no additional monitoring equipment and could be embedded into "
    "existing anaesthesia information management systems as an automated end-of-case ICU "
    "triage tool External validation in larger multi-centre cohorts with general surgical "
    "prevalence rates is needed"
)
word_count = len(wc_text.split())

wc = doc.add_paragraph()
wc.alignment = WD_ALIGN_PARAGRAPH.RIGHT
wc.paragraph_format.space_before = Pt(12)
run = wc.add_run(f"Word count (body): ~{word_count}")
run.font.size = Pt(9)
run.font.name = 'Times New Roman'
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
run.italic = True

# ── Save ─────────────────────────────────────────────────────────────────────
out_path = 'ICU_Prediction_Abstract.docx'
doc.save(out_path)
print(f'Saved: {out_path}')
print(f'Approximate word count (body): {word_count}')
