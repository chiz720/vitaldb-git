# Chapter 8 — Linear Regression

> *"All models are wrong, but some are useful."*
> — George Box

---

In Part II, you learned how to compare two groups — is the mean different between patients who got drug A vs. drug B? Is the proportion of hypotension different between protocols? These are important questions, but they have a fundamental limitation: they can only compare two groups at a time.

What if you want to understand not just *whether* variables are related, but *how* they are related? What if you want to predict an outcome from several predictors at once?

That is what **regression** does. This chapter covers **linear regression** — the workhorse method for understanding relationships between continuous variables and for prediction.

### What you will learn in this chapter

By the end, you will be able to:

- **Interpret regression coefficients** — what a slope of 0.5 actually means
- **Build a multiple regression model** — use several predictors together
- **Assess model fit** — understand R-squared and what it tells you
- **Check assumptions** — know when a linear model is appropriate
- **Use regression for prediction** — generate new predictions from your model

We start with the simplest case: one predictor, one outcome.

---

## 8.1 The Core Idea: Drawing the Line

### When to Use Linear Regression

Linear regression is the right tool when:

1. **Your outcome is continuous** — a number on a scale, not categories
2. **You want to understand relationships** — not just "is there a difference?" but "how does Y change when X changes?"
3. **You want to predict** — use known values to estimate unknown outcomes

**Clinical examples:**
- Predicting MAP from cardiac output and systemic vascular resistance
- Predicting tidal volume from driving pressure
- Estimating blood loss from surgical duration and patient weight

### The Basic Picture

Imagine you want to understand the relationship between **body weight** and **propofol induction dose**. You collect data from 50 patients:

| Weight (kg) | Propofol dose (mg) |
|---|---|
| 60 | 120 |
| 70 | 140 |
| 80 | 160 |
| ... | ... |

If you plot weight on the x-axis and dose on the y-axis, you suspect there is a linear relationship: heavier patients get more propofol. But exactly how much more?

Linear regression finds the **best-fit line** through your data:

$$
\text{Dose} = \beta_0 + \beta_1 \times \text{Weight} + \varepsilon
$$

Where:
- $\beta_0$ is the intercept — the dose when weight = 0 (not clinically meaningful, but part of the line)
- $\beta_1$ is the slope — how much dose increases for each 1 kg increase in weight
- $\varepsilon$ is the residual — the difference between the actual dose and what the line predicts

---

## 8.2 Simple Linear Regression: One Predictor

### The Formula

For simple linear regression (one predictor):

$$
Y = \beta_0 + \beta_1 X + \varepsilon
$$

- $Y$ is the outcome (dependent variable)
- $X$ is the predictor (independent variable)
- $\beta_0$ is the intercept
- $\beta_1$ is the slope (the coefficient)
- $\varepsilon$ is the error term

### Finding the Best Line

The regression line is chosen to **minimize the sum of squared errors** — the vertical distance between each data point and the line, squared and summed. This is why it is called **ordinary least squares (OLS)**.

The line that minimizes squared errors also turns out to be the line where:
- The slope equals: $\beta_1 = r \times \frac{SD_Y}{SD_X}$
- The intercept centers the line through the means: $\beta_0 = \bar{Y} - \beta_1 \bar{X}$

### A Worked Example

Using our VitalDB data, let us look at the relationship between **weight** and **propofol induction dose**:

- Mean weight: 64 kg
- Mean propofol dose: 128 mg
- SD of weight: 10 kg
- SD of propofol: 20 mg
- Correlation (r): 0.95

The slope:

$$
\beta_1 = 0.95 \times \frac{20}{10} = 1.9
$$

Interpretation: for every 1 kg increase in weight, propofol dose increases by 1.9 mg.

The intercept:

$$
\beta_0 = 128 - 1.9 \times 64 = 128 - 121.6 = 6.4
$$

The regression equation:

$$
\text{Propofol dose} = 6.4 + 1.9 \times \text{Weight}
$$

