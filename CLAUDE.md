# Petrichor

## Mission

Investigate the dose-response relationship between nature exposure and mental
health outcomes, with focus on identifying minimum effective doses, optimal
exposure types, and biological mechanisms across diverse populations.

## Background

Nature therapy (ecotherapy, forest bathing / shinrin-yoku, green prescriptions)
is a growing field with strong preliminary evidence but fragmented methodology.
Key open questions include: How much nature is enough? Which environments work
best? What are the biological pathways? Who benefits most?

This lab conducts **computational research**: systematic reviews, meta-analyses,
statistical modeling of existing datasets, and experimental design for future
studies. We do not run clinical trials directly — we synthesize, analyze, and
generate testable hypotheses.

## How This Lab Works

This is a decentralized science lab. You are one of potentially many AI agents
contributing. There is no central coordinator.

### Your workflow:

1. **Read `knowledge/`** to understand the current state of research
2. **Read `experiments/`** to see what analyses have been done
3. **Read `feedback/`** for human domain expertise and priority guidance
4. **Read `changelog.yaml`** to understand recent methodology changes
5. **Read `knowledge/hypotheses.yaml`** to find open questions
6. **Pick ONE unit of work** using a workflow from `workflows/`
7. **Do the work on a branch** named `experiment/<NNN>-<short-description>`
8. **Open a PR** with your results

### Units of work (pick one per session):

| Action | Description |
|--------|-------------|
| **Literature extraction** | Extract structured data from a paper into `knowledge/` |
| **Meta-analysis** | Pool effect sizes across studies on a specific question |
| **Statistical model** | Build a dose-response or moderator model from pooled data |
| **Hypothesis generation** | Propose a new testable hypothesis from current findings |
| **Experimental design** | Design a study protocol to test an open hypothesis |
| **Review** | Review another agent's work for methodological rigor |
| **Synthesis** | Combine multiple findings into an updated knowledge summary |
| **Propose workflow** | Propose a new workflow to fill a methodological gap (human-gated) |
| **Propose tool** | Propose a new tool to fill a capability gap (human-gated) |

## Rules

- **NEVER duplicate existing work.** Check `experiments/` and open branches first.
- **ALWAYS use a workflow** from `workflows/`. Do not improvise methodology.
- **ALWAYS record your reasoning** in `analysis.md` within your experiment folder.
- **ALWAYS cite sources** with DOI or PMID when referencing published work.
- **If a hypothesis is refuted**, add it to `knowledge/dead_ends.yaml` with explanation.
- **If you find something new**, add it to `knowledge/hypotheses.yaml`.
- **One PR = one unit of work.** Keep it small and reviewable.
- **Be conservative in claims.** State effect sizes with confidence intervals.
  Distinguish correlation from causation. Flag potential confounders.
- **Report negative results.** They are as valuable as positive ones.

## Available Workflows

- `workflows/literature-extraction.yaml` — Extract structured data from a study
- `workflows/meta-analysis.yaml` — Pool effect sizes across studies
- `workflows/dose-response-model.yaml` — Model dose-response relationships
- `workflows/moderator-analysis.yaml` — Test moderating variables
- `workflows/study-design.yaml` — Design a new study protocol
- `workflows/narrative-synthesis.yaml` — Synthesize qualitative findings

## Tools

- `tools/effect_size.py` — Calculate Cohen's d, Hedges' g, odds ratios from raw stats
- `tools/meta_pool.py` — Random-effects meta-analysis (DerSimonian-Laird)
- `tools/forest_plot.py` — Generate forest plots from pooled data
- `tools/funnel_plot.py` — Generate funnel plots for publication bias assessment
- `tools/dose_response.py` — Fit dose-response curves (linear, log, spline)
- `tools/quality_score.py` — Score study quality (adapted Cochrane RoB 2)
- `tools/prisma_flow.py` — Generate PRISMA flow diagrams

## Lab Evolution

This lab evolves over time. Agents can propose improvements to methodology.

### What you can change directly (agent peer review)
- Add experiments, findings, hypotheses, dead ends, reviews
- Update `knowledge/` with new evidence

### What requires HUMAN approval
- New or modified workflows in `workflows/`
- New or modified tools in `tools/`
- Changes to this file (`CLAUDE.md`)
- Changes to `lab.yaml`

### Proposing a new workflow
1. Open a PR adding a file to `workflows/`
2. In the PR description, explain:
   - **Why** existing workflows are insufficient
   - **Based on** which existing workflow (if any)
   - **Evidence** — which experiments or findings revealed the gap
3. Tag the PR with `methodology-change`
4. This PR requires HUMAN approval — do not expect agent merge

### Proposing a new tool
1. Open a PR adding a file to `tools/`
2. Include usage examples and expected output in the PR description
3. Keep dependencies to: Python stdlib, numpy, matplotlib, scipy, pyyaml
4. Include at least one test case demonstrating correctness
5. Tag the PR with `methodology-change`
6. This PR requires HUMAN approval

### Proposing a rule change
1. Open a PR modifying `CLAUDE.md` or `lab.yaml`
2. Explain the problem with the current rule
3. Show evidence from experiments that motivated the change
4. Tag the PR with `methodology-change`
5. This PR requires HUMAN approval

### Changelog
Read `changelog.yaml` to understand the history of methodology changes
and why the lab works the way it does.

## Human Feedback

Check `feedback/` during your OBSERVE step, alongside `knowledge/`.
Humans leave domain expertise, priority guidance, and methodological
concerns as YAML files. Treat human feedback as high-priority input —
if a human flags a confounder or methodological issue, address it
before proceeding with related work.

## Key Measurement Conventions

### Exposure measures (nature dose)
- **Duration**: minutes per session
- **Frequency**: sessions per week
- **Total dose**: minutes per week
- **Environment type**: forest | park | garden | waterfront | wilderness | mixed
- **Activity**: walking | sitting | gardening | exercising | mixed

### Outcome measures
- **Primary mental health**: PHQ-9 (depression), GAD-7 (anxiety), PSS (stress)
- **Biomarkers**: cortisol (salivary), heart rate variability (RMSSD), blood pressure
- **Cognitive**: attention (ANT), working memory (n-back), rumination (RRS)
- **Wellbeing**: WEMWBS, WHO-5, subjective vitality scale

### Effect size standard
- Report **Hedges' g** for continuous outcomes (small=0.2, medium=0.5, large=0.8)
- Report **odds ratios** for binary outcomes
- Always include **95% confidence intervals**
- Always report **I² heterogeneity** for pooled analyses

## Domain Knowledge References

Key foundational papers the lab builds on:
- Bratman et al. (2019) "Nature and mental health" — *Science Advances* — DOI:10.1126/sciadv.aax0903
- Jimenez et al. (2021) "Associations between nature exposure and health" — *Int J Environ Res Public Health*
- White et al. (2019) "120 minutes of nature per week" — *Scientific Reports* — DOI:10.1038/s41598-019-44097-3
- Li (2010) "Effect of forest bathing on immune function" — *Environ Health Prev Med*
- Kaplan (1995) "Attention Restoration Theory" — *J Environ Psychol*
- Ulrich et al. (1991) "Stress Recovery Theory" — *J Environ Psychol*
