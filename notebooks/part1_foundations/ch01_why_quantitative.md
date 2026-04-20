# Chapter 1 — Why Quantitative Anesthesia?

> *"The monitor is not an alarm system. It is a data stream. The question is whether you are listening."*

---

## The Most Quantitative Specialty That Rarely Does Quantitative Thinking

Consider what happens in the first three minutes of a general anesthetic.

A 67-year-old man, ASA 3, scheduled for laparoscopic colectomy. You induce with propofol 180 mg and fentanyl 100 μg. His mean arterial pressure drops from 94 to 58 mmHg. Heart rate rises from 68 to 91 bpm. SpO₂ holds at 99%. BIS falls from 94 to 42.

You have just generated — and discarded — a dataset. Heart rate trajectory over time. MAP nadir and its timing relative to drug administration. BIS slope as a function of propofol dose. The relationship between his SpO₂ and your ventilator settings.

You process all of this in real time, make a decision (give 6 mg of ephedrine, reduce propofol infusion to 4 mg/kg/hr), and move on. The monitor scrolls. The data disappears.

Anesthesiology is perhaps the most quantitative clinical specialty in medicine — every case generates continuous, timestamped, high-resolution physiological data across haemodynamic, respiratory, anaesthetic, and neurological domains simultaneously. Yet most of us were trained to *react* to these numbers rather than *understand* them. We know that MAP < 65 needs treatment. We know far less about *why*, *how much below matters*, *for how long*, or *which patients are most vulnerable*.

This book is built on a simple premise: **understanding the numbers makes you a better clinician**.

---

## What Quantitative Thinking Changed

The history of anesthesia practice is punctuated by quantitative findings that overturned clinical intuition.

### The POISE Trial: When a Good Number Hid a Bad Outcome

In 2008, the POISE trial enrolled 8,351 patients undergoing noncardiac surgery and randomly assigned them to extended-release metoprolol or placebo. The cardiovascular logic was sound: perioperative catecholamine surges cause myocardial ischaemia; beta-blockade should help.

The quantitative result was more complex than the biology predicted.

| Outcome | Metoprolol | Placebo | Relative Risk |
|---|---|---|---|
| Myocardial infarction | 4.2% | 5.7% | **0.73 (benefit)** |
| Stroke | 1.0% | 0.5% | **2.17 (harm)** |
| Death (all causes) | 3.1% | 2.3% | **1.33 (harm)** |

Metoprolol prevented heart attacks and caused strokes. The net mortality signal was *worse* with the intervention. No amount of physiological reasoning could have predicted this without counting the outcomes. Every anesthesiologist who had been prescribing perioperative beta-blockade based on mechanism — and many were — needed this trial to change their practice.

The lesson is not that physiology is wrong. The lesson is that **physiology tells you what might happen; data tells you what does happen**.

### The PRODIGY Trial: Counting to Save Lives

Postoperative opioid-induced respiratory depression (OIRD) is a preventable catastrophe — patients die quietly in monitored wards because intermittent pulse oximetry misses episodes of hypoxaemia between checks.

The PRODIGY trial (2019) used continuous pulse oximetry across 16 countries to identify patients at high risk of respiratory depression. By quantifying risk factors — opioid dose, sleep apnoea history, age, obesity — they developed a risk score that could stratify patients into low, intermediate, and high-risk groups with meaningfully different event rates.

This is the essence of quantitative anesthesia: measuring something continuously, defining an outcome rigorously, counting who experiences it, and building a model that predicts it.

### Depth of Anaesthesia Research: Numbers Revealing a Hidden Harm

A series of observational and interventional studies beginning in the 2000s examined an uncomfortable question: does the depth of anaesthesia matter beyond the immediate goal of preventing awareness?

The early observation — that cumulative time with BIS below 45 was independently associated with 1-year mortality in older patients — was striking enough to generate controversy. Subsequent trials (including the ENGAGES trial in 2019) investigated whether EEG-guided, lighter anaesthesia reduced delirium and other adverse outcomes in elderly patients, with mixed but directionally consistent results.

Whether or not depth of anaesthesia directly causes harm, the quantitative question is legitimate and the methodology is now established: define the exposure (time-below-threshold on a continuous BIS signal), define the outcome (mortality, delirium, length of stay), measure confounders, model the relationship. These are the tools of Chapters 8–19.

