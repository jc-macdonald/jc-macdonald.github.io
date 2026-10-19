---
layout: page
title: Inference and calibration
description: Working research software connects Bayesian parameter inference, calibration checks and study design for partially observed systems.
img: assets/img/research/beyond_onehealth.svg
img_alt: Public simulation and evaluation tools connect to working inference and calibration research software, which remains private and pre-release.
importance: 2
category: "lead developer · in development"
---

What can sparse, noisy measurements tell us about a dynamical system, and how
can we check whether the inference procedure is reliable for that question?
I am developing reusable tools that connect scientific models to parameter
inference, calibration checks and study design.

**Status:** working research software, private and pre-release. The implementation
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

This work builds on [OP System](/projects/op_system/) for model specification,
[OP Engine](/projects/op_engine/) for numerical simulation, and
[trade-study](/projects/trade_study/) for replicated evaluation. Their public
documentation and releases provide the foundations for this work.

{% include figure.liquid path="assets/img/research/beyond_onehealth.svg" class="img-fluid rounded" zoomable=true alt="Public tools cover specification, simulation, campaign execution and replicated evaluation. Working inference and calibration research software connects these capabilities and remains private and pre-release." caption="The inference work builds on public modeling, simulation and evaluation tools." %}

[Vector PDF](/assets/img/research/beyond_onehealth.pdf) · [Research in progress](/projects/current_analyses/) · [Figure sources and downloads](/figures/)
