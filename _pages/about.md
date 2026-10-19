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

My work determines what actions to take, what experiments to run, and what measurements are worth collecting in systems where interventions are costly and uncertainty is unavoidable. I build the computational machinery — generative models, scientific machine learning methods, inference algorithms, forecasting pipelines, and design and evaluation tools — that makes this possible for partially observed systems across health, environmental, and earth sciences; concretely, the infectious disease tools contribute multi-model evidence used for public-health planning, while other tools support wildlife disease surveillance design in sub-Saharan Africa and public health resource allocation. Prediction alone is not enough; the structural assumptions buried in every model must be exposed, tested, and defended before anyone acts on the output.

Currently I am an Assistant Scientist at the [International Vaccine Access Center](https://publichealth.jhu.edu/ivac) at Johns Hopkins (postdoctoral scholar there 2024–2026), where I develop operational infectious disease forecasting and decision support systems for [ACCIDDA](https://accidda.org/), a CDC Center for Forecasting and Outbreak Analytics collaboration. This work contributes scenario projections to the CDC Flu Scenario Modeling Hub, which supports public health resource allocation and intervention timing. I also collaborate with the [Jolles Lab](https://sites.google.com/view/jolles-lab/home) at Oregon State University on cross-scale modeling of Crimean–Congo hemorrhagic fever (CCHF) in wildlife and livestock systems, designing surveillance strategies that balance information gain against field cost. Previously I was a [Zuckerman STEM Leadership Fellow](https://zuckerman-scholars.org/) at Tel Aviv University, working with [Yoav Ram](https://www.yoavram.com/) on Bayesian dimensionality reduction for incomplete cultural and genetic datasets.

I hold a PhD in Mathematics from the University of Louisiana at Lafayette and a BA in Archaeology from UNC Greensboro — a combination that continues to shape how I think about inference from incomplete records.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/beyond_onehealth.svg" class="img-fluid rounded z-depth-1" zoomable=true alt="Public tools cover model specification with OP System, numerical execution with OP Engine, campaigns with FlepiMoP2, and replicated evaluation with trade-study. op_infer adds parameter inference, calibration and study-design checks; it is private, pre-alpha and unreleased." caption="Public simulation and evaluation tools connect to op_infer, a private pre-alpha statistical layer. Availability and scientific validation are separate questions." %}
</div>

---

#### The common structure

The systems I work on share a recurring architecture: a latent process we care about, an observation process that maps and distorts it, and the data we actually get. Whether the latent state is disease prevalence in a wildlife herd, nutrient cycling in a marine ecosystem, or cultural trait frequencies in a human population, the decision-relevant state is rarely fully observed. The observation assumptions and validation requirements remain domain-specific. The figure below maps this architecture across four domains.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/obs_model_general.svg" class="img-fluid rounded z-depth-1" zoomable=true alt="A latent process x(t) produces data y through an observation model p(y given x and observation parameters). Health, marine, earth and human systems have different observation assumptions and validation requirements." caption="Across domains, a partially observed latent process is connected to data through an explicit observation model." %}
</div>

This is not just a conceptual analogy. The mathematical structure is shared: each domain requires a generative model that encodes how hidden states produce observables, an inference engine that inverts the observation process under uncertainty, and a decision layer that translates posterior beliefs into actionable recommendations. Building this infrastructure so that it transfers across domains — rather than rebuilding it from scratch for each application — is the central goal of my research program.

The tools I build reflect this shared structure and compose into a stack — from model specification and simulation to inference, campaign execution and evaluation:

- **Model specification.** [OP System](https://github.com/ACCIDDA/op_system) compiles structured equations and transitions to NumPy, JAX or PyTorch evaluators, publishing reaction metadata, named observables, forcing schedules and checked independent-block contracts.
- **Numerical integration.** [OP Engine](https://github.com/ACCIDDA/op_engine) provides deterministic and stochastic methods, independent NumPy SSA banks, observations and replay, with method-specific NumPy/JAX/CPU PyTorch qualification. Separate providers connect it to the campaign framework.
- **Inference and calibration.** [op_infer](/projects/inference_calibration/) connects Bayesian parameter fitting, simulation-based calibration and study-design checks. Working implementations build on established inference libraries and the simulation and evaluation tools; the software remains private, pre-alpha and unreleased while application studies develop.
- **Orchestration.** [FlepiMoP2](https://github.com/ACCIDDA/flepimop2) drives configuration-defined campaigns over locations and scenarios, connecting systems, engines, parameters, processes, jobs, and persistence providers to operational modeling workflows.
- **Design and evaluation.** [trade-study](https://github.com/jcm-sci/trade-study) coordinates replicated simulation studies, paired comparisons, proper scoring rules, Pareto analysis and preference-based decisions, retaining uncertainty and result provenance. Benchmark evidence and validation on observed data remain separate requirements.
- **Dimensionality reduction.** The released [vbpca-py](https://github.com/yoavram-lab/VBPCApy) models latent structure in incomplete datasets with posterior uncertainty. Ongoing [pp-eigentest](/projects/pp_eigentest/) research investigates signal-rank selection and its calibration.

The simulation and evaluation packages are publicly released. The inference layer already has working implementations; its broader interfaces and scientific assessment remain in development. Each application needs explicit priors, observation models, estimator choices and evidence that its numerical and statistical checks are adequate for the intended use.

#### Where this is going

The research program connects three aims: extend models to new scientific systems, strengthen inference and evaluation, and make the resulting evidence useful for decisions. Current methodological work asks how to assess predictions against scientific constraints, how to check parameter inference under realistic observation designs, and how to recover latent structure from incomplete data.

#### Research in progress

- **[Structural scores and scientific prediction](/projects/current_analyses/#structural-scores-and-scientific-prediction).** Can we assess whether a prediction respects stated scientific constraints before the outcome is known? I am developing structural evaluation alongside predictive scoring, with attention to what each check can establish.
- **[Inference and calibration with op_infer](/projects/inference_calibration/).** How can reusable fitting tools support credible conclusions when measurements are sparse or noisy? Working software connects parameter inference, calibration checks and replicated studies; application-specific validation is ongoing.
- **[Incomplete data and latent structure](/projects/pp_eigentest/).** How much signal can an incomplete dataset support? Ongoing rank-selection research builds on the released [VBPCApy](/projects/vbpca_py/) tools and a [2024 preprint](https://arxiv.org/abs/2409.12129).

[Current application studies](/projects/current_analyses/#application-studies) address dengue within-host dynamics, COVID-19 observation noise, diphtheria vaccination, and CCHF surveillance. These summaries describe ongoing questions and aims; papers and public research artifacts are linked as they become available.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/future_directions_general.svg" class="img-fluid rounded z-depth-1" zoomable=true alt="The research agenda connects scientific systems, ongoing work on parameter inference, calibration, structural evaluation and rank selection, and decisions about interventions and surveillance. Observations and diagnostics inform new study choices." caption="Research directions connect methodological work to scientific applications and decision support." %}
</div>

[Vector downloads and editable figure sources](/figures/) are available for reuse.

The question that ties it all together: _what should we do, given what we can't observe?_

---

#### Software

<div class="table-responsive" markdown="1">

| Tool                                                  | What it does                                                                               | Status                                                                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| [op_system](https://github.com/ACCIDDA/op_system)     | Structured model compilation, reaction/observable metadata and forcing schedules           | [PyPI](https://pypi.org/project/op-system/) · [capabilities](https://accidda.github.io/op_system/latest/guides/capabilities/)           |
| [op_engine](https://github.com/ACCIDDA/op_engine)     | Deterministic/stochastic solvers, independent NumPy SSA banks, observations and replay     | [PyPI](https://pypi.org/project/op-engine/) · [qualification](https://accidda.github.io/op_engine/latest/guides/backend-qualification/) |
| [op_infer](/projects/inference_calibration/)          | Parameter fitting, simulation-based calibration and study-design checks                    | Working research software · private pre-alpha · unreleased                                                                              |
| [flepimop2](https://github.com/ACCIDDA/flepimop2)     | Configuration-driven campaigns and provider interfaces                                     | [PyPI](https://pypi.org/project/flepimop2/) · [docs](https://accidda.github.io/flepimop2/latest/)                                       |
| [trade-study](https://github.com/jcm-sci/trade-study) | Replicated studies, paired comparisons, Pareto analysis, preferences and result provenance | [PyPI](https://pypi.org/project/trade-study/) · [examples](https://jcm-sci.github.io/trade-study/guide/capabilities/)                   |
| [vbpca-py](https://github.com/yoavram-lab/VBPCApy)    | Variational Bayesian PCA for incomplete data with full posterior uncertainty               | Released on [PyPI](https://pypi.org/project/vbpca-py/) · JOSS submission in preparation                                                 |
| [pp-eigentest](/projects/pp_eigentest/)               | Posterior predictive eigenvalue testing for signal rank determination                      | Private pre-release · methods paper in preparation, extending [arXiv:2409.12129](https://arxiv.org/abs/2409.12129)                      |

</div>

---

#### Methods & Expertise

These capabilities are deployed to design interventions, optimize surveillance strategies, and determine what experiments and measurements are worth their cost.

**Modeling.** Generative models (ODE/PDE/stochastic/hybrid); compartmental and agent-based models; scientific machine learning (physics-embedded surrogates, lawful learning); multivariate data analysis and dimensionality reduction; stability, bifurcation, and sensitivity analysis; parameter identifiability and inverse problems.

**Inference.** Bayesian hierarchical models; variational and simulation-based inference; data assimilation; uncertainty quantification; model calibration and validation; proper scoring rules and forecast evaluation.

**Scientific computing.** Python, Julia, C++, Stan, R, MATLAB. High-performance numerical solvers; operator splitting; reproducible workflows (Git, CI/CD, containerization); data pipelines and exploratory analysis.
