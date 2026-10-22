---
layout: page
permalink: /talks/
title: Talks
description: Invited seminars, conference presentations, and symposia.
nav: false
nav_order: 8
---

## Invited talks and seminars

<ul class="cv-entries academic-entries list-unstyled">
{% for entry in site.data.cv.cv.sections['Invited Talks and Seminars'] %}
  {% include cv/rendercv-entry.liquid %}
{% endfor %}
</ul>

## Workshop presentations

<ul class="cv-entries academic-entries list-unstyled">
{% for entry in site.data.cv.cv.sections['Workshop Facilitation'] %}
  {% if entry.position contains 'Presenter' %}{% include cv/rendercv-entry.liquid %}{% endif %}
{% endfor %}
</ul>

## Selected conference presentations

<ul class="cv-entries academic-entries list-unstyled">
{% for entry in site.data.cv.cv.sections['Selected Conference Presentations'] %}
  {% include cv/rendercv-entry.liquid %}
{% endfor %}
</ul>

## Symposia organized

<ul class="cv-entries academic-entries list-unstyled">
{% for entry in site.data.cv.cv.sections['Professional Service'] %}
  {% if entry.name == 'Mini-symposium Co-organizer' %}{% include cv/rendercv-entry.liquid %}{% endif %}
{% endfor %}
</ul>
