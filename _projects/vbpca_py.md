---
layout: page
title: vbpca-py
description: Variational Bayesian PCA for incomplete data with native missing-data handling, uncertainty quantification, and C++-accelerated kernels. scikit-learn compatible.
img:
importance: 1
category: lead developer
github: https://github.com/yoavram-lab/VBPCApy
related_publications: true
---

**vbpca-py** implements variational Bayesian principal component analysis with first-class support for missing data. The algorithm jointly infers latent components, noise variance, and effective dimensionality while propagating uncertainty through the entire estimation pipeline.

Key features:
- Native MCAR/MAR/MNAR missing-data handling without imputation
- Automatic relevance determination for component selection
- C++-accelerated dense and sparse masked kernels via pybind11
- Full scikit-learn estimator API (`fit`, `transform`, `score`)
- Uncertainty quantification on all latent quantities

Available on [PyPI](https://pypi.org/project/vbpca-py/) and archived at [Zenodo](https://doi.org/10.5281/zenodo.19389250).

The companion paper {% cite macdonald2024vbpca %} develops the Bayesian rank estimation methodology using posterior predictive eigenvalue testing.
