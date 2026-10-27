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
last_modified_at: 2026-10-26
---

**OP Engine** is a general-purpose numerical core for models that change over time and space, including systems with random events. It supports partial differential equations (PDEs) with spatial or trait structure, nonlocal interactions, compartmental models, ordinary differential equations (ODEs) and stochastic reaction networks. These interfaces are not specific to public health; current examples span epidemiological and biogeochemical systems, and other domains can supply the same model contracts.

{% assign release = site.data.software_releases.packages.op_engine %}
{% include software_release_status.liquid slug="op_engine" %} · [{{ release.docs_label }} and executable examples]({{ release.docs_url }})

Its methods include explicit, implicit-explicit (IMEX) and implicit integration, exact stochastic simulation, and approximate tau-leaping. Independent stochastic runs use separate event clocks. Named observations, time-window summaries and optional reaction firing counts support analysis of the simulated outputs.

[OP System](/projects/op_system/) supplies model equations and metadata. OP Engine can also be used directly. The separately released `flepimop2-op_engine` provider connects compatible versions to [FlepiMoP2](/projects/flepimop2/); the provider and core have independent release lifecycles. No provider release currently accompanies OP Engine 0.9.1, so the core can be used directly pending a documented compatible provider release.

Supported backends and derivatives depend on the method and precision; {% assign qualification_docs = release.docs_url | replace: 'capabilities/', 'backend-qualification/' %}see the [qualification matrix]({{ qualification_docs }}). Spatial and temporal accuracy require separate checks. Derivatives through frozen-schedule replay hold step-size decisions fixed and are conditional on the recorded mesh.

{% include figure.liquid path="assets/img/research/stack/stack_spec_to_ssa.svg" class="img-fluid rounded" zoomable=true alt="Two panels: infectious hosts over time in a 400-host model with waning immunity, showing a percentile band across 256 exact stochastic paths, their median, and the deterministic solution of the same specification; and the mean cumulative infection, recovery and waning events per path from retained firing counts." caption="One transition specification run as an ODE and as 256 exact stochastic paths with retained event counts. Population is conserved and the state equals initial state plus stoichiometry times counts on every path. Illustrative parameters." %}

[What this figure supports and its limits](/software-examples/#op-stack-design-and-verification) · [Computed stochastic example, inputs and checks](/software-examples/#stochastic-transfers)

[Method diagram (SVG)](/assets/img/research/op_engine_slide.svg) · [Vector PDF](/assets/img/research/op_engine_slide.pdf) · [All figure sources and downloads](/figures/)
