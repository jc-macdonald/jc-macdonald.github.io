# Research figures

[Computed package demonstrations](computed/README.md) add spatial fields,
stochastic ensembles, replicated comparisons, incomplete-data reconstruction
and a commit-pinned public op_infer calibration fixture. They retain numerical
inputs, source identity and verification records.

The website uses SVG exports. Ten architecture/method schematics have editable
TikZ sources in [`tikz/`](tikz/); two numerical illustrations use
[`gen_research_figures.py`](gen_research_figures.py). Every figure also has a
vector PDF for papers/slides and a PNG at its original URL for compatibility.
The [figure gallery](https://jcmacdonald.dev/figures/) links the exports and sources.

## Rebuild and check

Install TeX Live with `standalone`, TikZ/PGF and Latin Modern, plus Poppler's
`pdftocairo`. On Debian/Ubuntu these are supplied by `texlive-latex-extra`,
`texlive-pictures`, `lmodern` and `poppler-utils`. Python dependencies for the
two plots are pinned in the builder's uv script metadata.

```sh
uv run assets/img/research/build_figures.py
python3 assets/img/research/build_figures.py --check
```

The schematics can be rebuilt without Python plotting packages:

```sh
python3 assets/img/research/build_figures.py --schematics
python3 assets/img/research/build_figures.py op_system_slide
```

The second command selects one figure. `--check` verifies source fingerprints,
accessible SVG descriptions, static references and the three export formats.
TeX builds reject missing glyphs and overfull boxes. Review generated figures
visually too: these checks cannot establish scientific correctness or detect
every collision between diagram elements.

After regeneration, run the repository's full Prettier command and review the
SVGs at desktop and mobile widths. Normal Jekyll builds serve committed assets
and require neither TeX nor client-side TikZ rendering. Exported glyph paths
keep typography independent of browser fonts. SVG titles/descriptions and page
alt text provide the textual alternative; the source and PDF retain editable
or extractable text.

Choose the layout from the relationships being explained. Compilation can
branch into several outputs, solver capabilities can be compared in a table,
provider interfaces can surround their consumer, and adaptive studies can have
feedback paths. Use numbered steps when the figure describes an actual ordered
procedure. Share typography and colors without imposing a fixed number of stages
or the same diagram structure on different packages.

## Scientific scope

`figures.json` records each figure's title, description and source. Keep its
claims aligned with the linked package capability guides and page text:

- The OP System/Engine schematics explicitly cover PDE/structured-field,
  nonlocal/integral, compartmental and stochastic reaction models. Shaped arrays
  and RHS callbacks are numerical representations; the compiler publishes
  contracts and numerical consumers own discretization and integration.
  Individual ODE or reaction examples illustrate a particular path.
- The package architecture diagrams separate mathematical cores from campaign
  providers. Backend qualification is method-specific and CPU/GPU evidence is
  stated explicitly. Cross-axis constraints are metadata in op_system.
- `cross_scale_systems` places study systems by scale. Solid outlines mark
  systems with a published paper at that scale; dashed outlines mark
  collaborative or in-progress work without one. The figure makes no
  empirical claim.
- `software_stack` distinguishes public simulation and evaluation tools from
  op_infer, working inference and calibration research software; operational
  application material remains private. `future_directions_general` presents
  established applications, methods and developing design questions as
  interacting areas rather than an ordered pipeline. `obs_model_general`
  distinguishes domains with published or operational evidence from a
  developing monitoring-design direction. None of these figures reports
  results from ongoing studies.
- `pp_eigentest_schematic` describes the research question and scope of
  private pre-release work. `vbpca_py_schematic` describes fitting and predictive
  assessment, without implying universal calibration.
- `op_infer_slide` summarizes working fitting, calibration and study-comparison
  capabilities in a compact graphic for the project card and detail page. The
  three capability panels do not imply unlisted adapters or report study
  results. Release status is maintained as structured site data rather than
  embedded in the graphic.
- `op_infer_normal_sbc` is a public synthetic software fixture imported from an
  exact op_infer commit. Its 64-replicate SBC bank is explicitly underpowered;
  the plot is not evidence of calibration or an application result.
- `optimal_design` uses synthetic candidate costs `[1, 2.1, 3, 3.7, 5.4]` and
  utilities `[0.28, 0.45, 0.43, 0.72, 0.80]`. These are illustrative inputs.
  Design C is dominated; D maximizes utility under the declared cost limit of 4.
- `structural_fidelity_comparison` constructs two sigmoid trajectories against
  an upper prevalence bound over the plotted horizon. A curve remaining below
  the bound on this interval does not establish how it was constructed or how
  it behaves elsewhere. The figure computes no predictive scores or
  uncertainty intervals.

## Choice of tools across the software repositories

| Figure type                                          | Source and export policy                                                                                                |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Architecture, contracts, mathematical methods        | TikZ source, SVG for documentation, PDF for publication; small editable SVGs can remain SVG sources.                    |
| Numerical results, diagnostics and uncertainty plots | Keep arrays and analysis in the example's plotting code; export vector SVG/PDF where useful and retain data/provenance. |
| Generated model graphs                               | Use the model/specification as the source; Graphviz or Mermaid can be appropriate for automatic topology.               |

The review found an editable chemostat operator-split SVG and a numerical
comparison PNG in op_engine. trade-study's calibration, Pareto, sensitivity and
study plots are generated by its example programs; FlepiMoP2's scenario plots
likewise have numerical/R/Python sources. Converting those plots to hand-entered
TikZ coordinates would sever their connection to computed results. The compiler
documentation primarily uses executable model examples rather than image assets.

Reference documentation: [PGF/TikZ](https://ctan.org/pkg/pgf),
[Poppler utilities](https://poppler.freedesktop.org/), and
[Matplotlib output](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html).
