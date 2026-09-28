# Experiment math, just enough

These are standard frequentist approximations for two-arm tests. For anything unusual, such as many arms, ratio metrics, heavy tails, or a sequential design, use your experimentation platform's calculator or ask a statistician, and cite which one you used.

## Sample size for a conversion-rate metric

Two arms of equal size, two-sided test, α = 0.05, power = 0.8:

```
n per arm ≈ 16 · p · (1 − p) / δ²
```

`p` is the baseline rate and `δ` is the absolute minimum detectable effect.

Example: baseline 20% (p = 0.2), and you want to detect +2 points (δ = 0.02):
n ≈ 16 · 0.2 · 0.8 / 0.0004 = 6,400 per arm.

Duration = total sample ÷ eligible traffic per day. Round up to whole weeks.

If the duration comes out longer than the decision can wait, you have four options: accept a larger MDE, use a more sensitive metric, apply variance reduction (e.g. CUPED with pre-period data), or skip the experiment and decide by judgment. Do not run an underpowered test and read its noise.

## Continuous metrics

```
n per arm ≈ 16 · σ² / δ²
```

`σ` is the standard deviation of the metric per unit. Revenue and time metrics are heavy-tailed, so cap or winsorize them first, and state that you did.

## Sample ratio mismatch (SRM)

For a planned 50/50 split with totals A and B, run a chi-square test of A and B against (A+B)/2 each. p < 0.001 means the split is broken. Typical causes are bots, redirects that drop one arm, caching, or assignment after an eligibility filter. Stop and fix the assignment or logging. Do not interpret the results.

Quick check: with 100,000 users, 50,500 vs 49,500 is fine (p ≈ 0.002, borderline). 51,000 vs 49,000 is not (p ≈ 1e-10).

## Reading results

- Report the difference and its 95% confidence interval: "+1.8 pts (95% CI +0.4 to +3.2)".
- If the interval includes zero and also includes the MDE, the test was inconclusive, not negative.
- If the interval excludes the MDE on the upside, there is no worthwhile effect. "No effect" is a result.
- Correct for multiple comparisons when you read several primary metrics, or name one in advance.

## Peeking

Checking a fixed-horizon test daily and stopping at the first p < 0.05 raises the false-positive rate well above 5%. Either commit to the duration up front, or use a method built for continuous monitoring (sequential testing or always-valid p-values) as your platform documents it.
