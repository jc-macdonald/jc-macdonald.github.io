---
layout: page
title: trade-study
description: Compare replicated studies, competing objectives and decision preferences, with uncertainty and provenance.
img: assets/img/research/trade_study_slide.svg
img_alt: Candidate designs feed replicated simulator/scorer evaluations and trial results. Results branch into comparisons and optional analyses, with a dashed return for adaptive search or phase refinement. Calibration and transfer require separate application evidence.
importance: 2
category: "lead developer · released"
github: https://github.com/jcm-sci/trade-study
---

**trade-study** coordinates design and evaluation studies across scientific domains. Users supply a simulator and scorer, define factors and objectives, and compare configurations such as model formulations, solver controls or measurement strategies.

[Released on PyPI](https://pypi.org/project/trade-study/), with [documentation and executable examples](https://jcm-sci.github.io/trade-study/guide/capabilities/) and a [Zenodo archive](https://doi.org/10.5281/zenodo.19599838).

Current capabilities include:

- Factorial and sampled design grids, constraints, hierarchical phases and optional parallel execution.
- Replicated trials, shared-random-number comparisons, and fixed or adaptive replication with recorded counts and assumptions.
- Optional proper scoring rules and sensitivity analysis, Pareto fronts, preference sweeps, regret and practical-equivalence reports.
- Adaptive optimization, successive halving/Hyperband and Gaussian-process or random-forest surrogates with validation diagnostics.
- Evaluation caches, resumable grids and result bundles with guarded provenance.

The core depends on NumPy; optional integrations wrap established libraries for scoring, optimization, sensitivity, model weighting and plots. Bayesian stacking uses log-likelihood information supplied by predictive models. Score-based weights optimize the supplied mean model scores, not the loss of an averaged prediction. Neither approach certifies calibration.

A Pareto front narrows the alternatives; selecting a design still needs explicit preferences or constraints. Replicate intervals describe uncertainty under their stated assumptions. Fixed Wilson precision is not gate power, and synthetic benchmark results need independent validation before transfer to observed data.

{% include figure.liquid loading="eager" path="assets/img/research/optimal_design.svg" class="img-fluid rounded z-depth-1" zoomable=true alt="Synthetic candidate costs and utilities illustrate Pareto efficiency and selection under a declared budget. These values are illustrative inputs, not a fitted study or empirical information estimates." caption="Constructed costs and utilities. C is dominated. D maximizes utility under the declared cost limit of 4." %}

{% include figure.liquid path="assets/img/research/trade_study_slide.svg" class="img-fluid rounded" zoomable=true alt="Candidate designs feed replicated simulator/scorer evaluations and trial results. Results branch into comparisons and optional analyses, with a dashed return for adaptive search or phase refinement. Calibration and transfer require separate application evidence." caption="Replicated design and evaluation with trade-study." %}

[Vector PDF](/assets/img/research/trade_study_slide.pdf) · [All figure sources and downloads](/figures/)
