---
layout: page
title: OP Engine
description: Simulate changing systems and random events, from spatial dynamics to population counts.
og_image: /assets/img/research/computed/stochastic_ensemble.png
img: assets/img/research/previews/stochastic_ensemble.svg
img_alt: Independent stochastic transfer paths with a pointwise 5th–95th percentile band and the analytic mean. All inputs are synthetic.
importance: 2
category: "Released software"
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** simulates how models change over time and space, including systems with random events. It supports partial differential equations (PDEs) with spatial or trait structure, nonlocal interactions, compartmental models, ordinary differential equations (ODEs) and stochastic reaction networks.

[Public alpha release on PyPI](https://pypi.org/project/op-engine/) · [v0.8 documentation and executable examples](https://accidda.github.io/op_engine/0.8/guides/capabilities/)

Its methods include explicit, implicit-explicit (IMEX) and implicit integration, exact stochastic simulation, and approximate tau-leaping. Independent stochastic runs use separate event clocks. Named observations, time-window summaries and optional reaction firing counts support analysis of the simulated outputs.

[OP System](/projects/op_system/) supplies model equations and metadata. OP Engine can also be used directly or through its separately packaged [FlepiMoP2](/projects/flepimop2/) provider.

Supported backends and derivatives depend on the method and precision; see the [qualification matrix](https://accidda.github.io/op_engine/0.8/guides/backend-qualification/). Spatial and temporal accuracy require separate checks. Derivatives through frozen-schedule replay hold step-size decisions fixed and are conditional on the recorded mesh.

{% include figure.liquid path="assets/img/research/computed/stochastic_ensemble.svg" class="img-fluid rounded" zoomable=true alt="512 independent exact stochastic transfer simulations, their empirical mean and pointwise 5th–95th percentile range, and the final distribution alongside analytic mean and binomial references. Synthetic demonstration." caption="512 independent stochastic transfer runs, with analytic mean and final-distribution references. The shaded range describes variation across runs." %}

[Computed example, inputs and checks](/software-examples/#stochastic-transfers)

[Method diagram (SVG)](/assets/img/research/op_engine_slide.svg) · [Vector PDF](/assets/img/research/op_engine_slide.pdf) · [All figure sources and downloads](/figures/)
