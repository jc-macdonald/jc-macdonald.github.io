---
search: true
layout: page
title: Modeling in practice
permalink: /operational-modeling/
description: My contributions to infectious disease scenario projections, vaccination studies and the software used to run them.
nav: true
nav_order: 3
last_modified_at: 2026-10-26
---

## Scenario Modeling Hubs

Multi-model scenario projections produced by the Scenario Modeling Hubs contribute evidence used by the [CDC Center for Forecasting and Outbreak Analytics (CFA)](https://www.cdc.gov/forecast-outbreak-analytics/index.html) and public-health partners for planning, preparedness, and evaluation.

At the Atlantic Coast Center for Infectious Disease Dynamics and Analytics (ACCIDDA), I develop and maintain operational models for the Flu and COVID-19 Scenario Modeling Hubs and contribute to the computational infrastructure that supports multi-round scenario projections.

### Flu Scenario Modeling Hub

Lead model developer for ACCIDDA's influenza scenario projections.

- **2026/27 operational round.** Supervising an undergraduate student on revisions to the ACCIDDA flu model.
- **2025/26 operational round.** Led revisions to the ACCIDDA flu model.
- **2024/25 operational round.** Initial model development and pipeline integration.

<figure>
  <img src="/assets/img/research/operational/flu_scenario_projections.svg" alt="Two panels. Panel a shows projected weekly influenza hospitalizations in the United States over 43 weeks from August 2025 under three vaccination scenarios, with the no-vaccination scenario highest. Panel b shows box plots of season hospitalizations averted relative to no vaccination under usual and low coverage; both are positive, and usual coverage averts more. Details follow." width="720" height="317" loading="lazy">
  <figcaption>ACCIDDA's projections for Round 1 of the 2025–26 Flu Scenario Modeling Hub, plotted from the team's public submission. The round asked how vaccination would affect the coming season under three scenarios: business-as-usual coverage (A), low coverage (B) and a counterfactual with no vaccination (C). (a) Projected weekly influenza hospitalizations in the United States for 43 weeks from 10 August 2025: the median across 600 trajectories per scenario and the 5th to 95th percentile band. (b) Season hospitalizations averted relative to no vaccination, computed for each trajectory, since the hub pairs trajectories across scenarios. The medians are about 127 000 under usual coverage and 96 000 under low coverage; boxes show the interquartile range and whiskers extend to 1.5 times that range. These are one team's projections, conditional on the scenario assumptions. They are not forecasts, not the hub's multi-model ensemble and not an evaluation against the observed season. <a href="/figures/#operational-projections">Summary tables, source and provenance</a>.</figcaption>
</figure>

[Hub repository](https://github.com/midas-network/flu-scenario-modeling-hub) · [Round results and reports](https://scenariomodelinghub.org/)

### COVID-19 Scenario Modeling Hub

Model development, fitting and scenario production for ACCIDDA's COVID-19 projections.

- **2026/27 Round 20.** Led the submission, including model development and calibration, migration to OP System and FlepiMoP2, scenario production and quality checks.
- **2025 health heterogeneities round.** Data cleaning, assimilation, and scenario analysis.

[Hub repository](https://github.com/midas-network/covid19-scenario-modeling-hub)

---

## Other operational work

### Hib vaccination modeling

I provide technical supervision for PhD students implementing an age- and immune-status-structured _Haemophilus influenzae_ type b (Hib) model. The study examines the effects of long-running vaccination programs in a partner-defined population and includes model fitting and policy analysis. Public descriptions remain general until the participating organizations approve more specific attribution.

### Diphtheria outbreak vaccination

I lead modeling analyses of outbreak-response vaccination strategies, including the interaction between surveillance, immunity and campaign timing. The working repository and partner-specific policy process remain private while the analysis matures.

---

## Infrastructure

This work informs development of [OP System](/projects/op_system/) for model specification, [OP Engine](/projects/op_engine/) for numerical simulation, and [FlepiMoP2](/projects/flepimop2/) for campaign execution. Separate provider packages, with release cycles independent of the cores, connect compatible versions of OP System and OP Engine to FlepiMoP2. Their requirements draw on the infectious disease modeling workflows described above. These operational programs are an important application context; OP System and OP Engine are cross-domain numerical cores.
