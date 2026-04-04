---
layout: page
title: OP System
description: Declarative governing equation specification compiler for structured dynamical systems. Transforms YAML model definitions into callable numerics.
img:
importance: 3
category: lead developer
github: https://github.com/ACCIDDA/op_system
---

**OP System** (Operator-Partitioned System) is a declarative specification compiler for structured dynamical systems. Users define governing equations, state variables, parameters, and operator partitions in YAML; the compiler transforms these into callable numerics consumed by [OP Engine](/projects/op_engine/) or other solvers.

The design eliminates the bookkeeping errors that arise when manually implementing large compartmental models (e.g., age-structured epidemic models with dozens of state variables) and reduces the barrier to simulation of complex structured models.
