---
layout: page
title: op_infer
description: Private pre-alpha statistical layer connecting Bayesian parameter inference, calibration checks and study design for partially observed systems.
img: assets/img/research/beyond_onehealth.svg
img_alt: Public simulation and evaluation tools connect to op_infer, a working statistical layer that remains private, pre-alpha and unreleased.
importance: 2
category: "lead developer · in development"
---

What can sparse, noisy measurements tell us about a dynamical system, and how
can we check whether the inference procedure is reliable for that question?
I am developing **op_infer**, the statistical layer of the op stack, to connect scientific models to parameter
inference, calibration checks and study design.

**Status:** working research software, private, pre-alpha and unreleased. The implementation
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

{% include figure.liquid path="assets/img/research/beyond_onehealth.svg" class="img-fluid rounded" zoomable=true alt="Public tools cover specification, simulation, campaign execution and replicated evaluation. op_infer connects inference and calibration to these capabilities and remains private, pre-alpha and unreleased." caption="op_infer builds on public modeling, simulation and evaluation tools." %}

[Vector PDF](/assets/img/research/beyond_onehealth.pdf) · [Research in progress](/projects/current_analyses/) · [Figure sources and downloads](/figures/)
