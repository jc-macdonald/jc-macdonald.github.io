---
layout: page
title: vbpca-py
description: Find shared patterns in incomplete datasets and assess uncertainty in those summaries.
img: assets/img/research/computed/incomplete_reconstruction.svg
img_alt: A synthetic two-pattern signal, noisy observed entries with unobserved cells in gray, and a VBPCA reconstruction. Held-out observations are excluded from fitting. This illustration does not establish rank selection or uncertainty calibration.
importance: 1
category: "lead developer · released"
github: https://github.com/yoavram-lab/VBPCApy
related_publications: true
---

**vbpca-py** looks for a smaller set of patterns that summarize an incomplete dataset. It fits variational Bayesian principal component analysis (PCA) models to observed entries. It estimates latent components, noise variance, and approximate posterior covariances for loadings, scores, and bias.

The package provides:

- Fitting to observed entries, with shared observation patterns used to reuse matrix factorizations.
- Automatic Relevance Determination for component pruning and sweeps for comparing candidate ranks.
- Predictive variance (`predictive_variance_`) that includes observation noise. Coverage needs assessment for the intended data and missingness pattern.
- Hyperparameter recommendations (`recommend_config`) derived from a surrogate-based simulation study. Rank recovery can differ outside the studied settings.
- Missing-aware preprocessing, including one-hot encoding, scaling, power transforms, and winsorization.
- C++ kernels through pybind11, with runtime autotuning for selected updates.
- A scikit-learn-compatible estimator API (`fit`, `transform`, `get_params`/`set_params`, cloning). Scikit-learn is an optional dependency.

Applied to genetic, cultural, and ecological datasets. Available as a beta release on [PyPI](https://pypi.org/project/vbpca-py/) and archived at [Zenodo](https://doi.org/10.5281/zenodo.19389250).

The 2024 preprint {% cite macdonald2024vbpca %} introduced an earlier version of the posterior predictive rank-testing methodology built on this codebase. Follow-up [pp-eigentest](/projects/pp_eigentest/) research investigates signal-rank selection and its calibration for incomplete data; its methods and software remain in development.

{% include figure.liquid path="assets/img/research/computed/incomplete_reconstruction.svg" class="img-fluid rounded" zoomable=true alt="A synthetic two-pattern signal, noisy observed entries with unobserved cells in gray, and a VBPCA reconstruction. Held-out observations are excluded from fitting. This illustration does not establish rank selection or uncertainty calibration." caption="A synthetic signal, noisy observed entries and reconstruction. Gray cells were excluded from fitting; the model uses two components." %}

[Computed example, inputs and checks](/software-examples/#incomplete-data)

{% include figure.liquid path="assets/img/research/vbpca_py_schematic.svg" class="img-fluid rounded" zoomable=true alt="An illustrative masked data matrix feeds a variational low-rank model for latent scores, loadings, bias, noise and ARD priors. Model outputs branch to reconstruction/prediction and assessment. Covariances are approximate; coverage and rank recovery need checks for the intended data." caption="VBPCApy observed-data model." %}

[Vector PDF](/assets/img/research/vbpca_py_schematic.pdf) · [All figure sources and downloads](/figures/)
