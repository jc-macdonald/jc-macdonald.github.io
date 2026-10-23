"""Render the two explicitly illustrative numerical figures.

Use build_figures.py to regenerate all formats and annotate the SVGs. Architecture
and method schematics are maintained as TikZ sources in tikz/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from palette import BLUE_HEALTH, CHARCOAL, GOLD_ACCENT, SLATE, TEAL_PRIMARY, WHITE

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