### Checking the Interpretation

For a 70 kg patient:
$$Predicted~dose = 6.4 + 1.9 \times 70 = 6.4 + 133 = 139.4~mg$$

For a 60 kg patient:
$$Predicted~dose = 6.4 + 1.9 \times 60 = 6.4 + 114 = 120.4~mg$$

Difference of 10 kg → difference of 19 mg. That matches: 1.9 mg/kg × 10 kg = 19 mg.

---

## 8.3 Interpreting the Slope: What Does "Per Unit" Mean?

### The Slope Is a Rate of Change

The coefficient $\beta_1$ tells you how much the outcome changes for a **one-unit increase** in the predictor.

But "one unit" depends on how the variable is measured:

| Predictor | Unit | Slope interpretation |
|---|---|---|
| Weight | 1 kg | Propofol dose increases by $\beta_1$ mg |
| Age | 1 year | Blood pressure increases by $\beta_1$ mmHg |
| Duration | 10 minutes | Blood loss increases by $10 \times \beta_1$ mL |

### The Problem of Scale

A slope of 0.03 mmHg/year for age×MAP sounds tiny. But that is 0.03 × 10 = 0.3 mmHg per decade — more meaningful.

Always ask: "what is a clinically relevant change in X?"

### Centering: Making Coefficients More Interpretable

Instead of using raw weight (40-120 kg), you can **center** the variable:

$$
\text{Weight centered} = \text{Weight} - 70~kg
$$

Now the intercept represents a 70 kg patient, not a theoretical 0 kg patient.

---

## 8.4 Multiple Linear Regression: More Than One Predictor

### The Real World Has Multiple Factors

The propofol dose depends on more than just weight. It also depends on:

- Age
- Sex
- Height (or ideal body weight)
- ASA class
- Surgical severity

Simple regression with one predictor ignores all of these. **Multiple regression** includes them all in one model:

$$
Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \beta_3 X_3 + \ldots + \varepsilon
$$

### A Clinical Example

Using VitalDB data, we model **propofol induction dose** from multiple predictors:

| Predictor | Coefficient | Interpretation |
|---|---|---|
| (Intercept) | 5.2 | Baseline dose (mg) |
| Weight (per 1 kg) | 1.8 | Each kg adds 1.8 mg |
| Age (per 10 years) | -12.3 | Each decade reduces dose by 12.3 mg |
| Female (vs. male) | -18.5 | Women need 18.5 mg less |
| ASA III (vs. I) | -22.1 | ASA III needs 22.1 mg less |

### Interpreting Each Coefficient

The coefficient for each predictor is **adjusted for all other predictors** in the model.

The coefficient for weight (1.8 mg/kg) is the effect of weight *after accounting for* age, sex, and ASA class. It is not confounded by those other variables.

### The Interpretation Trap

:::{important} Each coefficient tells you the effect of that predictor, holding other variables constant

In the model above, the coefficient for weight (1.8) is the effect of weight for patients of the same age, sex, and ASA class. It is the weight effect "at fixed values" of other variables.
:::

This is powerful but tricky. If you are comparing a 50-year-old man to a 70-year-old woman, you cannot simply add up the coefficients — the effects are estimated at fixed values of the other predictors.

---

## 8.5 R-Squared: How Well Does the Model Fit?

### What R² Means

**R-squared (R²)** is the proportion of variation in the outcome explained by the model.

$$
R^2 = \frac{SS_{model}}{SS_{total}} = \frac{\text{Variance explained}}{\text{Total variance}}
$$

- R² = 0.00: The model explains nothing — predicts the mean for everyone
- R² = 0.50: The model explains half the variation
- R² = 0.90: The model explains almost all variation

In our propofol example, if R² = 0.82, then 82% of the variation in propofol dose is explained by weight, age, sex, and ASA class. The remaining 18% is individual variation we cannot explain.

### R² in Simple vs. Multiple Regression

