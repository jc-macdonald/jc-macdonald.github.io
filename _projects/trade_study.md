---
layout: page
title: trade-study
description: Compare experiments and model choices, weighing uncertainty, information and cost.
img: assets/img/research/previews/replicated_tradeoff.svg
img_alt: Ten synthetic designs compared on mean squared error and assumed measurement cost. Nondominated designs are outlined.
importance: 3
category: "Released software"
github: https://github.com/jcm-sci/trade-study
---

**trade-study** helps researchers compare experiments, model settings and data-collection plans using repeated simulations. It coordinates design and evaluation studies across scientific domains. Users supply a simulator and scorer, define factors and objectives, and compare configurations such as model formulations, solver controls or measurement strategies.

[Public alpha release on PyPI](https://pypi.org/project/trade-study/), with [documentation and executable examples](https://jcm-sci.github.io/trade-study/guide/capabilities/) and a [Zenodo archive](https://doi.org/10.5281/zenodo.19599838).

Current capabilities include:

- Factorial and sampled design grids, constraints, hierarchical phases and optional parallel execution.
- Replicated trials, shared-random-number comparisons, and fixed or adaptive replication with recorded counts and assumptions.
- Optional proper scoring rules and sensitivity analysis, Pareto fronts, preference sweeps, regret and practical-equivalence reports.
- Adaptive optimization, successive halving/Hyperband and Gaussian-process or random-forest surrogates with validation diagnostics.
- Evaluation caches, resumable grids and result bundles with guarded provenance.

The core depends on NumPy, with optional integrations for scoring, optimization, sensitivity, model weighting and plots. Bayesian stacking uses log-likelihood information supplied by predictive models. Score-based weighting optimizes a weighted combination of supplied mean model scores. Assessing the resulting combined predictions requires a separate evaluation, including checks of calibration where relevant.

A Pareto front contains alternatives for which none of the other candidates is at least as good on every stated objective and better on at least one. Choosing among them needs stated preferences or constraints. Uncertainty intervals depend on the replicate design and assumptions. A precision target for a pass-rate estimate does not establish the probability of detecting an inadequate method. Application studies must assess whether synthetic benchmark findings carry over to observed data.

{% include figure.liquid path="assets/img/research/computed/replicated_tradeoff.svg" class="img-fluid rounded" zoomable=true alt="Ten synthetic sample-mean designs compared across 512 paired replicates. Nondominated mean error and assumed cost are marked, and empirical errors are compared with analytic variances. Costs are declared assumptions, not measured field costs." caption="Ten synthetic measurement designs, each evaluated on 512 paired replicates. Cost is an assumed input, not a measured field cost." %}

[Computed example, inputs and checks](/software-examples/#replicated-designs)

{% include figure.liquid loading="eager" path="assets/img/research/optimal_design.svg" class="img-fluid rounded z-depth-1" zoomable=true alt="Synthetic candidate costs and utilities illustrate Pareto efficiency and selection under a declared budget. These values are illustrative inputs, not a fitted study or empirical information estimates." caption="Constructed costs and utilities. C is dominated. D maximizes utility under the declared cost limit of 4." %}

{% include figure.liquid path="assets/img/research/trade_study_slide.svg" class="img-fluid rounded" zoomable=true alt="Candidate designs feed replicated simulator/scorer evaluations and trial results. Results branch into comparisons and optional analyses, with a dashed return for adaptive search or phase refinement. Calibration and transfer require separate application evidence." caption="Replicated design and evaluation with trade-study." %}

[Vector PDF](/assets/img/research/trade_study_slide.pdf) · [All figure sources and downloads](/figures/)