---

## What This Book Will — and Will Not — Teach You

### What This Book Will Teach You

- **How to think statistically**, not just how to run tests. You will understand *why* you use a Mann-Whitney U instead of a t-test for ordinal data, and what you lose if you get this wrong.
- **How to model physiological relationships**, from simple linear regression of tidal volume on height to non-linear pharmacodynamic dose-response curves for propofol and BIS.
- **How to work with real perioperative data** — messy, zero-inflated, censored, missing, time-varying data — using Python and the VitalDB dataset.
- **How to read the literature critically**. After Part II, you will be able to evaluate a methodology section in any anaesthesia journal and identify what the authors did, what they assumed, and what they cannot conclude.
- **How to build clinical prediction models** — and more importantly, how to evaluate whether they are good enough to trust with patients.

### What This Book Will Not Teach You

- **How to be a statistician.** There are no proofs, no measure theory, no sampling theory. This book is written by a clinician for clinicians.
- **How to run one-size-fits-all analyses.** There is no universal flowchart. The right analysis depends on the question, the data, and the assumptions you are willing to defend.
- **How to generate publishable p-values**. If your goal is to mine a dataset until something reaches p < 0.05, this book will make you better at seeing why that is wrong — and harder to get away with.

---

## The Five Principles of Quantitative Anesthesia

These principles run through every chapter. State them now; return to them when the mathematics gets hard.

**1. Every equation has a patient attached to it.**
The Henderson-Hasselbalch equation is not abstract algebra — it is the acid-base status of the patient bleeding on the table. The Hill equation is not a curve-fitting exercise — it is the relationship between the propofol concentration in a patient's brain and the depth of their unconsciousness.

**2. Show the uncertainty.**
A mean without a confidence interval is a guess dressed up as knowledge. Every estimate in this book carries uncertainty bounds. Medicine gives false certainty; statistics teaches appropriate humility.

**3. Reproducibility is not optional.**
Every result in this book can be reproduced by running the corresponding notebook against the VitalDB dataset. No results are transcribed by hand, copied from a figure, or "approximately read" from a graph.

**4. Complexity earns its place.**
A logistic regression with AUROC 0.78 that an anaesthetist can understand and explain to a family is better than a neural network with AUROC 0.82 that cannot be interrogated. Complexity must justify itself clinically, not just statistically.

**5. The physiology is always the ground truth.**
When the data disagrees with physiology, investigate before accepting. A result that shows propofol *raises* BIS at higher concentrations is probably a data quality problem, not a pharmacological discovery.

---

## Your Dataset: VitalDB at a Glance

All primary examples in this book use the **VitalDB dataset** — a publicly available, de-identified perioperative database from Seoul National University Hospital. Before we spend twenty chapters analysing it, we should know what it contains.

### Loading the Data for the First Time

:::{toggle} Show Python
```python
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path('/Volumes/iDrisAI/VitalDBGit/vital_db')

cases  = pd.read_csv(DATA_DIR / 'all_cases.csv')
labs   = pd.read_csv(DATA_DIR / 'labs.csv')
tracks = pd.read_csv(DATA_DIR / 'tracks.csv')

print(f'cases  : {cases.shape[0]:,} rows × {cases.shape[1]} columns')
print(f'labs   : {labs.shape[0]:,} rows × {labs.shape[1]} columns')
print(f'tracks : {tracks.shape[0]:,} rows × {tracks.shape[1]} columns')
```
:::

```text
cases  : 6,388 rows × 74 columns
labs   : 928,448 rows × 4 columns
tracks : 486,449 rows × 3 columns
```

Three files. Three levels of resolution. Together they describe what happened to 6,388 patients across their entire perioperative journey — from preoperative blood draw to hospital discharge.

### The Cohort in Ten Numbers

