---
layout: page
title: OP System
description: Compile PDE, nonlocal and reaction model specifications into evaluators and numerical metadata.
img: assets/img/research/op_system_slide.svg
img_alt: OP System compiles PDEs, nonlocal field dynamics, compartmental models and reactions into shaped evaluators and numerical metadata. Numerical consumers choose discretization and time or event integration. Cross-axis constraints remain metadata.
importance: 3
category: "lead developer · released"
github: https://github.com/ACCIDDA/op_system
---

**OP System** is the specification and compilation layer for structured dynamical systems, including spatial/trait-structured PDEs, nonlocal integral/mixing dynamics, compartmental flows, ODEs and stochastic reaction networks. Researchers define explicit governing equations or compartmental transitions; restricted expressions pass through a typed intermediate representation to vectorized evaluators for NumPy, JAX and PyTorch.

[Released on PyPI](https://pypi.org/project/op-system/) and actively developed. See the [capability guide and executable examples](https://accidda.github.io/op_system/latest/guides/capabilities/).

Categorical and continuous axes, aliases, staged chains, routing, kernels and operator metadata describe structured models. The compiler carries field and operator semantics; numerical consumers choose spatial discretization and time/event integration. Flat, PyTree and independent-block layouts let a numerical consumer choose its state representation. Named latent observables keep measured quantities and physical reductions separate from the dynamics.

For stochastic consumers, named reactions expose channel structure, propensity shapes, reactants/dependencies and checked independence declarations. Time-indexed parameters support linear interpolation or right-continuous held forcing, with published schedules and resolved-parameter callbacks. [OP Engine](/projects/op_engine/) consumes these contracts for solving and independent replicate banks.

Structural validation checks the specification and supported evaluator paths. Independent-equation fixtures and conditional reaction balances provide additional numerical evidence; none of these checks proves the scientific model correct. [Cross-axis constraints remain metadata](https://accidda.github.io/op_system/latest/guides/getting-started/#cross-axis-constraints-current-boundary), rather than an enforced filter on state cells or transitions.

{% include figure.liquid path="assets/img/research/op_system_slide.svg" class="img-fluid rounded" zoomable=true alt="OP System compiles PDEs, nonlocal field dynamics, compartmental models and reactions into shaped evaluators and numerical metadata. Numerical consumers choose discretization and time or event integration. Cross-axis constraints remain metadata." caption="OP System compilation and numerical interfaces." %}

[Vector PDF](/assets/img/research/op_system_slide.pdf) · [All figure sources and downloads](/figures/)
