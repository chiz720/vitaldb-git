# Chapter 6 — Hypothesis Testing

> *"The null hypothesis is what we assume to be true until we have enough evidence to reject it."*
> — R.A. Fisher

---

You learned in Chapter 5 how to calculate probabilities, odds, and risks from data. But every clinician faces a harder question: *how do I know if what I am seeing is real, or just random noise?*

Imagine this. You change your fluid management protocol — you start giving 500 mL of crystalloid before induction instead of 250 mL. Over the next month, you notice that only 2 of your 40 patients developed hypotension after induction, compared to the usual 8 or 10. Is that a real improvement, or just good luck? How would you decide whether to change your practice permanently?

This chapter gives you the formal tools to answer that question. We call it **hypothesis testing** — the art of deciding whether differences you observe in data are likely to be real, or could have happened by chance.

### What you will learn in this chapter

By the end, you will be able to:

- **Interpret a p-value** — and know what it does and does not tell you
- **Choose the right test** for your data (t-test, Mann-Whitney, chi-squared, or ANOVA)
- **Distinguish statistical significance from clinical importance** — why a p-value of 0.001 does not always mean the difference matters
- **Recognise common pitfalls** — why "p < 0.05" is not the same as "the treatment works"

We start with the simplest version of the problem: comparing two groups.

---

## 6.1 The Core Idea: Is This Different, or Just Noise?

### A Concrete Example

Let us go back to your fluid protocol change. Before the change, you had 100 patients and 10 developed hypotension — a rate of 10%. After the change, you have 40 patients and 2 developed hypotension — a rate of 5%.

The raw numbers look promising. But here is the uncomfortable question: *would you expect some variation even if nothing changed?* If the true rate is 10%, purely by chance you might see 2/40 = 5% in a small sample, or 8/40 = 20% in another. How do you know if 5% is "real"?

### The Two Hypotheses

Statisticians formalise this by setting up two competing claims:

- **Null hypothesis (H₀):** The new protocol makes no difference. The true hypotension rate is still 10%, and any difference you see is just random variation.
- **Alternative hypothesis (H₁):** The new protocol really does reduce hypotension. The true rate is lower than 10%.

You have data that seems to support H₁. But under H₀ — the assumption that nothing changed — could you reasonably expect to see 2/40 by chance alone?

This is what a **p-value** answers.

### What a P-Value Actually Means

The p-value is the probability of seeing data at least as extreme as what you observed, *if the null hypothesis were true*.

In our example:
- We observed 2/40 = 5%
- Under H₀, the true rate is 10%
- If nothing changed, what is the probability of seeing 2 or fewer events in 40 patients?

This is a Binomial(40, 0.10) calculation. The answer is about 0.14 — a 14% chance. In other words, if you repeated this experiment many times with no real change, you would see 2 or fewer events about 14% of the time.

The p-value is 0.14. That is not very surprising — it could easily happen by chance.

### Interpreting the P-Value

Here is the critical part that most people get wrong:

:::{important} The p-value is NOT the probability that the null hypothesis is true

A p-value of 0.14 does not mean "there is a 14% chance the null hypothesis is true." It means "if the null hypothesis were true, there is a 14% chance of seeing data this extreme."

This sounds like a subtle distinction, but it is fundamentally different. The p-value tells you about the *data*, not the *hypothesis*.
:::

Think of it this way: if you flip a coin 10 times and get 7 heads, the p-value answers "how surprised should I be if this is a fair coin?" It does not tell you whether the coin is biased — just whether the data you got would be unusual if the coin were fair.

### The Decision Rule

Conventionally, we say a result is "statistically significant" if p < 0.05. This means:

- If H₀ were true, there is less than a 5% chance of seeing data this extreme
- That is unusual enough that we decide to reject H₀ and act as if the difference is real

In our hypotension example, p = 0.14 > 0.05. We cannot conclude the fluid protocol works — the difference could easily be due to chance.

---

## 6.2 Choosing the Right Test

