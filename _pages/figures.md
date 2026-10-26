---
search: true
layout: page
title: Research figures
permalink: /figures/
last_modified_at: 2026-10-26
description: Computed examples, method diagrams and editable sources for research figures.
nav: false
---

The computed figures below use public synthetic data. Four use released
software; the op_infer fixture is imported from a pinned public pre-alpha
commit and does not imply a release. Each links to its assumptions, checks and
full multi-panel version. The method diagrams, a published-model computation,
three small model computations and constructed illustrations follow in
separate sections. Figures carry axis labels and legends only; the setting,
assumptions and attribution for each are in the caption beside it.

<nav class="page-links" aria-label="Figure sections">
  <a href="#computed-examples">Computed examples</a>
  <a href="#method-and-software-diagrams">Method diagrams</a>
  <a href="#published-model-computations">Published-model computations</a>
  <a href="#model-computations">Model computations</a>
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

Figures in this section are recomputed from the equations of a published model,
with parameters taken from the paper. They illustrate a published qualitative
result; they are not copied from the paper, and their numerical values belong
to the recomputation.

{% include figure_gallery.liquid figures=site.data.research_figures.published_models base='assets/img/research/' %}

[Python source for the published-model computation](/assets/img/research/gen_research_figures.py) · [Build and scope notes](/assets/img/research/README.md)

## Model computations

These figures compute a result from a small model with assumed parameters, in
plain NumPy. Two recompute textbook or published results; one is an
illustrative calculation from standard estimator theory. None is fitted to
data, none makes a novelty claim and none reports a result from an application
study. The literature behind each is cited in its caption on the
[research page](/projects/#which-records-would-tell).

{% include figure_gallery.liquid figures=site.data.research_figures.model_computations base='assets/img/research/' %}

[Python source](/assets/img/research/gen_research_figures.py) · [Build and scope notes](/assets/img/research/README.md)

## Constructed illustrations

These figures use explicitly constructed examples rather than application
results. They do not report empirical costs, information estimates or a
predictive-score comparison.

{% include figure_gallery.liquid figures=site.data.research_figures.illustrations base='assets/img/research/' %}

[Python source for constructed illustrations](/assets/img/research/gen_research_figures.py) · [Build and scope notes](/assets/img/research/README.md) · [Compact preview sources](/assets/img/research/previews/README.md)
