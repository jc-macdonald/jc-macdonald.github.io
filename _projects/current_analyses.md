---
layout: page
title: Research in progress
description: Ongoing work on structural scores, scientific machine learning and disease-modeling applications.
img: assets/img/research/structural_fidelity_comparison.svg
img_alt: Constructed trajectories illustrate adherence to a declared prevalence bound. No predictive scores are computed; predictive scoring and structural checks answer separate evaluation questions.
importance: 1
category: "lead developer · in development"
---

My current research connects mechanistic modeling, Bayesian inference and
evaluation for decisions under partial observation. The projects below are
ongoing. These summaries describe their questions and aims; public papers
and software are linked where available.

### Structural scores and scientific prediction

I am developing structural scores to assess predictions
against declared scientific constraints, including checks that can be made
before the outcome is observed. A forecast of a proportion, for example,
should respect its stated bounds.

The work asks how to report structural compliance alongside predictive
accuracy, and how to make the assumptions and limits of those checks clear.
Predictive scoring and structural evaluation address different questions:
passing a constraint check alone does not establish predictive skill or
scientific validity. Methods and companion software are in development.

{% include figure.liquid path="assets/img/research/structural_fidelity_comparison.svg" class="img-fluid rounded" zoomable=true alt="Constructed trajectories illustrate adherence to a declared prevalence bound. No predictive scores are computed; predictive scoring and structural checks answer separate evaluation questions." caption="Illustrative constructed trajectories; no predictive scores are computed." %}

[Vector PDF](/assets/img/research/structural_fidelity_comparison.pdf) · [All figure sources and downloads](/figures/)

### Inference and calibration

[op_infer](/projects/inference_calibration/) connects fitting tools,
simulation-based checks and replicated studies for incomplete or noisy observations.
The research software remains private, pre-alpha and unreleased while its scientific
applications are assessed.

### Scientific machine learning and incomplete data

I am exploring how scientific constraints can guide learning from sparse
observations of dynamical systems, with attention to the relationship between
reconstruction, uncertainty and scientific interpretation. This methodological
work is ongoing.

A related thread asks how many latent dimensions an incomplete dataset can
support. The released [VBPCApy](/projects/vbpca_py/) software provides Bayesian
dimensionality reduction; [pp-eigentest](/projects/pp_eigentest/) is ongoing
research on signal-rank selection, building on a
[2024 preprint](https://arxiv.org/abs/2409.12129).

### Application studies

**Dengue within-host dynamics.** Current work develops inference and model
assessment for viral and immune responses across successive infections and
their relationship to antibody-dependent enhancement. It builds on an
[earlier preprint](https://doi.org/10.1101/2023.08.29.555313).

**COVID-19 observation noise.** Controlled simulation studies examine how
assumptions about surveillance error affect inferred dynamics, predictive
uncertainty, and forecast assessment.

**Diphtheria outbreak vaccination.** Ongoing modeling compares the timing and
effects of response strategies under uncertain transmission and immunity.

**CCHF surveillance and control.** Cross-scale modeling investigates which
wildlife and livestock measurements inform disease risk and control choices,
alongside their field costs.

Working repositories remain private while the analyses mature. Public artifacts
will be added as they are released. See
[operational modeling](/operational-modeling/) for a separate account of my
contributions to ongoing forecasting and policy-support programs.
