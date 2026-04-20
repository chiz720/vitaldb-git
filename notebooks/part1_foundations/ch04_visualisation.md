# Chapter 4 — Visualisation: Seeing What the Numbers Mean

> *"A picture is worth a thousand p-values."*

---

A number without context is noise. A table of numbers is data. A well-chosen visualisation is understanding.

The anaesthetist already knows this intuitively. The arterial line waveform on the monitor is not a table of numbers — it is a continuous visual display of systolic peaks, diastolic troughs, the dicrotic notch, and the pulse pressure. You read pathophysiology directly from the shape: the pulsus paradoxus of tamponade, the bisferious pulse of hypertrophic cardiomyopathy, the damped flat trace of a kinked arterial line. The waveform is a visualisation, and you have trained your eye to extract clinical information from it.

This chapter applies the same principle to statistical data. The right plot for the right data type turns a table of 6,388 rows into a story about a surgical population — who they were, how they varied, and how their physiology connected to their outcomes.

---

## 4.1 The Grammar of Graphics

The **grammar of graphics** — introduced by Leland Wilkinson and operationalised in the `ggplot2` R library and Python's `plotnine` and `seaborn` — provides a systematic framework for thinking about visualisation. Every plot is a mapping from **data** to **visual channels**.

### Visual Channels

| Visual Channel | What it Encodes | Best For |
|---|---|---|
| Position (x-axis) | A continuous or ordered variable | The primary variable of interest |
| Position (y-axis) | A second continuous or ordered variable | Outcome or frequency |
| Colour (hue) | A categorical variable | Group membership (ASA class, sex, anaesthesia type) |
| Colour (saturation/lightness) | A continuous variable | Magnitude or intensity |
| Size | A continuous variable | A third quantitative dimension |
| Shape | A categorical variable (few levels) | Group membership when colour is already used |
| Opacity (alpha) | Data density | Overplotting in large scatter plots |

Choosing a visualisation means deciding which channels to use for which variables. Most errors in data visualisation are mismatches: using colour (a categorical channel) to represent a continuous variable, or using y-axis position (a linear channel) for an ordinal variable with unequal intervals.

### The Three Questions to Ask Before Plotting

1. **What type of variable am I showing?** (Nominal, ordinal, continuous — from Chapter 2)
2. **How many variables am I showing simultaneously?**
3. **What comparison am I trying to make?** (Distribution? Trend? Association? Composition?)

These three questions determine the plot type. Not the other way around.

---

## 4.2 Choosing the Right Plot for the Right Data Type

### One Variable: Distribution Plots

| Variable Type | Plot | Use When |
|---|---|---|
| Continuous | Histogram | Raw distribution, bin-level inspection |
| Continuous | Density (KDE) plot | Smooth shape comparison across groups |
| Continuous | Boxplot | Summary comparison across groups |
| Continuous | Violin plot | Full shape comparison across groups |
| Ordinal | Bar chart | Frequency by level |
| Nominal | Bar chart (sorted by frequency) | Category counts |
| Binary | Single bar or proportion | Simple proportion |

**Rule:** Never use a pie chart for more than 4–5 categories. Labels overlap, small slices are invisible, and the human eye cannot compare non-adjacent arc lengths. Use a sorted bar chart instead.

### Two Variables: Relationship Plots

| Variable Types | Plot | Use When |
|---|---|---|
| Continuous × Continuous | Scatter plot | Exploring association |
| Continuous × Continuous (large n) | Hexbin or 2D density | Overplotting in large datasets |
| Continuous × Categorical | Grouped boxplot / violin | Comparing distributions across groups |
| Continuous × Categorical | Strip plot + boxplot | Small samples — show all individual points |
| Continuous × Ordered time | Line plot | Trends over time or sequential measurements |
| Categorical × Categorical | Heatmap (count table) | Frequency of co-occurrence |
| Binary outcome × Continuous | ROC curve | Diagnostic test performance |

### Three or More Variables

Adding a third variable to a plot is powerful but can quickly become unreadable. The safest options are:

- **Faceting:** split the plot into small multiples, one panel per level of the third variable
- **Colour:** add a colour channel for a categorical third variable (≤5 levels)
- **Panel layout:** two side-by-side plots linked by a common axis

Avoid using both colour and shape simultaneously for the same variable — redundant encoding helps accessibility but uses two channels for one variable.

---

## 4.3 The Boxplot Autopsy

The boxplot is the workhorse of comparative clinical statistics. Misreading it is common. Here is a precise anatomical description of each component and what it means physiologically.

```
    ┌──────────────┐     ← Q3 (75th percentile)
    │              │
    │   IQR box    │     ← Contains the middle 50% of observations
    │              │
────┤──────────────├──── ← Median (Q2, 50th percentile)
    │              │
    │              │
    └──────────────┘     ← Q1 (25th percentile)
         │
         │  whisker      ← Extends to last point within Q1 − 1.5×IQR
         │
    ●               ● ● ← Outliers: points beyond 1.5×IQR from the box
```

