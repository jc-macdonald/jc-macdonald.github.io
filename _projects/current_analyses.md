---
layout: page
title: Research in progress
description: Ongoing work on structural scores, scientific machine learning and disease-modeling applications.
img: assets/img/research/structural_fidelity_comparison.svg
img_alt: Two constructed prevalence curves compared with an upper bound of one over the displayed horizon. One stays below the bound and the other crosses it; predictive accuracy is not evaluated.
importance: 1
category: "Research in progress"
last_modified_at: 2026-10-22
---

My current research asks what measurements reveal about a changing system,
how scientific assumptions affect predictions, and which data would help
answer a research or policy question. I use models of the underlying
processes, Bayesian inference and simulation studies. The projects below are
ongoing; public papers and software are linked where available.

## Structural scores and scientific prediction

I am developing structural scores to report whether a scientific prediction
satisfies stated constraints without using the outcome it is intended to
predict. Observations already available when the prediction is made may still
inform a check. A forecast of a proportion,
for example, should lie between zero and one.

The work examines how to report constraint compliance alongside predictive
accuracy, with explicit assumptions and limits. It distinguishes constraints
satisfied by construction from those observed to hold for a particular
prediction. Compliance alone does not establish predictive accuracy. The
methods and companion software remain in development.

{% include figure.liquid path="assets/img/research/structural_fidelity_comparison.svg" class="img-fluid rounded" zoomable=true alt="Two constructed prevalence curves compared with an upper bound of one over the displayed horizon. One stays below the bound and the other crosses it; predictive accuracy is not evaluated." caption="Illustrative constructed trajectories; no predictive scores are computed." %}

[Vector PDF](/assets/img/research/structural_fidelity_comparison.pdf) · [All figure sources and downloads](/figures/)

## Inference and calibration

[op_infer](/projects/inference_calibration/) connects fitting tools,
simulation-based checks and replicated studies for incomplete or noisy observations.
The codebase is public, pre-alpha and unreleased on PyPI while its scientific
applications are assessed. Application data and partner materials remain private.

## Scientific machine learning and incomplete data

I am studying representations of dynamical systems that satisfy selected
scientific constraints by construction. The work asks what sparse measurements
can reveal about a trajectory and which assumptions are needed to recover
scientific quantities from incomplete observations. Questions about
reconstruction accuracy, stability and uncertainty remain part of this ongoing
work.

A related thread asks how many underlying patterns can be distinguished from
noise in an incomplete dataset. The released [VBPCApy](/projects/vbpca_py/)
software provides Bayesian dimensionality reduction; [pp-eigentest](/projects/pp_eigentest/) is ongoing
research on signal-rank selection, building on a
[2024 preprint](https://arxiv.org/abs/2409.12129).

## Application studies

**Dengue within-host dynamics.** Current work develops inference and model
assessment for viral and immune responses across successive infections and
their relationship to antibody-dependent enhancement. It builds on an
[earlier preprint](https://doi.org/10.1101/2023.08.29.555313).

**COVID-19 observation noise.** Controlled simulation studies examine how
assumptions about surveillance error affect inferred dynamics, predictive
uncertainty, and forecast assessment.

**Diphtheria outbreak vaccination.** Ongoing modeling compares the timing and
effects of response strategies under uncertain transmission and immunity.

**Crimean-Congo hemorrhagic fever surveillance and control.** Modeling across
hosts and scales investigates which wildlife and livestock measurements inform
disease risk and control choices, alongside their field costs.

Working repositories remain private while the analyses mature. Public artifacts
will be added as they are released. See
[operational modeling](/operational-modeling/) for a separate account of my
contributions to ongoing forecasting and policy-support programs.
