---
layout: page
title: vbpca-py
description: Variational Bayesian PCA for incomplete data with full posterior uncertainty, automatic component pruning, native missingness handling, and C++-accelerated kernels.
img: assets/img/research/vbpca_py_schematic.png
importance: 1
category: "lead developer · released"
github: https://github.com/yoavram-lab/VBPCApy
related_publications: true
---

**vbpca-py** is a variational Bayesian PCA framework for incomplete data. It jointly infers latent components, noise variance, and effective dimensionality while propagating full posterior uncertainty (covariances on loadings, scores, and bias) through the entire estimation pipeline.

Key features:

- **Native per-entry missingness** handling via shared observation patterns that reuse matrix factorizations — no imputation required
- **Automatic Relevance Determination** prunes uninformative components; built-in model selection sweep identifies optimal rank
- **Missing-aware preprocessing pipeline**: one-hot encoding, scaling, power transforms, winsorization
- **C++-accelerated kernels** via pybind11 with runtime autotuning for performance-critical updates
- Full **scikit-learn estimator API** (`fit`, `transform`, `score`)

Applied to genetic, cultural, and ecological datasets. Available on [PyPI](https://pypi.org/project/vbpca-py/) and archived at [Zenodo](https://doi.org/10.5281/zenodo.19389250).

The companion paper {% cite macdonald2024vbpca %} develops the Bayesian rank estimation methodology using posterior predictive eigenvalue testing.
