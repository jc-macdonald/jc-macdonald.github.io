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

My work determines what actions to take, what experiments to run, and what measurements are worth collecting in systems where interventions are costly and uncertainty is unavoidable. I build the computational machinery — generative models, inference algorithms, forecasting pipelines, and model evaluation tools — that makes this possible for partially observed systems across health, environmental, and earth sciences; concretely, the infectious disease tools are developed for CDC-funded scenario modeling that contributes to the process used to set influenza vaccination policy, while other tools support wildlife disease surveillance design in sub-Saharan Africa and public health resource allocation. Prediction alone is not enough; the structural assumptions buried in every model must be exposed, tested, and defended before anyone acts on the output.

Currently I am a postdoctoral scholar at the [International Vaccine Access Center](https://www.jhsph.edu/ivac/) at Johns Hopkins, where I develop operational infectious disease forecasting and decision support systems for [ACCIDDA](https://accidda.org/), a CDC Center for Forecasting and Outbreak Analytics collaboration. This work contributes scenario projections to the CDC Flu Scenario Modeling Hub, which supports public health resource allocation and intervention timing. I also collaborate with the [Jolles Lab](https://sites.google.com/view/jolles-lab/home) at Oregon State University on cross-scale modeling of Crimean–Congo hemorrhagic fever (CCHF) in wildlife and livestock systems, designing surveillance strategies that balance information gain against field cost. Previously I was a [Zuckerman STEM Leadership Fellow](https://zuckerman-scholars.org/) at Tel Aviv University, working with [Yoav Ram](https://www.yoavram.com/) on Bayesian dimensionality reduction for incomplete cultural and genetic datasets.

I hold a PhD in Mathematics from the University of Louisiana at Lafayette and a BA in Archaeology from UNC Greensboro — a combination that continues to shape how I think about inference from incomplete records.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/beyond_onehealth.png" class="img-fluid rounded z-depth-1" %}
</div>

---

#### The common structure

Every system I work on shares the same architecture: a latent process we care about, an observation process that distorts it, and the data we actually get. Whether the latent state is disease prevalence in a wildlife herd, nutrient cycling in a marine ecosystem, or cultural trait frequencies in a human population, the challenge is identical — the thing we need to make decisions about is never directly observed. The figure below maps this architecture across four domains.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/obs_model_general.png" class="img-fluid rounded z-depth-1" %}
</div>

This is not just a conceptual analogy. The mathematical structure is shared: each domain requires a generative model that encodes how hidden states produce observables, an inference engine that inverts the observation process under uncertainty, and a decision layer that translates posterior beliefs into actionable recommendations. Building this infrastructure so that it transfers across domains — rather than rebuilding it from scratch for each application — is the central goal of my research program.

The operational tools I build reflect this shared structure and compose into a stack — from model specification to numerical integration to orchestration to evaluation:

- **Model specification.** [OP System](https://github.com/ACCIDDA/op_system) provides a declarative language for specifying structured dynamical systems with multi-axis stratification; the compiler produces validated model objects consumed by downstream solvers.
- **Numerical integration.** [OP Engine](https://github.com/ACCIDDA/op_engine) is an operator-partitioned ODE/PDE solver core with nine methods (explicit, IMEX, fully implicit), adaptive stepping, and zero per-step allocation.
- **Orchestration.** [FlepiMoP2](https://github.com/ACCIDDA/flepimop2) drives configuration-driven batch campaigns over locations and scenarios, connecting the specification and solver stack to CDC scenario modeling hubs and contributing projections used in influenza vaccination policy.
- **Design and evaluation.** [trade-study](https://github.com/jcm-sci/trade-study) uses simulators with known ground truth to score competing configurations — model formulations, solver choices, measurement strategies, or any design decision — against ground truth using proper scoring rules and multi-objective Pareto optimization, so that decisions validated on benchmarks transfer to real data.
- **Dimensionality reduction.** [vbpca-py](https://github.com/yoavram-lab/VBPCApy) and [pp-eigentest](https://github.com/yoavram-lab/pp-eigentest) recover latent population structure from incomplete datasets with full posterior uncertainty and principled rank determination.

#### Where this is going

The research program moves along three axes. First, _enable decisions_: determine what intervention to deploy, what experiment to run, and what to measure next — then package these recommendations into tested, documented, open-source software with CI pipelines so that collaborators and decision-makers can act on model output they have reason to trust. Second, _harden the inference_: build reusable tools for Bayesian rank selection ([pp-eigentest](https://github.com/yoavram-lab/pp-eigentest)), multi-objective design and evaluation ([trade-study](https://github.com/jcm-sci/trade-study)), and missing-data-native dimensionality reduction ([vbpca-py](https://github.com/yoavram-lab/VBPCApy)) that work across application areas. Third, _generalize_: extend the partially observed decision framework to new domains and new classes of systems — multi-host zoonoses, marine ecosystems, cultural evolution, spatial processes.

<div style="margin: 2.5rem 0;">
{% include figure.liquid loading="eager" path="assets/img/research/future_directions_general.png" class="img-fluid rounded z-depth-1" %}
</div>

The question that ties it all together: _what should we do, given what we can't observe?_

---

#### Software

| Tool                                                        | What it does                                                                                       | Status                                                                                        |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [op_system](https://github.com/ACCIDDA/op_system)           | Declarative language & compiler for structured dynamical systems                                   | Active development · [docs](https://accidda.github.io/op_system/)                             |
| [op_engine](https://github.com/ACCIDDA/op_engine)           | Operator-partitioned ODE/PDE solver (9 methods, adaptive, zero-alloc)                              | Developed for CDC-funded flu scenario modeling · [docs](https://accidda.github.io/op_engine/) |
| [flepimop2](https://github.com/ACCIDDA/flepimop2)           | Configuration-driven orchestration for forecasting & scenario analysis                             | Active development · CDC scenario modeling                                                    |
| [trade-study](https://github.com/jcm-sci/trade-study)       | Design & evaluation: score competing configurations against known ground truth via simulators, scoring rules, Pareto optimization, stacking | Active development (Python + [Julia](https://github.com/jcm-sci/TradeStudy.jl))               |
| [vbpca-py](https://github.com/yoavram-lab/VBPCApy)          | Variational Bayesian PCA for incomplete data with full posterior uncertainty                       | Released on [PyPI](https://pypi.org/project/vbpca-py/) · JOSS submission in preparation       |
| [pp-eigentest](https://github.com/yoavram-lab/pp-eigentest) | Posterior predictive eigenvalue testing for signal rank determination                              | Pre-release · companion to [arXiv:2409.12129](https://arxiv.org/abs/2409.12129)               |

---

#### Methods & Expertise

These capabilities are deployed to design interventions, optimize surveillance strategies, and determine what experiments and measurements are worth their cost.

**Modeling.** Generative models (ODE/PDE/stochastic/hybrid); compartmental and agent-based models; scientific AI/ML (physics-embedded surrogates); multivariate data analysis and dimensionality reduction; stability, bifurcation, and sensitivity analysis; parameter identifiability and inverse problems.

**Inference.** Bayesian hierarchical models; variational and simulation-based inference; data assimilation; uncertainty quantification; model calibration and validation; proper scoring rules and forecast evaluation.

**Scientific computing.** Python, Julia, C++, Stan, R, MATLAB. High-performance numerical solvers; operator splitting; reproducible workflows (Git, CI/CD, containerization); data pipelines and exploratory analysis.
