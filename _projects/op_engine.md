---
layout: page
title: OP Engine
description: Simulate deterministic and stochastic dynamics, with numerical checks, named observations and replay.
img: assets/img/research/op_engine_slide.svg
img_alt: Prepare state and operators, solve deterministic or stochastic dynamics, record observations and optional counts, then check accuracy and replay. Independent SSA clocks use NumPy; backend qualification is method-specific and replay derivatives depend on the recorded mesh.
importance: 2
category: "lead developer · released"
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** is a numerical core for compartmental and spatial dynamical systems. It supports explicit, IMEX, implicit and stochastic methods and can be used directly or through the separately packaged [FlepiMoP2](/projects/flepimop2/) provider.

**Status:** [Released on PyPI](https://pypi.org/project/op-engine/) and actively developed. The [capability guide](https://accidda.github.io/op_engine/latest/guides/capabilities/) maps public interfaces to runnable examples.

Current workflows include:

- ODE/PDE integration with explicit, split and implicit methods, spatial operators and nonlinear-stage diagnostics.
- Exact direct SSA, bounded thinning for time-varying hazards, and approximate fixed/adaptive tau-leaping.
- Independent NumPy CPU SSA banks with one event clock per replicate, stable replicate IDs, forcing boundaries and optional reaction firing counts.
- Named observations and window summaries, conditional conservation checks and steady-state analysis.
- Adaptive schedule discovery and frozen-schedule replay, with explicit accuracy and provenance checks.

The [backend qualification matrix](https://accidda.github.io/op_engine/latest/guides/backend-qualification/) specifies the tested NumPy, JAX and CPU PyTorch methods, precisions and derivatives. These guarantees vary by method and transform. GPU and CuPy paths require separate hardware qualification.

A frozen replay differentiates the recorded numerical map, conditional on its mesh; it does not differentiate step-size decisions. Accuracy checks and changes in parameters can require a fresh discovery solve.

[OP System](/projects/op_system/) supplies compiled equations, reactions and observation metadata. [trade-study](/projects/trade_study/) can compare solver configurations and simulation designs.

{% include figure.liquid path="assets/img/research/op_engine_slide.svg" class="img-fluid rounded" zoomable=true alt="Prepare state and operators, solve deterministic or stochastic dynamics, record observations and optional counts, then check accuracy and replay. Independent SSA clocks use NumPy; backend qualification is method-specific and replay derivatives depend on the recorded mesh." caption="OP Engine numerical workflow." %}

[Vector PDF](/assets/img/research/op_engine_slide.pdf) · [All figure sources and downloads](/figures/)
