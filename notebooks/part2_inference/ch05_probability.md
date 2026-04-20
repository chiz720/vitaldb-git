# Chapter 5 — Probability and Distributions

> *"Probability is the very guide of life."*
> — Marcus Tullius Cicero

---

You have spent Part I learning to describe data — to summarise it, visualise it, and recognise the shapes of distributions. But describing what you see is not the same as deciding what it means.

Here is a situation every anaesthetist has faced. You titrate propofol to a target BIS of 45 and the monitor bounces between 38 and 52. You do not panic. You do not bolus. You watch. Why? Because you have an *intuitive* sense of probability — you know that a BIS of 52 during surgical stimulation is probably fine, even though 52 is outside the "target" range. You are, without realising it, performing a probabilistic assessment: *given the noise in the BIS signal and the surgical stimulus, how likely is it that this patient is genuinely too light?*

This chapter gives you the formal language for that intuition. Do not worry — we will build everything up from scratch, one step at a time.

### What you will learn in this chapter

By the end, you will be able to:

- **Calculate probability, odds, and risk** from raw data — and know when they give different answers
- **Recognise five common distributions** (Normal, Log-normal, Binomial, Poisson, Exponential) and know which clinical variables follow which shape
- **Understand Bayes' theorem** well enough to explain why a positive troponin does not always mean a heart attack
- **Explain the Central Limit Theorem** — the single most important result in statistics — and why it means you can use standard methods even when your data is messy

We start with the basics — what probability actually means — and build up from there. If you are comfortable with fractions, you have all the maths you need.

---

## 5.1 Probability Basics

### What Is Probability?

Before we get into formulas, let us start with a simple question: **what do we mean when we say something is "likely"?**

Suppose you are in the recovery room and you have looked after 20 patients today. Three of them had postoperative nausea. If someone asks "what is the probability of nausea in your patients?", the answer is straightforward:

$$
\text{Probability} = \frac{\text{Number of patients with nausea}}{\text{Total number of patients}} = \frac{3}{20} = 0.15 \text{ (or 15\%)}
$$

That is all probability is — a fraction. The number of times something happened, divided by the total number of opportunities it could have happened. It always falls between 0 (never happens) and 1 (always happens).

In clinical medicine, **probability** and **risk** mean exactly the same thing. When we say "the risk of postoperative nausea is 15%", we mean the probability is 0.15. "Risk" is just the clinical word for probability when we are talking about something bad.

### What Are Odds?

Now here is where things get slightly trickier. **Odds** answer the same question — "how likely is this event?" — but they frame it differently.

Instead of dividing by *everyone*, odds divide by *the people who did NOT have the event*:

$$
\text{Odds} = \frac{\text{Number with the event}}{\text{Number without the event}} = \frac{3}{17} = 0.176
$$

Think of it as a ratio of "yes" to "no." If you are a betting person, this is the natural way to think: "for every 3 patients who had nausea, 17 did not" — odds of 3 to 17, or about 1 to 5.7.

### When Do Odds and Probability Differ?

For our nausea example: probability = 0.15, odds = 0.176. Close, but not identical. Now watch what happens as the event becomes more common:

| Event rate | Probability | Odds | Difference |
|---|---|---|---|
| 1 in 100 | 0.01 | 0.0101 | Negligible |
| 5 in 100 | 0.05 | 0.053 | Small |
| 20 in 100 | 0.20 | 0.25 | Noticeable |
| 50 in 100 | 0.50 | 1.00 | Large |
| 90 in 100 | 0.90 | 9.00 | Enormous |

**The pattern:** when the event is rare (< 5%), the denominators are nearly the same (total ≈ non-events), so probability ≈ odds. As the event becomes common, the denominators diverge and odds grow much faster than probability.

### Why Does This Matter?

Because **logistic regression** — the most widely used method for predicting binary outcomes in clinical research (Chapter 9) — naturally produces **odds ratios**, not risk ratios. When you read a paper that says "OR = 2.5 for postoperative nausea", you need to know whether that means the risk is 2.5 times higher (approximately true if nausea is rare) or something less dramatic (true if nausea is common).

