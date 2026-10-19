---
layout: page
title: trade-study
description: Replicated simulation studies, paired comparisons, Pareto analysis and preference-based decisions, with explicit uncertainty and result provenance.
img: assets/img/research/trade_study_slide.png
img_alt: trade-study workflow from a constrained design space through simulator protocols and scoring to Pareto and surrogate decision support.
importance: 2
category: "lead developer · released"
github: https://github.com/jcm-sci/trade-study
---

**trade-study** coordinates design and evaluation studies across scientific domains. Users supply a simulator and scorer, define factors and objectives, and compare configurations such as model formulations, solver controls or measurement strategies.

**Status:** [Released on PyPI](https://pypi.org/project/trade-study/), with [documentation and executable examples](https://jcm-sci.github.io/trade-study/guide/capabilities/) and a [Zenodo archive](https://doi.org/10.5281/zenodo.19599838).

Current capabilities include:

- Factorial and sampled design grids, constraints, hierarchical phases and optional parallel execution.
- Replicated trials, shared-random-number comparisons, and fixed or adaptive replication with recorded counts and assumptions.
- Optional proper scoring rules and sensitivity analysis, Pareto fronts, preference sweeps, regret and practical-equivalence reports.
- Adaptive optimization, successive halving/Hyperband and validated GP/RF surrogates, including regime-specific recommendations.
- Evaluation caches, resumable grids and result bundles with guarded provenance.

The core depends on NumPy; optional integrations wrap established libraries for scoring, optimization, sensitivity, model weighting and plots. Bayesian stacking uses log-likelihood information supplied by predictive models. Score-based weights optimize the supplied mean model scores, not the loss of an averaged prediction. Neither approach certifies calibration.

A Pareto front narrows the alternatives; selecting a design still needs explicit preferences or constraints. Replicate intervals describe uncertainty under their stated assumptions. Fixed Wilson precision is not gate power, and synthetic benchmark results need independent validation before transfer to observed data.

{% include figure.liquid loading="eager" path="assets/img/research/optimal_design.png" class="img-fluid rounded z-depth-1" zoomable=true alt="Observation-design example comparing candidate sampling strategies on a Pareto frontier of total cost and expected information, with one design selected under a stated budget." caption="Illustrative observation-design application: Pareto efficiency narrows the choices, but selecting a design still requires an explicit budget or utility." %}
