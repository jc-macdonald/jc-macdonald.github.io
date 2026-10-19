---
layout: page
title: vbpca-py
description: Bayesian dimensionality reduction for incomplete data, with posterior uncertainty and model-assessment tools.
img: assets/img/research/vbpca_py_schematic.svg
img_alt: Observed entries and a mask feed variational fitting of loadings, scores, bias, noise and ARD. The workflow includes convergence checks, component selection, held-out assessment and approximate posterior covariances.
importance: 1
category: "lead developer · released"
github: https://github.com/yoavram-lab/VBPCApy
related_publications: true
---

**vbpca-py** fits variational Bayesian PCA models to incomplete data. It estimates latent components, noise variance, and approximate posterior covariances for loadings, scores, and bias.

The package provides:

- Fitting to observed entries, with shared observation patterns used to reuse matrix factorizations.
- Automatic Relevance Determination for component pruning and sweeps for comparing candidate ranks.
- Predictive variance (`predictive_variance_`) that includes observation noise. Coverage needs assessment for the intended data and missingness pattern.
- Hyperparameter recommendations (`recommend_config`) derived from a surrogate-based simulation study. Rank recovery can differ outside the studied settings.
- Missing-aware preprocessing, including one-hot encoding, scaling, power transforms, and winsorization.
- C++ kernels through pybind11, with runtime autotuning for selected updates.
- A scikit-learn-compatible estimator API (`fit`, `transform`, `get_params`/`set_params`, cloning). Scikit-learn is an optional dependency.

Applied to genetic, cultural, and ecological datasets. Available on [PyPI](https://pypi.org/project/vbpca-py/) and archived at [Zenodo](https://doi.org/10.5281/zenodo.19389250).

The 2024 preprint {% cite macdonald2024vbpca %} introduced an earlier version of the posterior predictive rank-testing methodology built on this codebase. Follow-up [pp-eigentest](/projects/pp_eigentest/) research investigates signal-rank selection and its calibration for incomplete data; its methods and software remain in development.

{% include figure.liquid path="assets/img/research/vbpca_py_schematic.svg" class="img-fluid rounded" zoomable=true alt="Observed entries and a mask feed variational fitting of loadings, scores, bias, noise and ARD. The workflow includes convergence checks, component selection, held-out assessment and approximate posterior covariances." caption="VBPCApy missing-data workflow." %}

[Vector PDF](/assets/img/research/vbpca_py_schematic.pdf) · [All figure sources and downloads](/figures/)