:::{important} Odds ratios exaggerate risk when outcomes are common
An odds ratio of 2.0 for a rare outcome (baseline risk 1%) means the risk roughly doubles — straightforward. But an odds ratio of 2.0 for a common outcome (baseline risk 40%) only corresponds to a risk ratio of about 1.4. The more common the outcome, the more the odds ratio overstates the actual risk increase. Always ask: "what was the baseline rate?" before interpreting an odds ratio.
:::

### Quick Reference

| Measure | What you divide | Range | When to use |
|---|---|---|---|
| **Probability (Risk)** | Events ÷ total | 0 to 1 | The natural, intuitive measure — use this for communication |
| **Odds** | Events ÷ non-events | 0 to ∞ | The output of logistic regression — know how to convert back to probability |

---

### Relative Risk and Risk Difference — Two Ways to Compare Groups

When comparing two groups (say, ASA I vs. ASA III patients), there are two natural questions:

- **How many times more likely** is the event in one group? → **Relative Risk (RR)**
- **How many more patients per 100** have the event? → **Risk Difference (RD)**

$$
\text{Relative Risk (RR)} = \frac{P(\text{event} \mid \text{exposed})}{P(\text{event} \mid \text{unexposed})}
$$

$$
\text{Risk Difference (RD)} = P(\text{event} \mid \text{exposed}) - P(\text{event} \mid \text{unexposed})
$$

**A tale of two numbers:** If mortality is 0.5% in ASA I–II patients and 3.0% in ASA III–IV patients, the relative risk is 6.0 ("six times the risk") and the risk difference is 2.5 percentage points ("an additional 2.5 patients per 100 die"). Both statements are true. The first sounds alarming; the second sounds modest. Which one you choose to highlight shapes the clinical story you tell.

:::{warning} The newspaper headline trap
A drug that reduces mortality from 0.002% to 0.001% has a "50% relative risk reduction" — and that is what the press release will say. But the absolute risk difference is 0.001%, meaning you would need to treat 100,000 patients to prevent one death. Headlines love relative numbers because they sound impressive. Clinical decisions require absolute numbers because they tell you how many patients actually benefit. **Always report both.**
:::

---

### Conditional Probability — "Given That..."

Here is a subtle but critical distinction. The probability of an event **given** that something else has happened is written $P(A \mid B)$:

$$
P(A \mid B) = \frac{P(A \cap B)}{P(B)}
$$

The vertical bar $\mid$ means "given" or "assuming we already know that". The trap is that $P(A \mid B)$ and $P(B \mid A)$ are usually **not** the same thing — and confusing them can lead to serious clinical errors.

**A concrete example — hypotension and propofol:**

Imagine you are about to induce anaesthesia and you want to know:
- $P(\text{hypotension} \mid \text{propofol induction})$ — "If I use propofol, what is the chance of hypotension?" This is the **forward-looking** question. It helps you decide which induction agent to choose.

Now imagine a morbidity review meeting. A colleague presents 20 cases of post-induction hypotension and notes that propofol was used in 18 of them:
- $P(\text{propofol} \mid \text{hypotension})$ = 18/20 = 90%. This is the **backward-looking** question. It tells you that propofol was used in most hypotension cases — but of course it was, because propofol is used in most *all* cases. This 90% tells you almost nothing about whether propofol *caused* the hypotension.

Confusing these two directions — the "what will happen?" question with the "what did happen?" question — is called the **base rate fallacy**. It is the reason why anecdotal case series ("every time I saw X, the patient had received Y") can be profoundly misleading.

---

### Bayes' Theorem — How to Update Your Beliefs

Bayes' theorem is the mathematical tool that correctly links $P(A \mid B)$ to $P(B \mid A)$. In words: it tells you how to update what you believe about a diagnosis after receiving a new piece of evidence.

$$
P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B)}
$$

This looks abstract, so let us work through a real example.

**Scenario — Postoperative troponin screening:**

