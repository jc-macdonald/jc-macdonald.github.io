---
search: true
layout: page
title: Computed software examples
permalink: /software-examples/
description: Checked synthetic demonstrations from released packages and public pre-alpha op_infer.
nav: false
last_modified_at: 2026-10-26
design_comparison: true
---

The first four examples use released versions of OP System, OP Engine,
trade-study and VBPCApy. The fifth is an imported, commit-pinned artifact from
public pre-alpha op_infer; it does not imply a package release. A final section
shows design and verification examples for OP System and OP Engine.
All data are synthetic. The plots show computations rather than findings from
an application study; their captions state the assumptions and what is checked.

[Python source](/assets/img/research/computed/computed_examples.py) ·
[Numerical inputs and outputs](/assets/img/research/computed/computed_data.json) ·
[Versions and artifact hashes](/assets/img/research/computed/provenance.json) ·
[Build notes](/assets/img/research/computed/README.md)

{% include computed_versions.liquid %}

<nav class="page-links" aria-label="Computed examples">
  <a href="#spatial-diffusion">Spatial diffusion</a>
  <a href="#stochastic-transfers">Stochastic transfers</a>
  <a href="#replicated-designs">Design comparison</a>
  <a href="#incomplete-data">Incomplete data</a>
  <a href="#inference-calibration">Inference calibration</a>
  <a href="#op-stack-design-and-verification">OP stack design and verification</a>
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

## Inference calibration

op_infer evaluates one Normal-model fixture for which the posterior density is
available analytically. The left panel compares 1,024 seeded draws from that
fixture with the exact posterior density. The right panel summarizes randomized-rank
probability-integral-transform values from 64 simulation-based calibration (SBC)
replicates.

{% include figure.liquid path="assets/img/research/computed/op_infer_normal_sbc.svg" class="img-fluid rounded" zoomable=true alt="An exact Normal posterior density overlaid on 1,024 analytic-fixture draws, beside a histogram of randomized-rank PIT values from 64 SBC replicates." caption="A checked analytic fixture and an intentionally small SBC bank. Sixty-four replicates are underpowered and are not evidence that inference is calibrated." %}

The fixture completed all 64 requested replicates without a failed attempt. Its
recorded gate label is `underpowered pass`: the implementation and accounting
checks passed, but the replicate count is below the prespecified power floor.
The histogram is therefore a software demonstration, not a calibration
certificate or application result.

[Retained data](/assets/img/research/computed/op_infer_normal_sbc/data.json) ·
[Summary](/assets/img/research/computed/op_infer_normal_sbc/summary.txt) ·
[Upstream manifest](/assets/img/research/computed/op_infer_normal_sbc/manifest.json) ·
[Pinned source identity](/assets/img/research/computed/op_infer_normal_sbc/source.json) ·
[SVG](/assets/img/research/computed/op_infer_normal_sbc.svg) ·
[PDF](/assets/img/research/computed/op_infer_normal_sbc.pdf)

## OP stack design and verification

