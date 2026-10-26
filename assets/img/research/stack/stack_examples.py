# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#   "matplotlib==3.11.2", "numpy==2.5.4", "scipy==1.18.1",
#   "op-system==0.10.0", "op-engine==0.9.1", "jax==0.12.0.1", "torch==2.14.1",
# ]
# [[tool.uv.index]]
# name = "pytorch-cpu"
# url = "https://download.pytorch.org/whl/cpu"
# explicit = true
# [tool.uv.sources]
# torch = { index = "pytorch-cpu" }
# ///
"""Compute the figures that show what distinguishes the OP stack, with checks.

Run with ``uv run --python 3.12 stack_examples.py``; ``--check`` verifies the
committed hashes, regenerates into a temporary directory and compares every
retained deterministic array. Every figure uses a synthetic model with assumed
parameters and reports software behavior, not a finding about any system.

Single-call wall-clock timings are recorded in ``stack_data.json`` with the CPU
model and thread settings for the record only; they are not plotted, because
single calls without repetitions are not a benchmark.

Figures carry axis labels, legends and panel letters only. The setting, checks
and limits belong in the page captions and in README.md beside this file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import time
import xml.etree.ElementTree as ET
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")
import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np
import torch
from op_engine import (
    BatchedDirectSSASolver,
    BatchedSSAConfig,
    CoreSolver,
    FiringRecorder,
    ModelCore,
    SteadyStateConfig,
    from_compiled_replicates,
    steady_state,
)
from op_engine.core_solver import RunConfig
from op_engine.model_core import ModelCoreOptions
from op_system import compile_spec
from scipy.integrate import solve_ivp

jax.config.update("jax_enable_x64", True)

HERE = Path(__file__).resolve().parent
OUTPUT = HERE
SEED = 20261026
TEAL, BLUE, GOLD, RED, GREY, CHARCOAL = (
    "#148F77",
    "#2471A3",
    "#87641A",
    "#B03A2E",
    "#5D6D7E",
    "#2C3E50",
)
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
plt.rcParams.update(
    {
        "font.size": 14,
        "axes.labelsize": 14,
        "axes.titlesize": 14,
        "legend.fontsize": 12,
        "text.color": CHARCOAL,
        "axes.labelcolor": CHARCOAL,
        "xtick.color": GREY,
        "ytick.color": GREY,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.fonttype": "path",
        "svg.hashsalt": "jcmacdonald-stack-examples",
        "figure.facecolor": "white",
    }
)

# A six-state nutrient, producer and grazer chemostat written as hazard-style
# transitions. The three L* states are loss sinks that keep mass accounted for.
SPEC = {
    "kind": "transitions",
    "state": ["N", "P", "H", "LN", "LP", "LH"],
    "transitions": [
        {"name": "inN", "to": "N", "rate": "Dmix*N0"},
        {"name": "outN", "from": "N", "to": "LN", "rate": "Dmix"},
        {"name": "upN", "from": "N", "to": "LN", "rate": "muT*P/(Kn+N)"},
        {"name": "birthP", "to": "P", "rate": "muT*N/(Kn+N)*P"},
        {"name": "grazeP", "from": "P", "to": "LP", "rate": "Imax*H/(Kg+P)"},
        {"name": "mortP", "from": "P", "to": "LP", "rate": "mP"},
        {"name": "birthH", "to": "H", "rate": "eH*Imax*P*H/(Kg+P)"},
        {"name": "predH", "from": "H", "to": "LH", "rate": "Icop*Cop/(Kc+H)"},
        {"name": "mortH", "from": "H", "to": "LH", "rate": "mH"},
    ],
}
PARAMS = {
    "Dmix": 0.15,
    "N0": 1.0,
    "muT": 1.0,
    "Kn": 0.3,
    "Imax": 1.5,
    "Kg": 0.5,
    "mP": 0.05,
    "eH": 0.5,
    "Icop": 0.3,
    "Cop": 1.0,
    "Kc": 1.0,
    "mH": 0.10,
}
Y0 = np.array([1.0, 0.5, 0.5, 0.0, 0.0, 0.0])
T_END, NSTEP = 40.0, 400
TIMES = np.linspace(0.0, T_END, NSTEP + 1)


DESCRIPTIONS = {
    "stack_backend_parity": (
        "One compiled model under three array libraries",
        "Panel a: nutrient, producer and grazer concentrations over forty time units from a "
        "six-state chemostat integrated by fixed-step Runge-Kutta, with open markers from an "
        "adaptive reference solver lying on the curves. Panel b: bar chart of final-state error "
        "against that reference for NumPy, JAX and PyTorch in float64 and float32; the three "
        "float64 bars are equal to the displayed digits at about one times ten to the minus eight "
        "and the three float32 bars at about five times ten to the minus six. Dotted and dash-dot "
        "lines mark machine epsilon for float64 and float32 as references.",
    ),
    "stack_batched_ensemble": (
        "A parameter ensemble by vmap over one compiled evaluator",
        "Panel a: a 45 by 45 grid of two parameters, producer growth rate against inflow "
        "nutrient, coloured by the producer concentration at the final time; a marker shows the "
        "nominal pair. Panel b: producer concentration over time with the 5th to 95th percentile "
        "band across the 2025 members, their median, and a dashed line for a separately computed "
        "NumPy run at the nominal parameters.",
    ),
    "stack_gradient": (
        "A derivative through the fixed-step solver checked by finite differences",
        "Panel a: producer concentration at the final time against the producer growth-rate "
        "parameter, with a short tangent segment from automatic differentiation at parameter "
        "value one. Panel b: relative difference between central finite differences and the "
        "autodiff derivative against the finite-difference step on log axes; it falls with slope "
        "two to about ten to the minus ten, then rises as round-off dominates.",
    ),
    "stack_spec_to_ssa": (
        "One transition specification run deterministically and as exact stochastic draws",
        "Panel a: infectious hosts over 120 time units in a 400-host SIRS model: a shaded 5th to "
        "95th percentile band across 256 direct-SSA paths, their median, and the deterministic "
        "solution of the same specification. Panel b: mean cumulative infection, recovery and "
        "waning events per path from the retained event counts.",
    ),
    "stack_spatial_convergence": (
        "Spatial convergence of a supplied diffusion operator to an analytic solution",
        "Panel a: the heat equation on the unit interval, with the sine initial condition, the "
        "exact solution at time 0.5, and open circles from a 16-interval finite-difference "
        "solution lying on the exact curve. Panel b: maximum error against the exact solution on "
        "log axes for five meshes, lying on a line of slope two.",
    ),
    "stack_steady_states": (
        "Equilibria of a bistable cubic by vectorized pseudo-transient solves",
        "A diagram of equilibrium x against a forcing parameter a: an upper and a lower branch of "
        "stable states from the vectorized solves, a dashed unstable branch from the cubic's roots, "
        "and a bounded shaded interval of a in which both stable states exist.",
    ),
}


def letter_panels(axes):
    """Place (a), (b), ... at the top left of each panel, outside the frame."""
    for label, ax in zip("abcdef", np.atleast_1d(axes).ravel(), strict=False):
        ax.text(
            -0.08, 1.04, f"({label})", transform=ax.transAxes, fontsize=14, fontweight="bold",
            ha="right", va="bottom", color=CHARCOAL,
        )


def annotate_svg(path, name):
    """Embed an accessible title and description and a white background."""
    title, desc = DESCRIPTIONS[name]
    root = ET.parse(path).getroot()
    root.set("role", "img")
    root.set("aria-labelledby", "title description")
    for index, (tag, value) in enumerate((("title", title), ("desc", desc))):
        element = ET.Element(f"{{{SVG_NS}}}{tag}")
        element.set("id", "title" if tag == "title" else "description")
        element.text = value
        root.insert(index, element)
    x, y, width, height = root.attrib["viewBox"].split()
    root.insert(
        2,
        ET.Element(
            f"{{{SVG_NS}}}rect",
            {"x": x, "y": y, "width": width, "height": height, "fill": "#ffffff"},
        ),
    )
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def export(figure, name):
    """Write vector exports and a compatibility PNG with deterministic metadata."""
    figure.savefig(OUTPUT / f"{name}.svg", dpi=600, metadata={"Date": None})
    annotate_svg(OUTPUT / f"{name}.svg", name)
    figure.savefig(
        OUTPUT / f"{name}.pdf", metadata={"CreationDate": None, "ModDate": None}
    )
    figure.savefig(OUTPUT / f"{name}.png", dpi=200)
    plt.close(figure)


def cpu_description():
    """CPU model and thread settings, for the record beside single-call timings."""
    model = platform.processor() or platform.machine()
    try:
        text = Path("/proc/cpuinfo").read_text()
        found = re.search(r"model name\s*:\s*(.+)", text)
        if found:
            model = found.group(1).strip()
    except OSError:
        pass
    return {
        "model": model,
        "logical_cpus": os.cpu_count(),
        "threads_env": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "XLA_FLAGS") if os.environ.get(k)},
        "torch_threads": torch.get_num_threads(),
    }


def reference_trajectory(compiled):
    """Adaptive high-order reference for the chemostat, independent of the engine."""

    def rhs(t, y):
        return np.asarray(compiled.eval_fn(t, np.asarray(y), **PARAMS))

    sol = solve_ivp(
        rhs,
        (0.0, T_END),
        Y0,
        t_eval=TIMES,
        rtol=1e-12,
        atol=1e-14,
        method="DOP853",
    )
    return sol.y.T


def engine_run(compiled, to_backend, to_numpy, dtype, params):
    """Fixed-step RK4 through op_engine with the state held in one array namespace."""
    core = ModelCore(
        len(Y0), 1, TIMES, options=ModelCoreOptions(store_history=True, dtype=dtype)
    )
    core.set_initial_state(to_backend(np.asarray(Y0, dtype).reshape(-1, 1)))

    def rhs(t, y):
        return compiled.eval_fn(t, y[:, 0], **params).reshape(-1, 1)

    t0 = time.perf_counter()
    CoreSolver(core).run(rhs, config=RunConfig(method="rk4", adaptive=False, strict=True))
    elapsed = time.perf_counter() - t0
    return to_numpy(core.state_array[:, :, 0]), elapsed


def engine_run_jit(compiled, dtype, params):
    """The same fixed-step engine loop traced once under jax.jit with the scan loop."""
    jdtype = jnp.float32 if dtype is np.float32 else jnp.float64

    def final_state(y0):
        core = ModelCore(
            len(Y0), 1, TIMES, options=ModelCoreOptions(store_history=False, dtype=dtype)
        )
        core.set_initial_state(y0.reshape(-1, 1))
        CoreSolver(core).run(
            lambda t, y: compiled.eval_fn(t, y[:, 0], **params).reshape(-1, 1),
            config=RunConfig(method="rk4", adaptive=False, strict=True, fixed_loop="scan"),
        )
        return core.current_state[:, 0]

    fn = jax.jit(final_state)
    y0 = jnp.asarray(Y0, dtype=jdtype)
    t0 = time.perf_counter()
    fn(y0).block_until_ready()
    compile_s = time.perf_counter() - t0
    t0 = time.perf_counter()
    out = fn(y0).block_until_ready()
    warm_s = time.perf_counter() - t0
    return np.asarray(out), compile_s, warm_s


def backends():
    """Array namespace adapters: name -> (to_backend, to_numpy, dtype, params)."""
    out = {}
    for label, dtype in (("float64", np.float64), ("float32", np.float32)):
        jt = jnp.float32 if dtype is np.float32 else jnp.float64
        tt = torch.float32 if dtype is np.float32 else torch.float64
        out[f"NumPy {label}"] = (
            lambda a: a,
            np.asarray,
            dtype,
            {k: dtype(v) for k, v in PARAMS.items()},
        )
        out[f"JAX {label}"] = (
            lambda a, jt=jt: jnp.asarray(a, dtype=jt),
            np.asarray,
            dtype,
            {k: jnp.asarray(v, dtype=jt) for k, v in PARAMS.items()},
        )
        out[f"PyTorch {label}"] = (
            lambda a, tt=tt: torch.as_tensor(a, dtype=tt),
            lambda t: t.detach().cpu().numpy(),
            dtype,
            {k: torch.as_tensor(v, dtype=tt) for k, v in PARAMS.items()},
        )
    return out


def backend_parity(compiled, reference):
    """One compiled model under three array libraries and two precisions."""
    rhs_ref = np.asarray(compiled.eval_fn(0.0, Y0, **PARAMS))
    rows = {}
    numpy_traj = None
    for name, (to_backend, to_numpy, dtype, params) in backends().items():
        rhs = to_numpy(compiled.eval_fn(0.0, to_backend(np.asarray(Y0, dtype)), **params))
        traj, elapsed = engine_run(compiled, to_backend, to_numpy, dtype, params)
        rows[name] = {
            "rhs_rel_err": float(np.max(np.abs(rhs - rhs_ref)) / np.max(np.abs(rhs_ref))),
            "final_err": float(np.max(np.abs(traj[-1] - reference[-1]))),
            "max_err": float(np.max(np.abs(traj - reference))),
            "eager_s": elapsed,
        }
        if name == "NumPy float64":
            numpy_traj = traj
    for label, dtype in (("float64", np.float64), ("float32", np.float32)):
        params = backends()[f"JAX {label}"][3]
        final, compile_s, warm_s = engine_run_jit(compiled, dtype, params)
        rows[f"JAX {label} (jit)"] = {
            "final_err": float(np.max(np.abs(final - reference[-1]))),
            "compile_s": compile_s,
            "warm_s": warm_s,
        }
    assert rows["NumPy float64"]["max_err"] < 1e-6
    # The same method runs the same arithmetic in every namespace, so eager
    # evaluation is bit-identical across NumPy, JAX and PyTorch at each precision.
    # Compilation under jax.jit may fuse and reorder operations, so the jit path
    # is compared with a tolerance at the rounding level instead.
    for precision in ("float64", "float32"):
        base = rows[f"NumPy {precision}"]
        for name in (f"JAX {precision}", f"PyTorch {precision}"):
            for field in ("rhs_rel_err", "final_err", "max_err"):
                assert rows[name][field] == base[field], (name, field)
    assert abs(rows["JAX float64 (jit)"]["final_err"] - rows["NumPy float64"]["final_err"]) < 1e-14
    assert abs(rows["JAX float32 (jit)"]["final_err"] - rows["NumPy float32"]["final_err"]) < 1e-6
    rows["eager_bitwise_identical_across_namespaces"] = True

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained")
    states = [
        (0, "Nutrient", BLUE, "-", "o"),
        (1, "Producer", TEAL, "--", "s"),
        (2, "Grazer", GOLD, "-.", "^"),
    ]
    for idx, label, color, ls, marker in states:
        axes[0].plot(TIMES, numpy_traj[:, idx], color=color, ls=ls, lw=2, label=label)
        axes[0].plot(TIMES[::40], reference[::40, idx], marker, color=color, mfc="white", ms=5)
    axes[0].plot([], [], "o", color=GREY, mfc="white", ms=5, label="Adaptive reference")
    axes[0].set(xlabel="Time", ylabel="Concentration")
    axes[0].legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.24), fontsize=11)

    names = ["NumPy", "JAX", "PyTorch"]
    x = np.arange(len(names))
    w = 0.38
    for off, label, color, hatch in ((-w / 2, "float64", TEAL, None), (w / 2, "float32", RED, "//")):
        vals = [max(rows[f"{n} {label}"]["final_err"], 1e-17) for n in names]
        axes[1].bar(x + off, vals, w, color=color, hatch=hatch, edgecolor="white", label=label)
    for dtype, color, ls, label in (
        (np.float64, TEAL, ":", "Machine epsilon, float64"),
        (np.float32, RED, "-.", "Machine epsilon, float32"),
    ):
        axes[1].axhline(np.finfo(dtype).eps, color=color, ls=ls, lw=1.4, label=label)
    axes[1].set_yscale("log")
    axes[1].set(
        xticks=x,
        xticklabels=names,
        ylabel="Error at $t=40$ vs reference",
        ylim=(1e-17, 1e-3),
    )
    axes[1].legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.24), fontsize=11)
    letter_panels(axes)
    export(fig, "stack_backend_parity")
    return {"rows": rows, "trajectory_numpy_float64": numpy_traj.tolist()}


def scan_rk4(compiled, params, keep=None):
    """Fixed-step RK4 over the compiled evaluator as a JAX scan (for vmap and grad)."""
    h = T_END / NSTEP

    def f(y):
        return compiled.eval_fn(0.0, y, **params)

    def step(y, _):
        k1 = f(y)
        k2 = f(y + 0.5 * h * k1)
        k3 = f(y + 0.5 * h * k2)
        k4 = f(y + h * k3)
        y_next = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return y_next, (y[keep] if keep is not None else None)

    return jax.lax.scan(step, jnp.asarray(Y0), None, length=NSTEP)


def batched_ensemble(compiled):
    """A parameter ensemble by vmap over the same compiled evaluator.

    Single-call timings are recorded for the data file only; they are not
    plotted because single calls without repetitions are not a benchmark.
    """

    def member(mu_t, n0):
        final, producer = scan_rk4(compiled, dict(PARAMS, muT=mu_t, N0=n0), keep=1)
        return final, producer

    batched = jax.jit(jax.vmap(member))
    sizes = [1, 10, 100, 1000, 10000]
    rows = []
    for n in sizes:
        mu = jnp.linspace(0.8, 1.4, n)
        n0 = jnp.linspace(0.8, 2.0, n)
        t0 = time.perf_counter()
        batched(mu, n0)[0].block_until_ready()
        compile_s = time.perf_counter() - t0
        t0 = time.perf_counter()
        batched(mu, n0)[0].block_until_ready()
        warm_s = time.perf_counter() - t0
        loop_s = float("nan")
        if n <= 100:
            t0 = time.perf_counter()
            for a, b in zip(np.asarray(mu), np.asarray(n0), strict=True):
                engine_run(
                    compiled,
                    lambda x: x,
                    np.asarray,
                    np.float64,
                    dict(PARAMS, muT=float(a), N0=float(b)),
                )
            loop_s = time.perf_counter() - t0
        rows.append(
            {"n": n, "vmap_compile_s": compile_s, "vmap_warm_s": warm_s, "numpy_loop_s": loop_s}
        )

    # A two-dimensional design: a 45 x 45 grid over both parameters.
    side = 45
    mu_axis = np.linspace(0.8, 1.4, side)
    n0_axis = np.linspace(0.8, 2.0, side)
    mu_grid, n0_grid = np.meshgrid(mu_axis, n0_axis, indexing="ij")
    final, producer = batched(jnp.asarray(mu_grid.ravel()), jnp.asarray(n0_grid.ravel()))
    final_producer = np.asarray(final)[:, 1].reshape(side, side)
    producer = np.asarray(producer)
    single, _ = engine_run(
        compiled, lambda x: x, np.asarray, np.float64, {k: np.float64(v) for k, v in PARAMS.items()}
    )
    # A separately evaluated vectorized call at the nominal pair must agree with
    # the eager NumPy run through the engine.
    nominal = np.asarray(member(1.0, 1.0)[0])
    nominal_gap = float(np.max(np.abs(nominal - single[-1])))
    assert nominal_gap < 1e-9
    t_steps = TIMES[:-1]
    q05, q50, q95 = np.quantile(producer, [0.05, 0.5, 0.95], axis=0)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained")
    image = axes[0].pcolormesh(
        mu_axis, n0_axis, final_producer.T, shading="nearest", cmap="viridis", rasterized=True
    )
    axes[0].plot([1.0], [1.0], "o", color="white", mec=CHARCOAL, ms=9, label="Nominal parameters")
    axes[0].set(xlabel="Producer growth-rate parameter", ylabel="Inflow nutrient parameter")
    fig.colorbar(image, ax=axes[0], label="Producer at $t=40$", shrink=0.9)
    axes[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), fontsize=11)
    axes[1].fill_between(
        t_steps, q05, q95, color=TEAL, alpha=0.25, lw=0, label="5th to 95th percentile of members"
    )
    axes[1].plot(t_steps, q05, color=TEAL, lw=0.9, ls=":")
    axes[1].plot(t_steps, q95, color=TEAL, lw=0.9, ls=":")
    axes[1].plot(t_steps, q50, color=TEAL, lw=2, label=f"Median of {side * side} members")
    axes[1].plot(
        TIMES, single[:, 1], color=CHARCOAL, ls="--", lw=1.8, label="Nominal parameters, NumPy run"
    )
    axes[1].set(xlabel="Time", ylabel="Producer concentration")
    axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=1, fontsize=11)
    letter_panels(axes)
    export(fig, "stack_batched_ensemble")
    return {
        "timings_single_call": rows,
        "design": {"mu": mu_axis.tolist(), "n0": n0_axis.tolist()},
        "final_producer_grid": final_producer.tolist(),
        "nominal_vs_numpy_max_abs": nominal_gap,
        "quantiles": {"t": t_steps.tolist(), "q05": q05.tolist(), "q50": q50.tolist(), "q95": q95.tolist()},
    }


def gradient_check(compiled):
    """Derivative of a model output by autodiff, checked against finite differences."""

    def final_producer(mu_t):
        return scan_rk4(compiled, dict(PARAMS, muT=mu_t))[0][1]

    value = jax.jit(final_producer)
    grad = jax.jit(jax.grad(final_producer))
    mu_grid = np.linspace(0.7, 1.5, 41)
    curve = np.array([float(value(m)) for m in mu_grid])
    mu0 = 1.0
    g0 = float(grad(mu0))
    v0 = float(value(mu0))
    eps = np.array([1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 3e-6, 1e-6, 3e-7, 1e-7])
    fd = np.array([(float(value(mu0 + e)) - float(value(mu0 - e))) / (2 * e) for e in eps])
    rel = np.abs(fd - g0) / abs(g0)
    assert rel.min() < 1e-7

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained")
    axes[0].plot(mu_grid, curve, color=TEAL, lw=2, label="Model output")
    span = np.array([mu0 - 0.1, mu0 + 0.1])
    axes[0].plot(span, v0 + g0 * (span - mu0), color=RED, ls="--", lw=1.8, label="Tangent from autodiff")
    axes[0].plot([mu0], [v0], "o", color=RED, ms=7)
    axes[0].set(xlabel="Producer growth-rate parameter", ylabel="Producer at $t=40$")
    axes[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), fontsize=11)
    axes[1].loglog(eps, np.maximum(rel, 1e-17), "o-", color=TEAL, lw=2, label="|FD − autodiff| / |autodiff|")
    ref = rel[2] * (eps / eps[2]) ** 2
    axes[1].loglog(eps[:7], ref[:7], ":", color=GREY, lw=1.4, label="Slope 2 (central difference)")
    axes[1].set(xlabel="Finite-difference step", ylabel="Relative difference")
    axes[1].invert_xaxis()
    axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), fontsize=11)
    letter_panels(axes)
    export(fig, "stack_gradient")
    return {
        "mu": mu_grid.tolist(),
        "curve": curve.tolist(),
        "grad": g0,
        "value_at_nominal": v0,
        "eps": eps.tolist(),
        "fd": fd.tolist(),
        "fd_rel_err": rel.tolist(),
    }


def deterministic_and_stochastic():
    """One transition spec run as ODE and as an exact SSA bank with retained event counts.

    The spec declares a replicate axis and asks the compiler to factorize it;
    the compiler certifies that every reaction stays within its own replicate,
    which is what lets the batched exact solver give each replicate its own
    event clock. The deterministic run uses the same spec with one replicate.
    """
    pop, count = 400, 256
    params = {"beta": 0.5, "gamma": 0.2, "omega": 0.02, "Ntot": float(pop)}

    def spec_for(reps):
        return {
            "kind": "transitions",
            "axes": [{"name": "rep", "coords": [f"r{i}" for i in range(reps)]}],
            "factorize_axes": ["rep"],
            "state": ["S[rep]", "I[rep]", "R[rep]"],
            "transitions": [
                {"name": "infect", "from": "S[rep]", "to": "I[rep]", "rate": "beta*I[rep]/Ntot"},
                {"name": "recover", "from": "I[rep]", "to": "R[rep]", "rate": "gamma"},
                {"name": "wane", "from": "R[rep]", "to": "S[rep]", "rate": "omega"},
            ],
        }

    times = np.linspace(0.0, 120.0, 241)
    y0 = np.array([pop - 5.0, 5.0, 0.0])

    single = compile_spec(spec_for(1))
    core = ModelCore(3, 1, times)
    core.set_initial_state(y0.reshape(-1, 1))
    CoreSolver(core).run(
        lambda t, y: single.eval_fn(t, y[:, 0], **params).reshape(-1, 1),
        config=RunConfig(method="rk4", adaptive=False, strict=True),
    )
    ode = np.asarray(core.state_array)[:, :, 0]

    bank = compile_spec(spec_for(count))
    network = from_compiled_replicates(bank, params, batch_axis="rep")
    core_s = ModelCore(3, count, times)
    core_s.set_initial_state(np.repeat(y0[:, None], count, axis=1))
    recorder = FiringRecorder((0, 1, 2))
    stoich = np.asarray(network.stoichiometry, dtype=float)
    BatchedDirectSSASolver(core_s, network.stoichiometry).run(
        network.propensity,
        rng=np.random.SeedSequence(SEED),
        replicate_ids=tuple(range(count)),
        config=BatchedSSAConfig(forcing_breakpoints=network.forcing_breakpoints),
        recorder=recorder,
    )
    paths = np.asarray(core_s.state_array)
    np.testing.assert_array_equal(paths.sum(axis=1), pop)
    counts = np.asarray(recorder.cumulative)
    rebuilt = y0[None, :, None] + np.einsum("sr,trk->tsk", stoich, counts)
    np.testing.assert_array_equal(rebuilt, paths)
    infected = paths[:, 1, :]
    q05, q50, q95 = np.quantile(infected, [0.05, 0.5, 0.95], axis=1)
    extinct = float(np.mean(infected[-1] == 0))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), layout="constrained")
    axes[0].fill_between(
        times, q05, q95, color=TEAL, alpha=0.25, lw=0, label="5th to 95th percentile, 256 SSA paths"
    )
    axes[0].plot(times, q05, color=TEAL, lw=0.9, ls=":")
    axes[0].plot(times, q95, color=TEAL, lw=0.9, ls=":")
    axes[0].plot(times, q50, color=TEAL, lw=2, label="Median SSA path")
    axes[0].plot(times, ode[:, 1], color=CHARCOAL, ls="--", lw=1.8, label="ODE from the same spec")
    axes[0].set(xlabel="Time", ylabel="Infectious hosts")
    axes[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=1, fontsize=11)
    for k, (label, color, ls) in enumerate(
        (("Infection", RED, "-"), ("Recovery", BLUE, "--"), ("Waning", GOLD, "-."))
    ):
        axes[1].plot(times, counts[:, k, :].mean(axis=1), color=color, ls=ls, lw=2, label=label)
    axes[1].set(xlabel="Time", ylabel="Cumulative events per path (mean)")
    axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=3, fontsize=11)
    letter_panels(axes)
    export(fig, "stack_spec_to_ssa")
    return {
        "spec": spec_for(count),
        "params": params,
        "channels": list(network.channel_names),
        "stoichiometry": stoich.tolist(),
        "times": times.tolist(),
        "ode": ode.tolist(),
        "quantiles": {"q05": q05.tolist(), "q50": q50.tolist(), "q95": q95.tolist()},
        "fraction_extinct_at_end": extinct,
        "mean_counts": counts.mean(axis=2).tolist(),
        "final_infected_all_paths": infected[-1].tolist(),
        "paths_sha256": hashlib.sha256(paths.tobytes()).hexdigest(),
        "counts_sha256": hashlib.sha256(counts.tobytes()).hexdigest(),
    }


def spatial_convergence():
    """Second-order convergence of a diffusion discretization to the analytic solution.

    Heat equation on [0, 1] with zero Dirichlet boundaries and initial
    condition sin(pi x) has the exact solution sin(pi x) exp(-D pi^2 t). The
    centred finite-difference operator is supplied explicitly through a
    compiled named-axis contraction; RK4 integrates it with a step small
    enough that the spatial error dominates.
    """
    diffusivity, t_end = 0.1, 0.5
    sizes = [8, 16, 32, 64, 128]
    errors = []
    fields = {}
    for n in sizes:
        x = np.linspace(0.0, 1.0, n + 1)
        interior = x[1:-1]
        h = 1.0 / n
        m = n - 1
        lap = (np.eye(m, k=1) - 2 * np.eye(m) + np.eye(m, k=-1)) * diffusivity / h**2
        spec = {
            "kind": "expr",
            "axes": [
                {"name": "cell", "type": "categorical", "coords": [f"c{i}" for i in range(m)]}
            ],
            "state": ["u[cell]"],
            "equations": {"u[cell]": "apply_along(L[cell,cell:j]*u[cell:j], cell=j, kernel=sum)"},
        }
        compiled = compile_spec(spec)
        dt = 0.2 * h**2 / diffusivity
        steps = int(np.ceil(t_end / dt))
        times = np.linspace(0.0, t_end, steps + 1)
        core = ModelCore(1, m, times, options=ModelCoreOptions(store_history=False))
        core.set_initial_state(np.sin(np.pi * interior)[None, :])
        CoreSolver(core).run(
            lambda t, s, c=compiled, L=lap, mm=m: c.eval_fn(t, s.reshape(-1), L=L).reshape(1, mm),
            config=RunConfig(method="rk4", adaptive=False, strict=True),
        )
        u = np.asarray(core.current_state)[0]
        exact = np.sin(np.pi * interior) * np.exp(-diffusivity * np.pi**2 * t_end)
        errors.append(float(np.max(np.abs(u - exact))))
        fields[n] = (interior.tolist(), u.tolist(), exact.tolist())
    errors = np.array(errors)
    hs = 1.0 / np.array(sizes)
    order = float(np.polyfit(np.log(hs), np.log(errors), 1)[0])
    assert 1.9 < order < 2.1, order

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), layout="constrained")
    xs, u, exact = fields[16]
    axes[0].plot([0] + xs + [1], [0] + exact + [0], color=CHARCOAL, lw=2, label="Exact solution, $t=0.5$")
    axes[0].plot([0] + xs + [1], [0] + u + [0], "o", color=TEAL, mfc="white", ms=6, label="16 mesh intervals, $t=0.5$")
    axes[0].plot(
        [0] + xs + [1], [0] + list(np.sin(np.pi * np.array(xs))) + [0], ":", color=GREY, lw=1.4, label="Initial condition"
    )
    axes[0].set(xlabel="Position", ylabel="Field value")
    axes[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=1, fontsize=11)
    axes[1].loglog(hs, errors, "o-", color=TEAL, lw=2, label="Max error at $t=0.5$")
    axes[1].loglog(hs, errors[2] * (hs / hs[2]) ** 2, ":", color=GREY, lw=1.4, label="Slope 2 reference")
    axes[1].set(xlabel="Mesh spacing $h$", ylabel="Error vs exact solution")
    axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=1, fontsize=11)
    letter_panels(axes)
    export(fig, "stack_spatial_convergence")
    return {"mesh_intervals": sizes, "errors": errors.tolist(), "order": order}


def steady_state_branches():
    """Equilibria of a bistable model by pseudo-transient continuation, vmapped over a parameter.

    The cubic model x' = a + x - x^3 has one or three equilibria depending on a.
    Continuation from two initial guesses, mapped over a grid of a with
    jax.vmap, recovers both stable branches; the unstable branch is the
    remaining real root of the cubic, drawn from the polynomial as a reference.
    """
    # early_exit=False keeps the iteration a fixed-length traced loop so jax.vmap applies.
    config = SteadyStateConfig(
        dt0=0.1, max_iterations=400, residual_tol=1e-12, step_tol=1e-12, early_exit=False
    )

    def solve_from(a, guess):
        res = steady_state(lambda t, y: a + y - y**3, jnp.asarray([guess]), config=config)
        return res.state[0], res.converged

    a_grid = np.linspace(-0.6, 0.6, 121)
    hi, hi_ok = jax.vmap(lambda a: solve_from(a, 1.2))(jnp.asarray(a_grid))
    lo, lo_ok = jax.vmap(lambda a: solve_from(a, -1.2))(jnp.asarray(a_grid))
    hi, lo = np.asarray(hi), np.asarray(lo)
    hi_ok, lo_ok = np.asarray(hi_ok), np.asarray(lo_ok)
    fold = 2 / (3 * np.sqrt(3))
    real = []
    for a in a_grid:
        r = np.roots([-1.0, 0.0, 1.0, a])
        real.append(np.sort(r[np.abs(r.imag) < 1e-9].real))
    # Converged points must coincide with a root of the cubic. A continuation that
    # starts on a branch which does not exist at that a reports converged=False;
    # that may only happen outside the bistable range.
    for a, h_val, l_val, h_c, l_c, r in zip(a_grid, hi, lo, hi_ok, lo_ok, real, strict=True):
        if h_c:
            assert np.min(np.abs(r - h_val)) < 1e-6
        else:
            assert a < -fold + 1e-9
        if l_c:
            assert np.min(np.abs(r - l_val)) < 1e-6
        else:
            assert a > fold - 1e-9
    stable_hi = hi_ok & (hi > 1 / np.sqrt(3) - 1e-9)
    stable_lo = lo_ok & (lo < -1 / np.sqrt(3) + 1e-9)

    fig, ax = plt.subplots(figsize=(7.5, 4.6), layout="constrained")
    ax.axvspan(-fold, fold, color=GOLD, alpha=0.15, lw=0, label="Two stable states")
    for edge in (-fold, fold):
        ax.axvline(edge, color=GOLD, lw=1.0, ls="--")
    mid = [(a, r[1]) for a, r in zip(a_grid, real, strict=True) if len(r) == 3]
    ax.plot([a for a, _ in mid], [x for _, x in mid], "--", color=GREY, lw=1.6, label="Unstable (cubic roots)")
    ax.plot(a_grid[stable_hi], hi[stable_hi], "o", color=TEAL, ms=4, label="Upper branch, vectorized solves")
    ax.plot(a_grid[stable_lo], lo[stable_lo], "s", color=BLUE, ms=4, label="Lower branch, vectorized solves")
    ax.set(xlabel="Forcing parameter $a$", ylabel="Equilibrium $x$")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=11)
    export(fig, "stack_steady_states")
    return {
        "a": a_grid.tolist(),
        "upper": hi.tolist(),
        "lower": lo.tolist(),
        "fold": fold,
        "upper_converged": hi_ok.tolist(),
        "lower_converged": lo_ok.tolist(),
    }


FIGURES = [
    "stack_backend_parity",
    "stack_batched_ensemble",
    "stack_gradient",
    "stack_spec_to_ssa",
    "stack_spatial_convergence",
    "stack_steady_states",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(output):
    global OUTPUT
    OUTPUT = Path(output)
    compiled = compile_spec(SPEC)
    reference = reference_trajectory(compiled)
    data = {
        "spec": SPEC,
        "params": PARAMS,
        "y0": Y0.tolist(),
        "t_end": T_END,
        "steps": NSTEP,
        "backend_parity": backend_parity(compiled, reference),
        "batched_ensemble": batched_ensemble(compiled),
        "gradient": gradient_check(compiled),
        "spec_to_ssa": deterministic_and_stochastic(),
        "spatial_convergence": spatial_convergence(),
        "steady_states": steady_state_branches(),
        "machine": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            **cpu_description(),
            "timing_note": "Single calls, no repetitions; recorded for the data file only, not plotted.",
        },
    }
    (OUTPUT / "stack_data.json").write_text(json.dumps(data, indent=1) + "\n")
    packages = {
        p: version(p)
        for p in ("op-system", "op-engine", "jax", "torch", "numpy", "scipy", "matplotlib")
    }
    files = {}
    for name in FIGURES:
        for suffix in (".svg", ".pdf", ".png"):
            files[f"{name}{suffix}"] = digest(OUTPUT / f"{name}{suffix}")
    files["stack_data.json"] = digest(OUTPUT / "stack_data.json")
    manifest = {
        "schema_version": 1,
        "source_sha256": digest(Path(__file__)),
        "packages": packages,
        "files_sha256": files,
    }
    (OUTPUT / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return data


def check():
    """Verify committed hashes, then regenerate and compare every retained deterministic array.

    Excluded from comparison: single-call timings and the machine description.
    """
    manifest = json.loads((HERE / "provenance.json").read_text())
    assert manifest["source_sha256"] == digest(Path(__file__)), "Source changed; regenerate"
    for name, expected in manifest["files_sha256"].items():
        assert digest(HERE / name) == expected, f"Hash mismatch: {name}"
    committed = json.loads((HERE / "stack_data.json").read_text())
    with TemporaryDirectory(prefix="stack-examples-") as folder:
        fresh = generate(folder)

    def close(path, rtol=1e-10, atol=1e-12, exact=False):
        a, b = fresh, committed
        for key in path:
            a, b = a[key], b[key]
        if exact:
            assert a == b, path
        else:
            np.testing.assert_allclose(a, b, rtol=rtol, atol=atol, err_msg=str(path))

    close(("backend_parity", "trajectory_numpy_float64"))
    for row, vals in fresh["backend_parity"]["rows"].items():
        if not isinstance(vals, dict):
            close(("backend_parity", "rows", row), exact=True)
            continue
        for field in ("rhs_rel_err", "final_err", "max_err"):
            if field in vals:
                close(("backend_parity", "rows", row, field), atol=1e-12)
    close(("batched_ensemble", "final_producer_grid"), rtol=1e-9)
    for q in ("q05", "q50", "q95"):
        close(("batched_ensemble", "quantiles", q), rtol=1e-9)
    close(("gradient", "curve"), rtol=1e-9)
    close(("gradient", "grad"), rtol=1e-9)
    close(("gradient", "fd"), rtol=1e-6)
    close(("spec_to_ssa", "ode"), rtol=1e-10)
    close(("spec_to_ssa", "paths_sha256"), exact=True)
    close(("spec_to_ssa", "counts_sha256"), exact=True)
    close(("spec_to_ssa", "fraction_extinct_at_end"), exact=True)
    close(("spatial_convergence", "errors"), rtol=1e-8)
    close(("spatial_convergence", "order"), rtol=1e-6)
    close(("steady_states", "upper"), atol=1e-8)
    close(("steady_states", "lower"), atol=1e-8)
    close(("steady_states", "upper_converged"), exact=True)
    close(("steady_states", "lower_converged"), exact=True)
    print(
        f"Verified {len(manifest['files_sha256'])} stack artifacts; recomputed and compared "
        "trajectories, errors, ensemble grid and quantiles, gradient curve and finite differences, "
        "SSA path and count hashes, spatial errors and steady-state branches"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify hashes and recompute references")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate(HERE)
        print("Wrote", ", ".join(FIGURES))


if __name__ == "__main__":
    main()