You are managing a 72-year-old patient after hip replacement. The surgical team has ordered a routine postoperative troponin "just to check." It comes back elevated. What is the probability of a genuine myocardial infarction?

| What you know | Value | In plain language |
|---|---|---|
| $P(\text{MI})$ — prior probability | 5% | Before the test, about 1 in 20 high-risk surgical patients has a perioperative MI |
| $P(\text{trop+} \mid \text{MI})$ — sensitivity | 95% | The test catches 95% of real MIs |
| $P(\text{trop+} \mid \text{no MI})$ — false positive rate | 10% | But 10% of patients *without* MI also have elevated troponin (from renal impairment, skeletal muscle trauma, demand ischaemia) |

Now apply Bayes' theorem:

$$
P(\text{MI} \mid \text{trop+}) = \frac{0.95 \times 0.05}{(0.95 \times 0.05) + (0.10 \times 0.95)} = \frac{0.0475}{0.1425} = 0.333
$$

**The result is 33%, not 95%.** Even with a highly sensitive test, a positive troponin in a population where MI is uncommon (5% prior) is more likely to be a false alarm than a true diagnosis. The low base rate drags the posterior probability down.

This is exactly why experienced clinicians do not panic at a single elevated troponin after non-cardiac surgery. They integrate it with the clinical picture — the ECG, the haemodynamic trajectory, the patient's symptoms — each piece of evidence updating the probability. That process of sequential updating *is* Bayesian reasoning, whether or not you write down the formula.

:::{note} Bayes' theorem mirrors how clinicians actually think
You do not look at a single lab result in isolation. You start with a prior impression ("this patient is low risk"), receive evidence (an abnormal test result), and update ("now I'm more concerned, but not certain"). Then you order another test, and update again. Each new piece of information — a repeat troponin, an ECG, an echocardiogram — shifts the probability. Bayes' theorem simply formalises what good clinical reasoning already does intuitively.
:::

:::{toggle} Show Python
```python
# Bayesian posterior for troponin screening
prior       = 0.05   # P(MI)
sensitivity = 0.95   # P(trop+ | MI)
fp_rate     = 0.10   # P(trop+ | no MI)

p_trop_pos  = sensitivity * prior + fp_rate * (1 - prior)
posterior   = (sensitivity * prior) / p_trop_pos

print(f"Prior P(MI):      {prior:.1%}")
print(f"P(trop+ | MI):    {sensitivity:.1%}")
print(f"P(trop+ | no MI): {fp_rate:.1%}")
print(f"P(MI | trop+):    {posterior:.1%}")
```
:::

---

### Independence — Can You Multiply Probabilities?

Two events are **independent** if knowing about one tells you nothing about the other:

$$
P(A \cap B) = P(A) \cdot P(B) \quad \Leftrightarrow \quad P(A \mid B) = P(A)
$$

**Why this matters in practice:** If complications were independent, you could estimate the risk of having *both* nausea and pain by simply multiplying their individual probabilities. But in reality, nausea and pain often share a common cause — opioid administration, for instance — so they tend to occur together more often than multiplication would predict.

Most clinical variables are **dependent**. Haemoglobin and creatinine are linked (anaemia of chronic kidney disease). ASA class and mortality are linked (sicker patients die more often). Age and comorbidities are linked. Assuming independence when things are actually correlated leads to predictions that are overconfident — the model thinks it has more independent information than it really does.

A practical rule of thumb: if two variables share a plausible physiological or clinical mechanism, assume they are dependent until proven otherwise.

---

## 5.2 Common Distributions

A probability distribution is simply a description of what values a variable can take and how likely each value is. Think of it as the "shape" of the data — where most values cluster, how spread out they are, and whether they trail off symmetrically or have a long tail in one direction.

Why do we need to know about distributions? Because every statistical model makes assumptions about the shape of the data. Using a method designed for bell-curve data on something heavily skewed is like using a spanner on a screw — it might work, but probably not well.

Here are the five distributions you will encounter most often in perioperative data.

### The Normal (Gaussian) Distribution — The Bell Curve

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)
$$