The example above is simple: we are comparing two proportions (10% vs 5%). But clinical data comes in many forms, and you need different tests depending on:

1. What kind of data you have (continuous vs. categorical)
2. How many groups you are comparing
3. Whether the data is normally distributed

### Continuous vs. Categorical Data

- **Continuous data:** Numbers on a scale — blood pressure, BIS values, infusion rates. Can take any value within a range.
- **Categorical data:** Discrete categories — ASA class (I, II, III, IV), died/survived, yes/no. Counts how many fall into each category.

### The Decision Tree

| Your data | Comparison | Test |
|---|---|---|
| Continuous, 2 groups, normal distribution | Compare means | **t-test** |
| Continuous, 2 groups, non-normal | Compare medians | **Mann-Whitney** |
| Continuous, 3+ groups, normal | Compare means across groups | **ANOVA** |
| Continuous, 3+ groups, non-normal | Compare medians across groups | **Kruskal-Wallis** |
| Categorical (counts) | Compare proportions | **Chi-squared** |
| Paired measurements | Before vs. after in same patients | **Paired t-test** |

### A Clinical Decision Guide

**"Should I use a t-test or Mann-Whitney?"**

The t-test assumes your data is approximately Normally distributed. In practice, this matters most for small samples. With large samples (n > 30-50), the Central Limit Theorem (Chapter 5) means the means will be approximately normal even if the raw data is not.

- **Use t-test** when: sample size is reasonably large, or you have verified normality with a histogram or QQ plot
- **Use Mann-Whitney** when: sample is small AND data is obviously skewed (e.g., recovery room stay, which is always positive and often has a few very long stays)

---

## 6.3 The T-Test: Comparing Two Means

### When to Use It

The **independent samples t-test** compares the average of a continuous variable between two independent groups.

**Clinical example:** Does the mean propofol induction dose differ between patients with and without hypertension?

- Group 1 (HTN): propofol doses = [150, 180, 160, 170, 155, ...]
- Group 2 (no HTN): propofol doses = [140, 150, 145, 155, 135, ...]

### The Test Statistic

The t-statistic measures how far apart the group means are, relative to the variation within each group:

$$
t = \frac{\bar{x}_1 - \bar{x}_2}{\text{Standard Error of the difference}}
$$

- Large t → large difference between groups relative to noise → suggests real difference
- Small t → small difference relative to noise → could be chance

### An Intuition for the Formula

Think of the numerator as the *signal* (how different are the groups?) and the denominator as the *noise* (how variable is the data within each group?).

A t-statistic of 2.0 means the signal is twice as large as the noise. That is a reasonably strong difference. A t-statistic of 0.5 means the signal is smaller than the noise — not convincing.

### Worked Example

Suppose we want to compare BIS values at emergence between groups who received dexmedetomidine vs. control:

- Dex group: mean BIS = 72, SD = 8, n = 30
- Control: mean BIS = 65, SD = 9, n = 30

The difference in means is 7. The standard error of the difference is about 2.2. So t = 7 / 2.2 = 3.18.

With 58 degrees of freedom, this gives p = 0.002. Statistically significant.

But — and this is the important part — the p-value tells you the difference is unlikely to be zero. It does not tell you whether a difference of 7 BIS points *matters clinically*. You would still need to decide: is a 7-point higher BIS at emergence clinically meaningful?

---

## 6.4 Mann-Whitney: When Data Is Not Normal

### The Problem with Non-Normal Data

The t-test is robust — it handles some deviation from normality, especially with large samples. But sometimes your data is clearly not Normal:

- **Recovery room stay:** Most patients stay 30-60 minutes, but a few stay hours. Right-skewed distribution.
- **Troponin values:** Mostly undetectable, but occasionally very high. Many zeros.
- **Infusion durations:** Always positive, often with long tail.

For these, the mean is not a good summary — a few long stays can inflate the mean without representing most patients.

### The Solution: Compare Medians Instead

The **Mann-Whitney test** (also called the Wilcoxon rank-sum test) compares whether one group tends to have higher values than another, without assuming normality.

