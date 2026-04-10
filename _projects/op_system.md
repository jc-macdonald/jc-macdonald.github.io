---
layout: page
title: OP System
description: Declarative specification language and compiler for structured dynamical systems. Two specification pathways, multi-axis stratification, and compilation to validated bytecode closures.
img: assets/img/research/op_system_slide.png
importance: 3
category: "lead developer · in development"
github: https://github.com/ACCIDDA/op_system
---

**OP System** (Operator-Partitioned System) is a declarative specification language and compiler for structured dynamical systems. It serves as the specification layer of the operator-partitioned simulation stack, producing validated model objects consumed by [OP Engine](/projects/op_engine/) or other solvers.

Researchers define models through two declarative pathways:

- **Explicit governing equations** — state variables, parameters, and right-hand-side expressions written directly
- **Transition diagrams** — compartmental flows and rates that the compiler expands into governing equations

Both pathways support **multi-axis stratification** over categorical and continuous dimensions. The compiler performs automatic template expansion over axis products, chain synthesis for staged compartments (e.g., Erlang-distributed dwell times), and provides helper functions for aggregation and numerical quadrature.

Specifications are AST-validated and compiled to safe bytecode closures with restricted builtins. Structured metadata — axes, kernels, operators, and constraints — passes through to downstream solvers, enabling OP Engine to dispatch appropriate integration methods automatically.

The design eliminates the bookkeeping errors that arise when manually implementing large structured models (e.g., age×risk×vaccination-stratified epidemic models, trait-structured ecological models, or reaction-diffusion systems) and reduces the barrier to simulation of complex multi-physics systems.