**The whiskers** extend to the most extreme data point that is still within 1.5 × IQR of the box edge. Points beyond this threshold are plotted individually as outliers.

**What does 1.5 × IQR mean?** For a perfectly normal distribution, approximately 0.7% of observations fall beyond Q1 − 1.5×IQR or Q3 + 1.5×IQR. So whisker outliers are genuinely unusual — not just "far from the mean".

**Clinical example — boxplot of blood loss by ASA class:**

| Component | What it shows clinically |
|---|---|
| Median line | The typical blood loss for a patient at this ASA level |
| Box width (IQR) | The case-to-case variation that a well-calibrated surgeon would anticipate |
| Whisker length | How far from typical the extremes go — relevant for blood bank ordering |
| Outlier points | Individual cases of catastrophic haemorrhage — each one deserves inspection |

:::{important} The boxplot hides multimodality
A bimodal distribution — two distinct patient populations mixed together — can have an identical boxplot to a unimodal distribution with the same median and IQR. Always check the histogram or violin plot first. If bimodality is present (e.g., propofol dose, which has a zero-mass for volatile cases and a dose-mass for TIVA cases), the boxplot gives a misleading summary.
:::

### Violin Plots: Boxplots with Shape

A violin plot wraps a mirrored kernel density estimate around the boxplot. It shows:
- The full shape of the distribution (revealing skew, multimodality, and gaps)
- The IQR box and median (embedded within the violin)
- The width of the violin at any point is proportional to the data density there

For comparing blood loss across surgical departments — where distributions are heterogeneous in shape, not just location — the violin plot reveals structure that boxplots conceal.

---

## 4.4 Heatmaps for Correlation Matrices

When you have many continuous variables and want to understand which ones vary together, a **correlation matrix heatmap** provides an immediate, interpretable overview.

The preoperative laboratory values in `all_cases.csv` include haemoglobin, platelets, prothrombin time, APTT, sodium, potassium, glucose, albumin, AST, ALT, BUN, and creatinine — 12 variables. Computing all pairwise correlations yields a 12 × 12 matrix (66 unique pairs). Reading a 66-row table is impractical. A heatmap makes the structure visible in seconds.

**How to read a correlation heatmap:**
- Dark red / warm colour → strong positive correlation
- Dark blue / cool colour → strong negative correlation
- Pale / white → near-zero correlation
- The diagonal is always 1.0 (a variable is perfectly correlated with itself)
- The matrix is symmetric (the upper triangle mirrors the lower)

**Clinical patterns to look for:**

| Pattern | Clinical interpretation |
|---|---|
| ALT and AST co-correlated | Hepatocellular damage affects both simultaneously |
| BUN and creatinine co-correlated | Both reflect renal excretory function |
| Albumin negatively correlated with AST/ALT | Low albumin + elevated enzymes = chronic liver disease |
| Haemoglobin negatively correlated with BUN/creatinine | Anaemia of chronic kidney disease |
| PT and APTT co-correlated | Both elevated in coagulopathy / anticoagulation |

These correlations are not surprises — they reflect known clinical co-morbidity patterns. But seeing them emerge from 6,388 real cases, without any physician annotation, validates that the data is capturing true physiology. When a correlation matrix reveals an *unexpected* strong association, it is worth investigating as a potential clinical discovery or data-quality problem.

### Using Spearman for Lab Correlations

Laboratory values are frequently right-skewed and non-normal. Spearman rank correlation is more appropriate than Pearson for the full correlation matrix, as it captures monotonic relationships without assuming linearity or normality.

---

## 4.5 Time Series: The Intraoperative Monitor as Data

Every piece of monitoring equipment in the operating theatre generates a time series — measurements ordered in time at regular intervals. MAP is recorded every heartbeat. BIS is updated every second. End-tidal CO₂ is measured every breath. Temperature every minute.

Time series visualisation has specific requirements that ordinary scatter plots do not handle well.

### What a Line Plot Must Show

A well-constructed intraoperative time series plot should display:

1. **The signal over time** — the primary y-axis vs. time
2. **A reference band** — the target range (e.g., MAP 65–100 mmHg shown as a shaded zone)
3. **Clinical events** — drug administrations, incision, position changes marked as vertical lines
4. **Multiple physiological channels** — MAP, BIS, SpO₂ on separate panels with a shared time axis (not on the same axis with different scales, which distorts the visual relationship)

### The Dual-Axis Trap

Plotting two variables with different scales on the same axes using a primary and secondary y-axis is almost always misleading. The visual impression of correlation or divergence changes entirely depending on the arbitrary choice of the secondary axis scale. Two variables that are completely uncorrelated can be made to appear synchronised by adjusting the axis scales.

**Rule:** Use separate panels (facets) with a shared x-axis rather than dual y-axes.

### Smoothing and Artefact

Raw intraoperative data contains artefact — motion artefact in the SpO₂ trace during surgical manipulation, electrocautery interference in the BIS signal, pressure transducer disconnection in the arterial line. Before plotting a time series for analysis, decide whether to:

- Plot raw data and annotate artefact visually
- Apply a rolling median (more artefact-resistant than rolling mean) to smooth
- Exclude known artefact windows based on device-flagged quality metrics

In VitalDB, the `tracks.csv` file contains the raw waveform parameters. For population-level analysis, smoothing is appropriate. For individual case review, raw data preserves the clinical context.

---

## VitalDB Exercise: Visualising Pharmacodynamics and Lab Correlations

Two exercises in the companion notebook demonstrate the principles of this chapter:

**Exercise 1 — Preoperative Lab Correlation Heatmap**

Which preoperative laboratory values co-vary in this surgical cohort? The heatmap of Spearman correlations across 12 lab variables reveals co-morbidity patterns (renal dysfunction, liver disease, anaemia) without any clinical labels — purely from the correlation structure of the data.

**Exercise 2 — BIS vs. Propofol: Does the Pharmacodynamic Relationship Emerge?**

The `tracks.csv` file contains intraoperative BIS values and the `ppf_ce` (propofol effect-site concentration, computed by the TCI pump). Plotting BIS against propofol Ce across all general anaesthesia cases should reveal the characteristic sigmoid pharmacodynamic relationship — the Hill equation in action. If it does, it validates both the TCI model and the BIS monitor as coherent measures of the same underlying phenomenon: anaesthetic depth.

A scatter plot with a locally-weighted regression (LOWESS) smoother is the appropriate visualisation: the scatter shows the case-to-case variability in the relationship, and the smoother reveals the population-level trend.

---

## Common Visualisation Mistakes in Clinical Research

| Mistake | Why it Misleads | Fix |
|---|---|---|
| Y-axis not starting at zero for bar charts | Exaggerates differences; a 0.1% vs. 0.2% mortality difference looks enormous | Always start bar chart y-axis at zero |
| Reporting only mean ± SEM instead of SD | SEM shrinks with sample size — a large study has a tiny SEM that suggests impossibly tight data | Report SD for description; SEM only for inference about the mean |
| Connecting non-sequential points with lines | Implies a temporal or ordered relationship that does not exist | Use scatter plot or bar chart for unordered categories |
| Truncating boxplot whiskers without explanation | Hides the extent of skew; readers assume whiskers follow the 1.5×IQR rule | State whisker convention explicitly |
| Rainbow colour scales for continuous data | Perceptually non-uniform; regions appear artificially sharp | Use perceptually uniform colour maps (viridis, plasma, cividis) |
| 3D bar charts or pie charts | No additional information; perspective distorts area perception | Never use 3D for 2D data |
| Plotting all individual points when n > 1,000 | Overplotting conceals the distribution | Use transparency (alpha), jitter, or hexbin/violin instead |

---

## Connecting to the Monitor: Visualisation as Clinical Reasoning

The intraoperative monitor is a real-time visualisation system. Every anaesthetist spends years learning to read it — to extract clinical meaning from the shape of the arterial waveform, the trend of the BIS trace, the CO₂ waveform during two-lung ventilation.

The statistical visualisations in this chapter use the same perceptual machinery. A correlation heatmap is read like a monitor — not left-to-right, but as a pattern. A scatter plot with a LOWESS smoother tells the same kind of story as watching a MAP trace after phenylephrine: a baseline, a response, a new steady state.

The difference is that the statistical plot summarises 6,388 cases simultaneously. The anaesthetic monitor shows one.

---

## Summary

| Data situation | Plot type |
|---|---|
| One continuous variable | Histogram, density plot |
| One continuous variable across groups | Boxplot, violin plot |
| Two continuous variables | Scatter plot (small n), hexbin (large n) |
| Many continuous variables — correlations | Heatmap of correlation matrix |
| Continuous variable over time | Line plot with event markers |
| Pharmacodynamic relationship | Scatter + LOWESS smoother |
| Categorical variable | Sorted bar chart |

---

## Leading Into Part II

Part I has equipped you with the language of data. You know what kind of variables you have, how to summarise them, and how to visualise them. You have seen the VitalDB cohort as a whole — its demographics, its clinical heterogeneity, its physiological correlations.

Part II asks the harder question: when you see a difference between two groups, or a trend in a scatter plot, **how confident are you that it is real?** The logic of statistical inference — probability, hypothesis testing, confidence intervals — is the subject of the next three chapters.

---

## References

- Wilkinson, L. (2005). *The Grammar of Graphics* (2nd ed.). Springer.
- Tufte, E.R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.
- Weissgerber, T.L., Milic, N.M., Winham, S.J., & Garovic, V.D. (2015). Beyond bar and line graphs: time for a new data presentation paradigm. *PLOS Biology*, 13(4), e1002128.
- Rougier, N.P., Droettboom, M., & Bourne, P.E. (2014). Ten simple rules for better figures. *PLOS Computational Biology*, 10(9), e1003833.
- Crameri, F., Shephard, G.E., & Heron, P.J. (2020). The misuse of colour in science communication. *Nature Communications*, 11, 5444.
