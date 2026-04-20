# Chapter 2 — Types of Variables

> *"The beginning of wisdom is the definition of terms."* — Socrates

---

Before you touch a single line of code or choose a statistical test, you must answer one question: **what kind of data do I have?**

This is not a formality. The type of a variable determines everything downstream — which summary statistics are valid, which tests are appropriate, which visualisations make sense, and which analyses will produce nonsense even if the numbers look plausible.

Anesthesia generates an unusually rich mixture of variable types in a single case: a categorical sex, an ordinal ASA class, continuous blood pressures, a counted number of vasopressor boluses, binary mortality, and survival times all appear together in `all_cases.csv`. Getting these right is the foundation of everything that follows.

---

## 2.1 Categorical Variables

Categorical variables represent group membership. Their values name a category rather than measure a quantity. Two subtypes — nominal and ordinal — differ in one critical way: **whether the categories have a meaningful order**.

### Nominal Variables

Nominal variables have no inherent ordering. Calling one category "higher" than another is meaningless.

**Examples from VitalDB `all_cases.csv`:**

| Variable | Categories | Why Nominal |
|---|---|---|
| `sex` | M, F | No sensible ordering between sexes |
| `approach` | Open, Laparoscopic, Robotic | Surgical approaches are not ranked by severity |
| `ane_type` | General, Regional, Sedation | Anesthesia types are qualitatively different, not ordered |
| `department` | General Surgery, Thoracic, Orthopaedic... | Hospital departments are not on a scale |
| `position` | Supine, Lateral, Lithotomy, Prone | Patient positions are qualitatively distinct |
| `airway` | Oral, Nasal | Route of airway device |

**Legitimate operations on nominal data:**
- Counting (frequency tables)
- Mode (the most common category)
- Chi-squared tests and Fisher's exact tests
- Proportions and risk ratios

**Illegitimate operations:**
- Means (the "average" sex is meaningless)
- Standard deviations
- Any statement about being "higher" or "lower"

:::{important} Coding trap
When you code nominal variables as numbers for a model (`Open=0`, `Laparoscopic=1`, `Robotic=2`), the computer does not know these numbers are arbitrary labels. A linear model will assume `Robotic` is twice as far from `Open` as `Laparoscopic` is — which is wrong. **Always use one-hot encoding for nominal predictors.**
:::

---

### Ordinal Variables

Ordinal variables have categories that carry a **meaningful rank order**, but the intervals between ranks are not necessarily equal.

This is the crucial distinction: you know that `ASA 3 > ASA 2`, but you cannot say that the difference between ASA 2 and ASA 3 equals the difference between ASA 3 and ASA 4.

**Examples from VitalDB:**

**ASA Physical Status (the most important ordinal variable in anesthesia)**

| ASA Class | Definition | Clinical Meaning |
|---|---|---|
| 1 | Normal healthy | No physiological compromise |
| 2 | Mild systemic disease | Controlled hypertension, mild asthma |
| 3 | Severe systemic disease | Poorly controlled DM, COPD, morbid obesity |
| 4 | Life-threatening disease | Recent MI, severe CHF, end-stage renal failure |
| 5 | Moribund | Not expected to survive 24 hours without surgery |
| 6 | Brain-dead donor | Organ harvesting |

The step from ASA 1 to ASA 2 is not the same physiological leap as from ASA 4 to ASA 5. The numbers convey rank, not equal-interval distance.

**Cormack-Lehane Grade (airway difficulty)**

| Grade | View on Laryngoscopy |
|---|---|
| 1 | Full glottis visible |
| 2 | Only posterior commissure visible |
| 3 | Only epiglottis visible |
| 4 | No laryngeal structures visible |

Again: ordered, but not evenly spaced in terms of clinical difficulty.

**Legitimate operations on ordinal data:**
- Counts and proportions
- Median and interquartile range
- Non-parametric tests (Mann-Whitney, Kruskal-Wallis, Spearman correlation)
- Ordinal regression

**Often-illegitimate operations:**
- Means and standard deviations (though widely done, this assumes equal intervals)
- Pearson correlation

