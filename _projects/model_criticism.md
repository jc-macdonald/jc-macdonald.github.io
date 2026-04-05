---
layout: page
title: model-criticism
description: Observable-based model evaluation with Pareto optimization, proper scoring rules, and Bayesian stacking for simulation studies.
img: assets/img/research/structural_fidelity_comparison.png
importance: 2
category: "lead developer · in development"
github: https://github.com/jcm-sci/model-criticism
---

**model-criticism** is a Python framework for structured model evaluation in simulation studies. It connects model worlds, observables, and scoring rules into reproducible criticism pipelines with multi-objective optimization and Bayesian model combination.

Core capabilities:

- Protocol-driven architecture (ModelWorld, Scorer, Observable)
- Proper scoring rules (CRPS, energy, WIS, Brier) via scoringrules
- Experimental design (full factorial, Latin hypercube, Morris screening)
- Pareto front extraction and hypervolume indicators
- Bayesian stacking of predictive distributions
- Adaptive multi-objective optimization via optuna

In development; pre-release. Source at [jcm-sci/model-criticism](https://github.com/jcm-sci/model-criticism).

{% include figure.liquid loading="eager" path="assets/img/research/optimal_design.png" class="img-fluid rounded z-depth-1" zoomable=true %}
