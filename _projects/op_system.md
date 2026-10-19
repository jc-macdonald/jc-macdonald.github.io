---
layout: page
title: OP System
description: Describe models of changing systems, including spatial interactions and random events.
img: assets/img/research/previews/spatial_diffusion.svg
img_alt: Synthetic periodic diffusion on 64 cells, computed with OP System and OP Engine. The heatmap shows field values over position and time.
importance: 1
category: "Released software"
github: https://github.com/ACCIDDA/op_system
---

**OP System** turns readable descriptions of changing systems into calculations that simulation tools can use. It is the specification and compilation layer for structured dynamical systems, including partial differential equations (PDEs) with spatial or trait structure, nonlocal interactions, compartmental flows, ordinary differential equations (ODEs) and stochastic reaction networks. Researchers define explicit governing equations or compartmental transitions; the compiler translates supported expressions into numerical evaluators for NumPy, JAX and PyTorch.

[Public alpha release on PyPI](https://pypi.org/project/op-system/) and actively developed. See the [capability guide and executable examples](https://accidda.github.io/op_system/latest/guides/capabilities/).

Categorical and continuous axes, aliases, staged chains, routing, kernels and operator metadata describe structured models. The compiler carries field and operator semantics; numerical consumers choose spatial discretization and time/event integration. Flat, PyTree and independent-block layouts let a numerical consumer choose its state representation. Named latent observables keep measured quantities and physical reductions separate from the dynamics.

For stochastic consumers, named reactions expose channel structure, propensity shapes, reactants/dependencies and checked independence declarations. Time-indexed parameters support linear interpolation or right-continuous held forcing, with published schedules and resolved-parameter callbacks. [OP Engine](/projects/op_engine/) consumes these contracts for solving and independent replicate banks.

Specification validation checks supported expressions, shapes and numerical interfaces. Tests against independently written equations and reaction-balance checks provide numerical evidence under stated assumptions. Scientific adequacy requires assessment against the intended application. [Cross-axis constraints remain metadata](https://accidda.github.io/op_system/latest/guides/getting-started/#cross-axis-constraints-current-boundary), rather than an enforced filter on state cells or transitions.

{% include figure.liquid path="assets/img/research/computed/spatial_diffusion.svg" class="img-fluid rounded" zoomable=true alt="A 64-cell periodic diffusion field and profiles at four times, computed from an OP System specification with RK4 integration in OP Engine. Spatial discretization is supplied explicitly; all inputs are synthetic." caption="Synthetic periodic diffusion compiled by OP System and integrated by OP Engine. The spatial stencil is supplied explicitly." %}

[Computed example, inputs and checks](/software-examples/#spatial-diffusion)

{% include figure.liquid path="assets/img/research/op_system_slide.svg" class="img-fluid rounded" zoomable=true alt="A model specification feeds a compiler, which exports evaluators, operator/reaction metadata, and observation/forcing interfaces. Model classes include PDEs, nonlocal dynamics, compartments and reactions. Numerical consumers choose discretization and integration; cross-axis constraints remain metadata." caption="OP System compilation and numerical interfaces." %}

[Vector PDF](/assets/img/research/op_system_slide.pdf) · [All figure sources and downloads](/figures/)