:::{warning} The ordinal mean fallacy
Reporting "mean ASA 2.4 ± 0.8" is ubiquitous in the anesthesia literature. It is technically incorrect — ASA is ordinal, not continuous. The correct summary is median ASA [IQR]. In practice, ASA is often treated as continuous and the results are usually not dramatically wrong, but you should know what assumption you are making when you do this.
:::

---

## 2.2 Continuous Variables

Continuous variables represent measurements on a numerical scale. They can take any value within a range (at least in principle, limited only by measurement precision).

Two subtypes differ in whether **zero means the complete absence of the quantity**.

### Interval Variables

Interval variables have equal spacing between values, but **zero is arbitrary** — it does not mean "none of the quantity."

**Clinical examples:**

- **Temperature (°C or °F):** 0°C does not mean "no temperature." The zero point is defined by water's freezing point, not by the absence of molecular motion (that would be −273°C, i.e., 0 Kelvin).
- **pH:** pH 7.0 does not mean "no acid-base status." The scale is logarithmic and the zero is defined mathematically, not physiologically. pH 0 would be a proton concentration of 1 mol/L — incompatible with life.
- **Base excess (BE):** Can be negative. Zero does not mean absence of buffering.

**What you cannot do with interval data:**
- Meaningful ratios. A patient with a temperature of 40°C is not "twice as hot" as one at 20°C (in Celsius). They *would* be twice as hot in Kelvin (313 K vs. 293 K).

**What you can do:**
- All arithmetic operations on the values themselves
- Differences are meaningful: ΔpH of 0.1 is the same anywhere on the scale
- Mean, standard deviation, t-tests, linear regression

In anesthesia, you rarely encounter pure interval scales. Temperature in Kelvin (absolute zero = no thermal motion) would be a ratio scale. pH and temperature in Celsius are the main interval examples you will meet.

---

### Ratio Variables

Ratio variables have **equal intervals AND a true zero** — zero means complete absence of the quantity. Ratios between values are therefore meaningful.

Most physiological measurements in anesthesia are ratio variables:

| Variable | True Zero Meaning | Ratio Example |
|---|---|---|
| Blood pressure (MAP, mmHg) | 0 mmHg = no perfusion pressure | MAP 90 is twice MAP 45 |
| Heart rate (bpm) | 0 bpm = cardiac arrest | HR 120 is twice HR 60 |
| Propofol dose (mg) | 0 mg = no drug given | 200 mg is twice 100 mg |
| Haemoglobin (g/dL) | 0 g/dL = no haemoglobin | Hb 14 is twice Hb 7 |
| Urine output (mL) | 0 mL = anuria | 600 mL is twice 300 mL |
| Blood loss (mL) | 0 mL = no haemorrhage | Applies |

**All arithmetic is valid on ratio data**, and meaningful ratios can be stated: a patient who lost 1000 mL lost twice as much blood as one who lost 500 mL.

:::{note} Temperature in the OR
In practice, we treat temperature in Celsius as ratio-like because we rarely encounter values near 0°C and because clinical differences (35°C vs. 38°C) behave similarly to ratio quantities in our range of interest. This is a pragmatic simplification that does not usually cause harm, but it is worth knowing.
:::

---

## 2.3 Special Variable Types in Anesthesia

Beyond the Stevens scale, anesthesia data routinely contains variable types that require specific statistical methods.

### Binary Variables (Dichotomous)

Binary variables have exactly two mutually exclusive values: **yes/no, alive/dead, present/absent**.

They are a special case of nominal variables, but because there are only two categories, arithmetic is possible: the proportion (or probability) of the "yes" category is a meaningful summary.

**VitalDB examples:**

| Variable | Values | Clinical Meaning |
|---|---|---|
| `death_inhosp` | 0/1 | Did the patient die in hospital? |
| `emop` | 0/1 | Was this an emergency operation? |
| `preop_htn` | 0/1 | Pre-existing hypertension? |
| `preop_dm` | 0/1 | Pre-existing diabetes mellitus? |

**Appropriate statistics:**
- Proportion (prevalence, risk)
- Odds and odds ratio
- Risk ratio (relative risk)
- Logistic regression (Chapter 9)
- Chi-squared, Fisher's exact

**Derived binary variables** are frequently created in clinical research. For example, "intraoperative hypotension" might be defined as MAP < 65 mmHg for any duration during the case — a binary yes/no derived from a continuous time series.

---