**Parameters:** mean ($\mu$) — the centre — and standard deviation ($\sigma$) — the spread.

**What it looks like:** A symmetric bell. Most values cluster near the mean, and values become progressively rarer as you move away. The famous 68-95-99.7 rule: about 68% of values fall within 1 SD of the mean, 95% within 2 SDs, and 99.7% within 3 SDs.

**Where you will see it:**
- **Patient height** — most adults are near average, with roughly equal numbers of tall and short people
- **BMI** in a surgical population — approximately symmetric, perhaps slightly right-skewed
- **Resting blood pressure** in a healthy population

**When to expect it:** Variables that result from adding together many small, independent effects tend to be normal. Height, for example, is influenced by hundreds of genes plus nutrition and environment — each contributing a small amount. When you add many small things together, the sum tends toward a bell curve. (This is actually the Central Limit Theorem at work — see Section 5.3.)

:::{toggle} Show Python
```python
import numpy as np
from scipy import stats

# Fit a normal distribution to patient heights
heights = cases['height'].dropna()
mu, sigma = stats.norm.fit(heights)
print(f"Height: mean = {mu:.1f} cm, SD = {sigma:.1f} cm")
print(f"68% interval: [{mu - sigma:.1f}, {mu + sigma:.1f}]")
print(f"95% interval: [{mu - 2*sigma:.1f}, {mu + 2*sigma:.1f}]")
```
:::

---

### The Log-Normal Distribution — When the Tail Matters

If you take the logarithm of a variable and it becomes normally distributed, the original variable is **log-normal**.

**What it looks like:** A hump near the left with a long tail stretching to the right. Most values are modest, but a few are very large.

**Where you will see it:**
- **Drug doses** — most patients need a dose near the typical amount, but some require much more (enzyme inducers, high BMI, tolerance)
- **Laboratory values** like creatinine, AST, ALT — most patients have normal values, but a minority have very high values from organ dysfunction
- **Surgical duration** — most operations finish in a typical time, but some go on far longer than expected
- **Blood loss** — the majority of cases have minimal bleeding, but a few have massive haemorrhage

**When to expect it:** Variables that result from *multiplying* many factors tend to be log-normal. Drug metabolism involves multiplicative steps (clearance × volume × enzyme activity). Blood loss depends on the product of surgical complexity, tissue vascularity, and coagulation status.

**The practical implication:** For log-normal data, the ordinary average (arithmetic mean) is pulled upward by the long tail and does not represent a "typical" patient. The **geometric mean** — the average on the log scale, then converted back — is a better summary. When you see a lab value reported as "mean ± SD" with a huge SD, the authors probably should have log-transformed the data first.

:::{important} Log-transform before analysis
This is not a statistical trick — it reflects the actual data-generating process. When you log-transform creatinine values and they become normally distributed, you are not "cheating"; you are recognising that creatinine values arise from multiplicative physiological processes. The geometric mean and geometric SD are the natural summaries for such data.
:::

:::{toggle} Show Python
```python
# Fit log-normal distribution to propofol doses
ppf = cases['intraop_ppf'].dropna()
ppf = ppf[ppf > 0]  # Exclude zero doses (volatile-only cases)
shape, loc, scale = stats.lognorm.fit(ppf, floc=0)
log_mu  = np.log(scale)
log_sig = shape
print(f"Log-normal fit: log-mean = {log_mu:.2f}, log-SD = {log_sig:.2f}")
print(f"Geometric mean = {np.exp(log_mu):.1f} mg")
```
:::

---

### The Binomial Distribution — Counting Yes/No Outcomes

$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}
$$

**Parameters:** $n$ (number of patients) and $p$ (probability of the event per patient).

**In plain language:** You have $n$ patients, each with the same probability $p$ of having the event (say, developing AKI). The binomial distribution tells you how likely it is to see exactly $k$ events out of $n$ patients.

