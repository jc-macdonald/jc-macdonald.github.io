---
layout: page
title: pp-eigentest
description: Research on how much signal incomplete datasets can support. Methods and private pre-release software in development.
img: assets/img/research/pp_eigentest_schematic.svg
img_alt: Ongoing signal-rank research connects incomplete data, Bayesian latent-variable modeling, and assessment of signal and uncertainty. The methods and software remain in development.
importance: 3
category: "lead developer · in development"
---

**pp-eigentest** investigates posterior predictive eigenvalue testing to assess
how many dimensions reflect signal when entries are missing. It uses Bayesian latent-variable
models and examines how rank decisions depend on data quality, uncertainty
and model assessment.

This is ongoing methods research with private pre-release software. A methods
paper is in preparation. The work extends the approach described in the
[2024 preprint](https://arxiv.org/abs/2409.12129), which is the public reference
for the earlier methodology. It is distinct from the released
[VBPCApy](/projects/vbpca_py/) package.

The aim is to support interpretable rank decisions with an account of their
uncertainty and assumptions. Current research includes calibration and
evaluation across incomplete-data settings. Public artifacts will be linked as
the work is released.

{% include figure.liquid path="assets/img/research/pp_eigentest_schematic.svg" class="img-fluid rounded" zoomable=true alt="Ongoing signal-rank research connects incomplete data, Bayesian latent-variable modeling, and assessment of signal and uncertainty. The methods and software remain in development." caption="Signal-rank research for incomplete data." %}

[Vector PDF](/assets/img/research/pp_eigentest_schematic.pdf) · [All figure sources and downloads](/figures/)