Instead of comparing means, it ranks all the values from both groups together and asks: *do the ranks differ between groups?*

### Intuition

Imagine you line up all 60 patients from both groups in order of their BIS at emergence. The dex patients are, on average, ranked higher (have higher BIS) than the control patients? If the groups were truly the same, you would expect the ranks to be roughly evenly mixed.

Mann-Whitney p = 0.003 means: if the groups were truly the same, there is only a 0.3% chance of seeing ranks this separated by chance.

### When to Use Mann-Whitney

- Sample size < 30 per group AND data looks skewed on a histogram
- You naturally report medians (not means) for your variable
- Your data has outliers that you cannot remove
- Ordinal data (e.g., ASA class as 1, 2, 3, 4)

---

## 6.5 Chi-Squared: Comparing Proportions

### When to Use It

The **chi-squared test** compares counts or proportions between groups. This is what you use when both your outcome and your grouping variable are categorical.

**Clinical examples:**
- Does the proportion of hypotension differ between two fluid protocols? (Our opening example)
- Is there an association between BMI category anddifficult ventilation?
- Does the distribution of ASA class differ between surgical specialties?

### The Test Statistic

For a 2x2 table (two groups, two outcomes), the chi-squared statistic is:

$$
\chi^2 = \sum \frac{(O - E)^2}{E}
$$

where O = observed count and E = expected count (what you would expect if the groups were truly the same).

### Worked Example

Returning to our hypotension example:

| | Hypotension | No hypotension | Total |
|---|---|---|---|
| Old protocol | 10 | 90 | 100 |
| New protocol | 2 | 38 | 40 |
| **Total** | 12 | 128 | 140 |

The expected count under H₀ (no difference) would be:
- Old protocol, hypotension: 12 × 100/140 = 8.6
- New protocol, hypotension: 12 × 40/140 = 3.4

Chi-squared = (10-8.6)²/8.6 + (2-3.4)²/3.4 + (90-91.4)²/91.4 + (38-36.6)²/36.6 = 0.23 + 0.58 + 0.02 + 0.05 = 0.88

With 1 degree of freedom, p = 0.35. Not significant.

---

## 6.6 ANOVA: Comparing Three or More Groups

### Extending the T-Test

The t-test compares two groups. What if you have three or more?

A surgeon asks: "Does mean arterial pressure at incision differ between our three most common surgeries — orthopaedic, abdominal, and neurosurgical?" You have 150 patients across three groups.

You could run three t-tests, but this inflates the false-positive rate. **ANOVA** (Analysis of Variance) tests all groups simultaneously.

### How ANOVA Works

ANOVA compares two sources of variance:
1. **Between-group variance:** How far apart are the group means?
2. **Within-group variance:** How much do individuals within each group vary?

If between-group variance is large relative to within-group variance, the groups are likely different.

### The F-Statistic

$$
F = \frac{\text{Between-group variance}}{\text{Within-group variance}}
$$

Large F → groups are different. Small F → any differences are likely noise.

### Important Caveat: Significant ANOVA Does Not Tell You Which Groups Differ