**Where you will see it:**
- "Out of 100 patients, how many will develop AKI?" — if each has a 5% chance, the binomial says you would most often see 3–7 cases, rarely more than 12
- "What is the probability of 3 failed intubations in a row?" — if each attempt has a 2% failure rate, the binomial gives $0.02^3 = 0.000008$, or about 1 in 125,000
- Any time you are counting how many patients out of a group have a binary outcome

**When to use it:** Whenever your outcome is yes/no and you are counting across patients. The binomial is the foundation of proportions, risk calculations, and logistic regression.

:::{toggle} Show Python
```python
# Probability of observing k deaths in a sample of 100 patients
n = 100
p = 0.002  # Observed mortality rate in VitalDB

for k in range(4):
    prob = stats.binom.pmf(k, n, p)
    print(f"P(exactly {k} deaths in {n} patients) = {prob:.4f}")
```
:::

---

### The Poisson Distribution — Counting Rare Events

$$
P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

**Parameter:** $\lambda$ (the average rate), which equals both the mean and the variance.

**In plain language:** The Poisson distribution models how many times a rare event happens in a fixed window — how many blood transfusions a patient needs, how many vasopressor boluses are given in an hour, how many ventilator alarms go off per shift.

**Where you will see it:**
- Number of RBC units transfused per case (most patients get 0, some get 1–2, a few get many)
- Number of vasopressor boluses during a case
- Number of critical incidents per operating day
- Number of central line insertion attempts

**A key feature — equidispersion:** For a true Poisson variable, the mean equals the variance. If the variance is much larger than the mean (overdispersion), the Poisson model does not fit well — you probably have a mixture of processes (e.g., some patients who never need transfusion and others who need a lot). The companion notebook shows this in action with VitalDB transfusion data.

:::{toggle} Show Python
```python
# Fit Poisson to RBC transfusion counts
rbc = cases['intraop_rbc'].dropna()
rbc_int = rbc.round().astype(int)
lam = rbc_int.mean()
print(f"Mean RBC units = {lam:.2f}")
print(f"Variance = {rbc_int.var():.2f}")
print(f"Variance/Mean ratio = {rbc_int.var()/lam:.2f} (>1 = overdispersed)")
```
:::

---

### The Exponential Distribution — Waiting for the Next Event

$$
f(x) = \lambda e^{-\lambda x}, \quad x \geq 0
$$

**Parameter:** rate ($\lambda$). The average waiting time is $1/\lambda$.

**In plain language:** If events happen randomly at a steady rate (like Poisson events), the exponential distribution describes how long you wait between them. It has a curious property called **memorylessness**: the probability of the next event occurring in the next 10 minutes is the same whether you have been waiting 5 minutes or 5 hours.

**Where you will see it:**
- Time between vasopressor boluses
- Time between ventilator alarms
- Equipment failure intervals

**The clinical catch:** Memorylessness is a strong assumption. In reality, the longer an anaesthetic goes on, the more likely certain complications become — hypothermia worsens, fluid shifts accumulate, fatigue sets in. So while the exponential distribution is a useful starting point, real clinical hazard rates usually change over time. Chapter 10 (Survival Analysis) addresses this with time-varying hazard models.

---

### Distribution Reference Table

| Distribution | Type | Shape | VitalDB Example | When to Use |
|---|---|---|---|---|
| Normal | Continuous | Symmetric bell | Height, BMI | Data from additive processes; values can be negative |
| Log-normal | Continuous | Right-skewed, long tail | Propofol dose, creatinine, blood loss | Positive-only data from multiplicative processes |
| Binomial | Discrete | Hump-shaped (for moderate $p$) | Mortality count, AKI incidence | Counting yes/no outcomes in a fixed group |
| Poisson | Discrete | Right-skewed, starts at 0 | RBC units, vasopressor boluses | Counting rare events; check that mean ≈ variance |
| Exponential | Continuous | Steeply declining from 0 | Time between critical events | Waiting times when events are memoryless |

---

## 5.3 The Central Limit Theorem

If you remember only one thing from this chapter, make it this.

### The Big Idea

