---
layout: page
permalink: /publications/
title: Publications
description: Journal articles, preprints and manuscripts in preparation, with citation details and source links.
nav: true
nav_order: 2
---

Journal articles are listed by year, newest first, then by publication month.
Preprints and work in preparation are listed separately. Manuscript titles and
author lists may change before publication.

<nav class="page-links" aria-label="Publication sections">
  <a href="#published">Published</a>
  <a href="#under-review">Under review</a>
  <a href="#preprints">Preprints</a>
  <a href="#in-preparation">In preparation</a>
</nav>

{% include bib_search.liquid %}

<div class="publications">

<h2 id="published" class="bibliography-year">Published</h2>
{% bibliography --query @*[status=published] %}

<h2 id="under-review" class="bibliography-year">Under review</h2>
{% bibliography --query @*[status=under_review] %}

<h2 id="preprints" class="bibliography-year">Preprints</h2>
{% bibliography --query @*[status=preprint] %}

<h2 id="in-preparation" class="bibliography-year">In preparation</h2>
{% bibliography --query @*[status=in_preparation] %}

</div>
