# Chapter 3 — Descriptive Statistics: Summarising Your Patients

> *"You cannot understand a forest by studying a single tree — but if you study only the average tree, you will miss the fire."*

---

Before you build a model, run a test, or draw a conclusion, you must first **describe your data**. Descriptive statistics are not a preliminary formality. They are the step that catches errors, reveals the unexpected, and anchors every subsequent analysis in reality.

Consider the opening question of any clinical audit: what kind of patients did we operate on? In the anaesthetic world, this means: what was their age distribution? How sick were they (ASA class)? How long did the operations take? How much blood did they lose? How much propofol did they receive? These are all descriptive questions — and getting them right is the difference between a trustworthy analysis and one that collapses under reviewer scrutiny.

The VitalDB dataset provides 6,388 cases. By the end of this chapter, you will know how to summarise each of those cases into a coherent, defensible **Table 1** — the standard characterisation table that opens every clinical research paper.

---

## 3.1 Measures of Central Tendency

A measure of central tendency answers a deceptively simple question: *what is the typical value?*

There are three candidates — mean, median, and mode — and choosing the wrong one is one of the most common errors in clinical reporting.

### The Mean

The arithmetic mean is the sum of all values divided by the count:

$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

The mean uses every data point equally. Its strength is also its weakness: **it is sensitive to extreme values**. A single patient who lost 8,000 mL of blood pulls the mean blood loss up for the entire cohort.

**Clinical example:** Suppose blood loss in 10 patients (mL) is:

```
50, 100, 80, 120, 60, 70, 90, 100, 85, 5000
```

Mean = 675 mL. But nine of the ten patients lost less than 120 mL. The mean is dominated by one catastrophic haemorrhage and gives a completely misleading impression of the typical case.

### The Median

The median is the middle value when data are sorted. For *n* observations, it is the value at position (*n* + 1) / 2 (or the mean of the two central values when *n* is even).

For the blood loss example above, the median is 87.5 mL — a far more useful summary of the typical patient.

**When to prefer the median:**
- The distribution is skewed (blood loss, drug doses, lab values with long tails)
- Outliers are real and cannot be excluded but should not dominate the summary
- The variable is ordinal (always use median for ASA class)

### The Mode

The mode is the most frequently occurring value. It is rarely used for continuous clinical data but is the only valid measure of central tendency for **nominal variables**: the modal anaesthesia type, the modal surgical department, the modal ASA class.

### Why the Median Vasopressor Dose Matters More Than the Mean

Ephedrine administration in VitalDB is heavily zero-inflated: most patients receive none. Among those who do receive it, doses range from a single 4 mg bolus to repeated doses totalling 60 mg. The distribution is bimodal (a spike at zero, then a right-skewed non-zero distribution). The mean collapses these two groups into a single misleading number.

The correct approach is to report:

1. **Proportion who received any** (e.g., "ephedrine was used in 31% of cases")
2. **Median [IQR] among those who received it** (e.g., "8 mg [4–16] in those who received it")

This two-part structure applies to any zero-inflated clinical variable — colloid volume, vasopressor dose, blood transfusion units. Report the zero separately.

---

## 3.2 Measures of Spread

Knowing the typical value is not enough. Two cohorts with identical medians can have completely different distributions. Spread quantifies this variability.

### Range

The range is simply maximum − minimum. It is easy to interpret but fragile: a single outlier at either extreme changes it dramatically. Use range only to flag the extent of data — never as the primary spread summary.

### Interquartile Range (IQR)

The IQR is the distance between the 25th percentile (Q1) and 75th percentile (Q3):

$$\text{IQR} = Q_3 - Q_1$$

It describes the middle 50% of the data and is resistant to outliers. Report it alongside the median:

> "Median blood loss: 100 mL [IQR 50–300]"

The brackets and dash convention ([Q1–Q3]) is standard in clinical journals. Some journals use (Q1, Q3) with a comma — check the target journal's style.

### Standard Deviation

The standard deviation (SD) is the average distance of each observation from the mean:

$$s = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2}$$

