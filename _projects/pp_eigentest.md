---
layout: page
title: pp-eigentest
description: Research on distinguishing underlying patterns from noise in incomplete data. Private alpha research software.
img: assets/img/research/pp_eigentest_schematic.svg
img_alt: Ongoing signal-rank research connects incomplete data, Bayesian latent-variable modeling, and assessment of signal and uncertainty. The methods and software remain in development.
importance: 3
category: "Research in progress"
---

**pp-eigentest** investigates how many underlying patterns can be distinguished
from noise in an incomplete dataset. This count is the signal rank. The work
uses Bayesian models and repeated simulated datasets to study posterior
predictive eigenvalue testing.

This is ongoing methods research with private alpha software. The current work
revises and extends the approach described in the
[2024 preprint](https://arxiv.org/abs/2409.12129), which is the public reference
for the earlier methodology. It is distinct from the released
[VBPCApy](/projects/vbpca_py/) package.

The research examines how missing observations, noise and modeling assumptions
affect rank selection. Current studies assess the reliability of those
decisions across incomplete-data settings. Public artifacts will be linked as
the work is released.

{% include figure.liquid path="assets/img/research/pp_eigentest_schematic.svg" class="img-fluid rounded" zoomable=true alt="Ongoing signal-rank research connects incomplete data, Bayesian latent-variable modeling, and assessment of signal and uncertainty. The methods and software remain in development." caption="Signal-rank research for incomplete data." %}

[Vector PDF](/assets/img/research/pp_eigentest_schematic.pdf) · [All figure sources and downloads](/figures/)
