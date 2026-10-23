---
layout: page
title: vbpca-py
description: Find shared patterns in incomplete datasets and assess uncertainty in those summaries.
og_image: /assets/img/research/computed/incomplete_reconstruction.png
img: assets/img/research/previews/incomplete_reconstruction.svg
img_alt: A sample-by-feature heatmap of the reconstruction from an incomplete synthetic dataset. The VBPCA model uses a supplied count of two components.
importance: 4
category: "Released software"
github: https://github.com/yoavram-lab/VBPCApy
related_publications: true
last_modified_at: 2026-10-23
---

**vbpca-py** finds a smaller set of patterns that summarize an incomplete dataset. It fits variational Bayesian principal component analysis (PCA) to observed entries, estimating latent components, noise variance and approximate uncertainty in the fitted quantities.

{% assign release = site.data.software_releases.packages.vbpca_py %}
{% include software_release_status.liquid slug="vbpca_py" %} · [{{ release.docs_label }} and examples]({{ release.docs_url }})

The package provides missing-aware preprocessing, component pruning, comparisons of candidate ranks, fit diagnostics and a scikit-learn-style fitting interface. The fitted `scores_` array contains joint variational means for the training rows. `VBPCA.transform` instead computes conditional latent means for supplied rows, including new samples, and `transform_posterior` also returns conditional latent covariance matrices. Predictive variance includes observation noise, but these variational uncertainty approximations require coverage assessment for the intended data and missingness pattern.

The [2024 cultural-transmission paper](/publications/#macdonald2024austronesian) used this codebase. A [2024 preprint](https://arxiv.org/abs/2409.12129) introduced an earlier posterior predictive rank-testing method. Follow-up [pp-eigentest](/projects/pp_eigentest/) research studies signal-rank selection; its methods and software remain in development.

{% include figure.liquid path="assets/img/research/computed/incomplete_reconstruction.svg" class="img-fluid rounded" zoomable=true alt="A synthetic two-pattern signal, noisy observed entries with unobserved cells in gray, and a VBPCA reconstruction. Held-out observations are excluded from fitting. This illustration does not establish rank selection or uncertainty calibration." caption="A synthetic signal, noisy observed entries and reconstruction. Gray cells were excluded from fitting; the model uses two components." %}

[Computed example, inputs and checks](/software-examples/#incomplete-data)

[Method diagram (SVG)](/assets/img/research/vbpca_py_schematic.svg) · [Vector PDF](/assets/img/research/vbpca_py_schematic.pdf) · [All figure sources and downloads](/figures/)
