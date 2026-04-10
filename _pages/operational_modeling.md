---
layout: page
title: operational modeling
permalink: /operational-modeling/
description: Operational infectious disease forecasting and scenario modeling for CDC-CFA and the Scenario Modeling Hubs.
nav: true
nav_order: 4
---

## Scenario Modeling Hubs

Multi-model scenario projections produced by the Scenario Modeling Hubs are used by the [CDC Center for Forecasting and Outbreak Analytics (CFA)](https://www.cdc.gov/forecast-outbreak-analytics/) and the [Advisory Committee on Immunization Practices (ACIP)](https://www.cdc.gov/acip/) to inform vaccine policy and pandemic preparedness decisions.

I develop and maintain ACCIDDA's operational models for the Flu and COVID-19 Scenario Modeling Hubs and contribute to the computational infrastructure that supports multi-round scenario projections.

### Flu Scenario Modeling Hub

Lead model developer for ACCIDDA's influenza scenario projections.

- **2026/27 operational round** — supervising an undergraduate student in a scientific overhaul of the ACCIDDA flu model
- **2025/26 operational round** — leading scientific overhaul of the ACCIDDA flu model
- **2024/25 operational round** — initial model development and pipeline integration

[Hub repository](https://github.com/midas-network/flu-scenario-modeling-hub) · [Round results and reports](https://scenariomodelinghub.org/)

### COVID-19 Scenario Modeling Hub

Data assimilation and modeling support for ACCIDDA's COVID-19 projections.

- **2025 health heterogeneities round** — data cleaning, assimilation, and scenario analysis

[Hub repository](https://github.com/midas-network/covid19-scenario-modeling-hub)

---

## Other Operational Work

### Hib Vaccination Modeling (Navajo Nation)

Technical supervisor for an age- and immune-status-structured _Haemophilus influenzae_ type b (Hib) model evaluating the impact of long-running vaccination programs in the Navajo Nation. Managing PhD students through model implementation, calibration, and policy analysis.

---

## Infrastructure

This operational work directly informs the development of [FlepiMoP2](/projects/flepimop2/), [OP Engine](/projects/op_engine/), and [OP System](/projects/op_system/), which compose into a declarative modeling stack: researchers specify models via [OP System](/projects/op_system/)'s specification language, the compiler produces validated model objects consumed by [OP Engine](/projects/op_engine/)'s operator-partitioned solver, and [FlepiMoP2](/projects/flepimop2/) orchestrates batch scenario campaigns. This stack will serve as the modeling infrastructure for the 2026/27 flu round, the COVID-19 round, and the RSV round.
