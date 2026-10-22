---
search: true
layout: page
title: Modeling in practice
permalink: /operational-modeling/
description: My contributions to infectious disease scenario projections, vaccination studies and the software used to run them.
nav: true
nav_order: 3
last_modified_at: 2026-10-22
---

## Scenario Modeling Hubs

Multi-model scenario projections produced by the Scenario Modeling Hubs contribute evidence used by the [CDC Center for Forecasting and Outbreak Analytics (CFA)](https://www.cdc.gov/forecast-outbreak-analytics/index.html) and public-health partners for planning, preparedness, and evaluation.

At the Atlantic Coast Center for Infectious Disease Dynamics and Analytics (ACCIDDA), I develop and maintain operational models for the Flu and COVID-19 Scenario Modeling Hubs and contribute to the computational infrastructure that supports multi-round scenario projections.

### Flu Scenario Modeling Hub

Lead model developer for ACCIDDA's influenza scenario projections.

- **2026/27 operational round.** Supervising an undergraduate student on revisions to the ACCIDDA flu model.
- **2025/26 operational round.** Led revisions to the ACCIDDA flu model.
- **2024/25 operational round.** Initial model development and pipeline integration.

[Hub repository](https://github.com/midas-network/flu-scenario-modeling-hub) · [Round results and reports](https://scenariomodelinghub.org/)

### COVID-19 Scenario Modeling Hub

Model development, fitting and scenario production for ACCIDDA's COVID-19 projections.

- **2026/27 Round 20.** Led the submission, including model development and calibration, migration to OP System and FlepiMoP2, scenario production and quality checks.
- **2025 health heterogeneities round.** Data cleaning, assimilation, and scenario analysis.

[Hub repository](https://github.com/midas-network/covid19-scenario-modeling-hub)

---

## Other Operational Work

### Hib Vaccination Modeling

I provide technical supervision for PhD students implementing an age- and immune-status-structured _Haemophilus influenzae_ type b (Hib) model. The study examines the effects of long-running vaccination programs in a partner-defined population and includes model fitting and policy analysis. Public descriptions remain general until the participating organizations approve more specific attribution.

### Diphtheria Outbreak Vaccination

I lead modeling analyses of outbreak-response vaccination strategies, including the interaction between surveillance, immunity and campaign timing. The working repository and partner-specific policy process remain private while the analysis matures.

---

## Infrastructure

This work informs development of [OP System](/projects/op_system/) for model specification, [OP Engine](/projects/op_engine/) for numerical simulation, and [FlepiMoP2](/projects/flepimop2/) for campaign execution. Separate providers connect the packages. Their requirements draw on the infectious disease modeling workflows described above.
