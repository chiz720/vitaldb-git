# Quantitative Anesthesia: From Numbers to the Operating Room

> *"In God we trust; all others must bring data."* — W. Edwards Deming

## Overview

This Jupyter Book is written by an anesthesiologist, for anesthesiologists — and for anyone who manages critically ill patients, interprets physiological data, or wants to understand what the numbers on the monitor actually mean.

Anesthesiology is perhaps the most quantitative clinical specialty: every case generates continuous streams of hemodynamic, respiratory, anesthetic, and neurological data. Yet most training programs teach us to *react* to these numbers rather than *understand* them. This book bridges that gap.

The goal is not to make you a statistician. The goal is to make you a better anesthesiologist by helping you think quantitatively about physiology, pharmacology, and physics — the three pillars of our specialty.

---

## Primary Dataset: VitalDB

All examples in this book draw from the **[VitalDB dataset](https://vitaldb.net)** — a publicly available, de-identified perioperative database from Seoul National University Hospital containing:

| Dataset File | Records | Description |
|---|---|---|
| `all_cases.csv` | 6,388 cases | Demographics, surgical details, preop labs, intraop drugs/fluids, outcomes |
| `labs.csv` | 928,448 measurements | Serial laboratory results (34 test types) with timestamps |
| `tracks.csv` | 486,449 monitor records | Continuous physiological waveform parameters from 7 device types |

### What Makes This Dataset Exceptional

The dataset provides genuine end-to-end perioperative data — not just vital signs snapshots:

- **Depth of anesthesia:** BIS index, EEG waveforms, spectral edge frequency, suppression ratio
- **Pharmacological precision:** Propofol and remifentanil infusion rates *with* target-controlled infusion (TCI) plasma and effect-site concentrations
- **Hemodynamic granularity:** Direct arterial, central venous, and pulmonary artery pressures; cardiac output by thermodilution, pulse contour, and Doppler
- **Ventilator mechanics:** Real-time compliance, airway pressures, tidal volumes, gas concentrations, MAC values
- **Clinical outcomes:** Hospital mortality, ICU length of stay

This is the operating room in data form.

---

## Supplementary Open-Source Datasets

To broaden clinical context beyond a single centre, the following datasets are incorporated:

| Dataset | Source | Relevance |
|---|---|---|
| **MIMIC-IV** | PhysioNet / MIT | ICU data: ventilator management, vasopressor use, acute kidney injury, mortality prediction |
| **eICU Collaborative** | PhysioNet | Multi-centre ICU data across 208 US hospitals; cross-institutional generalisability |
| **PhysioNet AF Classification** | PhysioNet | ECG rhythm analysis; intraoperative arrhythmia detection |
| **ORCA (Open Registry of Cardiac Arrest)** | PhysioNet | Cardiac arrest physiology; CPR quality metrics |
| **HiRID** | PhysioNet | High-resolution ICU data (every 2 minutes); signal processing applications |
| **MIMIC Waveform Database** | PhysioNet | Raw arterial waveform, ECG, and SpO2 signals |
| **OpenAnesthesia Wiki** | openanesthesia.org | Reference pharmacology and physiology values |

> All datasets are either fully open or available after free registration. Data access instructions and DOIs are provided in each chapter.

---

## Book Structure

The book is organised as a progressive curriculum — each part builds on the last. A reader with no statistics background can start at Part I. A clinician comfortable with basic statistics can jump to Part III.

---

### Part I — Foundations: Learning the Language of Data

*Before you can analyse anesthesia data, you need to understand what kind of data you have.*

#### Chapter 1 — Why Quantitative Anesthesia?

- The monitor as a data source, not just an alarm
- How numbers generated in the OR translate to patient outcomes
- Landmark quantitative studies that changed anesthetic practice (e.g., POISE, DREAM, PRODIGY trials)
- What this book will teach you — and what it will not

**VitalDB preview:** Loading `all_cases.csv` for the first time — case counts by surgery type, ASA distribution, mortality rates

---

#### Chapter 2 — Types of Variables

*The type of variable determines every downstream analysis. Getting this wrong invalidates the statistics.*

**2.1 Categorical Variables**
- Nominal: sex, surgical approach (open/laparoscopic/robotic), anesthesia type
- Ordinal: ASA physical status (1–6), Cormack-Lehane grade, pain scores

**2.2 Continuous Variables**
- Interval: temperature, pH
- Ratio: blood pressure, heart rate, drug doses, lab values

**2.3 Special Variable Types in Anesthesia**
- Time-to-event (survival): time to extubation, time to discharge, time to death
- Compositional: fraction of inspired oxygen (FiO2), volatile agent concentration as %MAC
- Count: number of vasopressor boluses, number of intubation attempts
- Binary outcomes: mortality, ICU admission, intraoperative hypotension episode (yes/no)

**2.4 Clinically Dangerous Misclassification**
- Treating ordinal data (pain score 0–10) as continuous
- Dichotomising continuous data (MAP > 65 vs. ≤ 65) and what you lose

**VitalDB exercise:** Classify all 74 columns in `all_cases.csv` — nominal, ordinal, continuous, binary, time-to-event

---

#### Chapter 3 — Descriptive Statistics: Summarising Your Patients

**3.1 Measures of Central Tendency**
- Mean, median, mode — and when each is appropriate
- Why the *median* vasopressor dose matters more than the *mean*

**3.2 Measures of Spread**
- Range, interquartile range (IQR), standard deviation, variance
- Coefficient of variation: comparing variability across different scales (e.g., HR vs. MAP)

**3.3 Describing Distributions**
- Histograms, density plots, violin plots
- Skewness and kurtosis — with clinical examples (propofol dose distributions are right-skewed)
- The normal distribution: when it holds and when it does not

**3.4 Describing Associations**
- Cross-tabulation for categorical variables
- Scatter plots for continuous variables
- Correlation coefficient: Pearson (continuous-continuous), Spearman (ordinal or non-normal)

**3.5 Presenting Data in Clinical Tables**
- The "Table 1" in clinical trials: what it means and how to construct one
- Reporting rules: mean ± SD vs. median [IQR]

**VitalDB exercise:** Full descriptive analysis of the cohort — age, BMI, ASA class, surgical duration, intraop propofol dose, blood loss, fluid balance

**Physics connection:** Standard deviation of arterial pressure readings — instrument precision vs. biological variability

---

#### Chapter 4 — Visualisation: Seeing What the Numbers Mean

- The grammar of graphics: mapping data to visual channels
- Choosing the right plot for the right data type
- Boxplot autopsy: what each component means physiologically
- Heatmaps for correlation matrices (which preoperative labs co-vary?)
- Time series plots: the intraoperative monitor strip as data

**VitalDB exercise:** Plot BIS vs. propofol effect-site concentration for all general anesthesia cases — does the expected PD relationship emerge?

---

### Part II — Inference: Making Decisions from Data

*Moving from describing a sample to making conclusions about a population.*

#### Chapter 5 — Probability and Distributions

**5.1 Probability Basics**
- Probability, odds, and risk — the difference matters in clinical interpretation
- Conditional probability: P(hypotension | propofol induction) vs. P(propofol | hypotension)
- Bayes' theorem: pre-test probability, likelihood ratio, post-test probability
  - *Clinical example:* Interpreting a positive troponin in a post-cardiac-surgery patient

**5.2 Common Distributions in Anesthesia Data**
- Normal (Gaussian): height, BMI in healthy populations
- Log-normal: drug doses, lab values, time-to-event (most biologically skewed variables)
- Binomial: complication rates, mortality
- Poisson: count data (number of vasopressor boluses per case)
- Exponential: time between hypotensive episodes

**5.3 The Central Limit Theorem**
- Why sample means behave normally even when raw data does not
- Practical implication: when is n large enough?

**VitalDB exercise:** Fit distributions to MAP, BIS, and ETCO2 data — test goodness of fit with Q-Q plots and Kolmogorov-Smirnov test

---

#### Chapter 6 — Hypothesis Testing

**6.1 The Logic of Inference**
- Null and alternative hypotheses
- Type I error (α) and Type II error (β): the false positive/false negative trade-off
- Statistical power and sample size — why underpowered studies are dangerous
- P-value: what it means and the epidemic of misinterpretation

**6.2 Comparing Two Groups**
- Independent t-test: does propofol dose differ by sex?
- Mann-Whitney U (Wilcoxon rank-sum): non-parametric alternative
- Paired t-test: pre- vs. post-intubation MAP
- Effect size: Cohen's d — statistical significance ≠ clinical significance

**6.3 Comparing More Than Two Groups**
- One-way ANOVA: MAP differences across ASA classes
- Kruskal-Wallis: non-parametric alternative
- Post-hoc tests and the multiple comparisons problem

**6.4 Categorical Comparisons**
- Chi-squared test: mortality rates by anesthesia type
- Fisher's exact test: when cell counts are small

**6.5 The Multiple Testing Problem**
- Bonferroni correction, Benjamini-Hochberg procedure
- Why running 20 t-tests guarantees a false positive

**VitalDB exercise:** Compare intraoperative fentanyl dose between open vs. laparoscopic vs. robotic approaches — correct for multiple comparisons

---

#### Chapter 7 — Confidence Intervals and Clinical Significance

- Confidence intervals: the range of plausible values
- Why a 95% CI that crosses zero means something different from a P > 0.05
- Minimum clinically important difference (MCID): what MAP difference actually matters?
- Forest plots: reading meta-analyses like an anesthesiologist
- Number needed to treat (NNT) and number needed to harm (NNH)

**VitalDB exercise:** Bootstrap confidence intervals for median blood loss in colorectal cases

---

### Part III — Modelling: Understanding Relationships

*Moving from association to prediction to mechanism.*

#### Chapter 8 — Linear Regression

**8.1 Simple Linear Regression**
- The line of best fit: slope, intercept, R²
- Assumptions: linearity, independence, homoscedasticity, normality of residuals
- *Clinical example:* Predicting tidal volume from patient height (the ARDSNet foundation)

**8.2 Multiple Linear Regression**
- Controlling for confounders: does surgery duration independently predict blood loss after controlling for procedure type?
- Model building: forward, backward, stepwise selection
- Collinearity: why you cannot include both propofol dose and BIS in the same model
- Adjusted R² and model parsimony

**8.3 Assumptions and Diagnostics**
- Residual plots, leverage, influential observations
- What to do when assumptions are violated

**8.4 Transformations**
- Log transformation for skewed outcomes
- Standardisation (z-scores) for comparing coefficients across scales

**VitalDB exercise:** Predict intraoperative urine output from preoperative creatinine, crystalloid volume, and surgical duration

**Physics connection:** Ohm's law analogy in hemodynamics — MAP = CO × SVR modelled with linear regression

---

#### Chapter 9 — Logistic Regression

*The workhorse of clinical prediction in anesthesia.*

**9.1 Why Not Just Use Linear Regression for Binary Outcomes?**
- The logit transformation: log-odds and probability
- Interpreting odds ratios — and why they are not relative risks
- Confidence intervals for ORs

**9.2 Building a Clinical Prediction Model**
- Predicting intraoperative hypotension (MAP < 65 mmHg)
- Predictor selection: pre-induction MAP, age, ASA, propofol dose, type of surgery
- Calibration (Hosmer-Lemeshow) and discrimination (AUROC/C-statistic)
- Sensitivity, specificity, PPV, NPV — the ROC curve

**9.3 Model Validation**
- Internal validation: k-fold cross-validation
- External validation: why a model trained in Seoul may not work in London

**9.4 Penalised Regression**
- Ridge (L2) and LASSO (L1) regression for high-dimensional data
- LASSO for feature selection in the VitalDB labs dataset (34 potential predictors of AKI)

**VitalDB exercise:** Build and validate a logistic regression model predicting intraoperative transfusion from preoperative haemoglobin, planned procedure, and patient demographics

---

#### Chapter 10 — Survival Analysis

*Time matters. When something happens is as important as whether it happens.*

**10.1 Censoring and Survival Data Structure**
- Right-censoring: the patient who survived to discharge
- Why ordinary regression fails for time-to-event data

**10.2 Kaplan-Meier Curves**
- Reading and constructing survival curves
- Log-rank test: comparing time-to-extubation by anesthesia type

**10.3 Cox Proportional Hazards Model**
- Hazard ratio vs. odds ratio
- The proportional hazards assumption and how to check it
- *Clinical example:* Time to ICU discharge — which preoperative factors matter?

**10.4 Landmark Studies Read Quantitatively**
- Dissecting the POISE trial survival curves
- Understanding why the hazard ratio for stroke and death diverges over time

**VitalDB exercise:** Kaplan-Meier analysis of time to extubation — general vs. regional anesthesia

---

### Part IV — Physiology Made Quantitative

*Re-deriving clinical rules from first principles using data.*

#### Chapter 11 — Cardiovascular Physiology as a System of Equations

**11.1 The Hemodynamic Equations**
- MAP = CO × SVR (and why this is an oversimplification)
- CO = HR × SV; SV is determined by preload, afterload, contractility
- The Starling curve: quantifying preload dependence from VitalDB EV1000 data

**11.2 Pulse Pressure and Stroke Volume Variation**
- SVV as a predictor of fluid responsiveness — the physiology and the evidence
- Calculating SVV from VitalDB arterial pressure waveforms
- Receiver-operating characteristic analysis of SVV vs. PPV for fluid responsiveness prediction

**11.3 Vasopressor Pharmacodynamics**
- Phenylephrine: pure α-agonist — MAP up, CO unchanged or down
- Norepinephrine: α > β — MAP up, mild chronotropy
- Ephedrine: mixed — MAP up, CO up, heart rate up
- Modelling vasopressor dose-response from VitalDB infusion pump data

**11.4 The Frank-Starling Curve from Real Data**
- Plotting CVP vs. SV from pulmonary artery catheter cases
- Why the flat part of the Starling curve means more fluid will not help

**Physics connection:** Poiseuille's law — radius is the dominant variable in vascular resistance; why vasodilators work

---

#### Chapter 12 — Respiratory Physiology and Ventilator Mechanics

**12.1 Gas Laws in the Operating Room**
- Boyle's, Charles's, Dalton's: the physics behind gas delivery
- The alveolar gas equation: PAO2 = FiO2 × (Patm − PH2O) − PaCO2/RQ
- Predicting SpO2 from ventilator FiO2 settings using VitalDB data

**12.2 Respiratory Mechanics as a Linear Model**
- The equation of motion: Paw = (1/C) × V + R × V̇ + PEEP
- Static compliance = ΔV / ΔP (plateau − PEEP)
- Calculating compliance from VitalDB Primus ventilator data
- Driving pressure = Pplat − PEEP: why it predicts mortality better than tidal volume alone

**12.3 CO2 Physiology**
- Dead space: VD/VT = (PaCO2 − PetCO2) / PaCO2 (Bohr equation)
- The dissociation curve: buffering capacity and the Henderson-Hasselbalch equation
- Modelling ETCO2 during capnoperitoneum: VitalDB laparoscopic cases

**12.4 Oxygen Delivery and Consumption**
- DO2 = CO × (Hb × 1.34 × SaO2 + 0.003 × PaO2)
- Critical oxygen delivery: where the supply-demand mismatch begins
- Mixed venous saturation (SvO2) from VitalDB Vigilance PAC data

**VitalDB exercise:** Compute driving pressure for all ventilated cases; plot distribution and identify proportion above the 15 cmH2O safety threshold

---

#### Chapter 13 — Pharmacology Made Quantitative: PK/PD Modelling

*The most mathematical chapter — and the most clinically useful.*

**13.1 Pharmacokinetics: What the Body Does to the Drug**
- Compartment models: one-, two-, and three-compartment
- Volume of distribution, clearance, half-life
- Context-sensitive half-time: why propofol wears off fast but fentanyl does not

**13.2 The Target-Controlled Infusion (TCI) Model**
- Marsh vs. Schnider models for propofol
- The Minto model for remifentanil
- VitalDB Orchestra infusion pump records include Cp, Ce, and Ct — live TCI model validation

**13.3 Pharmacodynamics: What the Drug Does to the Body**
- The Hill equation (Emax model): E = Emax × Cᵞ / (EC50ᵞ + Cᵞ)
- Fitting BIS vs. propofol Ce from VitalDB: estimating EC50 and γ empirically
- Hysteresis and the ke0: why the brain lags behind the plasma

**13.4 Drug Interactions**
- Synergy and antagonism: the propofol-remifentanil interaction surface
- Response surface methodology: the isobologram and clinical implications
- Remimazolam vs. propofol: emerging PK/PD comparisons

**13.5 Neuromuscular Pharmacology**
- The dose-response curve for rocuronium
- Train-of-four ratio and residual paralysis: quantifying block depth
- Sugammadex reversal kinetics

**VitalDB exercise:** Fit a sigmoid Emax model (BIS as response, propofol Ce as exposure) using non-linear least squares; compare EC50 estimates across age groups

---

#### Chapter 14 — Depth of Anaesthesia: Signals from the Brain

**14.1 The EEG as a Physiological Signal**
- What the BIS monitor is actually measuring (and not measuring)
- Power spectral density: decomposing the EEG by frequency
- Alpha, beta, delta, theta power bands — what each means under anaesthesia

**14.2 BIS as a Pharmacodynamic Endpoint**
- Distribution of BIS in VitalDB: what does intraoperative BIS actually look like?
- BIS < 40 (deep anaesthesia) and long-term outcomes: regression analysis
- Burst suppression ratio: EEG correlate of overdose

**14.3 Limitations of Processed EEG**
- Ketamine paradox: why BIS goes *up* with induction
- Muscle artefact (EMG contamination): the VitalDB EMG channel
- Age-related EEG changes and why paediatric models differ

**VitalDB exercise:** Compare BIS, EMG, SEF, and suppression ratio across phases (pre-induction, maintenance, emergence) for propofol vs. volatile cases

---

### Part V — Advanced Data Science for the OR

*Machine learning is not magic. It is statistics with more parameters.*

#### Chapter 15 — Feature Engineering for Clinical Data

- Handling missing data: types (MCAR, MAR, MNAR) and imputation strategies
- Dealing with time-series irregularity in VitalDB lab data
- Encoding categorical variables: one-hot, ordinal, target encoding
- Creating derived features: fluid balance, MAP time-below-threshold (area under the curve of hypotension)
- Train/validation/test splits: temporal vs. random — why random is wrong for time series

---

#### Chapter 16 — Machine Learning for Prediction

**16.1 Decision Trees and Random Forests**
- The anatomy of a decision tree: impurity, splits, leaves
- Random forests: ensemble learning to reduce variance
- Variable importance: which preoperative factors predict postoperative AKI?

**16.2 Gradient Boosted Trees (XGBoost, LightGBM)**
- Why boosting outperforms random forests on tabular clinical data
- Hyperparameter tuning with cross-validation
- Predicting 30-day mortality from VitalDB perioperative data

**16.3 Evaluation Metrics for Clinical Models**
- AUROC: discrimination
- Calibration curve and Brier score: does the model's probability mean something?
- Decision curve analysis: clinical net benefit
- The danger of optimising for accuracy on imbalanced datasets (mortality is rare)

**16.4 Model Interpretability**
- SHAP (SHapley Additive exPlanations): explaining individual predictions
- Partial dependence plots: the population-level dose-response
- Global vs. local explanations — the difference between understanding a model and explaining a decision

**VitalDB exercise:** Train and interpret an XGBoost model predicting intraoperative transfusion; identify the 5 most important predictors using SHAP values

---

#### Chapter 17 — Time Series Analysis

*The intraoperative monitor generates a time series. Most clinical analyses ignore this.*

**17.1 Time Series Concepts**
- Stationarity, autocorrelation, partial autocorrelation
- Trend and seasonality — do blood pressures follow a circadian pattern in the ICU?

**17.2 Moving Averages and Smoothing**
- Exponential smoothing: the monitor's built-in filter
- Rolling statistics for detecting haemodynamic instability

**17.3 Forecasting**
- ARIMA models: predicting MAP trajectory from lagged values
- Dynamic time warping: comparing intraoperative haemodynamic profiles between cases

**17.4 Event Detection**
- Defining and detecting hypotensive episodes from arterial pressure tracks
- Alarm fatigue: the false positive rate of threshold-based monitoring
- Control charts (CUSUM): detecting systematic drift in a patient's MAP

**VitalDB exercise:** Detect all hypotensive events (MAP < 65 mmHg for > 1 minute) in VitalDB tracks; describe their duration, depth, and timing relative to drug administration events

---

#### Chapter 18 — Signal Processing for Anaesthesiologists

**18.1 The Arterial Waveform as Signal**
- Sampling frequency, Nyquist theorem: why the arterial line must sample at ≥ 125 Hz
- Fast Fourier Transform: decomposing the arterial waveform
- Pulse contour analysis: deriving stroke volume from the waveform

**18.2 Photoplethysmography (SpO2 Waveform)**
- Beer-Lambert law: the physics of pulse oximetry
- Plethysmographic variability index (PVI) as a non-invasive fluid responsiveness predictor
- Artefact detection in SpO2 signals

**18.3 ECG Analysis**
- R-peak detection: the Pan-Tompkins algorithm
- Heart rate variability (HRV): autonomic nervous system quantification
- ST-segment deviation: automated ischaemia detection from VitalDB ECG leads

**VitalDB exercise:** Compute HRV metrics (SDNN, RMSSD, LF/HF ratio) from the ECG_II channel during volatile vs. total intravenous anaesthesia

---

#### Chapter 19 — Causal Inference in Observational Data

*Association is not causation — but observational data can still answer causal questions if you do it right.*

**19.1 The Problem with Confounding**
- Why patients who receive more vasopressors have higher mortality (and why that does not mean vasopressors cause death)
- Indication bias and the healthy user effect

**19.2 Propensity Score Methods**
- Propensity score matching: comparing like with like
- Inverse probability of treatment weighting (IPTW)
- *Clinical question:* Does intraoperative BIS monitoring reduce awareness? Propensity-matched analysis from VitalDB

**19.3 Instrumental Variable Analysis**
- When randomisation is impossible, find a natural experiment
- *Clinical example:* Day of week as an instrument for ICU admission

**19.4 Interrupted Time Series**
- Before-after comparisons accounting for pre-existing trends
- *Clinical example:* Impact of a goal-directed fluid therapy protocol introduction

**VitalDB exercise:** Propensity score analysis — do patients receiving TIVA (propofol/remifentanil) have different PONV rates, ICU admission rates, or mortality compared to volatile anaesthesia?

---

#### Chapter 20 — Putting It All Together: A Clinical Data Science Workflow

A worked end-to-end analysis simulating a publishable study:

1. **Clinical question formulation:** Does intraoperative hypotension (MAP < 65 mmHg) predict postoperative AKI?
2. **Data extraction and cleaning:** VitalDB tracks + labs + cases merged on caseid
3. **Exposure operationalisation:** time-weighted average MAP below threshold
4. **Outcome definition:** postoperative creatinine rise ≥ 50% (KDIGO Stage 1 AKI)
5. **Confounding:** propensity score adjustment for age, baseline creatinine, surgical duration, blood loss, vasopressor use
6. **Primary analysis:** Logistic regression with AUROC and calibration
7. **Sensitivity analyses:** different MAP thresholds, different AKI definitions
8. **Machine learning comparison:** XGBoost vs. logistic regression
9. **Interpretation and clinical translation:** SHAP values, decision curve analysis
10. **Reporting:** STROBE checklist, reproducible notebook

---

### Appendices

**A — Python Environment Setup**
- Installing miniconda, creating the `qanes` environment
- Required packages: pandas, numpy, scipy, statsmodels, scikit-learn, lifelines, pingouin, seaborn, matplotlib, plotly, shap, pyEDFlib
- Jupyter Book build instructions

**B — Statistical Formulae Reference Card**
- One-page summary of all key equations

**C — VitalDB Data Dictionary**
- Full variable list with units, device source, and clinical notes for all 74 case variables, 34 lab tests, and 100+ monitor parameters

**D — Accessing Supplementary Datasets**
- PhysioNet registration and data use agreements
- MIMIC-IV, eICU, HiRID access instructions
- Direct download scripts

**E — Glossary**
- Statistical terms defined in clinical language

---

## Technical Architecture

### Tools and Frameworks

| Tool | Purpose |
|---|---|
| **Python 3.11+** | Primary analysis language |
| **Jupyter Book** | Authoring and rendering |
| **pandas / numpy** | Data wrangling |
| **scipy / statsmodels / pingouin** | Classical statistics |
| **lifelines** | Survival analysis |
| **scikit-learn** | Machine learning |
| **XGBoost / LightGBM** | Gradient boosting |
| **SHAP** | Model interpretability |
| **seaborn / matplotlib / plotly** | Visualisation |
| **pyEDFlib / MNE** | EEG and waveform processing |

### Repository Structure

```
VitalDBGit/
├── README.md                   # This file
├── _config.yml                 # Jupyter Book configuration
├── _toc.yml                    # Table of contents
├── environment.yml             # Conda environment specification
│
├── vital_db/                   # VitalDB data files
│   ├── all_cases.csv           # 6,388 surgical cases
│   ├── labs.csv                # 928,448 lab measurements
│   └── tracks.csv              # 486,449 monitor parameters
│
├── data/                       # Supplementary datasets
│   ├── mimic/                  # MIMIC-IV (user downloads separately)
│   ├── eicu/                   # eICU (user downloads separately)
│   └── processed/              # Cleaned, merged datasets (git-ignored)
│
├── notebooks/                  # Source notebooks for each chapter
│   ├── part1_foundations/
│   │   ├── ch01_why_quantitative.ipynb
│   │   ├── ch02_variable_types.ipynb
│   │   ├── ch03_descriptive_stats.ipynb
│   │   └── ch04_visualisation.ipynb
│   ├── part2_inference/
│   │   ├── ch05_probability.ipynb
│   │   ├── ch06_hypothesis_testing.ipynb
│   │   └── ch07_confidence_intervals.ipynb
│   ├── part3_modelling/
│   │   ├── ch08_linear_regression.ipynb
│   │   ├── ch09_logistic_regression.ipynb
│   │   └── ch10_survival_analysis.ipynb
│   ├── part4_physiology/
│   │   ├── ch11_cardiovascular.ipynb
│   │   ├── ch12_respiratory.ipynb
│   │   ├── ch13_pkpd.ipynb
│   │   └── ch14_depth_of_anaesthesia.ipynb
│   └── part5_data_science/
│       ├── ch15_feature_engineering.ipynb
│       ├── ch16_machine_learning.ipynb
│       ├── ch17_time_series.ipynb
│       ├── ch18_signal_processing.ipynb
│       ├── ch19_causal_inference.ipynb
│       └── ch20_full_workflow.ipynb
│
├── src/                        # Shared Python utilities
│   ├── vitaldb_loader.py       # Data loading and preprocessing
│   ├── hemodynamics.py         # Derived hemodynamic calculations
│   ├── pkpd.py                 # PK/PD model functions
│   └── plotting.py             # Custom plot themes
│
└── tests/                      # Unit tests for utility functions
```

---

## Guiding Principles

**1. Every equation has a patient attached to it.**
No formula is introduced without a clinical scenario. The Henderson-Hasselbalch equation is taught using a real arterial blood gas. The Hill equation is demonstrated using BIS data from a real patient's propofol infusion.

**2. Show the uncertainty.**
Every estimate has a confidence interval. Every model has a calibration curve. Medicine gives false certainty; data science teaches appropriate humility.

**3. Reproducibility is non-negotiable.**
Every result in this book can be reproduced by running the corresponding notebook. No results are manually transferred from one tool to another.

**4. Complexity earns its place.**
A logistic regression that is interpretable and achieves AUROC 0.80 is better than an uninterpretable neural network that achieves 0.83. Complexity must justify itself clinically, not just statistically.

**5. The physiology is always the ground truth.**
When the data disagrees with physiology, investigate before accepting. The model is wrong until proven otherwise.

---

## How to Use This Book

### For the Trainee Anaesthesiologist
Start at Chapter 1 and read sequentially. Complete the VitalDB exercises in each chapter using the provided Jupyter notebooks. By Part III you will be able to read and critically appraise a methodology section in any anaesthesia journal.

### For the Consultant / Attending
Jump to the chapter most relevant to your practice. Chapter 11 (cardiovascular) and Chapter 13 (PK/PD) contain quantitative treatments of concepts you already know — you may find that the mathematics makes clinical intuitions more precise.

### For the Researcher
Parts IV and V are the core. The worked example in Chapter 20 follows the structure of a publishable observational study and demonstrates modern standards for transparent, reproducible clinical research.

### For the Data Scientist New to Anaesthesia
Read Part IV (Chapters 11–14) before touching the machine learning chapters. The data is meaningless without the physiology.

---

## A Word on Statistics and Clinical Judgment

Statistical significance is not clinical significance. A propofol dose difference of 2 mg that is statistically significant across 6,000 cases means nothing to the patient on the table. Throughout this book, we will insist on effect sizes, confidence intervals, and clinical interpretation alongside p-values.

Equally, clinical intuition without data is not sufficient. The history of anaesthesia is littered with practices adopted on physiological grounds and abandoned when randomised trials showed harm — pulmonary artery catheters, tight glucose control, high-dose steroids in sepsis. Quantitative thinking protects patients from both bad statistics and bad intuition.

---

## Citation

If you use this book or the analysis code in your work, please cite:

```
[Author]. Quantitative Anesthesia: From Numbers to the Operating Room.
Jupyter Book, 2025. Data source: VitalDB (vitaldb.net).
DOI: [to be assigned]
```

---

## Contributing

This is a living document. Pull requests are welcome for:
- Corrections to statistical claims
- Additional VitalDB analyses
- New supplementary dataset integrations
- Translation of notebooks to R (a parallel R track is planned)

Please open an issue before submitting a large pull request.

---

## Licence

Text and notebooks: [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

VitalDB data: subject to VitalDB terms of use (see https://vitaldb.net)

---

*Numbers without context are noise. In anaesthesia, context is the patient.*