### Count Variables

Count variables record **how many times something occurred**. They are non-negative integers (0, 1, 2, 3...) and have a true zero.

**VitalDB examples:**

| Variable | What it Counts |
|---|---|
| `intraop_rbc` | Units of packed red blood cells transfused |
| `intraop_ffp` | Units of fresh frozen plasma transfused |
| `icu_days` | Days spent in ICU |

**Why count variables need special handling:**
- They are bounded below by zero (you cannot transfuse −1 units)
- They are often right-skewed (most patients receive 0 units; a few receive many)
- They are often zero-inflated (the majority of cases may have a count of zero)
- They require Poisson or negative binomial regression, not linear regression

Applying linear regression to count data can produce predictions of negative counts — a mathematical absurdity with a clinical consequence (a model predicts a patient needs −2 units of blood).

---

### Time-to-Event Variables (Survival Data)

Time-to-event variables record **the time until something happens**, where "something" is an event of interest.

**VitalDB context:**

The dataset contains absolute timestamps for key operative milestones:

| Variable | Event |
|---|---|
| `casestart`, `caseend` | Operating room entry and exit |
| `anestart`, `aneend` | Anesthesia start and end |
| `opstart`, `opend` | Surgical incision and closure |
| `adm`, `dis` | Hospital admission and discharge |

From these, you can derive:
- **Anesthesia duration:** `aneend − anestart`
- **Surgical duration:** `opend − opstart`
- **Hospital length of stay:** `dis − adm`
- **ICU length of stay:** directly available as `icu_days`

**The censoring problem:**

Time-to-event data is special because some patients **haven't had the event yet** when data collection ends — they are *censored*. A patient still alive at discharge is censored for time-to-death; their survival time is "at least X days," not exactly X days.

Ordinary regression ignores censoring and systematically underestimates survival times. **Survival analysis methods** (Kaplan-Meier curves, Cox models) handle censoring correctly. This is covered in Chapter 10.

$$\text{Hazard}(t) = \lim_{\Delta t \to 0} \frac{P(\text{event in } [t, t+\Delta t) \mid \text{survived to } t)}{\Delta t}$$

---

### Compositional Variables

Compositional variables are **bounded proportions that sum to a constant** (usually 1 or 100%).

**Clinical examples:**

- **FiO₂ (fraction of inspired oxygen):** Ranges 0.21–1.0. The remaining fraction is primarily nitrogen. FiO₂ + FiN₂ + FiOther = 1.0.
- **%MAC (minimum alveolar concentration):** Volatile agent concentration expressed as a fraction of the MAC. 0.5 MAC means half the dose needed for 50% of patients to be motionless to surgical incision.
- **SaO₂ (oxygen saturation):** Bounded 0–100%. The remaining fraction is deoxygenated haemoglobin.

**Why compositional data is special:**

Compositional variables violate the independence assumption of standard regression. A change in FiO₂ necessarily changes FiN₂. Specialised methods (e.g., isometric log-ratio transformations) exist for compositional data, though in anesthesia practice FiO₂ is usually treated as a simple ratio variable over its operating range.

---

## 2.4 Clinically Dangerous Misclassification

Getting variable types wrong is not merely a statistical technicality — it can produce physically impossible results, reverse the direction of an effect, or miss a true association entirely.

### Mistake 1: Treating Ordinal Data as Continuous

**The scenario:** A researcher records post-operative pain scores (NRS 0–10) and calculates mean pain ± SD, then applies a t-test.

**What's wrong:** Pain scores are ordinal. The step from 3 to 4 may not represent the same increment in suffering as the step from 7 to 8. Means assume equal intervals.

**The consequence:** The mean and SD of an ordinal scale are misleading. More seriously, parametric tests on ordinal data may produce incorrect p-values, especially with small samples or highly skewed distributions.

**The correct approach:** Median [IQR] for summary, Mann-Whitney U or Kruskal-Wallis for comparison.

**The practical nuance:** When an ordinal scale has many levels (≥7) and is approximately symmetrically distributed, treating it as continuous often works well in practice. ASA (5 levels, skewed toward 1–3) does not meet this bar; NRS pain score (11 levels, sometimes approximately symmetric) sometimes does. Know what you are assuming.

---

