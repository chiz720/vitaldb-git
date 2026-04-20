# CLAUDE.md — VitalDBGit Project Instructions

## Project Overview

Jupyter Book: **"Quantitative Anesthesia: From Numbers to the Operating Room"** by Dr. Idris.
An educational textbook that teaches statistics, physiology modelling, and machine learning using real perioperative data from VitalDB (6,388 surgical cases, Seoul National University Hospital).

## Target Audience

**The average anaesthesiologist** — a clinician who is smart, busy, and comfortable with clinical reasoning but has no background in statistics or programming. They did not study maths at university. They have never written a line of code. They want to understand data and evidence-based medicine better, not become a data scientist.

Write for this person at all times. Specifically:

- **Assume no prior statistics knowledge.** Do not assume the reader knows what a p-value is, what a confidence interval means, or what "normally distributed" means until the book has explained it.
- **Assume no programming knowledge.** Code is hidden behind toggle buttons. The reader should never need to read code to understand the content. All results, figures, and insights must be fully explained in the surrounding prose.
- **Assume strong clinical knowledge.** The reader knows physiology, pharmacology, and anaesthesia inside out. Use this as the bridge — explain statistical concepts through clinical analogies they already understand (drug dose-response curves, monitoring waveforms, clinical decision-making).
- **Avoid statistical jargon without explanation.** Never use terms like "heteroscedasticity", "likelihood function", "prior distribution", or "Type II error" without first explaining what they mean in plain English with a clinical example.
- **The test for every paragraph:** Could a consultant anaesthetist who has not opened a statistics textbook since medical school read this and follow along? If not, rewrite it.

## Environment

- **Conda env:** `vitaldb` (Python 3.12.12)
- **Kernel:** `vitaldb` (registered at `/Users/dr.idris/Library/Jupyter/kernels/vitaldb`)
- **Recreate:** `conda env create -f environment.yml`
- **Key packages:** vitaldb 1.6.0, pandas 3.0, numpy 2.4, scipy 1.17, matplotlib 3.10, seaborn 0.13, scikit-learn 1.8, statsmodels 0.14, ipywidgets, pyarrow

## Build

```bash
conda activate vitaldb
jupyter-book build .
```

- Output: `_build/html/`
- Execution mode: **off** (notebooks pre-executed, results cached — not re-run at build time)
- `run_in_temp: false` — working directory is the book root
- `only_build_toc_files: true` — only notebooks listed in `_toc.yml` are built

## Project Structure

```
.
├── _config.yml              # Jupyter Book config (sphinx_book_theme, MathJax macros)
├── _toc.yml                 # Table of contents (5 parts + appendices)
├── environment.yml          # Conda env spec
├── intro.md                 # Book landing page
├── references.bib           # Bibliography (BibTeX)
├── README.md                # Full project guide & curriculum outline
│
├── *.ipynb (17 files)       # Executable chapter notebooks (root level)
├── notebooks/               # Chapter framework directories (part1–part5)
├── appendices/              # Setup, formulae, datasets, glossary (stubs)
│
├── vital_db/                # Data: all_cases.csv, labs.csv, tracks.csv
├── *_cache/                 # Parquet caches (eeg, art, co, bis, hrv, icu)
├── *_figures/               # PNG outputs from notebooks
├── assets/                  # logo.png, favicon.ico
└── _build/                  # Build output (do NOT edit)
```

## Data

| File | Records | Description |
|------|---------|-------------|
| `vital_db/all_cases.csv` | 6,388 cases, 74 cols | Demographics, preop labs, intraop drugs/fluids, outcomes |
| `vital_db/labs.csv` | 928,448 rows | Laboratory measurements with timestamps |
| `vital_db/tracks.csv` | 486,449 rows | Monitor waveform records from 7 device types |

### Data loading convention

```python
from pathlib import Path
DATA_DIR = Path('vital_db')
cases  = pd.read_csv(DATA_DIR / 'all_cases.csv')
labs   = pd.read_csv(DATA_DIR / 'labs.csv')
tracks = pd.read_csv(DATA_DIR / 'tracks.csv')
```

**Always use relative paths** (`vital_db/...`) — the book root is the working directory.

## Chapter Map

All notebooks use kernel `vitaldb` (Python 3.12.12). Status: DONE = written & executed, PLANNED = stub/not yet written.

### Part I — Foundations: Learning the Language of Data

