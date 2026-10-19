---
layout: page
title: Research and software
nav_title: Research & software
permalink: /projects/
description: Models and software for studying changing systems, learning from incomplete data, and comparing interventions and research designs.
nav: true
nav_order: 3
display_categories: ["Released software", "Research in progress", "Collaborative infrastructure"]
horizontal: false
---

My research asks what we can learn from incomplete observations, how to evaluate
scientific predictions, and which measurements or interventions to compare.
The projects below include released tools and ongoing methods research.
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

{% include software_table.liquid %}

[Computed examples and comparison table](/software-examples/) · [Public source repositories](/repositories/)