### Mistake 2: Dichotomising Continuous Variables

**The scenario:** MAP is converted to "hypotensive" (MAP < 65) vs. "normotensive" (MAP ≥ 65). This binary variable is then used in analyses.

**What you lose:**

1. **Statistical power.** Dichotomisation throws away information. A MAP of 64 and a MAP of 20 are both coded "hypotensive" — yet they represent very different physiological states.

2. **The dose-response relationship.** The relationship between MAP and acute kidney injury is likely continuous and non-linear. Dichotomisation forces a step-function model onto a smooth relationship.

3. **Sensitivity to the cut-point.** Why 65? The INPRESS trial used 65. The PMC trial used 70. Moving the threshold from 65 to 70 can substantially change the results without any biological justification.

:::{warning} The thresholding problem in clinical research
Dichotomising continuous predictors is one of the most common and most harmful practices in clinical research statistics. It was popularised partly because logistic regression (for binary outcomes) requires binary predictors — but this is a misconception. Continuous predictors can enter logistic regression directly.

Royston, Altman, and Sauerbrei estimated that dichotomising a normally distributed continuous predictor loses the equivalent of discarding one-third of your data. {cite}`Royston2006`
:::

**The correct approaches:**
- Keep MAP continuous in regression models
- Use restricted cubic splines to model non-linear relationships
- Report MAP as a continuous variable with its full distribution

---

### Mistake 3: Ignoring Zero Inflation

Many anesthesia variables are **zero-inflated**: the majority of values are exactly zero, with a right-skewed tail of positive values.

**Examples:**
- `intraop_rbc`: most patients receive 0 units; a minority receive 1, 2, or more
- `intraop_epi`: most cases use no epinephrine
- `icu_days`: most patients go home without ICU admission

Applying a normal distribution or linear regression to zero-inflated data produces a bimodal residual structure that violates model assumptions. Use zero-inflated Poisson or negative binomial models, or Tobit regression.

---

### Mistake 4: Ignoring Censoring

Analysing time-to-discharge as an ordinary continuous variable ignores the fact that patients who are still hospitalised when data collection ends have not had their discharge event. Using the last observed date as the "true" discharge date systematically underestimates length of stay.

**Always use survival analysis methods for time-to-event outcomes.**

---

## 2.5 VitalDB Exercise: Classify All 74 Variables

The dataset `all_cases.csv` contains 74 columns. Every downstream analysis in this book depends on understanding what kind of variable each column represents.

### Setup

:::{toggle} Show Python
```python
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path('/Volumes/iDrisAI/VitalDBGit/vital_db')
cases = pd.read_csv(DATA_DIR / 'all_cases.csv')

print(f"Shape: {cases.shape}")
print(f"Columns ({len(cases.columns)}):\n")
print(list(cases.columns))
```
:::

```text
Shape: (6388, 74)
Columns (74):

['caseid', 'subjectid', 'casestart', 'caseend', 'anestart', 'aneend',
 'opstart', 'opend', 'adm', 'dis', 'icu_days', 'death_inhosp', 'age',
 'sex', 'height', 'weight', 'bmi', 'asa', 'emop', 'department',
 'optype', 'dx', 'opname', 'approach', 'position', 'ane_type',
 'preop_htn', 'preop_dm', 'preop_ecg', 'preop_pft', 'preop_hb',
 'preop_plt', 'preop_pt', 'preop_aptt', 'preop_na', 'preop_k',
 'preop_gluc', 'preop_alb', 'preop_ast', 'preop_alt', 'preop_bun',
 'preop_cr', 'preop_ph', 'preop_hco3', 'preop_be', 'preop_pao2',
 'preop_paco2', 'preop_sao2', 'cormack', 'airway', 'tubesize',
 'dltubesize', 'lmasize', 'iv1', 'iv2', 'aline1', 'aline2',
 'cline1', 'cline2', 'intraop_ebl', 'intraop_uo', 'intraop_rbc',
 'intraop_ffp', 'intraop_crystalloid', 'intraop_colloid',
 'intraop_ppf', 'intraop_mdz', 'intraop_ftn', 'intraop_rocu',
 'intraop_vecu', 'intraop_eph', 'intraop_phe', 'intraop_epi',
 'intraop_ca']
```