The **Central Limit Theorem (CLT)** says: if you take a sample of $n$ observations from *any* distribution and compute the sample mean, the distribution of that mean will be approximately **normal** — regardless of the shape of the original data — as long as $n$ is large enough.

$$
\bar{X} \sim N\left(\mu, \frac{\sigma^2}{n}\right) \quad \text{as } n \to \infty
$$

**Why is this remarkable?** Consider propofol doses in VitalDB — the distribution is heavily right-skewed, nowhere near a bell curve. But if you repeatedly draw random samples of 100 patients and compute the average dose each time, those averages *will* form a bell curve. The individual data points are messy; the averages are orderly.

The standard deviation of this bell curve of averages is $\sigma / \sqrt{n}$, called the **standard error of the mean (SEM)**. It shrinks as the sample size grows — which is why larger studies give more precise estimates.

### What the CLT Does and Does Not Say

This is where many people get confused:

| The CLT says | The CLT does **not** say |
|---|---|
| The *average* becomes normally distributed | Individual patients become normal |
| This works for any data shape (with finite variance) | The original data becomes normal |
| Larger samples converge faster | Any sample size is large enough |
| The SEM shrinks as $\sqrt{n}$ | The SD of individual patients shrinks |

**A common misconception:** "My data is not normally distributed, so I cannot use a t-test." In many cases, you can — because the t-test depends on the normality of the *mean*, not the raw data. The CLT ensures that the mean is approximately normal for large enough samples.

### How Large is "Large Enough"?

It depends on how skewed your data is:

| Data shape | Approximate $n$ needed |
|---|---|
| Symmetric (like height) | 10–20 |
| Mildly skewed (like BMI) | 20–30 |
| Moderately skewed (like blood loss) | 30–50 |
| Heavily skewed (like ICU length of stay) | 100+ |

The common "rule of 30" is a rough guide, not a guarantee. The companion notebook demonstrates this directly — we draw bootstrap samples from the heavily skewed propofol dose distribution and watch the sampling distribution of means gradually become normal.

### Three Things the CLT Means for Your Clinical Research

**1. Confidence intervals work even for non-normal data.** The confidence interval for a mean is based on the normality of $\bar{X}$, not of the raw data. With $n = 6{,}388$ VitalDB cases, the CLT is more than adequate for any variable.

**2. t-tests and ANOVA are more robust than you think.** These tests assume normality of the test statistic, not of the data itself. The CLT is why they work on blood loss data and drug doses.

**3. Beware the difference between SEM and SD.** This is a classic pitfall. The SD tells you how much individual patients vary. The SEM tells you how precisely you have estimated the average. With $n = 6{,}388$, the SEM is about 80 times smaller than the SD ($\text{SEM} = \text{SD} / \sqrt{6388}$). Reporting mean ± SEM instead of mean ± SD makes your data look 80 times more precise than it really is.

:::{warning} Large samples make everything "statistically significant"
With $n = 6{,}388$, even a trivial difference — say, 0.1 kg difference in mean weight between men and women — will be statistically significant (p < 0.05). This is not because the difference matters; it is because the SEM is so small that the test can detect absurdly tiny effects. Statistical significance is not clinical significance. A p-value tells you the effect is probably not zero; it does not tell you the effect is large enough to matter. Chapter 7 addresses this directly.
:::

:::{toggle} Show Python — CLT Simulation
```python
# CLT demonstration: sampling distribution of mean propofol dose
import numpy as np
import matplotlib.pyplot as plt

ppf = cases['intraop_ppf'].dropna().values
ppf = ppf[ppf > 0]  # heavily right-skewed

sample_sizes = [5, 30, 100, 500]
n_reps = 2000

fig, axes = plt.subplots(1, len(sample_sizes), figsize=(14, 3))
for ax, n in zip(axes, sample_sizes):
    means = [np.random.choice(ppf, size=n, replace=True).mean()
             for _ in range(n_reps)]
    ax.hist(means, bins=40, density=True, alpha=0.7, color='#4C72B0')
    ax.set_title(f'n = {n}')
    ax.set_xlabel('Sample mean (mg)')
plt.suptitle('Sampling Distribution of Mean Propofol Dose', fontweight='bold')
plt.tight_layout()
plt.show()
```
:::

