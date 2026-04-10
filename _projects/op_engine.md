---
layout: page
title: OP Engine
description: Operator-partitioned ODE/PDE solver core with nine integration methods (explicit, IMEX, fully implicit), adaptive step-size control, and zero per-step allocation.
img: assets/img/research/op_engine_slide.png
importance: 2
category: "lead developer · in development"
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** (Operator-Partitioned Engine) is an operator-partitioned ODE/PDE solver core. It splits the right-hand side into an explicit nonlinear part and an optional stiff linear operator, then advances them jointly through a choice of nine integration methods:

- **Explicit**: Euler, Heun
- **IMEX** (implicit-explicit): Euler, Heun–trapezoidal, TR-BDF2
- **Fully implicit**: Euler, trapezoidal, BDF2, Rosenbrock-W2

Key design features:

- **Adaptive step-size control** with embedded error estimates
- **Zero per-step allocation** — all buffers pre-allocated at construction
- **Cached implicit solves** with dense/sparse autodispatch
- **Stage operator factories** for time- and state-dependent operators

Consumes model specifications and structured metadata from [OP System](/projects/op_system/) and serves as the forward-simulation backend for campaign orchestrators like FlepiMoP2.