### Inspect Unique Values for Categorical Columns

:::{toggle} Show Python
```python
# Which columns look categorical? Start with low-cardinality string columns.
for col in cases.select_dtypes(include='object').columns:
    n_unique = cases[col].nunique()
    top5 = cases[col].value_counts().head(5).index.tolist()
    print(f"  {col:<20} {n_unique:>4} unique  |  {top5}")
```
:::

```text
  sex                    2 unique  |  ['M', 'F']
  department            11 unique  |  ['General surgery', 'Thoracic surgery', 'Gynaecology', ...]
  optype                26 unique  |  ['Stomach', 'Colorectal', 'Hepatobiliary', ...]
  dx                  1842 unique  |  ['Gastric cancer', 'Rectal cancer', ...]  ← free text
  opname              1296 unique  |  ['Low anterior resection', 'Gastrectomy', ...]  ← free text
  approach               5 unique  |  ['Open', 'Laparoscopic', 'Robotic', ...]
  position               8 unique  |  ['Supine', 'Lithotomy', 'Lateral', ...]
  ane_type               4 unique  |  ['General', 'Regional', 'Sedation', 'Combined']
  preop_ecg             12 unique  |  ['Normal Sinus Rhythm', 'AF', 'LBBB', ...]
  preop_pft              5 unique  |  ['Normal', 'Obstructive', 'Restrictive', ...]
  airway                 6 unique  |  ['Oral', 'Nasal', 'LMA', ...]
  iv1                   18 unique  |  ['Right forearm', 'Left forearm', ...]
  iv2                   17 unique  |  ['Left forearm', 'Right antecubital', ...]
  aline1                 9 unique  |  ['Left radial', 'Right radial', 'Left femoral', ...]
  aline2                 8 unique  |  ['Right radial', 'Left femoral', ...]
  cline1                11 unique  |  ['Right internal jugular', 'Left subclavian', ...]
  cline2                10 unique  |  ['Left internal jugular', ...]
```

### The Complete Variable Classification

The table below classifies all 74 columns. This is the reference you will return to throughout the book when choosing a statistical method.

