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
last_modified_at: 2026-10-23
---

**OP System** is a general-purpose model specification and compilation tool. It turns readable descriptions of partial differential equations (PDEs) with spatial or trait structure, nonlocal interactions, compartmental flows, ordinary differential equations (ODEs) and stochastic reaction networks into calculations for simulation. Researchers specify equations or transitions; the compiler produces NumPy and JAX evaluators and, within the documented qualified scopes, raw PyTorch evaluators. The model language is domain-independent rather than limited to epidemiological or public-health systems.

{% assign release = site.data.software_releases.packages.op_system %}
{% include software_release_status.liquid slug="op_system" %} · [{{ release.docs_label }} and executable examples]({{ release.docs_url }})

Named axes describe groups, space and traits. Model interfaces expose reactions, operators, named latent observables and time-varying parameters. [OP Engine](/projects/op_engine/) can use these interfaces for simulation; measurement-error and observation models belong in downstream analyses. Other numerical tools can consume the compiled calculations.

Numerical consumers choose spatial discretization and time or event integration. Validation checks expressions, shapes and interface contracts. {% assign constraint_docs = release.docs_url | replace: 'capabilities/', 'getting-started/#cross-axis-constraints-current-boundary' %}[Cross-axis constraints]({{ constraint_docs }}) are recorded as metadata and do not filter state cells or transitions. Numerical accuracy and scientific adequacy need checks for the intended application.

{% include figure.liquid path="assets/img/research/computed/spatial_diffusion.svg" class="img-fluid rounded" zoomable=true alt="A 64-cell periodic diffusion field and profiles at four times, computed from an OP System specification with RK4 integration in OP Engine. Spatial discretization is supplied explicitly; all inputs are synthetic." caption="Synthetic periodic diffusion compiled by OP System and integrated by OP Engine. The spatial stencil is supplied explicitly." %}

[Computed example, inputs and checks](/software-examples/#spatial-diffusion)

[Method diagram (SVG)](/assets/img/research/op_system_slide.svg) · [Vector PDF](/assets/img/research/op_system_slide.pdf) · [All figure sources and downloads](/figures/)
