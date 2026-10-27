---
search: true
layout: page
title: Research figures
permalink: /figures/
last_modified_at: 2026-10-26
description: Computed examples, method diagrams and editable sources for research figures.
nav: false
---

The computed figures below use public synthetic data. Five use released
software; the op_infer fixture is imported from a pinned public pre-alpha
commit and does not imply a release. Each links to its assumptions, checks and
full multi-panel version. The method diagrams, four published-model computations,
seven OP stack demonstrations, an operational projection and constructed
illustrations follow in separate sections. Figures carry axis labels and legends only; the setting,
assumptions and attribution for each are in the caption beside it.

<nav class="page-links" aria-label="Figure sections">
  <a href="#computed-examples">Computed examples</a>
  <a href="#method-and-software-diagrams">Method diagrams</a>
  <a href="#published-model-computations">Published-model computations</a>
  <a href="#op-stack-demonstrations">OP stack demonstrations</a>
  <a href="#operational-projections">Operational projections</a>
  <a href="#constructed-illustrations">Constructed illustrations</a>
</nav>

## Computed examples

{% include figure_gallery.liquid figures=site.data.research_figures.computed base='assets/img/research/computed/' computed=true %}

[Python source and pinned dependencies](/assets/img/research/computed/computed_examples.py) · [Numerical data](/assets/img/research/computed/computed_data.json) · [CSV comparison table](/assets/img/research/computed/design_comparison.csv) · [Assumptions and checks](/software-examples/)

## Method and software diagrams

TikZ sources accompany the SVG and PDF exports. Connections show relationships
between components; they do not prescribe one execution order. Capability and
qualification details remain in the corresponding package documentation.

{% include figure_gallery.liquid figures=site.data.research_figures.diagrams base='assets/img/research/' tikz=true %}

## Published-model computations

Figures in this section are recomputed from my first-author papers, using the
published model equations with parameters from the papers or their released
public code, or the data released with a paper. They
illustrate a published qualitative result; they are not copied from the paper,
and their numerical values belong to the recomputation.

{% include figure_gallery.liquid figures=site.data.research_figures.published_models base='assets/img/research/' %}

[Python source for the NPZD computation](/assets/img/research/gen_research_figures.py) · [Build and scope notes](/assets/img/research/README.md)

{% include figure_gallery.liquid figures=site.data.research_figures.published_recomputations base='assets/img/research/published/' %}

[Python source for the FMDV, COVID-19 and Austronesian recomputations](/assets/img/research/published/published_models.py) · [Input tables, numerical outputs and provenance](/assets/img/research/published/README.md)

## OP stack demonstrations

Each figure shows one design choice of the OP stack on a synthetic model with
an independent check, using released OP System 0.10.0 and OP Engine 0.9.1 with
JAX and CPU PyTorch. No timings are plotted; single-call wall-clock values are
retained in the data file with the CPU model for the record. The
[computed examples page](/software-examples/#op-stack-design-and-verification)
states what each figure supports and its limits.

{% include figure_gallery.liquid figures=site.data.research_figures.stack base='assets/img/research/stack/' %}

[Python source and pinned dependencies](/assets/img/research/stack/stack_examples.py) · [Numerical inputs and outputs](/assets/img/research/stack/stack_data.json) · [Versions and artifact hashes](/assets/img/research/stack/provenance.json) · [Checks and limits](/assets/img/research/stack/README.md)

## Operational projections

This figure plots a public submission to a Scenario Modeling Hub by the team I
work with at ACCIDDA. It shows one team's projections under the round's
scenario assumptions; it is not a forecast or an evaluation against observed
data.

{% include figure_gallery.liquid figures=site.data.research_figures.operational base='assets/img/research/operational/' %}

[Python source](/assets/img/research/operational/operational_projections.py) · [Summary tables and provenance](/assets/img/research/operational/README.md)

## Constructed illustrations

These figures use explicitly constructed examples rather than application
results. They do not report empirical costs, information estimates or a
predictive-score comparison.

{% include figure_gallery.liquid figures=site.data.research_figures.illustrations base='assets/img/research/' %}

[Python source for constructed illustrations](/assets/img/research/gen_research_figures.py) · [Build and scope notes](/assets/img/research/README.md) · [Compact preview sources](/assets/img/research/previews/README.md)