ANOVA tells you "at least one group is different." It does not tell you which one(s). You need **post-hoc tests** to compare pairs of groups, with a correction for multiple comparisons (e.g., Tukey's HSD).

---

## 6.7 The Epidemic of P-Value Misinterpretation

This section is the most important one in this chapter. The p-value is the most commonly misused statistic in medicine.

### What P-Values Do NOT Mean

| Misinterpretation | Correct interpretation |
|---|---|
| "p < 0.05 means the result is important" | p < 0.05 means the result is unlikely under the null hypothesis. It says nothing about clinical importance. |
| "p > 0.05 means there is no difference" | p > 0.05 means "we cannot detect a difference with this sample size." It could still be there — just too small to see. |
| "p = 0.001 is more significant than p = 0.04" | Technically true, but both are "significant." The numeric p-value does not tell you the effect is twice as big. |
| "The treatment works because p < 0.05" | The treatment may work, but the p-value does not prove it — it only says the data would be unlikely if it did not work. |

### The Sample Size Problem

Here is the uncomfortable truth: with enough patients, almost any small difference becomes "statistically significant."

Imagine a drug that reduces mortality from 10.0% to 9.5% — a tiny 0.5% absolute reduction. With 10,000 patients per group, this difference becomes significant (p = 0.04), even though clinically the effect is negligible.

:::{important} Statistical significance is not the same as clinical significance

Always ask: "what is the actual difference, and does it matter?" A p-value of 0.001 with a tiny effect may be less clinically meaningful than a p-value of 0.04 with a large effect.
:::

### The File Drawer Problem

Studies with "p < 0.05" get published. Studies with p = 0.06 get filed away as "not significant." This creates a publication bias — the literature appears more definitive than it is.

If 20 researchers test 20 useless drugs, on average one will get p < 0.05 by chance alone. If only that one gets published, the literature suggests "this drug works."

---

## 6.8 Confidence Intervals: Saying What You Do Not Know

We covered confidence intervals in detail in Chapter 7, but they are especially important in the context of hypothesis testing.

Instead of just asking "is p < 0.05?", report the **95% confidence interval** for your difference.

Returning to our hypotension example:

- Observed difference: 10% - 5% = 5% absolute reduction
- 95% CI: -2% to 12%

The CI includes zero. That is the same conclusion as p > 0.05 — we cannot be confident the reduction is real.

But the CI also tells you the range of plausible true effects: the reduction could be as large as 12% (impressive) or the new protocol could actually be worse (2% more hypotension). You cannot rule out either possibility.

---

## 6.9 A Practical Workflow

### Before You Test

1. **Define your research question clearly.** "Does the new fluid protocol reduce hypotension?" is clear. "Does anything differ?" is not.
2. **Choose your test based on the data.** Continuous vs. categorical, normal vs. non-normal, two groups vs. many.
3. **Set your significance level.** Conventionally α = 0.05, but consider the consequences of false positives vs. false negatives in your clinical context.

###After You Test

1. **Report the p-value precisely.** Not just "p < 0.05" — report "p = 0.14" or "p = 0.003."
2. **Report the effect size and confidence interval.** The difference, not just whether it is significant.
3. **Interpret clinically.** "With 95% CI of [-2%, 12%], the protocol could reduce hypotension by up to 12% or increase it by 2%. More data is needed before changing practice."

### Red Flags

- Someone says "the result is significant" without showing you the numbers
- The p-value is reported without an effect size or confidence interval
- Multiple comparisons are made without correction
- The sample size is very small and the p-value is exactly 0.05

---

## 6.10 Summary

| Test | Use when | Compares |
|---|---|---|
| **t-test** | Continuous data, 2 groups, normal | Means |
| **Mann-Whitney** | Continuous data, 2 groups, non-normal | Medians / ranks |
| **Chi-squared** | Categorical data | Proportions |
| **ANOVA** | Continuous data, 3+ groups | Means across groups |

Key takeaways:

- **The p-value** tells you how surprising your data would be if the null hypothesis were true
- **Statistical significance ≠ clinical importance.** Always report effect sizes.
- **Confidence intervals** are more informative than p-values alone
- **Choose your test** based on the nature of your data, not tradition
- **Beware of** interpreting p > 0.05 as "no difference"

---

## 6.11 Coming Next

In Chapter 7, we go deeper into **confidence intervals** — what they really mean, why they are more useful than p-values alone, and how to use them to make clinical decisions.

---

## Further Reading

- Altman, D.G. *Practical Statistics for Medical Research*. London: Chapman & Hall, 1991. [Chapters 4–6]
- Wasserstein, R.L. & Lazar, N.A. "The ASA Statement on P-Values." *The American Statistician* 70, no. 4 (2016): 200–201.
- Ioannidis, J.P.A. "Why Most Published Research Findings Are False." *PLoS Medicine* 2, no. 8 (2005): e124.