---
layout: page
permalink: /teaching/
title: Teaching
description: Teaching, workshop facilitation, and instructional experience.
nav: true
nav_order: 5
---

## University teaching

<ul class="cv-entries academic-entries list-unstyled">
{% for entry in site.data.cv.cv.sections.Teaching %}
  {% if entry.company == 'Johns Hopkins University' %}{% include cv/rendercv-entry.liquid %}{% endif %}
{% endfor %}
</ul>

## Workshop facilitation

<ul class="cv-entries academic-entries list-unstyled">
{% for entry in site.data.cv.cv.sections['Workshop Facilitation'] %}
  {% include cv/rendercv-entry.liquid %}
{% endfor %}
</ul>

## University of Louisiana at Lafayette

{% for entry in site.data.cv.cv.sections.Teaching %}
{% if entry.company == 'University of Louisiana at Lafayette' %}

<p><strong>{{ entry.position }}</strong>, {{ entry.start_date }}–{{ entry.end_date }}.</p>
{{ entry.summary | markdownify }}
{% endif %}
{% endfor %}

<ul class="cv-entries academic-entries list-unstyled">
{% for course in site.data.teaching_materials %}
  <li class="cv-entry">
    <div class="cv-entry-heading">
      <h3>{{ course.course }}</h3>
      <p class="cv-date">{{ course.term }}</p>
    </div>
    <p>{{ course.sections }} {% if course.sections == '1' %}section{% else %}sections{% endif %}</p>
    {{ course.materials | markdownify }}
  </li>
{% endfor %}
</ul>

## Earlier teaching

<ul class="cv-entries academic-entries list-unstyled">
{% for entry in site.data.cv.cv.sections.Teaching %}
  {% unless entry.company == 'Johns Hopkins University' or entry.company == 'University of Louisiana at Lafayette' %}
    {% include cv/rendercv-entry.liquid %}
  {% endunless %}
{% endfor %}
</ul>
