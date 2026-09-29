---
layout: page
title: pp-eigentest
description: Private pre-release work on posterior-predictive signal-rank selection, centered on a sequential fitted-model selector with explicit calibration and stopping diagnostics.
img: assets/img/research/pp_eigentest_schematic.png
importance: 3
category: "lead developer · in development"
---

**pp-eigentest** is a posterior predictive eigenvalue testing framework for determining signal rank in high-dimensional datasets. The current manuscript and analysis plan centers a **sequential fitted-model rank selector** with explicit calibration and stopping diagnostics.

Earlier ensemble/consensus approaches are retained as supplementary negative results rather than presented as the primary method. The strongest external comparator is still being finalized, so the manuscript is not yet ready for submission.

NumPy is the reference implementation. JAX is opt-in, and the C++ path is selected only when runtime measurement shows a benefit. Sparse inputs are accepted behind memory guards but are materialized for dense spectral computation; they are not a separate sparse computational backend.

In development as a private pre-release companion to [arXiv:2409.12129](https://arxiv.org/abs/2409.12129). A public source release is planned with the methods paper.
