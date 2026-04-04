---
layout: page
title: pp-eigentest
description: Posterior predictive eigenvalue testing for determining signal rank in covariance and Gram matrices. Supports ordered hypothesis testing with FWER and FDR control.
img:
importance: 4
category: software
---

**pp-eigentest** provides a posterior predictive framework for determining the number of significant eigenvalues (signal rank) in covariance and Gram matrices. The method generates posterior predictive null distributions for each ordered eigenvalue and tests whether observed eigenvalues exceed noise expectations.

Supports:
- Ordered hypothesis testing (sequential rejection)
- Family-wise error rate (FWER) control
- False discovery rate (FDR) control
- Integration with vbpca-py posterior output

In development; pre-release.
