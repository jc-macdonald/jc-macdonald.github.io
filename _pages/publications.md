---
layout: page
permalink: /publications/
title: Publications
description: Journal articles, accepted papers and preprints, with citation details and source links.
nav: true
nav_order: 2
last_modified_at: 2026-10-28
---

Journal articles are listed by year, newest first, then by publication month.
Accepted papers and preprints are separated from published work. Titles and
author lists may change before publication.

<nav class="page-links" aria-label="Publication sections">
  <a href="#published">Published</a>
  <a href="#accepted">Accepted</a>
  <a href="#preprints">Preprints</a>
</nav>

{% include bib_search.liquid %}

<div class="publications">

<h2 id="published" class="bibliography-year">Published</h2>
{% bibliography --query @*[status=published] %}

<h2 id="accepted" class="bibliography-year">Accepted, to appear</h2>
{% bibliography --query @*[status=accepted] %}

<h2 id="preprints" class="bibliography-year">Preprints</h2>
{% bibliography --query @*[status=preprint] %}

</div>
