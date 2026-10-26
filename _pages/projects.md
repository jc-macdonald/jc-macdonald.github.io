---
layout: page
title: Research and software
nav_title: Research
permalink: /projects/
description: The questions and study systems I work on, and the models and software I build to study them.
nav: true
nav_order: 4
last_modified_at: 2026-10-26
display_categories: ["Released software", "Research in progress", "Collaborative infrastructure"]
horizontal: false
---

I study how ecological and landscape change influences the movement and
connectivity of hosts, pathogens and cultural traits, and through them the
persistence and evolution of structured populations. The overarching interest is
landscape and metapopulation eco-evolutionary dynamics. My established work
addresses within- and between-host dynamics and cultural transmission, and
landscape-scale questions are a developing direction. Models, inference methods
and software are my tools for these questions, and they apply beyond these
systems.

<figure>
  <img src="/assets/img/research/cross_scale_systems.svg" alt="Four study systems arranged by scale, from within individuals to across populations, with published work marked by solid outlines and collaborative or unpublished work by dashed outlines. A chain links ecological and landscape change to movement and contact, connectivity among populations, and persistence, divergence and evolution. The research questions and study systems below describe each cell." width="1100" height="1044" loading="lazy">
  <figcaption>Study systems arranged by scale. Solid outlines mark systems with a published paper at that scale. Dashed outlines mark collaborative or unpublished work. A blank cell shows no work at that scale. The chain describes the direction of influence that frames the second research question below. <a href="/figures/">Figure downloads and editable source</a>.</figcaption>
</figure>

## Research questions

