---
layout: page
title: pp-eigentest
description: Posterior predictive eigenvalue testing for signal rank determination. Three-layer consensus architecture with FWER and FDR control; NumPy, C++, JAX, and sparse backends.
img: assets/img/research/pp_eigentest_schematic.png
importance: 3
category: "lead developer · in development"
github: https://github.com/yoavram-lab/pp-eigentest
---

**pp-eigentest** is a posterior predictive eigenvalue testing framework for determining signal rank in high-dimensional datasets. It uses an INID bootstrap over Gram spectra as the null model and tests eigenvalue ratios via a **three-layer consensus architecture**:

1. **Dimensionality heuristics** — parallel analysis variants, adjacent ratio/gap statistics, calibrated thresholds
2. **Adaptive thresholding** — data-driven cutoffs that adjust to spectral structure
3. **Multiple testing correction** — fixed-sequence FWER, Holm step-down, Benjamini–Hochberg FDR

Supports **NumPy, C++, JAX** (GPU-accelerated), and **sparse** backends. The rank-selection logic is model-agnostic: it consumes posterior mean/variance summaries from any generative engine — [vbpca-py](/projects/vbpca_py/), probabilistic PCA, or an empirical-Bayes Gaussian model — rather than depending on one specific upstream model.

In development; pre-release. Source at [yoavram-lab/pp-eigentest](https://github.com/yoavram-lab/pp-eigentest).
