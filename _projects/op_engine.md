---
layout: page
title: OP Engine
description: Simulate PDE/field, nonlocal and reaction dynamics, with observations, numerical checks and replay.
img: assets/img/research/op_engine_slide.svg
img_alt: OP Engine prepares field and reaction models, solves discretized PDEs, nonlocal dynamics and stochastic reactions, and records observations and firing counts. Independent SSA clocks use NumPy. Tested operations depend on the method. Replay derivatives are conditional on the recorded mesh.
importance: 2
category: "lead developer · released"
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** is a numerical core for structured dynamical systems: spatial/trait-structured PDEs, nonlocal integral/mixing dynamics, compartmental models, ODEs and stochastic reaction networks. It supports explicit, IMEX, implicit and stochastic methods and can be used directly or through the separately packaged [FlepiMoP2](/projects/flepimop2/) provider.

[Released on PyPI](https://pypi.org/project/op-engine/) and actively developed. The [capability guide](https://accidda.github.io/op_engine/latest/guides/capabilities/) maps public interfaces to runnable examples.

Current workflows include:

- Spatial/trait PDE and nonlocal field dynamics through declared grids, measures, matrix/kernel operators and explicit/IMEX/implicit stepping. Spatial and temporal accuracy require separate checks.
- ODE and compartmental integration, including nonlinear-stage diagnostics.
- Exact direct SSA, bounded thinning for time-varying hazards, and approximate fixed/adaptive tau-leaping.
- Independent NumPy CPU SSA banks with one event clock per replicate, stable replicate IDs, forcing boundaries and optional reaction firing counts.
- Named observations and window summaries, conditional conservation checks and steady-state analysis.
- Adaptive schedule discovery and frozen-schedule replay, with explicit accuracy and provenance checks.

The [backend qualification matrix](https://accidda.github.io/op_engine/latest/guides/backend-qualification/) lists tested NumPy, JAX and CPU PyTorch methods, precisions and derivatives. Coverage depends on the method and transform. GPU and CuPy paths require separate hardware qualification.

Replay derivatives are conditional on the recorded mesh. Step-size decisions are held fixed. Accuracy checks and changes in parameters can require a fresh discovery solve.

[OP System](/projects/op_system/) supplies compiled equations, reactions and observation metadata. [trade-study](/projects/trade_study/) can compare solver configurations and simulation designs.

{% include figure.liquid path="assets/img/research/op_engine_slide.svg" class="img-fluid rounded" zoomable=true alt="OP Engine prepares field and reaction models, solves discretized PDEs, nonlocal dynamics and stochastic reactions, and records observations and firing counts. Independent SSA clocks use NumPy. Tested operations depend on the method. Replay derivatives are conditional on the recorded mesh." caption="OP Engine numerical workflow." %}

[Vector PDF](/assets/img/research/op_engine_slide.pdf) · [All figure sources and downloads](/figures/)
