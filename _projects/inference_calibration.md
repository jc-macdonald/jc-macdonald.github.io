---
layout: page
title: op_infer
description: Estimate model quantities from incomplete data and assess fitting methods. Private pre-alpha research software.
img: assets/img/research/op_infer_slide.svg
img_alt: op_infer capabilities include fitting through established libraries, calibration checks on simulated data, and replicated study comparisons. Private, pre-alpha and unreleased.
importance: 2
category: "Research in progress"
---

I am developing **op_infer** to connect scientific models to parameter
inference, calibration checks and study design.

The software is private, pre-alpha and unreleased. The implementation
includes Bayesian fitting through established inference libraries,
simulation-based calibration, and replicated studies that test recovery on
simulated data. Broader interfaces and application-specific validation remain
in development.

The aim is to make it easier to distinguish uncertainty in the scientific
system from limitations of its measurements and inference procedure.
Simulation-based calibration checks an inference procedure against data
generated under stated assumptions; adequacy for observed scientific data
requires separate assessment. A reliable workflow also needs to ask whether
the available observations can identify the quantities that matter for a decision.

op_infer builds on [OP System](/projects/op_system/) for model specification,
[OP Engine](/projects/op_engine/) for numerical simulation, and
[trade-study](/projects/trade_study/) for replicated evaluation. Their public
documentation and releases provide the foundations for this work.

{% include figure.liquid path="assets/img/research/op_infer_slide.svg" class="img-fluid rounded" zoomable=true alt="op_infer capabilities include fitting through established libraries, calibration checks on simulated data, and replicated study comparisons. Private, pre-alpha and unreleased." caption="Working research capabilities; broader interfaces and application-specific validation remain in development." %}

[Vector PDF](/assets/img/research/op_infer_slide.pdf) · [Research in progress](/projects/current_analyses/) · [Figure sources and downloads](/figures/)
