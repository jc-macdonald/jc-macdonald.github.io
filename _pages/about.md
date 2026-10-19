---
layout: about
title: about
permalink: /
subtitle: Assistant Scientist · <a href='https://publichealth.jhu.edu/'>Johns Hopkins Bloomberg School of Public Health</a>

profile:
  align: right
  image: prof_pic.jpg
  image_alt: Profile photograph
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Baltimore, Maryland</p>

selected_papers: false # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

I study how models can inform interventions, surveillance and data collection when the underlying system is only partly observed. I develop simulation, statistical inference and model-evaluation methods for health, environmental and earth sciences.

I am an Assistant Scientist at the [International Vaccine Access Center](https://publichealth.jhu.edu/ivac), Johns Hopkins Bloomberg School of Public Health. With [ACCIDDA](https://accidda.org/), I develop infectious disease models and software for scenario projections and public health planning. I also collaborate with the [Jolles Lab](https://sites.google.com/view/jolles-lab/home) on wildlife and livestock disease surveillance.

<p>Email: <a href="mailto:{{ site.data.socials.email }}">{{ site.data.socials.email }}</a> · <a href="https://orcid.org/{{ site.data.socials.orcid_id }}">ORCID</a></p>

Previously, I was a Zuckerman STEM Leadership Fellow at Tel Aviv University, working with [Yoav Ram](https://www.yoavram.com/) on incomplete cultural and genetic data. I hold a PhD in Mathematics from the University of Louisiana at Lafayette and a BA in Archaeology from UNC Greensboro.

<nav class="page-links" aria-label="Explore my work">
  <a href="/publications/">Publications</a>
  <a href="/projects/">Research and software</a>
  <a href="/operational-modeling/">Operational modeling</a>
  <a href="/cv/">CV</a>
</nav>

## Research in progress

My current methodological work asks how measurement assumptions and scientific constraints affect what we can learn from a model.

- **[Structural scores](/projects/current_analyses/#structural-scores-and-scientific-prediction).** Assessing predictions against stated scientific constraints, including checks before outcomes are observed.
- **[Inference and calibration](/projects/inference_calibration/).** Estimating unknown model quantities and assessing fitting procedures with simulated data. The op_infer research software is private, pre-alpha and unreleased.
- **[Incomplete data and latent structure](/projects/pp_eigentest/).** Investigating how many patterns a dataset can support, building on [VBPCApy](/projects/vbpca_py/) and a [2024 preprint](https://arxiv.org/abs/2409.12129).

[Current application studies](/projects/current_analyses/#application-studies) address dengue within-host dynamics, observation noise, outbreak vaccination and Crimean-Congo hemorrhagic fever surveillance. These summaries describe ongoing questions; public papers and artifacts are linked as they become available.

## Computations and software

I build reusable tools for model specification, simulation, inference and study comparison. Projects use the pieces they need. OP System and OP Engine support spatial fields, nonlocal interactions, compartmental dynamics and stochastic reactions.

<div class="research-preview-grid">
  <figure>
    <a href="/software-examples/#spatial-diffusion"><img src="/assets/img/research/previews/spatial_diffusion.svg" alt="A synthetic periodic field becomes more uniform over time under diffusion." width="720" height="450" loading="lazy"></a>
    <figcaption><a href="/software-examples/#spatial-diffusion">Spatial simulation</a> with OP System and OP Engine. The supplied discretization is checked against its exact Fourier-mode solution.</figcaption>
  </figure>
  <figure>
    <a href="/software-examples/#incomplete-data"><img src="/assets/img/research/previews/incomplete_reconstruction.svg" alt="The fitted reconstruction of a synthetic incomplete matrix, with smoothly varying structure across columns." width="720" height="450" loading="lazy"></a>
    <figcaption><a href="/software-examples/#incomplete-data">Learning from incomplete data</a> with VBPCApy. Held-out observations assess this reconstruction; the component count is supplied.</figcaption>
  </figure>
</div>

[Software and project descriptions](/projects/) cover the packages and their development stages. [Computed examples](/software-examples/) include stochastic ensembles, a replicated design comparison, numerical inputs and checks. [Figure downloads](/figures/) provide vector graphics and editable sources.

## Selected publications

{% include selected_papers.liquid %}

[All publications, preprints and manuscripts in preparation](/publications/)
