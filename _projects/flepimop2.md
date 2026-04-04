---
layout: page
title: FlepiMoP2
description: Modular epidemic modeling and simulation pipeline for forecasting and scenario analysis. Core contributor to the redesign of ACCIDDA's operational infrastructure.
img:
importance: 1
category: collaborative infrastructure
github: https://accidda.github.io/flepimop2/latest/
---

**FlepiMoP2** (Flexible Epidemic Modeling Pipeline 2) is a modular simulation campaign orchestrator for infectious disease forecasting and scenario analysis. The pipeline manages config-driven batch runs over locations and scenarios with pluggable system and engine backends, parameter management, and output collection.

Core contributions include modular ODE solver interfaces, pluggable system/engine dispatch architecture, and performance benchmarking that identified vectorization-driven gains of 5--20x informing the redesign from FlepiMoP v1.
