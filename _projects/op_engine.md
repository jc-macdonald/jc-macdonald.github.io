---
layout: page
title: OP Engine
description: Operator-partitioned solver for composing heterogeneous subsystem solvers (ODE, PDE, stochastic, hybrid) into a single time-stepping pipeline with pluggable backends.
img: assets/img/research/op_engine_slide.png
importance: 2
category: "lead developer · in development"
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** (Operator-Partitioned Engine) is an operator-partitioned solver that composes heterogeneous subsystem solvers — ODE, PDE, stochastic, and hybrid — into a single time-stepping pipeline. This enables fast, modular solving for stiff multi-physics problems by splitting the system into independently solvable operators. Framework-agnostic; separates state/time management (`ModelCore`) from stepping logic (`CoreSolver`).

Designed to consume model specifications produced by [OP System](/projects/op_system/) and serve as the forward-simulation backend for campaign orchestrators like FlepiMoP2.
