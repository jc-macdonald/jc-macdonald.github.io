---
layout: page
permalink: /extracurricular/
title: Outside work
description: I love to travel, get outside, and move.
nav: false
nav_order: 8
---

> "The joy of life comes from our encounters with new experiences, and hence there is no greater joy than to have an endlessly changing horizon, for each day to have a new and different sun."
>
> — Alexander Supertramp McCandless

<style>
.gallery-row {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}
.gallery-row .gallery-item {
  flex: 1;
  overflow: hidden;
  border-radius: 0.25rem;
}
.gallery-row .gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.gallery-row.row-landscape { height: 260px; }
.gallery-row.row-mixed     { height: 320px; }
@media (max-width: 575px) {
  .gallery-row {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .gallery-row.row-landscape,
  .gallery-row.row-mixed { height: auto; }
  .gallery-row .gallery-item { aspect-ratio: 4 / 3; }
}
</style>

<div class="gallery-row row-landscape">
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_1.jpg" alt="A broad waterfall cascading over pale rock in a forest." class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_2.jpg" alt="A hiker in a white cap above a river bend in a red-rock canyon." class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_6.jpg" alt="Pedestrians outside a stone gateway flanked by two white towers." class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="gallery-row row-mixed">
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_3.jpg" alt="Small green plants with toothed traps among moss and leaves." class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_4.jpg" alt="Red-rock ledges and a shallow stream with visitors in the distance." class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_9.jpg" alt="A flat-topped rock formation rising from calm blue water." class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="gallery-row row-landscape">
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_5.jpg" alt="A river winding through wooded hills beneath a sunset sky." class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_8.jpg" alt="People walking beneath a large carved stone arch in a city square." class="img-fluid rounded z-depth-1" %}
  </div>
</div>
<div class="gallery-row row-landscape">
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_7.jpg" alt="A runner passing spectators at a city road race." class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="gallery-item">
    {% include figure.liquid loading="eager" path="assets/img/extracurricular/travel_10.jpg" alt="A sunlit beach with shade shelters beside pale blue water." class="img-fluid rounded z-depth-1" %}
  </div>
</div>
