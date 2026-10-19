---
layout: page
title: vbpca-py
description: Variational Bayesian PCA for incomplete data with full posterior uncertainty, calibrated predictive variance, automatic component pruning, native missingness handling, and C++-accelerated kernels.
img: assets/img/research/vbpca_py_schematic.svg
img_alt: Observed entries and a mask feed variational fitting of loadings, scores, bias, noise and ARD. Convergence, component selection and held-out assessment support posterior prediction and uncertainty for the intended data regime.
importance: 1
category: "lead developer · released"
github: https://github.com/yoavram-lab/VBPCApy
related_publications: true
---

**vbpca-py** is a variational Bayesian PCA framework for incomplete data. It jointly infers latent components, noise variance, and effective dimensionality while propagating full posterior uncertainty (covariances on loadings, scores, and bias) through the entire estimation pipeline.

Key features:

- **Native per-entry missingness** handling via shared observation patterns that reuse matrix factorizations — no imputation required
- **Automatic Relevance Determination** prunes uninformative components; built-in model selection sweep identifies optimal rank
- **Calibrated predictive variance** (`predictive_variance_`) that folds in observation noise, restoring nominal prediction-interval coverage on noisy held-out entries
- **Regime-aware default hyperparameters** (`recommend_config`) distilled from a surrogate-based trade study, tuned to maximize correct rank recovery
- **Missing-aware preprocessing pipeline**: one-hot encoding, scaling, power transforms, winsorization
- **C++-accelerated kernels** via pybind11 with runtime autotuning for performance-critical updates
- Full **scikit-learn-compatible estimator API** (`fit`, `transform`, `get_params`/`set_params`, cloning) — scikit-learn is an optional dependency

Applied to genetic, cultural, and ecological datasets. Available on [PyPI](https://pypi.org/project/vbpca-py/) and archived at [Zenodo](https://doi.org/10.5281/zenodo.19389250).

The 2024 preprint {% cite macdonald2024vbpca %} introduced an earlier version of the posterior predictive rank-testing methodology built on this codebase. Follow-up [pp-eigentest](/projects/pp_eigentest/) research investigates signal-rank selection and its calibration for incomplete data; its methods and software remain in development.

{% include figure.liquid path="assets/img/research/vbpca_py_schematic.svg" class="img-fluid rounded" zoomable=true alt="Observed entries and a mask feed variational fitting of loadings, scores, bias, noise and ARD. Convergence, component selection and held-out assessment support posterior prediction and uncertainty for the intended data regime." caption="VBPCApy missing-data workflow." %}

[Vector PDF](/assets/img/research/vbpca_py_schematic.pdf) · [All figure sources and downloads](/figures/)