In simple regression with one predictor, R² = r² (the squared correlation).

Adding more predictors always increases R² — even if the new predictors are meaningless. This is why **adjusted R²** penalizes for the number of predictors:

$$
R^2_{adj} = 1 - \frac{(1-R^2)(n-1)}{n-k-1}
$$

where n = sample size and k = number of predictors.

### What Is a Good R²?

It depends on the context:

| Domain | Typical R² |
|---|---|
| Physical measurements (weight → dose) | 0.7-0.9 |
| Clinical outcomes | 0.1-0.4 |
| Social/behavioral outcomes | 0.05-0.2 |

Human biology is noisy. R² of 0.3 for a clinical prediction model is often good.

:::{important} Do not chase R²

A model with R² = 0.35 is not "worse" than one with R² = 0.40 for clinical use. The question is: does the model predict well enough to be useful? Does it improve on clinical judgment?
:::

---

## 8.6 The Regression Assumptions

Linear regression is valid when four assumptions are met:

### 1. Linearity

The relationship between each predictor and the outcome is linear.

**How to check:** Plot residuals vs. fitted values. No pattern = good. Curved pattern = problem.

If non-linear, consider:
- Transformations (log, square root)
- Polynomial terms (X²)
- Splines

### 2. Independence

Each observation is independent of others.

**Clinical concern:** Repeated measurements on the same patient are not independent. Time series data is not independent.

Use **mixed models** or **generalized estimating equations** for correlated data.

### 3. Homoscedasticity

The variability of residuals is constant across all fitted values.

**How to check:** Plot residuals vs. fitted values. Funnel shape = problem (heteroscedasticity).

If heteroscedastic, use:
- Weighted least squares
- Robust standard errors
- Bootstrap confidence intervals

### 4. Normality of Residuals

The residuals are approximately Normally distributed.

**How to check:** Histogram or Q-Q plot of residuals.

With large samples (n > 50-100), this matters less due to the Central Limit Theorem.

---

## 8.7 Checking Assumptions Visually

### The Four-Panel Diagnostic Plot

After fitting a regression model, always check this plot:

| Panel | What to check |
|---|---|
| 1. Residuals vs. Fitted | No pattern = linearity OK; curved = non-linear |
| 2. Q-Q Plot | Points on line = normality OK; s-shaped = non-normal |
| 3. Scale-Location | Horizontal line = homoscedasticity OK; funnel = heteroscedastic |
| 4. Residuals vs. Leverage | Points with high leverage and large residuals are influential |

### What to Look For

- **Curved pattern in Panel 1:** The relationship is not linear — consider transformation
- **S-shaped Q-Q in Panel 2:** Residuals are skewed — consider transformation or bootstrap
- **Funnel in Panel 3:** Heteroscedasticity — use robust standard errors
- **Points in top-right corner of Panel 4:** Influential outliers — check these cases individually

---

## 8.8 Categorical Predictors in Regression

### Dummy Variables

Linear regression requires numeric predictors. To include categorical variables, create **dummy variables** (also called indicator variables).

For **sex** (Male/Female):
- Create one dummy: Female = 1 if female, 0 if male
- Reference category: Male (coded 0)

The coefficient for Female tells you the difference between females and males (the reference).

### For More Than Two Categories

For **ASA class** (I, II, III, IV):
- Create three dummies: ASA_II, ASA_III, ASA_IV
- Reference category: ASA I (all = 0)

The coefficient for ASA_III is the difference between ASA III and ASA I patients.

### Interpretation Example

Model: $\text{Propofol} = 140 + 1.8 \times \text{Weight} - 18.5 \times \text{Female}$

- For a 70 kg male: $140 + 1.8\times70 = 266$ mg
- For a 70 kg female: $140 + 1.8\times70 - 18.5 = 247.5$ mg

Women need 18.5 mg less, after adjusting for weight.

---

## 8.9 Interaction Terms

### What Is an Interaction?

