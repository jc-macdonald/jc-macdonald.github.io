---
layout: page
title: Research figures
permalink: /figures/
description: Computed software examples, vector downloads and editable sources for research figures.
nav: false
---

[Computed software examples](/software-examples/) use the released packages for spatial fields, stochastic ensembles, replicated design comparisons and incomplete-data reconstruction. They include retained data and a generated comparison table.

Architecture and method diagrams are built from TikZ. Numerical illustrations
retain their Python plotting sources. SVGs scale on screen; PDFs are available
for slides and print. See the [build and scope notes](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/README.md) for regeneration and scientific context.

<div class="table-responsive" markdown="1">

| Figure                                             | Screen                                                         | Print                                                          | Source                                                                                                                          |
| -------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Simulation, inference and decisions                | [SVG](/assets/img/research/beyond_onehealth.svg)               | [PDF](/assets/img/research/beyond_onehealth.pdf)               | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/beyond_onehealth.tex)          |
| Partial observability across scientific domains    | [SVG](/assets/img/research/obs_model_general.svg)              | [PDF](/assets/img/research/obs_model_general.pdf)              | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/obs_model_general.tex)         |
| Current research directions                        | [SVG](/assets/img/research/future_directions_general.svg)      | [PDF](/assets/img/research/future_directions_general.pdf)      | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/future_directions_general.tex) |
| OP System compilation and numerical interfaces     | [SVG](/assets/img/research/op_system_slide.svg)                | [PDF](/assets/img/research/op_system_slide.pdf)                | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/op_system_slide.tex)           |
| OP Engine method families                          | [SVG](/assets/img/research/op_engine_slide.svg)                | [PDF](/assets/img/research/op_engine_slide.pdf)                | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/op_engine_slide.tex)           |
| op_infer research capabilities                     | [SVG](/assets/img/research/op_infer_slide.svg)                 | [PDF](/assets/img/research/op_infer_slide.pdf)                 | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/op_infer_slide.tex)            |
| FlepiMoP2 provider relationships                   | [SVG](/assets/img/research/flepimop2_slide.svg)                | [PDF](/assets/img/research/flepimop2_slide.pdf)                | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/flepimop2_slide.tex)           |
| Replicated design and evaluation with trade-study  | [SVG](/assets/img/research/trade_study_slide.svg)              | [PDF](/assets/img/research/trade_study_slide.pdf)              | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/trade_study_slide.tex)         |
| Signal rank with incomplete data                   | [SVG](/assets/img/research/pp_eigentest_schematic.svg)         | [PDF](/assets/img/research/pp_eigentest_schematic.pdf)         | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/pp_eigentest_schematic.tex)    |
| VBPCApy observed-data model                        | [SVG](/assets/img/research/vbpca_py_schematic.svg)             | [PDF](/assets/img/research/vbpca_py_schematic.pdf)             | [TikZ](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/tikz/vbpca_py_schematic.tex)        |
| Illustrative observation-design tradeoffs          | [SVG](/assets/img/research/optimal_design.svg)                 | [PDF](/assets/img/research/optimal_design.pdf)                 | [Python](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/gen_research_figures.py)          |
| Predictive evaluation and structural admissibility | [SVG](/assets/img/research/structural_fidelity_comparison.svg) | [PDF](/assets/img/research/structural_fidelity_comparison.pdf) | [Python](https://github.com/jc-macdonald/jc-macdonald.github.io/blob/main/assets/img/research/gen_research_figures.py)          |

</div>

The cost/utility and structural-admissibility plots use explicitly constructed
examples. They are illustrations, with no empirical study results or predictive
score comparison asserted. Package capability and qualification details remain
in the corresponding software documentation.

### Computed package demonstrations

| Example                         | Screen                                                             | Print                                                              |
| ------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Periodic spatial diffusion      | [SVG](/assets/img/research/computed/spatial_diffusion.svg)         | [PDF](/assets/img/research/computed/spatial_diffusion.pdf)         |
| Independent stochastic ensemble | [SVG](/assets/img/research/computed/stochastic_ensemble.svg)       | [PDF](/assets/img/research/computed/stochastic_ensemble.pdf)       |
| Replicated design comparison    | [SVG](/assets/img/research/computed/replicated_tradeoff.svg)       | [PDF](/assets/img/research/computed/replicated_tradeoff.pdf)       |
| Incomplete-data reconstruction  | [SVG](/assets/img/research/computed/incomplete_reconstruction.svg) | [PDF](/assets/img/research/computed/incomplete_reconstruction.pdf) |

[Python source and pinned dependencies](/assets/img/research/computed/computed_examples.py) · [Numerical data](/assets/img/research/computed/computed_data.json) · [CSV table](/assets/img/research/computed/design_comparison.csv) · [Assumptions and checks](/software-examples/)