The $(n-1)$ denominator (Bessel's correction) makes $s$ an unbiased estimator of the population standard deviation when working from a sample. For large $n$ (as in VitalDB), the difference between $n$ and $n-1$ is negligible.

**SD is appropriate when the distribution is approximately normal (symmetric).** When data are normally distributed, approximately:
- 68% of observations fall within ±1 SD of the mean
- 95% fall within ±2 SD
- 99.7% fall within ±3 SD

**Reporting convention:** mean ± SD (e.g., "age 58.2 ± 12.4 years")

:::{important} Mean ± SD vs. median [IQR] — the most common reporting error
Reporting mean ± SD for skewed data implies a symmetric distribution that does not exist. For propofol dose (right-skewed, zero-inflated), reporting mean ± SD will routinely produce an "upper bound" of mean + 2SD that exceeds the maximum dose any real patient could receive, and a "lower bound" that is negative — physically impossible. Always check skewness before choosing your summary statistic.
:::

### Variance

Variance is SD². It is the foundation of many statistical methods (ANOVA, regression, mixed models) but has the wrong units for direct interpretation (mmHg² for blood pressure — meaningless clinically). Report SD, not variance.

### Coefficient of Variation

The coefficient of variation (CV) expresses SD as a percentage of the mean:

$$\text{CV} = \frac{s}{\bar{x}} \times 100\%$$

It allows comparison of variability across variables measured on different scales. Is MAP more variable than heart rate? CV answers this in a dimensionless way.

**Clinical use:** In haemodynamic monitoring, CV of MAP over 10-minute windows can quantify haemodynamic instability — high CV patients may require more active management even if their average MAP is within target range.

| Variable | Mean | SD | CV |
|---|---|---|---|
| MAP (mmHg) | 85 | 14 | 16% |
| Heart rate (bpm) | 72 | 13 | 18% |
| SpO₂ (%) | 98.5 | 1.2 | 1.2% |
| Propofol infusion rate (mg/kg/hr) | 6.8 | 3.4 | 50% |

SpO₂ has the lowest CV (tightly regulated, narrow physiological range). Propofol infusion rate has the highest CV (anaesthetists vary dosing considerably between patients and over time). Both are real and biologically meaningful signals about each variable's nature.

---

## 3.3 Describing Distributions

Summary statistics compress data into one or two numbers. They are useful but lossy. The distribution tells you the full shape of the data — and shape matters.

### Histograms and Density Plots

A histogram divides the range of a variable into bins and counts how many observations fall in each bin. A density plot is a smoothed version that estimates the underlying probability density function.

**What to look for:**
- **Symmetry:** does the distribution look the same on both sides of the peak?
- **Number of peaks (modes):** unimodal, bimodal, or multimodal?
- **Tails:** does the distribution extend more to the right (positive skew) or left (negative skew)?
- **Outliers:** isolated bars far from the main body of the distribution

**Common distributions in anaesthesia data:**

| Variable | Typical Shape | Appropriate Summary |
|---|---|---|
| Patient age | Roughly normal (slight negative skew in surgical populations) | Mean ± SD |
| BMI | Mildly right-skewed | Mean ± SD or median [IQR] |
| ASA class | Heavily left-skewed (most patients are ASA 1–2) | Median [IQR] |
| Surgical duration | Strongly right-skewed | Median [IQR] |
| Blood loss | Strongly right-skewed, zero-inflated | Median [IQR]; % with EBL > threshold |
| Propofol dose | Right-skewed, zero-inflated (volatile GA cases have 0 propofol) | Separate TIVA vs. volatile groups |
| Phenylephrine dose | Bimodal zero-inflation | % used + median [IQR] among users |

### Skewness and Kurtosis

**Skewness** measures the asymmetry of a distribution. Positive skew means a long right tail (most values are small, but a few are very large — classic for blood loss, drug doses, ICU length of stay). Negative skew means a long left tail.

$$\text{Skewness} = \frac{1}{n} \sum_{i=1}^{n} \left(\frac{x_i - \bar{x}}{s}\right)^3$$

A rule of thumb:
- |skewness| < 0.5: approximately symmetric → mean ± SD is appropriate
- 0.5 < |skewness| < 1: moderately skewed → consider median [IQR]
- |skewness| > 1: substantially skewed → median [IQR] is strongly preferred

**Kurtosis** measures the "tailedness" of a distribution — whether extreme values are more or less common than a normal distribution would predict. High kurtosis (leptokurtic) means heavy tails and sharp peaks; low kurtosis (platykurtic) means light tails and flat peaks.

Kurtosis matters in anaesthesia when modelling rare adverse events: a variable with high kurtosis has more extreme values in the tails than a normal distribution would suggest, which affects risk estimates.

### The Normal (Gaussian) Distribution

The normal distribution is the bell-shaped, symmetric distribution described entirely by its mean (μ) and standard deviation (σ). It arises when a variable is the sum of many independent random effects — which explains why height and weight in a general population are approximately normal (influenced by hundreds of genetic and environmental factors independently).

**When does the normal distribution hold in anaesthesia?**

| Variable | Approximately Normal? |
|---|---|
| Patient age (surgical cohort) | Yes — use mean ± SD |
| BMI | Borderline — mild right skew in most populations |
| Preoperative haemoglobin | Approximately normal, with a left tail from anaemic patients |
| Surgical duration | No — strongly right-skewed |
| Blood loss | No — strongly right-skewed and zero-inflated |
| Propofol total dose | No — zero-inflated, multimodal |
| ICU length of stay | No — strongly right-skewed; many patients have 0 days |

:::{note}
A common mistake is to assume that large samples *make* a variable normally distributed. The Central Limit Theorem guarantees that *sample means* are normally distributed as $n$ increases — not the raw data themselves. In a cohort of 6,000 patients, blood loss is still right-skewed. The mean of blood loss across many studies of 6,000 patients each would be normally distributed. These are different things.
:::

### Violin Plots: More Information Than a Boxplot

A boxplot summarises a distribution through five numbers (minimum, Q1, median, Q3, maximum) and is excellent for side-by-side group comparison. But it cannot reveal bimodality, granularity, or the exact shape of the tails.

A violin plot combines a boxplot with a mirrored density estimate, showing the full distribution shape. For comparing blood loss across ASA classes, a violin plot reveals not just the different medians but whether the distributions are differently shaped — which matters for choosing statistical tests.

---

## 3.4 Describing Associations

After describing each variable individually, the next question is: **do two variables vary together?**

### Cross-tabulation for Categorical Variables

When both variables are categorical, the primary tool is the **contingency table** (cross-tabulation): a grid showing the count and percentage in each combination of categories.

**Example:** Does mortality differ by anaesthesia type?

| Anaesthesia Type | Alive | Dead | Mortality |
|---|---|---|---|
| General | 5,432 | 38 | 0.69% |
| Regional | 812 | 4 | 0.49% |
| Sedation | 89 | 15 | 14.4% |

The table immediately reveals that the sedation group has dramatically higher apparent mortality — but this is almost certainly because sedation is chosen for the highest-risk, most compromised patients who cannot safely receive general anaesthesia, not because sedation itself is harmful. This is **confounding by indication**, and it is one of the most important concepts in clinical data analysis. Chapter 19 deals with it formally.

Reading a cross-tabulation should always prompt the question: *is this association causal, or is it because a third variable is driving both?*

### Scatter Plots for Continuous Variables

When both variables are continuous, the scatter plot is the most informative first step. Before computing any correlation coefficient, look at the scatter plot. The reason: correlation coefficients summarise only one aspect of the relationship — its linearity and strength — but a scatter plot reveals:

- **Non-linearity:** the relationship exists but is curved
- **Heteroscedasticity:** the spread of one variable changes across levels of the other
- **Outliers:** a few extreme points driving an apparent correlation
- **Clusters:** distinct sub-populations with different relationships

**A famous cautionary example is Anscombe's Quartet** — four datasets with identical means, SDs, and Pearson correlations but completely different scatter plot shapes, including one with a single outlier driving the entire apparent association.

### Correlation Coefficients

A correlation coefficient quantifies the strength and direction of a linear (or monotonic) relationship between two continuous variables. It ranges from −1 (perfect negative) through 0 (no association) to +1 (perfect positive).

**Pearson correlation ($r$)** — for normally distributed continuous variables:

$$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{(n-1) \cdot s_x \cdot s_y}$$

Pearson $r$ is sensitive to outliers and assumes a linear relationship.

**Spearman rank correlation ($\rho$)** — for ordinal variables or non-normally distributed continuous variables:

$$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2-1)}$$

