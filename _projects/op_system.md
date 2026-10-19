---
layout: page
title: OP System
description: Specify PDE/field, nonlocal and reaction models; compile evaluators, operators and observables.
img: assets/img/research/op_system_slide.svg
img_alt: PDEs, nonlocal field dynamics, compartmental models and reactions are specified with coordinates and parameters, compiled through restricted syntax and typed IR, and published as shaped evaluators plus operator, reaction, observable and forcing contracts. Numerical consumers own discretization and time/event integration; cross-axis constraints remain metadata.
importance: 3
category: "lead developer · released"
github: https://github.com/ACCIDDA/op_system
---

**OP System** is the specification and compilation layer for structured dynamical systems, including spatial/trait-structured PDEs, nonlocal integral/mixing dynamics, compartmental flows, ODEs and stochastic reaction networks. Researchers define explicit governing equations or compartmental transitions; restricted expressions pass through a typed intermediate representation to vectorized evaluators for NumPy, JAX and PyTorch.

**Status:** [Released on PyPI](https://pypi.org/project/op-system/) and actively developed. See the [capability guide and executable examples](https://accidda.github.io/op_system/latest/guides/capabilities/).

Categorical and continuous axes, aliases, staged chains, routing, kernels and operator metadata describe structured models. The compiler carries field and operator semantics; numerical consumers choose spatial discretization and time/event integration. Flat, PyTree and independent-block layouts let a numerical consumer choose its state representation. Named latent observables keep measured quantities and physical reductions separate from the dynamics.

For stochastic consumers, named reactions expose channel structure, propensity shapes, reactants/dependencies and checked independence declarations. Time-indexed parameters support linear interpolation or right-continuous held forcing, with published schedules and resolved-parameter callbacks. [OP Engine](/projects/op_engine/) consumes these contracts for solving and independent replicate banks.

Structural validation checks the specification and supported evaluator paths. Independent-equation fixtures and conditional reaction balances provide additional numerical evidence; none of these checks proves the scientific model correct. [Cross-axis constraints remain metadata](https://accidda.github.io/op_system/latest/guides/getting-started/#cross-axis-constraints-current-boundary), rather than an enforced filter on state cells or transitions.

{% include figure.liquid path="assets/img/research/op_system_slide.svg" class="img-fluid rounded" zoomable=true alt="PDEs, nonlocal field dynamics, compartmental models and reactions are specified with coordinates and parameters, compiled through restricted syntax and typed IR, and published as shaped evaluators plus operator, reaction, observable and forcing contracts. Numerical consumers own discretization and time/event integration; cross-axis constraints remain metadata." caption="OP System compilation and numerical contracts." %}

[Vector PDF](/assets/img/research/op_system_slide.pdf) · [All figure sources and downloads](/figures/)
