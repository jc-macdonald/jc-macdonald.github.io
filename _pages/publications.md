---
layout: page
permalink: /publications/
title: publications
description:
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">

<h2 class="bibliography-year">Published</h2>
{% bibliography --query @*[status=published] %}

<h2 class="bibliography-year">Under Review</h2>
{% bibliography --query @*[status=under_review] %}

<h2 class="bibliography-year">Preprints</h2>
{% bibliography --query @*[status=preprint] %}

<h2 class="bibliography-year">In Preparation</h2>
{% bibliography --query @*[status=in_preparation] %}

</div>
