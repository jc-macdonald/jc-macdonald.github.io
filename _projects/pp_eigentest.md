---
layout: page
title: pp-eigentest
description: Ongoing research on posterior-predictive signal-rank selection for incomplete datasets, building on a 2024 preprint.
img: assets/img/research/pp_eigentest_schematic.svg
img_alt: Ongoing signal-rank research connects incomplete data, Bayesian latent-variable modeling, and assessment of signal and uncertainty. The methods and software remain in development.
importance: 3
category: "lead developer · in development"
---

How many dimensions of a dataset reflect signal rather than noise, especially
when entries are missing? **pp-eigentest** investigates posterior predictive
eigenvalue testing for this question. It builds on Bayesian latent-variable
models and examines how rank decisions depend on data quality, uncertainty
and model assessment.

**Status:** ongoing methods research and private pre-release software; a methods
paper is in preparation. The work extends the approach described in the
[2024 preprint](https://arxiv.org/abs/2409.12129), which is the public reference
for the earlier methodology. It is distinct from the released
[VBPCApy](/projects/vbpca_py/) package.

The aim is to support interpretable rank decisions with an account of their
uncertainty and assumptions. Current research includes calibration and
evaluation across incomplete-data settings. Public artifacts will be linked as
the work is released.

{% include figure.liquid path="assets/img/research/pp_eigentest_schematic.svg" class="img-fluid rounded" zoomable=true alt="Ongoing signal-rank research connects incomplete data, Bayesian latent-variable modeling, and assessment of signal and uncertainty. The methods and software remain in development." caption="Research scope: signal-rank assessment for incomplete data." %}

[Vector PDF](/assets/img/research/pp_eigentest_schematic.pdf) · [All figure sources and downloads](/figures/)
