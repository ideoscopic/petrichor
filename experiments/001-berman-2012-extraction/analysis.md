# Experiment 001: Literature Extraction — Berman et al. (2012)

## Study Reference

Berman MG, Kross E, Krpan KM, Askren MK, Burson A, Deldin PJ, Kaplan S,
Sherdell L, Gotlib IH, Jonides J (2012). Interacting with nature improves
cognition and affect for individuals with depression. *Journal of Affective
Disorders*, 140(3), 300-305. DOI: 10.1016/j.jad.2012.03.012. PMID: 22464936.

## Why This Study

This is one of very few experimental studies examining nature exposure
specifically in a clinically depressed population (MDD). It is directly
relevant to:

- **H001** (minimum effective dose): Provides a single-session data point
  at 50 minutes showing cognitive benefit.
- **H004** (clinical vs healthy moderation): Extends Berman et al. (2008),
  which demonstrated similar cognitive effects in healthy adults, to a
  clinical MDD sample.

The lab's `knowledge/studies/` was empty — this extraction seeds the database
for future meta-analyses.

## Design Summary

Within-subjects crossover design. 20 adults with MDD completed both a nature
walk (arboretum) and an urban walk (downtown), one week apart, order
counterbalanced. Before each walk, participants completed a rumination
induction (thinking about a painful experience). Outcomes assessed pre- and
post-walk.

## Key Extracted Effect Sizes (Hedges' g)

| Outcome | g | 95% CI | p | Interpretation |
|---------|---:|--------|---|----------------|
| Backward Digit Span | 0.58 | [-0.06, 1.21] | <.001 | Medium; nature improved working memory |
| PANAS Positive Affect | 0.23 | [-0.39, 0.85] | <.05 | Small; nature boosted positive mood more |
| PANAS Negative Affect | -0.14 | [-0.76, 0.48] | n.s. | Negligible; both conditions reduced NA |
| Rumination | -0.09 | [-0.71, 0.53] | .72 | Negligible; no difference |

**Important methodological note:** These effect sizes were computed treating
the two conditions as independent groups (using `tools/effect_size.py`), which
is conservative for a crossover design. The within-subjects analyses reported
by the authors (partial eta-squared = 0.53 for BDS, 0.29 for PA) reflect
the true precision of the crossover design and yield larger effects. The
Hedges' g values here are suitable for pooling with between-subjects studies
in future meta-analyses but will underestimate the study's internal precision.

## Quality Assessment

- **Overall risk of bias:** High (due to unblinded self-report outcomes)
- **Quality score:** 2.3/3.0
- **Key strengths:** Crossover design, clinical sample, validated measures
- **Key concerns:** Small N, no blinding, single session only

## Interpretation

1. **Cognitive effects are the strongest finding.** Working memory (BDS)
   showed a medium effect (g=0.58) favoring nature, consistent with Attention
   Restoration Theory (Kaplan, 1995). This extends Berman et al. (2008)'s
   finding in healthy adults to a clinical population.

2. **Affective effects are modest and selective.** Positive affect improved
   more after nature walks, but negative affect decreased equally in both
   conditions. This suggests nature's advantage in depression may be
   primarily cognitive (restored directed attention) rather than affective
   (direct mood improvement).

3. **A single 50-minute nature walk is sufficient to produce cognitive
   benefits in MDD.** This is a lower dose than the 120-minute weekly
   threshold from White et al. (2019), though the designs are not directly
   comparable (single session vs. habitual weekly exposure).

4. **The rumination induction is a double-edged feature.** It increases
   ecological validity (depressed individuals often ruminate), but limits
   comparability with studies that don't use mood induction.

## Implications for Lab Hypotheses

- **H001 (minimum dose):** Provides one data point — 50 min single session
  produced cognitive but not robust affective benefit. We need more studies
  at different doses to build a dose-response curve.
- **H004 (clinical moderation):** This study in MDD can be compared with
  Berman et al. (2008) in healthy adults for a preliminary moderator signal.
  Extracting that study next would enable a direct comparison.

## Recommended Next Steps

1. **Extract Berman et al. (2008)** — healthy population analog of this study,
   enabling direct clinical vs. healthy comparison for H004.
2. **Extract Bratman et al. (2015)** — another RCT with neuroimaging, already
   in findings (F003) but not formally extracted to `knowledge/studies/`.
3. **Extract dose-response relevant studies** — Shanahan et al. (2016),
   Barton & Pretty (2010), White et al. (2019) — to build toward a
   dose-response model for H001.