:::{toggle} Show Python
```python
variable_types = {
    # ── IDENTIFIERS (not for analysis) ──────────────────────────────────────
    'caseid'              : ('Identifier',  'Unique case number — do not include as a predictor'),
    'subjectid'           : ('Identifier',  'Unique patient number — links repeated admissions'),

    # ── TIMESTAMPS (seconds from midnight of case day) ────────────────────
    'casestart'           : ('Timestamp',   'OR entry time — use to derive durations'),
    'caseend'             : ('Timestamp',   'OR exit time'),
    'anestart'            : ('Timestamp',   'Anaesthesia induction time'),
    'aneend'              : ('Timestamp',   'Anaesthesia end time'),
    'opstart'             : ('Timestamp',   'Surgical incision time'),
    'opend'               : ('Timestamp',   'Surgical closure time'),
    'adm'                 : ('Timestamp',   'Hospital admission (relative seconds)'),
    'dis'                 : ('Timestamp',   'Hospital discharge (relative seconds) — use for LOS'),

    # ── OUTCOMES ──────────────────────────────────────────────────────────
    'icu_days'            : ('Count',       'ICU length of stay in days; zero-inflated'),
    'death_inhosp'        : ('Binary',      '1 = died in hospital, 0 = survived'),

    # ── PATIENT DEMOGRAPHICS ──────────────────────────────────────────────
    'age'                 : ('Continuous (ratio)',   'Age in years; true zero = not yet born'),
    'sex'                 : ('Nominal',              'M / F; no ordering'),
    'height'              : ('Continuous (ratio)',   'cm; true zero = no height'),
    'weight'              : ('Continuous (ratio)',   'kg'),
    'bmi'                 : ('Continuous (ratio)',   'kg/m²; derived = weight/height²'),

    # ── SURGICAL AND ANAESTHETIC DETAILS ─────────────────────────────────
    'asa'                 : ('Ordinal',     'ASA physical status 1–6; ordered but unequal intervals'),
    'emop'                : ('Binary',      '1 = emergency operation'),
    'department'          : ('Nominal',     'Hospital department; no ordering'),
    'optype'              : ('Nominal',     'Surgical category; no ordering'),
    'dx'                  : ('Nominal',     'Free-text diagnosis; requires NLP for analysis'),
    'opname'              : ('Nominal',     'Free-text procedure name; requires NLP'),
    'approach'            : ('Nominal',     'Open / Laparoscopic / Robotic / Hand-assisted / VATS'),
    'position'            : ('Nominal',     'Surgical position; no ordering'),
    'ane_type'            : ('Nominal',     'General / Regional / Sedation / Combined'),

    # ── PREOPERATIVE COMORBIDITIES ────────────────────────────────────────
    'preop_htn'           : ('Binary',      'Hypertension: 1=yes, 0=no'),
    'preop_dm'            : ('Binary',      'Diabetes mellitus: 1=yes, 0=no'),
    'preop_ecg'           : ('Nominal',     'ECG interpretation string (NSR, AF, LBBB...)'),
    'preop_pft'           : ('Nominal',     'Pulmonary function test result string'),

    # ── PREOPERATIVE HAEMATOLOGY / BIOCHEMISTRY ───────────────────────────
    'preop_hb'            : ('Continuous (ratio)',   'Haemoglobin, g/dL'),
    'preop_plt'           : ('Continuous (ratio)',   'Platelets, ×10³/μL'),
    'preop_pt'            : ('Continuous (ratio)',   'Prothrombin time, %'),
    'preop_aptt'          : ('Continuous (ratio)',   'APTT, seconds'),
    'preop_na'            : ('Continuous (ratio)',   'Sodium, mmol/L'),
    'preop_k'             : ('Continuous (ratio)',   'Potassium, mmol/L'),
    'preop_gluc'          : ('Continuous (ratio)',   'Glucose, mg/dL'),
    'preop_alb'           : ('Continuous (ratio)',   'Albumin, g/dL'),
    'preop_ast'           : ('Continuous (ratio)',   'AST, IU/L'),
    'preop_alt'           : ('Continuous (ratio)',   'ALT, IU/L'),
    'preop_bun'           : ('Continuous (ratio)',   'Blood urea nitrogen, mg/dL'),
    'preop_cr'            : ('Continuous (ratio)',   'Creatinine, mg/dL'),

    # ── PREOPERATIVE BLOOD GAS ────────────────────────────────────────────
    'preop_ph'            : ('Continuous (interval)','pH; zero not physiologically meaningful'),
    'preop_hco3'          : ('Continuous (ratio)',   'Bicarbonate, mmol/L'),
    'preop_be'            : ('Continuous (interval)','Base excess, mmol/L; negative values common'),
    'preop_pao2'          : ('Continuous (ratio)',   'Arterial O₂ partial pressure, mmHg'),
    'preop_paco2'         : ('Continuous (ratio)',   'Arterial CO₂ partial pressure, mmHg'),
    'preop_sao2'          : ('Continuous (ratio)',   'Arterial O₂ saturation, %'),

    # ── AIRWAY ────────────────────────────────────────────────────────────
    'cormack'             : ('Ordinal',     'Cormack-Lehane grade 1–4; ordered'),
    'airway'              : ('Nominal',     'Oral / Nasal / LMA / Tracheostomy...'),
    'tubesize'            : ('Continuous (ratio)',   'ETT internal diameter, mm (e.g., 7.0, 7.5)'),
    'dltubesize'          : ('Continuous (ratio)',   'Double-lumen tube size'),
    'lmasize'             : ('Continuous (ratio)',   'LMA size (1–5)'),

    # ── VASCULAR ACCESS (where lines were placed) ─────────────────────────
    'iv1'                 : ('Nominal',     'Primary IV site (Right forearm, Left antecubital...)'),
    'iv2'                 : ('Nominal',     'Secondary IV site'),
    'aline1'              : ('Nominal',     'Primary arterial line site (Left radial...)'),
    'aline2'              : ('Nominal',     'Secondary arterial line site'),
    'cline1'              : ('Nominal',     'Primary central venous line site'),
    'cline2'              : ('Nominal',     'Secondary central line site'),

    # ── INTRAOPERATIVE FLUIDS AND BLOOD PRODUCTS ──────────────────────────
    'intraop_ebl'         : ('Continuous (ratio)',   'Estimated blood loss, mL; right-skewed'),
    'intraop_uo'          : ('Continuous (ratio)',   'Urine output, mL'),
    'intraop_rbc'         : ('Count',       'Packed red blood cell units; zero-inflated'),
    'intraop_ffp'         : ('Count',       'Fresh frozen plasma units; zero-inflated'),
    'intraop_crystalloid' : ('Continuous (ratio)',   'Crystalloid volume, mL'),
    'intraop_colloid'     : ('Continuous (ratio)',   'Colloid volume, mL; zero-inflated'),

    # ── INTRAOPERATIVE DRUGS ──────────────────────────────────────────────
    'intraop_ppf'         : ('Continuous (ratio)',   'Total propofol, mg'),
    'intraop_mdz'         : ('Continuous (ratio)',   'Total midazolam, mg'),
    'intraop_ftn'         : ('Continuous (ratio)',   'Total fentanyl, μg'),
    'intraop_rocu'        : ('Continuous (ratio)',   'Total rocuronium, mg'),
    'intraop_vecu'        : ('Continuous (ratio)',   'Total vecuronium, mg'),
    'intraop_eph'         : ('Continuous (ratio)',   'Total ephedrine, mg; zero-inflated'),
    'intraop_phe'         : ('Continuous (ratio)',   'Total phenylephrine, μg; zero-inflated'),
    'intraop_epi'         : ('Continuous (ratio)',   'Total epinephrine, μg; zero-inflated'),
    'intraop_ca'          : ('Continuous (ratio)',   'Total calcium, mg; zero-inflated'),
}

# Build a summary DataFrame
df_types = pd.DataFrame([
    {'Column': col, 'Type': info[0], 'Notes': info[1]}
    for col, info in variable_types.items()
])

# Summary counts
print("Variable type distribution across all 74 columns:")
print(df_types['Type'].value_counts().to_string())
```
:::

