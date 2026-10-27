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

- **How do processes within hosts shape transmission and persistence?** My [buffalo studies](/publications/#macdonald2024fmdv) of three foot-and-mouth disease virus strains (SAT-1, -2 and -3) indicate that viral replication rate correlates with transmission among buffalo and that the adaptive immune activation rate determines the infectious period. A [carrier-transmission model](/publications/#atkins2026fmdcarrier), on which I am a co-author, extends this to persistent infection. As senior personnel on a multi-institution project linking cells to landscapes in African buffalo, I develop and parameterize the within-host models. The SAT serotypes, for which African buffalo are a wildlife host, have recently spread beyond sub-Saharan Africa. SAT-1 was reported for the first time in nine countries from Egypt to Mongolia in 2025 and 2026, including Cyprus, and again in Greece, Lebanon and Türkiye after sixty years ([WOAH, August 2026](https://www.woah.org/en/article/the-spread-of-fmd-to-new-areas-is-concerning-but-consequences-could-be-worse/)). The buffalo estimates describe infection in buffalo; transmission in cattle and small ruminants was not studied. The same within-host-to-population approach underlies my [dengue and Crimean-Congo hemorrhagic fever applications](/projects/current_analyses/#application-studies).
- **How do landscape, movement and contact shape spread, persistence and divergence across populations?** This is a developing direction. Published work relates [cultural variation to geography and language](/publications/#macdonald2024austronesian) among Austronesian-speaking societies, without modeling landscape change. Collaborative work in progress models Crimean-Congo hemorrhagic fever transmission between livestock and wildlife hosts, and spatial structure is a possible extension if movement data allow. The range of this virus's main vectors is changing. _Hyalomma_ ticks are endemic in, or have been detected at least once in, 40 European countries ([Parvage et al. 2025](https://doi.org/10.1186/s13071-025-07104-3)), and Spain reported two locally acquired human cases by July 2026 ([ECDC](https://cchf-weekly.ecdc.europa.eu/)). A bighorn sheep project asks how immune phenotypes vary among metapopulations.
- **How should we measure, vaccinate and decide under uncertainty?** For Crimean-Congo hemorrhagic fever, I ask which wildlife and livestock measurements would change a surveillance or control decision, given their field costs. [Modeling in practice](/operational-modeling/) describes outbreak-response vaccination and respiratory-virus scenario work, and [trade-study](/projects/trade_study/) supports comparing study designs.

<figure>
  <img src="/assets/img/research/published/fmdv_within_host.svg" alt="Four panels recomputed from the published within-host foot-and-mouth disease model: viral load and adaptive response over thirty days for three strains at median parameters, strain transmission rate against replication rate, and per-host infectious period against adaptive activation rate. Details follow." width="720" height="605" loading="lazy">
  <figcaption>Within-host dynamics and their link to transmission, recomputed from <a href="/publications/#macdonald2024fmdv">Macdonald et al. (2024)</a>. (a) Blood viral load and (b) adaptive immune response over 30 days from the published within-host model at each strain's median parameters (medians over the 10 000 Monte Carlo estimates per strain released with the paper's <a href="https://github.com/jc-macdonald/FMDV-Fitting-Bootstrap">code</a>). For the viral-load curves in (a), this recomputation gives SAT-1 the highest and earliest peak, SAT-2 the lowest and SAT-3 the latest; in (b), SAT-1 rises first, SAT-2 next and SAT-3 last to the lowest plateau. Because the released strain summaries do not contain each host's minimum haptoglobin, the innate inflow term approximates it with the strain-median initial innate value. (c) The transmission rate estimated per strain in the paper against the host-median viral replication rate, with the host range as a bar: both increase from SAT-3 to SAT-2 to SAT-1. (d) Infectious period against adaptive activation rate across the 12 experimentally infected hosts, from the paper's released host table (Spearman ρ = −0.77). The paper's conclusions about strain differences in the immune response rest on the fitted per-host parameters and data, which these median-parameter curves illustrate but do not test. Recomputed from the model equations and released parameters; not copied from the paper, and not a fit to data. <a href="/figures/#published-model-computations">Figure downloads, data and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/published/ehs_delta_scores.svg" alt="Two panels. Panel a shows per-culture delta scores, a measure of how far cultural distances depart from a tree, for religion, social organisation and subsistence among Austronesian-speaking societies; religion has the highest scores and subsistence the lowest. Panel b shows the recomputed scores against the scores released with the paper, lying on the line of equality." width="720" height="331" loading="lazy">
  <figcaption>Relative tree-likeness of three cultural classes, recomputed from <a href="/publications/#macdonald2024austronesian">Macdonald et al. (2024)</a>. The δ-score (<a href="https://doi.org/10.1093/oxfordjournals.molbev.a004030">Holland et al. 2002</a>) measures how far the pairwise distances among each set of four cultures depart from a tree. A low score indicates a tree-like network, mostly owing to vertical transmission, and a high score a less tree-like network, probably owing to non-vertical transmission or parallel evolution. (a) The δ-score of each culture, computed from the pairwise cultural distance matrices released with the paper's <a href="https://github.com/yoavram-lab/Cultural-Clusters-and-Networks">code</a>, for religion (137 cultures, from Pulotu) and for social organisation and subsistence (130 cultures each, from the Ethnographic Atlas in D-PLACE). The class means are 0.32, 0.25 and 0.22, as reported in the paper, so religion is less tree-like than social organisation and subsistence. (b) Each recomputed score against the SplitsTree output released with the paper; the largest difference is 3.5 × 10<sup>−4</sup>. Recomputed from the released distances; not copied from the paper. <a href="/figures/#published-model-computations">Figure downloads, data and source</a>.</figcaption>
</figure>

Earlier work includes a [COVID-19 model of testing, lockdown speed and fatigue across 55 U.S. jurisdictions](/publications/#macdonald2021covid), and theory on [hysteresis and Hopf bifurcation in a plankton model of harmful algal blooms](/publications/#macdonald2023npzd).

<figure>
  <img src="/assets/img/research/published/covid_lockdown_factor.svg" alt="Two panels on log axes: cumulative infections and peak prevalence against the lockdown rate factor. A line shows the paper's closed-form scaling; open markers show the closed form at each of 55 jurisdictions' published parameters and filled markers the model solved with each jurisdiction's published fatigue rate, joined by vertical segments. Details follow." width="720" height="403" loading="lazy">
  <figcaption>How the lockdown rate factor scales outbreak size, recomputed from <a href="/publications/#macdonald2021covid">Macdonald et al. (2021)</a>. In that model, susceptible people enter self-quarantine at a rate proportional to the force of infection, with proportionality constant ψ, and leave it at a fatigue rate. The paper's closed forms give the final size and the peak as the classical values multiplied by 1/(1 + ψ) when there is no fatigue. (a) Cumulative infections and (b) peak outbreak size, the maximum of <em>I</em>/<em>N</em>, against ψ: the closed form at the U.S. median <em>R</em><sub>0</sub> of 2.32 (line); the closed form at each of the 55 state and territorial jurisdictions' published <em>R</em><sub>0</sub> and ψ (open markers, Table 2 of the paper); and the model solved for 400 days from each jurisdiction's published initial infections with its published fatigue rate (filled markers, joined to the open marker). Fatigue returns quarantined people to circulation; in every jurisdiction the 400-day outcome is at or above its no-fatigue closed form, which the code asserts. Triangles identify fatigue half-lives under 15 days. The filled markers are 400-day model outcomes, not the paper's 31 May 2020 estimates and not necessarily final epidemic sizes. Recomputed from the model equations (public <a href="https://github.com/jc-macdonald/programfilesUSCOVID">code</a>) and the published parameter table; not copied from the paper. <a href="/figures/#published-model-computations">Figure downloads, data and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/npzd_hysteresis.svg" alt="Two panels from a published nutrient-phytoplankton-zooplankton-detritus (NPZD) plankton model. Panel a plots equilibrium phytoplankton against the maximum harmful effect of phytoplankton on zooplankton. Above a threshold the zooplankton-free state is locally stable and no coexistence equilibrium exists; below it a coexistence branch folds into an S shape, giving two stable coexistence states over an intermediate range. Panel b shows two simulations at a marked value in that range that differ only in initial zooplankton: low initial zooplankton leads to the high-phytoplankton state (circle) and high initial zooplankton to the low-phytoplankton state (square), with matching markers in panel a." width="720" height="368" loading="lazy">
  <figcaption>Forward hysteresis in the published nutrient-phytoplankton-zooplankton-detritus (NPZD) model (Macdonald and Gulbudak 2023). (a) Equilibria against the maximum harmful effect of phytoplankton on zooplankton. Coexistence equilibria exist only below the threshold at which the paper's zooplankton persistence number, labelled <i>P</i><sub>0</sub><sup>z</sup> in (a), equals one; above it, the zooplankton-free state is locally stable. At this threshold a coexistence branch bifurcates forward from the zooplankton-free state and folds twice, so two stable coexistence states exist over an intermediate range. Solid branches are locally stable; dashed and dotted branches are unstable. (b) Two simulations at the value marked in (a), differing only in initial zooplankton. With low initial zooplankton, phytoplankton settles at the high stable state (circle); with high initial zooplankton, it settles at the low stable state (square). The markers match those in (a), and faint dotted lines in (b) mark the two stable equilibria. Recomputed from the model equations with parameters from the paper, which agree with the paper's public <a href="https://github.com/jc-macdonald/NPZBifurcationAndBlooms">code</a>; not copied from the paper. <a href="/figures/#published-model-computations">Figure downloads and source</a>.</figcaption>
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

### How the OP stack compares

[OP System](/projects/op_system/) and [OP Engine](/projects/op_engine/) bring to
Python the separation of model specification from numerical method that
[odin2 and dust2](https://mrc-ide.github.io/odin2/) provide in R and that
[Catalyst](https://docs.sciml.ai/Catalyst/stable/) and ModelingToolkit provide in
Julia. A specification is configuration rather than code, so a scenario
pipeline can validate it before a run. It is compiled once, and the array
library (NumPy, JAX or PyTorch) is chosen when the model is called, so the same
model can be evaluated over a parameter grid or differentiated without being
rewritten. Model authors can compare a compiled model with equations they write
independently. The same specifications run in operational scenario projections
through [FlepiMoP2](/projects/flepimop2/) and in research analyses.

<figure>
  <img src="/assets/img/research/stack/stack_backend_parity.svg" alt="Two-panel synthetic chemostat example comparing trajectories with an adaptive reference and showing final errors under NumPy, JAX and PyTorch at two precisions. Details follow." width="720" height="317" loading="lazy">
  <figcaption>One compiled model under three array libraries. (a) A six-state nutrient, producer and grazer chemostat written as hazard-style transitions, compiled once and integrated with fixed-step fourth-order Runge-Kutta through OP Engine; open markers are an adaptive high-order reference (SciPy DOP853, relative tolerance 10<sup>−12</sup>). (b) Error at the final time against that reference. Because the same method performs the same arithmetic in each namespace, eager evaluation under NumPy, JAX and PyTorch is bit-identical at each precision in this run (1.26 × 10<sup>−8</sup> in float64, 4.63 × 10<sup>−6</sup> in float32), and the code asserts that equality. Traced once under <code>jax.jit</code>, which may fuse and reorder operations, the float64 error differs from the eager value only at the 10<sup>−15</sup> level. The dotted and dash-dot lines are machine epsilon for each precision, drawn as references; the error of a 400-step integration is well above epsilon, as expected. Synthetic model, assumed parameters. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

<figure>
  <img src="/assets/img/research/stack/stack_qualification.svg" alt="Two panels. Panel a shows the largest relative disagreement between a compiled age-by-place model and independently written equations under NumPy, JAX and PyTorch, near ten to the minus fifteen in float64 and a few times ten to the minus six in float32. Panel b shows that a copy with a transposed contact matrix passes the population balance check but fails the comparison with independent equations. Details follow." width="720" height="317" loading="lazy">
  <figcaption>Checking a compiled model against independently written equations. A susceptible-infectious-recovered model with three age groups in four places, with an asymmetric contact matrix for mixing within each place and movement between places, is compiled once from a configuration specification. OP System's qualification report compares the compiled right-hand side with the same model written cell by cell in plain Python at three test states, in the flat and structured layouts. (a) The largest relative disagreement under NumPy, JAX and PyTorch is between 2 × 10<sup>−15</sup> and 1 × 10<sup>−14</sup> in float64 and between 7 × 10<sup>−7</sup> and 5 × 10<sup>−6</sup> in float32, within the report's relative tolerances of 10<sup>−7</sup> and 10<sup>−5</sup>. (b) The same checks on a copy whose contact matrix is indexed the wrong way round. Every population total is still conserved, so the balance check passes (residual 3 × 10<sup>−14</sup>); the comparison with independent equations fails, with relative disagreement between 0.17 and 16. Agreement at selected states is not a proof for all parameter values, and the check does not assess the accuracy of a time integrator. Synthetic model, assumed parameters. <a href="/figures/#op-stack-demonstrations">Figure downloads, data and source</a>.</figcaption>
</figure>

For several needs another tool is the better choice. The table states where
the stack fits and where another tool does more.

| Need                                                                                                          | Established tools                                                                                                               | The OP stack                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Reaction networks run as ordinary differential equations, stochastic differential equations or jump processes | [Catalyst](https://docs.sciml.ai/Catalyst/stable/) (Julia); [GillesPy2](https://github.com/StochSS/GillesPy2) and PySB (Python) | Ordinary differential equations, exact stochastic simulation and tau-leaping from one specification; no chemical Langevin equations |
| Adaptive, differentiable solves in JAX                                                                        | [Diffrax](https://docs.kidger.site/diffrax/)                                                                                    | Derivatives through fixed-step methods only; the adaptive step controller is not traced                                             |
| Epidemic models written in a domain-specific language, with particle filters and Markov chain Monte Carlo     | [odin2, dust2 and monty](https://mrc-ide.github.io/odin2/) (R)                                                                  | Python and Array API based; the inference layer, [op_infer](/projects/inference_calibration/), is in development                    |
| Agent-based or renewal-equation models                                                                        | [Starsim and LASER](https://www.idmod.org/tools/); [PyRenew](https://github.com/CDCgov/PyRenew) and EpiNow2                     | Not provided; the stack covers population-level compartmental, spatial and reaction-network models                                  |

Five further examples (a parameter ensemble by vectorization, a derivative
through the solver, deterministic and exact stochastic runs of one
specification, spatial convergence to an analytic solution, and vectorized
steady-state solves) are on the
[computed examples page](/software-examples/#op-stack-design-and-verification),
with their checks and limits. Each layer of the stack is a separate package
with its own release and evidence. [trade-study](/projects/trade_study/)
compares replicated designs, and [op_infer](/projects/inference_calibration/)
(in development) adds inference adapters and calibration checks. The stage
labels in the [software guide](#software-guide) describe maturity, not
validity.

<nav class="page-links" aria-label="Project sections">
  <a href="#research-questions">Research questions</a>
  <a href="#study-systems">Study systems</a>
  <a href="#methods-and-software">Methods and software</a>
  <a href="#how-the-op-stack-compares">The OP stack</a>
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