| Ch | Title | File | Status |
|----|-------|------|--------|
| 1 | Why Quantitative Anaesthesia? | `notebooks/part1_foundations/ch01_why_quantitative.md` | DONE |
| 1.1 | The VitalDB Dataset: Your Laboratory | `vitaldb_analysis.ipynb` | DONE |
| 1.2 | ASA Classification and Mortality | `asa_mortality.ipynb` | DONE |
| 2 | Types of Variables | `notebooks/part1_foundations/ch02_variable_types.md` | DONE |
| 3 | Descriptive Statistics | `notebooks/part1_foundations/ch03_descriptive_stats.md` | DONE |
| 3.1 | Descriptive Analysis of VitalDB Cohort | `ch03_cohort_descriptive.ipynb` | DONE |
| 4 | Visualisation | `notebooks/part1_foundations/ch04_visualisation.md` | DONE |
| 4.1 | Visualisation Exercises | `ch04_visualisation_exercise.ipynb` | DONE |

### Part II — Inference: Making Decisions from Data

| Ch | Title | File | Status |
|----|-------|------|--------|
| 5 | Probability and Distributions | `notebooks/part2_inference/ch05_probability.md` | DONE |
| 5.1 | Probability and Distributions in the VitalDB Cohort | `ch05_probability_vitaldb.ipynb` | DONE |
| 6 | Hypothesis Testing | `notebooks/part2_inference/ch06_hypothesis_testing.md` | PLANNED |
| 7 | Confidence Intervals and Clinical Significance | `notebooks/part2_inference/ch07_confidence_intervals.md` | PLANNED |

### Part III — Modelling: Understanding Relationships

| Ch | Title | File | Status |
|----|-------|------|--------|
| 8 | Linear Regression | `notebooks/part3_modelling/ch08_linear_regression.md` | PLANNED |
| 9 | Logistic Regression | `notebooks/part3_modelling/ch09_logistic_regression.md` | PLANNED |
| 9.1 | Haemodynamic Predictors of AKI and Mortality | `hemodynamics_analysis.ipynb` | DONE |
| 9.2 | Arterial Line Dynamics and AKI | `art_aki_analysis.ipynb` | DONE |
| 9.3 | Cardiac Index, Perfusion Pressure, and the Kidney | `ci_aki.ipynb` | DONE |
| 9.4 | Perioperative Cardiac Risk Framework | `stemi_data_practice.ipynb` | DONE |
| 10 | Survival Analysis | `notebooks/part3_modelling/ch10_survival_analysis.md` | PLANNED |

### Part IV — Physiology Made Quantitative

| Ch | Title | File | Status |
|----|-------|------|--------|
| 11 | Cardiovascular Physiology | `notebooks/part4_physiology/ch11_cardiovascular.md` | PLANNED |
| 11.1 | Cardiac Output, O₂ Delivery, and Fick Principle | `co_perfusion_analysis.ipynb` | DONE |
| 11.2 | The Anaesthetic Triad: BIS, MAP, and CO | `bis_map_co_coupling.ipynb` | DONE |
| 11.3 | Heart Rate Variability and the ANS | `hrv_anaesthesia.ipynb` | DONE |
| 12 | Respiratory Physiology and Ventilator Mechanics | `notebooks/part4_physiology/ch12_respiratory.md` | PLANNED |
| 13 | Pharmacology: PK/PD Modelling | `notebooks/part4_physiology/ch13_pkpd.md` | PLANNED |
| 13.1 | Propofol PK/PD: Sigmoid Emax Model | `ppf_bis_analysis.ipynb` | DONE |
| 14 | Depth of Anaesthesia: Signals from the Brain | `notebooks/part4_physiology/ch14_depth_of_anaesthesia.md` | PLANNED |
| 14.1 | EEG Spectral Analysis During Anaesthesia | `eeg_waveform_analysis.ipynb` | DONE |

### Part V — Advanced Data Science for the OR

| Ch | Title | File | Status |
|----|-------|------|--------|
| 15 | Feature Engineering for Clinical Data | `notebooks/part5_data_science/ch15_feature_engineering.md` | PLANNED |
| 16 | Machine Learning for Prediction | `notebooks/part5_data_science/ch16_machine_learning.md` | PLANNED |
| 16.1 | Predicting Intraoperative Hypotension | `art_hypotension_prediction.ipynb` | DONE |
| 16.2 | Predicting Unplanned ICU Admission | `intraop_icu_prediction.ipynb` | DONE |
| 16.3 | Unsupervised Haemodynamic Phenotyping | `haemodynamic_phenotyping.ipynb` | DONE |
| 17 | Time Series Analysis | `notebooks/part5_data_science/ch17_time_series.md` | PLANNED |
| 18 | Signal Processing for Anaesthesiologists | `notebooks/part5_data_science/ch18_signal_processing.md` | PLANNED |
| 18.1 | Intraoperative Arrhythmia Detection | `arryhthmia.ipynb` | DONE (stub) |
| 19 | Causal Inference in Observational Data | `notebooks/part5_data_science/ch19_causal_inference.md` | PLANNED |
| 20 | A Full Clinical Data Science Workflow | `notebooks/part5_data_science/ch20_full_workflow.md` | PLANNED |