where $d_i$ is the difference in ranks. Spearman converts both variables to their ranks first, making it robust to outliers and valid for any monotonic relationship (not just linear).

**Choosing between Pearson and Spearman in anaesthesia:**

| Scenario | Use |
|---|---|
| Preoperative Hb vs. intraoperative transfusion (both continuous, approximately normal) | Pearson |
| ASA class vs. surgical duration (ordinal vs. continuous) | Spearman |
| Propofol dose vs. BIS (continuous, but propofol dose is right-skewed) | Spearman |
| Log(blood loss) vs. surgical duration (after log transformation) | Pearson |

:::{important} Correlation is not causation — and correlation magnitude needs context
An $r = 0.3$ between propofol dose and blood loss sounds modest. Over a range of doses from 0 to 2,000 mg, it may represent a clinically meaningful gradient. An $r = 0.8$ between two preoperative lab values may simply reflect that they are both elevated in liver disease — correlation does not mean one causes the other. Always interpret correlation with clinical context.
:::

---

## 3.5 Presenting Data in Clinical Tables

Clinical papers open with a **Table 1** — a standardised characterisation of the study cohort (or, in comparative studies, side-by-side characterisation of two or more groups). Understanding how to construct and read a Table 1 is a core competency for any clinical researcher.

### The Structure of Table 1

