---
layout: page
title: OP Engine
description: Numerical simulation engine for mechanistic models of biological and epidemiological systems. Supports ODE, PDE, and hybrid operator-splitting solvers with pluggable backends.
img:
importance: 2
category: software
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** (Operator-Partitioned Engine) provides a modular numerical simulation backend for structured dynamical systems. The engine supports ODE and PDE solvers with operator-splitting schemes (IMEX, Strang, Lie--Trotter), enabling composition of fast subsystem solvers for stiff multi-physics problems.

Designed to consume model specifications produced by [OP System](/projects/op_system/) and serve as the forward-simulation backend for campaign orchestrators like FlepiMoP2.
