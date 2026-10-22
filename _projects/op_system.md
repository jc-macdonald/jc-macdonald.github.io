---
layout: page
title: OP System
description: Describe models of changing systems, including spatial interactions and random events.
og_image: /assets/img/research/computed/spatial_diffusion.png
img: assets/img/research/previews/spatial_diffusion.svg
img_alt: Synthetic periodic diffusion on 64 cells, computed with OP System and OP Engine. The heatmap shows field values over position and time.
importance: 1
category: "Released software"
github: https://github.com/ACCIDDA/op_system
last_modified_at: 2026-10-22
---

**OP System** turns readable model descriptions into calculations for simulation. It supports partial differential equations (PDEs) with spatial or trait structure, nonlocal interactions, compartmental flows, ordinary differential equations (ODEs) and stochastic reaction networks. Researchers specify equations or transitions; the compiler produces numerical evaluators for NumPy, JAX and PyTorch.

[Public alpha release on PyPI](https://pypi.org/project/op-system/) · [v0.9 documentation and executable examples](https://accidda.github.io/op_system/0.9/guides/capabilities/)

Named axes describe groups, space and traits. Model interfaces expose reactions, operators, named latent observables and time-varying parameters. [OP Engine](/projects/op_engine/) can use these interfaces for simulation; measurement-error and observation models belong in downstream analyses. Other numerical tools can consume the compiled calculations.

Numerical consumers choose spatial discretization and time or event integration. Validation checks expressions, shapes and interface contracts. [Cross-axis constraints](https://accidda.github.io/op_system/0.9/guides/getting-started/#cross-axis-constraints-current-boundary) are recorded as metadata and do not filter state cells or transitions. Numerical accuracy and scientific adequacy need checks for the intended application.

{% include figure.liquid path="assets/img/research/computed/spatial_diffusion.svg" class="img-fluid rounded" zoomable=true alt="A 64-cell periodic diffusion field and profiles at four times, computed from an OP System specification with RK4 integration in OP Engine. Spatial discretization is supplied explicitly; all inputs are synthetic." caption="Synthetic periodic diffusion compiled by OP System and integrated by OP Engine. The spatial stencil is supplied explicitly." %}

[Computed example, inputs and checks](/software-examples/#spatial-diffusion)

[Method diagram (SVG)](/assets/img/research/op_system_slide.svg) · [Vector PDF](/assets/img/research/op_system_slide.pdf) · [All figure sources and downloads](/figures/)