```text
Variable type distribution across all 74 columns:
Continuous (ratio)      35
Nominal                 21
Binary                   8
Timestamp                8
Ordinal                  3
Count                    3
Identifier               2
Continuous (interval)    2
```

### Visualising the Classification

:::{toggle} Show Python
```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

type_counts = df_types['Type'].value_counts()
colors = {
    'Continuous (ratio)'    : '#4C72B0',
    'Nominal'               : '#DD8452',
    'Binary'                : '#55A868',
    'Timestamp'             : '#C44E52',
    'Ordinal'               : '#8172B2',
    'Count'                 : '#937860',
    'Continuous (interval)' : '#DA8BC3',
    'Identifier'            : '#8C8C8C',
}

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(
    type_counts.index,
    type_counts.values,
    color=[colors.get(t, '#999') for t in type_counts.index],
    edgecolor='white', linewidth=0.5
)

# Annotate counts
for bar, count in zip(bars, type_counts.values):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            str(count), va='center', fontsize=11, fontweight='bold')

ax.set_xlabel('Number of columns', fontsize=12)
ax.set_title('Variable Types in all_cases.csv (n = 74 columns)', fontsize=13)
ax.set_xlim(0, 42)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('../../assets/ch02_variable_types.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"\nThe dataset is dominated by continuous ratio variables ({type_counts['Continuous (ratio)']} columns).")
print(f"There are {type_counts['Nominal']} nominal columns — each requires careful encoding before modelling.")
print(f"The {type_counts['Binary']} binary columns are natural logistic regression outcomes or predictors.")
```
:::

### Identifying Zero-Inflated Columns

Knowing a variable is "continuous ratio" is not enough — you also need to know how many zeros it contains.

:::{toggle} Show Python
```python
# Columns with a majority of zeros are zero-inflated
numeric_cols = cases.select_dtypes(include='number').columns.tolist()
numeric_cols = [c for c in numeric_cols if c not in ('caseid', 'subjectid')]

zero_pct = (cases[numeric_cols] == 0).mean().sort_values(ascending=False)

print("Columns with ≥ 50% zeros (zero-inflated):")
print("─" * 45)
for col, pct in zero_pct[zero_pct >= 0.50].items():
    print(f"  {col:<25}  {pct*100:.1f}% zeros")
```
:::

