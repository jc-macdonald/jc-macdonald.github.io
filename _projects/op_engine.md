---
layout: page
title: OP Engine
description: Lightweight multiphysics solver core for time-dependent systems. Supports explicit ODE solvers and IMEX/operator-splitting schemes for PDE-like models with pluggable backends.
img: assets/img/research/op_engine_slide.png
importance: 2
category: "lead developer · in development"
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** (Operator-Partitioned Engine) is a lightweight multiphysics solver core for time-dependent systems. The engine supports explicit ODE solvers and IMEX/operator-splitting schemes for PDE-like models, enabling composition of fast subsystem solvers for stiff multi-physics problems. Framework-agnostic; separates state/time management (`ModelCore`) from stepping logic (`CoreSolver`).

Designed to consume model specifications produced by [OP System](/projects/op_system/) and serve as the forward-simulation backend for campaign orchestrators like FlepiMoP2.
