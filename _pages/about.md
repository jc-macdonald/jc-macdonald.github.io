---
layout: about
title: about
permalink: /
subtitle: Computational Scientist · <a href='https://publichealth.jhu.edu/'>Johns Hopkins Bloomberg School of Public Health</a>

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

I study how models can inform interventions, surveillance, and data collection when the underlying system is only partly observed. I develop simulation, statistical inference, numerical methods, and model-evaluation software for health, environmental, and earth sciences. A recurring question is how assumptions about the system and its measurements affect the conclusions we draw.

Currently I am an Assistant Scientist at the [International Vaccine Access Center](https://publichealth.jhu.edu/ivac) at Johns Hopkins (postdoctoral scholar there 2024–2026), where I develop operational infectious disease forecasting and decision support systems for [ACCIDDA](https://accidda.org/), a CDC Center for Forecasting and Outbreak Analytics collaboration. This work contributes scenario projections to the CDC Flu Scenario Modeling Hub, which supports public health resource allocation and intervention timing. I also collaborate with the [Jolles Lab](https://sites.google.com/view/jolles-lab/home) at Oregon State University on cross-scale modeling of Crimean–Congo hemorrhagic fever (CCHF) in wildlife and livestock systems, designing surveillance strategies that balance information gain against field cost. Previously I was a [Zuckerman STEM Leadership Fellow](https://zuckerman-scholars.org/) at Tel Aviv University, working with [Yoav Ram](https://www.yoavram.com/) on Bayesian dimensionality reduction for incomplete cultural and genetic datasets.

I hold a PhD in Mathematics from the University of Louisiana at Lafayette and a BA in Archaeology from UNC Greensboro. Both inform my work on inference from incomplete records.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/beyond_onehealth.svg" class="img-fluid rounded z-depth-1" zoomable=true alt="Public tools cover field/equation/reaction specification with OP System, PDE/nonlocal/reaction simulation with OP Engine, campaigns with FlepiMoP2, and replicated evaluation with trade-study. op_infer adds parameter inference, calibration and study-design checks; it is private, pre-alpha and unreleased." caption="Public simulation and evaluation tools connect to op_infer, a private pre-alpha statistical layer. Availability and scientific validation are separate questions." %}
</div>

---

#### The common structure

Many of these projects distinguish an underlying process from how it is measured. Disease prevalence, nutrient cycling, and cultural trait frequencies are inferred from observations that may be incomplete or noisy. The figure below shows this distinction across four domains. Each application has its own observation assumptions and validation requirements.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/obs_model_general.svg" class="img-fluid rounded z-depth-1" zoomable=true alt="A latent process x(t) produces data y through an observation model p(y given x and observation parameters). Health, marine, earth and human systems have different observation assumptions and validation requirements." caption="Across domains, a partially observed latent process is connected to data through an explicit observation model." %}
</div>

I develop reusable tools for specifying models, simulating observations, fitting parameters, and comparing study designs. Reusing software can reduce implementation work, while scientific assumptions and validation remain specific to each application.

The packages have distinct roles in this workflow.

- **Model specification.** [OP System](https://github.com/ACCIDDA/op_system) specifies PDE/field, nonlocal and reaction models and compiles NumPy, JAX or PyTorch evaluators, publishing reaction metadata, named observables, forcing schedules and checked independent-block contracts.
- **Numerical integration.** [OP Engine](https://github.com/ACCIDDA/op_engine) advances PDEs, nonlocal dynamics, compartmental models and stochastic reactions. It provides independent NumPy SSA banks, observations and replay. The tested NumPy, JAX and CPU PyTorch operations depend on the method.
- **Inference and calibration.** [op_infer](/projects/inference_calibration/) connects Bayesian parameter fitting, simulation-based calibration and study-design checks. Working implementations build on established inference libraries and the simulation and evaluation tools; the software remains private, pre-alpha and unreleased while application studies develop.
- **Orchestration.** [FlepiMoP2](https://github.com/ACCIDDA/flepimop2) drives configuration-defined campaigns over locations and scenarios, connecting systems, engines, parameters, processes, jobs, and persistence providers to operational modeling workflows.
- **Design and evaluation.** [trade-study](https://github.com/jcm-sci/trade-study) coordinates replicated simulation studies, paired comparisons, proper scoring rules, Pareto analysis and preference-based decisions, retaining uncertainty and result provenance. Benchmark evidence and validation on observed data remain separate requirements.
- **Dimensionality reduction.** The released [vbpca-py](https://github.com/yoavram-lab/VBPCApy) models latent structure in incomplete datasets with posterior uncertainty. Ongoing [pp-eigentest](/projects/pp_eigentest/) research investigates signal-rank selection and its calibration.

The simulation and evaluation packages are publicly released. The inference layer already has working implementations; its broader interfaces and scientific assessment remain in development. Each application needs explicit priors, observation models, estimator choices and evidence that its numerical and statistical checks are adequate for the intended use.

#### Research aims

Current methodological work examines scientific constraints on predictions, parameter inference under realistic observation designs, and latent structure in incomplete data. Application studies use these methods to compare interventions and surveillance choices.

#### Research in progress

- **[Structural scores and scientific prediction](/projects/current_analyses/#structural-scores-and-scientific-prediction).** Assessing predictions against stated scientific constraints, including checks before the outcome is known.
- **[Inference and calibration with op_infer](/projects/inference_calibration/).** Research software for parameter inference, calibration checks and replicated studies. Validation for specific applications is ongoing.
- **[Incomplete data and latent structure](/projects/pp_eigentest/).** Research on signal-rank selection for incomplete data, building on the released [VBPCApy](/projects/vbpca_py/) tools and a [2024 preprint](https://arxiv.org/abs/2409.12129).

[Current application studies](/projects/current_analyses/#application-studies) address dengue within-host dynamics, COVID-19 observation noise, diphtheria vaccination, and CCHF surveillance. These summaries describe ongoing questions and aims; papers and public research artifacts are linked as they become available.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/future_directions_general.svg" class="img-fluid rounded z-depth-1" zoomable=true alt="The research agenda connects scientific systems, ongoing work on parameter inference, calibration, structural evaluation and rank selection, and decisions about interventions and surveillance. Observations and diagnostics inform new study choices." caption="Research directions connect methodological work to scientific applications and decision support." %}
</div>

[Vector downloads and editable figure sources](/figures/) are available for reuse.

---

#### Software

<div class="table-responsive" markdown="1">

| Tool                                                  | What it does                                                                               | Status                                                                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| [op_system](https://github.com/ACCIDDA/op_system)     | PDE/field, nonlocal and reaction specifications; operators, observables and forcing        | [PyPI](https://pypi.org/project/op-system/) · [capabilities](https://accidda.github.io/op_system/latest/guides/capabilities/)           |
| [op_engine](https://github.com/ACCIDDA/op_engine)     | PDE/nonlocal operators, deterministic and stochastic solvers, observations and replay      | [PyPI](https://pypi.org/project/op-engine/) · [qualification](https://accidda.github.io/op_engine/latest/guides/backend-qualification/) |
| [op_infer](/projects/inference_calibration/)          | Parameter fitting, simulation-based calibration and study-design checks                    | Working research software · private pre-alpha · unreleased                                                                              |
| [flepimop2](https://github.com/ACCIDDA/flepimop2)     | Configuration-driven campaigns and provider interfaces                                     | [PyPI](https://pypi.org/project/flepimop2/) · [docs](https://accidda.github.io/flepimop2/latest/)                                       |
| [trade-study](https://github.com/jcm-sci/trade-study) | Replicated studies, paired comparisons, Pareto analysis, preferences and result provenance | [PyPI](https://pypi.org/project/trade-study/) · [examples](https://jcm-sci.github.io/trade-study/guide/capabilities/)                   |
| [vbpca-py](https://github.com/yoavram-lab/VBPCApy)    | Variational Bayesian PCA for incomplete data with approximate posterior uncertainty        | Released on [PyPI](https://pypi.org/project/vbpca-py/) · JOSS submission in preparation                                                 |
| [pp-eigentest](/projects/pp_eigentest/)               | Posterior predictive eigenvalue testing for signal rank determination                      | Private pre-release · methods paper in preparation, extending [arXiv:2409.12129](https://arxiv.org/abs/2409.12129)                      |

</div>

---

#### Methods & Expertise

My work uses these methods to study interventions, compare surveillance strategies, and assess the value of additional observations.

**Modeling.** Differential-equation, stochastic, hybrid and agent-based models; machine learning with scientific constraints; multivariate data analysis and dimensionality reduction; stability, bifurcation, and sensitivity analysis; parameter identifiability and inverse problems.

**Inference.** Bayesian hierarchical models; variational and simulation-based inference; data assimilation; uncertainty quantification; model calibration and validation; proper scoring rules and forecast evaluation.

**Scientific computing.** Python, Julia, C++, Stan, R, MATLAB. High-performance numerical solvers; operator splitting; reproducible workflows (Git, CI/CD, containerization); data pipelines and exploratory analysis.