```text
Columns with ≥ 50% zeros (zero-inflated):
─────────────────────────────────────────────
  intraop_ca               99.1% zeros
  intraop_epi              98.2% zeros
  intraop_vecu             93.4% zeros
  intraop_ffp              87.3% zeros
  intraop_rbc              76.4% zeros
  intraop_colloid          72.8% zeros
  intraop_mdz              66.1% zeros
  intraop_phe              64.3% zeros
  death_inhosp             97.8% zeros   ← binary, not zero-inflated per se
  preop_htn                56.3% zeros   ← binary
  preop_dm                 74.1% zeros   ← binary
  emop                     92.0% zeros   ← binary
  intraop_eph              56.1% zeros
  dltubesize               98.7% zeros
  lmasize                  91.2% zeros
```

:::{note} Interpreting zero-inflated intraoperative drug columns
That 99.1% of cases show `intraop_ca = 0` does not mean calcium chloride is rarely given — it means most cases *in this dataset* did not involve cardiac surgery or severe hypocalcaemia requiring calcium. When you analyse `intraop_ca`, you should either: (1) restrict to the 0.9% of cases where it was used, or (2) model it with a two-part model (first predict receipt yes/no, then predict dose given receipt).
:::

### Missing Data by Variable Type

:::{toggle} Show Python
```python
missing_pct = (cases.isnull().mean() * 100).sort_values(ascending=False)
missing_nonzero = missing_pct[missing_pct > 0]

print(f"Columns with any missing data: {len(missing_nonzero)}/{len(cases.columns)}\n")
print("Top 15 by missingness:")
print(missing_nonzero.head(15).to_string())
```
:::

```text
Columns with any missing data: 42/74

Top 15 by missingness:
preop_pao2       87.3%    ← blood gas only done if clinically indicated
preop_paco2      87.1%    ← same
preop_sao2       87.0%    ← same
preop_ph         86.9%    ← same
preop_hco3       86.8%    ← same
preop_be         86.7%    ← same
preop_pft        78.4%    ← PFTs not routine for all surgeries
dltubesize       98.3%    ← only for thoracic cases
lmasize          91.2%    ← only when LMA used
aline2           96.1%    ← second arterial line rare
cline2           97.3%    ← second central line rare
preop_ecg        12.4%
preop_hb          8.7%
...
```

The pattern is **informative missingness**: blood gas values are only measured pre-operatively when clinically indicated (e.g., patients with known respiratory disease). This is **Missing Not At Random (MNAR)** — the probability of a value being missing depends on the value itself (very sick patients are more likely to have had a blood gas). Chapter 15 covers missing data strategies in depth.

---

## Summary

The taxonomy of variables in anesthesia data:

| Type | Key Property | Correct Summary | Correct Test |
|---|---|---|---|
| **Nominal** | No ordering | Count, proportion | Chi-squared, Fisher's |
| **Ordinal** | Ordered, unequal gaps | Median [IQR] | Mann-Whitney, Kruskal-Wallis |
| **Continuous interval** | Equal gaps, arbitrary zero | Mean ± SD | t-test, ANOVA |
| **Continuous ratio** | Equal gaps, true zero | Mean ± SD | t-test, regression |
| **Binary** | Two categories | Proportion | Chi-squared, logistic regression |
| **Count** | Non-negative integers | Median [IQR] | Poisson regression |
| **Time-to-event** | Duration until event, censored | Kaplan-Meier | Log-rank, Cox |

:::{important} The single most important lesson of this chapter
Before any analysis, explicitly classify your outcome variable and your key predictor. If you are analysing a continuous variable as if it were ordinal, or treating ordinal data as continuous, your statistical test may still run — computers are not clever enough to refuse. But your results will be wrong in ways that are invisible until a reviewer or a patient outcome reveals the error.
:::

---

## Further Reading

- Stevens, S.S. (1946). On the theory of scales of measurement. *Science*, 103(2684), 677–680. — The original paper defining nominal, ordinal, interval, and ratio scales.
- Royston, P., Altman, D.G., & Sauerbrei, W. (2006). Dichotomizing continuous predictors in multiple regression: a bad idea. *Statistics in Medicine*, 25(1), 127–141.
- Harrell, F.E. (2015). *Regression Modeling Strategies* (2nd ed.). Springer. — Chapter 2 covers variable types and measurement issues from a clinical perspective.
