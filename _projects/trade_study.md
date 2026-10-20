---
layout: page
title: trade-study
description: Compare experiments and model choices, weighing uncertainty, information and cost.
og_image: /assets/img/research/computed/replicated_tradeoff.png
img: assets/img/research/previews/replicated_tradeoff.svg
img_alt: Ten synthetic designs compared on mean squared error and assumed measurement cost. Nondominated designs are outlined.
importance: 3
category: "Released software"
github: https://github.com/jcm-sci/trade-study
---

**trade-study** helps researchers compare experiments, model settings and data-collection plans using repeated simulations. Users supply a simulator and scorer, define factors and objectives, and compare choices such as model formulations, numerical methods or measurement strategies.

[Public alpha release on PyPI](https://pypi.org/project/trade-study/) · [Documentation and executable examples](https://jcm-sci.github.io/trade-study/guide/capabilities/) · [Archived release](https://doi.org/10.5281/zenodo.19599838)

The package supports design grids, replicated and paired comparisons, adaptive searches, sensitivity analysis and model weighting. Saved results, caches and provenance support resuming and checking a study.

A Pareto front identifies candidates for which no alternative improves one stated objective without worsening another. Choosing among them also requires preferences or constraints. Statistical comparisons depend on the replicate design; synthetic findings need separate assessment before being applied to observed data. The [computed example](/software-examples/#replicated-designs) states its measurement model, assumed costs and numerical checks.

{% include figure.liquid path="assets/img/research/computed/replicated_tradeoff.svg" class="img-fluid rounded" zoomable=true alt="Ten synthetic sample-mean designs compared across 512 paired replicates. Nondominated mean error and assumed cost are marked, and empirical errors are compared with analytic variances. Costs are declared assumptions, not measured field costs." caption="Ten synthetic measurement designs, each evaluated on 512 paired replicates. Cost is an assumed input, not a measured field cost." %}

[Computed example, inputs and checks](/software-examples/#replicated-designs)

[Method diagram (SVG)](/assets/img/research/trade_study_slide.svg) · [Vector PDF](/assets/img/research/trade_study_slide.pdf) · [All figure sources and downloads](/figures/)
