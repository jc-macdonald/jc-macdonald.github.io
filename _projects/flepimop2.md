---
layout: page
title: FlepiMoP2
description: Configuration-driven orchestration engine for CDC-supported infectious disease forecasting and scenario analysis. Plugin architecture decoupling model specification, integration, and persistence.
img: assets/img/research/flepimop2_slide.png
importance: 1
category: collaborative infrastructure
github: https://accidda.github.io/flepimop2/latest/
---

**FlepiMoP2** (Flexible Epidemic Modeling Pipeline 2) is a configuration-driven orchestration engine for infectious disease forecasting and scenario analysis, supporting CDC-CFA operations. The pipeline decouples model specification (System), numerical integration (Engine), and output persistence (Backend) via a **plugin architecture** with abstract base classes, Pydantic-validated configuration, and dynamic module loading.

Core contributions include the modular System/Engine/Backend dispatch architecture, ODE solver interfaces consumed by [OP Engine](/projects/op_engine/), and performance benchmarking across FlepiMoP v1 that identified 5–20× gains and motivated the v2 redesign.