A well-constructed Table 1 presents:

| Column | Content |
|---|---|
| Variable | Name of the variable, with units |
| Overall | Summary for the full cohort |
| Group A | Summary for subgroup A (e.g., elective surgery) |
| Group B | Summary for subgroup B (e.g., emergency surgery) |
| P value | Result of group comparison test |

### Reporting Rules

The summary statistic depends on the variable type:

| Variable Type | Report As | Example |
|---|---|---|
| Continuous, approximately normal | Mean ± SD | Age 58.2 ± 12.4 years |
| Continuous, skewed | Median [Q1–Q3] | Blood loss 100 [50–300] mL |
| Binary | n (%) | Female 2,614 (40.9%) |
| Nominal with >2 categories | n (%) for each category | — |
| Ordinal | Median [Q1–Q3] | ASA class 2 [2–3] |

**The p-value column in Table 1** is a source of ongoing debate. Many journals still require it, but methodologists increasingly argue it is inappropriate for a descriptive table — you are not testing hypotheses about baseline characteristics, you are describing them. A large study will produce statistically significant differences in baseline variables that are clinically meaningless (e.g., a 0.3-year difference in mean age with p < 0.001). A better approach is to report the **standardised mean difference** (SMD) as a measure of balance — SMD < 0.1 is typically considered negligible imbalance.

### Missing Data

Table 1 must report missing data. The standard format is to include "(n = X missing)" or "available in X%" in the variable name, or to include a separate column showing the sample size for each variable. Presenting the complete-case analysis without acknowledging missingness is a transparency failure — and in the VitalDB dataset, many variables have substantial missingness (propofol dose is 0 for volatile-anaesthesia cases; preoperative lab values are missing when not clinically indicated).

---

## VitalDB Exercise: A Table 1 for the Cohort

We will now construct a complete descriptive analysis of the VitalDB cohort. This is the Table 1 for any paper using this dataset.

### Setup and Data Loading

:::{toggle} Show Python
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── Paths ────────────────────────────────────────────────────────────────────
from pathlib import Path
DATA_DIR = Path('/Volumes/iDrisAI/VitalDBGit/vital_db')

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_DIR / 'all_cases.csv')
print(f"Cases loaded: {len(df):,}")
print(f"Columns: {df.shape[1]}")
print(f"\nColumn names:\n{list(df.columns)}")
```
:::

### Derive Surgical Duration

:::{toggle} Show Python
```python
# opstart and opend are integer seconds elapsed from case start — not datetime strings
# Surgical duration in minutes = (opend − opstart) / 60
df['op_dur_min'] = (df['opend'] - df['opstart']) / 60

# Sanity check — flag implausible values
print(f"Negative surgical durations: {(df['op_dur_min'] < 0).sum()}")
print(f"Durations > 12 hours: {(df['op_dur_min'] > 720).sum()}")
print(f"\nSurgical duration (minutes):")
print(df['op_dur_min'].describe().round(1))
```
:::

:::{note}
Some cases may have missing or implausible timestamps. In real analysis, exclude cases where `op_dur_min < 5` (likely data entry errors) or where the timestamp is missing. Removing implausible records is not "cherry-picking" — it is data quality control. Document every exclusion in a flow diagram.
:::

### Derive Fluid Balance

:::{toggle} Show Python
```python
# Total fluid input = crystalloid + colloid
df['total_fluid_in'] = df['intraop_crystalloid'].fillna(0) + df['intraop_colloid'].fillna(0)

# Fluid balance = total in − urine output (simplified; blood loss contributes to output)
# This is a rough estimate — accurate balance requires blood transfusion and surgical drainage
df['fluid_balance'] = df['total_fluid_in'] - df['intraop_uo'].fillna(0)

