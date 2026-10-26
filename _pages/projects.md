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

Earlier theoretical work examined [hysteresis and Hopf bifurcation in a plankton model of harmful algal blooms](/publications/#macdonald2023npzd).

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

### What sets the OP stack apart

Many modelling tools fix one array library, one model class or one solver
family when they are designed. The OP stack separates these choices and makes
each of them explicit.

- **One specification, compiled once, with the array library chosen at call time.** [OP System](/projects/op_system/) compiles a validated, declarative description (equations or hazard-style transitions, with named axes for groups, space and traits) into a single evaluator. The array library is selected from the inputs: the same compiled model runs under NumPy, under JAX with just-in-time compilation, vectorization and automatic differentiation, and, within the documented qualified scope, under PyTorch with autograd. A model written for one deterministic run can be batched over a parameter grid, differentiated for inference or moved to an accelerator without being rewritten.
- **One solver surface for several model classes.** [OP Engine](/projects/op_engine/) takes the same compiled model into explicit and adaptive ordinary-differential-equation methods, operator-split and implicit schemes for partial differential equations, exact stochastic simulation with retained event counts, tau-leaping and steady-state continuation. Specification and numerics stay separate: the compiler publishes interface contracts, and the engine owns discretization and integration.
- **Qualification is part of the tooling, not an afterthought.** Backend qualification tables state which methods are tested under which array libraries. Model authors can compare a compiled right-hand side against independently written equations. Benchmarks separate preprocessing, compilation and warm evaluation so that a timing can be read correctly. The figure below shows the simplest form of such a check.
- **Each layer is a separate package with its own release and evidence.** [FlepiMoP2](/projects/flepimop2/) runs campaigns over the cores, [trade-study](/projects/trade_study/) compares replicated designs, and [op_infer](/projects/inference_calibration/) (in development) adds inference adapters and calibration checks. Projects use the layers they need.

Layered designs of this kind exist elsewhere, for example in the symbolic
modelling and differential-equation ecosystems of Julia. The OP stack makes the
same separation in Python's Array API ecosystem, with the backend chosen at call
time and qualification recorded per method and per backend. The stage labels in
the [software guide](#software-guide) describe maturity, not validity.

<figure>
  <img src="/assets/img/research/rk4_known_solution.svg" alt="Two panels. Panel a shows logistic growth from 0.05 to 1 over twenty time units with eight fixed Runge-Kutta steps marked on the exact curve. Panel b plots absolute error at the final time against the number of steps on log axes for float64 and float32. Both fall along a slope of minus four, then float32 flattens near one part in ten million after about forty steps and rises with more steps, while float64 flattens near one part in ten to the fifteenth after a few thousand steps." width="720" height="343" loading="lazy">
  <figcaption>Truncation and round-off against a known solution. A fixed-step fourth-order Runge-Kutta method applied to logistic growth, whose solution is known in closed form, in float64 and float32. (a) The problem and eight steps of the method. (b) Absolute error at the final time against the number of steps. The error falls as the fourth power of the step size (dotted reference, slope −4) until round-off takes over; the floor is near 10<sup>−7</sup> for float32 after about forty steps and near 10<sup>−16</sup> for float64, and beyond the floor the error grows with the number of steps. Comparing against an exact solution rather than against another solver separates integration error from floating-point error. The trade-off is textbook material (<a href="https://doi.org/10.1007/978-3-540-78862-1">Hairer, Nørsett and Wanner</a>; <a href="https://doi.org/10.1137/1.9780898718027">Higham 2002</a>), and checking a code against a known or manufactured solution is standard verification practice (<a href="https://doi.org/10.1115/1.1436090">Roache 2002</a>). The computation is plain NumPy; it shows the kind of check the stack's qualification tools are meant to make routine and is not a result about those tools. <a href="/figures/#model-computations">Figure downloads and source</a>.</figcaption>
</figure>

<nav class="page-links" aria-label="Project sections">
  <a href="#research-questions">Research questions</a>
  <a href="#which-records-would-tell">Which records would tell</a>
  <a href="#study-systems">Study systems</a>
  <a href="#methods-and-software">Methods and software</a>
  <a href="#what-sets-the-op-stack-apart">The OP stack</a>
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
