"""Render the numerical research figures.

Two figures are explicitly constructed illustrations. ``npzd_hysteresis`` is
recomputed from the published equations of the rescaled NPZD model (Macdonald
and Gulbudak 2023), with parameters from its table and bifurcation-figure
caption; it is not copied from the paper, and its threshold and fold values
belong to this recomputation. Three further figures are small model
computations written here in plain NumPy with assumed parameters:
``rk4_known_solution`` checks a fixed-step integrator against a closed-form
solution in float32 and float64; ``siwr_reservoir_speed`` and
``record_type_precision`` illustrate mechanisms of transmission and observation.
None reports a result from an application study.
Use build_figures.py to regenerate all formats and annotate the SVGs. Architecture
and method schematics are maintained as TikZ sources in tikz/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from palette import (
    BLUE_HEALTH,
    CHARCOAL,
    GOLD_ACCENT,
    SLATE,
    TEAL_ENVIRON,
    TEAL_PRIMARY,
    WHITE,
)

HERE = Path(__file__).resolve().parent
RED = "#B03A2E"
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 13,
        "text.color": CHARCOAL,
        "axes.labelcolor": CHARCOAL,
        "xtick.color": SLATE,
        "ytick.color": SLATE,
        "svg.fonttype": "path",
        "svg.hashsalt": "jcmacdonald-research",
    }
)


def save(fig, name, title):
    """Export vectors for the site/print and a compatibility PNG."""
    fig.savefig(
        HERE / f"{name}.svg",
        bbox_inches="tight",
        facecolor=WHITE,
        metadata={"Date": None, "Title": title},
    )
    fig.savefig(
        HERE / f"{name}.pdf",
        bbox_inches="tight",
        facecolor=WHITE,
        metadata={"CreationDate": None, "ModDate": None, "Title": title},
    )
    fig.savefig(HERE / f"{name}.png", dpi=220, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


# Rescaled NPZD model without seasonality (Macdonald and Gulbudak 2023). Values
# come from its Table "tab:sims" and its alpha/xi bifurcation-figure caption
# (a = 0.4); xi = 10 is the upper end of the tabulated range.
NPZD = {
    "k": 0.5,
    "gamma": 0.5,
    "gamma_t": 0.29,
    "c": 10.0,
    "a": 0.4,
    "s": 0.3,
    "theta": 12.0,
    "psi": 0.15,
    "eps": 0.3,
    "xi": 10.0,
}


def _grazing(p):
    return p * p / (1 + p * p)


def _npzd_rhs(y, alpha, q):
    p, z, n, d = y
    uptake = n / (q["k"] + n) * p * (1 - p / q["c"])
    harm = alpha * p / (q["xi"] + p)
    return np.array(
        [
            uptake - _grazing(p) * z - q["eps"] * p,
            q["gamma_t"] * (_grazing(p) - harm - q["a"] * z) * z,
            -uptake - q["s"] * (n - q["theta"]) + q["psi"] * d,
            (1 - q["gamma"]) * _grazing(p) * z + q["eps"] * p - q["psi"] * d,
        ]
    )


def _npzd_max_real_eigenvalue(y, alpha, q):
    """Largest real part of the Jacobian spectrum (central differences)."""
    jac = np.empty((4, 4))
    for i in range(4):
        step = 1e-6 * max(1.0, abs(y[i]))
        up, down = y.copy(), y.copy()
        up[i] += step
        down[i] -= step
        jac[:, i] = (_npzd_rhs(up, alpha, q) - _npzd_rhs(down, alpha, q)) / (2 * step)
    return np.linalg.eigvals(jac).real.max()


def _npzd_coexistence(p, q):
    """Coexistence equilibrium parameterized by p.

    At equilibrium n = theta - gamma h(p) z / s and the p-equation becomes
    G(z) = 0, with G strictly decreasing in z. Bisection gives the unique root;
    the z-equation then determines alpha.
    """
    h = _grazing(p)
    growth = p * (1 - p / q["c"])

    def residual(z):
        n = q["theta"] - q["gamma"] * h * z / q["s"]
        return n / (q["k"] + n) * growth - h * z - q["eps"] * p

    lo, hi = 0.0, q["theta"] * q["s"] / (q["gamma"] * h)
    if residual(lo) <= 0:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    z = 0.5 * (lo + hi)
    n = q["theta"] - q["gamma"] * h * z / q["s"]
    d = ((1 - q["gamma"]) * h * z + q["eps"] * p) / q["psi"]
    alpha = (h - q["a"] * z) * (q["xi"] + p) / p
    return alpha, np.array([p, z, n, d])


def _runs(mask):
    """Index ranges of consecutive equal values in a boolean array."""
    edges = np.flatnonzero(np.diff(mask.astype(int))) + 1
    starts = np.concatenate([[0], edges])
    stops = np.concatenate([edges, [len(mask)]])
    return [(a, b) for a, b in zip(starts, stops, strict=True)]


def _npzd_simulate(y0, alpha, q, t_end=160.0, dt=0.05):
    """Fixed-step fourth-order Runge-Kutta trajectory of the NPZD model."""
    steps = int(round(t_end / dt))
    out = np.empty((steps + 1, 4))
    out[0] = y0
    y = np.array(y0, dtype=float)
    for i in range(steps):
        k1 = _npzd_rhs(y, alpha, q)
        k2 = _npzd_rhs(y + dt / 2 * k1, alpha, q)
        k3 = _npzd_rhs(y + dt / 2 * k2, alpha, q)
        k4 = _npzd_rhs(y + dt * k3, alpha, q)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out[i + 1] = y
    return np.linspace(0.0, steps * dt, steps + 1), out


def npzd_hysteresis():
    """Equilibria against the harmful effect, with simulations in the bistable range."""
    from matplotlib.lines import Line2D

    q = NPZD
    p0 = q["theta"] / (q["k"] + q["theta"]) / q["eps"]
    p_hat = q["c"] * (1 - 1 / p0)
    alpha_star = _grazing(p_hat) * (q["xi"] + p_hat) / p_hat
    alpha_max = 3.0
    alpha_sim = 1.85

    rows = []
    for p in np.linspace(1e-3, p_hat * (1 - 1e-9), 3000):
        found = _npzd_coexistence(p, q)
        if found is None or found[0] <= 0:
            continue
        alpha, state = found
        rows.append((p, alpha, _npzd_max_real_eigenvalue(state, alpha, q) < 0))
    rows = np.array(rows)
    p_branch, alpha_branch, stable = rows[:, 0], rows[:, 1], rows[:, 2].astype(bool)
    turns = np.flatnonzero(np.diff(np.sign(np.diff(alpha_branch)))) + 1
    fold_alphas = np.sort(alpha_branch[turns])

    # Stable equilibria at alpha_sim, interpolated on the computed branch.
    crossings = []
    for i in np.flatnonzero(np.diff(np.sign(alpha_branch - alpha_sim))):
        if stable[i] and stable[i + 1]:
            w = (alpha_sim - alpha_branch[i]) / (alpha_branch[i + 1] - alpha_branch[i])
            crossings.append(p_branch[i] + w * (p_branch[i + 1] - p_branch[i]))
    p_low_eq, p_high_eq = sorted(crossings)

    # Two runs that differ only in initial zooplankton.
    runs = {
        "low": _npzd_simulate([1.0, 0.5, 10.0, 5.0], alpha_sim, q),
        "high": _npzd_simulate([1.0, 1.5, 10.0, 5.0], alpha_sim, q),
    }
    styles = {
        "low": ("Low initial zooplankton", BLUE_HEALTH, "-", "o", p_high_eq),
        "high": ("High initial zooplankton", RED, "--", "s", p_low_eq),
    }

    fig, (ax_eq, ax_sim) = plt.subplots(
        1,
        2,
        figsize=(10.0, 4.6),
        sharey=True,
        gridspec_kw={"width_ratios": [1.2, 1.0]},
    )
    fig.subplots_adjust(bottom=0.3, top=0.84, wspace=0.14)

    ax_eq.axvspan(
        fold_alphas[0],
        fold_alphas[-1],
        color=GOLD_ACCENT,
        alpha=0.12,
        lw=0,
        label="Two stable coexistence states",
    )
    labelled = set()
    for start, stop in _runs(stable):
        is_stable = stable[start]
        key = "Coexistence, stable" if is_stable else "Coexistence, unstable"
        end = stop + (0 if stop == len(stable) else 1)
        ax_eq.plot(
            alpha_branch[start:end],
            p_branch[start:end],
            color=TEAL_ENVIRON if is_stable else SLATE,
            lw=2.6 if is_stable else 1.8,
            ls="-" if is_stable else "--",
            label=None if key in labelled else key,
        )
        labelled.add(key)
    ax_eq.plot(
        [alpha_star, alpha_max],
        [p_hat, p_hat],
        color=CHARCOAL,
        lw=2.6,
        label="Zooplankton-free, stable",
    )
    ax_eq.plot(
        [0, alpha_star],
        [p_hat, p_hat],
        color=CHARCOAL,
        lw=1.6,
        ls=":",
        label="Zooplankton-free, unstable",
    )
    ax_eq.annotate(
        "Zooplankton-free state",
        (0.05, p_hat),
        xytext=(0, 6),
        textcoords="offset points",
        fontsize=11,
        color=CHARCOAL,
    )
    ax_eq.axvline(alpha_star, color=SLATE, lw=1.0, ls="-.")
    ax_eq.annotate(
        r"$\mathcal{P}_0^z = 1$",
        (alpha_star, 0.35),
        xytext=(6, 0),
        textcoords="offset points",
        fontsize=12,
        color=SLATE,
    )
    ax_eq.axvline(alpha_sim, color=GOLD_ACCENT, lw=1.8)
    ax_eq.annotate(
        "Simulated in (b)",
        (alpha_sim, 0.35),
        xytext=(-6, 0),
        textcoords="offset points",
        ha="right",
        fontsize=11,
        color=GOLD_ACCENT,
    )
    for _label, color, _ls, marker, p_eq in styles.values():
        ax_eq.plot(alpha_sim, p_eq, marker, color=color, ms=8, zorder=4)
    ax_eq.set(
        xlabel=r"Maximum harmful effect of phytoplankton, $\tilde{\alpha}$",
        ylabel="Phytoplankton, $p$",
        xlim=(0, alpha_max),
        ylim=(0, 8.2),
    )
    ax_eq.set_title("(a) Equilibria", loc="left", fontsize=14)
    ax_eq.grid(alpha=0.18)
    eq_handles, eq_labels = ax_eq.get_legend_handles_labels()
    order = [
        "Coexistence, stable",
        "Coexistence, unstable",
        "Zooplankton-free, stable",
        "Zooplankton-free, unstable",
        "Two stable coexistence states",
    ]
    by_label = dict(zip(eq_labels, eq_handles, strict=True))
    fig.legend(
        [by_label[name] for name in order],
        order,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.0),
        ncol=3,
        frameon=False,
        fontsize=11,
    )

    handles = []
    for key, (label, color, ls, marker, p_eq) in styles.items():
        time, states = runs[key]
        ax_sim.axhline(p_eq, color=color, lw=0.8, ls=":", alpha=0.6)
        ax_sim.plot(time, states[:, 0], color=color, lw=2.2, ls=ls)
        ax_sim.plot(
            time[-1], states[-1, 0], marker, color=color, ms=8, clip_on=False, zorder=4
        )
        handles.append(
            Line2D([], [], color=color, lw=2.2, ls=ls, marker=marker, ms=8, label=label)
        )
    ax_sim.set(xlabel="Time (rescaled)", xlim=(0, runs["low"][0][-1]))
    ax_sim.set_title("(b) Simulations", loc="left", fontsize=14)
    ax_sim.grid(alpha=0.18)
    ax_sim.legend(handles=handles, loc="center right", frameon=False, fontsize=11)

    fig.suptitle(
        "Forward hysteresis in an NPZD model", x=0.02, ha="left", fontsize=18
    )
    save(fig, "npzd_hysteresis", "Forward hysteresis in an NPZD model")


def optimal_design():
    """Use the declared synthetic costs/utilities from the original schematic."""
    costs = np.array([1.0, 2.1, 3.0, 3.7, 5.4])
    utility = np.array([0.28, 0.45, 0.43, 0.72, 0.80])
    labels = list("ABCDE")
    frontier = [0, 1, 3, 4]
    fig, ax = plt.subplots(figsize=(7.0, 5.5))
    fig.subplots_adjust(bottom=0.23, top=0.85)
    ax.plot(
        costs[frontier],
        utility[frontier],
        "--",
        color=TEAL_PRIMARY,
        lw=1.6,
        label="Pareto-efficient designs",
    )
    ax.scatter(costs, utility, color=BLUE_HEALTH, s=65, zorder=3)
    ax.scatter(
        [costs[3]],
        [utility[3]],
        color=GOLD_ACCENT,
        s=140,
        edgecolor=CHARCOAL,
        zorder=4,
        label="D: selected at cost ≤ 4",
    )
    ax.scatter([costs[2]], [utility[2]], color=SLATE, marker="x", s=80, zorder=4)
    for i, (cost, value, label) in enumerate(zip(costs, utility, labels, strict=True)):
        ax.annotate(
            label + (" (dominated)" if i == 2 else ""),
            (cost, value),
            xytext=(7, -19 if i == 2 else 9),
            textcoords="offset points",
            fontsize=12,
        )
    ax.axvline(4.0, color=GOLD_ACCENT, lw=1.3, ls=":")
    ax.set(
        xlabel="Declared cost (arbitrary units)",
        ylabel="Illustrative utility (larger is better)",
        xlim=(0.6, 6.1),
        ylim=(0.18, 0.92),
    )
    ax.set_title("Observation-design tradeoffs", loc="left", pad=20, fontsize=18)
    ax.grid(alpha=0.18)
    ax.legend(loc="lower right", frameon=False, fontsize=10)
    fig.text(
        0.02,
        0.02,
        "Synthetic inputs for illustration; no fitted study or information estimates.\nThe budget and utility define the selected design.",
        fontsize=10,
        color=SLATE,
        va="bottom",
    )
    save(fig, "optimal_design", "Illustrative observation-design tradeoffs")


def structural_fidelity():
    """Construct curves with distinct behavior against an explicit upper bound."""
    time = np.linspace(0, 12, 120)
    bounded = 0.18 + 0.72 / (1 + np.exp(-(time - 5.2) / 1.55))
    crossing = 0.16 + 0.96 / (1 + np.exp(-(time - 6.2) / 1.45))
    fig, ax = plt.subplots(figsize=(7.0, 5.5))
    fig.subplots_adjust(bottom=0.23, top=0.85)
    ax.plot(
        time,
        bounded,
        color=TEAL_PRIMARY,
        lw=2.5,
        ls="-",
        marker="o",
        markevery=14,
        ms=4,
        label="A: remains within the bound",
    )
    ax.plot(
        time,
        crossing,
        color=BLUE_HEALTH,
        lw=2.5,
        ls="--",
        marker="s",
        markevery=14,
        ms=4,
        label="B: crosses the bound",
    )
    ax.axhline(1.0, color=RED, ls="--", lw=1.5, label="Declared prevalence bound")
    ax.fill_between(time, 1.0, 1.18, color=RED, alpha=0.07)
    ax.set(
        xlabel="Illustrative forecast horizon",
        ylabel="Prevalence proportion",
        xlim=(0, 12),
        ylim=(0, 1.18),
    )
    ax.set_title(
        "Scientific constraints and predictions", loc="left", pad=20, fontsize=18
    )
    ax.grid(alpha=0.18)
    ax.legend(
        loc="lower right",
        frameon=True,
        facecolor=WHITE,
        edgecolor="none",
        framealpha=0.95,
        fontsize=10,
    )
    fig.text(
        0.02,
        0.02,
        "Constructed trajectories; no predictive scores or intervals are computed.\nConstraint checks describe the stated bound over the plotted horizon.",
        fontsize=10,
        color=SLATE,
        va="bottom",
    )
    save(
        fig,
        "structural_fidelity_comparison",
        "Illustrative scientific constraints and predictions",
    )


def _rk4_fixed(rhs, y0, t_end, steps, dtype):
    """Fixed-step RK4 with every operand held in ``dtype``.

    The step, parameters and state are cast once so that a float32 run does not
    silently promote to float64 inside NumPy arithmetic.
    """
    dt = dtype(t_end) / dtype(steps)
    half = dtype(0.5)
    sixth = dtype(1.0 / 6.0)
    two = dtype(2.0)
    y = np.asarray(y0, dtype=dtype)
    t = dtype(0.0)
    for _ in range(steps):
        k1 = rhs(t, y)
        k2 = rhs(t + half * dt, y + half * dt * k1)
        k3 = rhs(t + half * dt, y + half * dt * k2)
        k4 = rhs(t + dt, y + dt * k3)
        y = y + dt * sixth * (k1 + two * k2 + two * k3 + k4)
        t = t + dt
    return y


def rk4_known_solution():
    """Error of fixed-step RK4 against a closed-form solution in two precisions.

    Logistic growth y' = r y (1 - y / K) has the exact solution
    y(t) = K / (1 + (K / y0 - 1) exp(-r t)). Comparing against it separates the
    integrator's truncation error (which falls as the fourth power of the step)
    from floating-point round-off (which sets a floor and grows with the number
    of steps). The figure is a numerical check of one method on one problem.
    """
    r, cap, y0, t_end = 0.8, 1.0, 0.05, 20.0
    exact_end = cap / (1 + (cap / y0 - 1) * np.exp(-r * t_end))
    step_counts = np.unique(np.geomspace(8, 400_000, 22).astype(int))
    errors = {}
    for dtype in (np.float64, np.float32):
        pr, pk = dtype(r), dtype(cap)

        def rhs(t, y, pr=pr, pk=pk):
            return pr * y * (dtype(1.0) - y / pk)

        errors[dtype] = np.array(
            [
                abs(float(_rk4_fixed(rhs, [y0], t_end, int(n), dtype)[0]) - exact_end)
                for n in step_counts
            ]
        )
    # An error of exactly zero cannot be drawn on a log axis; draw it at the floor.
    floor = 1e-17
    errors = {k: np.maximum(v, floor) for k, v in errors.items()}

    time = np.linspace(0.0, t_end, 401)
    exact_curve = cap / (1 + (cap / y0 - 1) * np.exp(-r * time))
    coarse_steps = 8
    coarse_t = np.linspace(0.0, t_end, coarse_steps + 1)
    coarse_y = [y0]
    for n in range(1, coarse_steps + 1):

        def rhs64(t, y):
            return r * y * (1.0 - y / cap)

        coarse_y.append(
            float(_rk4_fixed(rhs64, [y0], coarse_t[n], n, np.float64)[0])
        )

    fig, (ax_curve, ax_err) = plt.subplots(
        1, 2, figsize=(10.0, 4.6), gridspec_kw={"width_ratios": [0.9, 1.1]}
    )
    fig.subplots_adjust(bottom=0.34, top=0.9, wspace=0.36)

    ax_curve.plot(time, exact_curve, color=CHARCOAL, lw=2.4, label="Exact solution")
    ax_curve.plot(
        coarse_t,
        coarse_y,
        "o",
        color=GOLD_ACCENT,
        ms=7,
        label=f"RK4, {coarse_steps} steps (float64)",
    )
    ax_curve.set(xlabel="Time", ylabel="State, $y$", xlim=(0, t_end), ylim=(0, 1.05))
    ax_curve.set_title("(a) Problem with a known solution", loc="left", fontsize=14)
    ax_curve.grid(alpha=0.18)
    ax_curve.legend(loc="lower right", frameon=False, fontsize=11)

    ax_err.loglog(
        step_counts,
        errors[np.float64],
        "o-",
        color=TEAL_ENVIRON,
        lw=2.0,
        ms=5,
        label="float64",
    )
    ax_err.loglog(
        step_counts,
        errors[np.float32],
        "s--",
        color=RED,
        lw=2.0,
        ms=5,
        label="float32",
    )
    anchor = 3
    reference = (
        4.0 * errors[np.float64][anchor] * (step_counts / step_counts[anchor]) ** -4.0
    )
    ax_err.loglog(
        step_counts[: anchor + 7],
        reference[: anchor + 7],
        color=SLATE,
        lw=1.4,
        ls=":",
        label="Slope $-4$ (truncation)",
    )
    for dtype, color, name in (
        (np.float64, TEAL_ENVIRON, "float64"),
        (np.float32, RED, "float32"),
    ):
        ax_err.axhline(
            np.finfo(dtype).eps,
            color=color,
            lw=0.9,
            ls="-.",
            alpha=0.7,
            label=f"Machine epsilon, {name}",
        )
    ax_err.set(
        xlabel="Number of steps",
        ylabel="Absolute error at $t = 20$",
        ylim=(3e-18, 1.0),
    )
    ax_err.set_title("(b) Error against the exact value", loc="left", fontsize=14)
    ax_err.grid(alpha=0.18, which="both")
    ax_err.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=2,
        frameon=False,
        fontsize=10,
    )

    save(fig, "rk4_known_solution", "Truncation and round-off against a known solution")


def siwr_reservoir_speed():
    """Case curves of an SIWR model at one R0 under slow and fast reservoirs.

    Susceptible-infectious-reservoir dynamics: infection comes directly from
    infectious hosts (reproduction number R_d) and from a shared environmental
    reservoir W fed by shedding and lost at rate delta (R_w). At a fixed total
    R0 = R_d + R_w, the share carried by the reservoir changes the epidemic
    curve only when the reservoir turns over slowly relative to the epidemic.
    When it turns over quickly, the curves coincide and case counts alone
    cannot separate the two routes. Parameters are assumed, not fitted.
    """
    gamma, r0, horizon, dt = 0.2, 2.5, 120.0, 0.02
    i0 = 1e-4
    shares = ((0.0, SLATE, "-"), (0.5, TEAL_ENVIRON, "--"), (0.9, RED, ":"))
    deltas = ((0.05, "(a) Slow reservoir, decay 0.05 per day"), (5.0, "(b) Fast reservoir, decay 5 per day"))
    steps = int(round(horizon / dt))
    time = np.linspace(0.0, horizon, steps + 1)

    def incidence(share, delta):
        bd = r0 * (1 - share) * gamma
        bw = r0 * share * gamma * delta

        def rhs(t, y):
            s, i, w = y
            force = bd * i + bw * w
            return np.array([-force * s, force * s - gamma * i, i - delta * w])

        y = np.array([1 - i0, i0, i0 / delta])
        out = np.empty(steps + 1)
        out[0] = (bd * y[1] + bw * y[2]) * y[0]
        for n in range(steps):
            k1 = rhs(0, y)
            k2 = rhs(0, y + 0.5 * dt * k1)
            k3 = rhs(0, y + 0.5 * dt * k2)
            k4 = rhs(0, y + dt * k3)
            y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            out[n + 1] = (bd * y[1] + bw * y[2]) * y[0]
        return out * 1000.0

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.6), sharey=True)
    fig.subplots_adjust(bottom=0.16, top=0.9, wspace=0.12)
    for ax, (delta, title) in zip(axes, deltas, strict=True):
        for share, color, ls in shares:
            ax.plot(
                time,
                incidence(share, delta),
                color=color,
                lw=2.3,
                ls=ls,
                label=f"Reservoir share of $R_0$: {share:.0%}",
            )
        ax.set(xlabel="Days", xlim=(0, horizon))
        ax.set_title(title, loc="left", fontsize=14)
        ax.grid(alpha=0.18)
    axes[0].set(ylabel="New infections per day\nper 1000 hosts")
    axes[0].legend(loc="upper right", frameon=False, fontsize=11)
    save(fig, "siwr_reservoir_speed", "One reproduction number, two transmission routes")


def record_type_precision():
    """Precision of a growth-rate estimate from two kinds of record.

    Infections grow as i0 exp(r t). An environmental signal is incidence
    convolved with a shedding kernel and observed with log-normal noise every
    two days, so its logarithm is linear in time and the least-squares slope
    has the usual regression variance. Reported counts are Poisson with mean
    rho * i0 * exp(r t) each day, and the large-sample variance of the
    Poisson-regression slope follows from its information matrix. Panel (b)
    compares the two standard errors as the record lengthens; circles check the
    environmental closed form by simulation. Parameters are assumed.
    """
    rng = np.random.default_rng(2026)
    i0, r, sigma_env, step_env = 50.0, 0.08, 0.5, 2.0
    days_grid = np.arange(10, 61)
    days_grid_env = np.arange(10, 61, 2)
    rho_levels = ((0.1, "Counts, 10% reported", BLUE_HEALTH, "-"), (0.01, "Counts, 1% reported", BLUE_HEALTH, "--"), (0.001, "Counts, 0.1% reported", BLUE_HEALTH, ":"))

    def se_env(days):
        ts = np.arange(0.0, days + 1e-9, step_env)
        return sigma_env / np.sqrt(np.sum((ts - ts.mean()) ** 2))

    def se_counts(rho, days):
        ts = np.arange(0.0, days + 1e-9, 1.0)
        mu = rho * i0 * np.exp(r * ts)
        design = np.column_stack([np.ones_like(ts), ts - ts.mean()])
        info = design.T @ (design * mu[:, None])
        return np.sqrt(np.linalg.inv(info)[1, 1])

    # Simulation check of the environmental closed form (ordinary least squares).
    check_days = np.array([14, 21, 28, 42, 56])
    check_sd = []
    for days in check_days:
        ts = np.arange(0.0, days + 1e-9, step_env)
        design = np.column_stack([np.ones_like(ts), ts])
        logs = np.log(i0) + r * ts + sigma_env * rng.standard_normal((800, ts.size))
        slopes = np.linalg.lstsq(design, logs.T, rcond=None)[0][1]
        check_sd.append(slopes.std(ddof=1))

    # One realization of each record over 42 days.
    show_days = 42
    t_daily = np.arange(0.0, show_days + 1e-9, 1.0)
    tau = np.arange(0.0, 30.0)
    kernel = tau * np.exp(-tau / 2.5)
    kernel /= kernel.sum()
    t_env = np.arange(0.0, show_days + 1e-9, step_env)
    signal = np.array(
        [np.sum(kernel * i0 * np.exp(r * (t - tau))) for t in t_env]
    ) * np.exp(sigma_env * rng.standard_normal(t_env.size))
    counts = rng.poisson(0.01 * i0 * np.exp(r * t_daily))

    fig, (ax_rec, ax_se) = plt.subplots(1, 2, figsize=(10.0, 4.6))
    fig.subplots_adjust(bottom=0.34, top=0.9, wspace=0.3)
    ax_rec.semilogy(
        t_daily,
        i0 * np.exp(r * t_daily),
        color=CHARCOAL,
        lw=2.0,
        label="Infections per day (unobserved)",
    )
    ax_rec.semilogy(
        t_env,
        signal,
        "o",
        color=TEAL_ENVIRON,
        ms=5,
        label="Environmental signal, every 2 days",
    )
    ax_rec.semilogy(
        t_daily[counts > 0],
        counts[counts > 0],
        "s",
        color=BLUE_HEALTH,
        ms=4,
        label="Reported counts, 1% reported",
    )
    ax_rec.set(
        xlabel="Days",
        ylabel="Record value (log scale)",
        xlim=(0, show_days),
        ylim=(0.7, 3e4),
    )
    ax_rec.set_title("(a) Two records of one epidemic", loc="left", fontsize=14)
    ax_rec.grid(alpha=0.18, which="both")
    ax_rec.legend(loc="upper left", frameon=False, fontsize=10)

    ax_se.semilogy(
        days_grid_env,
        [se_env(d) for d in days_grid_env],
        color=TEAL_ENVIRON,
        lw=2.4,
        label="Environmental (closed form)",
    )
    ax_se.semilogy(
        check_days,
        check_sd,
        "o",
        color=TEAL_ENVIRON,
        ms=7,
        mfc=WHITE,
        label="Environmental (800 simulations)",
    )
    for rho, label, color, ls in rho_levels:
        ax_se.semilogy(
            days_grid,
            [se_counts(rho, d) for d in days_grid],
            color=color,
            lw=2.0,
            ls=ls,
            label=label,
        )
    ax_se.set(
        xlabel="Days of data",
        ylabel="SE of the growth rate (per day)",
        xlim=(days_grid[0], days_grid[-1]),
    )
    ax_se.set_title("(b) Precision as the record lengthens", loc="left", fontsize=14)
    ax_se.grid(alpha=0.18, which="both")
    ax_se.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=2,
        frameon=False,
        fontsize=10,
    )
    save(fig, "record_type_precision", "Growth-rate precision from two kinds of record")


if __name__ == "__main__":
    optimal_design()
    structural_fidelity()
    npzd_hysteresis()
    rk4_known_solution()
    siwr_reservoir_speed()
    record_type_precision()