- **How do processes within hosts shape transmission and persistence?** My [buffalo studies](/publications/#macdonald2024fmdv) connect virus growth and immune response in individual animals to transmission between them, and a [carrier-transmission model](/publications/#atkins2026fmdcarrier), on which I am a co-author, extends this to persistent infection. As senior personnel on a multi-institution project linking cells to landscapes in African buffalo, I develop and parameterize the within-host models. The same within-host-to-population approach underlies my [dengue and Crimean-Congo hemorrhagic fever applications](/projects/current_analyses/#application-studies).
- **How do landscape, movement and contact shape spread, persistence and divergence across populations?** This is a developing direction. Published work relates [cultural variation to geography and language](/publications/#macdonald2024austronesian) among Austronesian-speaking societies, without modeling landscape change. Collaborative work in progress models Crimean-Congo hemorrhagic fever transmission between livestock and wildlife hosts, and spatial structure is a possible extension if movement data allow. A bighorn sheep project asks how immune phenotypes vary among metapopulations.
- **How should we measure, intervene and decide under uncertainty?** For Crimean-Congo hemorrhagic fever, I ask which wildlife and livestock measurements would change a surveillance or control decision, given their field costs. A developing extension asks the same question for managed and monitored populations, such as research colonies, hatcheries and monitored water bodies, where the records are often indirect (environmental samples, pooled tests, sentinel animals) and the quantity to control is a threshold. The models for these questions exist so far as small illustrative computations ([below](#which-records-would-tell)); no experimental or field study is under way. [Modeling in practice](/operational-modeling/) describes outbreak-response vaccination and respiratory-virus scenario work, and [trade-study](/projects/trade_study/) supports comparing study designs.

Earlier work includes a [COVID-19 model of testing, lockdown speed and fatigue across 55 U.S. jurisdictions](/publications/#macdonald2021covid), and theory on [hysteresis and Hopf bifurcation in a plankton model of harmful algal blooms](/publications/#macdonald2023npzd).

<figure>
  <img src="/assets/img/research/published/covid_lockdown_factor.svg" alt="Two panels on log axes: cumulative infections and peak prevalence against the lockdown rate factor. A line shows the paper's closed-form scaling; open markers show the closed form at each of 55 jurisdictions' published parameters and filled markers the model solved with each jurisdiction's published fatigue rate, joined by vertical segments. Details follow." width="720" height="403" loading="lazy">
  <figcaption>How the lockdown rate factor scales outbreak size, recomputed from <a href="/publications/#macdonald2021covid">Macdonald et al. (2021)</a>. In that model, susceptible people enter self-quarantine at a rate proportional to the force of infection, with proportionality constant ψ, and leave it at a fatigue rate. The paper's closed forms give the final size and the peak as the classical values multiplied by 1/(1 + ψ) when there is no fatigue. (a) Cumulative infections and (b) peak outbreak size, the maximum of <em>I</em>/<em>N</em>, against ψ: the closed form at the U.S. median <em>R</em><sub>0</sub> of 2.32 (line); the closed form at each of the 55 state and territorial jurisdictions' published <em>R</em><sub>0</sub> and ψ (open markers, Table 2 of the paper); and the model solved for 400 days from each jurisdiction's published initial infections with its published fatigue rate (filled markers, joined to the open marker). Fatigue returns quarantined people to circulation; in every jurisdiction the 400-day outcome is at or above its no-fatigue closed form, which the code asserts. Triangles identify fatigue half-lives under 15 days. The filled markers are 400-day model outcomes, not the paper's 31 May 2020 estimates and not necessarily final epidemic sizes. Recomputed from the model equations (public <a href="https://github.com/jc-macdonald/programfilesUSCOVID">code</a>) and the published parameter table; not copied from the paper. <a href="/figures/#published-model-computations">Figure downloads, data and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/npzd_hysteresis.svg" alt="Two panels from a published nutrient-phytoplankton-zooplankton-detritus (NPZD) plankton model. Panel a plots equilibrium phytoplankton against the maximum harmful effect of phytoplankton on zooplankton. Above a threshold the zooplankton-free state is locally stable and no coexistence equilibrium exists; below it a coexistence branch folds into an S shape, giving two stable coexistence states over an intermediate range. Panel b shows two simulations at a marked value in that range that differ only in initial zooplankton: low initial zooplankton leads to the high-phytoplankton state (circle) and high initial zooplankton to the low-phytoplankton state (square), with matching markers in panel a." width="720" height="368" loading="lazy">
  <figcaption>Forward hysteresis in the published nutrient-phytoplankton-zooplankton-detritus (NPZD) model (Macdonald and Gulbudak 2023). (a) Equilibria against the maximum harmful effect of phytoplankton on zooplankton. Coexistence equilibria exist only below the threshold at which the paper's zooplankton persistence number, labelled <i>P</i><sub>0</sub><sup>z</sup> in (a), equals one; above it, the zooplankton-free state is locally stable. At this threshold a coexistence branch bifurcates forward from the zooplankton-free state and folds twice, so two stable coexistence states exist over an intermediate range. Solid branches are locally stable; dashed and dotted branches are unstable. (b) Two simulations at the value marked in (a), differing only in initial zooplankton. With low initial zooplankton, phytoplankton settles at the high stable state (circle); with high initial zooplankton, it settles at the low stable state (square). The markers match those in (a), and faint dotted lines in (b) mark the two stable equilibria. Recomputed from the model equations with parameters from the paper; not copied from the paper. <a href="/figures/#published-model-computations">Figure downloads and source</a>.</figcaption>
</figure>

## Which records would tell

Two small computations illustrate the third question in its developing form.
Both use assumed parameters and plain NumPy; neither is fitted to data, and
neither reports a finding from an application study. The first recomputes a
published result; the second is an illustrative calculation from standard
estimator theory. They are here to show the kind of question, not to answer
it for any system.

<figure>
  <img src="/assets/img/research/siwr_reservoir_speed.svg" alt="Two panels of epidemic curves from a susceptible-infectious-reservoir model at a fixed reproduction number of 2.5, for transmission splits of 0, 50 and 90 percent through an environmental reservoir. In panel a the reservoir decays slowly and the three curves differ, peaking later and lower as the reservoir share rises. In panel b the reservoir decays quickly and the three curves coincide." width="720" height="351" loading="lazy">
  <figcaption>One reproduction number, two transmission routes. New infections per day per thousand hosts in a susceptible-infectious-reservoir model with basic reproduction number 2.5 and a five-day infectious period, for three splits of transmission between direct contact and a shared environmental reservoir. (a) With a slowly decaying reservoir (0.05 per day) the curves differ. (b) With a fast reservoir (5 per day) they coincide: case counts then determine only the sum of the two routes' contributions, not the split. This is the known fast-reservoir limit of the waterborne-pathogen model of <a href="https://doi.org/10.1007/s11538-010-9507-6">Tien and Earn (2010)</a>, whose identifiability consequences were shown by <a href="https://doi.org/10.1016/j.jtbi.2012.12.021">Eisenberg, Robertson and Tien (2013)</a>; the figure recomputes it. Assumed parameters; no inference is performed. <a href="/figures/#model-computations">Figure downloads and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/record_type_precision.svg" alt="Two panels. Panel a shows one simulated epidemic growing exponentially, recorded as an environmental signal every two days with noise and as daily reported counts at one percent reporting. Panel b shows the standard error of the estimated growth rate against days of data for the environmental signal, with simulation checks as circles, and for Poisson counts at ten, one and one tenth of a percent reporting; the environmental curve crosses the one percent counts curve near forty days." width="720" height="325" loading="lazy">
  <figcaption>Growth-rate precision from two kinds of record. (a) One simulated epidemic growing at 0.08 per day from fifty infections per day, recorded as an environmental signal (incidence convolved with a shedding kernel, sampled every two days, log-normal noise with standard deviation 0.5) and as daily reported counts with one percent reporting. (b) Standard error of the estimated growth rate against days of data: the least-squares slope of the log environmental signal (closed form; circles are 800 simulations) and the large-sample standard error of a Poisson-regression slope for counts at three reporting fractions. Both standard errors follow from standard estimator theory (<a href="https://doi.org/10.1007/978-1-4899-3242-6">McCullagh and Nelder 1989</a>; for epidemic growth rates, <a href="https://doi.org/10.1007/s11538-013-9918-2">Ma, Dushoff, Bolker and Earn 2014</a>). The comparison itself is an illustrative calculation, not a published result; wastewater-based estimates of epidemic growth are compared with case-based estimates in practice by, for example, <a href="https://doi.org/10.1289/EHP10050">Huisman and colleagues (2022)</a>. Which record is more precise depends on the reporting fraction and the record length. Detection time is a separate question and is not shown. Assumed values. <a href="/figures/#model-computations">Figure downloads and source</a>.</figcaption>
</figure>

## Study systems

- **Foot-and-mouth disease virus in African buffalo.** A first-author within-host model and a co-authored carrier-transmission model, developed with collaborators in the Jolles Lab and a multi-institution project.

<figure>
  <img src="/assets/img/research/published/fmdv_within_host.svg" alt="Four panels recomputed from the published within-host foot-and-mouth disease model: viral load and adaptive response over thirty days for three strains at median parameters, strain transmission rate against replication rate, and per-host infectious period against adaptive activation rate. Details follow." width="720" height="605" loading="lazy">
  <figcaption>Within-host dynamics and their link to transmission, recomputed from <a href="/publications/#macdonald2024fmdv">Macdonald et al. (2024)</a>. (a) Blood viral load and (b) adaptive immune response over 30 days from the published within-host model at each strain's median parameters (medians over the 10 000 Monte Carlo estimates per strain released with the paper's <a href="https://github.com/jc-macdonald/FMDV-Fitting-Bootstrap">code</a>). For the viral-load curves in (a), this recomputation gives SAT1 the highest and earliest peak, SAT2 the lowest and SAT3 the latest; in (b), SAT1 rises first, SAT2 next and SAT3 last to the lowest plateau. Because the released strain summaries do not contain each host's minimum haptoglobin, the innate inflow term approximates it with the strain-median initial innate value. (c) The transmission rate estimated per strain in the paper against the host-median viral replication rate, with the host range as a bar: both increase from SAT3 to SAT2 to SAT1. (d) Infectious period against adaptive activation rate across the 12 experimentally infected hosts, from the paper's released host table (Spearman ρ = −0.77). The paper's conclusions about strain differences in the immune response rest on the fitted per-host parameters and data, which these median-parameter curves illustrate but do not test. Recomputed from the model equations and released parameters; not copied from the paper, and not a fit to data. <a href="/figures/#published-model-computations">Figure downloads, data and source</a>.</figcaption>
</figure>
- **Crimean-Congo hemorrhagic fever virus in livestock and wildlife.** Collaborative transmission models and surveillance design; modeling in progress.
- **Human cultural transmission.** Published analysis of networks and clusters of cultural traits, with a methods [preprint](/publications/#preprints) on incomplete cultural data.
- **Bighorn sheep immune ecology.** Collaborative analysis in progress.

## Methods and software

The projects below provide software for these questions and describe ongoing
methods research. OP System, OP Engine, op_infer and trade-study are
general-purpose tools for dynamical systems and study comparison; their scope
is not limited to infectious disease or public health. Health, ecological,
environmental and social systems provide applications of the same underlying
methods.

The pages keep three kinds of status separate. **Lifecycle** labels say whether
software is released or still in development. **Evidence** labels identify the
support: linked publications, operational work, executable software or explicitly
identified work in progress. **Example type** says whether an illustration uses observed,
synthetic or constructed inputs. None of these labels, by itself, establishes
scientific validity for a new application.

Two further questions concern methods.

- **What can we learn from incomplete data?** My [cultural transmission research](/publications/#macdonald2024austronesian) uses statistical summaries of cultural traits. [VBPCApy](/projects/vbpca_py/) and [signal-rank research](/projects/pp_eigentest/) develop tools for incomplete datasets.
- **How should we assess models and compare studies?** [Current methods research](/projects/current_analyses/) examines scientific constraints and inference. The [replicated design example](/software-examples/#replicated-designs) shows a synthetic comparison of estimation error and assumed cost.

The software packages can be used independently or in combination.

### OP stack design and verification examples

The stack separates three choices that many modelling tools fix at design
time: the array library, the model class and the solver family. The examples
below show each separation on a synthetic model with an independent check.
Every figure reports software behavior within the packages' documented scope,
not a finding about a study system. Numerical inputs and outputs, package
versions and artifact hashes are retained with the
[stack examples](/assets/img/research/stack/README.md); the examples are
recomputed and compared in continuous integration.

**The array library is chosen at call time.** [OP System](/projects/op_system/)
compiles a validated, declarative description (equations or hazard-style
transitions, with named axes for groups, space and traits) into one evaluator.
The array library is selected from the inputs, so the same compiled model runs
under NumPy, under JAX, and, within the documented qualified scope, under
PyTorch. The numerical method does not change with the namespace.

<figure>
  <img src="/assets/img/research/stack/stack_backend_parity.svg" alt="Two-panel synthetic chemostat example comparing trajectories with an adaptive reference and showing final errors under NumPy, JAX and PyTorch at two precisions. Details follow." width="720" height="317" loading="lazy">
  <figcaption>One compiled model under three array libraries. (a) A six-state nutrient, producer and grazer chemostat written as hazard-style transitions, compiled once and integrated with fixed-step fourth-order Runge-Kutta through OP Engine; open markers are an adaptive high-order reference (SciPy DOP853, relative tolerance 10<sup>−12</sup>). (b) Error at the final time against that reference. Because the same method performs the same arithmetic in each namespace, eager evaluation under NumPy, JAX and PyTorch is bit-identical at each precision in this run (1.26 × 10<sup>−8</sup> in float64, 4.63 × 10<sup>−6</sup> in float32), and the code asserts that equality. Traced once under <code>jax.jit</code>, which may fuse and reorder operations, the float64 error differs from the eager value only at the 10<sup>−15</sup> level. The dotted and dash-dot lines are machine epsilon for each precision, drawn as references; the error of a 400-step integration is well above epsilon, as expected. Synthetic model, assumed parameters. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

A model written for one run can then be evaluated over a parameter grid, or
differentiated with respect to a parameter, without being rewritten.

<figure>
  <img src="/assets/img/research/stack/stack_batched_ensemble.svg" alt="Two-panel synthetic chemostat ensemble showing a two-parameter grid of final producer values and the median and percentile band over time. Details follow." width="720" height="317" loading="lazy">
  <figcaption>A parameter ensemble by <code>jax.vmap</code> over the same compiled evaluator. (a) Producer concentration at the final time over a 45 × 45 grid of two parameters (producer growth rate and inflow nutrient), from one vectorized call; the marker is the nominal pair. (b) The 2025 members over time: median and 5th to 95th percentile band, with a separately computed eager NumPy run at the nominal parameters overlaid. A vectorized JAX evaluation at the nominal pair agrees with that NumPy run to within 10<sup>−9</sup> maximum absolute difference. No timing is shown; single-call wall-clock values are recorded in the data file with the CPU model for the record only, since single calls without repetitions are not a benchmark. Synthetic model, assumed parameters. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/stack/stack_gradient.svg" alt="Two-panel derivative check showing a model output with its local autodiff tangent, and finite-difference disagreement against step size. Details follow." width="720" height="317" loading="lazy">
  <figcaption>Differentiating a model output through the fixed-step solver. (a) Producer concentration at the final time as a function of the producer growth-rate parameter, with the local tangent at the nominal value from <code>jax.grad</code> through 400 fixed Runge-Kutta steps over the compiled evaluator. (b) Central finite differences of the same discrete 400-step calculation approach the autodiff derivative with slope 2 as the step shrinks, reaching 1.3 × 10<sup>−10</sup> relative disagreement before round-off dominates. This checks the derivative of the discrete solver, not continuous-time sensitivity, and it covers the engine's fixed-step methods; the adaptive step controller is not a traced path, as the package documentation states. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

**One solver surface for several model classes.** [OP Engine](/projects/op_engine/)
takes compiled models into explicit and adaptive ordinary-differential-equation
methods, operator-split and implicit schemes for partial differential equations,
exact stochastic simulation with retained event counts, tau-leaping and
steady-state solves. Specification and numerics stay separate: the compiler
publishes interface contracts, and the engine owns time integration; the user
supplies any spatial discretization.

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
  <figcaption>Equilibria by vectorized steady-state solves. For the bistable model <em>x</em>′ = <em>a</em> + <em>x</em> − <em>x</em>³, the engine's pseudo-transient steady-state solver is mapped over 121 values of <em>a</em> with <code>jax.vmap</code> from two starting guesses; with early exit disabled, each solve is a fixed-length traced loop. These are independent solves at each parameter value, not continuation along a branch. Every state with a true convergence flag lies within 10<sup>−6</sup> of a root of the cubic; states with a false flag occur only where the branch being sought does not exist past a fold, and they are omitted from the plot. The unstable branch is drawn from the cubic's roots as a reference. A one-state toy chosen for its closed-form check; it is not the published plankton model shown earlier on this page. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

**Qualification is part of the tooling.** Backend qualification tables in the
packages state which methods are tested under which array libraries. Model
authors can compare a compiled right-hand side against independently written
equations. The checks in the figures above (an adaptive reference, finite
differences, exact conservation identities, an analytic solution, polynomial
roots) are the kind of check the tooling is built to make routine; the simplest
form, a fixed-step method against a closed-form solution in two precisions, is
in the [figure gallery](/figures/#model-computations).

**Each layer is a separate package with its own release and evidence.**
[FlepiMoP2](/projects/flepimop2/) runs campaigns over the cores,
[trade-study](/projects/trade_study/) compares replicated designs, and
[op_infer](/projects/inference_calibration/) (in development) adds inference
adapters and calibration checks. Projects use the layers they need. Layered
designs exist elsewhere, for example in the symbolic modelling and
differential-equation ecosystems of Julia; the OP stack makes the same
separation in Python's Array API ecosystem. The stage labels in the
[software guide](#software-guide) describe maturity, not validity.

<nav class="page-links" aria-label="Project sections">
  <a href="#research-questions">Research questions</a>
  <a href="#which-records-would-tell">Which records would tell</a>
  <a href="#study-systems">Study systems</a>
  <a href="#methods-and-software">Methods and software</a>
  <a href="#op-stack-design-and-verification-examples">The OP stack</a>
  <a href="#released-software">Released software</a>
  <a href="#research-in-progress">Research in progress</a>
  <a href="#collaborative-infrastructure">Collaborative infrastructure</a>
  <a href="#software-guide">Software guide</a>
</nav>

<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <h2 id="{{ category | slugify }}" class="category">{{ category }}</h2>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  {% assign project_columns = 2 %}
  {% if sorted_projects.size == 3 %}{% assign project_columns = 3 %}{% endif %}
  <!-- Generate cards for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-{{ project_columns }}">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>

## Software guide

The labels below describe software development stage and availability. They do
not establish numerical accuracy or scientific validity for a particular use.
Package availability and the linked evidence were last reviewed on 23 October 2026.

{% include software_table.liquid %}

[Computed examples and comparison table](/software-examples/) · [Public source repositories](/repositories/)
