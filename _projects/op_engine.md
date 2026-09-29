---
layout: page
title: OP Engine
description: Array-API-polymorphic ODE/PDE solver with portable numerical kernels and backend-native execution providers for explicit, IMEX, implicit, and stochastic integration.
img: assets/img/research/op_engine_slide.png
img_alt: OP Engine workflow connecting prepared models, numerical kernel families, backend-native providers, and execution diagnostics.
importance: 2
category: "lead developer · in development"
github: https://github.com/ACCIDDA/op_engine
---

**OP Engine** (Operator-Partitioned Engine) is an operator-partitioned ODE/PDE solver core. It splits the right-hand side into an explicit nonlinear part and an optional stiff linear operator, then advances them with explicit, IMEX, fully implicit, or stochastic methods.

The central design separates **portable model and numerical semantics** from **backend-native execution strategy**. A model is prepared once; NumPy, JAX, PyTorch, or compatible CuPy arrays select the numerical namespace at call time. Provider integrations add native control flow, compilation, checkpointing, schedule validation, and sparse-solver adaptation where the backend supports them.

Key design features:

- **NumPy:** broad eager support plus mutable, preallocated fast paths for selected methods
- **JAX:** `jit`/autodiff support, device-resident adaptive discovery for explicit methods, and frozen `lax.scan` replay
- **PyTorch:** eager fixed-step integration with autograd-preserving array operations
- **CuPy:** dense Array-API execution plus a tested sparse adapter; not every method/backend combination has parity
- **Prepared execution and structured state:** reusable plans, PyTrees, and block layouts reduce repeated setup work
- **Adaptive-schedule diagnostics:** local-error freshness checks detect when a recorded mesh should be rebuilt

For differentiable adaptive workflows, mesh discovery and numerical replay are deliberately separated. Gradients through a frozen replay are conditional on that recorded mesh, not on discrete step-size decisions. The schedule should therefore be refreshed after a failed accuracy diagnostic or a material parameter change.

OP Engine consumes model specifications and structured metadata from [OP System](/projects/op_system/) and serves as a forward-simulation backend for campaign orchestrators such as FlepiMoP2.
