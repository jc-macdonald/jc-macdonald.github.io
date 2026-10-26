# OP stack demonstrations

These figures show the design choices that distinguish the OP stack, each with
an independent check, on synthetic models with assumed parameters. They
complement the [computed package examples](../computed/README.md) and report
software behavior, not findings about any application.

Run from the website repository:

```sh
uv run --python 3.12 assets/img/research/stack/stack_examples.py
uv run --python 3.12 assets/img/research/stack/stack_examples.py --check
```

The script pins OP System 0.10.0, OP Engine 0.9.1, JAX, CPU PyTorch, NumPy,
SciPy and Matplotlib. Regeneration writes SVG/PDF/PNG exports (each SVG carries
a title and a long description for assistive technology), the numerical inputs
and outputs in `stack_data.json`, and `provenance.json` with source and
artifact hashes.

`--check` verifies the committed hashes, regenerates into a temporary directory
and compares these retained quantities against the committed data file: the
NumPy float64 trajectory and every recorded backend error; the 45 × 45 ensemble
grid and its time quantiles; the gradient curve, the autodiff value and the
finite-difference sequence; the ODE solution, the SHA-256 of the full SSA path
bank and of the full event-count bank, and the extinct fraction; the spatial
errors and fitted order; both steady-state branches and both convergence-flag
vectors. Not compared: single-call timings and the machine description. The
`Computed figures` workflow runs this check when sources or artifacts change.

Timings are not plotted. Single-call wall-clock values are recorded in
`stack_data.json` under `timings_single_call` and `backend_parity.rows`, with
the CPU model, logical CPU count and PyTorch thread count under `machine`, for
the record only; single calls without repetitions are not a benchmark.

Figures carry axis labels, legends and panel letters only. The setting, checks
and limits are stated in the page captions and below.

## What each figure shows, and its check

| Figure                      | Claim it supports                                                                                                                                                                          | Independent check                                                                                                                                                                                                                                                                             | Limits                                                                                                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `stack_backend_parity`      | One compiled specification runs under NumPy, JAX and PyTorch, in float64 and float32, with the array library chosen at call time; the numerical method does not change with the namespace. | Final-state error against an adaptive DOP853 reference (SciPy, rtol 1e-12). Eager evaluation is bit-identical across the three namespaces at each precision and the code asserts equality; the `jax.jit` path, which may fuse and reorder operations, agrees with eager float64 within 1e-14. | This is one run of one model; it illustrates the documented backend scope and does not extend it. Machine epsilon lines are references, not expected error levels. |
| `stack_batched_ensemble`    | A parameter ensemble runs by `jax.vmap` over the same compiled evaluator without rewriting the model.                                                                                      | A separately evaluated vectorized call at the nominal pair agrees with an eager NumPy run through the engine within 1e-9 maximum absolute difference.                                                                                                                                         | The nominal run is computed separately, not drawn from the grid. No timing is plotted.                                                                             |
| `stack_gradient`            | A model output can be differentiated with respect to a parameter through the fixed-step solver.                                                                                            | Central finite differences of the same discrete 400-step calculation converge to the autodiff value with slope 2 before round-off; closest agreement 1.3e-10 relative.                                                                                                                        | Checks the derivative of the discrete solver, not continuous-time sensitivity. Fixed-step methods only; the adaptive controller is not a traced path.              |
| `stack_spec_to_ssa`         | One transition specification with a replicate axis the compiler verifies runs as an ODE and as a direct-SSA bank with retained event counts.                                               | By array equality on every path: total population is constant, and state equals initial state plus stoichiometry times cumulative counts. The full path and count banks are hash-compared on recheck.                                                                                         | "Exact" refers to the specified Markov jump process. Parameters are illustrative. ODE-versus-median agreement at N = 400 is qualitative, not a convergence test.   |
| `stack_spatial_convergence` | A supplied finite-difference operator, compiled as a named-axis contraction, converges to the analytic heat-equation solution at the expected order.                                       | Max error against sin(pi x) exp(-D pi^2 t) over five meshes (8 to 128 intervals) has fitted order 2.00; the time step is small enough that spatial error dominates.                                                                                                                           | One-dimensional, Dirichlet boundaries, centred differences. The user supplies the operator; the compiler does not choose a discretization.                         |
| `stack_steady_states`       | Pseudo-transient steady-state solves run under `jax.vmap` across a parameter grid, with `early_exit=False` so each solve is a fixed-length traced loop.                                    | Every state with a true convergence flag lies within 1e-6 of a root of the cubic; false flags occur only past the fold where the sought branch does not exist, and those states are omitted from the plot.                                                                                    | Independent solves at each parameter value, not continuation along a branch. A one-state toy; the unstable branch comes from the polynomial roots.                 |

## Scope statements

- All models are synthetic. None is fitted to data and none is a model of any
  study system on this site.
- The chemostat specification uses hazard-style transitions with explicit loss
  sinks so that every flow is accounted for.
- The replicate SSA path uses `factorize_axes`, under which the compiler
  verifies that no reaction crosses the replicate axis; the batched solver gives
  each replicate its own event clock and replays under a root seed with stable
  replicate identifiers.
- Backend qualification is method-specific and is documented in the packages.
  These figures illustrate the documented scope; they do not extend it.
