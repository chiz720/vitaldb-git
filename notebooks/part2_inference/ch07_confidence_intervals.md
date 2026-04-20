# Chapter 7 — Confidence Intervals and Clinical Significance

> *"It is not the statistician's job to tell us what is true, but to tell us what we do not know."*
> — Sir David Cox

---

In Chapter 6, you learned about hypothesis testing — the art of deciding whether a difference you observe is likely to be real or just random noise. You learned that the p-value tells you how surprising your data would be if nothing were really happening.

But the p-value has a fundamental limitation: it answers the wrong question.

What you actually want to know is: *how big is the difference, and how sure are we about that estimate?* Not "is it different from zero?" but "what is the range of plausible values?"

This chapter introduces **confidence intervals** — the answer to that question. And then we go one step further: what does the difference *mean clinically*? This requires the **minimum clinically important difference**, and two summary measures you will use every day: **number needed to treat (NNT)** and **number needed to harm (NNH)**.

### What you will learn in this chapter

By the end, you will be able to:

- **Interpret a 95% CI** — and explain what "95% confidence" actually means
- **Use a CI instead of (or alongside) a p-value** — and know why this gives you more information
- **Calculate the minimum clinically important difference** — the threshold below which a difference does not matter, regardless of statistical significance
- **Calculate NNT and NNH** — and communicate treatment effects in clinically meaningful terms

We start with the simplest question: how do you go from a sample to an estimate?

---

## 7.1 From Sample to Estimate

### The Problem with Point Estimates

Chapter 3 showed you how to calculate the mean, median, and proportion from your data. These are **point estimates** — the single best guess from your sample.

But your sample is never the full population. Every time you take a different group of 40 patients, you get a slightly different mean BIS. The mean from your 40 patients is an estimate of the *true* mean in the population — but how good is that estimate?

This is the core problem of inference: **how far off might your estimate be?**

### The Standard Error

The **standard error (SE)** quantifies the uncertainty in your estimate. It tells you how much the estimate would vary if you repeated the study many times.

For a mean:
$$
SE = \frac{SD}{\sqrt{n}}
$$

For a proportion:
$$
SE = \sqrt{\frac{p(1-p)}{n}}
$$

**Intuition:** As sample size (n) increases, the SE shrinks — larger samples give more precise estimates. As the standard deviation increases, the SE grows — more variable data means less precise estimates.

### A Concrete Example

In Chapter 6, we compared hypotension rates between protocols:

- Old protocol: 10/100 = 10%
- New protocol: 2/40 = 5%

The point estimate of the difference is 10% - 5% = 5% absolute reduction.

But how precise is that 5%? If you repeated this study with different 100+40 patients, you might get a reduction of 2%, or 8%, or even an increase. The SE of the difference tells you how much that variation to expect.

For proportions, the SE of the difference is about 5.4%:

- SE = √[(10%×90%/100) + (5%×95%/40)] ≈ 5.4%

This means: if you repeated the study many times, the typical variation in the difference around the true value is about 5.4%.

---

## 7.2 What Does "95% Confidence" Actually Mean?

This is the most misunderstood concept in statistics. Here is what a 95% confidence interval is — and is not.

### What It Is

A 95% CI is constructed so that if you repeated the study many times, 95% of the intervals you calculate would contain the true population value.

For our hypotension example:
- Observed difference: 5%
- 95% CI: 5% ± (1.96 × 5.4%) = -5.6% to 15.6%

This interval stretches from 5.6% more hypotension with the new protocol to 15.6% less hypotension. It includes zero — you cannot rule out that there is no difference at all.

### What It Is Not

:::{important} The 95% CI is NOT a probability statement about the true value

The interval [-5.6%, 15.6%] does NOT mean "there is a 95% chance the true difference is in this range." The true difference is either in the interval or it is not — we simply do not know which.

The "95%" refers to the method, not the specific interval. If you use this method repeatedly, 95% of the intervals will capture the truth.
:::

This is subtle but important. Think of it like a fishing net:

- The true value is a fish swimming somewhere in the river
- Your study gives you a net (the CI) cast in one spot
- 95% of the times you cast this net, you catch the fish
- But this one cast either caught the fish or it did not

### Why 95%, Not 100%?

Two reasons:

1. **You can never be 100% confident.** Any study with variability has some chance of being misled by random noise. 100% CI would require an infinitely wide interval — useless.

2. **Convention.** 95% is the balance between confidence and precision. You could use 90% or 99% — 95% is simply the most common standard.

---

## 7.3 Confidence Intervals vs. P-Values: Same Information, Different Format

### The Correspondence

For a two-group comparison, there is a direct correspondence:

- If the 95% CI **does not include 0**, then p < 0.05
- If the 95% CI **includes 0**, then p > 0.05

In our hypotension example:

- CI: [-5.6%, 15.6%] includes 0
- p = 0.35 (from Chapter 6)

Both convey the same information: we cannot rule out zero.

### Why CIs Are More Informative

But look at what the CI tells you that the p-value does not:

| P-value only | CI adds |
|---|---|
| "p = 0.35 — not significant" | The true effect could be anywhere from -5.6% to +15.6% |
| | Could be a 15.6% improvement |
| | Could be a 5.6% worsening |
| | We honestly do not know which |

The CI forces you to acknowledge the uncertainty. A p-value of 0.35 says "this could be noise." The CI shows you exactly how wide the range of plausible values is.

### A Second Example

Suppose a different study of the same protocol gave:

- Observed difference: 8%
- 95% CI: [2%, 14%]
- p = 0.01

Here, p < 0.05 and the CI does not include 0 — both agree the difference is statistically significant.

But the CI adds: the true reduction is probably between 2% and 14%. Even the lower bound (2%) is clinically meaningful. You can be confident the protocol helps.

---

## 7.4 The Minimum Clinically Important Difference

### The Problem with Statistical Significance

Imagine you conduct a study of 10,000 patients and find:

- Control group mortality: 10.0%
- Treatment group mortality: 9.8%
- p < 0.001 (highly significant)
- 95% CI: [0.1%, 0.3%]

The difference is 0.2 percentage points — 2 patients per 1000. Statistically, this is rock solid. Clinically, does it matter?

This is the **minimum clinically important difference (MCID)** — the smallest difference that would actually change your practice.

### Defining MCID

The MCID is not a statistical concept. It is a clinical judgment that depends on:

1. **What the outcome matters.** Survival? Quality of life? Recovery time?
2. **What treatments are involved.** Risk, cost, burden of the intervention.
3. **What alternatives exist.** Is there something better?

**Examples:**
- For a life-threatening outcome (death, ICU admission), even a small absolute reduction may matter.
- For a minor outcome (nausea, mild dizziness), a larger reduction may be needed to justify changing practice.
- For an expensive or risky intervention, you need a larger benefit to justify it.

### How to Use MCID

Before you start a study, define the MCID:

- "I would change my practice if the treatment reduced mortality by at least 1%."
- "I would switch protocols if hypotension decreased by at least 5%."

This changes how you interpret results:

- Study shows 0.2% reduction, p < 0.001, but MCID = 1%: **Not clinically significant** — do not change practice.
- Study shows 2% reduction, p = 0.04, MCID = 1%: **Clinically significant** — consider changing practice.

### The Crucial Distinction

:::{important} Always ask two questions

1. **Statistical question:** Is the difference likely to be real? (p-value, CI)
2. **Clinical question:** Is the difference big enough to matter? (MCID)

Both matter. A result can be statistically significant but not clinically important. And conversely — a result can be clinically important but not statistically significant (too small a sample).
:::

---

## 7.5 Number Needed to Treat (NNT)

### The Clinical Translation

Clinicians do not think in "percentage point reductions." They think in "how many patients do I need to treat to prevent one bad outcome?"

The **Number Needed to Treat (NNT)** answers that question.

### The Formula

$$
NNT = \frac{1}{\text{Absolute Risk Reduction}}
$$

where Absolute Risk Reduction (ARR) = Control event rate - Treatment event rate.

### Worked Example

In our hypotension example:

- Control rate: 10%
- Treatment rate: 5%
- ARR = 10% - 5% = 5% = 0.05
- NNT = 1/0.05 = 20

Interpretation: You need to treat 20 patients with the new protocol to prevent one case of hypotension compared to the old protocol.

### Interpretation Guide

| NNT | Clinical meaning |
|---|---|
| 1 | Every patient benefits — guaranteed |
| < 10 | Excellent — like many effective drugs |
| 10-25 | Good — worth considering |
| 25-50 | Moderate — depends on context |
| > 50 | Weak — unlikely to justify change |
| > 100 | Very weak — barely meaningful |

### Inverse: NNT = 1/ARR

This is simple arithmetic. If the ARR is 2% (0.02), NNT = 50. If the ARR is 20% (0.20), NNT = 5.

The smaller the NNT, the more effective the treatment.

---

## 7.6 Number Needed to Harm (NNH)

### When Harms Matter

Every intervention has potential harms. The **Number Needed to Harm (NNH)** is the mirror of NNT — how many patients must be exposed to the treatment to cause one additional harmful outcome?

### The Formula

$$
NNH = \frac{1}{\text{Absolute Risk Increase}}
$$

where Absolute Risk Increase = Treatment harm rate - Control harm rate.

### Worked Example

Suppose the new fluid protocol causes allergic reactions in 1/200 patients (0.5%), while the old protocol causes none:

- Control harm rate: 0%
- Treatment harm rate: 0.5%
- ARI = 0.5% - 0% = 0.5% = 0.005
- NNH = 1/0.005 = 200

Interpretation: You need to use the new protocol on 200 patients to cause one allergic reaction.

### Comparing Benefit and Harm

The clinical decision depends on the balance:

| | NNT | NNH | Verdict |
|---|---|---|---|
| New protocol | 20 (prevent 1 hypotension) | 200 (cause 1 reaction) | Worth it — benefit outweighs harm |
| New drug | 10 (prevent 1 death) | 15 (cause 1 serious AE) | Borderline — close call |
| New drug | 50 (prevent 1 hypotension) | 20 (cause 1 reaction) | Not worth it — harms outweigh benefits |

---

## 7.7 Combining It All: A Decision Framework

### The Full Picture

When you read a study or collect your own data, work through these steps:

1. **What is the point estimate?** (e.g., 5% absolute reduction)
2. **What is the 95% CI?** (e.g., -5.6% to 15.6%)
3. **Is the CI consistent with clinical significance?** (e.g., even the best case is within MCID)
4. **What is the NNT?** (e.g., 20)
5. **What is the NNH?** (e.g., 200)
6. **Is the benefit worth the risk/cost?** (clinical judgment)

### Clinical Scenario

A colleague shows you a paper on a new vasopressor:

- Control: 15% hypotension at induction
- New drug: 8% hypotension at induction
- p = 0.02, 95% CI: [2%, 12%]
- NNT = 1/(15%-8%) = 1/0.07 ≈ 14
- Side effect: 1% mild tachycardia vs. 0.2% in control
- NNH = 1/(1%-0.2%) = 1/0.008 = 125

Your MCID for hypotension is 5%. Even the lower CI bound (2%) is below your MCID — but it is not far below, and the CI does cross your MCID.

Interpretation: The drug probably reduces hypotension, possibly by enough to matter. The NNT of 14 is reasonable. The NNH of 125 means one episode of tachycardia per 125 patients — manageable. Worth considering for high-risk patients.

---

## 7.8 Common Pitfalls

### 1. Interpreting CI Width Without Context

A narrow CI (precise estimate) is not necessarily clinically important. A wide CI (imprecise estimate) may still contain clinically important values.

Always look at where the CI sits relative to your MCID.

### 2. Ignoring Sample Size

With very large samples, even tiny differences become "statistically significant." Always ask: "is this clinically important, or just statistically detectable?"

### 3. Mixing Up Absolute and Relative Risk

A study reports "50% relative risk reduction!" That sounds impressive. But if the event rate is 2% → 1%, the absolute reduction is only 1 percentage point. NNT = 100, not 2.

:::{important} Always convert to absolute terms

When you see a relative risk reduction, ask: "2% of what?" Convert to absolute terms before making clinical decisions.
:::

### 4. Forgotting to Consider Harms

Every decision has trade-offs. NNT without NNH is incomplete. An NNT of 5 with an NNH of 6 is a net negative.

### 5. Using the Wrong CI Formula

Different statistics have different CI formulas. The normal-approximation CI (mean ± 1.96 × SE) works for means and large samples, but not for:

- Proportions near 0% or 100%
- Small samples with skewed data
- Non-parametric statistics

For small samples or non-normal data, use **bootstrap confidence intervals** — resample from your data thousands of times to get the empirical distribution.

---

## 7.9 Summary

| Concept | What it tells you |
|---|---|
| **Standard error (SE)** | How precise your estimate is — smaller is better |
| **95% CI** | The range of plausible values for the true effect |
| **CI includes 0** | No statistically significant difference at α = 0.05 |
| **MCID** | The smallest difference that would change your practice |
| **NNT** | How many patients need treatment to prevent one outcome |
| **NNH** | How many patients need exposure to cause one harm |

Key takeaways:

- **CIs are more informative than p-values** — they show you the range of plausible values, not just whether zero is included
- **Always check clinical significance** — a p < 0.001 result can be clinically trivial
- **Convert to NNT/NNH** — these are the clinical scales that matter for decisions
- **Consider both benefit and harm** — the clinical decision is always a trade-off

---

## 7.10 Coming Next

In Part III, we move from inference (comparing groups) to **modelling** (understanding relationships). Chapter 8 introduces **linear regression** — the fundamental method for understanding how one variable relates to another, and for predicting outcomes from predictors.

---

## Further Reading

- Guyatt, G. et al. "Users' Guides to the Medical Literature." *JAMA* 271, no. 1 (1994): 59–65. [Series on NNT/evidence-based medicine]
- Altman, D.G. *Practical Statistics for Medical Research*. London: Chapman & Hall, 1991. [Chapter 10]
- Sackett, D.L. et al. *Evidence-Based Medicine: How to Practice and Teach EBM*. Edinburgh: Churchill Livingstone, 2000.