print("Fluid balance (mL) — all cases:")
print(df['fluid_balance'].describe().round(0))
```
:::

### Descriptive Statistics: Continuous Variables

:::{toggle} Show Python
```python
def describe_continuous(series, label, normal=True):
    """
    Summarise a continuous variable.
    normal=True  → mean ± SD (for approximately normal distributions)
    normal=False → median [IQR] (for skewed distributions)
    """
    n       = series.count()
    missing = series.isna().sum()
    skew    = series.skew()

    if normal:
        summary = f"{series.mean():.1f} ± {series.std():.1f}"
    else:
        q1, med, q3 = series.quantile([0.25, 0.50, 0.75])
        summary = f"{med:.0f} [{q1:.0f}–{q3:.0f}]"

    print(f"{label:<35} n={n:>5,}  missing={missing:>4,}  "
          f"skew={skew:>5.2f}  {summary}")

print(f"\n{'Variable':<35} {'n':>7}  {'missing':>9}  {'skew':>7}  Summary")
print("─" * 80)

describe_continuous(df['age'],           'Age (years)',                  normal=True)
describe_continuous(df['bmi'],           'BMI (kg/m²)',                  normal=True)
describe_continuous(df['op_dur_min'],    'Surgical duration (min)',       normal=False)
describe_continuous(df['intraop_ebl'],   'Blood loss (mL)',               normal=False)
describe_continuous(df['intraop_ppf'],   'Propofol dose (mg)',            normal=False)
describe_continuous(df['intraop_ftn'],   'Fentanyl dose (μg)',            normal=False)
describe_continuous(df['intraop_crystalloid'], 'Crystalloid (mL)',        normal=False)
describe_continuous(df['intraop_uo'],    'Urine output (mL)',             normal=False)
describe_continuous(df['fluid_balance'], 'Fluid balance (mL)',            normal=False)
describe_continuous(df['icu_days'],      'ICU length of stay (days)',     normal=False)
```
:::

### Descriptive Statistics: Categorical Variables

:::{toggle} Show Python
```python
def describe_categorical(series, label, top_n=None):
    """Frequency table for a categorical variable."""
    vc = series.value_counts(dropna=False)
    n_missing = series.isna().sum()
    n_valid   = series.count()
    print(f"\n{label}  (n={n_valid:,}, missing={n_missing:,})")
    print("─" * 50)
    for cat, count in vc.head(top_n).items():
        pct = count / len(series) * 100
        print(f"  {str(cat):<30} {count:>5,}  ({pct:.1f}%)")

describe_categorical(df['sex'],      'Sex')
describe_categorical(df['asa'],      'ASA class')
describe_categorical(df['ane_type'], 'Anaesthesia type')
describe_categorical(df['emop'],     'Emergency surgery')
describe_categorical(df['department'], 'Surgical department', top_n=8)
```
:::

### Zero-inflation Check: Drug Administration Variables

:::{toggle} Show Python
```python
zero_inflated_vars = {
    'intraop_ppf'  : 'Propofol',
    'intraop_ftn'  : 'Fentanyl',
    'intraop_eph'  : 'Ephedrine',
    'intraop_phe'  : 'Phenylephrine',
    'intraop_epi'  : 'Epinephrine',
    'intraop_rocu' : 'Rocuronium',
    'intraop_colloid': 'Colloid',
    'intraop_rbc'  : 'RBC transfusion',
}

print(f"\n{'Drug / Fluid':<25} {'% receiving any':>16}  "
      f"{'Median dose (receivers)':>24}  {'IQR':>20}")
print("─" * 90)

for col, name in zero_inflated_vars.items():
    if col not in df.columns:
        continue
    series    = df[col].fillna(0)
    pct_used  = (series > 0).mean() * 100
    receivers = series[series > 0]
    if len(receivers) > 0:
        med = receivers.median()
        q1  = receivers.quantile(0.25)
        q3  = receivers.quantile(0.75)
        dose_str = f"{med:.0f}  [{q1:.0f}–{q3:.0f}]"
    else:
        dose_str = "—"
    print(f"{name:<25} {pct_used:>15.1f}%  {dose_str:>44}")
```
:::

### Distribution Plots: Visualising the Cohort

:::{toggle} Show Python
```python
fig = plt.figure(figsize=(14, 10))
fig.suptitle('VitalDB Cohort — Key Variable Distributions', fontsize=14, fontweight='bold', y=1.01)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