:::{toggle} Show Python
```python
tracks['device'] = tracks['tname'].str.split('/').str[0]

print('─' * 45)
print('VitalDB at a glance')
print('─' * 45)
print(f'  Surgical cases          :  {len(cases):,}')
print(f'  Unique patients         :  {cases["subjectid"].nunique():,}')
print(f'  Overall mortality       :  {cases["death_inhosp"].mean()*100:.2f}%')
print(f'  Emergency surgeries     :  {cases["emop"].sum():,}  ({cases["emop"].mean()*100:.1f}%)')
print(f'  ICU admissions          :  {(cases["icu_days"]>0).sum():,}  ({(cases["icu_days"]>0).mean()*100:.1f}%)')
print(f'  Mean age                :  {cases["age"].mean():.1f} ± {cases["age"].std():.1f} years')
print(f'  Male                    :  {(cases["sex"]=="M").mean()*100:.1f}%')
print(f'  Lab records             :  {len(labs):,}')
print(f'  Unique lab test types   :  {labs["name"].nunique()}')
print(f'  Monitor track records   :  {len(tracks):,}')
print(f'  Unique signals          :  {tracks["tname"].nunique()}')
print(f'  Monitoring devices      :  {tracks["device"].nunique()}')
print('─' * 45)
```
:::

```text
─────────────────────────────────────────────
VitalDB at a glance
─────────────────────────────────────────────
  Surgical cases          :  6,388
  Unique patients         :  5,853
  Overall mortality       :  0.89%
  Emergency surgeries     :  782   (12.2%)
  ICU admissions          :  1,204  (18.8%)
  Mean age                :  57.3 ± 15.0 years
  Male                    :  50.8%
  Lab records             :  928,448
  Unique lab test types   :  34
  Monitor track records   :  486,449
  Unique signals          :  173
  Monitoring devices      :  11
─────────────────────────────────────────────
```

### What Surgeries Are in the Dataset?

:::{toggle} Show Python
```python
print('Top 10 surgical procedures:')
cases['opname'].value_counts().head(10).to_frame('cases')
```
:::

```text
Top 10 surgical procedures:
                                          cases
opname
Cholecystectomy                             503
Distal gastrectomy                          342
Lung lobectomy                              332
Breast-conserving surgery                   295
Anterior resection                          247
Lung wedge resection                        236
Excision                                    228
Exploratory laparotomy                      215
Hemicolectomy                               193
Low anterior resection                      181
```

This is a surgical oncology–heavy dataset: gastrectomy, colectomy, lobectomy. That matters when we interpret propofol doses, blood loss patterns, and ICU admission rates — this is not a general district hospital population.

### ASA Distribution and Outcome Preview

:::{toggle} Show Python
```python
asa_summary = cases.groupby('asa').agg(
    n        = ('caseid',       'count'),
    mortality = ('death_inhosp', lambda x: f"{x.mean()*100:.2f}%"),
    icu_rate  = ('icu_days',     lambda x: f"{(x>0).mean()*100:.1f}%"),
).reset_index()

print(asa_summary.to_string(index=False))
```
:::

```text
 asa     n  mortality  icu_rate
   1  1065      0.00%      3.7%
   2  3136      0.16%     11.6%
   3  1951      1.79%     31.2%
   4   216      6.48%     65.3%
   5    18     27.78%     88.9%
   6     2        —%        —%
```

Even this two-line table contains a story worth a chapter: ASA class, despite being ordinal and subjective, predicts mortality with a gradient that spans two orders of magnitude. An ASA 5 patient is 170 times more likely to die in hospital than an ASA 1 patient. The data *validates* the scale — even though no one designed ASA classification with logistic regression in mind.

This relationship — and its interaction with emergency surgery — is examined in detail in **Section 1.2**.

### What the Monitor Recorded

:::{toggle} Show Python
```python
top_devices = tracks['device'].value_counts().head(6)
print('Track records by monitoring device:')
print(top_devices.to_string())
```
:::

```text
Track records by monitoring device:
device
Primus       201,733   ← Dräger anaesthetic workstation (ventilator + gas analyser)
Solar8000    167,024   ← GE patient monitor (ECG, SpO₂, NIBP, arterial line, CVP)
BIS           45,742   ← Medtronic BIS (depth of anaesthesia: BIS, EMG, SEF, SR)
Orchestra     43,324   ← Fresenius TIVA pump (propofol Cp, Ce, Ct, rate, volume)
SNUADC        21,260   ← SNU A/D converter (raw arterial, CVP waveforms at 500 Hz)
EV1000         4,422   ← Edwards haemodynamic platform (FloTrac CO, SVV, SVR)
```

