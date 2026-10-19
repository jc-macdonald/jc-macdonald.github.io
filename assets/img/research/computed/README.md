# Computed software examples

These figures run public packages on synthetic inputs. They complement the
TikZ architecture diagrams with spatial fields, stochastic paths, replicated
objective comparisons and incomplete-data reconstruction. No private research
data, fitted application parameters or unpublished results are used.

Run from the website repository:

```sh
uv run --python 3.12 assets/img/research/computed/computed_examples.py
uv run --python 3.12 assets/img/research/computed/computed_examples.py --check
```

The script pins OP System 0.8.0, OP Engine 0.7.0, trade-study 0.5.1,
VBPCApy 0.4.6, NumPy and Matplotlib. Regeneration writes SVG/PDF/PNG exports,
full input/output arrays in `computed_data.json`, `design_comparison.csv`,
its copy in `_data/computed_designs.csv`, and `provenance.json` with source,
registry and artifact hashes. Jekyll reads the CSV copy for the example table.
Normal site builds serve the exports without importing the scientific packages.
Production builds preserve the files in this directory without minification.
The deployment workflow checks their bytes against the committed provenance
after Jekyll finishes, so even a whitespace-only JSON rewrite fails publication.
Heatmap pixels are embedded in SVG/PDF at export resolution, while curves and
labels remain vector elements. This keeps the homepage field plot compact.

`--check` first verifies committed hashes and accessible SVG descriptions.
It regenerates the computations into a temporary directory, checks independent
equations and invariants, and compares retained numerical results. The seeded
SSA bank must replay exactly. Floating-point field and study results use tight
tolerances; VBPCA reconstruction allows small platform-dependent differences.
The check does not require byte-identical fresh PDF or font rendering across
platforms. Checked-in exports remain covered by their artifact hashes.

The `Computed figures` workflow runs this check when sources or artifacts
change. After regeneration, format the repository and review the figures at
desktop and mobile widths. Generated SVGs and numerical/provenance JSON are
excluded from Prettier because their bytes are checksummed; the Python builder
owns their formatting.

## Checks and limitations

| Figure                      | Computation                                                                                         | Independent check                                                                                                                                                      |
| --------------------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `spatial_diffusion`         | A periodic finite-difference stencil compiled by OP System and integrated by OP Engine RK4          | Known Fourier-mode solution of the discrete stencil; conservation of the spatial mean. This does not measure continuum discretization error.                           |
| `stochastic_ensemble`       | 512 independent exact SSA transfer paths with accepted firing counts                                | Constant total population, firing-count identity and analytic pointwise mean reference. The percentile band describes paths, not a confidence interval for their mean. |
| `replicated_tradeoff`       | Ten sample-mean designs with 512 paired replicates, two measurement-noise levels and declared costs | Analytic variance reference and an independent dominance check. Costs are assumptions and the estimated front is conditional on the replicate bank.                    |
| `incomplete_reconstruction` | A two-component VBPCA fit to observed entries of a noisy synthetic matrix                           | Held-out reconstruction error. The component count is supplied; rank selection and uncertainty coverage are not tested here.                                           |

The SSA and study examples adapt
[op_engine's replicate example](https://github.com/ACCIDDA/op_engine/blob/3f3dc246f9f0aa938bc15d87c52efce30e66e4fa/examples/replicate_ssa.py)
and [trade-study's replicated example](https://github.com/jcm-sci/trade-study/blob/ee0136b842c7c15feb35cf4a7933639c0df972d5/examples/replicated_study.py).
Their MIT notices are retained in `NOTICE`. Layout choices follow the plotting
conventions used in my other research repositories: common scales for comparison,
separate panels for trajectories and summaries, readable export sizes, and tables
drawn from the computed results. Research-specific datasets and findings stay in
their originating projects.
