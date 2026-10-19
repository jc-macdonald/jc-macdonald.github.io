---
layout: page
title: FlepiMoP2
description: Coordinate simulation runs across locations and scenarios, with reusable models and data tools.
img: assets/img/research/flepimop2_slide.svg
img_alt: Validated configuration selects campaign targets connected to System/Parameter, Engine, Backend, Process and Job providers. Connections indicate interface relationships, not execution order. Cores can also run independently.
importance: 1
category: "Collaborative infrastructure"
github: https://github.com/ACCIDDA/flepimop2
---

**FlepiMoP2** (Flexible Pipeline for Interchangeable Model Processing) runs configuration-defined infectious disease forecasting and scenario campaigns used in CDC-CFA work. Separate providers handle model specification (System), numerical integration (Engine), and result storage (Backend). Other interfaces cover parameters, processing steps, scenarios, and batch jobs. Configuration is validated with Pydantic, and modules are loaded through plugins.

My contributions include the System, Engine, and Backend interfaces, numerical interfaces used by [OP Engine](/projects/op_engine/), and performance profiling of FlepiMoP v1 that informed the redesign.

The pipeline has a [public alpha release on PyPI](https://pypi.org/project/flepimop2/). See the
[current documentation](https://accidda.github.io/flepimop2/latest/) for its
configuration and provider interfaces. The mathematical and numerical cores
remain usable independently; provider availability and backend qualification
are separate from the orchestration API.

{% include figure.liquid path="assets/img/research/flepimop2_slide.svg" class="img-fluid rounded" zoomable=true alt="Validated configuration selects campaign targets connected to System/Parameter, Engine, Backend, Process and Job providers. Connections indicate interface relationships, not execution order. Cores can also run independently." caption="FlepiMoP2 provider relationships." %}

[Vector PDF](/assets/img/research/flepimop2_slide.pdf) · [All figure sources and downloads](/figures/)
