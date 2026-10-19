---
layout: page
title: Research figures
permalink: /figures/
description: Computed examples, method diagrams and editable sources for research figures.
nav: false
---

The computed figures below use public synthetic data and released software.
Each links to its assumptions, numerical checks and full multi-panel version.
The method diagrams and constructed illustrations follow in separate sections.

<nav class="page-links" aria-label="Figure sections">
  <a href="#computed-examples">Computed examples</a>
  <a href="#method-and-software-diagrams">Method diagrams</a>
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

## Constructed illustrations

These figures use explicitly constructed examples rather than application
results. They do not report empirical costs, information estimates or a
predictive-score comparison.

{% include figure_gallery.liquid figures=site.data.research_figures.illustrations base='assets/img/research/' %}

[Python source for constructed illustrations](/assets/img/research/gen_research_figures.py) · [Build and scope notes](/assets/img/research/README.md) · [Compact preview sources](/assets/img/research/previews/README.md)
