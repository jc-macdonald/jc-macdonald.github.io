---
layout: about
title: about
permalink: /
subtitle: Assistant Scientist · <a href='https://publichealth.jhu.edu/'>Johns Hopkins Bloomberg School of Public Health</a>
last_modified_at: 2026-10-28

profile:
  align: right
  image: prof_pic.jpg
  image_alt: Portrait of Joshua C. Macdonald
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

My overarching interest is how ecological and landscape change influences the movement and connectivity of hosts, pathogens and cultural traits, and through them the persistence and evolution of structured populations. My established work addresses within- and between-host dynamics and cultural transmission, and landscape-scale questions are a developing direction. I build mechanistic models, inference methods and open research software for these questions and for decisions under uncertainty. Applications include infectious disease, public and global health and ecology. I also develop methods for incomplete multivariate data. Developing work includes scientific machine learning and the design of monitoring programs and studies with field and domain partners.

I am an Assistant Scientist at the [International Vaccine Access Center](https://publichealth.jhu.edu/ivac), Johns Hopkins Bloomberg School of Public Health. With the [Atlantic Coast Center for Infectious Disease Dynamics and Analytics (ACCIDDA)](https://accidda.org/), I develop infectious disease models and software for scenario projections and public health planning. I also collaborate with the [Jolles Lab](https://sites.google.com/view/jolles-lab/home) on foot-and-mouth disease in African buffalo and Crimean-Congo hemorrhagic fever in livestock and wildlife, including transmission between species and surveillance design.

<p>Email: <a href="mailto:{{ site.data.socials.email }}">{{ site.data.socials.email }}</a> · <a href="https://orcid.org/{{ site.data.socials.orcid_id }}">ORCID</a></p>

Previously, I was a Zuckerman STEM Leadership Fellow at Tel Aviv University, working with [Yoav Ram](https://www.yoavram.com/) on incomplete cultural and genetic data. I hold a PhD in Mathematics from the University of Louisiana at Lafayette and a BA in Archaeology from UNC Greensboro.

<nav class="page-links" aria-label="Explore my work">
  <a href="/publications/">Publications</a>
  <a href="/operational-modeling/">Operational modeling</a>
  <a href="/projects/">Research</a>
  <a href="/reviewer-profile/">Reviewer and collaborator profile</a>
  <a href="/cv/">CV</a>
</nav>

## Research questions

My research asks three questions, studied in systems that include foot-and-mouth disease in African buffalo, Crimean-Congo hemorrhagic fever in livestock and wildlife, and human cultural transmission. [The research page](/projects/) describes each system.

- **How do processes within hosts shape transmission and persistence?** My buffalo studies link virus growth and immune response to transmission between animals for three strains of the SAT serotypes of foot-and-mouth disease virus. SAT-1 was reported for the first time in nine countries from Egypt to Mongolia in 2025 and 2026 ([WOAH](https://www.woah.org/en/article/the-spread-of-fmd-to-new-areas-is-concerning-but-consequences-could-be-worse/)).
- **How do landscape, movement and contact shape spread, persistence and divergence across populations?** This is a developing direction; the published work so far concerns cultural variation across geography and language, and the rest is collaborative work in progress.
- **How should we measure, vaccinate and decide under uncertainty?** I address this through surveillance, vaccination and scenario modeling.

## Currently

As of October 2026:

- Collaborative modeling of Crimean-Congo hemorrhagic fever transmission between livestock and wildlife, and of the measurements that would inform its surveillance.
- Development and release of the [OP stack](/projects/#how-the-op-stack-compares) for model specification, simulation and replicated study comparison.
- Scenario modeling for respiratory viruses with ACCIDDA ([modeling in practice](/operational-modeling/)).

I welcome enquiries from field, laboratory and public-health partners about study and surveillance design, and about applying the OP stack to a new system. I work mainly in Python (NumPy, JAX, PyTorch) and Julia.

## Selected publications

{% include selected_papers.liquid %}

[All publications, accepted papers and preprints](/publications/)

## Research in progress

My current methods research asks how measurements and scientific assumptions affect what we can learn about a system.

- **[Inference and calibration](/projects/inference_calibration/).** Estimating unknown model quantities and assessing fitting procedures with simulated data. The op_infer source is public; application materials remain private. Its current development and release status is maintained on the project page.
- **[Incomplete data and latent structure](/projects/pp_eigentest/).** Investigating how many patterns can be distinguished from noise in incomplete data, building on [VBPCApy](/projects/vbpca_py/) and a [2024 preprint](https://arxiv.org/abs/2409.12129).
- **[Constraint checks for predictions](/projects/current_analyses/#constraint-checks-for-predictions).** Reporting whether a prediction satisfies stated scientific constraints. This is now being folded into the validation layer of the software rather than developed as a separate method.

Current [public- and global-health application studies](/projects/current_analyses/#application-studies) address dengue within-host dynamics, observation noise, outbreak vaccination and Crimean-Congo hemorrhagic fever surveillance. These studies apply the methods above; they do not define the methods' scope. The summaries describe ongoing questions; public papers and artifacts are linked as they become available.

## Software

I build reusable, cross-domain tools spanning model specification, simulation, inference, calibration and validation, observation and experimental design, and comparison of decisions under scientific and resource constraints. Projects use the pieces they need. OP System and OP Engine support spatial fields, nonlocal interactions, compartmental dynamics and stochastic reactions. The stack brings to Python the separation of model specification from numerical method that odin2 and dust2 provide in R and that Catalyst provides in Julia. A specification is compiled once, and the array library (NumPy, JAX or PyTorch) is chosen when the model is called; model authors can check a compiled model against equations they write independently. The same specifications run in operational scenario projections and in research analyses ([how the stack compares](/projects/#how-the-op-stack-compares)).

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

[Software and project descriptions](/projects/) cover the packages and their development stages. [Computed examples](/software-examples/) include stochastic ensembles and a replicated design comparison, with their numerical inputs and checks. [Figure downloads](/figures/) provide vector graphics and editable sources.
