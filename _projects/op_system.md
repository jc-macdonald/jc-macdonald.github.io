---
layout: page
title: OP System
description: Restricted expression language and compiler for structured dynamical systems, lowering model specifications through typed IR to vectorized, Array-API-polymorphic code.
img: assets/img/research/op_system_slide.png
img_alt: OP System compiler workflow from equations or transition diagrams through validation, typed intermediate representation, and portable evaluators.
importance: 3
category: "lead developer · in development"
github: https://github.com/ACCIDDA/op_system
---

**OP System** (Operator-Partitioned System) is a declarative specification language and compiler for structured dynamical systems. It serves as the specification layer of the operator-partitioned simulation stack, producing validated model objects consumed by [OP Engine](/projects/op_engine/) or other solvers.

Researchers define models through two declarative pathways:

- **Explicit governing equations** — state variables, parameters, and right-hand-side expressions written directly
- **Transition diagrams** — compartmental flows and rates that the compiler expands into governing equations

Both pathways support **multi-axis stratification** over categorical and continuous dimensions. The compiler performs automatic template expansion over axis products, chain synthesis for staged compartments (e.g., Erlang-distributed dwell times), and provides helper functions for aggregation and numerical quadrature.

Specifications pass through a restricted expression parser, typed intermediate representation, and vectorized AST/code-object compiler with restricted builtins. Structured metadata — axes, state layouts, kernels, operators, reactions, routing, and constraints — passes through to downstream solvers. The same compiled right-hand side runs with NumPy or JAX arrays and supports PyTorch autograd without a separate model-compilation path. Flat, block, and PyTree state layouts allow the representation to match the execution provider.

The design eliminates the bookkeeping errors that arise when manually implementing large structured models (e.g., age×risk×vaccination-stratified epidemic models, trait-structured ecological models, or reaction-diffusion systems) and reduces the barrier to simulation of complex multi-physics systems.