### Appendices

| App | Title | File | Status |
|-----|-------|------|--------|
| A | Python Environment Setup | `appendices/appendix_a_setup.md` | PLANNED |
| B | Statistical and Physiological Formulae | `appendices/appendix_b_formulae.md` | PLANNED |
| C | VitalDB Data Dictionary | `appendices/appendix_c_data_dictionary.md` | PLANNED |
| D | Supplementary Open-Source Datasets | `appendices/appendix_d_datasets.md` | PLANNED |
| E | Glossary | `appendices/appendix_e_glossary.md` | PLANNED |

## Code Conventions

- **Imports:** pandas, numpy, matplotlib.pyplot, seaborn in every notebook; scipy, sklearn, statsmodels as needed
- **Plot style:** `sns.set_theme(style='whitegrid', palette='muted')`, `dpi=120`, clean spines
- **Caching:** Intermediate results cached as Parquet files in `*_cache/` directories for fast reload
- **Figures:** Saved to `*_figures/` directories as PNG
- **Statistics:** Always show confidence intervals and uncertainty; calibration over accuracy
- **VitalDB API:** `import vitaldb` for live data pulls; local CSV cache preferred for reproducibility

## Writing Style — Human-Readable First

This book must be readable by clinicians who are not statisticians. Every piece of content — prose chapters and notebook markdown — must follow these rules:

- **Every chapter and notebook starts gently.** Begin with a plain-language introduction that explains *what* the chapter covers, *why* it matters clinically, and *what the reader will be able to do* by the end. Do not jump straight into formulas or code. Set the scene first.
- **Define terminology before using it.** Before using a term like "odds ratio" or "log-normal", explain what it means from first principles. Show how it is derived step by step — where the numbers come from, what you divide by what, and why. A reader encountering the term for the first time should be able to follow along without looking anything up.
- **Build up from simple to complex.** Start with the simplest version of a concept using a small, concrete example (e.g., "Out of 10 patients, 2 had nausea — that is a probability of 2/10 = 0.2"). Then generalise to the formal definition. Then show the VitalDB data. Never lead with the general case.
- **Plain language before formulas.** Every concept gets a simple, jargon-free explanation *before* the maths. If a reader skips the equation, they should still understand the idea from the surrounding text.
- **Explain the "so what?"** After every result, table, or figure, explain what it means clinically. Do not leave the reader staring at numbers without interpretation. Walk them through the output: "Look at the ASA IV row — the odds ratio is 66 but the risk ratio is only 50. That gap matters because..."
- **Use concrete clinical scenarios.** Instead of "consider event A and event B", write "imagine you are about to induce anaesthesia and you want to know the chance of hypotension." Ground every abstraction in something the reader has seen in the operating theatre.
- **Conversational, not lecturing.** Write as if explaining to a smart colleague over coffee, not presenting at a conference. Use "you" and "we". Ask rhetorical questions. It is fine to say "this is the important part" or "here is the catch."
- **Narrate figures step by step.** Do not just show a plot and move on. Walk the reader through it: "In the left panel, notice that... In the right panel, the pattern changes because..."
- **Section headers should ask questions or promise answers.** Prefer "Do Odds and Probability Really Mean the Same Thing?" over "Probability and Odds Comparison." Engage the reader's curiosity.
- **Short paragraphs, clear structure.** No wall-of-text paragraphs. Use bullet points, tables, and bold text to make key points scannable.

## Guiding Principles

1. **Every equation has a patient attached** — no abstract formulas without clinical context
2. **Show uncertainty** — confidence intervals, calibration curves, not just point estimates
3. **Reproducibility is non-negotiable** — all figures regenerable from code
4. **Complexity must justify itself clinically** — simplest adequate model wins
5. **Physiology is the ground truth** — models serve understanding, not the reverse
6. **If no one reads it, it does not matter how correct it is** — accessibility and clarity come first

## Important Rules

- **Do NOT edit files in `_build/`** — these are generated outputs
- **Do NOT re-execute notebooks at build time** — execution is set to "off" in `_config.yml`
- **Use relative paths** for data files (not `/Volumes/iDrisAI/...`)
- **All code cells must have the `hide-input` tag** — this enables the show/hide toggle in rendered HTML. When creating new notebooks or adding code cells, always include `"tags": ["hide-input"]` in cell metadata
- **All notebooks must use kernel `vitaldb`** with Python 3.12.12
- **Keep `_toc.yml` in sync** when adding or removing chapters
- **MathJax macros** are defined in `_config.yml` — use `\MAP`, `\CO`, `\SVR`, `\DOtwo`, `\VOtwo` etc. in LaTeX
- **Spelling:** Use British/international English (e.g., "modelling", "anaesthesia", "haemodynamic")
