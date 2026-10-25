---
layout: page
title: Research and software
nav_title: Research
permalink: /projects/
description: The questions and study systems I work on, and the models and software I build to study them.
nav: true
nav_order: 4
last_modified_at: 2026-10-24
display_categories: ["Released software", "Research in progress", "Collaborative infrastructure"]
horizontal: false
---

I study how ecological and landscape change influences the movement and
connectivity of hosts, pathogens and cultural traits, and through them the
persistence and evolution of structured populations. The overarching interest is
landscape and metapopulation eco-evolutionary dynamics. My established work
addresses within- and between-host dynamics and cultural transmission, and
landscape-scale questions are a developing direction. Models, inference methods
and software are my tools for these questions, and they apply beyond these
systems.

<figure>
  <img src="/assets/img/research/cross_scale_systems.svg" alt="Four study systems arranged by scale, from within individuals to across populations, with published work marked by solid outlines and collaborative or unpublished work by dashed outlines. A chain links ecological and landscape change to movement and contact, connectivity among populations, and persistence, divergence and evolution. The research questions and study systems below describe each cell." width="1100" height="1044" loading="lazy">
  <figcaption>Study systems arranged by scale. Solid outlines mark systems with a published paper at that scale. Dashed outlines mark collaborative or unpublished work. A blank cell shows no work at that scale. The chain describes the direction of influence that frames the second research question below. <a href="/figures/">Figure downloads and editable source</a>.</figcaption>
</figure>

## Research questions

- **How do processes within hosts shape transmission and persistence?** My [buffalo studies](/publications/#macdonald2024fmdv) connect virus growth and immune response in individual animals to transmission between them, and a [carrier-transmission model](/publications/#atkins2026fmdcarrier), on which I am a co-author, extends this to persistent infection. As senior personnel on a multi-institution project linking cells to landscapes in African buffalo, I develop and parameterize the within-host models. The same within-host-to-population approach underlies my [dengue and Crimean-Congo hemorrhagic fever applications](/projects/current_analyses/#application-studies).
- **How do landscape, movement and contact shape spread, persistence and divergence across populations?** This is a developing direction. Published work relates [cultural variation to geography and language](/publications/#macdonald2024austronesian) among Austronesian-speaking societies, without modeling landscape change. Collaborative work in progress models Crimean-Congo hemorrhagic fever transmission between livestock and wildlife hosts, and spatial structure is a possible extension if movement data allow. A bighorn sheep project asks how immune phenotypes vary among metapopulations.
- **How should we measure, vaccinate and decide under uncertainty?** For Crimean-Congo hemorrhagic fever, I ask which wildlife and livestock measurements would change a surveillance or control decision, given their field costs. [Modeling in practice](/operational-modeling/) describes outbreak-response vaccination and respiratory-virus scenario work, and [trade-study](/projects/trade_study/) supports comparing study designs.

Earlier theoretical work examined [hysteresis and Hopf bifurcation in a plankton model of harmful algal blooms](/publications/#macdonald2023npzd).

## Study systems

- **Foot-and-mouth disease virus in African buffalo.** A first-author within-host model and a co-authored carrier-transmission model, developed with collaborators in the Jolles Lab and a multi-institution project.
- **Crimean-Congo hemorrhagic fever virus in livestock and wildlife.** Collaborative transmission models and surveillance design; modeling in progress.
- **Human cultural transmission.** Published analysis of networks and clusters of cultural traits, with a methods [preprint](/publications/#preprints) on incomplete cultural data.
- **Bighorn sheep immune ecology.** Collaborative analysis in progress.

## Methods and software

The projects below provide software for these questions and describe ongoing
methods research. OP System, OP Engine, op_infer and trade-study are
general-purpose tools for dynamical systems and study comparison; their scope
is not limited to infectious disease or public health. Health, ecological,
environmental and social systems provide applications of the same underlying
methods.

The pages keep three kinds of status separate. **Lifecycle** labels say whether
software is released or still in development. **Evidence** labels identify the
support: linked publications, operational work, executable software or explicitly
identified work in progress. **Example type** says whether an illustration uses observed,
synthetic or constructed inputs. None of these labels, by itself, establishes
scientific validity for a new application.

Two further questions concern methods.

- **What can we learn from incomplete data?** My [cultural transmission research](/publications/#macdonald2024austronesian) uses statistical summaries of cultural traits. [VBPCApy](/projects/vbpca_py/) and [signal-rank research](/projects/pp_eigentest/) develop tools for incomplete datasets.
- **How should we assess models and compare studies?** [Current methods research](/projects/current_analyses/) examines scientific constraints and inference. The [replicated design example](/software-examples/#replicated-designs) shows a synthetic comparison of estimation error and assumed cost.

The software packages can be used independently or in combination.

<nav class="page-links" aria-label="Project sections">
  <a href="#research-questions">Research questions</a>
  <a href="#study-systems">Study systems</a>
  <a href="#methods-and-software">Methods and software</a>
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
