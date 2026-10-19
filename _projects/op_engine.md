---
layout: page
title: OP Engine
description: Simulate changing systems and random events, from spatial dynamics to population counts.
img: assets/img/research/previews/stochastic_ensemble.svg
img_alt: Independent stochastic transfer paths with a pointwise 5th–95th percentile band and the analytic mean. All inputs are synthetic.
importance: 2
category: "Released software"
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** simulates how modeled systems change over time and space, including systems with random events. It is a numerical core for structured dynamical systems: partial differential equations (PDEs) with spatial or trait structure, nonlocal interactions, compartmental models, ordinary differential equations (ODEs) and stochastic reaction networks. It supports explicit, implicit-explicit (IMEX), implicit and stochastic methods and can be used directly or through the separately packaged [FlepiMoP2](/projects/flepimop2/) provider.

[Public alpha release on PyPI](https://pypi.org/project/op-engine/) and actively developed. The [capability guide](https://accidda.github.io/op_engine/latest/guides/capabilities/) maps public interfaces to runnable examples.

Current workflows include:

- Spatial/trait PDE and nonlocal field dynamics through declared grids, measures, matrix/kernel operators and explicit/IMEX/implicit stepping. Spatial and temporal accuracy require separate checks.
- ODE and compartmental integration, including nonlinear-stage diagnostics.
- Exact simulation with the direct stochastic simulation algorithm (SSA), bounded thinning for time-varying event rates, and approximate fixed/adaptive tau-leaping.
- Independent NumPy CPU SSA banks with one event clock per replicate, stable replicate IDs, forcing boundaries and optional reaction firing counts.
- Named observations and window summaries, conditional conservation checks and steady-state analysis.
- Adaptive schedule discovery and frozen-schedule replay, with explicit accuracy and provenance checks.

The [backend qualification matrix](https://accidda.github.io/op_engine/latest/guides/backend-qualification/) lists tested NumPy, JAX and CPU PyTorch methods, precisions and derivatives. Coverage depends on the method and transform. GPU and CuPy paths require separate hardware qualification.

Replay derivatives are conditional on the recorded mesh. Step-size decisions are held fixed. Accuracy checks and changes in parameters can require a fresh discovery solve.

[OP System](/projects/op_system/) supplies compiled equations, reactions and observation metadata. [trade-study](/projects/trade_study/) can compare solver configurations and simulation designs.

{% include figure.liquid path="assets/img/research/computed/stochastic_ensemble.svg" class="img-fluid rounded" zoomable=true alt="512 independent exact stochastic transfer simulations, their empirical mean and pointwise 5th–95th percentile range, and the final distribution alongside analytic mean and binomial references. Synthetic demonstration." caption="512 independent stochastic transfer runs, with analytic mean and final-distribution references. The shaded range describes variation across runs." %}

[Computed example, inputs and checks](/software-examples/#stochastic-transfers)

{% include figure.liquid path="assets/img/research/op_engine_slide.svg" class="img-fluid rounded" zoomable=true alt="A capability table groups deterministic solvers, stochastic solvers and schedule replay. It lists PDE/field, nonlocal, ODE and reaction models, observations and optional firing counts. Independent SSA clocks use NumPy. Replay derivatives are conditional on the recorded mesh; tested backends vary by method." caption="OP Engine method families." %}

[Vector PDF](/assets/img/research/op_engine_slide.pdf) · [All figure sources and downloads](/figures/)
