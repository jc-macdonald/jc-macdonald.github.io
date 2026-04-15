---
layout: page
title: trade-study
description: Design and evaluation framework for scientific simulation studies. Score competing configurations — model formulations, solver choices, measurement strategies, or any design decision — against known ground truth via protocol-driven simulators, proper scoring rules, hierarchical phases, multi-objective Pareto optimization, and Bayesian model stacking.
img: assets/img/research/structural_fidelity_comparison.png
importance: 2
category: "lead developer · released on PyPI"
github: https://github.com/jcm-sci/trade-study
---

**trade-study** is a design and evaluation framework for scientific simulation studies. Users define **simulators** — protocol-conformant objects that generate `(truth, observations)` pairs from a configuration — then score competing configurations (model formulations, solver choices, measurement strategies, or any design decision) against known ground truth, so that decisions validated on synthetic benchmarks transfer reliably to real observational data.

Evaluation proceeds through **hierarchical phases** — from broad experimental design (full factorial, Latin hypercube, or Bayesian-adaptive search) to focused refinement — scored with proper scoring rules (CRPS, WIS, Brier, coverage).

A **four-tier observable hierarchy** (embedded constraints, penalized objectives, diagnostic metrics, cost axes) structures multi-objective **Pareto optimization** with hypervolume and IGD+ front-quality metrics. Calibrated ensemble predictions are produced via **Bayesian or score-based model stacking**. Global **sensitivity analysis** (Morris screening) identifies which factors matter most.

Available in Python and Julia. Released on [PyPI](https://pypi.org/project/trade-study/). Documentation at [jcm-sci.github.io/trade-study](https://jcm-sci.github.io/trade-study/).

- Python: [jcm-sci/trade-study](https://github.com/jcm-sci/trade-study)
- Julia: [jcm-sci/TradeStudy.jl](https://github.com/jcm-sci/TradeStudy.jl)

{% include figure.liquid loading="eager" path="assets/img/research/optimal_design.png" class="img-fluid rounded z-depth-1" zoomable=true %}