An **interaction** exists when the effect of one predictor depends on another predictor.

Example: The effect of weight on propofol dose might be different in men vs. women. Men might need more propofol per kg than women.

### How to Model It

Create the interaction term by multiplying the two predictors:

$$
\text{Dose} = \beta_0 + \beta_1 \times \text{Weight} + \beta_2 \times \text{Female} + \beta_3 \times (\text{Weight} \times \text{Female})
$$

The coefficient $\beta_3$ tells you how much the effect of weight differs between sexes.

### Interpretation

- $\beta_1$ = effect of weight in males (Female = 0)
- $\beta_1 + \beta_3$ = effect of weight in females (Female = 1)

If $\beta_3$ is significant, the relationship is different between groups.

### When to Include Interactions

- Clinically suspected moderation (e.g., drugs work differently in elderly)
- When the effect of one variable naturally depends on another
- When exploring heterogeneity

Be cautious — each interaction term uses one degree of freedom. With many predictors, interactions bloat the model.

---

## 8.10 Prediction vs. Explanation

### Two Goals, Two Approaches

Regression can serve two purposes:

| | Prediction | Explanation |
|---|---|---|
| **Goal** | Accurate prediction of new cases | Understand the relationships |
| **Focus** | Overall accuracy (R², MAE) | Individual coefficients |
| **Model** | May include non-linear terms | Keep it simple and interpretable |
| **Validation** | Cross-validation, test set | Check assumptions |

### For Prediction

Use the full model. Even if coefficients are hard to interpret, the predictions may be accurate.

Validate on new data. A model that fits your data perfectly may not generalize.

### For Explanation

Keep the model simple.Interpretable coefficients are more valuable than a black box.

Report confidence intervals for coefficients — the uncertainty in each effect.

---

## 8.11 A Practical Workflow

### Step 1: Define Your Question

Are you predicting an outcome, or understanding relationships?

### Step 2: Choose Your Outcome and Predictors

- Outcome: continuous
- Predictors: clinical variables you have access to

### Step 3: Check Your Data

- Missing values?
- Outliers?
- Appropriate scales?

### Step 4: Fit the Model

```python
from sklearn import linear_model
model = linear_model.LinearRegression()
model.fit(X, y)
```

### Step 5: Check Diagnostics

- Four-panel plots
- Assumption checks

### Step 6: Interpret

- Coefficients and CIs
- R² and adjusted R²

### Step 7: Validate (if prediction)

- Cross-validation
- Test set performance

---

## 8.12 Summary

| Concept | What it tells you |
|---|---|
| **Simple regression** | Relationship between one predictor and outcome |
| **Multiple regression** | Joint effects of multiple predictors |
| **Coefficient ($\beta$)** | Change in outcome per unit change in predictor |
| **R²** | Proportion of variance explained |
| **Adjusted R²** | R² penalized for number of predictors |
| **Dummy variable** | Coding categorical predictors as 0/1 |
| **Interaction** | Effect that depends on another variable |

Key takeaways:

- **Regression extends comparison** beyond two groups — continuous relationships
- **Each coefficient is adjusted** for all other predictors in the model
- **Check assumptions** — linearity, independence, homoscedasticity, normality
- **R² tells you overall fit** — but interpretability matters more than raw R²

---

## 8.13 Coming Next

In Chapter 9, we move from continuous outcomes to binary outcomes. **Logistic regression** handles yes/no decisions — hypotension or not, survival or death, ICU admission or discharge. The math is different, but the logic is the same.

---

## Further Reading

- Kutner, M.H. et al. *Applied Linear Statistical Models*. 5th ed. New York: McGraw-Hill, 2004. [Chapter 2-3]
- Weisberg, S. *Applied Linear Regression*. 3rd ed. Thousand Oaks: Sage, 2005.
- Harrell, F.E. *Regression Modeling Strategies*. 2nd ed. Cham: Springer, 2015. [Chapters 4-6]