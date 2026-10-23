---
layout: page
title: Research and software
nav_title: Research & software
permalink: /projects/
description: Models and software for studying changing systems, learning from incomplete data, and comparing interventions and research designs.
nav: true
nav_order: 4
last_modified_at: 2026-10-23
display_categories: ["Released software", "Research in progress", "Collaborative infrastructure"]
horizontal: false
---

My work combines scientific models, statistical inference and study design.
The projects below provide software for these questions and describe ongoing
methods research. OP System, OP Engine, op_infer and trade-study are
general-purpose tools for dynamical systems and study comparison; their scope
is not limited to infectious disease or public health. Health, ecological,
environmental and social systems provide applications of the same underlying
methods.

The pages keep three kinds of status separate. **Lifecycle** labels say whether
software is released or still in development. **Evidence** comes from linked
publications, operational work, executable software or explicitly identified
work in progress. **Example type** says whether an illustration uses observed,
synthetic or constructed inputs. None of these labels, by itself, establishes
scientific validity for a new application.

- **How do processes across scales shape changing systems?** My [buffalo disease studies](/publications/#macdonald2024fmdv) connect infection within animals to transmission between them, while an [NPZD model](/publications/#macdonald2024lbaopd) links physical and ecological processes in harmful algal blooms. [Modeling in practice](/operational-modeling/) describes vaccination and respiratory-virus scenario work as one application area.
- **What can we learn from incomplete data?** My [cultural transmission research](/publications/#macdonald2024austronesian) uses statistical summaries of cultural traits. [VBPCApy](/projects/vbpca_py/) and [signal-rank research](/projects/pp_eigentest/) develop tools for incomplete datasets.
- **How should we assess models and compare studies?** [Current methods research](/projects/current_analyses/) examines scientific constraints and inference. The [replicated design example](/software-examples/#replicated-designs) shows a synthetic comparison of estimation error and assumed cost.

The software packages can be used independently or in combination.

<nav class="page-links" aria-label="Project sections">
  <a href="#released-software">Released software</a>
  <a href="#research-in-progress">Research in progress</a>
  <a href="#collaborative-infrastructure">Collaborative infrastructure</a>
  <a href="#software-guide">Software guide</a>
</nav>

<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <h2 id="{{ category | slugify }}" class="category">{{ category }}</h2>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  {% assign project_columns = 2 %}
  {% if sorted_projects.size == 3 %}{% assign project_columns = 3 %}{% endif %}
  <!-- Generate cards for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-{{ project_columns }}">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>

## Software guide

The labels below describe software development stage and availability. They do
not establish numerical accuracy or scientific validity for a particular use.
Package availability and the linked evidence were last reviewed on 23 October 2026.

{% include software_table.liquid %}

[Computed examples and comparison table](/software-examples/) · [Public source repositories](/repositories/)
