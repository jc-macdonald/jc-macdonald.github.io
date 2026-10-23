---
layout: page
title: op_infer
description: Estimate model quantities from incomplete data and assess fitting methods with public research software.
img: assets/img/research/previews/op_infer_normal_sbc.svg
img_alt: Randomized-rank PIT counts from an intentionally underpowered 64-replicate synthetic SBC demonstration.
importance: 2
category: "Research in progress"
last_modified_at: 2026-10-23
---

I am developing **op_infer** as a domain-independent bridge from scientific
models to parameter inference, calibration checks and study design.

{% include software_release_status.liquid slug="inference_calibration" %}

The implementation includes selected adapters to inference libraries,
simulation-based calibration and replicated studies that test recovery on
simulated data. Broader interfaces and application-specific validation remain
in development; operational data, partner discussions and application
materials remain private.

{% assign release = site.data.software_releases.packages.inference_calibration %}
[Public source](https://github.com/ACCIDDA/op_infer) · [{{ release.docs_label }}: capabilities and executable examples]({{ release.docs_url }})

The research asks how measurement assumptions and fitting procedures affect
what can be learned about a scientific system. Simulation-based calibration
assesses posterior inference using repeated data generated from the assumed
model and prior. It does not establish that those assumptions describe observed
data. Identifying a quantity from data also depends on the model, measurement
process and available observations.

op_infer builds on [OP System](/projects/op_system/) for model specification,
[OP Engine](/projects/op_engine/) for numerical simulation, and
[trade-study](/projects/trade_study/) for replicated evaluation. Their public
documentation and releases provide the foundations for this work.

{% include figure.liquid path="assets/img/research/computed/op_infer_normal_sbc.svg" class="img-fluid rounded" zoomable=true alt="An exact Normal posterior density overlaid on 1,024 analytic-fixture draws, beside randomized-rank PIT counts from 64 SBC replicates." caption="A checked synthetic fixture from public pre-alpha op_infer. The SBC bank is deliberately underpowered and is not calibration evidence." %}

[Example assumptions and retained data](/software-examples/#inference-calibration) ·
[Capability diagram](/assets/img/research/op_infer_slide.svg) ·
[Research in progress](/projects/current_analyses/) ·
[Figure sources and downloads](/figures/)
