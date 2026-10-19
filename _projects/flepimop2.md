---
layout: page
title: FlepiMoP2
description: Configuration-driven orchestration engine for CDC-supported infectious disease forecasting and scenario analysis. Plugin architecture decoupling model specification, integration, and persistence.
img: assets/img/research/flepimop2_slide.png
img_alt: FlepiMoP2 workflow from validated configuration and plugin resolution through campaign execution and persisted outputs.
importance: 1
category: collaborative infrastructure
github: https://github.com/ACCIDDA/flepimop2
---

**FlepiMoP2** (Flexible Pipeline for Interchangeable Model Processing) is a configuration-driven orchestration engine for infectious disease forecasting and scenario analysis, supporting CDC-CFA operations. The pipeline decouples model specification (System), numerical integration (Engine), and output persistence (Backend) — along with parameters, post-processing steps, scenario grids, and batch job execution — via a **plugin architecture** with abstract base classes, Pydantic-validated configuration, and dynamic module loading.

Core contributions include the modular System/Engine/Backend dispatch architecture, ODE solver interfaces consumed by [OP Engine](/projects/op_engine/), and performance benchmarking across FlepiMoP v1 that identified 5–20× gains and motivated the v2 redesign.

The pipeline is [published on PyPI](https://pypi.org/project/flepimop2/). See the
[current documentation](https://accidda.github.io/flepimop2/latest/) for its
configuration and provider interfaces. The mathematical and numerical cores
remain usable independently; provider availability and backend qualification
are separate from the orchestration API.