plot_vars = [
    ('age',              'Age (years)',              True,  gs[0, 0]),
    ('bmi',              'BMI (kg/m²)',              True,  gs[0, 1]),
    ('op_dur_min',       'Surgical Duration (min)',  False, gs[0, 2]),
    ('intraop_ebl',      'Blood Loss (mL)',          False, gs[1, 0]),
    ('intraop_ppf',      'Propofol Dose (mg)',       False, gs[1, 1]),
    ('intraop_crystalloid', 'Crystalloid (mL)',      False, gs[1, 2]),
]

for col, title, is_normal, pos in plot_vars:
    ax = fig.add_subplot(pos)
    data = df[col].dropna()
    data = data[data >= 0]  # exclude negative values (data errors)

    # Cap extreme outliers at 99th percentile for visualisation
    cap = data.quantile(0.99)
    data_capped = data[data <= cap]

    ax.hist(data_capped, bins=40, color='#4C72B0', edgecolor='white',
            linewidth=0.4, alpha=0.85)

    # Overlay mean or median
    if is_normal:
        ax.axvline(data.mean(), color='#C44E52', linewidth=1.8, linestyle='--',
                   label=f'Mean {data.mean():.1f}')
        ax.legend(fontsize=8, frameon=False)
    else:
        med = data.median()
        q1, q3 = data.quantile(0.25), data.quantile(0.75)
        ax.axvline(med, color='#C44E52', linewidth=1.8, linestyle='--',
                   label=f'Median {med:.0f}')
        ax.axvspan(q1, min(q3, cap), alpha=0.15, color='#C44E52', label='IQR')
        ax.legend(fontsize=8, frameon=False)

    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlabel('Value', fontsize=9)
    ax.set_ylabel('Cases', fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=8)
    ax.set_title(f'{title}\n(shown up to 99th %ile)', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()
```
:::

### Association Analysis: Surgical Duration vs. Blood Loss

:::{toggle} Show Python
```python
# Filter to cases with valid values and cap extreme outliers for plotting
mask = (
    df['op_dur_min'].notna() & df['intraop_ebl'].notna() &
    (df['op_dur_min'] > 0) & (df['intraop_ebl'] >= 0) &
    (df['op_dur_min'] < 600) & (df['intraop_ebl'] < 5000)
)
sub = df[mask].copy()

# Compute Spearman correlation (both variables are right-skewed)
rho, pval = stats.spearmanr(sub['op_dur_min'], sub['intraop_ebl'])

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Surgical Duration vs. Blood Loss', fontsize=12, fontweight='bold')

# Raw scatter
ax = axes[0]
ax.scatter(sub['op_dur_min'], sub['intraop_ebl'],
           alpha=0.12, s=8, color='#4C72B0', rasterized=True)
ax.set_xlabel('Surgical Duration (min)', fontsize=10)
ax.set_ylabel('Blood Loss (mL)', fontsize=10)
ax.set_title(f'Raw scale\nSpearman ρ = {rho:.3f}, p {"< 0.001" if pval < 0.001 else f"= {pval:.3f}"}',
             fontsize=9)
ax.spines[['top', 'right']].set_visible(False)

# Log-log scatter (reveals relationship more clearly for skewed data)
ax = axes[1]
log_dur = np.log1p(sub['op_dur_min'])
log_ebl = np.log1p(sub['intraop_ebl'])
r_log, p_log = stats.pearsonr(log_dur, log_ebl)

ax.scatter(log_dur, log_ebl,
           alpha=0.12, s=8, color='#55A868', rasterized=True)
# Regression line on log scale
m, b = np.polyfit(log_dur, log_ebl, 1)
x_line = np.linspace(log_dur.min(), log_dur.max(), 200)
ax.plot(x_line, m * x_line + b, color='#C44E52', linewidth=2)
ax.set_xlabel('log(Surgical Duration + 1)', fontsize=10)
ax.set_ylabel('log(Blood Loss + 1)', fontsize=10)
ax.set_title(f'Log–log scale\nPearson r = {r_log:.3f} (after log transform)', fontsize=9)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.show()

print(f"\nSpearman ρ (raw):        {rho:.3f}  (p {'< 0.001' if pval < 0.001 else f'{pval:.4f}'})")
print(f"Pearson r (log-log):     {r_log:.3f}  (p {'< 0.001' if p_log < 0.001 else f'{p_log:.4f}'})")
print("\nInterpretation: longer operations tend to have higher blood loss,")
print("but the relationship is weak — procedure type is a stronger predictor.")
```
:::

### Building the Table 1

:::{toggle} Show Python
```python
# ── Stratify by emergency vs. elective ──────────────────────────────────────
elective  = df[~df['emop'].astype(bool)]
emergency = df[df['emop'].astype(bool)]

print(f"\nCohort: {len(df):,} total  |  {len(elective):,} elective ({len(elective)/len(df)*100:.1f}%)  "
      f"|  {len(emergency):,} emergency ({len(emergency)/len(df)*100:.1f}%)")
print()

# ── Table 1 function ─────────────────────────────────────────────────────────
def table1_row_continuous(col, label, groups, skewed=False):
    """Print one Table 1 row for a continuous variable."""
    row = f"  {label:<40}"
    for name, grp in groups:
        s = grp[col].dropna()
        if skewed:
            q1, med, q3 = s.quantile([0.25, 0.50, 0.75])
            row += f"  {med:.0f} [{q1:.0f}–{q3:.0f}]".ljust(22)
        else:
            row += f"  {s.mean():.1f} ± {s.std():.1f}".ljust(22)
    # Comparison test
    vals = [grp[col].dropna() for _, grp in groups]
    if skewed:
        stat, p = stats.mannwhitneyu(vals[0], vals[1], alternative='two-sided')
    else:
        stat, p = stats.ttest_ind(vals[0], vals[1])
    p_str = "< 0.001" if p < 0.001 else f"{p:.3f}"
    print(row + f"  p {p_str}")

def table1_row_binary(col, label, groups, true_val=1):
    """Print one Table 1 row for a binary variable."""
    row = f"  {label:<40}"
    for name, grp in groups:
        n_true = (grp[col] == true_val).sum()
        pct    = n_true / len(grp) * 100
        row += f"  {n_true:,} ({pct:.1f}%)".ljust(22)
    vals = [[1 if v == true_val else 0 for v in grp[col].dropna()] for _, grp in groups]
    from scipy.stats import chi2_contingency
    ct = pd.crosstab(df[col], df['emop'])
    chi2, p, _, _ = chi2_contingency(ct)
    p_str = "< 0.001" if p < 0.001 else f"{p:.3f}"
    print(row + f"  p {p_str}")

groups = [('Elective', elective), ('Emergency', emergency)]
header = f"\n  {'Variable':<40}  {'Elective':^20}  {'Emergency':^20}  P value"
print(header)
print("═" * 90)
print(f"\n  {'N':.<40}  {len(elective):>6,}            {len(emergency):>6,}")

print("\n  ── Demographics ──────────────────────────────")
table1_row_continuous('age',    'Age (years)',             groups, skewed=False)
table1_row_binary('sex',        'Female sex',              groups, true_val='M')
table1_row_continuous('bmi',    'BMI (kg/m²)',             groups, skewed=False)
table1_row_continuous('asa',    'ASA class',               groups, skewed=True)
table1_row_binary('death_inhosp', 'In-hospital mortality', groups, true_val=1)

print("\n  ── Intraoperative Characteristics ────────────")
table1_row_continuous('op_dur_min',         'Surgical duration (min)',  groups, skewed=True)
table1_row_continuous('intraop_ebl',        'Blood loss (mL)',          groups, skewed=True)
table1_row_continuous('intraop_crystalloid','Crystalloid (mL)',         groups, skewed=True)
table1_row_continuous('intraop_ppf',        'Propofol dose (mg)',       groups, skewed=True)
table1_row_continuous('intraop_ftn',        'Fentanyl dose (μg)',       groups, skewed=True)
table1_row_continuous('intraop_uo',         'Urine output (mL)',        groups, skewed=True)
```
:::

---

## Interpreting the Table 1: What the Numbers Reveal

The elective-vs-emergency stratification demonstrates several key features of descriptive statistics in action:

**Sicker patients emerge in emergency surgery.** ASA class will be higher in the emergency group, even before any other adjustment. This is selection bias in its most visible form: the patients are not comparable at baseline. Any comparison of outcomes between elective and emergency cases must account for this — which is why simple descriptive statistics are insufficient for causal inference.

**Right skew dominates surgical data.** Blood loss, surgical duration, crystalloid volume, propofol dose, and fentanyl dose are all substantially right-skewed. For every variable in this list, median [IQR] is the correct summary. Reporting mean ± SD would overstate the typical case and produce misleading comparisons.

**Zero-inflation splits drug variables.** Propofol dose is zero for every patient who received volatile anaesthesia. Computing a single summary of "propofol dose" across all cases combines a mass of zeros (the volatile cases) with a distribution of real doses (the TIVA cases). The correct analysis separates these groups first — or uses a two-part model that handles the zero-inflation explicitly.

**P-values in Table 1 need context.** With 6,388 cases, even trivially small differences in age (e.g., 58.1 years vs. 58.9 years) will yield p < 0.001. Statistical significance is not clinical significance. Always report effect sizes alongside p-values.

---

## Physics Connection: Precision, Accuracy, and the Standard Deviation of Arterial Pressure

The arterial line transducer that displays MAP on the anaesthetic monitor measures pressure by detecting deformation of a strain gauge. Its output has two sources of variability:

**1. Biological variability:** The patient's MAP genuinely fluctuates from beat to beat due to respiratory cycles, sympathetic tone, and cardiac output changes. This is real signal — the SD of beat-to-beat MAP in a stable patient is approximately 5–10 mmHg.

**2. Instrument noise:** The transducer has a measurement uncertainty of approximately ±1–2 mmHg due to electrical noise, zero-drift, and damping characteristics. This is measurement error — uninformative noise added to the biological signal.

The displayed value at any moment is:

$$\text{MAP}_{\text{displayed}} = \text{MAP}_{\text{true}} + \epsilon_{\text{biological}} + \epsilon_{\text{instrument}}$$

When you compute the SD of MAP over a 10-minute window, you are computing the combined variability from *both* sources:

$$\sigma^2_{\text{observed}} = \sigma^2_{\text{biological}} + \sigma^2_{\text{instrument}}$$

Variances add (when errors are independent). Standard deviations do *not* simply add — this is a common confusion.

**Clinical implication:** A patient with high MAP variability (large $\sigma_{\text{observed}}$) could have either genuine haemodynamic instability (large $\sigma_{\text{biological}}$) or a poorly calibrated, over-damped arterial line (large $\sigma_{\text{instrument}}$). Standard deviation alone cannot distinguish them — you need to examine the waveform morphology (an over-damped waveform has a rounded peak and absent dicrotic notch) alongside the statistics.

This principle — that observed variability reflects the sum of true variability and measurement error — is the foundation of **measurement theory**, which matters enormously when using VitalDB waveform data for modelling. If your model uses noisy signals, your effect estimates will be attenuated toward zero — a phenomenon called **regression dilution bias** (or attenuation bias).

---

## Summary

| Concept | Key Rule |
|---|---|
| Mean vs. median | Use mean ± SD only for approximately symmetric distributions; use median [IQR] for skewed data |
| IQR | The correct spread summary for ordinal or skewed continuous variables |
| Zero-inflation | Report % receiving any + median [IQR] among receivers separately |
| Correlation | Always visualise with scatter plot before computing $r$; use Spearman for non-normal or ordinal data |
| Table 1 | Match summary statistic to variable type; report missing data; interpret p-values with effect sizes |
| SD of a measurement | Combines biological variability and instrument noise; attenuation bias follows if noise is large |

---

## Leading Into Chapter 4

Descriptive statistics compress data into numbers. The next step is to **visualise** it — to see patterns that numbers alone cannot reveal. Chapter 4 introduces the grammar of graphics and demonstrates how choosing the right plot type can transform the same dataset from noise into narrative.

The most important visualisation in perioperative research — the dose-response relationship between anaesthetic depth (BIS) and propofol effect-site concentration — will serve as the worked example: does the expected pharmacodynamic sigmoid emerge from real intraoperative data?

---

## References

- Altman, D.G. (1990). *Practical Statistics for Medical Research*. Chapman & Hall.
- Royston, P., Altman, D.G., & Sauerbrei, W. (2006). Dichotomizing continuous predictors in multiple regression: a bad idea. *Statistics in Medicine*, 25(1), 127–141.
- Anscombe, F.J. (1973). Graphs in statistical analysis. *The American Statistician*, 27(1), 17–21.
- Bland, J.M. & Altman, D.G. (1996). Statistics notes: measurement error. *BMJ*, 313, 744.
- Kahan, B.C., Jairath, V., Doré, C.J., & Morris, T.P. (2014). The risks and rewards of covariate adjustment in randomised trials: an assessment of 12 outcomes from 8 studies. *Trials*, 15, 139.
