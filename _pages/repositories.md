---
search: true
layout: page
permalink: /repositories/
title: repositories
description: GitHub repositories for research software and collaborative infrastructure.
last_modified_at: 2026-10-23
nav: false
nav_order: 5
---

The source repositories below are public. [Projects](/projects/) also covers
research software in development, including [op_infer](/projects/inference_calibration/),
whose source is public, and private [pp-eigentest](/projects/pp_eigentest/)
research software. Current release stages are maintained on their project pages.

## Public source repositories

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>

## GitHub profiles

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for user in site.data.repositories.github_users %}
    {% include repository/repo_user.liquid username=user %}
  {% endfor %}
</div>