These examples show design choices of [OP System](/projects/op_system/) and
[OP Engine](/projects/op_engine/) on synthetic models, each with an independent
check. They use released OP System 0.10.0 and OP Engine 0.9.1 with JAX and CPU
PyTorch. Every figure reports software behavior within the packages' documented
scope, not a finding about a study system. The
[research page](/projects/#how-the-op-stack-compares) compares the stack with
related tools.

[Python source and pinned dependencies](/assets/img/research/stack/stack_examples.py) ·
[Numerical inputs and outputs](/assets/img/research/stack/stack_data.json) ·
[Versions and artifact hashes](/assets/img/research/stack/provenance.json) ·
[Build notes](/assets/img/research/stack/README.md)

**The array library is chosen at call time.** OP System compiles a validated,
declarative description (equations or hazard-style transitions, with named axes
for groups, space and traits) into one evaluator. The array library is selected
from the inputs, so the same compiled model runs under NumPy, under JAX and,
within the documented qualified scope, under PyTorch. The numerical method does
not change with the namespace.

<figure>
  <img src="/assets/img/research/stack/stack_backend_parity.svg" alt="Two-panel synthetic chemostat example comparing trajectories with an adaptive reference and showing final errors under NumPy, JAX and PyTorch at two precisions. Details follow." width="720" height="317" loading="lazy">
  <figcaption>One compiled model under three array libraries. (a) A six-state nutrient, producer and grazer chemostat written as hazard-style transitions, compiled once and integrated with fixed-step fourth-order Runge-Kutta through OP Engine; open markers are an adaptive high-order reference (SciPy DOP853, relative tolerance 10<sup>−12</sup>). (b) Error at the final time against that reference. Because the same method performs the same arithmetic in each namespace, eager evaluation under NumPy, JAX and PyTorch is bit-identical at each precision in this run (1.26 × 10<sup>−8</sup> in float64, 4.63 × 10<sup>−6</sup> in float32), and the code asserts that equality. Traced once under <code>jax.jit</code>, which may fuse and reorder operations, the float64 error differs from the eager value only at the 10<sup>−15</sup> level. The dotted and dash-dot lines are machine epsilon for each precision, drawn as references; the error of a 400-step integration is well above epsilon, as expected. Synthetic model, assumed parameters. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

**Model authors can check a compiled model.** OP System's qualification report
compares a compiled right-hand side with equations the author writes
independently, under each array library and precision, and records optional
balance checks with their stated conditions.

<figure>
  <img src="/assets/img/research/stack/stack_qualification.svg" alt="Two panels. Panel a shows the largest relative disagreement between a compiled age-by-place model and independently written equations under NumPy, JAX and PyTorch, near ten to the minus fifteen in float64 and a few times ten to the minus six in float32. Panel b shows that a copy with a transposed contact matrix passes the population balance check but fails the comparison with independent equations. Details follow." width="720" height="317" loading="lazy">
  <figcaption>Checking a compiled model against independently written equations. A susceptible-infectious-recovered model with three age groups in four places, with an asymmetric contact matrix for mixing within each place and movement between places, is compiled once from a configuration specification. OP System's qualification report compares the compiled right-hand side with the same model written cell by cell in plain Python at three test states, in the flat and structured layouts. (a) The largest relative disagreement under NumPy, JAX and PyTorch is between 2 × 10<sup>−15</sup> and 1 × 10<sup>−14</sup> in float64 and between 7 × 10<sup>−7</sup> and 5 × 10<sup>−6</sup> in float32, within the report's relative tolerances of 10<sup>−7</sup> and 10<sup>−5</sup>. (b) The same checks on a copy whose contact matrix is indexed the wrong way round. Every population total is still conserved, so the balance check passes (residual 3 × 10<sup>−14</sup>); the comparison with independent equations fails, with relative disagreement between 0.17 and 16. Agreement at selected states is not a proof for all parameter values, and the check does not assess the accuracy of a time integrator. Synthetic model, assumed parameters. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

**A model written for one run can be batched or differentiated.** The same
compiled evaluator can be mapped over a parameter grid or differentiated with
respect to a parameter without being rewritten.

<figure>
  <img src="/assets/img/research/stack/stack_batched_ensemble.svg" alt="Two-panel synthetic chemostat ensemble showing a two-parameter grid of final producer values and the median and percentile band over time. Details follow." width="720" height="317" loading="lazy">
  <figcaption>A parameter ensemble by <code>jax.vmap</code> over the same compiled evaluator. (a) Producer concentration at the final time over a 45 × 45 grid of two parameters (producer growth rate and inflow nutrient), from one vectorized call; the marker is the nominal pair. (b) The 2025 members over time: median and 5th to 95th percentile band, with a separately computed eager NumPy run at the nominal parameters overlaid. A vectorized JAX evaluation at the nominal pair agrees with that NumPy run to within 10<sup>−9</sup> maximum absolute difference. No timing is shown; single-call wall-clock values are recorded in the data file with the CPU model for the record only, since single calls without repetitions are not a benchmark. Synthetic model, assumed parameters. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/stack/stack_gradient.svg" alt="Two-panel derivative check showing a model output with its local autodiff tangent, and finite-difference disagreement against step size. Details follow." width="720" height="317" loading="lazy">
  <figcaption>Differentiating a model output through the fixed-step solver. (a) Producer concentration at the final time as a function of the producer growth-rate parameter, with the local tangent at the nominal value from <code>jax.grad</code> through 400 fixed Runge-Kutta steps over the compiled evaluator. (b) Central finite differences of the same discrete 400-step calculation approach the autodiff derivative with slope 2 as the step shrinks, reaching 1.3 × 10<sup>−10</sup> relative disagreement before round-off dominates. This checks the derivative of the discrete solver, not continuous-time sensitivity, and it covers the engine's fixed-step methods; the adaptive step controller is not a traced path, as the package documentation states. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

**One specification, several solvers.** OP Engine takes compiled models into
explicit and adaptive ordinary-differential-equation methods, operator-split and
implicit schemes for partial differential equations, exact stochastic
simulation with retained event counts, tau-leaping and steady-state solves. The
compiler publishes interface contracts, and the engine owns time integration;
the user supplies any spatial discretization.

<figure>
  <img src="/assets/img/research/stack/stack_spec_to_ssa.svg" alt="Two-panel synthetic SIRS example comparing deterministic prevalence with 256 direct-SSA paths and showing mean cumulative event counts. Details follow." width="720" height="331" loading="lazy">
  <figcaption>One transition specification, two solvers. A susceptible-infectious-recovered model with waning immunity (400 hosts) is written once with a declared replicate axis; the compiler verifies that no reaction crosses replicates, which lets the batched direct stochastic simulation algorithm give every replicate its own event clock. The direct SSA generates exact draws from the specified continuous-time Markov jump process; "exact" refers to that process, not to the ODE or to any disease. (a) 256 paths against the deterministic solution of the same specification. Finite-population extinction is visible: in this seeded sample 26.2% of paths have no infectious hosts at the final time, and the median sits below the deterministic second wave. (b) Mean cumulative events per path from the retained firing counts. Two identities hold exactly, by array equality, on every path: the total population is constant, and the state equals the initial state plus the stoichiometry matrix times the cumulative counts. Illustrative parameters. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/stack/stack_spatial_convergence.svg" alt="Two-panel heat-equation verification comparing a 16-interval finite-difference solution with the analytic solution and showing maximum error over five meshes. Details follow." width="720" height="317" loading="lazy">
  <figcaption>Convergence of a supplied spatial operator to an analytic solution. The heat equation on [0, 1] with zero boundary values and a sine initial condition has the closed-form solution sin(πx) exp(−Dπ²t). A centred finite-difference operator is supplied explicitly and compiled as a named-axis contraction; OP Engine integrates it in time with a step small enough that spatial error dominates. (a) The exact and computed solutions at <em>t</em> = 0.5 on 16 mesh intervals (15 interior unknowns). (b) Maximum error against the exact solution over five meshes, with fitted order 2.00. Checking against a known solution, rather than against another solver, is the standard verification practice for numerical codes (<a href="https://doi.org/10.1115/1.1436090">Roache 2002</a>). <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/stack/stack_steady_states.svg" alt="Cubic-model bifurcation diagram showing two stable branches from vectorized solves, the unstable branch from the polynomial roots, and the interval with two stable states. Details follow." width="720" height="442" loading="lazy">
  <figcaption>Equilibria by vectorized steady-state solves. For the bistable model <em>x</em>′ = <em>a</em> + <em>x</em> − <em>x</em>³, the engine's pseudo-transient steady-state solver is mapped over 121 values of <em>a</em> with <code>jax.vmap</code> from two starting guesses; with early exit disabled, each solve is a fixed-length traced loop. These are independent solves at each parameter value, not continuation along a branch. Every state with a true convergence flag lies within 10<sup>−6</sup> of a root of the cubic; states with a false flag occur only where the branch being sought does not exist past a fold, and they are omitted from the plot. The unstable branch is drawn from the cubic's roots as a reference. A one-state toy chosen for its closed-form check; it is not the published plankton model on the <a href="/projects/">research page</a>. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

[Architecture diagrams and other figure downloads](/figures/)