---

## VitalDB Exercise: Probability and Distributions in Practice

The companion notebook (`ch05_probability_vitaldb.ipynb`) takes every concept from this chapter and applies it to the VitalDB cohort — real numbers, real patients, real results.

**Exercise 1 — Empirical Probabilities, Odds, and Risk Ratios**

We compute mortality probability, odds, and relative risk across ASA classes and see for ourselves that odds ≈ probability for rare events (mortality) but not for common events (elevated creatinine). The divergence between odds ratios and risk ratios is not an abstract concern — it is visible in our own data.

**Exercise 2 — Fitting Distributions to Real Clinical Data**

We fit Normal, Log-normal, and Poisson distributions to VitalDB variables (height, propofol dose, creatinine, RBC transfusions) and check the fits with Q-Q plots and Kolmogorov–Smirnov tests. Some distributions fit well; others fail — and the failures are as instructive as the successes.

**Exercise 3 — The Central Limit Theorem in Action**

We draw thousands of bootstrap samples from the heavily skewed propofol dose distribution and watch — visually and statistically — as the sampling distribution of the mean transforms from a skewed mess into a bell curve. You will see the exact sample size at which the magic happens.

---

## 5.4 Summary

| Concept | The One-Sentence Version | Why It Matters in Anaesthesia |
|---|---|---|
| Probability vs. odds | Probability = events/total; odds = events/non-events — nearly identical for rare events, very different for common ones | Odds ratios from logistic regression overstate risk when the outcome is common (>10%) |
| Conditional probability | $P(A \mid B) \neq P(B \mid A)$ — the probability of rain given clouds is not the probability of clouds given rain | Sensitivity (test positive given disease) is not the same as positive predictive value (disease given test positive) |
| Bayes' theorem | Start with a prior belief, multiply by the evidence, get an updated belief | Explains why screening tests generate false alarms in low-risk populations — and why experienced clinicians integrate multiple information sources |
| Normal distribution | The bell curve — symmetric, from additive processes | Height, BMI, blood pressure; the foundation of most classical statistics |
| Log-normal distribution | Right-skewed with a long tail — from multiplicative processes | Drug doses, lab values, surgical duration; use geometric mean, not arithmetic |
| Binomial distribution | Counting yes/no outcomes across patients | Mortality rates, complication incidence, the basis of logistic regression |
| Poisson distribution | Counting rare events; mean should equal variance | Transfusion units, vasopressor boluses; check for overdispersion |
| Exponential distribution | Time between random events; memoryless | A starting point for inter-event intervals, but real hazards usually change over time |
| Central Limit Theorem | Averages become normally distributed, even when the data is not | Justifies t-tests, confidence intervals, and most of inferential statistics — provided $n$ is large enough for the degree of skew |
| SEM vs. SD | SEM = SD/$\sqrt{n}$ — precision of the average, not spread of the data | Reporting SEM instead of SD makes data look falsely precise; always report SD for description |

---

## Further Reading

- Bland, M. (2015). *An Introduction to Medical Statistics* (4th ed.). Oxford University Press. — Chapters 5 and 7 are excellent, accessible introductions to probability and the normal distribution for clinicians.
- Gigerenzer, G. (2002). *Calculated Risks: How to Know When Numbers Deceive You*. Simon & Schuster. — A superb and highly readable account of Bayesian reasoning, the base rate fallacy, and why doctors and patients alike misunderstand screening test results. If you read one book on probability, make it this one.
- Altman, D.G., & Bland, J.M. (1994). Diagnostic tests 2: predictive values. *BMJ*, 309(6947), 102. — A concise two-page primer on how sensitivity, specificity, and prevalence interact.
- Limpert, E., Stahel, W.A., & Abbt, M. (2001). Log-normal distributions across the sciences: keys and clues. *BioScience*, 51(5), 341–352. — Why the log-normal distribution is everywhere, and why it matters.