The Orchestra pump records propofol infusion *with* target-controlled infusion plasma and effect-site concentrations. The BIS monitor records the brain's response. The SNUADC records the raw arterial waveform at 500 Hz. **The pharmacodynamic relationship between propofol Ce and BIS is directly observable in this dataset** — we will fit that curve in Chapter 13.

---

## How to Use This Book

### If you are a trainee anaesthesiologist

Read sequentially from Chapter 1. Complete the VitalDB exercises in each chapter using the notebooks. By Part III you will be able to read and critically appraise a methodology section in any anaesthesia journal. By Part V you will be able to build and validate a clinical prediction model.

The mathematics is introduced gradually. Chapter 2 needs no more than secondary school algebra. Chapter 13 (PK/PD modelling) requires comfort with exponential functions. By the time you reach it, the earlier chapters will have built the intuition.

### If you are a consultant or attending

Jump to the chapter most relevant to your practice. Chapters 11–14 (physiology made quantitative) contain rigorous mathematical treatments of concepts you already know clinically — you may find that the formulas make your intuitions more precise, or that the data challenges assumptions you did not know you were making.

### If you are a clinical researcher

Parts IV and V are the core. Chapter 20 walks through a complete published-quality observational study from question formulation to STROBE-compliant reporting. Chapters 15–19 cover the methods most commonly misapplied in anaesthesia research: feature engineering, machine learning, time-series analysis, and causal inference from observational data.

### If you are a data scientist new to anaesthesia

Read Part IV (Chapters 11–14) before touching the machine learning chapters. The data is meaningless without the physiology. A model that predicts "mortality" from propofol dose without understanding that propofol dose is confounded by case duration, surgical complexity, patient weight, and comorbidity is not a mortality model — it is a case-complexity model. Knowing the domain saves you from building things that are technically impressive and clinically wrong.

---

## What Comes Next

### Section 1.1 — The VitalDB Dataset: Your Laboratory

A deeper tour of the dataset: every file, every device, every signal category. We will look at how preoperative haemoglobin correlates with mortality, how perioperative creatinine changes around surgery, and how the monitor's temporal resolution (500 Hz waveforms vs. 1-per-minute vital signs vs. once-daily labs) determines what questions you can ask.

### Section 1.2 — ASA Classification and Mortality: A First Look

A worked quantitative analysis of the simplest clinical question in this book: does ASA class predict mortality? The analysis takes the ASA scale — subjective, ordinal, inter-rater variable — and tests it against the hard endpoint of death. The relationship is real, steep, and modified by the emergency/elective distinction in ways that have direct clinical implications.

This is the first encounter with the core workflow that will recur throughout the book: load data, define exposure, define outcome, visualise the relationship, quantify the association, check for confounders.

---

## A Note on Uncertainty

This book will repeatedly ask you to be precise about what you do not know. Confidence intervals, calibration curves, sensitivity analyses — these are not defensive statistics. They are the honest acknowledgement that data from 6,388 patients in one tertiary hospital in Seoul cannot speak with authority about what will happen to your next patient in Nairobi, Glasgow, or Buenos Aires.

External validation is not a final step — it is an ongoing obligation. Every number in this book comes from a specific population, a specific time period, and a specific measurement protocol. Know what you are generalising from, and to.

> *"Numbers without context are noise. In anaesthesia, context is the patient."*

---

## Further Reading

- Sessler, D.I., et al. (2008). Perioperative Quality Initiative: An executive summary. *Anesthesiology*, 109(5), 768–776.
- Devereaux, P.J., et al. (2008). Effects of extended-release metoprolol succinate in patients undergoing non-cardiac surgery (POISE trial). *Lancet*, 371(9627), 1839–1847.
- Khanna, A.K., et al. (2019). Prediction of Opioid-Induced Respiratory Depression on Inpatient Wards Using Continuous Capnography and Oximetry: An International Prospective, Observational Trial (PRODIGY). *Anesthesia & Analgesia*, 129(5), 1339–1354.
- Wildes, T.S., et al. (2019). Effect of Electroencephalography-Guided Anesthetic Administration on Postoperative Delirium Among Older Adults Undergoing Major Surgery (ENGAGES trial). *JAMA*, 321(5), 473–483.
- Monk, T.G., et al. (2005). Anesthetic Management and One-Year Mortality After Noncardiac Surgery. *Anesthesia & Analgesia*, 100(1), 4–10.
