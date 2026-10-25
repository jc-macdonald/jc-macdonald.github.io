"""Render the numerical research figures.

Two figures are explicitly constructed illustrations. ``npzd_hysteresis`` is
recomputed from the published equations of the rescaled NPZD model (Macdonald
and Gulbudak 2023), with parameters from its table and bifurcation-figure
caption; it is not copied from the paper, and its threshold and fold values
belong to this recomputation.
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


def npzd_hysteresis():
    """Equilibrium phytoplankton against the maximum harmful effect alpha."""
    q = NPZD
    p0 = q["theta"] / (q["k"] + q["theta"]) / q["eps"]
    p_hat = q["c"] * (1 - 1 / p0)
    alpha_star = _grazing(p_hat) * (q["xi"] + p_hat) / p_hat
    alpha_max = 3.0

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

    fig, ax = plt.subplots(figsize=(7.0, 5.5))
    fig.subplots_adjust(bottom=0.25, top=0.85)
    ax.axvspan(
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
        ax.plot(
            alpha_branch[start : stop + (0 if stop == len(stable) else 1)],
            p_branch[start : stop + (0 if stop == len(stable) else 1)],
            color=TEAL_ENVIRON if is_stable else SLATE,
            lw=2.6 if is_stable else 1.8,
            ls="-" if is_stable else "--",
            label=None if key in labelled else key,
        )
        labelled.add(key)
    ax.plot(
        [alpha_star, alpha_max],
        [p_hat, p_hat],
        color=CHARCOAL,
        lw=2.6,
        label="No zooplankton, stable",
    )
    ax.plot(
        [0, alpha_star],
        [p_hat, p_hat],
        color=CHARCOAL,
        lw=1.6,
        ls=":",
        label="No zooplankton, unstable",
    )
    ax.axvline(alpha_star, color=SLATE, lw=1.0, ls="-.")
    ax.annotate(
        "No zooplankton",
        (alpha_max - 0.04, p_hat),
        xytext=(0, 7),
        textcoords="offset points",
        ha="right",
        fontsize=9.5,
        color=CHARCOAL,
    )
    ax.annotate(
        r"$\mathcal{P}_0^z = 1$",
        (alpha_star, 0.4),
        xytext=(6, 0),
        textcoords="offset points",
        fontsize=12,
        color=SLATE,
    )
    ax.set(
        xlabel=r"Maximum harmful effect of phytoplankton, $\tilde{\alpha}$",
        ylabel="Phytoplankton at equilibrium, $p$",
        xlim=(0, alpha_max),
        ylim=(0, 8.2),
    )
    ax.set_title(
        "Forward hysteresis in an NPZD model", loc="left", pad=20, fontsize=18
    )
    ax.grid(alpha=0.18)
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.0, 0.8),
        frameon=False,
        fontsize=10,
    )
    fig.text(
        0.02,
        0.02,
        "Recomputed from the rescaled NPZD model of Macdonald and Gulbudak (2023),\n"
        "with parameters from its table and bifurcation-figure caption\n"
        r"($\xi = 10$, $a = 0.4$, $\theta = 12$, $\tilde{\gamma} = 0.29$, $\tilde{\epsilon} = 0.3$). "
        "Solid: locally stable; dashed or dotted: unstable.",
        fontsize=10,
        color=SLATE,
        va="bottom",
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


if __name__ == "__main__":
    optimal_design()
    structural_fidelity()
    npzd_hysteresis()
