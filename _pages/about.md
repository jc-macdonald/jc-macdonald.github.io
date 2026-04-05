---
layout: about
title: about
permalink: /
subtitle: Computational Scientist · <a href='https://www.jhsph.edu/'>Johns Hopkins Bloomberg School of Public Health</a>

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>International Vaccine Access Center</p>
    <p>Department of International Health</p>
    <p>Johns Hopkins Bloomberg School of Public Health</p>
    <p>Baltimore, MD</p>

selected_papers: false # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

Decision-makers across health, environmental, and earth sciences routinely act on models that assume away what they can't observe. My work makes that gap explicit: I build the computational infrastructure — generative models, inference algorithms, forecasting pipelines, and model evaluation tools — that turns partially observed systems into defensible decision support. Prediction alone is not enough; the structural assumptions buried in every model must be exposed, tested, and defended before anyone acts on the output.

Currently I am a postdoctoral scholar at the [International Vaccine Access Center](https://www.jhsph.edu/ivac/) at Johns Hopkins, where I develop operational infectious disease forecasting and decision support systems for [ACCIDDA](https://accidda.org/), a CDC Center for Forecasting and Outbreak Analytics collaboration. This work delivers real-time scenario projections that inform public health resource allocation and intervention timing. I also collaborate with the [Jolles Lab](https://sites.google.com/view/jolles-lab/home) at Oregon State University on cross-scale modeling of Crimean–Congo hemorrhagic fever (CCHF) in wildlife and livestock systems, designing surveillance strategies that balance information gain against field cost. Previously I was a [Zuckerman STEM Leadership Fellow](https://zuckerman-scholars.org/) at Tel Aviv University, working with [Yoav Ram](https://www.yoavram.com/) on Bayesian dimensionality reduction for incomplete cultural and genetic datasets.

{% include figure.liquid loading="eager" path="assets/img/research/obs_model_general.png" class="img-fluid rounded z-depth-1" %}

Each domain shares the same core problem: partially observed systems where the cost of a wrong structural assumption compounds through the decision chain — from surveillance design, to intervention evaluation, to resource deployment. Whether the system is a multi-host zoonosis, a real-time epidemic forecast, or the coevolution of genes and culture, the question is the same: *what should we do, given what we can't observe?*

{% include figure.liquid loading="eager" path="assets/img/research/beyond_onehealth.png" class="img-fluid rounded z-depth-1" %}

I hold a PhD in Mathematics from the University of Louisiana at Lafayette and a BA in Archaeology from UNC Greensboro — a combination that continues to shape how I think about inference from incomplete records.

{% include figure.liquid loading="eager" path="assets/img/research/future_directions.png" class="img-fluid rounded z-depth-1" %}

---

#### Methods & Expertise

All in service of moving from *"what does the model predict?"* to *"what should we do, given what we can't observe?"*

**Modeling.** Generative models (ODE/PDE/stochastic/hybrid); compartmental and agent-based models; scientific AI/ML (physics-embedded surrogates, lawful learning); multivariate data analysis and dimensionality reduction; stability, bifurcation, and sensitivity analysis; parameter identifiability and inverse problems.

**Inference.** Bayesian hierarchical models; variational and simulation-based inference; data assimilation; uncertainty quantification; model calibration and validation; proper scoring rules and forecast evaluation.

**Scientific computing.** Python, Julia, C++, Stan, R, MATLAB. High-performance numerical solvers; operator splitting; reproducible workflows (Git, CI/CD, containerization); data pipelines and exploratory analysis.
