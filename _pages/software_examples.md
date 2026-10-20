---
search: true
layout: page
title: Computed software examples
permalink: /software-examples/
description: Spatial fields, stochastic simulations, replicated comparisons and incomplete-data reconstruction using released packages.
nav: false
design_comparison: true
---

These examples use released versions of OP System, OP Engine, trade-study and
VBPCApy. All data are synthetic. The plots show computations rather than
findings from an application study; their captions state the assumptions and
what is checked.

[Python source](/assets/img/research/computed/computed_examples.py) ·
[Numerical inputs and outputs](/assets/img/research/computed/computed_data.json) ·
[Versions and artifact hashes](/assets/img/research/computed/provenance.json) ·
[Build notes](/assets/img/research/computed/README.md)

<nav class="page-links" aria-label="Computed examples">
  <a href="#spatial-diffusion">Spatial diffusion</a>
  <a href="#stochastic-transfers">Stochastic transfers</a>
  <a href="#replicated-designs">Design comparison</a>
  <a href="#incomplete-data">Incomplete data</a>
</nav>

## Spatial diffusion

OP System compiles a named-axis expression for a periodic diffusion stencil;
OP Engine integrates the resulting field with fourth-order Runge–Kutta (RK4).
The stencil is supplied explicitly on 64 equally spaced cells. Faster spatial variation fades sooner
than slower variation.

{% include figure.liquid path="assets/img/research/computed/spatial_diffusion.svg" class="img-fluid rounded" zoomable=true alt="A 64-cell periodic diffusion field and profiles at four times, computed from an OP System specification with RK4 integration in OP Engine. Spatial discretization is supplied explicitly; all inputs are synthetic." caption="A periodic spatial field at 121 output times and four selected profiles. The spatial mean is conserved." %}

The code checks the full trajectory against the exact Fourier-mode solution
of the **discrete spatial stencil**, with a maximum absolute difference below
`2e-10`. This measures temporal integration error for the chosen grid. It does
not measure error against a continuum PDE or establish accuracy for other
spatial discretizations.

[SVG](/assets/img/research/computed/spatial_diffusion.svg) · [PDF](/assets/img/research/computed/spatial_diffusion.pdf)

## Stochastic transfers

OP Engine runs 512 independent realizations of a two-state transfer process
using the exact stochastic simulation algorithm (SSA), with one event clock
per run. Each starts with 40 units; each remaining unit transfers at rate 0.6.
The example retains the accepted firing counts and checks conservation and
the correspondence between counts and transferred units.

{% include figure.liquid path="assets/img/research/computed/stochastic_ensemble.svg" class="img-fluid rounded" zoomable=true alt="512 independent exact stochastic transfer simulations, their empirical mean and pointwise 5th–95th percentile range, and the final distribution alongside analytic mean and binomial references. Synthetic demonstration." caption="Individual paths vary. The reference mean and final binomial distribution are known for this transfer process. The shaded range is pointwise variability across runs, not uncertainty in the estimated mean." %}

[SVG](/assets/img/research/computed/stochastic_ensemble.svg) · [PDF](/assets/img/research/computed/stochastic_ensemble.pdf)

## Replicated designs

trade-study evaluates ten sample-mean designs using 512 paired replicates.
The measurement standard deviation is either 1 or 1.5. The noisier measurement
is assigned a lower cost; the standard measurement has a fixed setup cost.
Those costs are illustrative assumptions. The circles mark designs for which
no alternative improves both mean error and assumed cost.

{% include figure.liquid path="assets/img/research/computed/replicated_tradeoff.svg" class="img-fluid rounded" zoomable=true alt="Ten synthetic sample-mean designs compared across 512 paired replicates. Nondominated mean error and assumed cost are marked, and empirical errors are compared with analytic variances. Costs are declared assumptions, not measured field costs." caption="Increasing the sample count reduces estimation error in this toy problem. The right panel compares the Monte Carlo estimates with the known variance of a sample mean." %}

The table reads the same generated data as the figure. Error estimates depend
on these 512 simulated replicates. A design is nondominated when no other
design is at least as good on both stated objectives and better on at least
one. Choosing a design for an application also requires preferences or
constraints relevant to that application.

{% include design_comparison.liquid %}

[CSV table](/assets/img/research/computed/design_comparison.csv) · [SVG](/assets/img/research/computed/replicated_tradeoff.svg) · [PDF](/assets/img/research/computed/replicated_tradeoff.pdf)

## Incomplete data

VBPCApy fits a two-component model to observed entries of a noisy synthetic
matrix. Roughly 35% of entries are withheld, shown in gray. The generating
signal uses two patterns; that choice is supplied to the fitted model.

{% include figure.liquid path="assets/img/research/computed/incomplete_reconstruction.svg" class="img-fluid rounded" zoomable=true alt="A synthetic two-pattern signal, noisy observed entries with unobserved cells in gray, and a VBPCA reconstruction. Held-out observations are excluded from fitting. This illustration does not establish rank selection or uncertainty calibration." caption="Left: generating signal. Middle: available noisy observations. Right: fitted reconstruction. All panels share a color scale." %}

The root mean squared reconstruction error on withheld noisy observations is
about 0.22 for this seeded example; the generating noise standard deviation is
0.2. This is one reconstruction check with a known component count. Choosing
the rank and assessing uncertainty calibration require separate studies.

[SVG](/assets/img/research/computed/incomplete_reconstruction.svg) · [PDF](/assets/img/research/computed/incomplete_reconstruction.pdf)

[Architecture diagrams and other figure downloads](/figures/)
